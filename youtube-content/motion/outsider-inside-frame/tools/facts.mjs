#!/usr/bin/env node
// Outsider Inside — source → scene link.
//
// Every number, finding, verdict and citation shown on screen comes from
// <project>/scene-facts.json, and every entry there is tied to a claim ID in the
// script's fact-checked -sources.md and (when it is a paper) to a PubMed record.
//
//   node facts.mjs fetch  <project>              cache PubMed records for every ref (needs network)
//   node facts.mjs apply  <project> [--lang fr]  write fact texts + citations into index.html
//   node facts.mjs verify <project> [--lang fr] [--draft]
//   node facts.mjs all    <project> [--lang fr]  fetch → apply → verify
//
// verify fails (exit 1) when:
//   - a fact's claim ID is not in the -sources.md, or its last verdict there is ❌ / ❓ / 🕒
//     (unless the fact carries an explicit "override" reason)
//   - a number on a fact is not found in that claim's text, the sources it cites, or the PubMed record
//   - a cited paper is retracted / has an expression of concern
//   - a figure or verdict is on screen without its reference on screen
//   - a verdict is outside the fixed vocabulary
//   - any digit appears in visible on-screen text that is not bound to a fact (data-fact / data-ref)
//     or explicitly exempted (data-fact-exempt="reason") / per-language chrome (data-chrome="id", from spec.chrome)
//   - bound text on screen differs from scene-facts.json (run apply)
//   - a TODO is left in scene-facts.json (drafts from facts-draft.mjs; warning only with --draft)
// No dependencies; Node 18+.

import fs from 'node:fs';
import path from 'node:path';

const VERDICTS = {
  fr: ['PREUVE SOLIDE', 'PREUVE FAIBLE', 'NON PROUVÉ', 'NON RECOMMANDÉ', 'ÇA DÉPEND'],
  tr: ['GÜÇLÜ KANIT', 'ZAYIF KANIT', 'KANITLANMADI', 'ÖNERİLMEZ', 'DURUMA GÖRE'],
  en: ['STRONG EVIDENCE', 'WEAK EVIDENCE', 'NOT PROVEN', 'NOT RECOMMENDED', 'IT DEPENDS'],
};
const BAD_PUBTYPES = ['Retracted Publication', 'Retraction of Publication', 'Expression of Concern'];
const EUTILS = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils';

// ---------- cli ----------
const [cmd, projArg, ...rest] = process.argv.slice(2);
const flag = (name) => rest.includes(`--${name}`);
const opt = (name) => { const i = rest.indexOf(`--${name}`); return i >= 0 ? rest[i + 1] : undefined; };
if (!cmd || !projArg || !['fetch', 'apply', 'verify', 'all'].includes(cmd)) {
  console.log('usage: node facts.mjs <fetch|apply|verify|all> <project-dir> [--lang fr|tr|en] [--draft]');
  process.exit(2);
}
const project = path.resolve(projArg);
const factsPath = path.join(project, 'scene-facts.json');
const htmlPath = path.join(project, opt('html') || 'index.html');
const cacheDir = path.join(project, '.facts-cache');
if (!fs.existsSync(factsPath)) die(`missing ${factsPath}`);
const spec = JSON.parse(fs.readFileSync(factsPath, 'utf8'));
const lang = opt('lang') || spec.lang || 'fr';
const refIds = Object.keys(spec.refs || {});

function die(msg) { console.error(`✖ ${msg}`); process.exit(1); }
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const pick = (v) => (v && typeof v === 'object' ? v[lang] : v);

// ---------- numbers ----------
// "58,5 %" → 58.5 · "1 936" / "1.936" / "1,936" → 1936 · "36/410" → 36, 410 · "−3,4" → 3.4
function numbersIn(text) {
  const out = [];
  const re = /\d+(?:[   .,]\d+)*/g;
  for (const m of String(text).matchAll(re)) {
    let s = m[0].replace(/[   ]/g, (c, i, str) => (/^\d{3}(\D|$)/.test(str.slice(i + 1)) ? '' : '|'));
    for (let part of s.split('|')) {
      if (/^\d{1,3}([.,]\d{3})+$/.test(part)) part = part.replace(/[.,]/g, ''); // thousands
      else part = part.replace(',', '.');
      const n = Number(part);
      if (Number.isFinite(n)) out.push(n);
    }
  }
  return out;
}
const sameNum = (a, b) => Math.abs(a - b) < 1e-9;

// ---------- sources.md ----------
function loadSources() {
  const rel = spec.sources_md;
  if (!rel) die('scene-facts.json: "sources_md" is required');
  const cands = [path.resolve(project, rel), path.resolve(process.cwd(), rel)];
  const p = cands.find((c) => fs.existsSync(c));
  if (!p) die(`sources file not found: ${rel}`);
  return { path: p, text: fs.readFileSync(p, 'utf8') };
}
function expandIds(cell) { // "C03–C04" → C03,C04 · "C07, C08" → both
  const ids = [];
  for (const piece of cell.split(/[,/]/)) {
    const m = piece.trim().match(/^([A-Z]+)(\d+)([a-z]?)\s*[–-]\s*[A-Z]*(\d+)$/);
    if (m) { for (let i = +m[2]; i <= +m[4]; i++) ids.push(m[1] + String(i).padStart(m[2].length, '0')); }
    else if (/^[A-Z]+\d+[a-z]?$/.test(piece.trim())) ids.push(piece.trim());
  }
  return ids;
}
function claimContext(src, id, depth = 0) {
  const lines = src.text.split(/\r?\n/);
  const rows = []; // table rows whose first cell names the id, in file order
  lines.forEach((ln, i) => {
    const m = ln.match(/^\|\s*([^|]+?)\s*\|/);
    if (m && expandIds(m[1]).includes(id)) rows.push({ line: i + 1, text: ln });
  });
  // "### S2 — …" style sections
  const secs = [];
  lines.forEach((ln, i) => {
    const h = ln.match(/^#{2,4}\s+([A-Z]+\d+[a-z]?)\b/);
    if (h && h[1] === id) {
      let j = i + 1; while (j < lines.length && !/^#{1,4}\s/.test(lines[j])) j++;
      secs.push({ line: i + 1, text: lines.slice(i, j).join('\n') });
    }
  });
  const own = [...rows, ...secs];
  // sources a claim row points to (S1, S2 …) count as its evidence too
  const cited = new Set(own.flatMap((r) => [...r.text.matchAll(/\bS\d+\b/g)].map((m) => m[0])));
  cited.delete(id);
  const citedText = depth ? '' : [...cited].map((sid) => claimContext(src, sid, 1).ownText).join('\n');
  const verdictRows = rows.filter((r) => /[✅⚠❌❓🕒]/u.test(r.text));
  const last = verdictRows.at(-1);
  const lastVerdict = last ? (last.text.match(/✅|⚠️|⚠|❌|❓|🕒/u) || [null])[0] : null;
  return { found: own.length > 0, lines: own.map((r) => r.line), ownText: own.map((r) => r.text).join('\n'),
           citedText, lastVerdict, lastVerdictLine: last?.line };
}

// ---------- pubmed cache ----------
const cacheFile = (pmid) => path.join(cacheDir, `pmid-${pmid}.json`);
async function fetchPubmed(pmid) {
  const sum = await (await fetch(`${EUTILS}/esummary.fcgi?db=pubmed&id=${pmid}&retmode=json`)).json();
  const r = sum.result?.[pmid];
  if (!r || r.error) throw new Error(`PubMed has no record ${pmid}`);
  const abs = await (await fetch(`${EUTILS}/efetch.fcgi?db=pubmed&id=${pmid}&rettype=abstract&retmode=text`)).text();
  return {
    pmid, fetched: new Date().toISOString().slice(0, 10),
    authors: r.authors.filter((a) => a.authtype === 'Author').map((a) => a.name),
    title: r.title, journal: r.source, pubdate: r.pubdate, volume: r.volume, issue: r.issue, pages: r.pages,
    doi: (r.articleids.find((a) => a.idtype === 'doi') || {}).value || null,
    pubtype: r.pubtype, abstract: abs,
  };
}
function readCache(pmid) { return fs.existsSync(cacheFile(pmid)) ? JSON.parse(fs.readFileSync(cacheFile(pmid), 'utf8')) : null; }
function shortPages(p) { // 2117-2125 → 2117-25
  const m = String(p || '').match(/^(\d+)-(\d+)$/); if (!m || m[1].length !== m[2].length) return p || '';
  let i = 0; while (i < m[1].length - 1 && m[1][i] === m[2][i]) i++; return `${m[1]}-${m[2].slice(i)}`;
}
function citation(rec) {
  const first = rec.authors[0] || ''; const etal = rec.authors.length > 1 ? ', et al.' : '';
  const year = String(rec.pubdate).slice(0, 4);
  const vi = rec.volume ? `;${rec.volume}${rec.issue ? `(${rec.issue})` : ''}` : '';
  const pg = rec.pages ? `:${shortPages(rec.pages)}` : '';
  return `${first}${etal} ${rec.journal}. ${year}${vi}${pg}`;
}
function refText(id, field) {
  const ref = spec.refs[id]; const marker = `[${refIds.indexOf(id) + 1}]`;
  if (field === 'marker') return marker;
  if (field === 'design') { const d = pick(ref.design); return ref.n ? `${d} · n = ${ref.n}` : d; }
  if (ref.pmid) { const rec = readCache(ref.pmid); if (!rec) die(`no cache for PMID ${ref.pmid} — run: facts.mjs fetch`); return `${marker} ${citation(rec)}`; }
  return `${marker} ${pick(ref.label)}`; // guideline / label / SmPC without PMID
}
function factText(f, field = 'text') { const v = pick(f[field]); if (v == null) die(`fact ${f.id}: no "${field}" for lang ${lang}`); return v; }

// ---------- html ----------
const VOID = new Set(['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr']);
function parse(html) {
  const tagRe = /<!--[\s\S]*?-->|<(\/?)([a-zA-Z][\w-]*)([^>]*?)(\/?)>/g;
  const stack = []; const bound = []; const texts = []; let last = 0; let raw = null; let m;
  const attr = (s, n) => { const a = s.match(new RegExp(`\\s${n}\\s*=\\s*("([^"]*)"|'([^']*)')`)); return a ? (a[2] ?? a[3]) : undefined; };
  while ((m = tagRe.exec(html))) {
    if (m[0].startsWith('<!--')) { last = tagRe.lastIndex; continue; }
    const [whole, close, nameRaw, attrs] = m; const name = nameRaw.toLowerCase();
    if (raw && !(close && name === raw)) continue;
    if (!raw && m.index > last) texts.push({ text: html.slice(last, m.index), at: m.index, stack: [...stack] });
    if (close) {
      raw = null;
      for (let i = stack.length - 1; i >= 0; i--) if (stack[i].name === name) {
        const el = stack[i]; el.innerEnd = m.index; if (el.bind) bound.push(el); stack.length = i; break;
      }
    } else {
      const el = { name, innerStart: tagRe.lastIndex, fact: attr(attrs, 'data-fact'), ref: attr(attrs, 'data-ref'), chrome: attr(attrs, 'data-chrome'),
                   field: attr(attrs, 'data-field'), exempt: attr(attrs, 'data-fact-exempt'),
                   hidden: /\b(aria-hidden="true"|hidden\b)/.test(attrs), line: html.slice(0, m.index).split('\n').length };
      el.bind = !!(el.fact || el.ref || el.chrome);
      if (name === 'script' || name === 'style' || name === 'title') raw = name;
      if (!VOID.has(name) && !m[4]) stack.push(el);
    }
    last = tagRe.lastIndex;
  }
  return { bound, texts };
}
const decode = (s) => s.replace(/&#(\d+);/g, (_, n) => String.fromCodePoint(+n)).replace(/&#x([\da-f]+);/gi, (_, n) => String.fromCodePoint(parseInt(n, 16)))
  .replace(/&nbsp;/g, ' ').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&amp;/g, '&');
const norm = (s) => decode(s).replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
function wanted(el) {
  if (el.chrome) { const c = (spec.chrome || {})[el.chrome]; if (!c) return { err: `unknown data-chrome="${el.chrome}"` }; const t = pick(c); return t == null ? { err: `chrome ${el.chrome}: no text for ${lang}` } : { text: t }; }
  if (el.fact) { const f = spec.facts.find((x) => x.id === el.fact); if (!f) return { err: `unknown data-fact="${el.fact}"` }; return { text: factText(f, el.field || 'text') }; }
  if (!spec.refs[el.ref]) return { err: `unknown data-ref="${el.ref}"` };
  return { text: refText(el.ref, el.field || 'citation') };
}

// ---------- commands ----------
async function doFetch() {
  fs.mkdirSync(cacheDir, { recursive: true });
  for (const [id, ref] of Object.entries(spec.refs)) {
    if (!ref.pmid) { console.log(`· ${id}: no PMID (label used)`); continue; }
    const rec = await fetchPubmed(ref.pmid);
    fs.writeFileSync(cacheFile(ref.pmid), JSON.stringify(rec, null, 2));
    console.log(`✔ ${id}: PMID ${ref.pmid} → ${citation(rec)}  [${rec.pubtype.join(', ')}]`);
  }
}
function doApply() {
  let html = fs.readFileSync(htmlPath, 'utf8');
  const { bound } = parse(html); let n = 0;
  for (const el of bound.sort((a, b) => b.innerStart - a.innerStart)) {
    const w = wanted(el); if (w.err) die(`${path.basename(htmlPath)}:${el.line} ${w.err}`);
    html = html.slice(0, el.innerStart) + esc(w.text) + html.slice(el.innerEnd); n++;
  }
  html = html.replace(/<html\b([^>]*?)\slang="[^"]*"/, `<html$1 lang="${lang}"`);
  fs.writeFileSync(htmlPath, html);
  console.log(`✔ apply: ${n} bound element(s) written (${lang})`);
}
function doVerify() {
  const errors = []; const warns = []; const ok = [];
  const E = (m) => errors.push(m); const W = (m) => (flag('draft') ? warns : errors).push(m);
  const src = loadSources();
  // refs
  for (const [id, ref] of Object.entries(spec.refs)) {
    if (!ref.pmid) { if (!pick(ref.label)) E(`ref ${id}: needs "pmid" or a "label"`); continue; }
    const rec = readCache(ref.pmid);
    if (!rec) { E(`ref ${id}: PMID ${ref.pmid} not cached — run: facts.mjs fetch`); continue; }
    const bad = rec.pubtype.filter((t) => BAD_PUBTYPES.includes(t));
    if (bad.length) E(`ref ${id}: PMID ${ref.pmid} is flagged on PubMed: ${bad.join(', ')}`);
    if (ref.n && !numbersIn(rec.abstract).some((x) => sameNum(x, numbersIn(ref.n)[0]))) W(`ref ${id}: n = ${ref.n} not found in the PubMed abstract`);
    ok.push(`ref ${id}: ${citation(rec)} (PubMed, fetched ${rec.fetched})`);
  }
  // facts
  for (const f of spec.facts) {
    const tag = `fact ${f.id}`;
    if (f.kind === 'quoted') { // the claim being examined (brochure, marketing, common belief)
      if (!f.origin) E(`${tag}: kind "quoted" needs "origin" (where the claim comes from)`);
      continue;
    }
    if (!f.claim) { E(`${tag}: needs "claim" (ID in ${path.basename(src.path)})`); continue; }
    const ctx = claimContext(src, f.claim);
    if (!ctx.found) { E(`${tag}: claim ${f.claim} not found in ${path.basename(src.path)}`); continue; }
    if (['❌', '❓', '🕒'].includes(ctx.lastVerdict) && !f.override)
      E(`${tag}: last verdict for ${f.claim} is ${ctx.lastVerdict} (line ${ctx.lastVerdictLine}); fix the script/fact or add "override": "<reason>"`);
    if (!ctx.lastVerdict) warns.push(`${tag}: no per-claim verdict row found for ${f.claim} — make sure the fact-check report covers it`);
    if (f.override) warns.push(`${tag}: override — ${f.override}`);
    if ((f.kind === 'figure' || f.kind === 'verdict') && !f.ref) E(`${tag}: ${f.kind} needs "ref"`);
    if (f.ref && !spec.refs[f.ref]) E(`${tag}: unknown ref ${f.ref}`);
    if (f.kind === 'verdict') {
      const v = factText(f); if (!VERDICTS[lang].includes(v)) E(`${tag}: verdict "${v}" not in the ${lang} vocabulary (${VERDICTS[lang].join(' · ')})`);
    }
    // every number must trace to the claim row, the sources it cites, or the PubMed record
    const rec = f.ref && spec.refs[f.ref]?.pmid ? readCache(spec.refs[f.ref].pmid) : null;
    const pool = numbersIn([ctx.ownText, ctx.citedText, rec?.abstract || ''].join('\n'));
    for (const field of ['text', 'label']) {
      if (!f[field]) continue;
      for (const L of Object.keys(typeof f[field] === 'object' ? f[field] : { [lang]: f[field] })) {
        const s = typeof f[field] === 'object' ? f[field][L] : f[field];
        for (const x of numbersIn(s)) if (!pool.some((y) => sameNum(x, y)))
          E(`${tag} (${L}.${field}): number ${x} in "${s}" is not in claim ${f.claim}, its cited sources or the PubMed record`);
      }
    }
    ok.push(`${tag}: ${f.claim} ${ctx.lastVerdict || '·'} → "${factText(f)}"`);
  }
  // drafts (tools/facts-draft.mjs): every TODO must be written before render
  const todo = []; (function walk(v, at) { if (typeof v === 'string') { if (/\bTODO\b/.test(v)) todo.push(at); }
    else if (v && typeof v === 'object') for (const [k, x] of Object.entries(v)) if (!k.startsWith('_')) walk(x, at ? `${at}.${k}` : k); })(
    { refs: spec.refs, chrome: spec.chrome, facts: Object.fromEntries((spec.facts || []).map((f) => [f.id, f])) }, '');
  for (const t of todo) W(`TODO left in scene-facts.json at ${t} — write the on-screen text`);
  // chrome: titles / chapter numbers only — never data
  for (const [id, c] of Object.entries(spec.chrome || {})) for (const [L, t] of Object.entries(c))
    for (const x of numbersIn(t)) if (!(Number.isInteger(x) && x < 100)) E(`chrome ${id} (${L}): "${t}" carries a number (${x}); chrome is for titles and chapter numbers only — use a fact`);
  // html
  if (!fs.existsSync(htmlPath)) E(`missing ${htmlPath}`);
  else {
    const html = fs.readFileSync(htmlPath, 'utf8'); const { bound, texts } = parse(html);
    for (const el of bound) {
      const w = wanted(el); if (w.err) { E(`html:${el.line} ${w.err}`); continue; }
      const have = norm(html.slice(el.innerStart, el.innerEnd));
      if (have !== norm(esc(w.text))) E(`html:${el.line} ${el.fact ? 'data-fact=' + el.fact : el.ref ? 'data-ref=' + el.ref : 'data-chrome=' + el.chrome} shows "${have}" but scene-facts says "${w.text}" — run apply`);
    }
    for (const t of texts) {
      const s = norm(t.text); if (!/\d/.test(s)) continue;
      if (t.stack.some((e) => e.bind || e.exempt || e.hidden)) continue;
      E(`html:${html.slice(0, t.at).split('\n').length} unsourced number on screen: "${s}" — bind it with data-fact / data-ref or mark data-fact-exempt="reason"`);
    }
    const onScreenRefs = new Set(bound.filter((b) => b.ref && (b.field || 'citation') === 'citation').map((b) => b.ref));
    const seen = new Set();
    for (const b of bound.filter((x) => x.fact)) {
      const f = spec.facts.find((x) => x.id === b.fact);
      if (!f || seen.has(f.id)) continue; seen.add(f.id);
      if ((f.kind === 'figure' || f.kind === 'verdict') && f.ref && !onScreenRefs.has(f.ref))
        E(`html:${b.line} ${f.kind} ${f.id} is on screen but its reference ${f.ref} is not (add data-ref="${f.ref}")`);
    }
  }
  ok.forEach((m) => console.log(`✔ ${m}`)); warns.forEach((m) => console.log(`⚠ ${m}`)); errors.forEach((m) => console.log(`✖ ${m}`));
  console.log(errors.length ? `\nverify FAILED: ${errors.length} error(s)` : `\nverify passed (${lang}) — every on-screen number traces to ${path.basename(src.path)}`);
  if (errors.length) process.exit(1);
}

if (cmd === 'fetch') await doFetch();
if (cmd === 'apply') doApply();
if (cmd === 'verify') doVerify();
if (cmd === 'all') { await doFetch(); doApply(); doVerify(); }
