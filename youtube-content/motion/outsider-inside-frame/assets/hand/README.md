# El yazısı kütüphanesi (Dr. Aksoy, tükenmez kalem, 2026-10-17)

Dr. Aksoy'un boş bir sayfaya yazdığı notlardan kesildi; mürekkep yoğunluğu alfa olarak korundu, renk `{colors.ink}`
(#1B2230). Ham fotoğraf depoda tutulmaz. Liste: `hand-library.json`.

| Tür | Dosyalar |
|---|---|
| Kelime (yalnızca FR kanalı) | `attention-fr`, `pas-prouve-fr`, `important-fr`, `ete-fr` (örnek kelime) |
| Ok | `arrow-right-01` (çift uçlu), `arrow-right-02`, `arrow-left-01/02`, `arrow-up-01`, `arrow-down-01` |
| İşaret | `question-01`, `underline-double-01` |

Kurallar
- El yazısı **mürekkep rengidir, hüküm değildir**: kırmızı kalem (assets/pen) yargı içindir; el yazısı not, ok ve vurgu içindir.
- Kelimeler yalnızca kendi dilinde: `-fr` dosyaları `.only-fr` ile FR sürümde görünür. TR/EN için Dr. Aksoy'un kendi el
  yazısıyla ayrı sayfa gerekir (Dikkat · Kanıtlanmadı · Önemli / Careful · Not proven · Important); o gelene kadar TR/EN'de
  yalnızca dilden bağımsız işaretler (ok, soru işareti, çift alt çizgi) kullanılır.
- Okunurluk: el yazısı kelime en az doğal boyutun 1,3 katı (yükseklik ≥ 130 px @1080) kullanılır; çizgi incedir, telefonda
  daha küçüğü okunmaz. Kelime bilgi taşıyorsa (ör. "Pas prouvé") aynı bilgi ekranda dizgi metin ya da damga olarak da vardır.
- Açılış: `assets/pen/pen.css` `.pen` maskesiyle yazılıyormuş gibi açılır (`--p` 0→1, 0,5–0,8 sn; oklar ucuna doğru).
  Ses: `assets/sfx/pen-*.wav` (aynı sesi arka arkaya kullanma). Karede en fazla bir el yazısı öğe + bir ok.
