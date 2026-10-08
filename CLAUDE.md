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
  `@DocentDrSenaiAksoy` (`UCbO5qpAnmaQPBJlGMM9ITiw`, Turkce). Kanallari asla
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
