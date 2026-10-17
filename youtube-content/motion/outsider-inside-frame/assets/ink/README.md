# Mürekkep çizgileri (rough.js, 2026-10-17)

`ink.js` = şema kutuları, bağlantı okları ve taralı çubuklar; yalnızca mürekkep rengi (#1B2230).
Kütüphane: rough.js 4.6.6 (MIT, `LICENSE-roughjs.txt`).

Kurallar (Dr. Aksoy kararı, 2026-10-17)
- **Kırmızı kalem asla üretilmez.** Üstü çizme, daire, alt çizgi ve damga Dr. Aksoy'un gerçek izleridir
  (`assets/pen`, `tools/pen.mjs`). Bu dosya yalnızca siyah mürekkepli şema çizgileri içindir; el yazısı da üretmez.
- Tohum `<html data-ink-seed>`'ten gelir (`tools/pen.mjs apply` yazar): aynı video aynı çizgiler, sonraki video farklı.
- Seek-safe: şekiller yüklemede bir kez kurulur; çizilme GSAP ile stroke-dashoffset tween'i.
- Yazı fontları geç yüklenebilir: kutuyu yazının ölçüsüne göre değil, CSS'te sabit boyutlu kutuya göre çiz.

Kullanım: `example-layouts/flux-A`, `arbre-A`, `barres-A`.
```html
<script src="assets/ink/rough-4.6.6.js"></script>
<script src="assets/ink/ink.js"></script>
…
const ink = oiInk.layer('#root');
ink.draw(tl, ink.boxAround('#n1', 4), 1.0, 0.55);
ink.draw(tl, ink.arrow([[x1, y1], [x2, y2]], { bend: 18 }), 1.7, 0.4);
ink.draw(tl, ink.hatch(x, y, w, h), 2.0, 1.0);
```
