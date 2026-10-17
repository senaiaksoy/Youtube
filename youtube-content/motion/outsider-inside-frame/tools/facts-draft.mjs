#!/usr/bin/env node
// Outsider Inside — draft a scene-facts.json from the script's fact-checked -sources.md.
//
//   node facts-draft.mjs <sources.md> <scene-dir> [--claims C02,C15,C22] [--force]
//
// Reads the claim register / verification tables of the -sources.md (the same parsing rules as facts.mjs:
// a table row whose first cell is a claim ID such as C07 or a range C03–C04; "### S2 — …" source sections; the
// LAST row carrying ✅ ⚠️ ❌ ❓ 🕒 is the claim's verdict) and writes <scene-dir>/scene-facts.json with:
//   - refs   R1, R2 … one per PubMed record cited by the chosen claims (pmid; design/n left as TODO)
//   - facts  one per claim, kind "statement", text TODO in fr/tr/en, plus helper fields for the author:
//            _claim (what the register says), _numbers (every number found for that claim, to pick figures from),
//            _verdict, _pmids. facts.mjs ignores keys starting with "_".
//   - chrome chapter (TODO)
// Claims whose last verdict is ❌ / ❓ / 🕒 are NOT drafted (they may not go on screen); they are listed.
// Without --claims every claim with ✅ or ⚠️ (or no verdict row yet, flagged) is drafted.
// Every "TODO" makes facts.mjs verify fail (warning with --draft) until the author writes the on-screen text.
// Never invents an on-screen sentence or a number: it only lays out what the register already says.
import fs from 'node:fs';
import path from 'node:path';

const args = process.argv.slice(2);
const opt = (k) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : undefined; };
const pos = args.filter((a, i) => !a.startsWith('--') && !(i > 0 && ['--claims'].includes(args[i - 1])));
const [srcArg, sceneArg] = pos;
if (!srcArg || !sceneArg) { console.log('usage: node facts-draft.mjs <sources.md> <scene-dir> [--claims C02,C15] [--force]'); process.exit(2); }
const srcPath = path.resolve(srcArg); const scene = path.resolve(sceneArg);
if (!fs.existsSync(srcPath)) { console.error(`✖ missing ${srcPath}`); process.exit(2); }
fs.mkdirSync(scene, { recursive: true });
const out = path.join(scene, 'scene-facts.json');
if (fs.existsSync(out) && !args.includes('--force')) { console.error(`✖ ${out} exists — pass --force to overwrite`); process.exit(2); }

const text = fs.readFileSync(srcPath, 'utf8'); const lines = text.split(/\r?\n/);
function expandIds(cell) { // same rules as facts.mjs
  const ids = [];
  for (const piece of cell.split(/[,/]/)) {
    const m = piece.trim().match(/^([A-Z]+)(\d+)([a-z]?)\s*[–-]\s*[A-Z]*(\d+)$/);
    if (m) { for (let i = +m[2]; i <= +m[4]; i++) ids.push(m[1] + String(i).padStart(m[2].length, '0')); }
    else if (/^[A-Z]+\d+[a-z]?$/.test(piece.trim())) ids.push(piece.trim());
  }
  return ids;
}
function numbersIn(s) { // simplified copy of facts.mjs: "58,5 %" → 58.5, "1 936" → 1936
  const outN = [];
  for (const m of String(s).matchAll(/\d+(?:[  .,]\d+)*/g)) {
    let p = m[0];
    if (/^\d{1,3}([  .,]\d{3})+$/.test(p)) p = p.replace(/[  .,]/g, ''); else p = p.replace(/[  ]/g, '').replace(',', '.');
    const n = Number(p); if (Number.isFinite(n)) outN.push(n);
  }
  return outN;
}
const VERD = /✅|⚠️|⚠|❌|❓|🕒/u;
const claims = new Map(); // id → { rows: [], verdict, firstCell }
const sections = new Map(); // S1 → text
lines.forEach((ln, i) => {
  const m = ln.match(/^\|\s*([^|]+?)\s*\|/);
  if (m && !/^-+$/.test(m[1].replace(/[:\s]/g, ''))) for (const id of expandIds(m[1])) {
    if (!/^C\d/.test(id)) continue;
    const c = claims.get(id) || { rows: [], verdict: null, line: i + 1 };
    c.rows.push(ln); const v = ln.match(VERD); if (v) c.verdict = v[0].replace('⚠️', '⚠');
    claims.set(id, c);
  }
  const h = ln.match(/^#{2,4}\s+(S\d+)\b/);
  if (h) { let j = i + 1; while (j < lines.length && !/^#{1,4}\s/.test(lines[j])) j++; sections.set(h[1], lines.slice(i, j).join('\n')); }
});
if (!claims.size) { console.error('✖ no claim rows (| C01 | …) found in the sources file'); process.exit(1); }

const wanted = opt('--claims') ? opt('--claims').split(',').map((s) => s.trim()) : [...claims.keys()];
const drafted = [], skipped = [], missing = [];
for (const id of wanted) {
  const c = claims.get(id); if (!c) { missing.push(id); continue; }
  if (['❌', '❓', '🕒'].includes(c.verdict)) { skipped.push(`${id} ${c.verdict}`); continue; }
  drafted.push(id);
}
const pmidsOf = (s) => [...new Set([...String(s).matchAll(/(?:PMID[:\s*]*|pubmed\.ncbi\.nlm\.nih\.gov\/)(\d{6,9})/gi)].map((m) => m[1]))];
const refs = {}; const refByPmid = {};
const facts = drafted.map((id, k) => {
  const c = claims.get(id); const own = c.rows.join('\n');
  const cited = [...new Set([...own.matchAll(/\bS\d+\b/g)].map((m) => m[0]))].map((s) => sections.get(s) || '').join('\n');
  const pmids = pmidsOf(own + '\n' + cited);
  for (const p of pmids) if (!refByPmid[p]) { const r = `R${Object.keys(refs).length + 1}`; refByPmid[p] = r;
    refs[r] = { pmid: p, design: { fr: 'TODO', tr: 'TODO', en: 'TODO' } };
    // a source section that talks about a retraction: flag it (facts.mjs verify also checks PubMed's publication type)
    const sec = [...sections.values()].find((t) => t.includes(p)) || lines.find((l) => l.includes(p)) || '';
    if (/retract|geri çek|rétract|expression of concern/i.test(sec)) refs[r]._warn = 'the source text around this PMID mentions a retraction — do not cite it on screen'; }
  const cells = c.rows[0].split('|').map((x) => x.trim()).filter(Boolean);
  const nums = [...new Set(numbersIn(own.replace(/PMID[:\s*]*\d+/gi, '').replace(/\b[CS]\d+\b/g, '')))];
  return { id: `F${String(k + 1).padStart(2, '0')}`, kind: 'statement', claim: id, ...(pmids.length ? { ref: refByPmid[pmids[0]] } : {}),
           text: { fr: 'TODO', tr: 'TODO', en: 'TODO' },
           _claim: cells[1] || '', _verdict: c.verdict || 'none yet', _numbers: nums, _pmids: pmids };
});
const spec = { video: `${path.basename(scene)} — DRAFT from ${path.basename(srcPath)}`, lang: 'fr',
  sources_md: path.relative(scene, srcPath).split(path.sep).join('/'), refs,
  chrome: { chapter: { fr: 'TODO', tr: 'TODO', en: 'TODO' } }, facts };
fs.writeFileSync(out, JSON.stringify(spec, null, 2) + '\n');
console.log(`draft → ${path.relative(process.cwd(), out)}`);
for (const [r, x] of Object.entries(refs)) if (x._warn) console.log(`  ⚠ ${r} PMID ${x.pmid}: ${x._warn}`);
console.log(`  refs = every PMID the drafted claims cite: keep only those whose citation goes on screen`);
console.log(`  ${facts.length} fact(s): ${drafted.join(', ') || '—'} · ${Object.keys(refs).length} ref(s): ${Object.values(refs).map((r) => 'PMID ' + r.pmid).join(', ') || '— (guideline/label refs: add "label")'}`);
if (skipped.length) console.log(`  not drafted (verdict forbids the screen): ${skipped.join(', ')}`);
if (missing.length) console.log(`  not in the sources file: ${missing.join(', ')}`);
const nov = facts.filter((f) => f._verdict === 'none yet').map((f) => f.claim);
if (nov.length) console.log(`  ⚠ no verdict row yet for ${nov.join(', ')} — the fact-check report must cover them before render`);
console.log('next: write each fact\'s on-screen text (fr/tr/en; numbers only from _numbers), set kind figure/label/verdict where needed,\n'
  + '      fill design / n per ref and chrome, then: node facts.mjs fetch <scene> && node facts.mjs verify <scene> --draft');
