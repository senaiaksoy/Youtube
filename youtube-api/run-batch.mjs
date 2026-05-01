/**
 * YouTube SEO Batch Update Runner
 *
 * Kullanım:
 *   node youtube-api/run-batch.mjs                  # dry-run (önizleme)
 *   node youtube-api/run-batch.mjs --apply          # gerçek güncelleme
 *   node youtube-api/run-batch.mjs --video b8wT1pAbX3A   # tek video
 *
 * Ön koşul: Next.js dev server çalışıyor olmalı (npm run dev)
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { loadFixes } from './load-fixes.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const FIXES_PATH = path.join(__dirname, 'video_fixes.json');
const BASE_URL = process.env.BASE_URL ?? 'http://localhost:3000';

async function main() {
  const args = process.argv.slice(2);
  const dryRun = !args.includes('--apply');
  const videoFilter = args.find((a, i) => args[i - 1] === '--video');

  console.log('═'.repeat(60));
  console.log('  YouTube SEO Batch Updater — Dr. Senai Aksoy');
  console.log('═'.repeat(60));

  // ── Auth durumunu kontrol et ──
  try {
    const statusRes = await fetch(`${BASE_URL}/api/auth/status`);
    const status = await statusRes.json();
    if (!status.connected) {
      console.error('\n❌ YouTube hesabı bağlı değil!');
      console.error(`   Tarayıcıda ${BASE_URL} adresine gidip "Google ile Bağlan" butonuna tıklayın.`);
      console.error('   Bağlantı tamamlandıktan sonra bu scripti tekrar çalıştırın.\n');
      process.exit(1);
    }
    console.log('✅ YouTube bağlantısı aktif');
    if (status.hasRefreshToken) console.log('✅ Refresh token mevcut');
  } catch (e) {
    console.error('\n❌ Next.js sunucusuna erişilemiyor!');
    console.error(`   Önce sunucuyu başlatın: cd D:\\A-klasör\\Youtube && npm run dev`);
    console.error(`   Ardından bu scripti tekrar çalıştırın.\n`);
    process.exit(1);
  }

  // ── Düzeltmeleri yükle ──
  if (!fs.existsSync(FIXES_PATH)) {
    console.error(`\n❌ ${FIXES_PATH} bulunamadı!`);
    process.exit(1);
  }

  let fixes = loadFixes(FIXES_PATH);

  if (videoFilter) {
    fixes = fixes.filter((f) => f.video_id === videoFilter);
    if (!fixes.length) {
      console.error(`\n❌ ${videoFilter} video_fixes.json'da bulunamadı`);
      process.exit(1);
    }
  }

  console.log(`\n📦 ${fixes.length} video ${dryRun ? '(DRY RUN — değişiklik yapılmayacak)' : '(CANLI — değişiklikler UYGULANACAK)'}`);

  if (!dryRun) {
    console.log('\n⚠️  Gerçek güncelleme yapılacak. Devam? (Ctrl+C ile iptal, Enter ile devam)');
    await new Promise((resolve) => {
      process.stdin.once('data', resolve);
    });
  }

  // ── Batch API çağrısı ──
  console.log('\n🚀 Güncelleme başlatılıyor...\n');

  const res = await fetch(`${BASE_URL}/api/youtube/batch-update`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ fixes, dryRun }),
  });

  if (!res.ok) {
    const err = await res.text();
    console.error(`❌ API hatası ${res.status}: ${err}`);
    process.exit(1);
  }

  const data = await res.json();

  // ── Sonuçları göster ──
  for (const r of data.results) {
    const icon = r.status === 'updated' ? '✅'
               : r.status === 'dry_run' ? '🔍'
               : r.status === 'skipped' ? '⏭️'
               : '❌';

    console.log(`  ${icon} ${r.video_id}: ${r.status}`);

    if (r.changes) {
      for (const [key, val] of Object.entries(r.changes)) {
        if (key === 'title') {
          console.log(`     Başlık: "${val.old?.slice(0, 50)}…" → "${val.new?.slice(0, 50)}"`);
        } else if (key === 'description') {
          console.log(`     Açıklama hook güncellendi`);
        } else if (key === 'tags') {
          console.log(`     Tags: +${val.new?.split(', ').length - val.old?.split(', ').length} yeni`);
        }
      }
    }
    if (r.error) {
      console.log(`     Hata: ${r.error}`);
    }
  }

  // ── Özet ──
  console.log('\n' + '═'.repeat(60));
  const s = data.summary;
  console.log(`  ✅ Güncellendi: ${s.updated}`);
  console.log(`  🔍 Dry run: ${s.dry_run}`);
  console.log(`  ⏭️  Atlandı: ${s.skipped}`);
  console.log(`  ❌ Hata: ${s.errors}`);
  console.log('═'.repeat(60));

  // ── Log kaydet ──
  const logPath = path.join(__dirname, `batch-log-${Date.now()}.json`);
  fs.writeFileSync(logPath, JSON.stringify(data, null, 2), 'utf-8');
  console.log(`\n📄 Log: ${logPath}`);
}

main().catch((e) => {
  console.error('Fatal error:', e);
  process.exit(1);
});
