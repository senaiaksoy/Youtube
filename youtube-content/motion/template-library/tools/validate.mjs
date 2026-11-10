#!/usr/bin/env node
// Template library: runs every gate on the demo scenes of a world, in both aspects, and writes demos/report.json.
//
//   node validate.mjs <template|all> [--kinds claim,bars] [--lang fr] [--jobs 3] [--no-check]
//
// Per scene: facts apply + verify → legibility 16:9 → aspect.mjs → legibility 9:16 → hyperframes check (both aspects).
import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const lib = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const T = path.resolve(lib, '..', 'outsider-inside-frame', 'tools');
const catalog = JSON.parse(fs.readFileSync(path.join(lib, 'templates.json'), 'utf8'));
const args = process.argv.slice(2);
const opt = (n, d) => { const i = args.indexOf(`--${n}`); return i >= 0 ? args[i + 1] : d; };
const target = args.find((a) => !a.startsWith('--')) || 'all';
const lang = opt('lang', 'fr'); const jobs = +opt('jobs', 3); const noCheck = args.includes('--no-check');
const kinds = opt('kinds', catalog.kinds.join(',')).split(',');
const worlds = target === 'all' ? Object.entries(catalog.templates).filter(([, t]) => t.engine === 'kit').map(([k]) => k) : [target];

const run = (cmd, argv, cwd, ms = 150000) => new Promise((res) => {
  const p = spawn(cmd, argv, { cwd, shell: cmd === 'npx', env: { ...process.env, HYPERFRAMES_SKIP_SKILLS: '1', GEMINI_API_KEY: '' } });
  let out = ''; p.stdout.on('data', (d) => { out += d; }); p.stderr.on('data', (d) => { out += d; });
  const k = setTimeout(() => { out += '\n[timeout]'; p.kill(); }, ms);
  p.on('close', (code) => { clearTimeout(k); res({ code, out }); });
});
const gate = async (name, cmd, argv, cwd, r) => {
  const x = await run(cmd, argv, cwd); r.gates[name] = x.code === 0;
  if (x.code !== 0) r.fails.push(`${name}: ${x.out.split(/\r?\n/).filter((l) => /✖|error|fail|timeout/i.test(l)).slice(0, 8).join(' | ').slice(0, 700)}`);
};
async function one(world, kind) {
  const d = path.join(lib, 'demos', world, kind); const r = { world, kind, gates: {}, fails: [] };
  await gate('facts-apply', 'node', [path.join(T, 'facts.mjs'), 'apply', d, '--lang', lang], lib, r);
  await gate('facts-verify', 'node', [path.join(T, 'facts.mjs'), 'verify', d, '--lang', lang], lib, r);
  await gate('legibility-16x9', 'node', [path.join(T, 'legibility.mjs'), d, '--samples', '12'], lib, r);
  await gate('aspect', 'node', [path.join(T, 'aspect.mjs'), d], lib, r);
  await gate('legibility-9x16', 'node', [path.join(T, 'legibility.mjs'), path.join(d, 'shorts'), '--samples', '12'], lib, r);
  if (!noCheck) {
    await gate('check-16x9', 'npx', ['-y', 'hyperframes@0.9.29', 'check'], d, r);
    await gate('check-9x16', 'npx', ['-y', 'hyperframes@0.9.29', 'check'], path.join(d, 'shorts'), r);
  }
  console.log(`${r.fails.length ? '✖' : '✔'} ${world}/${kind}${r.fails.length ? `\n    ${r.fails.join('\n    ')}` : ''}`);
  return r;
}
const queue = worlds.flatMap((w) => kinds.map((k) => [w, k])); const results = [];
await Promise.all(Array.from({ length: jobs }, async () => { while (queue.length) { const [w, k] = queue.shift(); results.push(await one(w, k)); } }));
const report = path.join(lib, 'demos', 'report.json');
const prev = fs.existsSync(report) ? JSON.parse(fs.readFileSync(report, 'utf8')) : [];
const merged = [...prev.filter((p) => !results.some((r) => r.world === p.world && r.kind === p.kind)), ...results];
fs.writeFileSync(report, JSON.stringify(merged, null, 1));
const bad = results.filter((r) => r.fails.length).length;
console.log(`\n${results.length - bad}/${results.length} scenes passed every gate`);
process.exitCode = bad ? 1 : 0;
