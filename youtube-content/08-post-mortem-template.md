---
type: post-mortem-template
domain: youtube-content-production
master-source: wiki/youtube/seo-youtube-tr.md + wiki/youtube/seo-youtube.md (ölçüm bölümleri)
created: 2026-05-04
---

# 08 — Post-Mortem Template (Per-Video)

> Her yayınlanan videodan sonra **7 gün / 14 gün / 28 gün** yaş kontrol noktalarında doldurulan instance şablonu. Amaç: tekil performansı kayıt + tekrar eden öğrenme. Kullanım: bu dosyayı kopyala → `post-mortems/YYYY-MM-DD-[video-id]-[slug].md` adıyla kaydet → ilgili işaret günlerinde alanları doldur.

**Kullanım kuralları:**
- Yayın günü "Production retro" + boş analytics tablo doldurulur (5 dakika)
- 7d: ilk hız + erken sinyal (10 dakika)
- 14d: trend onayı + yorum kalitesi (10 dakika)
- 28d: kümülatif tablo + öğrenme + sonraki video aksiyon listesi (15-20 dakika)
- 28d sonrası `09-production-pipeline.md` "measurement queue"'dan çıkarılır

---

## Frontmatter (her instance için doldur)

```yaml
---
type: post-mortem
video-id: [YouTube video ID — 11 karakter, ör. "abc123XYZ_0"]
slug: [URL slug — description CTA'da kullanılan]
title: [tam video başlığı]
channel: [TR | FR]
language: [tr | fr]
length-category: [K1 | K2 | K3 | K4 | K5]
topic-type: [konsept | pazarlama-eleştirisi | kılavuz | hassas | konuk-uzman]
topic-pack: [pack-id, ör. "peptid-longevity-2026-04" — yoksa "tek-video"]
publish-date: YYYY-MM-DD
publish-time-tsi: HH:MM
post-mortem-author: Dr. Aksoy
status: [7d-pending | 7d-done | 14d-done | 28d-done | archived]
last-updated: YYYY-MM-DD
---
```

---

## 1. Production retro (yayın günü doldur)

| Üretim girdisi | Değer / Not |
|---|---|
| **Hook tipi** | (`04-hooks-bank.md` # numarası) |
| **Anchor cümle var mı?** | (Evet/Hayır — varsa hangi aile üyesi) |
| **Aile üyesi (1 adet maks.)** | (`01-voice-checklist.md` üye numarası) |
| **Tema ailesi** | (`00-INDEX.md` Tema A-G) |
| **Hassas konu mu?** | (Evet → metafor yok teyidi / Hayır) |
| **Description konu tipi** | (`07-description-library.md` 4 tip) |
| **Disclaimer alternatifi** | (5'ten hangisi) |
| **Thumbnail varyantı** | (A / B — Studio Test & Compare aktif mi?) |
| **Çekim notu** | (1-2 cümle: ses, ışık, set notu) |
| **UTM kampanya** | (`utm_campaign=` değeri) |

**Topic-pack/master vault çapraz bağlantı:**
- [ ] `wiki/youtube/topic-packs/[pack-id].md`
- [ ] `wiki/medical/concepts/[concept].md` (ilgili kanıt çapası)
- [ ] `06-anchor-rotation-tracker.md`'a satır eklendi

---

## 2. Analytics snapshots

> YouTube Studio → Analytics → tek video sayfasından, her işaret gününde aşağı tabloyu doldur.

### Ana metrikler

| Metrik | 7d | 14d | 28d | Hedef / yorum |
|---|---|---|---|---|
| **Görüntüleme (views)** | | | | Kanal ortalamasıyla kıyasla |
| **CTR (impression CTR %)** | | | | TR/FR hedef > %5 (`seo-youtube-tr.md` §Ölçüm) |
| **Ortalama izlenme süresi (sn)** | | | | |
| **Ortalama izlenme % (retention)** | | | | TR/FR hedef > %50 |
| **Watch time (saat)** | | | | Algoritma için hayati |
| **Beğeni / görüntüleme** | | | | |
| **Yorum sayısı** | | | | (kalite ayrı bölümde) |
| **Paylaşım** | | | | |
| **Kanal aboneliği (delta)** | | | | Bu videodan kazanılan |
| **Kayıp abone** | | | | Sinyal: konu zıtlığı / hayal kırıklığı |

### Trafik kaynakları (28d)

| Kaynak | % | Not |
|---|---|---|
| YouTube önerileri | | |
| Arama (YouTube içi) | | İlk 3 anahtar kelime ne? |
| Tarama (browse / homepage) | | |
| Harici (Google, sosyal) | | |
| Doğrudan + bilinmeyen | | |
| Son ekran / kart | | |

**İlk 3 YouTube arama anahtar kelimesi:**
1.
2.
3.

**Önerilerde gelen üst 3 kaynak video:** (kendi videolar mı, başka kanal mı?)

### Retention curve sinyalleri (28d)

| İşaret | Var mı? | Saniye / not |
|---|---|---|
| **Erken bırakma (0-15 sn)** | (>%30 düşüş?) | Hook zayıf? |
| **Bağlam çıkışı (15-60 sn)** | | TLDR yetersiz? |
| **Beat A → Beat B düşüşü** | | Konsept-kanıt geçişi |
| **Beat C → Beat D düşüşü** | | Klinik karar-yorum sıkıcı? |
| **Son 20 sn (CTA / end screen)** | (>%70 takip?) | End screen tıklanma |
| **Tekrar izleme (re-watch peak)** | | Hangi an? |

---

## 3. Yorum analizi (14d / 28d)

| Soru | Sayım / not |
|---|---|
| Toplam yorum | |
| Hasta sorusu (yanıt gerekli) | (`youtube-responses` kategorisi) |
| Pozitif geri bildirim | |
| Eleştirel / tartışmacı | |
| Spam / off-topic | |
| Mevzuat-riskli (silinmesi gerekti) | |

**En sık 3 soru kümesi:**
1. (→ kategori # / yeni şablon adayı?)
2.
3.

**Yeni topic backlog adayı:** (yorumdan doğan video fikri)

---

## 4. Description / hashtag / başlık retro

| Bileşen | Çalıştı / çalışmadı | Sonraki sefer |
|---|---|---|
| Snippet (ilk 150 ch) | | |
| Başlık | (CTR sinyali) | |
| Hashtag (3-5) | (hangileri arama getirdi?) | |
| Thumbnail | (CTR) | |
| Sabitlenmiş yorum | (engagement var mı?) | |
| UTM hedef domain trafiği | (GA4'ten al) | |

**A/B varyantı sonucu:** (Studio Test & Compare → kazanan thumbnail/başlık + delta)

---

## 5. Öğrenme + aksiyon (28d ana çıktı)

### Ne işe yaradı

- (3-5 madde, somut)

### Ne işe yaramadı

- (3-5 madde, somut — neden hipotezi ile)

### Sonraki video / pack için aksiyon

- [ ] (somut, çalıştırılabilir)
- [ ]
- [ ]

### Çapraz bağlama

- [ ] Master `wiki/youtube/topic-packs/[pack-id].md` "post-mortem öğrenmeleri" bölümüne özet eklendi
- [ ] `topics-backlog.md` yeni fikir(ler) eklendi (yorumlardan)
- [ ] `09-production-pipeline.md` measurement queue → archived
- [ ] Eğer öğrenme **tüm kanal ölçeğinde geçerliyse** master `wiki/youtube/channel-strategy-{tr/fr}.md` güncellemesi tetiklendi

---

## 6. Hassas konu ek kontrol (sadece topic-type=hassas için)

> Hassas konuda (POI, RPL, donör, kanser FP, ileri yaş, RIF, kayıp) standart metriklere ek olarak izleme:

- Yorumlarda **hasta hikayesi** paylaşan oldu mu? (mahremiyet riski → şablonla yumuşak yöneltme)
- Yorumlarda **tehlike sinyali** (kendine zarar, ağır depresyon) var mı? (varsa profesyonel destek hattı önerme cevabı)
- Disclaimer satırı yeterince görünür miydi? (sabitlenmiş yorum + description + on-screen + sesli kombosu)
- Konu hakkında 28d sonra **takip videosu** ihtiyacı doğdu mu? (ör. POI → "POI'de kemik koruma" derinlemesine)

---

## 7. Versiyon takibi (instance-level)

| Tarih | Değişiklik |
|---|---|
| YYYY-MM-DD | İlk doldurma — production retro |
| YYYY-MM-DD | 7d snapshot |
| YYYY-MM-DD | 14d snapshot |
| YYYY-MM-DD | 28d snapshot + öğrenme |
| YYYY-MM-DD | Archived → `09-production-pipeline.md`'dan çıkarıldı |
