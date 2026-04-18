/**
 * After `next build` with output: 'standalone', copy static assets
 * and public folder into the standalone directory so the server
 * can serve them correctly.
 */
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const standaloneDir = path.join(root, '.next', 'standalone');

function copyDir(src, dest) {
  if (!fs.existsSync(src)) {
    console.warn(`⚠ Source not found, skipping: ${src}`);
    return;
  }
  fs.mkdirSync(dest, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

// 1. Copy .next/static → standalone/.next/static
const staticSrc = path.join(root, '.next', 'static');
const staticDest = path.join(standaloneDir, '.next', 'static');
console.log('📁 Copying .next/static...');
copyDir(staticSrc, staticDest);

// 2. Copy public → standalone/public
const publicSrc = path.join(root, 'public');
const publicDest = path.join(standaloneDir, 'public');
console.log('📁 Copying public/...');
copyDir(publicSrc, publicDest);

// 3. Copy .env if exists
const envSrc = path.join(root, '.env');
const envDest = path.join(standaloneDir, '.env');
if (fs.existsSync(envSrc)) {
  console.log('📁 Copying .env...');
  fs.copyFileSync(envSrc, envDest);
}

console.log('✅ Standalone build ready.');
