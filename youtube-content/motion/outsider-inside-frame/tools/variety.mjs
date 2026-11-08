#!/usr/bin/env node
// Variety gate: keeps consecutive videos from looking the same. Every video gets its own template (visual world) from
// ../template-library/templates.json; Dr. Aksoy decision 2026-11-07.
//
//   node variety.mjs pick <series> [--lang fr] [--seed N] [--only <template>]   FIRST STEP of a video: seeded choice of template + palette + variant
//   node variety.mjs check  <project>   before render: validates <project>/look.json, compares with the log
//   node variety.mjs log    <project>   after the final render: appends the look to the log
//   node variety.mjs status             last videos + series / layouts not used lately
//   node variety.mjs suggest <series> [--seed N]   seeded proposal (first graphic + one layout per family of the
//                                       series, see series.json "families") that passes the gate against the log
//
// look.json (project root), kit worlds:
//   { "template": "gazete", "palette": "bleu", "variant": "a", "seed": 4112, "series": "chiffres", "first_graphic": "figure", "layouts": ["figure", "bars", "verdict"] }
// outsider-inside (paper world):
//   { "template": "outsider-inside", "series": "chiffres", "papers": ["kareli", "a4"], "first_graphic": "chiffre-B",
//     "layouts": ["chiffre-B", "promesse-A"], "pen_marks": ["oval-01", "strike-02"], "stamp_flip": false }
// Log: youtube-content/motion/look-log.json (one entry per published video and language).
// Rules (frame.md § Series & Variety):
//   ✖ no template, unknown template, template not built
//   ✖ same template as one of the last rotation.avoid_last videos of that language (log entries without a template count as outsider-inside)
//   ✖ kit world: unknown palette or variant, kind outside templates.json "kinds"
//   ⚠ series outside the template's "fit"
//   The rules below compare videos of the same template:
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
const library = JSON.parse(fs.readFileSync(path.resolve(here, '..', '..', 'template-library', 'templates.json'), 'utf8'));
const avoidLast = library.rotation.avoid_last;
const tplOf = (e) => e.template || 'outsider-inside';
const baseName = (n) => String(n).replace(/-shorts$/, '');
const logPath = process.env.LOOK_LOG || path.resolve(here, '..', '..', 'look-log.json');
const readLog = () => (fs.existsSync(logPath) ? JSON.parse(fs.readFileSync(logPath, 'utf8')) : []);
const [cmd, proj] = process.argv.slice(2);
const lang = (() => { const i = process.argv.indexOf('--lang'); return i > 0 ? process.argv[i + 1] : 'fr'; })();
// videos of one language, oldest first, without Shorts twins and without the video being checked
const videos = (l, self) => readLog().filter((e) => (e.lang || 'fr') === l && !String(e.project).endsWith('-shorts') && e.project !== self);
const same = (a = [], b = []) => a.length === b.length && [...a].sort().join('|') === [...b].sort().join('|');

const projName = (p) => { const r = path.resolve(p), b = path.basename(r);
  return b === 'shorts' ? `${path.basename(path.dirname(r))}-shorts` : b; };

function loadLook(p) {
  const f = path.join(path.resolve(p), 'look.json');
  if (!fs.existsSync(f)) { console.error(`✖ missing ${f}`); process.exit(2); }
  return JSON.parse(fs.readFileSync(f, 'utf8'));
}

function check(p) {
  const look = loadLook(p); const E = [], W = [];
  const s = catalog.series[look.series];
  if (!s) E.push(`unknown series "${look.series}" (${Object.keys(catalog.series).join(', ')})`);
  const tname = look.template; const t = library.templates[tname];
  if (!tname) E.push('template missing: run variety.mjs pick <series> and copy the result into look.json');
  else if (!t) E.push(`unknown template "${tname}" (${Object.keys(library.templates).join(', ')})`);
  else if (t.status !== 'built') E.push(`template "${tname}" is not built`);
  if (t && s && !t.fit.includes(look.series)) W.push(`series "${look.series}" is outside the fit of "${tname}" (${t.fit.join(', ')})`);
  const base = baseName(projName(p));
  const recent = videos(lang, base).slice(-avoidLast);
  const clash = recent.find((e) => tplOf(e) === tname);
  if (tname && clash) E.push(`template "${tname}" was used by ${clash.project}, inside the last ${avoidLast} ${lang} videos: pick another`);
  if (t && t.engine === 'kit') return checkKit(p, look, t, E, W, recent);
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

  const name = projName(p);
  const prev = readLog().filter((e) => e.project !== name && (e.lang || 'fr') === lang && tplOf(e) === 'outsider-inside').slice(-3);
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

function checkKit(p, look, t, E, W, recent) {
  if (!t.palettes.includes(look.palette)) E.push(`palette "${look.palette}" not in ${look.template}: ${t.palettes.join(', ')}`);
  if (!['a', 'b'].includes(look.variant)) E.push(`variant "${look.variant}" must be a or b`);
  const layouts = look.layouts || [];
  if (!look.first_graphic) E.push('first_graphic missing (the first graphic after the hook of Dr. Aksoy)');
  for (const l of new Set([...layouts, look.first_graphic].filter(Boolean))) if (!library.kinds.includes(l)) E.push(`unknown scene kind "${l}" (${library.kinds.join(', ')})`);
  if (look.first_graphic && !layouts.includes(look.first_graphic)) E.push('first_graphic must also be listed in layouts');
  if (recent.at(-1)?.first_graphic === look.first_graphic) W.push(`first graphic kind "${look.first_graphic}" = previous video`);
  console.log(`variety · ${projName(p)} · ${lang} · template ${look.template} (${look.palette}, ${look.variant}) · series ${look.series} · compared with ${recent.length} previous video(s)`);
  for (const w of W) console.log(`⚠ ${w}`); for (const e of E) console.log(`✖ ${e}`);
  console.log(E.length ? `\nvariety FAILED (${E.length})` : '\nvariety passed');
  process.exitCode = E.length ? 1 : 0;
}

const OPENERS = { mythe: 'claim', labo: 'process', questions: 'claim', chiffres: 'figure', conseils: 'process' };

function pick(series) {
  if (!catalog.series[series]) { console.error(`unknown series "${series}" (${Object.keys(catalog.series).join(', ')})`); process.exitCode = 2; return; }
  const arg = (n) => { const i = process.argv.indexOf(`--${n}`); return i > 0 ? process.argv[i + 1] : undefined; };
  const seed = Number(arg('seed') ?? (Date.now() % 1000000)); let a = seed >>> 0;
  const rnd = () => { a = (a + 0x6d2b79f5) >>> 0; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  const one = (x) => x[Math.floor(rnd() * x.length)];
  const hist = videos(lang); const recent = new Set(hist.slice(-avoidLast).map(tplOf));
  const lastUse = (k) => hist.map(tplOf).lastIndexOf(k);
  const built = Object.entries(library.templates).filter(([, t]) => t.status === 'built').map(([k]) => k);
  let pool = built.filter((k) => !recent.has(k) && library.templates[k].fit.includes(series));
  if (!pool.length) pool = built.filter((k) => !recent.has(k));
  if (!pool.length) { console.log('✖ every built template is inside the rotation window: build another or lower rotation.avoid_last'); process.exitCode = 1; return; }
  // never used first, then the longest rested, random inside that group
  const rested = pool.filter((k) => lastUse(k) < 0); const group = rested.length ? rested : [...pool].sort((x, y) => lastUse(x) - lastUse(y)).slice(0, 3);
  const name = arg('only') || one(group); const t = library.templates[name];
  if (!t) { console.error(`unknown template "${name}"`); process.exitCode = 2; return; }
  if (recent.has(name)) console.log(`⚠ "${name}" is inside the last ${avoidLast} ${lang} videos: check will refuse it`);
  console.log(`pick · ${series} · ${lang} · seed ${seed} · rested pool: ${group.join(', ')}`);
  console.log(`template: ${name} · ${t.name[lang] || t.name.tr} · ${t.feel}`);
  if (t.engine === 'outsider') { console.log(`→ paper world: run  node variety.mjs suggest ${series}  and add "template": "outsider-inside" to look.json`); return; }
  const prevSame = [...hist].reverse().find((e) => tplOf(e) === name);
  const palettes = t.palettes.filter((x) => x !== prevSame?.palette);
  const first = OPENERS[series];
  console.log(JSON.stringify({ template: name, palette: one(palettes), variant: one(['a', 'b']), seed, series, first_graphic: first, layouts: [first, ...library.kinds.filter((k) => k !== first)] }, null, 2));
  console.log(`→ copy into look.json, trim "layouts" to the kinds this video uses, then: node ../../template-library/tools/world.mjs new ${name} <kind> <scene-dir> --palette <p> --variant <v> --seed <seed> --lang ${lang}`);
}

function log(p) {
  const look = loadLook(p); const name = projName(p);
  const entries = readLog().filter((e) => !(e.project === name && (e.lang || 'fr') === lang));
  entries.push({ project: name, lang, date: new Date().toISOString().slice(0, 10), ...look });
  fs.writeFileSync(logPath, JSON.stringify(entries, null, 2) + '\n');
  console.log(`logged ${name} (${lang}) → ${path.relative(process.cwd(), logPath)}`);
}

function status() {
  const e = readLog().filter((x) => (x.lang || 'fr') === lang); const recent = e.slice(-5);
  console.log(`last ${recent.length} (${lang}):`); for (const x of recent) console.log(`  ${x.date}  ${x.project.padEnd(40)} ${tplOf(x).padEnd(16)} ${x.series.padEnd(10)} ${x.first_graphic}`);
  const seen = new Set(videos(lang).slice(-avoidLast).map(tplOf));
  console.log(`templates free now (not in the last ${avoidLast}):`, Object.entries(library.templates).filter(([k, v]) => v.status === 'built' && !seen.has(k)).map(([k]) => k).join(', ') || '—');
  const used = new Set(e.slice(-4).map((x) => x.series));
  console.log('series not used in the last 4:', Object.keys(catalog.series).filter((s) => !used.has(s)).join(', ') || '—');
  const ul = new Set(e.slice(-4).flatMap((x) => x.layouts || []));
  console.log('built layouts not used in the last 4:', Object.entries(catalog.layouts).filter(([k, v]) => v.status === 'built' && !ul.has(k)).map(([k]) => k).join(', ') || '—');
}

function suggest(series) {
  const s = catalog.series[series]; if (!s) { console.error(`unknown series "${series}"`); process.exitCode = 2; return; }
  const fnv = (x) => { let h = 0x811c9dc5; for (const c of Buffer.from(x, 'utf8')) { h ^= c; h = Math.imul(h, 0x01000193) >>> 0; } return h; };
  let a = Number((() => { const i = process.argv.indexOf('--seed'); return i > 0 ? process.argv[i + 1] : fnv(series + Date.now().toString().slice(0, -5)); })());
  const rnd = () => { a = (a + 0x6d2b79f5) >>> 0; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  const e = readLog().filter((x) => (x.lang || 'fr') === lang && !String(x.project).endsWith('-shorts'));
  const last = e.at(-1); const recent = new Set(e.slice(-4).flatMap((x) => x.layouts || []));
  const built = Object.entries(catalog.layouts).filter(([, v]) => v.status === 'built').map(([k]) => k);
  const byFam = (f) => built.filter((k) => k.split('-')[0] === f);
  // prefer layouts not used in the last 4 videos; random among equals
  const choose = (arr) => { const fresh = arr.filter((k) => !recent.has(k)); const pool = fresh.length ? fresh : arr; return pool[Math.floor(rnd() * pool.length)]; };
  for (let tries = 0; tries < 50; tries++) {
    const layouts = s.families.map((f) => byFam(f)).filter((x) => x.length).map(choose);
    const firstPool = layouts.filter((k) => k.split('-')[0] === s.families[0] && (!last || k !== last.first_graphic));
    const first = firstPool[0] || layouts.find((k) => !last || k !== last.first_graphic);
    const clash = e.slice(-3).some((x) => x.series === series && same(x.layouts, layouts));
    if (first && !clash) {
      console.log(`suggest · ${series} (${s[lang] || s.fr}) · paper ${s.paper} · compared with ${Math.min(e.length, 4)} previous video(s)`);
      console.log(JSON.stringify({ series, papers: [s.paper], first_graphic: first, layouts: [first, ...layouts.filter((k) => k !== first)] }, null, 2));
      console.log('→ copy into look.json; pen_marks / seed / stamp_flip are filled by tools/pen.mjs apply');
      return;
    }
  }
  console.log('✖ no combination passes — build another layout variant for this series (series.json "spec" → "built")'); process.exitCode = 1;
}

if (cmd === 'pick' && proj) pick(proj); else if (cmd === 'suggest' && proj) suggest(proj); else if (cmd === 'check' && proj) check(proj); else if (cmd === 'log' && proj) log(proj); else if (cmd === 'status') status();
else { console.log('usage: node variety.mjs pick <series> [--lang fr] [--seed N] [--only <template>] · check|log <project> [--lang fr] · status · suggest <series> [--seed N]'); process.exitCode = 2; }
