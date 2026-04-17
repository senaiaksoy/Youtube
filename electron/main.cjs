const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

const PORT = Number(process.env.DESKTOP_PORT || 3000);

function nextBin() {
  if (process.platform === 'win32') return path.join(process.cwd(), 'node_modules', '.bin', 'next.cmd');
  return path.join(process.cwd(), 'node_modules', '.bin', 'next');
}

function tokensFilePath() {
  return path.join(app.getPath('userData'), 'google-tokens.json');
}

function legacyFilePath() {
  return path.join(app.getPath('userData'), 'auth-secrets.json');
}

function startNext() {
  const isDev = process.env.NODE_ENV !== 'production';
  const bin = nextBin();
  const args = isDev ? ['dev', '-p', String(PORT)] : ['start', '-p', String(PORT)];

  const child = spawn(`"${bin}"`, args, {
    stdio: 'inherit',
    shell: true,
    env: {
      ...process.env,
      YOUTUBE_TOKENS_FILE: process.env.YOUTUBE_TOKENS_FILE || tokensFilePath(),
      YOUTUBE_LEGACY_FILE: process.env.YOUTUBE_LEGACY_FILE || legacyFilePath(),
      NEXTAUTH_URL: process.env.NEXTAUTH_URL || `http://localhost:${PORT}`,
    },
  });

  child.on('exit', () => {
    if (!app.isQuitting) app.quit();
  });

  return child;
}

async function waitForNext(url) {
  const waitOn = require('wait-on');
  await waitOn({ resources: [url], timeout: 120000 });
}

function createWindow(url) {
  const win = new BrowserWindow({
    width: 1400,
    height: 900,
    webPreferences: {
      preload: path.join(__dirname, 'preload.cjs'),
    },
  });

  win.loadURL(url);
}

let nextProcess;

app.whenReady().then(async () => {
  nextProcess = startNext();
  const url = `http://localhost:${PORT}`;
  await waitForNext(url);
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
