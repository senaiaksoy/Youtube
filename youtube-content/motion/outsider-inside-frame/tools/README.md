# Render öncesi iki kapı

| Araç | Neyi durdurur | Komut |
|---|---|---|
| `facts.mjs` | kaynağa bağlanmamış rakam / hüküm / künye | `node …/tools/facts.mjs all <proje> --lang fr` |
| `legibility.mjs` | telefonda okunamayacak kadar küçük yazı | `node …/tools/legibility.mjs <proje>` |

İkisi de geçmeden `npx hyperframes render` yapılmaz.

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
