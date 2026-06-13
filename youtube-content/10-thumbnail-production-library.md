---
type: thumbnail-production-library
domain: youtube-content-production
master-source: wiki/youtube/thumbnail-rules.md + wiki/youtube/seo-youtube-tr.md + wiki/youtube/seo-youtube.md
created: 2026-05-04
---

# 10 — Thumbnail Production Library

> Yeniden kullanılabilir thumbnail üretim altyapısı (TR + FR ortak çekirdek, kanala göre adaptasyon notları). Her video için kopyalanan **per-video brief şablonu** + **A/B test protokolü** + **mobil okunabilirlik testi** + **mevcut video backfill stratejisi**. Per-campaign (örn. FR Mayıs 2026) prod-pack'leri bu kütüphaneyi temel alır.

`channel-operations-memory-2026-05-01.md` notu: TR kanalda thumbnail yenileme henüz başlamadı (FR'de `senaiaksoy-fr-thumbnail-production-pack-2026-05-02.md` mevcut, TR muadili yok). Bu dosya o boşluğu kapatır.

---

## Teknik spesifikasyon

| Alan | Değer |
|---|---|
| Çözünürlük | **1280 × 720 px** (16:9) |
| Format | `.jpg` (preferred) veya `.png` |
| Maksimum dosya boyutu | 2 MB (YouTube limiti) |
| Renk profili | sRGB |
| Mobil test boyutu | **120 × 68 px** — mobil önerilerinde gerçek görünür boyut |
| Snippet/önizleme | TV / large screen ve mobil ikisinde de okunabilir |

---

## Renk paleti — Dr. Aksoy marka evreni

`wiki/youtube/thumbnail-rules.md` master tablosu (TR + FR ortak; Estranova ile paylaşılan palet, marka tutarlılığı):

| Renk | Hex | Kullanım |
|---|---|---|
| Burgundy derin | `#6B2D3E` | Ana vurgu, arka plan şerit, anahtar kelime arka tahtası |
| Gold (ılık) | `#C9A96E` | Metin vurgusu, çizgi, çerçeve |
| Cream | `#FAF6EE` | Açık arka plan |
| Koyu gri | `#2D2D2D` | Metin gövdesi |
| Beyaz | `#FFFFFF` | Arka plan / negatif boşluk |

> **Yasak renkler (her iki kanal):** parlak kırmızı (`#FF0000`), neon turuncu, neon sarı, klikbeyt yeşili. Marka paletinin dışına çıkılmaz.

---

## Tipografi

| Rol | Font ailesi | Notlar |
|---|---|---|
| **Birincil (anahtar kelime)** | Serif editöryal — Newsreader, Playfair Display, Cormorant | Konu adı; büyük, kalın |
| **İkincil (alt-vurgu)** | Sans-serif bold — Inter, Manrope, Geist | Soru / kontrast cümlesi |
| **Atletik vurgu (sayı, "vs", "?")** | Sans-serif extra bold | Tek-iki karakter; opsiyonel |

**Yasak fontlar:** Comic Sans, Papyrus, dekoratif/script (Brush Script vb.), tüm büyük harfli dökme blokmajüskül süslü fontlar.

---

## 4 master pattern — kanal-bağımsız çatı

Her video aşağıdaki 4 pattern'den birine düşer. Master `thumbnail-rules.md` tabloyu sağlar; bu altbölüm ona ek olarak **konu tipi → pattern eşlemesi** ekler.

### Pattern A — "Konu kartı" (varsayılan)

**Yapı:**
- Sol: Dr. Aksoy portresi (omuz yukarısı, nötr ifade, kameraya bakış)
- Sağ üst: konu adı (1-2 kelime, serif)
- Sağ alt: alt-soru (2-3 kelime, sans-serif)

**Örnek:**
```
[Dr. Aksoy portresi]    DHEA
                        VAJİNAL Mİ, SİSTEMİK Mİ?
```

**En uygun konu tipleri:** kavram açıklayıcı, kılavuz değerlendirmesi.

### Pattern B — "Kontrast"

**Yapı:**
- Orta veya hafif sağa: Dr. Aksoy portresi
- Üst: kontrastı yapan iki kelime/yıl (serif), aralarında ince gold ayraç
- Alt: küçük açıklayıcı

**Örnek:**
```
2016  |  2023
[Dr. Aksoy]
ERA TESTİ — NE DEĞİŞTİ?
```

**En uygun konu tipleri:** kılavuz değerlendirmesi (yıl bazlı), pazarlama vs bilim ayrımı.

### Pattern C — "Mini-seri / sayı"

**Yapı:**
- Üst şerit: seri adı veya "1/5" gibi bölüm numarası
- Orta: Dr. Aksoy + ana anahtar kelime
- Alt: bağlam (opsiyonel)

**Örnek:**
```
3 YANILGI
[Dr. Aksoy]
AMH HAKKINDA
```

**En uygun konu tipleri:** sayı-bazlı pillar ("3 yanılgı", "5 soru", "4 işaret"), Q&A serisi.

### Pattern D — "Klinik görüş / opinion"

**Yapı:**
- Ana metin: "Klinik gözlemim" veya kısa tez cümlesi
- Dr. Aksoy portresi sol veya sağ
- Sade, metnin nefes alacağı negatif boşluk

**Örnek:**
```
NEDEN GARANTİ
VERMİYORUM
[Dr. Aksoy]
```

**En uygun konu tipleri:** Beat D yoğun videolar, dürüst-eleştirel pozisyon, pazarlama eleştirisi.

> **Hassas konu istisnası (POI/RPL/donör/kanser FP/ileri yaş/RIF/kayıp):** 4 pattern'in herhangi biri kullanılabilir AMA **görsel yüksek-mimik / dramatik aydınlatma / koyu vinyet** kullanılmaz. Pattern A (konu kartı) sade-empatik versiyon önerilir; soru cümlesi yumuşak tonda ("AMH düşük, ne anlama gelir?" — "AMH FELAKETTİR" değil).

---

## Topic-type × pattern matrisi

`07-description-library.md` 4 konu tipiyle paralel:

| Konu tipi | Birincil pattern | İkincil pattern | Yasak pattern |
|---|---|---|---|
| **Kavram açıklayıcı** (DHEA nedir, AMH nedir) | A — Konu kartı | C — Sayı (3 yanılgı vb.) | — |
| **Pazarlama eleştirisi** (peptid, longevity) | D — Klinik görüş | A — Konu kartı | C — sayı yanıltıcı pazarlama hissi yaratabilir |
| **Kılavuz değerlendirmesi** (ESHRE 2023, NAMS) | B — Kontrast (yıl) | A — Konu kartı | — |
| **Hassas konu** (POI, RPL, donör, kanser FP, ileri yaş) | A — Konu kartı (sade versiyon) | D — Klinik görüş (yumuşak) | B — kontrast (drama hissi); C — "5 işaret" tipi sayı (klikbeyt algısı) |

---

## Yasaklar (TR + FR ortak + TR-spesifik)

`wiki/youtube/thumbnail-rules.md` + `seo-youtube-tr.md` §"Thumbnail yasakları" + SB Tanıtım Yönetmeliği:

### Görsel yasaklar (her iki kanal)

- Ok işaretleri (kafa/sırt vurma) — clickbait sinyali
- Dairesel kırmızı vurgu (kafaya, sayıya) — clickbait sinyali
- Aşırı mimik (ağız açık şaşkınlık, kaş kalkık abartı) — youtube algoritması ceza veriyor
- "ŞOK!", "MUCİZE!", "İNANILMAZ!", "GİZLİ!" yazıları
- Photoshop abartı (kafanın aşırı büyütülmesi, gözün aşırı parlaması)
- Sansasyonel görseller: üzgün hasta yüzü, hamile karın, bebek görseli (duygu sömürüsü)
- Kırmızı/turuncu agresif arka plan
- Uyarı sembolü (! / ⚠️) ana vurgu olarak

### Klinik pazarlama yasakları

- Klinik logosu, klinik adı, klinik adresi
- Hekim ünvan vurgusu ("Türkiye'nin en başarılı...", "30 yıllık X uzmanı")
- Fiyat sayısı, "%" işareti (oran iddiası)
- "Ücretsiz", "Özel İndirim", "Sınırlı süre"
- Önce/sonra kombinasyonu

### TR-spesifik ek yasaklar (SB Tanıtım Yönetmeliği + TR pazar duyarlılığı)

- "Kesin sonuç", "Garantili", "%X başarı"
- "Bu yöntem MUTLAKA çalışır" tipi kantitatif iddia
- Coğrafi-klinik kombinasyonu ("İstanbul tüp bebek")
- Hasta yüzü, hasta hikayesi öyküsel görseli (mahremiyet)
- Belirli ürün/marka adı görseli (NAD damar, peptid markası vb.)
- Dini sembol kombinasyonu (kültürel hassasiyet — pazarlama bağlamı)

---

## Üretim akışı (5 aşama)

| # | Aşama | Çıktı | Kapı |
|---|---|---|---|
| 1 | **Brief** | Per-video brief dosyası (aşağıdaki şablon) — 2 varyant (Option A + B) | Brief onaylı |
| 2 | **Design** | İki .jpg/.png varyantı, isimlendirme kuralına uygun | Görsel kontrol checklist geçti |
| 3 | **Review** | Mobil test (120×68), kontrast, palet, font, yasak kontrol | Reviewer onayı |
| 4 | **Upload** | YouTube Studio'ya iki varyant; Option A canlıya | A varyantı 7d sonra metrik var |
| 5 | **A/B test** | Studio Test & Compare → 2-7 gün → kazanan kalır | Kazanan thumbnail kalıcı; post-mortem'e not |

> **Tek varyant istisnası:** Hassas konu videolarında (POI, RPL, donör, kanser FP) A/B test yapılmaz — duygusal-empatik etki tek bir tasarıma odaklanılır. `09-production-pipeline.md` measurement queue'da "A/B: yok" olarak işaretlenir.

---

## Per-video brief şablonu

Her yeni video için bu şablon kopyalanır → `thumbnails/[YYYY-MM-DD]-[video-slug]-brief.md` olarak kaydedilir → Option A + B doldurulur → designer'a (veya kendin Canva/Photoshop) verilir.

```markdown
---
type: thumbnail-brief
video-id: [YouTube ID, henüz yoksa "TBD"]
slug: [URL slug]
title-working: [çalışma başlığı]
channel: [TR | FR]
length-category: [K1 | K2 | K3 | K4 | K5]
topic-type: [konsept | pazarlama-eleştirisi | kılavuz | hassas | konuk-uzman]
pattern: [A | B | C | D]
ab-test: [evet | hayır (hassas konu)]
created: YYYY-MM-DD
designer: [Dr. Aksoy / [diğer]]
---

# Thumbnail Brief — [Konu]

## Hedef

(1 cümle: bu thumbnail'ın yapması gereken klikleme + beklenti yönetimi)

## Option A

\```text
[ANA KELIME]
[ALT-SORU veya KONTRAST]
\```

**Kompozisyon:**
- Dr. Aksoy konumu: [sol / orta / sağ]
- İkincil görsel: [yok / şematik organ / takvim / kalp / vb.]
- Renk vurgusu: [hangi palet rengi]

**Vurgu:** (hangi kelime en büyük)

## Option B

\```text
[ALTERNATIF YAKLAŞIM]
\```

**Kompozisyon:** [farklı yön — örneğin daha sayı-temelli, daha minimal]

**Vurgu:** (farklı kelime)

## Yasak (bu video için ek)

- (varsa video-spesifik yasak — örn. "polip videosunda kanser yazma")

## Dosya isimleri

- `tr-thumb-[N]-[konu-slug]-A.jpg`
- `tr-thumb-[N]-[konu-slug]-B.jpg`

## Notlar

(designer'a not: kanal görsel hafıza, önceki thumbnail kıyası, marka tutarlılığı)
```

---

## A/B test protokolü (Studio Test & Compare)

YouTube Studio'nun yerleşik **Test & Compare** özelliği (2024 sonu itibarıyla aşamalı yayında) — manuel A/B test yerine.

### Aktivasyon

- YouTube Studio → Video → Thumbnail → "Test & Compare" butonu (mevcutsa)
- Eğer kanal/bölge için aktif değilse: manuel A/B (kısa-pencere değişim, aşağıda)

### Studio Test & Compare ayarları

| Ayar | Tavsiye |
|---|---|
| Varyant sayısı | 2 (A vs B) |
| Test süresi | 4-7 gün (algoritma için yeterli view hacmi) |
| Optimizasyon hedefi | "Watch time" (tek başına CTR yanıltıcı) |
| Otomatik kazanan seçimi | Açık |

### Manuel A/B (Test & Compare yoksa)

1. Yayın günü Option A canlı
2. 4 gün sonra Option B'ye değiştir, **ekran görüntüsü** + tarih notu
3. 4 gün daha geçtikten sonra Studio Analytics'te iki periyot karşılaştır:
   - CTR (impression CTR)
   - Average view duration
   - Average percentage viewed
4. Kazanan varyant kalır
5. Sonuç → `08-post-mortem-template.md` "Description / hashtag / başlık retro" tablosunda "A/B varyantı sonucu" satırı

> **Sınır:** Manuel A/B'de **dış değişken kontrolü zayıf** (YouTube algoritması day-of-week + recency effect ekler). Studio Test & Compare daha temiz; manuel kullanım sadece Studio özelliği yoksa.

---

## Mobil okunabilirlik test (yayın öncesi zorunlu)

Her thumbnail yayından önce:

- [ ] **120 × 68 px küçültme:** Photoshop / Canva'da dosyayı 120×68'e indir; ana kelime hala okunuyor mu?
- [ ] **Telefon ekranı testi:** thumbnail'ı kendi telefonunda YouTube önerilerinde nasıl göründüğünü gör (yayın günü ilk view öncesi quick test)
- [ ] **Kontrast oranı:** metin vs arka plan WCAG AA (≥4.5:1 normal metin, ≥3:1 büyük metin)
- [ ] **Renk körlüğü testi:** Coblis / Sim Daltonism gibi araçla protanopia/deuteranopia testleri (Burgundy + Gold paletinde sorun düşük ama kontrol şart)
- [ ] **Kanal kıyası:** son 4 thumbnail yan yana — marka tutarlı mı, fark eden öne çıkıyor mu?

---

## Dosya isimlendirme konvansiyonu

```
{kanal}-thumb-{NN}-{konu-slug}-{varyant}.jpg
```

**Kanal kodları:**
- `tr` — TR kanal (tupbebek.com'a hizmet)
- `fr` — FR kanal (@senaiaksoy)
- `est` — Estranova (kurulduğunda)

**Örnekler:**
- `tr-thumb-01-dhea-vajinal-vs-sistemik-A.jpg`
- `tr-thumb-01-dhea-vajinal-vs-sistemik-B.jpg`
- `fr-thumb-06-fiv-turquie-A.jpg`
- `fr-thumb-06-fiv-turquie-B.jpg`

NN = pack-id sırasındaki numara veya tek-video için 00.

**Saklama yeri:**
- Brief dosyaları: `Youtube/youtube-content/thumbnails/[YYYY-MM]/...`
- Görsel dosyaları: `Youtube/youtube-content/thumbnails/[YYYY-MM]/assets/...`

---

## Mevcut video backfill stratejisi

`channel-operations-memory-2026-05-01.md` ve `senaiaksoy-fr-channel-operations-summary-2026-05-02.md`:

- TR kanal: 72 video, sabitlenmiş yorumlar tamamlandı, playlist oturdu, **thumbnail backfill yapılmadı**
- FR kanal: 91 video, başlık + description optimizasyon dalgası tamamlandı, **thumbnail kasten değişmedi** ("thumbnails non modifiées volontairement")

### Karar

- **Yeni videolar:** bu kütüphane tam uygulanır
- **Mevcut TR 72 + FR 91 video:** **bulk thumbnail değişimi yapılmaz** — algoritma resetleme riski + kapasite. Sadece **seçici** güncelleme.

### Seçici güncelleme tetikleyicileri (her ikisi de geçerli olmalı)

1. **Performans tetikleyicisi:** video yayın sonrası 90+ gün, CTR < %2, retention < %35 (kanal alt çeyrek dilimde)
2. **Strateji tetikleyicisi:** (a) konu mevzuat-riski taşıyan eski thumbnail (örn. "garanti" kelimesi); (b) konu yeni kılavuzla çelişen mesaj; (c) palet/marka eski (Burgundy paletine geçiş öncesi); (d) hasta yüzü / önce-sonra ihlal görseli

### Seçici süreç

1. TR + FR için 90+ günlük video listesi → CTR/retention sıralaması
2. Alt çeyrek dilim → strateji filtresinden geç
3. Tetikleyici çift sağlanan videolarda yeni thumbnail brief açılır
4. **Eski thumbnail dosyası arşivlenir** (mevcut kayıt için)
5. Yeni thumbnail yayını → 14d sonra CTR/retention farkı ölçülür
6. Kayıt → `thumbnail-backfill-log-YYYY-MM.md` (ay başına yeni)

> **Uyarı:** Algoritma cezası mümkün — yüklü video thumbnail değişimi sonrası 7-14 gün impression düşüşü olabilir. Bu yüzden batch olmaz, **video başına izole** ve metrikle teyit edilir.

---

## Çapraz bağlantılar

- [03-script-format-checklist.md](03-script-format-checklist.md) — script bölümünde thumbnail brief checklist
- [05-topic-packs-index.md](05-topic-packs-index.md) — pack-id konvansiyonu
- [07-description-library.md](07-description-library.md) — başlık + thumbnail uyumu (snippet ↔ thumbnail metni örtüşmemeli, tamamlamalı)
- [08-post-mortem-template.md](08-post-mortem-template.md) — "Description / hashtag / başlık retro" tablosunda A/B sonucu
- [09-production-pipeline.md](09-production-pipeline.md) — thumbnail aşaması durum 5 (edited) içinde
- Per-campaign örnek: `senaiaksoy-fr-thumbnail-production-pack-2026-05-02.md` — bu kütüphaneyi kullanan canlı uygulama
- Master: `wiki/youtube/thumbnail-rules.md`, `wiki/youtube/seo-youtube-tr.md` §Thumbnail, `wiki/youtube/seo-youtube.md` §Thumbnail

---

## Versiyon takibi

| Tarih | Değişiklik |
|---|---|
| 2026-05-04 | İlk versiyon — teknik spesifikasyon, palet, tipografi, 4 master pattern (A/B/C/D), topic-type × pattern matrisi, yasaklar (TR+FR ortak + TR-spesifik), 5 aşamalı üretim akışı, per-video brief şablonu, A/B test protokolü (Studio Test & Compare + manuel fallback), mobil okunabilirlik checklist (5 madde), dosya isimlendirme konvansiyonu, mevcut video backfill stratejisi (seçici tetikleyiciler + süreç) |
