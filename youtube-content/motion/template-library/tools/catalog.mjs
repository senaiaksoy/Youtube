#!/usr/bin/env node
// Template library: policy view of the HyperFrames catalog (heygen-com/hyperframes registry, Apache-2.0).
//
//   node catalog.mjs sync [raw.json]           refresh catalog.json (from `npx hyperframes@latest catalog --json`, or a saved dump)
//   node catalog.mjs find <words…> [--all]     search usable items; --all also lists blocked ones with the reason
//   node catalog.mjs stats
//
// A catalog item is installed into a scene with `npx hyperframes add <name>`, then recoloured with the world's tokens.
// Blocked = cannot appear in a medical video whatever the world: brand or platform look-alikes, proof and testimonial cards (F3),
// logo stings and intros (hard rule), code/product demos with no use here. caption-* items are Shorts-only: 16:9 carries no burned-in subtitles.
import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const lib = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const out = path.join(lib, 'catalog.json');
const RULES = [
  ['brand', /^(apple-|chatgpt|claude-|x-post|x-follow|reddit|tiktok|instagram|spotify|slack|heygen|ios26|macos|liquid-glass-notification|yt-comment|yt-logo|yt-lcd|yt-prism|yt-vertical|vpn-youtube|blue-sweater|north-korea|canopy|lower-third-bild|week-in-merges|ai-answer|ai-chat|vfx-iphone|share-sheet|store-badge|native-notification)/],
  ['proof', /^(testimonial|social-proof|star-rating|trust-strip|logo-wall|avatar-|spotlight-testimonial)/],
  ['intro', /(^logo-|-logo$|logo-|^extruded-logo|wordmark|-intro|^titlecard-lockup|^cta-lockup)/],
  ['product', /^(code-|terminal|app-showcase|product-|signup|onboarding|settings-|menu-|modal-|tabs-|toggle-|cursor-|agent-cursor|dart-cursor|oversized-cursor|magnetic-cursor|multiplayer|browser-|device-|multi-device|parallax-device|sticky-mock|screen-flow|scroll-feed|pull-to-refresh|chat-|typing-indicator|notification-|message-thread|thread-message|typed-prompt|streaming-text|vector-editor|gesture-tap|touch-indicator|press-ripple|swipe-rail|input-feedback|vfx-text-cursor|hw-pipeline-demo)/],
  ['place', /^(us-map|spain-map|nyc-paris|world-map)/],
  ['party', /^(confetti|beat-|rubber-band|caption-emoji|caption-particle)/],
];
const policy = (i) => {
  for (const [why, re] of RULES) if (re.test(i.name)) return why;
  if (/^caption-/.test(i.name)) return 'shorts-only';
  if ((i.tags || []).includes('ad-template')) return 'product';
  return 'ok';
};
const read = () => JSON.parse(fs.readFileSync(out, 'utf8'));
const [cmd, ...rest] = process.argv.slice(2);

if (cmd === 'sync') {
  const raw = rest[0] ? fs.readFileSync(rest[0], 'utf8') : execSync('npx -y hyperframes@latest catalog --json', { encoding: 'utf8', maxBuffer: 1 << 26, env: { ...process.env, HYPERFRAMES_SKIP_SKILLS: '1' } });
  const items = JSON.parse(raw).map((i) => ({ name: i.name, type: i.type, title: i.title, description: (i.description || '').slice(0, 220), tags: i.tags || [], policy: policy(i) }));
  fs.writeFileSync(out, JSON.stringify({ source: 'heygen-com/hyperframes registry', license: 'Apache-2.0', synced: new Date().toISOString().slice(0, 10), items }, null, 1) + '\n');
  console.log(`catalog.json: ${items.length} items`);
} else if (cmd === 'stats') {
  const c = {}; for (const i of read().items) c[i.policy] = (c[i.policy] || 0) + 1;
  console.log(c);
} else if (cmd === 'find' && rest.length) {
  const all = rest.includes('--all'); const words = rest.filter((w) => !w.startsWith('--')).map((w) => w.toLowerCase());
  const hits = read().items.filter((i) => (all || i.policy === 'ok' || i.policy === 'shorts-only') && words.every((w) => `${i.name} ${i.title} ${i.description} ${i.tags.join(' ')}`.toLowerCase().includes(w)));
  for (const i of hits) console.log(`${i.policy.padEnd(11)} ${i.type.padEnd(9)} ${i.name.padEnd(30)} ${i.description.slice(0, 90)}`);
  console.log(`${hits.length} match(es)`);
} else { console.log('usage: node catalog.mjs sync [raw.json] · find <words…> [--all] · stats'); process.exitCode = 2; }
