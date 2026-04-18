const { app, BrowserWindow } = require('electron');
const path = require('path');
const fs = require('fs');
const { spawn, fork } = require('child_process');
const http = require('http');

const isDev = !app.isPackaged;
const PORT = Number(process.env.DESKTOP_PORT || 3000);

// --------------- paths ---------------

function getResourcePath() {
  if (isDev) return process.cwd();
  return path.join(process.resourcesPath, 'app-resources');
}

function tokensFilePath() {
  return path.join(app.getPath('userData'), 'google-tokens.json');
}

function legacyFilePath() {
  return path.join(app.getPath('userData'), 'auth-secrets.json');
}

// --------------- .env loader (no deps) ---------------

function loadEnvFile(envPath) {
  if (!fs.existsSync(envPath)) return;
  const content = fs.readFileSync(envPath, 'utf-8');
  for (const line of content.split('\n')) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const eqIdx = trimmed.indexOf('=');
    if (eqIdx === -1) continue;
    const key = trimmed.slice(0, eqIdx).trim();
    const value = trimmed.slice(eqIdx + 1).trim();
    if (!process.env[key]) process.env[key] = value;
  }
}

function setupEnv() {
  // Load .env from multiple possible locations
  loadEnvFile(path.join(app.getPath('userData'), '.env'));
  loadEnvFile(path.join(getResourcePath(), '.env'));
  if (isDev) loadEnvFile(path.join(process.cwd(), '.env'));

  process.env.YOUTUBE_TOKENS_FILE = process.env.YOUTUBE_TOKENS_FILE || tokensFilePath();
  process.env.YOUTUBE_LEGACY_FILE = process.env.YOUTUBE_LEGACY_FILE || legacyFilePath();
  process.env.NEXTAUTH_URL = process.env.NEXTAUTH_URL || `http://localhost:${PORT}`;
  process.env.PORT = String(PORT);
}

// --------------- Next.js server ---------------

let nextProcess;

function startNextDev() {
  const bin = path.join(process.cwd(), 'node_modules', '.bin',
    process.platform === 'win32' ? 'next.cmd' : 'next');

  nextProcess = spawn(`"${bin}"`, ['dev', '-p', String(PORT)], {
    stdio: 'inherit',
    shell: true,
    env: process.env,
    cwd: process.cwd(),
  });

  nextProcess.on('exit', () => {
    if (!app.isQuitting) app.quit();
  });
}

function startNextProd() {
  const resPath = getResourcePath();
  const serverJs = path.join(resPath, 'server.js');

  nextProcess = fork(serverJs, [], {
    cwd: resPath,
    env: { ...process.env, PORT: String(PORT), HOSTNAME: 'localhost' },
    silent: false,
  });

  nextProcess.on('exit', () => {
    if (!app.isQuitting) app.quit();
  });
}

// --------------- wait for server (no external deps) ---------------

function waitForServer(url, timeout = 120000) {
  return new Promise((resolve, reject) => {
    const start = Date.now();
    const check = () => {
      if (Date.now() - start > timeout) return reject(new Error('Server timeout'));
      const req = http.get(url, () => { resolve(); });
      req.on('error', () => setTimeout(check, 500));
      req.setTimeout(2000, () => { req.destroy(); setTimeout(check, 500); });
    };
    check();
  });
}

// --------------- window ---------------

function createWindow(url) {
  const win = new BrowserWindow({
    width: 1400,
    height: 900,
    title: 'YouTube Manager',
    webPreferences: {
      preload: path.join(__dirname, 'preload.cjs'),
    },
  });
  win.loadURL(url);
}

// --------------- app lifecycle ---------------

app.whenReady().then(async () => {
  setupEnv();

  if (isDev) {
    startNextDev();
  } else {
    startNextProd();
  }

  const url = `http://localhost:${PORT}`;
  await waitForServer(url);
  createWindow(url);

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow(url);
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

app.on('before-quit', () => {
  app.isQuitting = true;
  if (nextProcess && !nextProcess.killed) nextProcess.kill();
});
