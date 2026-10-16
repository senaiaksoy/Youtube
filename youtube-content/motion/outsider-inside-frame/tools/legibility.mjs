#!/usr/bin/env node
// Outsider Inside — phone legibility check for HyperFrames scenes.
//
// Opens the composition in HyperFrames' own Chrome, seeks the timeline to many points,
// and measures the rendered size of every visible piece of text (transforms included).
// Fails when any visible text is smaller than the phone floor.
//
//   node legibility.mjs <project-dir> [--min 40] [--samples 24] [--html index.html]
//
// Floor: 40 px at 1080 px on the short side of the frame (2.1cqw on 1920×1080), scaled for
// other sizes. On a 6" phone held sideways that is ≈1.3 mm x-height — the smallest size that
// stays readable at arm's length. Elements may opt out only with data-legibility-exempt="reason"
// (e.g. text that is part of real footage); every exemption is printed.
// No dependencies; Node 22+ (global WebSocket). Chrome path from `npx hyperframes browser path`.

import fs from 'node:fs';
import http from 'node:http';
import path from 'node:path';
import { spawn, execSync } from 'node:child_process';
import net from 'node:net';

const args = process.argv.slice(2);
const opt = (n, d) => { const i = args.indexOf(`--${n}`); return i >= 0 ? args[i + 1] : d; };
const project = path.resolve(args.find((a) => !a.startsWith('--') && !/^\d/.test(a)) || '.');
const htmlName = opt('html', 'index.html');
const samples = +opt('samples', 24);
const floor1080 = +opt('min', 40);
if (!fs.existsSync(path.join(project, htmlName))) { console.error(`✖ missing ${path.join(project, htmlName)}`); process.exit(2); }

const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css', '.png': 'image/png',
  '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.woff': 'font/woff',
  '.json': 'application/json', '.wav': 'audio/wav', '.mp3': 'audio/mpeg', '.mp4': 'video/mp4', '.webm': 'video/webm' };
const server = http.createServer((req, res) => {
  const p = path.join(project, decodeURIComponent(new URL(req.url, 'http://x').pathname));
  if (!p.startsWith(project) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': MIME[path.extname(p).toLowerCase()] || 'application/octet-stream' });
  fs.createReadStream(p).pipe(res);
});
const freePort = () => new Promise((r) => { const s = net.createServer(); s.listen(0, () => { const p = s.address().port; s.close(() => r(p)); }); });

function chromePath() {
  if (process.env.HF_CHROME) return process.env.HF_CHROME;
  const out = execSync('npx -y hyperframes browser path', { encoding: 'utf8', env: { ...process.env, HYPERFRAMES_SKIP_SKILLS: '1' } });
  return out.trim().split(/\r?\n/).filter(Boolean).at(-1);
}

async function main() {
  const httpPort = await freePort(); await new Promise((r) => server.listen(httpPort, '127.0.0.1', r));
  const cdpPort = await freePort();
  const chrome = spawn(chromePath(), ['--headless', `--remote-debugging-port=${cdpPort}`, '--no-sandbox', '--hide-scrollbars',
    '--window-size=1920,1080', '--force-device-scale-factor=1', 'about:blank'], { stdio: 'ignore' });
  let ws; try {
    let target; for (let i = 0; i < 200 && !target; i++) { // cold Chrome start can take ~15 s
      try { target = (await (await fetch(`http://127.0.0.1:${cdpPort}/json/list`)).json()).find((t) => t.type === 'page'); } catch {}
      if (!target) await new Promise((r) => setTimeout(r, 200));
    }
    if (!target) throw new Error('Chrome did not start');
    ws = new WebSocket(target.webSocketDebuggerUrl); await new Promise((r, j) => { ws.onopen = r; ws.onerror = j; });
    let id = 0; const pending = new Map(); const events = [];
    ws.onmessage = (m) => { const d = JSON.parse(m.data); if (d.id && pending.has(d.id)) { pending.get(d.id)(d); pending.delete(d.id); } else events.push(d); };
    const send = (method, params = {}) => new Promise((r) => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
    const evaluate = async (expr) => { const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true });
      if (r.result?.exceptionDetails) throw new Error(r.result.exceptionDetails.exception?.description || 'eval error'); return r.result?.result?.value; };

    await send('Page.enable');
    await send('Page.navigate', { url: `http://127.0.0.1:${httpPort}/${htmlName}` });
    for (let i = 0; i < 100; i++) { if (await evaluate('document.readyState') === 'complete') break; await new Promise((r) => setTimeout(r, 100)); }
    const meta = await evaluate(`(async () => {
      await document.fonts.ready;
      const root = document.querySelector('[data-composition-id]') || document.body;
      const W = +root.getAttribute('data-width') || innerWidth, H = +root.getAttribute('data-height') || innerHeight;
      const tls = window.__timelines || {}; const tl = tls[root.getAttribute('data-composition-id')] || Object.values(tls)[0];
      return { W, H, dur: tl ? tl.duration() : +root.getAttribute('data-duration') || 0, hasTl: !!tl };
    })()`);
    const floor = floor1080 * Math.min(meta.W, meta.H) / 1080;
    const times = [...Array(samples + 1).keys()].map((i) => +(meta.dur * i / samples).toFixed(3));
    const found = new Map(); const exempt = new Map();
    for (const t of times) {
      const rows = await evaluate(`(async () => {
        const root = document.querySelector('[data-composition-id]') || document.body;
        const tls = window.__timelines || {}; const tl = tls[root.getAttribute('data-composition-id')] || Object.values(tls)[0];
        if (tl) tl.seek(${t}, false);
        await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
        const out = []; const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        const sel = (el) => el.id ? '#' + el.id : el.tagName.toLowerCase() + (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\\s+/).join('.') : '');
        for (let n; (n = walker.nextNode());) {
          const txt = n.textContent.replace(/\\s+/g, ' ').trim(); if (!txt || !/[\\p{L}\\p{N}]/u.test(txt)) continue;
          const el = n.parentElement; if (!el || el.closest('script,style,title,head')) continue;
          let op = 1, hidden = false;
          for (let e = el; e && e !== document.documentElement; e = e.parentElement) {
            const cs = getComputedStyle(e); if (cs.display === 'none' || cs.visibility === 'hidden') { hidden = true; break; } op *= +cs.opacity;
          }
          if (hidden || op < 0.05) continue;
          const range = document.createRange(); range.selectNodeContents(n); const rects = [...range.getClientRects()].filter((r) => r.width > 0 && r.height > 0);
          if (!rects.length) continue;
          const r = rects[0]; if (r.right < 0 || r.bottom < 0 || r.left > innerWidth || r.top > innerHeight) continue;
          const cs = getComputedStyle(el); const fs = parseFloat(cs.fontSize);
          // rendered scale from all ancestor transforms: on-screen box / untransformed layout box
          // (rotation only enlarges the box, so the ratio is capped at 1; scale-down shrinks it)
          const bb = el.getBoundingClientRect();
          const sx = el.offsetWidth ? bb.width / el.offsetWidth : 1, sy = el.offsetHeight ? bb.height / el.offsetHeight : 1;
          const px = fs * Math.min(1, Math.max(Math.min(sx, sy), 0));
          const ex = el.closest('[data-legibility-exempt]');
          out.push({ txt: txt.slice(0, 60), sel: sel(el), px: Math.round(px * 10) / 10, fs, exempt: ex ? ex.getAttribute('data-legibility-exempt') : null });
        }
        return out;
      })()`);
      for (const r of rows) {
        const key = r.sel + '|' + r.txt; const tgt = r.exempt ? exempt : found;
        const prev = tgt.get(key); if (!prev || r.px < prev.px) tgt.set(key, { ...r, t });
      }
    }
    const all = [...found.values()].sort((a, b) => a.px - b.px);
    const bad = all.filter((r) => r.px + 0.5 < floor);
    console.log(`frame ${meta.W}×${meta.H} · phone floor ${floor.toFixed(0)} px · ${times.length} samples over ${meta.dur}s · ${all.length} text runs`);
    for (const r of all) console.log(`${r.px + 0.5 < floor ? '✖' : '✔'} ${String(r.px).padStart(6)} px  ${r.sel.padEnd(28)} "${r.txt}"${r.px + 0.5 < floor ? `  (smallest at ${r.t}s)` : ''}`);
    for (const r of exempt.values()) console.log(`· exempt (${r.exempt}): ${r.px} px "${r.txt}"`);
    console.log(bad.length ? `\nlegibility FAILED: ${bad.length} text run(s) below ${floor.toFixed(0)} px` : `\nlegibility passed — every visible text ≥ ${floor.toFixed(0)} px`);
    process.exitCode = bad.length ? 1 : 0;
  } finally { try { ws?.close(); } catch {} chrome.kill(); server.close(); }
}
main().catch((e) => { console.error(`✖ ${e.message}`); process.exit(2); });
