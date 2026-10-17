# El yazısı kütüphanesi (Dr. Aksoy, tükenmez kalem, 2026-10-17)

Dr. Aksoy'un boş sayfalara yazdığı notlardan kesildi (FR sayfası; TR/EN sayfası aynı gün); mürekkep yoğunluğu alfa olarak korundu, renk `{colors.ink}`
(#1B2230). Ham fotoğraf depoda tutulmaz. Liste: `hand-library.json`.

| Tür | Dosyalar |
|---|---|
| Kelime — FR | `attention-fr`, `pas-prouve-fr`, `important-fr`, `ete-fr` (örnek kelime) |
| Kelime — TR | `dikkat-tr` (Dikkat!), `kanitlanmadi-tr`, `onemli-tr` |
| Kelime — EN | `careful-en` (Careful!), `important-en` (Important!) — « Not proven » yok (sayfada yazım hatalı, yeniden yazılacak) |
| Ok | `arrow-right-01` (çift uçlu), `arrow-right-02`, `arrow-left-01/02`, `arrow-up-01`, `arrow-down-01` |
| İşaret | `question-01`, `underline-double-01` |

Kurallar
- El yazısı **mürekkep rengidir, hüküm değildir**: kırmızı kalem (assets/pen) yargı içindir; el yazısı not, ok ve vurgu içindir.
- Kelimeler yalnızca kendi dilinde: `-fr` / `-tr` / `-en` dosyaları `.only-fr` / `.only-tr` / `.only-en` ile yalnızca o dil
  sürümünde görünür (`facts.mjs apply --lang` `<html lang>`'ı ayarlar). Ok, soru işareti ve çift alt çizgi her dilde kullanılır.
  Bir sahnede kelime kullanılıyorsa üç dilin karşılığı birlikte konur (ör. `notes`: Important · Önemli · Careful!).
- TR/EN kelimeler daha düşük çözünürlüklü bir fotoğraftan kesildi ve kalem kalınlığı FR ile eşleşsin diye 1,4× büyütüldü;
  bu yüzden 1,3× kuralının üstüne fazla çıkılmaz (en fazla ~2×), daha büyüğü yumuşak görünür.
- Okunurluk: el yazısı kelime en az doğal boyutun 1,3 katı (yükseklik ≥ 130 px @1080) kullanılır; çizgi incedir, telefonda
  daha küçüğü okunmaz. Kelime bilgi taşıyorsa (ör. "Pas prouvé") aynı bilgi ekranda dizgi metin ya da damga olarak da vardır.
- Açılış: `assets/pen/pen.css` `.pen` maskesiyle yazılıyormuş gibi açılır (`--p` 0→1, 0,5–0,8 sn; oklar ucuna doğru).
  Ses: `assets/sfx/pen-*.wav` (aynı sesi arka arkaya kullanma). Karede en fazla bir el yazısı öğe + bir ok.
