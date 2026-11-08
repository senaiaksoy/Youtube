#!/usr/bin/env node
// Template library: scaffolds a HyperFrames scene in any visual world.
//
//   node world.mjs list
//   node world.mjs new  <template> <kind> <dest> [--palette p] [--variant a|b] [--seed n] [--lang fr] [--duration 8]
//   node world.mjs demo <template|all> [--lang fr] [--palette p] [--variant a|b]   → demos/<template>/<kind>/ with the ERA reference facts
//
// A scene is a normal HyperFrames project: index.html + assets/{world,kit,fonts,vendor}. Slot ids (Q1, F1, K1, R1…) are placeholders:
// in a real video rename them to the ids of the scene-facts.json drafted by tools/facts-draft.mjs. facts.mjs, legibility.mjs,
// aspect.mjs and `hyperframes check` run on it unchanged. The outsider-inside template does not use this tool: it has its own scenes.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const lib = path.resolve(here, '..');
const frame = path.resolve(lib, '..', 'outsider-inside-frame');
const catalog = JSON.parse(fs.readFileSync(path.join(lib, 'templates.json'), 'utf8'));
const args = process.argv.slice(2);
const opt = (n, d) => { const i = args.indexOf(`--${n}`); return i >= 0 ? args[i + 1] : d; };
// fs.cpSync crashes natively on Node 24 + Windows when the path holds a non-ASCII letter (A-klasör)
const copyDir = (a, b) => { fs.mkdirSync(b, { recursive: true }); for (const e of fs.readdirSync(a, { withFileTypes: true })) { const x = path.join(a, e.name), y = path.join(b, e.name); if (e.isDirectory()) copyDir(x, y); else fs.copyFileSync(x, y); } };
const pos = args.filter((a, i) => !a.startsWith('--') && !(i > 0 && args[i - 1].startsWith('--')));
const [cmd, a1, a2, a3] = pos;

const ref = `<div class="slip" id="slip"><div class="t" data-ref="R1">[1] Doyle N, et al. JAMA. 2022;328(21):2117-25</div><div data-ref="R1" data-field="design">Essai randomisé multicentrique · n = 767</div></div>`;
const mk = `<span class="mk" data-ref="R1" data-field="marker">[1]</span>`;
const kicker = `<div class="kicker" id="kicker"><span data-chrome="chapter">07 · Test ERA</span></div>`;
const foot = `<div class="foot" id="foot"></div>`;
const note = `<div class="side-note" id="note"><div class="k" data-fact="K1">Naissances vivantes par transfert</div><div class="n" data-fact="F2">58,5 %</div><div class="l" data-fact="F2" data-field="label">Transfert guidé par l’ERA</div><div class="ref"><div data-ref="R1">[1] Doyle N, et al. JAMA. 2022;328(21):2117-25</div></div></div>`;
const icons = `<svg viewBox="0 0 24 24"><path id="like" d="M7 21H4V10h3v11Zm3 0h7.6a2 2 0 0 0 2-1.6l1.3-6.6A2 2 0 0 0 19 10.4h-5.2l.8-4.2a1.7 1.7 0 0 0-3-1.4L7.9 10v9.6L10 21Z"/></svg><svg viewBox="0 0 24 24"><path id="bell" d="M12 3a6 6 0 0 0-6 6v4.2L4.3 16.6a.9.9 0 0 0 .8 1.4h13.8a.9.9 0 0 0 .8-1.4L18 13.2V9a6 6 0 0 0-6-6Zm-2.4 17a2.5 2.5 0 0 0 4.8 0"/></svg>`;

const SCENES = {
  claim: { frame: 'split', body: `${kicker}
        <div class="claim hero" id="claim"><span class="s" id="s" data-fact="Q1">« Le test ERA améliore vos chances. »</span></div>
        <div class="evidence" id="ev"><span data-fact="F1">Essai randomisé : aucun bénéfice démontré.</span>${mk}</div>
        ${ref}`, script: `K.in('#kicker', 0.2); K.big('#claim', 0.4); K.strike('#s', 2.2); K.in('#ev', 3.0); K.in('#slip', 3.6);` },
  figure: { frame: 'split', body: `${kicker}
        <div class="label" id="label" data-fact="K1">Naissances vivantes par transfert</div>
        <div class="fig hero" id="fig" data-fact="F2">58,5 %</div>
        <div class="ctx" id="ctx"><span data-fact="F1">Essai randomisé : aucun bénéfice démontré.</span>${mk}</div>
        ${ref}`, script: `K.in('#kicker', 0.2); K.in('#label', 0.4); K.big('#fig', 0.9); K.in('#ctx', 2.4); K.in('#slip', 3.0);` },
  bars: { frame: '', body: `${kicker}
        <div class="title" id="title" data-fact="K1">Naissances vivantes par transfert</div>
        <div class="bars">
          <div class="bar" id="b1"><div class="bar-name" data-fact="F2" data-field="label">Transfert guidé par l’ERA</div><div class="bar-row"><div class="bar-track"><div class="bar-fill" id="f1"></div></div><div class="bar-val" data-fact="F2">58,5 %</div></div></div>
          <div class="bar" id="b2"><div class="bar-name" data-fact="F3" data-field="label">Transfert à horaire standard</div><div class="bar-row"><div class="bar-track"><div class="bar-fill" id="f2"></div></div><div class="bar-val" data-fact="F3">61,9 %</div></div></div>
        </div>
        ${ref}`, script: `K.in('#kicker', 0.2); K.big('#title', 0.4); K.in('#b1', 1.2); K.bar('#f1', 1.4, 58.5); K.in('#b2', 2.2); K.bar('#f2', 2.4, 61.9); K.in('#slip', 3.6);` },
  process: { frame: '', body: `${kicker}
        <div class="title" id="title" data-chrome="ftitle">La FIV, étape par étape</div>
        <div class="steps">
          <div class="step" id="p1"><div class="step-n" data-chrome="s1">01</div><div class="step-t" data-chrome="n1">Stimulation</div></div>
          <div class="step" id="p2"><div class="step-n" data-chrome="s2">02</div><div class="step-t" data-chrome="n2">Ponction</div></div>
          <div class="step" id="p3"><div class="step-n" data-chrome="s3">03</div><div class="step-t" data-chrome="n3">Fécondation</div></div>
          <div class="step" id="p4"><div class="step-n" data-chrome="s4">04</div><div class="step-t" data-chrome="n4">Transfert</div></div>
        </div>`, script: `K.in('#kicker', 0.2); K.big('#title', 0.4); ['#p1', '#p2', '#p3', '#p4'].forEach((s, i) => K.in(s, 1.4 + i * 0.8));` },
  verdict: { frame: 'right', body: `${kicker}
        <div class="head" id="head" data-fact="H1">Le test ERA en routine</div>
        <div class="stamp" id="stamp" data-stamp data-fact="V1">NON PROUVÉ</div>
        <div class="ctx" id="ctx"><span data-fact="F1">Essai randomisé : aucun bénéfice démontré.</span>${mk}</div>
        ${ref}`, script: `K.in('#kicker', 0.2); K.big('#head', 0.4); K.stamp('#stamp', 1.8); K.in('#ctx', 2.6); K.in('#slip', 3.2);` },
  chapter: { frame: '', body: `<div class="ch-n" id="n" data-chrome="num2">08</div>
        <div class="ch-title" id="t" data-chrome="ctitle">Ce que disent les essais</div>`, script: `K.in('#n', 0.2); K.big('#t', 0.5);` },
  closing: { frame: '', body: `<div class="signature" id="sig"><span data-chrome="sig_pre">« Les </span><span class="w" data-chrome="sig_word">garanties</span><span data-chrome="sig_post">, c’est pour les réfrigérateurs, pas pour la biologie. »</span></div>
        <div class="channel" id="ch" data-chrome="handle">@SenaiAksoy</div>`, script: `K.big('#sig', 0.3); K.in('#ch', 2.2);` },
  talking: { overlay: true, body: `${foot}
      <div class="lower-third" id="lt"><div class="who" data-chrome="who">Dr Senai Aksoy</div><div class="role" data-chrome="role">Médecine de la reproduction · Istanbul</div></div>
      ${note}`, script: `K.in('#lt', 0.4); K.in('#note', 2.2);` },
  footage: { overlay: true, body: `${foot}
      <div class="tab" id="tab" data-chrome="footage">Laboratoire FIV · image réelle</div>`, script: `K.pushIn('#foot'); K.in('#tab', 0.4);` },
  cta: { overlay: true, body: `${foot}
      <div class="cta" id="cta">${icons}<div class="sub" id="sub" data-chrome="sub">Abonnez-vous</div></div>`,
    script: `K.in('#cta', 0.4); K.tl.to('#like', { fillOpacity: 1, duration: 0.2 }, 1.4); K.tl.set('#sub', { className: 'sub on' }, 2.2); K.tl.to('#bell', { fillOpacity: 1, duration: 0.2 }, 3.0);` },
};

const page = ({ template, kind, palette, variant, seed, lang, duration }) => {
  const s = SCENES[kind];
  const body = s.overlay ? s.body : `<div class="frame ${s.frame}">
        ${s.body}
      </div>`;
  return `<!doctype html>
<html lang="${lang}" data-template="${template}" data-palette="${palette}" data-variant="${variant}" data-seed="${seed}">
  <!-- Template « ${template} » · scene « ${kind} ». One source, two aspects (aspect.mjs → shorts/).
       Facts: node …/outsider-inside-frame/tools/facts.mjs all . --lang ${lang} · phone floor: node …/outsider-inside-frame/tools/legibility.mjs . -->
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="assets/vendor/gsap.min.js"></script>
    <link rel="stylesheet" href="assets/fonts/fonts.css" />
    <link rel="stylesheet" href="assets/kit/kit.css" />
    <link rel="stylesheet" href="assets/world/world.css" />
    <style>
      .foot { background-image: url(assets/footage/still-16x9.jpg); }
      :root[data-aspect="9x16"] .foot { background-image: url(assets/footage/still-9x16.jpg); background-position: 58% center; }
    </style>
    <script src="assets/kit/kit.js"></script>
    <script src="assets/world/world.js"></script>
  </head>
  <body>
    <div id="root" class="scene scene--${kind}" data-composition-id="main" data-start="0" data-duration="${duration}" data-width="1920" data-height="1080">
      ${s.overlay ? '' : '<div class="bg"></div><div class="deco"></div>'}
      ${body}
    </div>
    <script>
      window.__timelines = window.__timelines || {};
      const K = Kit.start();
      ${s.script}
      const tl = K.done();
      window.__timelines['main'] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
`;
};

function scaffold(template, kind, dest, o) {
  const t = catalog.templates[template];
  if (!t) throw new Error(`unknown template "${template}": ${Object.keys(catalog.templates).join(', ')}`);
  if (t.engine !== 'kit') throw new Error(`"${template}" has its own scenes (see ${t.scenes}); this tool only builds kit worlds`);
  if (!SCENES[kind]) throw new Error(`unknown kind "${kind}": ${Object.keys(SCENES).join(', ')}`);
  const palette = o.palette || t.palettes[0]; const variant = o.variant || 'a';
  if (!t.palettes.includes(palette)) throw new Error(`"${template}" has no palette "${palette}": ${t.palettes.join(', ')}`);
  const out = path.resolve(dest); const A = path.join(out, 'assets');
  fs.mkdirSync(A, { recursive: true });
  fs.writeFileSync(path.join(out, 'index.html'), page({ template, kind, palette, variant, seed: o.seed || 1, lang: o.lang || 'fr', duration: o.duration || 8 }));
  copyDir(path.join(lib, 'worlds', template), path.join(A, 'world'));
  copyDir(path.join(lib, 'kit', 'shared'), path.join(A, 'kit'));
  copyDir(path.join(lib, 'fonts'), path.join(A, 'fonts'));
  fs.mkdirSync(path.join(A, 'vendor'), { recursive: true });
  fs.copyFileSync(path.join(frame, 'assets', 'vendor', 'gsap.min.js'), path.join(A, 'vendor', 'gsap.min.js'));
  fs.mkdirSync(path.join(A, 'footage'), { recursive: true });
  fs.copyFileSync(path.join(frame, 'assets', 'footage', 'lab', 'lab-14-portrait-professional.jpg'), path.join(A, 'footage', 'still-16x9.jpg'));
  fs.copyFileSync(path.join(frame, 'assets', 'footage', 'lab', 'lab-01-portrait-icsi-station.jpg'), path.join(A, 'footage', 'still-9x16.jpg'));
  for (const f of ['hyperframes.json', 'package.json']) fs.copyFileSync(path.join(frame, 'example-layouts', 'chiffre-C', f), path.join(out, f));
  return out;
}

function demoFacts(dest, lang) {
  const rd = (p) => JSON.parse(fs.readFileSync(path.join(frame, p, 'scene-facts.json'), 'utf8'));
  const base = rd('example-components/talking-head');
  const extra = ['example-layouts/verdict-B', 'example-layouts/flux-A', 'example-components/cta', 'example-components/cloture', 'example-components/etiquettes', 'example-components/chapitre'].map(rd);
  for (const e of extra) { base.chrome = { ...e.chrome, ...base.chrome }; for (const f of e.facts) if (!base.facts.some((x) => x.id === f.id)) base.facts.push(f); }
  base.lang = lang; base.video = 'template-library demo (ERA reference facts)';
  base.sources_md = path.relative(dest, path.join(frame, 'example-era', 'era-sources.md')).split(path.sep).join('/');
  fs.writeFileSync(path.join(dest, 'scene-facts.json'), JSON.stringify(base, null, 2) + '\n');
  copyDir(path.join(frame, 'example-layouts', 'chiffre-C', '.facts-cache'), path.join(dest, '.facts-cache'));
}

if (cmd === 'list') {
  for (const [k, t] of Object.entries(catalog.templates)) console.log(`${k.padEnd(18)} ${t.status.padEnd(6)} ${t.engine.padEnd(9)} ${(t.palettes || []).join('/').padEnd(26)} ${t.feel}`);
  console.log('\nkinds:', Object.keys(SCENES).join(', '));
} else if (cmd === 'new' && a1 && a2 && a3) {
  const out = scaffold(a1, a2, a3, { palette: opt('palette'), variant: opt('variant'), seed: opt('seed'), lang: opt('lang'), duration: opt('duration') });
  console.log(`scene → ${out}`);
} else if (cmd === 'demo' && a1) {
  const lang = opt('lang', 'fr');
  const list = a1 === 'all' ? Object.entries(catalog.templates).filter(([, t]) => t.engine === 'kit').map(([k]) => k) : [a1];
  for (const t of list) for (const kind of Object.keys(SCENES)) {
    const d = path.join(lib, 'demos', t, kind);
    fs.rmSync(d, { recursive: true, force: true, maxRetries: 8, retryDelay: 500 });
    scaffold(t, kind, d, { lang, palette: opt('palette'), variant: opt('variant'), seed: 7 });
    demoFacts(d, lang);
  }
  console.log(`demos → ${path.join(lib, 'demos')} (${list.length} template(s) × ${Object.keys(SCENES).length} kinds)`);
} else { console.log('usage: node world.mjs list · new <template> <kind> <dest> [--palette p] [--variant a|b] [--seed n] [--lang fr] [--duration 8] · demo <template|all> [--lang fr]'); process.exitCode = 2; }
