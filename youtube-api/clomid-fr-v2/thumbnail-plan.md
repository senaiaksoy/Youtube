# Küçük resim planı — Clomid FR (97g8_8_Wcmc)

Durum: PLAN. Henüz görsel üretilmedi, hiçbir şey yüklenmedi. Kaynak kurallar: `.claude/skills/yt-pipeline/references/thumbnails.md`, `youtube-content/02-compliance-checklist.md` (F13).

## Dönüşüm (rotasyon) seçimi — `yt_thumb_compose.py --channel fr --check-variety` → OK
| Eksen | Seçim | Neden |
|---|---|---|
| template | **coral-contrast** (A) / **yellow-focus** (B, Test & Compare) | FR günlüğünde son 4 video classic-gold/amber-eyebrow; coral-contrast FR'de hiç kullanılmadı |
| side | **right** (doktor solda, yazı sağ %55) | son 4 FR video `left` |
| outfit | **white-coat** | son 4 FR video `scrubs` |
| pose | **pointing** (sakin, işaret parmağı yazıya) | son FR pozu `chin`; soru/yönlendirme temasına uygun |
| backdrop | **chart-data** (takvim ızgarası + hafif yükselen hormon eğrisi) | konu: takvim, döngü, ovülasyon; `cells-molecules` yasak |

## Yazı (F13: ilaç markası, kırmızı daire/ok, "%" iddiası, şaşkın yüz yok → "Clomid" yerine molekül adı)
- **A (coral-contrast):** satır 1 `PAS DE GROSSESSE` · satır 2 `SOUS CLOMIFÈNE ?` · pill `OVULATION ?`
- **B (yellow-focus, aynı taban görsel):** satır 1 `OVULATION ?` · satır 2 `OUI OU NON ?` · pill `CLOMIFÈNE`
- Başlık ile kancayı tekrar etme: başlık zaten "Clomid et pas de grossesse : quand changer de plan ?"

## Taban görsel (Higgsfield `gpt_image_2_5`, ~0,25 kredi/görsel; tavan önerisi 3 kredi)
- Referanslar (kimlik): `D:\A-klasör\Youtube\thumbs_fr_scan\thumbs\001_pqc9UgCIqo0.jpg`, `002_Uw2xfxw7N48.jpg` (white-coat).
- Prompt taslağı: "Wide 16:9 clean clinical editorial photo, Dr. Aksoy on the LEFT third wearing a crisp white doctor's coat over a shirt and tie, calm reassuring expression, one hand with index finger raised pointing gently toward the empty right side, soft warm clinic light; behind him a softly blurred wall calendar grid and a subtle rising hormone curve in warm amber/teal tones; keep the RIGHT 55 % clean and uncluttered for text. No text, no letters, no numbers, no logos, no syringes, no baby, no pregnant belly."
- Kontroller: yüz sadakati (gözlük, eller), ≥1 gözle karşılaştırma son 3 kanal küçük resmiyle, 120×68 mobil kanıt, dosya ≤2 MB, 1280×720.

## Uygulama sırası (onayından sonra)
1. `yt_thumb_compose.py --check-variety` (yukarıdaki kombinasyon) → taban görseli üret → A/B'yi birleştir (`--log-variety` ile günlüğe işle).
2. İki varyantı ve mobil kanıtı sana göster.
3. Onayla: `yt_thumbnail.py --channel fr` önce dry-run, sonra `--go` (yalnızca A). B'yi Test & Compare için Studio'da elle yüklersin (API'de yok).
