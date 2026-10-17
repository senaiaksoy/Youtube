#!/usr/bin/env node
// Outsider Inside — variety gate: keeps consecutive videos from looking the same.
//
//   node variety.mjs check  <project>   before render: validates <project>/look.json, compares with the log
//   node variety.mjs log    <project>   after the final render: appends the look to the log
//   node variety.mjs status             last videos + series / layouts not used lately
//
// look.json (project root):
//   { "series": "chiffres", "papers": ["kareli", "a4"], "first_graphic": "chiffre-B",
//     "layouts": ["chiffre-B", "promesse-A"], "pen_marks": ["oval-01", "strike-02"], "stamp_flip": false }
// Log: youtube-content/motion/look-log.json (one entry per published video and language).
// Rules (frame.md § Series & Variety):
//   ✖ first_graphic identical to the previous video's
//   ✖ same series AND identical layout set as one of the last 3 videos
//   ✖ identical pen-mark set as the previous video
//   ✖ more than 2 papers, unknown series / paper / layout / pen mark, main paper ≠ series paper
//   ⚠ same series 3 videos in a row · ⚠ layout marked "spec" (not built yet: build it, then mark built)
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const catalog = JSON.parse(fs.readFileSync(path.join(here, '..', 'series.json'), 'utf8'));
const logPath = process.env.LOOK_LOG || path.resolve(here, '..', '..', 'look-log.json');
const readLog = () => (fs.existsSync(logPath) ? JSON.parse(fs.readFileSync(logPath, 'utf8')) : []);
const [cmd, proj] = process.argv.slice(2);
const lang = (() => { const i = process.argv.indexOf('--lang'); return i > 0 ? process.argv[i + 1] : 'fr'; })();
const same = (a = [], b = []) => a.length === b.length && [...a].sort().join('|') === [...b].sort().join('|');

function loadLook(p) {
  const f = path.join(path.resolve(p), 'look.json');
  if (!fs.existsSync(f)) { console.error(`✖ missing ${f}`); process.exit(2); }
  return JSON.parse(fs.readFileSync(f, 'utf8'));
}

function check(p) {
  const look = loadLook(p); const E = [], W = [];
  const s = catalog.series[look.series];
  if (!s) E.push(`unknown series "${look.series}" (${Object.keys(catalog.series).join(', ')})`);
  const papers = look.papers || [];
  if (!papers.length) E.push('papers: list the main paper first');
  if (papers.length > 2) E.push(`papers: ${papers.length} > 2 — one main paper + at most one contrast paper per video`);
  for (const x of papers) if (!catalog.papers[x]) E.push(`unknown paper "${x}"`);
  if (s && papers[0] && papers[0] !== s.paper) E.push(`main paper "${papers[0]}" ≠ series paper "${s.paper}"`);
  const layouts = look.layouts || [];
  if (!look.first_graphic) E.push('first_graphic missing (the first graphic after Dr. Aksoy\'s hook)');
  for (const l of new Set([...layouts, look.first_graphic].filter(Boolean))) {
    const c = catalog.layouts[l];
    if (!c) E.push(`unknown layout "${l}"`); else if (c.status !== 'built') W.push(`layout "${l}" is spec only — build it, then set status "built" in series.json`);
  }
  if (look.first_graphic && !layouts.includes(look.first_graphic)) E.push('first_graphic must also be listed in layouts');
  for (const m of look.pen_marks || []) if (!catalog.pen_marks.includes(m)) E.push(`unknown pen mark "${m}"`);

  const name = path.basename(path.resolve(p));
  const prev = readLog().filter((e) => e.project !== name && (e.lang || 'fr') === lang).slice(-3);
  const last = prev.at(-1);
  if (last) {
    if (last.first_graphic === look.first_graphic) E.push(`first graphic "${look.first_graphic}" = previous video (${last.project}) — open with a different treatment/variant`);
    if ((look.pen_marks || []).length && same(look.pen_marks, last.pen_marks)) E.push(`pen marks identical to previous video (${last.project}) — swap at least one mark`);
    if (prev.length >= 2 && prev.slice(-2).every((e) => e.series === look.series)) W.push(`series "${look.series}" 3 videos in a row`);
  }
  for (const e of prev) if (e.series === look.series && same(e.layouts, layouts)) E.push(`same series and identical layout set as ${e.project} — change at least one layout variant`);

  console.log(`variety · ${name} · ${lang} · series ${look.series} · papers ${papers.join(' + ')} · compared with ${prev.length} previous video(s)`);
  for (const w of W) console.log(`⚠ ${w}`); for (const e of E) console.log(`✖ ${e}`);
  console.log(E.length ? `\nvariety FAILED (${E.length})` : '\nvariety passed');
  process.exitCode = E.length ? 1 : 0;
}

function log(p) {
  const look = loadLook(p); const name = path.basename(path.resolve(p));
  const entries = readLog().filter((e) => !(e.project === name && (e.lang || 'fr') === lang));
  entries.push({ project: name, lang, date: new Date().toISOString().slice(0, 10), ...look });
  fs.writeFileSync(logPath, JSON.stringify(entries, null, 2) + '\n');
  console.log(`logged ${name} (${lang}) → ${path.relative(process.cwd(), logPath)}`);
}

function status() {
  const e = readLog().filter((x) => (x.lang || 'fr') === lang); const recent = e.slice(-5);
  console.log(`last ${recent.length} (${lang}):`); for (const x of recent) console.log(`  ${x.date}  ${x.project.padEnd(40)} ${x.series.padEnd(10)} ${x.first_graphic}`);
  const used = new Set(e.slice(-4).map((x) => x.series));
  console.log('series not used in the last 4:', Object.keys(catalog.series).filter((s) => !used.has(s)).join(', ') || '—');
  const ul = new Set(e.slice(-4).flatMap((x) => x.layouts || []));
  console.log('built layouts not used in the last 4:', Object.entries(catalog.layouts).filter(([k, v]) => v.status === 'built' && !ul.has(k)).map(([k]) => k).join(', ') || '—');
}

if (cmd === 'check' && proj) check(proj); else if (cmd === 'log' && proj) log(proj); else if (cmd === 'status') status();
else { console.log('usage: node variety.mjs check|log <project> [--lang fr] · node variety.mjs status'); process.exitCode = 2; }
