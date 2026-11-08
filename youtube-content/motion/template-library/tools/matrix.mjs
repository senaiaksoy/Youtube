#!/usr/bin/env node
// Template library: runs validate.mjs over every non-default palette, with variant b, in TR and EN.
//   node matrix.mjs [--kinds claim,figure,bars,process,verdict] [--jobs 4]
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const lib = path.resolve(here, '..');
const cat = JSON.parse(fs.readFileSync(path.join(lib, 'templates.json'), 'utf8'));
const args = process.argv.slice(2);
const opt = (n, d) => { const i = args.indexOf(`--${n}`); return i >= 0 ? args[i + 1] : d; };
const kinds = opt('kinds', 'claim,figure,bars,process,verdict'); const jobs = opt('jobs', '4');
let fails = 0, total = 0;
for (const [w, t] of Object.entries(cat.templates)) {
  if (t.engine !== 'kit') continue;
  for (const [palette, lang] of [[t.palettes[1], 'tr'], [t.palettes[2], 'en']]) {
    spawnSync('node', [path.join(here, 'world.mjs'), 'demo', w, '--lang', lang, '--palette', palette, '--variant', 'b'], { cwd: lib, stdio: 'ignore' });
    const r = spawnSync('node', [path.join(here, 'validate.mjs'), w, '--lang', lang, '--kinds', kinds, '--jobs', jobs], { cwd: lib, encoding: 'utf8' });
    const lines = r.stdout.split(/\r?\n/);
    const bad = lines.filter((l) => l.startsWith('✖') || l.startsWith('    '));
    total += kinds.split(',').length; fails += lines.filter((l) => l.startsWith('✖')).length;
    console.log(`${w} ${palette} ${lang} b: ${lines.filter((l) => /scenes passed/.test(l)).join('')}`);
    for (const b of bad) console.log(`  ${b.slice(0, 400)}`);
  }
}
console.log(`\nmatrix: ${total - fails}/${total} scenes passed every gate`);
process.exitCode = fails ? 1 : 0;
