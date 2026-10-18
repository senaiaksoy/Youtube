# Render öncesi üç kapı

| Araç | Neyi durdurur | Komut |
|---|---|---|
| `facts.mjs` | kaynağa bağlanmamış rakam / hüküm / künye | `node …/tools/facts.mjs all <proje> --lang fr` |
| `legibility.mjs` | telefonda okunamayacak kadar küçük yazı | `node …/tools/legibility.mjs <proje>` |
| `variety.mjs` | önceki videolarla aynı görünüm (ilk grafik, kalem izleri, seri + yerleşim seti) | `node …/tools/variety.mjs check <proje>` |

Hepsi geçmeden `npx hyperframes render` yapılmaz.

# aspect.mjs — tek sahne, iki en-boy

`node …/tools/aspect.mjs <proje>` → `<proje>/shorts/`: `index.html`'in 1080×1920 kopyası (`<html data-aspect="9x16">`),
`scene-facts.json` (kaynak yolu bir üst klasöre göre düzeltilmiş), `.facts-cache`, `look.json` (+ `"aspect": "9x16"`) ve
`assets` bağlantısı (Windows'ta junction). `facts.mjs apply`'dan SONRA çalıştırılır. `shorts/index.html` elle düzenlenmez.
`legibility.mjs` dikey karede ayrıca alt %18'i ve sağ ikon sütununu (son 120 px, alt %55) denetler; her en-boyda kadrajdan
taşan yazıyı durdurur.

# variety.mjs — çeşitlilik kapısı

Projedeki `look.json`'u (`series`, `papers`, `first_graphic`, `layouts`, `pen_marks`, `stamp_flip`) `../series.json`
kataloğuna göre doğrular ve `youtube-content/motion/look-log.json`'daki son videolarla karşılaştırır.
`check <proje>` render öncesi, `log <proje> --lang fr` final render sonrası, `status` son videoları ve uzun süredir
kullanılmayan seri/yerleşimleri gösterir. Kurallar: `frame.md` § Series & Variety.

# make_papers.py — kâğıt zeminleri

`python3 tools/make_papers.py <spiral-fotoğrafı> assets/papers` zeminleri ve `papers.json` geometrisini yeniden üretir.
Ölçüler (renk, çizgi aralığı/kalınlığı, kesik/noktalı desen) Dr. Aksoy'un fotoğraflarından alındı ve dosyanın
başında yazılı; yalnızca spiral tel fotoğraftan kesilir. Ham fotoğraflar depoda tutulmaz.

# legibility.mjs — telefon okunurluk tabanı

Sahneyi HyperFrames'in kendi Chrome'unda açar, zaman çizelgesini 25 noktada (varsayılan) durdurur ve
ekranda görünen her yazının gerçek boyutunu ölçer (transform/scale dahil). Taban: **1080 px kısa kenarda
40 px** (16:9'da 2.1cqw); farklı çözünürlükte orantılı. Altında kalan her yazı ✖ ile ve en küçük olduğu
saniyeyle listelenir; çıkış kodu 1.

```
node youtube-content/motion/outsider-inside-frame/tools/legibility.mjs projects/<slug> [--samples 24] [--min 40] [--html index.html]
```

- Node 22+ (ek paket yok). Chrome yolu `npx hyperframes browser path`'ten; istenirse `HF_CHROME=/yol/chrome`.
- Muafiyet yalnızca gerçek görüntünün parçası olan yazıya: `data-legibility-exempt="neden"` (raporda görünür).
- `--min` yalnızca daha büyük taban için yükseltilir; düşürülmez.

# facts.mjs — kaynaktan sahneye bağ

Ekrandaki her sayı, bulgu, hüküm damgası ve künye `scene-facts.json`'dan gelir. Her kayıt, scriptin
bilimsel doğrulamadan geçmiş `-sources.md` dosyasındaki bir iddia ID'sine (C02, S1…) ve makaleyse PubMed
kaydına bağlıdır. Künyeler elle yazılmaz; PubMed'den üretilir.

## Akış (her yeni sahne)

1. Script yazılır → yt-script-factcheck çalışır → `-sources.md` güncel.
2. Proje klasöründe `scene-facts.json` yazılır (aşağıdaki şema). Her ekran öğesi bir iddia ID'sine bağlanır.
3. `index.html`'de ekran öğeleri boş bırakılıp bağlanır:
   - `data-fact="F2"` (metin) · `data-fact="F2" data-field="label"` (etiket)
   - `data-ref="R1"` (künye) · `data-ref="R1" data-field="design"` (tasarım · n) · `data-ref="R1" data-field="marker"` ([1])
   - Dile göre değişen ama bilgi taşımayan metin (bölüm başlığı): `data-chrome="chapter"` → `scene-facts.json` içinde `"chrome"`;
     yalnızca başlık ve 100'den küçük bölüm numarası taşıyabilir, veri taşıyamaz
   - Gerçek bilgi olmayan sayılar (bölüm numarası vb.): `data-fact-exempt="neden"`
4. Çalıştır (Node 18+, ek paket yok):

   ```
   node youtube-content/motion/outsider-inside-frame/tools/facts.mjs all projects/<slug> --lang fr
   ```

   `fetch` PubMed kaydını `.facts-cache/` altına yazar (commit edilir; çevrimdışı render ve "o gün PubMed ne
   diyordu" kaydı için) → `apply` metinleri HTML'e yazar → `verify` denetler.
   `apply`, `<html lang>` etiketini de dile göre ayarlar (Türkçede büyük harf İ/I doğru çıkar; dile özel CSS `:lang(tr)` ile yazılır).
5. `verify` geçmeden `npx hyperframes check` / `render` yapılmaz. Aynı sahne `--lang tr` / `--lang en` ile diğer
   kanallar için yeniden üretilir.

## verify neyi durdurur

- İddia ID'si `-sources.md`'de yok
- O iddianın son karar satırı ❌ / ❓ / 🕒 (bilinçli istisna: kayda `"override": "gerekçe"`; raporda görünür)
- Kayıttaki bir sayı ne iddia satırında, ne onun atıf yaptığı S-kaynağında, ne de PubMed abstract'ında var
- Makale PubMed'de geri çekilmiş / "Expression of Concern"
- Rakam veya hüküm ekranda ama künyesi ekranda değil
- Hüküm sabit sözlük dışında (FR: PREUVE SOLIDE · PREUVE FAIBLE · NON PROUVÉ · NON RECOMMANDÉ · ÇA DÉPEND; TR/EN karşılıkları frame.md'de)
- Ekranda bağlanmamış herhangi bir rakam
- HTML'deki metin `scene-facts.json`'dan farklı (`apply` çalıştırılmamış)

Uyarı (durdurmaz): iddia için satır bazlı karar bulunamadı (rapor yalnızca toplamları veriyorsa). `--draft`
bayrağı bazı hataları uyarıya çevirir; yayın render'ında kullanılmaz.

## Sınırlar

Araç izlenebilirliği mekanik olarak denetler; iddianın doğruluğuna karar vermez. O karar yt-script-factcheck
raporu ve Dr. Aksoy'un onayıdır. Popülasyon, payda, kesinlik gibi nüansların ekranda/seste korunması hâlâ
insan denetimidir.

## scene-facts.json şeması

```json
{
  "lang": "fr",
  "sources_md": "../../youtube-content/video-script-<konu>-sources.md",
  "refs": {
    "R1": { "pmid": "36472596", "n": "767",
            "design": { "fr": "Essai randomisé multicentrique", "tr": "…", "en": "…" } },
    "R2": { "label": { "fr": "ESHRE, guideline 2025", "tr": "…", "en": "…" } }
  },
  "chrome": { "chapter": { "fr": "07 · Test ERA", "tr": "07 · ERA testi", "en": "07 · The ERA test" } },
  "facts": [
    { "id": "Q1", "kind": "quoted", "origin": "nereden geldiği", "text": { "fr": "« … »" } },
    { "id": "F1", "kind": "statement", "claim": "C01", "ref": "R1", "text": { "fr": "…" } },
    { "id": "F2", "kind": "figure", "claim": "C02", "ref": "R1", "text": { "fr": "58,5 %" }, "label": { "fr": "…" } },
    { "id": "V1", "kind": "verdict", "claim": "C01", "ref": "R1", "text": { "fr": "NON PROUVÉ" } }
  ]
}
```

- `kind`: `quoted` (üstü çizilecek iddia; kaynağı `origin`), `statement`, `figure`, `label`, `verdict`
- `figure` ve `verdict` için `ref` zorunlu; PMID'siz kaynak (kılavuz, SmPC) `label` ile yazılır
- Örnek: `../example-era/` (`scene-facts.json`, `era-sources.md`, `index.html`)


## pen.mjs — videoya özel tohum (2026-10-17)

```
node tools/pen.mjs apply <sahne> [<sahne> …]   # videonun bütün sahneleri, akış sırasıyla; facts apply / aspect'ten ÖNCE
node tools/pen.mjs show  <sahne> …             # ne seçeceğini yazar, dosyaya dokunmaz
```
- `look.json` `seed` (yoksa video klasör adından türetilir ve geri yazılır). Aynı video = aynı sonuç, sonraki video = farklı.
- `<img class="pen" data-pen="strike|underline|loop|arrow|question" data-pen-tool="round|chisel">`: Dr. Aksoy'un gerçek
  izlerinden aynı tür/araç/biçimde olanı seçer (videoda aynı iz arka arkaya gelmez), ayna, ± açı, yükseklik ve hafif
  eğrilik verir. İz asla programla çizilmez. `data-pen-fixed="<id>"` sabitler.
- `data-stamp` (−6° → −2,5°, maske a/b), `<audio data-sfx="pen|stamp|ink-tap">` (aynı kayıt arka arkaya yok),
  `<html data-ink-seed>` (assets/ink çizgileri).
- Seçilen izler `look.json` `pen_marks`'a yazılır; önceki videoyla aynı küme çıkarsa tohum ilerletilir.

## variety.mjs suggest

`node tools/variety.mjs suggest <seri> [--seed N]` → seri ailelerinden (series.json "families") kapıyı geçen bir
first_graphic + yerleşim seti önerir; son 4 videoda kullanılmayanlar önce.

## facts-draft.mjs — kaynak dosyasından ekran verisi taslağı (2026-10-17)

```
node tools/facts-draft.mjs <video-script-…-sources.md> <sahne> [--claims C02,C15] [--force]
```
- İddia kaydındaki satırları (`| C07 |`, `| C03–C04 |`) ve `### S2 —` kaynak bölümlerini facts.mjs ile aynı kurallarla okur;
  son ✅/⚠/❌/❓/🕒 satırı iddianın kararıdır.
- ❌ / ❓ / 🕒 iddialar taslağa alınmaz (ekrana çıkamaz). Karar satırı olmayanlar uyarıyla alınır.
- Her iddia için `kind: statement`, metin `TODO` (fr/tr/en) ve yazara yardımcı `_claim`, `_numbers`, `_verdict`, `_pmids`;
  iddiaların kaynak gösterdiği her PMID için bir ref (design/n `TODO`). Geri çekilme geçen kaynak işaretlenir.
- Ekran cümlesi ve rakam **uydurmaz**: yazar metni yazar, rakamı yalnızca `_numbers`'tan seçer.
- `facts.mjs verify` artık `TODO` kalan her alanda başarısız olur (`--draft` ile uyarı).

## captions.mjs — Shorts pop-up altyazı (2026-10-18)

```
node tools/captions.mjs <words.json> <başlangıç_s> <bitiş_s> <çıkış.ass> [--size 62] [--max-words 3] [--max-chars 20]
ffmpeg -i short.mp4 -vf "ass=çıkış.ass:fontsdir=<outsider-inside-frame>/assets/fonts" -c:v libx264 -crf 17 -c:a copy short-altyazi.mp4
```
- Her Shorts'a gömülü pop-up altyazı konur (Dr. Aksoy kararı); 16:9 videoya konmaz.
- `words.json`: konuşulan kelimeler, kaynak saniyesiyle (`[[kelime, başlangıç, bitiş], …]` ya da transcriber çıktısı). Aralık, Short'un
  kesildiği kaynak aralığıdır; süreler 0'a kaydırılır. Metin söylenen metindir; yayından önce kayda karşı okunur.
- Görünüm: Plex Sans SemiBold 62 px, kâğıt kutu üzerinde mürekkep, kart başına 1–3 kelime, 100 ms "pop". Konum: Shorts arayüzünün
  hemen üstündeki altyazı bandı (yüksekliğin %76,5–82'si); `legibility.mjs` Shorts sahnelerinin kendi yazısını bu banttan uzak tutar.
