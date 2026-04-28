---
type: readme
domain: youtube-content-production
owner: Dr. Senai Aksoy
created: 2026-04-26
sister-system: youtube-responses (yorum yanıtlama)
master-source: D:/A-klasör/obsidian-vaults/draksoyivf-knowledge/wiki/
---

# YouTube İçerik Üretim Sistemi (operasyonel referans)

Bu klasör, **YouTube video üretimi** için hazır **çekim öncesi hızlı checklist + protokol** belgeleridir. Yorum yanıtlama sisteminin (`../youtube-responses/`) kardeş alt sistemidir.

## Amaç

- Çekim öncesi, **5 dakikada** ses + uyumluluk + format kontrolü
- "Buzdolabı metaforu son hangi videoda kullanıldı?" gibi rotasyon takibi
- Yazar/agent/Dr. Aksoy için ortak operasyonel referans
- Mevzuat-uyumlu ifade rehberi hızlı erişim

## Master ve mirror ilişkisi

| Konum | Rol |
|---|---|
| `D:/A-klasör/obsidian-vaults/draksoyivf-knowledge/wiki/` | **Canlı master** — tüm kanıt çapası, hub, knowledge backend, full topic packs, voice family detayı |
| `D:/A-klasör/Youtube yorum yanıtlama/youtube-content/` (bu klasör) | **Operasyonel mirror** — kısa checklist, hızlı tablo, çekim-anı referansı |

**Kural:** Master değişirse mirror güncellenir; mirror direkt düzenlenmez. Detay için bkz. `sync-policy.md`.

## Klasör yapısı

```
youtube-content/
├── README.md                          ← bu dosya
├── 00-INDEX.md                        ← hızlı içindekiler + tematik harita
├── 01-voice-checklist.md              ← metaphor family hızlı seçim + protokol + anti-pattern
├── 02-compliance-checklist.md         ← TR + FR yasak/güvenli ifade tablosu (tek bakış)
├── 03-script-format-checklist.md      ← video format + hook + CTA + thumbnail kontrol
├── 04-hooks-bank.md                   ← 30 anti-pazarlama hook (TR + FR)
├── 05-topic-packs-index.md            ← tüm topic-pack'lerin özet listesi + master link
├── 06-anchor-rotation-tracker.md      ← anchor cümle + aile üyesi son kullanım kaydı (manuel)
└── sync-policy.md                     ← master-mirror senkronizasyon kuralları
```

## Kullanım workflow'u

### Yeni video çekimi öncesi (5 dakika)

1. **`00-INDEX.md`** aç → konu tipini bul
2. **`06-anchor-rotation-tracker.md`** kontrol et → son anchor + son aile üyesi ne zaman?
3. **`01-voice-checklist.md`** → bu konu için tema-eşleşme önerisi
4. **`03-script-format-checklist.md`** → süre kategorisi seçimi + bölüm yapısı + Beat D kapanış kontrolü
5. **`02-compliance-checklist.md`** → script taraması (yasak ifade var mı?)
6. Çekim sonrası → tracker'ı güncelle (kullanılan üye + tarih)

### Yeni topic pack üretimi

1. Master'da yaz: `wiki/youtube/topic-packs/<isim>.md`
2. Mirror'a özet ekle: `05-topic-packs-index.md`
3. `sync-policy.md` izle: tarihler, çapraz referans

### Aylık review (her ayın 1'i)

- `06-anchor-rotation-tracker.md` arşivle (önceki ay)
- Yeni boş tracker başlat
- Master'daki güncellemeleri mirror'a yansıt

## Master kanıt zinciri

Bu klasör YouTube üretim odaklıdır. **Klinik kanıt + kılavuz çapası** master vault'ta:

- `wiki/medical/concepts/supplement-vitamin-peptid-deneysel.md` — supplement/peptid/longevity hub
- `wiki/medical/concepts/intraovarian-prp.md`, `era-test.md`, `pgt-a.md`, vb.
- `wiki/medical/guidelines/` — ESHRE, NAMS, NICE, IMS, HFEA
- `wiki/brand/voice.md` — Dr. Aksoy ses + metaphor ailesi (canlı master)
- `wiki/youtube/` — channel-strategy, voice TR/FR, hooks-library, video-format, thumbnail-rules, seo-youtube TR/FR, topics-backlog, cross-reference-policy

## Yorum yanıtlama sistemi ile ilişki

| Sistem | Klasör | Amaç |
|---|---|---|
| **Yorum yanıtlama** | `../youtube-responses/` | Mevcut videoların altındaki hasta yorumlarına cevap |
| **İçerik üretim** (bu) | `youtube-content/` | Yeni video script + format + ses + uyumluluk |

İki sistem **aynı sesi** kullanır (Dr. Aksoy + metaphor ailesi) ama farklı operasyonel hedefler — yorum kısa, video uzun; yorum bireysel hasta, video genel kitle.

İki sistem ortak referansları:
- `voice` ilkeleri (master vault `wiki/brand/voice.md`)
- Disclaimer politikası (`../youtube-responses/disclaimer.md`)
- Editöryal kurallar (`../youtube-responses/editorial-rules.md`)
