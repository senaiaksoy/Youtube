# Thumbnail Üretim Kuralları ve Master Prompt

Kanal: Dr. Senai Aksoy (@SenaiAksoy) — infertilite / FIV
Amaç: yüksek CTR'li, tutarlı markalı kapaklar. Hedef CTR %6+ (Shorts hariç).

## İş akışı
1. Kullanıcı KENDİ gerçek fotoğrafını verir (AI yüz KULLANMA — uzman markası gerçek yüzle güven kazanır).
2. Görsel aracında (Nano Banana/Gemini, ChatGPT görsel, Midjourney `--cref`) fotoğrafı referans ver.
3. Aşağıdaki master prompt'ta 3 değişkeni doldur: DUYGU, KONU GÖRSELİ, METİN.
4. Metni model bozuk yazarsa o satırı sil, yazıyı Canva'da ekle (en garanti yol).

## Sabit marka kuralları
- Yüze %99 sadık kal; güzelleştirme/inceltme/yaşlandırma YOK ("do not beautify" satırı kritik).
- Giysi: temiz beyaz önlük VEYA lacivert scrubs. Günlük tişört / marka logosu YOK.
  Bir kez sabitle, TÜM videolarda aynı kıyafet = marka tanınırlığı.
- Yerleşim: doktor sağ üçte bir (göğüsten yukarı), metin sol üçte iki.
- Renk: lacivert→teal gradyan + tek parlak vurgu (genelde cyan).
- Metin: 3-4 kelime, max 2 satır, sarı kalın sans-serif, koyu kontur + gölge.
- Küçük beyaz rozet: "IVF 2026".
- Telefonda (320px) okunmuyorsa font büyüt.

## MASTER PROMPT (kopyala, köşeli parantezleri doldur)

Using the attached photo of me as the EXACT reference, create a 16:9 YouTube
thumbnail (1280x720). Keep my face, identity, skin tone, head and glasses 99%
identical to the photo — do not beautify, slim, age, or alter my features; this
is a real doctor's personal brand and the face must stay recognizable. Replace my
clothing with a clean professional medical outfit — a crisp white doctor's coat
over a light shirt (or navy-blue scrubs) — and remove any casual t-shirt or brand
logos. Cleanly cut me out and place me on the RIGHT third of the frame, chest up,
with a [DUYGU: confident reassuring / concerned questioning] expression and a
subtle bright rim light separating me from the background, plus a thin edge glow
around my silhouette. Fill the LEFT two-thirds with a softly blurred, high-contrast
medical background showing [KONU GÖRSELİ: a single sperm cell selected by a
micro-pipette under a microscope], dark navy-to-teal gradient with one bright cyan
accent glow; keep the left area clean for text. Place bold text on the left: large
yellow headline "[METİN: Mieux choisir le sperme ?]" in a heavy sans-serif font
with dark outline and drop shadow, plus a small white badge "IVF 2026". Text must
be sharp, correctly spelled, readable on a phone. Cinematic studio lighting, ultra
sharp, professional, no watermark.

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
