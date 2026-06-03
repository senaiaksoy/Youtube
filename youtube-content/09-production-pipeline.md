---
type: production-pipeline
domain: youtube-content-production
channel-coverage: tr + fr
master-source: wiki/youtube/topic-packs/ + wiki/youtube/topics-backlog.md
created: 2026-05-04
updated: 2026-06-03
---

# 09 — Production Pipeline & Measurement Queue

> **TR + FR YouTube kanallarının canlı üretim haritası.** Her video bir satır; durumu güncellenir. Yayın sonrası 28 gün boyunca measurement queue'da kalır, sonra arşiv. Bu dosya **mirror-özel operasyonel veri** — master vault'ta yer almaz.

---

## Durum tanımları (8 aşamalı pipeline)

| # | Durum | Tanım | Çıkış kriteri |
|---|---|---|---|
| 1 | **idea** | Konu fikri (`topics-backlog.md` veya yorumdan) | Pack'e atandı + Beat planı taslağı |
| 2 | **outlined** | Beat A-D taslağı yazıldı; hook seçildi; anchor kararı verildi | Tam script taslağı tamam |
| 3 | **scripted** | Tam script TR/FR yazıldı; hassas konu ise metafor yokluğu doğrulandı | Çekim hazır (sahne/ışık/zaman) |
| 4 | **filmed** | Çekim tamam, ham video editörde | İlk kurgu turu yapıldı |
| 5 | **edited** | Kurgu, alt yazı, on-screen text, thumbnail teslim | Studio'ya yüklendi |
| 6 | **scheduled** | YouTube Studio'da yayın saati ayarlı; description + tag + thumbnail + sabitlenmiş yorum hazır | Yayın saati geldi |
| 7 | **published** | Canlıda; `06-anchor-rotation-tracker.md`'a satır eklendi; post-mortem dosyası açıldı | 7d analytics gelmeye başladı |
| 8 | **measured** | 28d post-mortem tamamlandı; öğrenme master'a yansıdı | Archive |

> **Hızlı geçiş engelleri:** her durumdan bir sonrakine geçiş için `03-script-format-checklist.md` kontrolü + `02-compliance-checklist.md` taraması zorunlu (özellikle 3→4 ve 5→6 noktalarında).

---

## TR kanal pipeline

> Kanal: `UCbO5qpAnmaQPBJlGMM9ITiw` (tupbebek.com baş editörü). Hedef yayın temposu: **haftada 1**.

| Sıra | Durum | Konu / başlık çalışması | K# | Konu tipi | Pack-id | Hassas? | Hedef yayın | Blocker / not |
|---|---|---|---|---|---|---|---|---|
| _(boş — yeni video planlamaya başlandığında doldur)_ | | | | | | | | |

> **Kullanım örnekleri (silmeden referans tut):**
>
> | 1 | scripted | "DHEA: vajinal vs sistemik" | K3 | konsept | peptid-longevity-2026-04 | hayır | 2026-05-13 | Çekim sahnesi 2026-05-09 |
> | 2 | outlined | "Wellness peptidleri — bilim mi influencer mı?" | K3 | pazarlama-eleştirisi | peptid-longevity-2026-04 | hayır | 2026-05-20 | — |
> | 3 | idea | "İnositol vs metformin PCOS" | K3 | konsept | peptid-longevity-2026-04 | hayır | 2026-05-27 | — |

### TR — sıradaki 4 hafta yayın hedefi

| Hafta | Hedef yayın tarihi | Pack | Konu | Durum |
|---|---|---|---|---|
| W+1 | | | | |
| W+2 | | | | |
| W+3 | | | | |
| W+4 | | | | |

---

## FR kanal pipeline

> Kanal: `@senaiaksoy` (draksoyivf.com'a hizmet eden). Hedef yayın temposu: **haftada 1**. `senaiaksoy-fr-next-session-brief-2026-05-02.md` notu: bulk metadata operasyonu durdu, **yeni içerik fazına geçildi**.

> Not: Mevcut FR videolarda EN/AR alt yazı ve dubbing var. İlk paylaşım metninde ve video/on-screen text içinde gerekli yerlerde bunu belirt.

| Sıra | Durum | Konu / başlık çalışması | K# | Konu tipi | Pack-id | Hassas? | Hedef yayın | Blocker / not |
|---|---|---|---|---|---|---|---|---|
| _(boş — FR brief'in talep ettiği "10 prochaines vidéos FR" listesi buraya inecek; aşağıdaki "Backlog" bölümünden taşınır)_ | | | | | | | | |

### FR — backlog (FR brief'in 10 yeni video önceliği)

> `senaiaksoy-fr-next-session-brief-2026-05-02.md` "Prochaine meilleure session" → "créer le backlog des 10 prochaines vidéos FR". Bu liste Analytics ölçümünün sonucuna göre **finalize edilir**; aşağıdaki yapı bekletme alanı.

| Aday # | Başlık çalışması | Pack-id | Konu tipi | Kazanan veriden seçim mi? | Not |
|---|---|---|---|---|---|
| FR-A1 | | | | (28d analytics sonrası) | |
| FR-A2 | | | | | |
| FR-A3 | | | | | |
| FR-A4 | | | | | |
| FR-A5 | | | | | |
| FR-A6 | | | | | |
| FR-A7 | | | | | |
| FR-A8 | | | | | |
| FR-A9 | | | | | |
| FR-A10 | | | | | |

### FR — sıradaki 4 hafta yayın hedefi

| Hafta | Hedef yayın tarihi | Pack | Konu | Durum |
|---|---|---|---|---|
| W+1 | | | | |
| W+2 | | | | |
| W+3 | | | | |
| W+4 | | | | |

---

## Measurement queue (28d post-mortem bekleyen videolar)

> Yayınlanan video → 7d/14d/28d kontrolleri için 08-post-mortem-template.md instance'ı. 28d tamam → "archived". Tek bakışta hangi videoda hangi gün hatırlatıcı.

| Video ID | Kanal | Başlık | Yayın | 7d | 14d | 28d | Post-mortem dosya |
|---|---|---|---|---|---|---|---|
| _(boş)_ | | | | ☐ | ☐ | ☐ | post-mortems/YYYY-MM-DD-[id]-[slug].md |

---

## Özel kohort: FR bulk metadata 2026-05 ölçümü

> `senaiaksoy-fr-channel-operations-summary-2026-05-02.md` — 91 FR videoda başlık + ilk 150 karakter description + hashtag + homepage playlist optimizasyonu yapıldı. Brief: "comparer 28 jours avant / 28 jours après, identifier les sujets gagnants."

### Hipotez

Toplu metadata değişikliği (başlık + snippet + hashtag + ana sayfa raf düzeni) **CTR + retention + arama trafiği**'nde anlamlı yükseliş yaratır. Konu kümesi başına farklı yanıt beklenir.

### Ölçüm penceresi

- **Müdahale tarihi:** 2026-05-02
- **Before:** 2026-04-04 → 2026-05-01 (28 gün)
- **After:** 2026-05-03 → 2026-05-30 (28 gün)
- **Erken sinyal okuması:** 2026-05-16 (14 gün)
- **Tam okuma:** 2026-05-31 itibarıyla

### Kohort segmentasyonu

| Segment | # video | Beklenen sinyal | Notlar |
|---|---|---|---|
| Evergreen (yıl boyu arama getiren) | | Yüksek lift | Önce bunlardan yanıt gelir |
| Konjonktürel (yeni kılavuz / haber bağlamı) | | Orta lift | Bağlam tükendi mi? |
| Eski kuyruk (>3 yıl, düşük volume) | | Düşük / nötr | Kayıp değil baseline |
| Cerrahi arşiv | | Düşük | Strateji-dışı |

### Karar matrisi (28d sonra)

| Bulgu | Karar |
|---|---|
| Evergreen segmentte CTR ≥ +%20 ve retention ≥ +%10 | **Strateji onaylı**; aynı yaklaşım yeni 10 videoda uygulanır |
| Evergreen segmentte CTR ≥ +%10 ama retention nötr | **Başlık/snippet işe yaradı, içerik aynı tonda** — content yönü değişmez |
| Konjonktürel segmentte yükseliş yok ama evergreen iyi | **Konjonktürel videolar bağlam-eskimişi**; yeniden çekim/arşiv |
| Hiçbir segmentte yükseliş yok | **Strateji yenilemesi**; thumbnail + içerik açısı (sadece metadata değil) işe alınır |
| Hiçbir segmentte değişiklik yok ama abone büyümesi var | **Kanal-altı ölçü farklı çalışıyor**; sub/view oranı + community tab incelemesi |

### Veri çıkarma

- **YouTube Studio Analytics → Advanced mode**: video bazında CTR, average view duration, average percentage viewed, traffic source breakdown
- **CSV export**: `youtube-api/` altına `fr-bulk-metadata-2026-05-export.csv` (kullanıcı el ile)
- **GA4 (draksoyivf.com tarafı)**: `utm_source=youtube&utm_medium=description` aynı pencerede session + bounce karşılaştırması

### Ölçüm sonrası dosya

- 2026-05-31 sonrası: `D:/A-klasör/Youtube/youtube-content/fr-bulk-metadata-2026-05-readout.md` — bulgular + karar matrisinden seçim + 10 yeni video önceliği finalize
- O dosya yazıldığında bu bölüm "**Sonuç →** [link]" satırıyla kapatılır

---

## Aylık review checklist (her ayın 1'inde)

- [ ] **Pipeline'ı tara:** her satır doğru durumda mı? `idea > 60 gün` ise demote/elimine
- [ ] **Measurement queue'yu tara:** 28d geçmişler `archived`'a taşındı mı?
- [ ] **Hedef yayın tarihleri:** kayan videolar var mı? Sebep + yeniden planlama
- [ ] **Kapasite kontrolü:** TR + FR ayrı, "scripted" üstü en fazla 4 video (üst-orta darboğaz)
- [ ] **Topic-pack tüketimi:** mevcut pack'ten kaç video çıktı, sıradaki pack hazırlanıyor mu?
- [ ] **Anchor rotation tracker** (`06-anchor-rotation-tracker.md`) ile çapraz: aynı satırlar, aynı sıra
- [ ] **Post-mortem öğrenmeleri:** son ay 28d tamam olan videolardan toplu öğrenme çıkarımı (5-10 madde) → master `wiki/youtube/channel-strategy-{tr/fr}.md`
- [ ] **Backfill log:** `description-backfill-log-YYYY-MM.md` (varsa) tarandı, etki ölçüldü
- [ ] **Bu dosyanın `updated:` tarihi** ay başına güncellendi

---

## Çapraz bağlantılar

- [00-INDEX.md](00-INDEX.md) — sistem girişi
- [03-script-format-checklist.md](03-script-format-checklist.md) — script kontrolü (durum 3 → 4 geçiş kapısı)
- [05-topic-packs-index.md](05-topic-packs-index.md) — pack-id kaynağı
- [06-anchor-rotation-tracker.md](06-anchor-rotation-tracker.md) — yayın sonrası anchor/aile üyesi kayıt
- [07-description-library.md](07-description-library.md) — durum 5 → 6 geçişinde description hazırlık
- [08-post-mortem-template.md](08-post-mortem-template.md) — durum 7 → 8 measurement instance
- Master `wiki/youtube/topics-backlog.md` — idea kaynağı
- Master `wiki/youtube/channel-strategy-tr.md` / `channel-strategy-fr.md` — strateji yansıma yönü

---

## Versiyon takibi

| Tarih | Değişiklik |
|---|---|
| 2026-06-03 | FR videolarda EN/AR alt yazı + dubbing olduğu ve bunun ilk paylaşım/video içinde uygun yerlerde belirtilmesi gerektiği eklendi |
| 2026-05-04 | İlk versiyon — 8 aşamalı durum enum, TR + FR pipeline + 4 hafta hedef + backlog tabloları, measurement queue, FR bulk metadata 2026-05 özel kohort (hipotez + pencere + segment + karar matrisi + veri çıkarma + sonuç dosyası planı), aylık review checklist, çapraz bağlantılar |
