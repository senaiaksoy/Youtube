# Memory

## Kanal
**Dr. Senai Aksoy** — Doç. Dr., kadın hastalıkları/infertilite & FIV (tüp bebek) uzmanı.
YouTube kanalı (@SenaiAksoy, UC51eCoXFnN1DiBd1dWcJpPQ): doğurganlık, tüp bebek, embriyoloji.
10.372 abone · 313 video. Diller: ağırlıklı **Fransızca**, ayrıca TR/EN/AR dublaj+altyazı.
Site: draksoyivf.com

## YouTube SEO — Çekirdek Kurallar
1. **Başlık kancası kuralı:** Başlığın ilk kelimeleri hasta diliyle fayda/merak + soru olmalı. Teknik kısaltmayla BAŞLAMA (örn. "IMSI, PICSI, MACS" gibi). Kanıt: bu başlık %1,2 CTR; sade soru başlıkları %8–12 CTR.
2. **İyi CTR kalıbı:** "Qualité du sperme : 5 facteurs à corriger" (%9,8), "Inositol et SOPK : utile ou surestimé ?" (%12,4) — kopyala.
3. **Sağlıklı CTR eşiği:** %6+ iyi. Kanal ortalaması %6,4. %4 altı → thumbnail/başlık testi aç.
4. **Yeni video zayıf açılırsa (CTR <%3):** hemen Studio → İçerik → video → "Küçük resim testi" ile 3 alternatif kapak + başlık dene. Bekleme.
5. **Shorts'ta düşük CTR (%1–3) NORMAL** — panik yapma. Ama Shorts abone getirmiyor (0–2/video); rolünü sorgula.
6. **Metadata zaten iyi:** açıklamalarda bölüm/zaman damgası, blog linki, hashtag, çok dilli altyazı var. Bunları koru.
7. **Görüntüleme düşüşü ≠ thumbnail sorunu.** Önce trafik kaynağına bak (Studio: önerilenler/arama). Arama düşükse evergreen soru-videosu üret; önerilenler düşükse bitiş ekranı+kartla videoları birbirine bağla.
8. **Evergreen formatı işe yarıyor:** tek konu + soru başlığı (Clomid, Polypes, Azoospermie, Hystéroscopie). Bunlardan daha çok üret.

## Referans Performans (28 gün, 2026-07-01)
- Kanal: 19.032 görüntüleme · 158.682 gösterim · **CTR %6,3** · +196 abone · €16,00 · 716,1 saat izlenme
- Trafik atfı (YouTube): görüntüleme ~ortalama/yatay; geçen ayki düşüş (önerilen −%23, arama −%20) TOPARLANDI
- Müdahale (CTR <%3 uzun video): DHEA/hormone de croissance en FIV (12:41, %2,0) → thumbnail testi
- Detay tablo + analiz: memory/youtube-seo-rules.md

## Tercihler
- Yanıtlar kısa ve net, gereksiz açıklama yok.
- Tıbbi/teknik konularda jinekolog-FIV uzmanı perspektifi.
- Dil: Türkçe (kanal içeriği Fransızca).

## YouTube API Pipeline Skill

Kalici YouTube API islemleri icin `.claude/skills/yt-pipeline/` kullanilir.
Yeni tek kullanimlik Python scriptleri yazma; altyazi/caption, metadata,
playlist, kanal dogrulama ve toplu SRT duzeltmeleri icin skill altindaki
`scripts/yt_*.py` CLI'larini calistir.

- Interpreter hard rule: `py -3.12`. `googleapiclient` varsayilan Python'da yok.
- Windows encoding hard rule: Python scriptleri UTF-8 cikti disiplinini kullanir;
  ara/veri denetimleri konsola degil acik UTF-8 dosyalara yazilir.
- Kanal ayrimi hard rule: `--channel fr` = `@SenaiAksoy`
  (`UC51eCoXFnN1DiBd1dWcJpPQ`, Fransizca); `--channel tr` =
  `@DocentDrSenaiAksoy` (`UCbO5qpAnmaQPBJlGMM9ITiw`, Turkce); `--channel en` =
  `@DrAksoyFertility` (`UCo3ZeBXk0ng-OigXd9jqJqQ`, Ingilizce). Kanallari asla
  konsolide etme. Her mutasyondan once scriptin live `mine=True` kanal
  dogrulamasini goster; uyusmazlikta dur.
- OAuth: canonical tokenlar `youtube-api/token.senaiaksoy.20260510-193158.json`
  (FR) ve `youtube-api/token.json` (TR). `token.wrong-*` dosyalarina veya baska
  legacy tokenlara otomatik fallback yapma; gerekirse `yt_oauth.py` ile tek
  seferlik dogru token uret.
- Mutasyon kapisi: upload/replace/delete/update/add islemleri once dry-run,
  sonra kullanici onayi ile `--go`.
- FR metin review: Fransizca altyazi/aciklama/baslik metni uretildiyse yayina
  almadan once Dr. Aksoy'a goster. Yeni tibbi makale/uzun metin uretiliyorsa
  draksoyivf `CLAUDE.md` stil rehberi gate'i gecerlidir.

## HyperFrames Motion Tasarım Sistemi (2026-10-15'ten itibaren)

- Ana şablon: `youtube-content/motion/outsider-inside-frame/frame.md` ("Outsider Inside" —
  kâğıt / mürekkep / kırmızı kalem; iddia italik + üstü çizilir, kanıt düz yazı; hüküm damgası;
  her rakamın yanında referans kartı).
- Hard rule: 2026-10-15 ve sonrası açılan her yeni HyperFrames projesinde bu `frame.md`
  projenin köküne kopyalanır; ayrıca DESIGN.md yazılmaz, HyperFrames house-style varsayılanları
  (glow, gradient, ghost text, nefes alan arka plan, flash/glitch geçişler) kullanılmaz.
- Eski projelere (`projects/fiv-apres-quarante-ans-hyperframes`, `videos/bhcg-*`,
  `youtube-content/motion/intro-pilot`) dokunma; kendi frame.md/DESIGN.md'leriyle kalırlar.
- Ana şablonu değiştirmek tüm gelecek videoları etkiler: önce Dr. Aksoy'a sor.
- Hard rule (kaynaktan sahneye): ekrandaki her rakam, bulgu, hüküm ve künye `scene-facts.json` üzerinden scriptin
  `-sources.md` iddia ID'sine (ve PMID'ye) bağlanır; künye elle yazılmaz. Render öncesi
  `node youtube-content/motion/outsider-inside-frame/tools/facts.mjs all <proje> --lang <fr|tr|en>` geçmeli.
- Hard rule (telefon okunurluğu, 2026-10-16): motion grafikte görünen her yazı ≥ 40 px @1080 kısa kenar
  (16:9'da 2.1cqw; künye, etiket, [1] işareti dahil). Sığmıyorsa yazı kısaltılır, küçültülmez. Render öncesi
  `node youtube-content/motion/outsider-inside-frame/tools/legibility.mjs <proje>` geçmeli.
- Hard rule (intro yok, 2026-10-16): kanal intro'su / logo bumper'ı hiçbir videoda kullanılmaz; video
  Dr. Aksoy'la (tam kadraj) açılır ve doğrudan içeriğe girer.
- Hard rule (çeşitlilik, 2026-10-17): her video bir seriye ait (mythe · labo · questions · chiffres · conseils), her
  serinin kendi kâğıdı var (frame.md § Series & Variety). Projede `look.json` yazılır; render öncesi
  `node youtube-content/motion/outsider-inside-frame/tools/variety.mjs check <proje>` geçmeli, final render sonrası
  `variety.mjs log <proje> --lang <fr|tr|en>`. Videoda en fazla 2 kâğıt.
- Shorts (2026-10-17): sahne tek kaynak (`index.html`, 16:9); dikey düzen aynı dosyada `:root[data-aspect="9x16"]` ile.
  `tools/aspect.mjs <proje>` → `<proje>/shorts/` (elle düzenlenmez); legibility + check orada da geçmeli (alt %18 ve sağ
  ikon sütununda yazı yok).
- Hard rule (Shorts altyazı, 2026-10-18): her Shorts'a ekranda pop-up altyazı konur (Dr. Aksoy'un söylediği, kart başına 1–3 kelime,
  Plex Sans SemiBold 62 px, kâğıt kutu üzerinde mürekkep, 100 ms pop; zıplama/emoji/kelime rengi yok). `node youtube-content/motion/outsider-inside-frame/tools/captions.mjs`
  ile ASS üretilir, ffmpeg `ass=` ile basılır; metin yayından önce kayda karşı okunur. Altyazı bandı (yüksekliğin %76,5–82'si) Shorts
  sahnelerinde boş kalır (legibility.mjs denetler). 16:9 ana videoda gömülü altyazı yok (yalnızca YouTube altyazı izi).
- Hard rule (AI espri sahneleri, 2026-10-18): scriptteki espri, örnek ve canlandırılan absürt sahneler (`[GAG]`) Higgsfield ile
  3–8 sn'lik AI kliplerle gösterilebilir; varsayılan görünüm gerçekçi sinematik, videoda tek görünüm, video başına 4–8 sahne,
  model sesi kapalı, tüm süre illustration-tab. Bilgi (rakam/hüküm/künye) asla AI klipte değil. İsteğe bağlı kurgusal « Monsieur »
  karakteri. Gametler yalnızca açıkça çizgi film karakter olarak ve yalnızca espri sahnesinde. Gerçek kişi (ünlü, Dr. Aksoy, hasta),
  logo/marka, görselde üretilmiş yazı, embriyo/ultrason/lab, gerçekmiş gibi klinik sahne yok. Sayı, görünüm ve kredi tavanı tek
  onay mesajında (frame.md § AI gag scenes).
- Hard rule (tohum, 2026-10-17): `node youtube-content/motion/outsider-inside-frame/tools/pen.mjs apply <sahneler…>` facts apply'dan
  önce çalışır (videonun bütün sahneleri, akış sırasıyla). Kırmızı kalem izleri yalnızca Dr. Aksoy'un gerçek izleridir, asla
  üretilmez; rough.js (`assets/ink`) yalnızca siyah mürekkepli şema kutu/ok/çubukları içindir. Şema levhalarında
  (`assets/schema`, Servier CC BY 4.0) künye satırı ekranda kalır.
- Kurulum adımları ve eksik varlık listesi: `youtube-content/motion/outsider-inside-frame/README.md`.
