# Video şablon kütüphanesi

Her video kendi görsel dünyasıyla yapılır (Dr. Aksoy kararı, 2026-11-07). Bir şablon bütün videonun rengini, yazısını, kompozisyonunu, hareket yasasını ve bindirmelerini belirler. `outsider-inside-recut` skill'i şablonu buradan seçer.

## Akış

```bash
node ../outsider-inside-frame/tools/variety.mjs status --lang fr
```

```bash
node ../outsider-inside-frame/tools/variety.mjs pick chiffres --lang fr
```

Çıkan JSON projenin `look.json` dosyası olur. `layouts` listesi videonun kullandığı sahne türlerine indirilir. Her sahne şöyle kurulur:

```bash
node tools/world.mjs new gazete figure <proje>/hyperframes/s03 --palette bleu --variant a --seed 4112 --lang fr --duration 9
```

Render öncesi kapılar (`facts.mjs`, `legibility.mjs`, `aspect.mjs`, `variety.mjs check`, `hyperframes check`) kâğıt dünyasındakiyle aynıdır. Final render'dan sonra `variety.mjs log`.

## Dosyalar

- `templates.json`: şablonlar, paletler, seri uyumu, rotasyon penceresi, her dünyada geçerli kurallar ("universal").
- `worlds/<id>/`: bir dünyanın `world.css` (token, kompozisyon) ve `world.js` (hareket yasası, arka plan) dosyaları.
- `kit/shared/`: ortak sahne iskeleti ve hareket API'si (`K.in`, `K.big`, `K.strike`, `K.stamp`, `K.bar`, `K.pushIn`).
- `fonts/`: yerel yazı tipleri (SIL OFL 1.1; lisanslar aynı klasörde).
- `catalog.json`: HyperFrames kataloğunun politika etiketli anlık görüntüsü.
- `tools/`: `world.mjs` (iskelet, demo), `validate.mjs` (tüm kapılar), `sheet.mjs` (kontak sayfası), `catalog.mjs` (katalog araması).
- `demos/`: üretilen sınama sahneleri, depoya girmez.

## Sahne türleri

`claim` · `figure` · `bars` · `process` · `verdict` · `chapter` · `closing` · `talking` · `footage` · `cta`

Sahnedeki kimlikler (Q1, F1, K1, R1…) yer tutucudur; gerçek videoda `scene-facts.json` kimlikleriyle değiştirilir.

## Katalogdan parça eklemek

```bash
node tools/catalog.mjs find chart
```

`find` yalnızca kullanılabilir öğeleri listeler; `--all` engellileri nedeniyle gösterir. Öğe `npx hyperframes add <ad>` ile sahneye kurulur ve dünyanın token'larına bağlanır. Katalog güncellemek için `node tools/catalog.mjs sync`.

## Yeni şablon eklemek

1. `worlds/<id>/world.css` ve `world.js` yaz. Sahne iskeletine dokunma; kompozisyonu `world.css` değiştirir.
2. `templates.json`'a ekle: `status`, `feel`, `fit`, `palettes`, `name`, `sources` (repo, öğe, lisans).
3. `node tools/world.mjs demo <id>`
4. `node tools/validate.mjs <id>` (10 sahne, 16:9 ve 9:16)
5. `node tools/sheet.mjs <çıktı>.png --worlds <id> --kinds claim,figure,verdict` ile gözle bak. Kapılar renk uyumsuzluğunu ve kompozisyon tekrarını yakalamaz: bu kütüphanede siyah üstüne siyah çizgi ve metne binen kâğıt parçası kapılardan geçmişti, gözle bulundu.

Yalnızca lisansı açık kaynaklardan yararlanılır. Gerçek bir markanın, kişinin veya yayının görünümü taklit edilmez.

## Kaynak notu

`hyperframer.com/bookmark/templates/` incelendi ve kullanılmadı: orası Framer web sitesi şablonlarının dizini, video şablonu içermiyor ve lisans bilgisi vermiyor. Kaynaklar `THIRD_PARTY.md` dosyasında.
