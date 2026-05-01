/**
 * Sync homepage playlists and channel shelves.
 *
 * Usage:
 *   node youtube-api/sync-homepage.mjs         # dry-run
 *   node youtube-api/sync-homepage.mjs --apply # live sync
 */

import fs from 'fs';
import path from 'path';

const BASE_URL = process.env.BASE_URL ?? 'http://localhost:3000';
const CONFIG_PATH = path.join(process.cwd(), 'youtube-api', 'homepage-config.json');

function readConfig() {
  return JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));
}

async function main() {
  const args = process.argv.slice(2);
  const dryRun = !args.includes('--apply');
  const config = readConfig();

  console.log('='.repeat(64));
  console.log('  YouTube Homepage Sync - Dr. Senai Aksoy');
  console.log('='.repeat(64));

  const statusRes = await fetch(`${BASE_URL}/api/auth/status`);
  const status = await statusRes.json();
  if (!status.connected) {
    console.error('\nYouTube hesabi bagli degil.');
    process.exit(1);
  }

  console.log(`\nPlaylist sayisi: ${config.playlists.length}`);
  console.log('Ana sayfa sirasi:');
  for (const [index, title] of config.homepageOrder.entries()) {
    console.log(`  ${index + 1}. ${title}`);
  }

  const res = await fetch(`${BASE_URL}/api/youtube/homepage`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ dryRun }),
  });

  if (!res.ok) {
    const errorText = await res.text();
    console.error(`\nAPI hatasi ${res.status}: ${errorText}`);
    process.exit(1);
  }

  const data = await res.json();

  console.log(`\n${dryRun ? 'DRY RUN' : 'CANLI'} sonuc:\n`);
  for (const item of data.playlistResults) {
    console.log(`  [${item.status}] ${item.title}`);
    if (item.playlistId) console.log(`     Playlist ID: ${item.playlistId}`);
    if (typeof item.videosSet === 'number') console.log(`     Video sayisi: ${item.videosSet}`);
    if (item.error) console.log(`     Hata: ${item.error}`);
  }

  console.log('\nSection sync:');
  console.log(`  Durum: ${data.sectionResult.status}`);
  if (data.sectionResult.desiredTitles?.length) {
    for (const [index, title] of data.sectionResult.desiredTitles.entries()) {
      console.log(`  ${index + 1}. ${title}`);
    }
  }
  if (data.sectionResult.error) {
    console.log(`  Hata: ${data.sectionResult.error}`);
  }

  console.log('\nOzet:');
  console.log(`  Created: ${data.summary.created}`);
  console.log(`  Updated: ${data.summary.updated}`);
  console.log(`  Unchanged: ${data.summary.unchanged}`);
  console.log(`  Dry run: ${data.summary.dryRun}`);
  console.log(`  Errors: ${data.summary.errors}`);
  console.log('\n' + '='.repeat(64));
}

main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});
