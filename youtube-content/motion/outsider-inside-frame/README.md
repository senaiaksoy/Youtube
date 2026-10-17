# Outsider Inside — HyperFrames ana tasarım şablonu

`frame.md` = 2026-10-15 ve sonrasında başlayan TÜM HyperFrames projelerinin tasarım sistemi.
Önceki projeler (fiv-apres-quarante-ans-hyperframes, videos/bhcg-*, motion/intro-pilot) kendi
frame.md / DESIGN.md dosyalarıyla kalır; onlara dokunulmaz.

## Yeni proje açarken
1. `npx hyperframes init projects/<slug>`
2. Bu klasördeki `frame.md` dosyasını projenin KÖKÜNE kopyala (adı küçük harfle `frame.md`).
   Projede `DESIGN.md` oluşturulmaz — HyperFrames önce `frame.md` okur.
3. `assets/` altındaki alt klasörleri projeye kopyala (fonts, textures, pen, footage) ve
   `index.html` içine `assets/fonts/fonts.css` ve `assets/pen/pen.css` stil dosyalarını bağla.
4. Ekrandaki her rakam/bulgu/künye için `scene-facts.json` yaz (scriptin `-sources.md` iddia ID'lerine bağlı), HTML'de
   `data-fact` / `data-ref` ile bağla ve çalıştır: `node youtube-content/motion/outsider-inside-frame/tools/facts.mjs all projects/<slug> --lang fr`.
   `verify` geçmeden render yok. Ayrıntı: `tools/README.md`.
5. Cep telefonu okunurluğu: `node youtube-content/motion/outsider-inside-frame/tools/legibility.mjs projects/<slug>`.
   Ekranda görünen her yazı ≥ 40 px (1080 kısa kenarda) olmalı; geçmeden render yok. Sığmıyorsa yazıyı kısalt
   veya kareyi ikiye böl — küçültme.
6. Seri ve çeşitlilik: projeye `look.json` yaz (seri, kâğıt, ilk grafik, yerleşimler, kalem izleri) ve
   `node youtube-content/motion/outsider-inside-frame/tools/variety.mjs check projects/<slug>` çalıştır; son videolarla
   aynı görünüm seçilmişse durdurur. Final render'dan sonra `variety.mjs log projects/<slug> --lang fr`.
   Hangi seri ne için: `frame.md` § Series & Variety; örnek sahneler `example-series/`.
7. Projeye özel değişiklik gerekiyorsa projedeki kopyada yap; ana şablonu değiştirmek
   tüm gelecek videoları etkiler — yalnızca bilinçli kararla güncelle.

## Hazır varlıklar
- `assets/fonts/` → Literata (variable, roman + italik) + IBM Plex Sans 400/600, WOFF2, FR + TR karakterleri doğrulandı (`test/font-testcard.png`). Lisans: SIL OFL 1.1.
- `assets/textures/paper-grain-16x9.png` / `-9x16.png` → gerçek A4 fotoğrafından kâğıt dokusu (ışık farkı temizlendi); `soft-light`, opaklık 0.35 (`test/paper-preview.png`).
- `assets/textures/stamp-mask.png` → hüküm damgası için mürekkep dokusu maskesi; gerçek kaşe baskısına göre ayarlandı (`test/stamp-test.png`). Not: maske yalnızca http üzerinden çalışır (HyperFrames preview/render zaten öyle).
- `assets/pen/` → Dr. Aksoy'un elle çizdiği 14 gerçek kalem izi (üstünü çizme, daire, altını çizme, ok, soru işareti; ince ve kalın uçlu), kırmızıya çevrildi; `pen.css` ile kendini çizerek açılır (`test/pen-test.png`).

- `assets/sfx/` → Dr. Aksoy'un kaydettiği gerçek sesler: 3 kalem hışırtısı, 2 damga vuruşu, 2 ıstampa tıkırtısı (temizlendi, seviyelendi). Kullanım: `assets/sfx/README.md`.
- `assets/footage/` → 15 laboratuvar fotoğrafı + 5 embriyo görüntüsü; hasta bilgisi taşıyabilecek kâğıt/etiketler bulanıklaştırıldı, meta veriler silindi. Kullanım ve durum listesi: `assets/footage/INDEX.md`.

- `assets/papers/` → Dr. Aksoy'un fotoğrafladığı 4 kâğıttan ölçülerek yeniden çizilen zeminler: reçete kâğıdı (antetsiz), krem çizgili defter, spiral lab defteri (gerçek spiral), kareli kâğıt. Fotoğraflardaki baskı yazısı, logo, iletişim bilgisi, el yazısı ve arkadan geçen yazılar kullanılmadı; ham fotoğraflar depoya konmadı. Üretici: `tools/make_papers.py`.

## Açık kararlar
- (2026-10-17) Her video aynı görünmesin: 5 seri (mythe / labo / questions / chiffres / conseils), her biri kendi kâğıdıyla; `look.json` + `tools/variety.mjs` son 3 videoyla aynı kombinasyonu engeller. Örnekler `example-series/`.
- (2026-10-16) Kanal intro'su kullanılmaz (Dr. Aksoy kararı): video Dr. Aksoy'la açılır, doğrudan içeriğe girer; logo/bumper yok.
- (2026-10-16) Motion grafikteki tüm yazılar cep telefonunda okunur boyutta: taban 40 px @1080 (16:9'da 2.1cqw), `tools/legibility.mjs` ile denetlenir.
- (2026-10-16) `lab-02` meslektaş izni ve `lab-14` kullanım hakkı Dr. Aksoy tarafından onaylandı; ikisi de kullanılabilir.
- (2026-10-16) Hastane logosu görünmeyecek (Dr. Aksoy kararı): `lab-09` ve `lab-12`'deki logolu kitapçık bulanıklaştırıldı; yeni görüntülerde de logo bulanıklaştırılır.
- Video çekimleri (time-lapse, mikroskop kaydı) geldikçe `assets/footage/` altına eklenir.

## Referans örnek
- `example-era/` (ekran bilgileri `scene-facts.json` + `era-sources.md` üzerinden bağlı) → 10 sn'lik onaylanmış deneme sahnesi (ERA iddiası → kalemle çizilir → kanıt → rakamlar + referans kartı → NON PROUVÉ damgası; kalem ve damga sesli). Kaynak: Doyle N, et al. JAMA 2022;328(21):2117-25 (PubMed 36472596). `index.html` yeni sahneler için kalıp olarak kullanılır; çalıştırmak için şablonun `assets/` klasörünü yanına kopyala ve GSAP'ı `assets/vendor/gsap.min.js` olarak koy (ya da CDN satırına çevir).
