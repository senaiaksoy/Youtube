#!/usr/bin/env node
// Outsider Inside — pop-up captions for Shorts (Dr. Aksoy, 2026-10-18: every Short carries burned pop-up captions;
// the 16:9 video never does).
//
//   node captions.mjs <words.json> <from_s> <to_s> <out.ass> [--size 62] [--max-words 3] [--max-chars 20]
//   ffmpeg -i short.mp4 -vf "ass=out.ass:fontsdir=<outsider-inside-frame>/assets/fonts" -c:v libx264 -crf 17 -c:a copy out.mp4
//
// words.json: the spoken words with times in SOURCE seconds — either [[word, start, end], …] (script-aligned list) or the
// transcriber's {segments:[{words:[{w,s,e}]}]}. <from_s>/<to_s> is the source range the Short was cut from; times are
// shifted so the Short starts at 0. Text is what Dr. Aksoy SAYS (check it against the recording; never rewrite it).
// Look: IBM Plex Sans SemiBold, ink #1B2230 on a paper box #F4F0E6, 1–3 words per card, 100 ms pop (scale 88→100 %),
// no bounce, no colour per word. Placed in the caption band just above the Shorts UI (box ≈ y 1494–1574 on 1080×1920);
// legibility.mjs keeps every Shorts scene's own text out of that band (76.5–82 % of the height).
import fs from 'node:fs';

const a = process.argv.slice(2);
const opt = (k, d) => { const i = a.indexOf(k); return i >= 0 ? Number(a[i + 1]) : d; };
const [src, from, to, out] = a.filter((x, i) => !x.startsWith('--') && !(i > 0 && a[i - 1].startsWith('--')));
if (!out) { console.log('usage: node captions.mjs <words.json> <from_s> <to_s> <out.ass> [--size 62] [--max-words 3] [--max-chars 20]'); process.exit(2); }
const SIZE = opt('--size', 62), MAXW = opt('--max-words', 3), MAXC = opt('--max-chars', 20);
const F = Number(from), T = Number(to);

let J = JSON.parse(fs.readFileSync(src, 'utf8'));
if (!Array.isArray(J)) J = J.segments.flatMap((s) => s.words.map((w) => [w.w, w.s, w.e]));
const clean = (w) => w.replace(/ /g, ' ').replace(/[«»]/g, '').trim().replace(/[,.;:…]+$/, '').trim();
const words = J.filter(([, s]) => s >= F - 0.05 && s < T - 0.05).map(([w, s, e]) => ({ raw: w, t: clean(w), s: s - F, e: e - F }))
  .filter((w) => /[\p{L}\p{N}]/u.test(w.t));

const chunks = []; let cur = [];
for (const w of words) {
  const txt = [...cur, w].map((x) => x.t).join(' ');
  if (cur.length && (cur.length >= MAXW || txt.length > MAXC || w.s - cur.at(-1).e > 0.45)) { chunks.push(cur); cur = []; }
  cur.push(w);
  if (/[.!?…,:;»]\s*$/.test(w.raw.replace(/ /g, ' '))) { chunks.push(cur); cur = []; }
}
if (cur.length) chunks.push(cur);

const ts = (x) => { let cs = Math.round(x * 100); const h = Math.floor(cs / 360000); cs -= h * 360000; const m = Math.floor(cs / 6000); cs -= m * 6000;
  const s = Math.floor(cs / 100); cs -= s * 100; return `${h}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}.${String(cs).padStart(2, '0')}`; };
const dur = T - F;
const lines = chunks.map((c, k) => {
  const txt = c.map((x) => x.t).join(' ').replace(/\s+/g, ' ').replace(/ ([?!])/g, ' $1');
  const s = c[0].s; let e = k + 1 < chunks.length ? chunks[k + 1][0].s : c.at(-1).e + 0.4;
  e = Math.min(e, c.at(-1).e + 0.6, dur); if (e - s < 0.25) e = s + 0.25;
  return `Dialogue: 0,${ts(s)},${ts(e)},Pop,,0,0,0,,{\\fad(40,0)\\fscx88\\fscy88\\t(0,100,\\fscx100\\fscy100)}${txt}`;
});
const head = `[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Pop,IBM Plex Sans SemiBold,${SIZE},&H0030221B,&H0030221B,&H00E6F0F4,&H00E6F0F4,0,0,0,0,100,100,0,0,3,16,0,2,110,120,352,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
`;
fs.writeFileSync(out, head + lines.join('\n') + '\n');
console.log(`${out}: ${lines.length} caption cards over ${dur.toFixed(1)} s — read them against the recording before publishing`);
