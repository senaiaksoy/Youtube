#!/usr/bin/env node
// Outsider Inside — per-video variation of Dr. Aksoy's REAL pen marks, stamps and pen foley.
//
//   node pen.mjs apply <scene> [<scene> …] [--look <look.json>] [--seed N]
//   node pen.mjs show  <scene> [<scene> …]                         (prints what apply would choose, writes nothing)
//
// Nothing is drawn by code: every mark is one of the strokes Dr. Aksoy drew (assets/pen/pen-library.json).
// The seed only decides WHICH real stroke a slot gets and how it sits on the page:
//   <img class="pen …" src="assets/pen/<default>.png" data-pen="strike|underline|loop|arrow|question" [data-pen-tool="round|chisel"]
//        [data-pen-fixed="oval-01"] …>   — the pool is: same type + tool + a shape close to the default src (aspect ±30 %)
//     → src + data-pen-id + data-pen-flip + style vars --pen-rot / --pen-sy / --pen-fx / --pen-warp
//       (assets/pen/pen.css turns those into CSS rotate / scale / an SVG displacement that bends the stroke slightly)
//   <div class="stamp" data-stamp …>   → --stamp-rot (± 4°; the scene's .stamp transform must use it:
//                                          rotate(calc(-6deg + var(--stamp-rot, 0deg)))) + data-stamp-var a|b (mask mirrored)
//   <audio data-sfx="pen|stamp|ink-tap" …> → src from assets/sfx, never the same file twice in a row
//   <html data-ink-seed>                  → seed for the black-ink diagram lines drawn by assets/ink/ink.js (rough.js)
//
// Seed: look.json "seed"; when absent it is derived from the video's folder name and written back, so a re-render
// of the same video is identical and the next video differs. Scenes are processed in the order given, so pass
// all scenes of one video in running order: a mark id is never used twice in a row within the video.
// The chosen ids are written to look.json "pen_marks" (+ "stamp_flip"); if that set equals the previous video's
// (look-log.json) the seed is advanced until it differs — the variety gate then passes on pen marks by construction.
// Run BEFORE facts.mjs apply / aspect.mjs (the Shorts twin copies the result).
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const T = path.resolve(here, '..');
const library = JSON.parse(fs.readFileSync(path.join(T, 'assets/pen/pen-library.json'), 'utf8'));
const logPath = process.env.LOOK_LOG || path.resolve(T, '..', 'look-log.json');
const args = process.argv.slice(2);
const cmd = args[0];
const opt = (k) => { const i = args.indexOf(k); return i > 0 ? args[i + 1] : undefined; };
const scenes = args.slice(1).filter((a, i, all) => !a.startsWith('--') && !(i > 0 && all[i - 1].startsWith('--')));
if (!['apply', 'show'].includes(cmd) || !scenes.length) {
  console.log('usage: node pen.mjs apply|show <scene> [<scene> …] [--look <look.json>] [--seed N]'); process.exit(2);
}

// ---- deterministic randomness ----
const fnv = (s) => { let h = 0x811c9dc5; for (const c of Buffer.from(s, 'utf8')) { h ^= c; h = Math.imul(h, 0x01000193) >>> 0; } return h; };
const mulberry = (a) => () => { a = (a + 0x6d2b79f5) >>> 0; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };

// ---- look.json ----
function findLook(dir) {
  for (let d = path.resolve(dir); ; d = path.dirname(d)) {
    const f = path.join(d, 'look.json'); if (fs.existsSync(f)) return f;
    if (path.dirname(d) === d) return null;
  }
}
const lookPath = opt('--look') ? path.resolve(opt('--look')) : findLook(scenes[0]);
if (!lookPath) { console.error(`✖ no look.json in ${scenes[0]} or above — write it first (series, papers, layouts…)`); process.exit(2); }
const look = JSON.parse(fs.readFileSync(lookPath, 'utf8'));
const videoName = path.basename(path.dirname(lookPath));
let seed = Number(opt('--seed') ?? look.seed ?? fnv(videoName) % 100000);

// ---- per-type variation ranges (kept small: the stroke must still read as the same hand) ----
const V = {
  strike:    { rot: 3.0, sy: [0.8, 1.35], flipX: true,  flipY: true,  warp: 16 },
  underline: { rot: 3.0, sy: [0.8, 1.3], flipX: true,  flipY: false, warp: 12 },
  loop:      { rot: 12,  sy: [0.9, 1.1], flipX: true,  flipY: false, warp: 8 },
  arrow:     { rot: 4,   sy: [0.9, 1.1],  flipX: false, flipY: false, warp: 6 },
  question:  { rot: 5,   sy: [0.95, 1.05], flipX: false, flipY: false, warp: 0 },
};
const toolOf = (m) => (m.tool === 'marker-chisel' ? 'chisel' : 'round');
const sfxDir = path.join(T, 'assets/sfx');
const sfx = (kind) => fs.readdirSync(sfxDir).filter((f) => f.startsWith(kind + '-') && f.endsWith('.wav')).sort();

const attr = (tag, name) => { const m = tag.match(new RegExp(`\\s${name}="([^"]*)"`)); return m ? m[1] : undefined; };
const setAttr = (tag, name, val) => {
  const re = new RegExp(`\\s${name}="[^"]*"`);
  if (val === undefined) return tag.replace(re, '');
  return re.test(tag) ? tag.replace(re, ` ${name}="${val}"`) : tag.replace(/\s*(\/?)>$/, (m, s) => ` ${name}="${val}"${s ? ' /' : ''}>`);
};
const setVars = (tag, vars) => {
  let style = (attr(tag, 'style') || '').split(';').map((s) => s.trim()).filter((s) => s && !/^--(pen|stamp)-/.test(s));
  for (const [k, v] of Object.entries(vars)) style.push(`${k}:${v}`);
  return setAttr(tag, 'style', style.join(';'));
};
const r2 = (x) => Math.round(x * 100) / 100;

function plan(s) {
  const rnd = mulberry(s);
  const pick = (arr) => arr[Math.floor(rnd() * arr.length)];
  const lastByType = {}; const lastSfx = {}; const used = []; let stampFlip = false; let warpN = 0;
  const out = [];
  for (const dir of scenes) {
    const file = path.join(path.resolve(dir), 'index.html');
    let html = fs.readFileSync(file, 'utf8');
    const warps = [];
    // rough.js ink lines (assets/ink/ink.js) take their seed from <html data-ink-seed>
    html = html.replace(/<html\b([^>]*)>/, (m, a) => `<html${a.replace(/\s*data-ink-seed="[^"]*"/, '')} data-ink-seed="${(s % 100000) + 7 * out.length + 1}">`);
    html = html.replace(/<img\b[^>]*\bdata-pen="[^"]*"[^>]*>/g, (tag) => {
      const type = attr(tag, 'data-pen'); const v = V[type];
      if (!v) throw new Error(`${file}: unknown data-pen="${type}" (${Object.keys(V).join(', ')})`);
      const tool = attr(tag, 'data-pen-tool') || 'round';
      const fixed = attr(tag, 'data-pen-fixed');
      // same type + tool, and a similar shape to the scene's default stroke (an oval slot never gets a round loop)
      const base = library.find((x) => `assets/pen/${x.file}` === attr(tag, 'src'));
      const ar = (x) => x.width / x.height;
      let pool = library.filter((m) => m.type === type && toolOf(m) === tool && (!base || Math.abs(ar(m) / ar(base) - 1) < 0.3));
      if (!pool.length) throw new Error(`${file}: no ${tool} ${type} in pen-library.json`);
      const m = fixed ? library.find((x) => x.id === fixed) : (() => {
        const fresh = pool.filter((x) => x.id !== lastByType[type]);
        return pick(fresh.length ? fresh : pool);
      })();
      if (!m) throw new Error(`${file}: data-pen-fixed="${fixed}" not in pen-library.json`);
      lastByType[type] = m.id; used.push(m.id);
      const fx = v.flipX && rnd() < 0.5, fy = v.flipY && rnd() < 0.5;
      const vars = { '--pen-rot': `${r2((rnd() * 2 - 1) * v.rot)}deg`, '--pen-sy': r2((v.sy[0] + rnd() * (v.sy[1] - v.sy[0])) * (fy ? -1 : 1)), '--pen-fx': fx ? -1 : 1 };
      if (v.warp) { const id = `pen-warp-${++warpN}`; warps.push({ id, seed: 1 + Math.floor(rnd() * 997), scale: v.warp, type }); vars['--pen-warp'] = `url(#${id})`; }
      let t = setAttr(tag, 'src', `assets/pen/${m.file}`);
      t = setAttr(t, 'data-pen-id', m.id); t = setAttr(t, 'data-pen-flip', [fx && 'x', fy && 'y'].filter(Boolean).join(' ') || undefined);
      return setVars(t, vars);
    });
    html = html.replace(/<div\b[^>]*\bdata-stamp\b[^>]*>/g, (tag) => {
      const variant = rnd() < 0.5 ? 'b' : 'a'; if (variant === 'b') stampFlip = true;
      return setVars(setAttr(tag, 'data-stamp-var', variant), { '--stamp-rot': `${r2((rnd() * 2 - 1) * 4)}deg` });
    });
    html = html.replace(/<audio\b[^>]*\bdata-sfx="([^"]*)"[^>]*>/g, (tag, kind) => {
      const files = sfx(kind); if (!files.length) throw new Error(`${file}: no assets/sfx/${kind}-*.wav`);
      const fresh = files.filter((f) => f !== lastSfx[kind]); const f = pick(fresh.length ? fresh : files);
      lastSfx[kind] = f; return setAttr(tag, 'src', `assets/sfx/${f}`);
    });
    // one hidden <svg> of displacement filters per scene (bends each stroke a little; static, seek-safe)
    html = html.replace(/\n?\s*<svg id="pen-warp-defs"[\s\S]*?<\/svg>/, '');
    if (warps.length) {
      const defs = warps.map((w) => `<filter id="${w.id}" x="-6%" y="-40%" width="112%" height="180%"><feTurbulence type="fractalNoise" baseFrequency="${w.type === 'loop' ? '0.006' : '0.0035 0.02'}" numOctaves="1" seed="${w.seed}" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="${w.scale}" xChannelSelector="R" yChannelSelector="G"/></filter>`).join('');
      const svg = `<svg id="pen-warp-defs" width="0" height="0" style="position:absolute" aria-hidden="true"><defs>${defs}</defs></svg>`;
      html = html.replace(/(<div id="root"[^>]*>)/, `$1\n      ${svg}`);
      if (!html.includes('id="pen-warp-defs"')) throw new Error(`${file}: no <div id="root"> to hold the warp filters`);
    }
    out.push({ file, html });
  }
  return { out, used, stampFlip };
}

const readLog = () => (fs.existsSync(logPath) ? JSON.parse(fs.readFileSync(logPath, 'utf8')) : []);
const prev = readLog().filter((e) => e.project !== videoName && !String(e.project).endsWith('-shorts')).at(-1);
const same = (a = [], b = []) => a.length === b.length && [...a].sort().join('|') === [...b].sort().join('|');
let res; let tries = 0;
for (;;) {
  res = plan(seed);
  if (!prev || !res.used.length || !same([...new Set(res.used)], prev.pen_marks) || tries >= 20) break;
  seed += 1; tries++;
}
const set = [...new Set(res.used)];
console.log(`pen · ${videoName} · seed ${seed}${tries ? ` (advanced ${tries}× to differ from ${prev.project})` : ''} · ${set.join(', ') || 'no data-pen marks'}${res.stampFlip ? ' · stamp mask b' : ''}`);
if (cmd === 'apply') {
  for (const { file, html } of res.out) fs.writeFileSync(file, html);
  Object.assign(look, { seed, pen_marks: set, stamp_flip: res.stampFlip });
  fs.writeFileSync(lookPath, JSON.stringify(look, null, 2) + '\n');
  console.log(`wrote ${res.out.length} scene(s) + ${path.relative(process.cwd(), lookPath)}`);
}
