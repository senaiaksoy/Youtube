---
type: sync-policy
domain: youtube-content-production
created: 2026-04-26
master: D:/A-klasör/obsidian-vaults/draksoyivf-knowledge/wiki/
mirror: D:/A-klasör/Youtube yorum yanıtlama/youtube-content/
---

# Sync Policy — Master / Mirror Senkronizasyonu

## Master (kanonik kaynak)

`D:/A-klasör/obsidian-vaults/draksoyivf-knowledge/wiki/`

### Master sahipliği
- **Tüm klinik kanıt çapası, kılavuz pozisyonu, GRADE** → master
- **Detaylı topic packs (full text)** → master
- **Voice + metaphor family full sözlüğü** → master
- **Hub knowledge backend** (supplement-vitamin-peptid-deneysel.md) → master

### Master güncelleme süreci
1. Doğrudan `wiki/` içinde edit
2. `log.md` entry yaz
3. Eğer YouTube üretimini etkiliyorsa → mirror güncellemesi de yapılır

## Mirror (operasyonel referans)

`D:/A-klasör/Youtube yorum yanıtlama/youtube-content/`

### Mirror sahipliği
- **Hızlı checklist + protokol özetleri** → mirror
- **Çekim öncesi kontrol listeleri** → mirror
- **Anchor / aile üyesi rotation tracker** (operasyonel veri) → SADECE mirror
- **Topic-packs özet listesi** → mirror (master'da full)

### Mirror güncelleme kuralları

- **Mirror direkt düzenlenmez** — master'dan beslenir
- İstisna: `06-anchor-rotation-tracker.md` operasyonel verisi (yayın tarihi, kullanılan hook, vb.) — bu master'da yok, sadece mirror'da

### Mirror dosyaları master'a karşı

| Mirror dosyası | Master kaynağı | Sync türü |
|---|---|---|
| `README.md` | (yok) | Mirror-özel |
| `00-INDEX.md` | (yok) | Mirror-özel |
| `01-voice-checklist.md` | `wiki/brand/voice.md` §"Metaphor Ailesi" | Özet (master full) |
| `02-compliance-checklist.md` | `wiki/youtube/topic-packs/.../Ek Araç 3` | Özet |
| `03-script-format-checklist.md` | `wiki/youtube/video-format.md` + topic-pack | Özet |
| `04-hooks-bank.md` | `wiki/youtube/topic-packs/.../Ek Araç 1` + `wiki/youtube/hooks-library.md` | Birleşik özet |
| `05-topic-packs-index.md` | `wiki/youtube/topic-packs/` (klasör listesi) | Özet liste |
| `06-anchor-rotation-tracker.md` | (yok — operasyonel veri) | Mirror-özel |
| `sync-policy.md` | (bu dosya) | Mirror-özel |

## Senkron tetikleyicileri

### Master değişikliği → Mirror güncellemesi gerek

1. **`wiki/brand/voice.md` değiştiğinde**
   → `01-voice-checklist.md` güncel mi kontrol et
   → Yeni aile üyesi eklendiyse hızlı tabloya ekle

2. **`wiki/youtube/topic-packs/` yeni dosya eklendiğinde**
   → `05-topic-packs-index.md` özetini ekle

3. **`wiki/youtube/hooks-library.md` veya topic-pack hook bölümü değiştiğinde**
   → `04-hooks-bank.md` güncelle

4. **`wiki/youtube/video-format.md` değiştiğinde**
   → `03-script-format-checklist.md` güncelle

5. **Mevzuat değişikliği** (TR SB Tanıtım, FR Code santé publique, FDA/EMA, ARCOM/CSA)
   → `02-compliance-checklist.md` güncelle (master'da topic-pack §"Ek Araç 3" + brand/compliance.md)

### Mirror değişikliği → Master'a yansıma

- `06-anchor-rotation-tracker.md` operasyonel veri → master'a aktarılmaz; mirror-özel
- Eğer mirror'da yeni bir checklist kalıbı keşfedilirse → master'a editöryal protokol olarak eklenir

## Aylık senkron review (her ayın 1'i)

1. Master `log.md` son ayın değişikliklerini gözden geçir
2. YouTube ile ilgili güncellemeler var mı? Mirror'a yansıt
3. Mirror tracker arşivle (`archive/YYYY-MM-anchor-tracker.md`)
4. Yeni boş tracker başlat
5. Bu sync-policy dosyasını "updated" tarihine güncelle

## Çelişki durumunda

**Master kazanır.**

Eğer mirror'da bir bilgi master ile çelişiyorsa, master'daki versiyon doğru kabul edilir. Mirror düzeltilir.

## Arşiv ve tarihsel kayıt

- Aylık trackerlar `archive/YYYY-MM-anchor-tracker.md` formatında
- Eski topic-pack mirror özetleri `archive/YYYY-MM-topic-packs-snapshot.md`
- Master log: `wiki/log.md` (proje ana logu, ana referans)

## Yorum yanıtlama sistemi ile paralel ilişki

`../youtube-responses/` (kardeş sistem):
- Editöryal kurallar (`editorial-rules.md`) — bu mirror ile uyumlu olmalı
- Disclaimer (`disclaimer.md`) — bu mirror ile uyumlu olmalı
- Şablon güncellemeleri yorum yanıtlama'da olur; mirror'da etkisi yoksa müdahale yok

İki sistem ortak:
- Dr. Aksoy ses (master `wiki/brand/voice.md`)
- Marka uyumluluğu (master `wiki/brand/compliance.md`)
- TR + FR + EN + AR dil profilleri

## Versiyon geçmişi

| Tarih | Değişiklik |
|---|---|
| 2026-04-26 | İlk versiyon — youtube-content/ alt sistemi kuruldu (7 dosya) |
