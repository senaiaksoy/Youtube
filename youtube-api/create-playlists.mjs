/**
 * YouTube Playlist Creator
 *
 * Kullanim:
 *   node youtube-api/create-playlists.mjs         # dry-run
 *   node youtube-api/create-playlists.mjs --apply # gercek olusturma
 */

const BASE_URL = process.env.BASE_URL ?? 'http://localhost:3000';

const playlists = [
  {
    title: 'İlk Kez Tüp Bebek',
    description:
      'Tüp bebek sürecine yeni başlayanlar için temel bilgiler, ilk kararlar, süreç adımları ve en sık sorulan sorular. Daha bilinçli ve daha sakin karar vermek isteyenler için başlangıç rehberi.',
    videoIds: [
      'NLvPH9mZIaE',
      'HRYFoDkjohE',
      'GP809hiOu_Y',
      'kk-_4y0mn4M',
      'sDcaagphlHU',
      '6UwNaQa_di4',
    ],
    privacyStatus: 'public',
  },
  {
    title: 'Embriyo ve Transfer',
    description:
      'Embriyo kalitesi, transfer süreci, dondurulmuş ve taze transfer seçenekleri, tutunma dönemi ve embriyo ile ilgili en kritik karar noktaları hakkında bilimsel ve anlaşılır videolar.',
    videoIds: [
      'yT2dmjxZ3Qs',
      'S8xkWrHylTE',
      'a1yCSFO24Gs',
      '_2-1G9akYgk',
      'wybruaMaIdY',
      '8Dx-f4ea6h4',
      'vwsgOtGVTPY',
      'k_W6KF7NuvA',
    ],
    privacyStatus: 'public',
  },
  {
    title: 'AMH ve Yumurta Rezervi',
    description:
      'AMH, over rezervi, yaş faktörü, hedef yumurta sayısı ve yumurta dondurma hakkında net, bilimsel ve hasta odaklı açıklamalar.',
    videoIds: ['w29IsrwxHWA', 'LyLGywUUipg', 'HRYFoDkjohE'],
    privacyStatus: 'public',
  },
  {
    title: 'Endometriozis ve Kısırlık',
    description:
      'Endometriozis tanısı, doğurganlığa etkisi, tedavi seçenekleri ve tüp bebekle ilişkisi hakkında güncel ve kanıta dayalı videolar.',
    videoIds: ['-FxkIwmlO9g', 'ciH_IHqVrxw', '-blY0f_9WCE'],
    privacyStatus: 'public',
  },
  {
    title: 'Erkek İnfertilitesi',
    description:
      'Sperm analizi, azospermi, TESE ve erkek faktörü kaynaklı infertilite hakkında bilimsel, güncel ve anlaşılır bilgiler.',
    videoIds: ['1pXII-iRU-U', 'RRDTPsS8SVc'],
    privacyStatus: 'public',
  },
  {
    title: 'Hangi Test Gerçekten Gerekli?',
    description:
      'Sık önerilen testlerin, ek işlemlerin ve tüp bebek add-on uygulamalarının gerçekten gerekli olup olmadığını bilimsel verilerle değerlendiren videolar.',
    videoIds: ['b8wT1pAbX3A', 'GP809hiOu_Y', 'oyBpALzZzEU', 'DbCrz_VPyC4', '6UwNaQa_di4', 'wybruaMaIdY'],
    privacyStatus: 'public',
  },
];

async function main() {
  const args = process.argv.slice(2);
  const dryRun = !args.includes('--apply');

  console.log('='.repeat(60));
  console.log('  YouTube Playlist Creator - Dr. Senai Aksoy');
  console.log('='.repeat(60));

  try {
    const statusRes = await fetch(`${BASE_URL}/api/auth/status`);
    const status = await statusRes.json();
    if (!status.connected) {
      console.error('\nYouTube hesabi bagli degil!');
      process.exit(1);
    }
    console.log('YouTube baglantisi aktif\n');
  } catch {
    console.error('\nNext.js sunucusuna erisilemiyor!');
    process.exit(1);
  }

  console.log(`${playlists.length} playlist ${dryRun ? '(DRY RUN)' : '(CANLI - olusturulacak)'}\n`);

  for (const p of playlists) {
    console.log(`  - ${p.title} (${p.videoIds.length} video)`);
  }

  console.log('\nGonderiliyor...\n');

  const res = await fetch(`${BASE_URL}/api/youtube/playlists`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ playlists, dryRun }),
  });

  if (!res.ok) {
    const err = await res.text();
    console.error(`API hatasi ${res.status}: ${err}`);
    process.exit(1);
  }

  const data = await res.json();

  for (const r of data.results) {
    const icon =
      r.status === 'created'
        ? '[created]'
        : r.status === 'dry_run'
          ? '[dry-run]'
          : r.status === 'exists'
            ? '[exists]'
            : '[error]';
    console.log(`  ${icon} ${r.title}`);
    if (r.playlistId) console.log(`     ID: ${r.playlistId}`);
    if (typeof r.videosAdded === 'number') console.log(`     Videolar: ${r.videosAdded}`);
    if (r.error) console.log(`     Hata: ${r.error}`);
  }

  console.log('\n' + '='.repeat(60));
}

main().catch((e) => {
  console.error('Fatal error:', e);
  process.exit(1);
});
