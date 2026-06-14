# Thumbnail Üretim Kuralları ve Master Prompt

Kanal: Dr. Senai Aksoy (@SenaiAksoy) — infertilite / FIV
Amaç: yüksek CTR'li, tutarlı markalı kapaklar. Hedef CTR %6+ (Shorts hariç).

## İş akışı
1. Kullanıcı KENDİ gerçek fotoğrafını verir (AI yüz KULLANMA — uzman markası gerçek yüzle güven kazanır).
2. Görsel aracında (Nano Banana/Gemini, ChatGPT görsel, Midjourney `--cref`) fotoğrafı referans ver.
3. Aşağıdaki master prompt'ta 3 değişkeni doldur: DUYGU, KONU GÖRSELİ, METİN.
4. Metni model bozuk yazarsa o satırı sil, yazıyı Canva'da ekle (en garanti yol).

## SABİT marka çıpaları (her videoda aynı)
- Yüze %99 sadık kal; güzelleştirme/inceltme/yaşlandırma YOK ("do not beautify" satırı kritik).
- Giysi: temiz beyaz önlük (veya lacivert scrubs). Günlük tişört / marka logosu YOK.
- Font ailesi: kalın sans-serif, sarı metin, koyu kontur + gölge.
- Küçük beyaz rozet: "FIV 2026". Klinik logosu (önlükte/köşede).
- Metin: 3-4 kelime, max 2 satır. Telefonda (320px) okunmuyorsa font büyüt.

## ÇEŞİTLİLİK — videodan videoya DEĞİŞTİR (kontrollü varyasyon)
Çıpalar sabit, gerisi değişir. "Tema aynı, kostüm değişir." Kural: art arda 3 video
asla aynı DÜZEN + aynı RENK + aynı POZ olmasın.

- **DÜZEN:** A) doktor sağda / metin solda · B) doktor solda / metin sağda ·
  C) tam ekran tıbbi görsel + altta şerit metin + doktor küçük köşede.
- **POZ/DUYGU:** güven veren · kaşı çatık/kaygılı · eliyle işaret eden · şaşkın/soru soran.
- **VURGU RENGİ (glow):** sperm/erkek → cyan · yumurtalık/SOPK → mor ·
  embriyo/transfer → amber · enfeksiyon/uyarı → kırmızı. (Sarı metin sabit kalır.)
- **PLAN/YAKINLIK:** büyük yakın yüz · göğüsten · doktor küçük + tıbbi görsel hâkim.
- **GÖRSEL STİLİ:** gerçek ultrason · 3B anatomik render · mikroskop — dönüşümlü kullan.

Mevcut 5 kapak hep "DÜZEN A + cyan + göğüsten" oldu; bir sonrakiler B/C, mor/amber,
farklı poz ile çeşitlensin.

## MASTER PROMPT (kopyala, köşeli parantezleri doldur — varyasyon için DÜZEN/POZ/RENK/PLAN değiştir)

Using the attached photo of me as the EXACT reference, create a 16:9 YouTube
thumbnail (1280x720). Keep my face, identity, skin tone, head and glasses 99%
identical to the photo — do not beautify, slim, age, or alter my features; this
is a real doctor's personal brand and the face must stay recognizable. Replace my
clothing with a crisp white doctor's coat over a light shirt, and remove any casual
t-shirt or brand logos. Cleanly cut me out and place me on the [DÜZEN: RIGHT third /
LEFT third] of the frame, [PLAN: chest up / tight close-up of my face / smaller so
the medical visual dominates], with a [POZ: confident reassuring / concerned
questioning / pointing with my hand / surprised] expression and a subtle bright rim
light plus a thin edge glow around my silhouette. Fill the OTHER side with a softly
blurred, high-contrast medical visual showing [KONU GÖRSELİ: ...] in
[GÖRSEL STİLİ: a real ultrasound scan / a 3D anatomical render / a microscope view],
dark navy-to-teal gradient with one bright [VURGU RENGİ: cyan / purple / amber / red]
accent glow; keep the text side clean. Place bold text there: large yellow headline
"[METİN: ...]" in a heavy sans-serif font with dark outline and drop shadow, plus a
small white badge "FIV 2026". Text must be sharp, correctly spelled, readable on a
phone. Cinematic studio lighting, ultra sharp, professional, no watermark.

## Değişken örnekleri
- DUYGU: kaygı/uyarı videosu → "concerned questioning"; bilgi/güven videosu → "confident reassuring"
- KONU GÖRSELİ örnekleri:
  - Sperm seçimi: "a single sperm cell selected by a micro-pipette under a microscope"
  - Yumurtalık/SOPK: "an ultrasound image of a polycystic ovary"
  - Embriyo transferi: "a blastocyst embryo under a microscope, glowing"
  - Endometriyum: "an ultrasound of the uterine lining"
- METİN: hasta dilinde kısa soru. Teknik kısaltmayla BAŞLAMA (IMSI/PICSI vb. battı, %1,2 CTR).

## Kanıt
- Başarısız: "IMSI, PICSI, MACS ..." başlık → %1,2 CTR.
- Başarılı kalıp: "Qualité du sperme : 5 facteurs à corriger" %9,8 · "Inositol et SOPK : utile ou surestimé ?" %12,4.

## ÖNEMLİ — A/B testi geçmişi olan videolarda kapak değiştirme (otomasyon kısıtı)
"A/B testi tamamlandı" rozetli videolarda canlı kapak "test kazananı" olarak kilitlidir.
- Otomatik dosya yükleme (file_upload) yeni görseli "seçenek" olarak ekler AMA canlı kapak yapamaz; Kaydet çoğu kez DONAR ve değişiklik işlenmez.
- Bu videolarda BAŞTAN MANUEL yol izle:
  1. Video → Küçük resim bölümü (birden çok kapak görünür).
  2. Yeni kapağın ⋮ Seçenekler → "Küçük resim olarak ayarla" (veya kapağa tıklayıp seç).
  3. Eski A/B test kapağını ⋮ → Kaldır (isteğe bağlı).
  4. Kaydet.
- Kalıcı çözüm: bu videoların A/B test geçmişini temizlersen sonraki otomatik yüklemeler sorunsuz çalışır.
- A/B test geçmişi OLMAYAN videolarda otomatik yükleme sorunsuz çalışıyor (kanıt: IMSI, Endomètre, Varicocèle).

## Video ID referansları (thumbnail işleri)
- IMSI/PICSI/MACS: pqc9UgCIqo0 (✅ kapak güncellendi)
- Endomètre avant transfert: Uw2xfxw7N48 (✅ güncellendi)
- Varicocèle Opération ou FIV: gBrcdndP5XI (✅ güncellendi)
- Fibromes utérins peuvent-ils rendre infertile: j-JkDrle5IU (⚠️ A/B test — manuel; dosya yüklü: thumb-fibromes-v1)
- Kyste ovarien fonctionnel: FlVV8qNhJXU (⚠️ A/B test — manuel; dosya yüklü: thumb-kyste-v1)
