/**
 * YouTube Playlist Creator
 *
 * Kullanım:
 *   node youtube-api/create-playlists.mjs              # dry-run
 *   node youtube-api/create-playlists.mjs --apply       # gerçek oluşturma
 */

const BASE_URL = process.env.BASE_URL ?? 'http://localhost:3000';

const playlists = [
  {
    title: '🔬 IVF Add-on Gerçekleri (Kanıta Dayalı Eleştiri)',
    description:
      'Tüp bebek tedavisinde ekstra önerilen işlemler (add-on) gerçekten işe yarıyor mu? Doç. Dr. Senai Aksoy, Cochrane ve ESHRE verileriyle her birini tek tek değerlendiriyor. Kanıta dayalı, bağımsız, reklamsız.',
    videoIds: [
      'b8wT1pAbX3A', // ERA Testi JAMA Analizi
      '-i981BtfKVY', // ERA Testi Nedir? (Short)
      'wybruaMaIdY', // Embryo Glue
      'oyBpALzZzEU', // Rahim Çizme
      'DbCrz_VPyC4', // Bağışıklık Aşısı ve Serumları
      'GP809hiOu_Y', // Histeroskopi
      '6UwNaQa_di4', // Soğan Suyu ve Akupunktur
      '8Dx-f4ea6h4', // Embriyoskop ve Yapay Zeka
    ],
    privacyStatus: 'public',
  },
  {
    title: '🧬 Embriyo ve Transfer Süreci',
    description:
      'Embriyo kalitesi nasıl değerlendirilir? Transfer hazırlığında hangi protokol seçilmeli? Dondurulmuş ve taze transfer farkı nedir? Bilimsel verilerle embriyo ve transfer sürecinin tüm aşamaları.',
    videoIds: [
      'yT2dmjxZ3Qs', // 4AA, 3BB, 5BC Embriyo
      'S8xkWrHylTE', // Dondurulmuş Embriyo Transferi
      'wybruaMaIdY', // Embryo Glue (çapraz)
      '8Dx-f4ea6h4', // Embriyoskop (çapraz)
    ],
    privacyStatus: 'public',
  },
  {
    title: '👩‍⚕️ Kadın Üreme Sağlığı',
    description:
      'Endometriozis, vajinal mikrobiyota, yumurta dondurma ve kadın üreme sağlığını etkileyen faktörler. Doç. Dr. Senai Aksoy\'dan bilimsel ve güncel bilgiler.',
    videoIds: [
      '-FxkIwmlO9g', // Endometriozis ve Kısırlık
      '-blY0f_9WCE', // Vajinal Mikrobiyota
      'w29IsrwxHWA', // Yumurta Dondurma
      'zGzzDHRkjN4', // Mantar mı, Bakteriyel Vajinoz mu
    ],
    privacyStatus: 'public',
  },
  {
    title: '👨‍⚕️ Erkek Faktörü',
    description:
      'Erkek infertilitesi, azospermi ve sperm analizi hakkında bilimsel ve güncel bilgiler.',
    videoIds: [
      '1pXII-iRU-U', // Azospermide İzotretinoin
    ],
    privacyStatus: 'public',
  },
];

async function main() {
  const args = process.argv.slice(2);
  const dryRun = !args.includes('--apply');

  console.log('═'.repeat(60));
  console.log('  YouTube Playlist Creator — Dr. Senai Aksoy');
  console.log('═'.repeat(60));

  // Auth kontrolü
  try {
    const statusRes = await fetch(`${BASE_URL}/api/auth/status`);
    const status = await statusRes.json();
    if (!status.connected) {
      console.error('\n❌ YouTube hesabı bağlı değil!');
      process.exit(1);
    }
    console.log('✅ YouTube bağlantısı aktif\n');
  } catch {
    console.error('\n❌ Next.js sunucusuna erişilemiyor!');
    process.exit(1);
  }

  console.log(`📦 ${playlists.length} playlist ${dryRun ? '(DRY RUN)' : '(CANLI — oluşturulacak)'}\n`);

  for (const p of playlists) {
    console.log(`  📋 ${p.title} (${p.videoIds.length} video)`);
  }

  // API çağrısı
  console.log('\n🚀 Gönderiliyor...\n');

  const res = await fetch(`${BASE_URL}/api/youtube/playlists`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ playlists, dryRun }),
  });

  if (!res.ok) {
    const err = await res.text();
    console.error(`❌ API hatası ${res.status}: ${err}`);
    process.exit(1);
  }

  const data = await res.json();

  for (const r of data.results) {
    const icon = r.status === 'created' ? '✅' : r.status === 'dry_run' ? '🔍' : '❌';
    console.log(`  ${icon} ${r.title}`);
    if (r.playlistId) console.log(`     ID: ${r.playlistId}`);
    if (r.videosAdded) console.log(`     Videolar: ${r.videosAdded} eklendi`);
    if (r.error) console.log(`     Hata: ${r.error}`);
  }

  console.log('\n' + '═'.repeat(60));
}

main().catch((e) => {
  console.error('Fatal error:', e);
  process.exit(1);
});
