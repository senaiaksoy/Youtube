#!/usr/bin/env node
// Template library: contact sheets for eye review. One row per world.
//   node sheet.mjs <out.png> --kinds claim,figure,verdict [--worlds a,b] [--shorts] [--at 6.5] [--jobs 4]
import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const lib = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const catalog = JSON.parse(fs.readFileSync(path.join(lib, 'templates.json'), 'utf8'));
const args = process.argv.slice(2);
const opt = (n, d) => { const i = args.indexOf(`--${n}`); return i >= 0 ? args[i + 1] : d; };
const out = path.resolve(args.find((a) => a.endsWith('.png')));
const kinds = opt('kinds', 'claim,figure,verdict').split(',');
const worlds = opt('worlds', Object.entries(catalog.templates).filter(([, t]) => t.engine === 'kit').map(([k]) => k).join(',')).split(',');
const shorts = args.includes('--shorts'); const at = opt('at', '6.5'); const jobs = +opt('jobs', 4);
const run = (cmd, argv, cwd) => new Promise((res) => { const p = spawn(cmd, argv, { cwd, shell: cmd === 'npx', stdio: 'ignore', env: { ...process.env, HYPERFRAMES_SKIP_SKILLS: '1', GEMINI_API_KEY: '' } }); p.on('close', res); });
const tmp = path.join(lib, 'demos', '_frames', shorts ? 's' : 'l'); fs.mkdirSync(tmp, { recursive: true });
const queue = worlds.flatMap((w) => kinds.map((k) => [w, k])); const tiles = [];
await Promise.all(Array.from({ length: jobs }, async () => {
  while (queue.length) {
    const [w, k] = queue.shift(); const d = path.join(lib, 'demos', w, k, shorts ? 'shorts' : ''); const o = path.join(tmp, `${w}-${k}`);
    fs.rmSync(o, { recursive: true, force: true });
    await run('npx', ['-y', 'hyperframes@0.9.29', 'snapshot', '.', '--at', at, '--no-end', '-o', o, '--describe', 'false'], d);
    const f = fs.existsSync(o) ? fs.readdirSync(o).find((x) => x.endsWith('.png')) : null;
    tiles.push({ w, k, f: f ? path.join(o, f) : null });
  }
}));
const order = worlds.flatMap((w) => kinds.map((k) => tiles.find((t) => t.w === w && t.k === k)));
const missing = order.filter((t) => !t.f); if (missing.length) console.log('missing:', missing.map((t) => `${t.w}/${t.k}`).join(' '));
const W = shorts ? 270 : 640, H = shorts ? 480 : 360;
const inputs = order.filter((t) => t.f).flatMap((t) => ['-i', t.f]);
const n = order.filter((t) => t.f).length; const cols = kinds.length; const rows = Math.ceil(n / cols);
const chains = Array.from({ length: n }, (_, i) => `[${i}:v]scale=${W}:${H}[v${i}]`).join(';');
const layout = Array.from({ length: n }, (_, i) => `${(i % cols) * (W + 6)}_${Math.floor(i / cols) * (H + 6)}`).join('|');
const code = await run('ffmpeg', ['-y', '-v', 'error', ...inputs, '-filter_complex', `${chains};${Array.from({ length: n }, (_, i) => `[v${i}]`).join('')}xstack=inputs=${n}:layout=${layout}:fill=0x777777[o]`, '-map', '[o]', '-frames:v', '1', out], lib);
console.log(code === 0 ? `sheet → ${out} (${rows}×${cols})` : `ffmpeg failed (${code})`);
