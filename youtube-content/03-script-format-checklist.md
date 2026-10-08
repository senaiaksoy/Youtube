---
type: script-format-checklist
domain: youtube-content-production
master-source: wiki/youtube/video-format.md + wiki/youtube/topic-packs/supplement-peptid-longevity-pack-2026-04-26.md
updated: 2026-10-06
version: 2026-10-06-abi-baba-katmani
---

# 03 — Script Format Checklist

## Script teslim biçimi ve ton

İç plan bu dosyadaki başlıkları ve kontrol kutularını kullanabilir; kullanıcıya teslim edilen nihai script ise düz metin olmalıdır.

- [ ] Nihai metin tablo, madde işareti, Markdown başlığı, emoji veya senaryo sütunları olmadan okunabilir düz metin halinde
- [ ] Reji/görsel notları script gövdesine karıştırılmadı; gerekiyorsa metnin sonunda ayrı `REJİ NOTLARI` bloğunda verildi
- [ ] Kaynaklar ve disclaimer konuşma metninden ayrı teslim edildi; kaynak numaraları sesli okunmadı
- [ ] Cümleler konuşulabilir uzunlukta; paragraf başına tek ana fikir var
- [ ] Çeviri kokusu yok; hedef dilde doğal, gündelik ve sesli okunabilir

### Özgün gözlemci mizah modu

Belirli yaşayan bir komedyenin birebir cümle yapısı, personası veya imza esprileri taklit edilmez. Kullanılacak özgün ton:

- Gündelik bir gözlemle başlayıp klinik gerçeğe bağlanan kuru mizah
- Abartılı ama anlaşılır bir benzetme; benzetme biyolojiyi açıklamıyorsa çıkarılır
- Beklenmedik kısa dönüş; ardından hemen kanıta ve ana mesaja dönülür
- Mizahın hedefi hasta değil, internet efsanesi, sahte kesinlik veya pazarlama dili
- Sıcak, zeki ve kendini fazla ciddiye almayan anlatım; bağıran, küçümseyen veya gösterişli punchline yok
- Hassas konularda mizah ve metafor yok: düşük, tekrarlayan gebelik kaybı, POI/POF, kanser sonrası fertilite, donör kararı ve ciddi kötü haberler

> Mizah kotası yoktur. Bir bölümde doğal bir gözlem yoksa espri eklenmez. Her mizahi dönüş en geç bir-iki cümle içinde klinik açıklamaya bağlanır.

### "İşini bilen komik abi/baba" katmanı (2026-10-06)

> Master: `wiki/youtube/video-format.md` § aynı başlık · üst kaynak `wiki/brand/voice.md` §3. Uygulama: `.claude/skills/yt-script-{tr,fr,en}`.

Videolar ders anlatır gibi olmamalı: samimi, içimizden biri, komik ama işini çok iyi bilen bir abi/baba; espriler gözde canlanır.

- [ ] **Sahne:** Genel ifade yerine somut an (nesne, saat, yer)
- [ ] **İç ses:** En fazla bir cümle, ardından "bu çok insani" normalleştirmesi
- [ ] **Kendine dönük sıcaklık:** Hekimlerin genel alışkanlıkları; anı/hasta hikâyesi/klinik olay uydurulmadı
- [ ] **Baba esprisi:** En fazla bir kez (TR "baba esprisi", FR *blague Carambar*, EN *dad joke*)
- [ ] **Gündelik abartı:** Açıkça abartı olarak duyuluyor, bulgu gibi sunulmadı
- [ ] **Stand-up dozu (2026-10-06; yoğunluk 2026-10-08'de artırıldı):** Hassas olmayan konuda açılış bir sahneyle; açılış sahnesi uzunsa önce başlık sorusu + doğrulanmış kısa cevap (ilk ~20 kelime), sonra sahne; hassas olmayan bölümlerde yoğun mizah (her paragrafta bir ters köşe serbest; ölçü: Dr. Aksoy'un "première échographie" FR metni); sonda 1–2 callback ve kapanış cevabı açılış sorusuyla birebir eşleşiyor; tablolar ekranda; kayıp, yaş, risk, dış gebelik ve acil cümleleri mizahsız; kaygıyı etiketleyen ("panique") veya hastayı suçlayan ifade yok; kişisel an Dr. Aksoy'un onayladığı gerçek bir an
- [ ] **Açıklayan benzetme:** En fazla 2; her biri kavramı açıklıyor (çıkarılınca anlama azalıyor); kavramın ilk anlatıldığı yerde; gerekiyorsa sınırı söylendi; örtük bilgisi doğrulandı; kapanışta yalnızca geri dönüş
- [ ] **Canlandırma:** Sus, SFX ve karakter notları `REJİ NOTLARI` bloğunda
- [ ] **Kulak için yazım:** Konuşma doğallığı geçişi yapıldı (ünlem, söylem belirleyici, izleyiciye soru, soru-cevap, kendini düzeltme, vurgu tekrarı). Her öğe bir duygu ya da geçiş taşıyor
- [ ] **Ölçü:** Paragraf başına ≤1 ünlem; aynı ünlem videoda ≤2; ardışık paragraflar farklı belirleyiciyle başlıyor; "eee/ııı" yazılmadı; dini çağrışımlı ünlem ve argo yok
- [ ] **Sesli okuma:** Yapıldı ya da DURUM alanına "sesli okunmadı" yazıldı

### Yazım sonrası bilimsel doğrulama (zorunlu, 2026-10-06)

> Master: `wiki/youtube/video-format.md` § aynı başlık · Uygulama: `.claude/skills/yt-script-factcheck`

- [ ] Doğrulama, yazım ve doğallık geçişinden **sonra** yapıldı
- [ ] İddialar cümle cümle çıkarıldı (espri içindeki örtük iddialar ve mutlak dil dahil)
- [ ] Her iddia kaynak metinden yeniden doğrulandı; hiçbir PMID/DOI hafızadan yazılmadı; güncellik ve geri çekilme kontrol edildi
- [ ] Çarpıtma kontrolü yapıldı: popülasyon, sonuç (oosit ≠ canlı doğum), payda, göreli/mutlak, kesinlik, nedensellik, aritmetik, birim, çeviri kayması
- [ ] Bağımsız alt ajan kullanıldı (kullanılamadıysa raporda yazıyor)
- [ ] Rapor `-sources.md` dosyasında; ❌, ❓ ve 🕒 kalmadı; düzeltilen cümleler yeniden doğrulandı
- [ ] "Hekim onayı gereken" maddeler Dr. Aksoy'a sunuldu; "klinik onaylı" etiketi yalnızca onun onayıyla

Espri testi (her espri için):
- [ ] Hedef hasta değil (beden, yaş, kaygı, bütçe, tedavi sonucu, kayıp); punchline kaybı **ima etmiyor**
- [ ] Din, cinsellik, argo, marka adı yok
- [ ] Aile/kültür esprisi varsa (2026-10-06'dan beri serbest): aile tipi genel kurulmuş; "ne zaman çocuk?" esprisinde hedef akraba ve espri empatiyle kapanıyor; başka toplumlar tek tip gösterilmemiş; ağır aile baskısı ve hassas konu yok
- [ ] Tek başına dinlenince yanlış tavsiye ya da alay gibi duyulmuyor
- [ ] Espri çıkarılınca bilgi eksiksiz kalıyor
- [ ] Acil durum/güvenlik cümleleri mizahsız

**Dil notu:** İngilizce kanal (@DrAksoyFertility) için ABD ve UK'ye ayrı sürüm yok; tek ortak İngilizce stil (`voice.md` → EN, `yt-script-en`).

## Süre kategorileri (5 kategori)

| Kod | Kategori | Hedef süre | Bağlam | Chapter |
|---|---|---|---|---|
| **K1** | Shorts | 20-180 sn (20-60 veya 60-180 alt tipi seç) | Tek soru-cevap veya tek kanıt/karar | 0 |
| **K2** | Konsept açıklayıcı | 6-10 dk başlangıç aralığı | "X nedir?" sade konu | 3+ ise faydalı |
| **K3** | Standart pillar (varsayılan) | 10-15 dk başlangıç aralığı | Derin kanıt + klinik karar + görüş | 3+ ise faydalı |
| **K4** | Uzun pillar / Live Q&A | 15-25 dk başlangıç aralığı | Çok yönlü, panel, abone Q&A | 3+ ise faydalı |
| **K5** | Konuk segmenti / podcast | 20-40 dk başlangıç aralığı | Uzman ile diyalog | 3+ ise faydalı |

**Kategori seçim ipucu:**
- ESHRE/NAMS pillar (DHEA, peptid eleştirisi vb.) → **K3** (varsayılan)
- "DHEA vajinal vs sistemik nedir?" tek-kavram → **K2**
- Q&A ya da panel → **K4**
- Pillar makaleden 20-180sn kompresyon → **K1** (konuya göre kısa veya extended alt tipi)
- Konuk uzman → **K5** (gelecek)

> Bu süreler yayın kapısı değil, ilk hipotezdir. Konunun ihtiyacı ve aynı formattaki kanal retention verisi daha önemlidir. Shorts için YouTube’un güncel kare/dikey 3 dakika sınırı ayrıca kontrol edilir.

## 0. Çekim öncesi video brief’i

- [ ] Hedef izleyici yazıldı: yeni / casual / regular / hasta yakını
- [ ] İzleyici niyeti yazıldı: arama / karar / mit kontrolü / destek
- [ ] Tek cümlelik izleyici vaadi ve videonun tek ana sonucu yazıldı
- [ ] YouTube Trends/Audience, yorumlar veya içerik boşluğu ile konu gerekçelendirildi
- [ ] En az 3 başlık ve 2 thumbnail vaadi taslağı hazırlandı
- [ ] Başlık + thumbnail + ilk 30 saniye aynı beklentiyi kuruyor

## Bölüm yapısı (K2-K4 ortak iskelet)

### 1. Hook — ilk saniyeler / ilk 30 saniye vaadi
İzleyiciyi yakalayan, konunun özünü veya şaşırtıcı bir gerçeği söyleyen cümle.

- ❌ Yanlış: "Merhaba, bugün konuşacağımız konu..."
- ✅ Doğru: Hook bankasından (`04-hooks-bank.md`) seçim
- ✅ Ton örneği: Gündelik bir internet/komşu/arama motoru gözlemi → net klinik soru

**Araştırmaya dayalı hook kontrolü (2026-10-06)**

> Master: `wiki/youtube/video-format.md` § "Araştırmaya dayalı hook ilkeleri" · Ayrıntı: `.claude/skills/yt-script-shared/HOOK.md`

- [ ] İlk cümle başlıktaki soruyu ya da vaadi tanınır kılıyor
- [ ] İlk 30 saniyede doğrulanmış bir ilk değer var (sayı, ayrım ya da kısa cevap)
- [ ] "Bu videoda…" planı 30. saniye civarında; kimlik hook'tan sonra ve kısa
- [ ] Tek ana soru açılıyor ve erken kapanıyor; karar ve güvenlik cevabı saklanmıyor
- [ ] Klikbeyt sözcüğü ("sır", "yasak", "şok") yok; korku açılışı yok; risk varsa çözüm aynı nefeste
- [ ] Sayılar doğal sıklıkla; başarı hikâyesi yanlılığı yok
- [ ] 2–3 açılış alternatifi ayrı blokta; hook türü rotasyonu kontrol edildi
- [ ] Shorts: metin, ses ve görsel aynı; sessizken anlaşılır; cevap Short'un içinde
- [ ] Yayın sonrası: Studio'daki Intro metriği (30. saniyede %) kanalın benzer uzunluktaki son 10 videosuyla karşılaştırıldı

**Kontrol:**
- [ ] İlk saniyelerde konu netleşti mi? (5 saniye katı kural değil)
- [ ] İlk 30 saniye başlık ve thumbnail vaadini karşılıyor mu?
- [ ] Şaşırtıcı tek istatistik veya iddia var mı?
- [ ] Anchor cümle hook'ta DEĞİL (Beat D kapanışında uygun) ✓

### 2. Bağlam — 15-60 saniye
- Problem çerçevesi
- Neden bu konu, neden şimdi
- TLDR: "Ne öğreneceksiniz?" (3 madde)

### 3. Ana içerik — 4 beat

> **2026-08-04 güncelleme:** Görsel değişiklik sabit 60–90 saniye kuralı değil; her görsel veya tonal seçim anlatılan bilgiyi açıklamalı, işaretlemeli ya da gereksiz bilişsel yükü azaltmalıdır. `[B-Roll / Tıbbi Şema / Ekranda Anahtar Kelime / Zoom-In]` yalnızca işlevi varsa kullanılır.
>
> İstatistikli IVF konularında per-cycle/per-transfer ayrımına ek olarak popülasyon, payda, mutlak oran, karşılaştırma grubu ve belirsizlik yazılır.

| Beat | Soru | İçerik | Tipik süre (K3) |
|---|---|---|---|
| **A. Konsept** | "X tam olarak ne?" | Terim + sade açıklama, mekanizma temeli, tek cümlelik ara özet | 1:00-3:00 |
| **B. Kanıt** | "Çalışmalar ne diyor?" | RCT, meta-analiz, kılavuz, GRADE; iddia–kaynak tablosu; payda, mutlak/göreli oran, belirsizlik | 3:00-6:00 |
| **C. Klinik karar** | "Kim için, kim için değil — pratikte nasıl?" | Endikasyon + kontrendikasyon + alternatif; kime uygun olmayabilir, kırmızı bayraklar, ne zaman hekime başvurmalı | 6:00-9:00 |
| **D. Dr. Aksoy yorumu** | "Klinik gözlemim..." | Kişisel perspektif; **kanıt vs görüş açık ayrım** | 9:00-10:30 |

#### Beat D ses ayrımı

> "Veriler şunu söylüyor. Benim klinik gözlemim, ki gerçek değil, şu..." formatı.

- Anchor cümle (#1 buzdolabı) burada uygun (kullanım kuralı: **4-5 videoda 1**)
- Aile üyesi metaforu (1 adet) Beat C-D köprüsünde veya Beat D kapanışında
- Hassas konularda (POI/RIF/donör/kanser FP) **metafor yok** — bkz. `01-voice-checklist.md`

#### İddia–kaynak ve güvenlik kaydı

Her klinik iddia için script dışında veya altında kısa bir kayıt tutulur: iddia, kaynak/PMID/DOI, popülasyon, karşılaştırma, sonuç, belirsizlik, sınırlılık, kılavuz tarihi ve videoda kullanıldığı cümle. Kaynaklar açıklamada izlenebilir biçimde tekrarlanır.

### 4. CTA + disclaimer + Next Video Bridge — 1 dakika

- **Next Video Bridge (Sonraki Video Köprüsü — 2026 Oturum Katkısı Standardı):** Videoyu "Abone olun" diyerek kapatmayın (drop-off yaratır). İzleyiciyi konuyla doğrudan ilişkili bir sonraki videoya yönlendirin (ör. *"Eğer 40 yaş üstü yumurta kalitesini artıran takviyelerin kanıtsal analizini merak ediyorsanız, ekrandaki şu videoma tıklayarak devam edin"*).
- Nötr CTA: "Detay için tupbebek.com" / "Plus d'infos sur draksoyivf.com" — UTM linkli
- "Genel sorular için yorum" — kişisel test sonucu, telefon veya kimlik bilgisi paylaşılmaması gerektiği belirtilir
- Disclaimer (on-screen + sesli) — **içerik tipine göre seç** (5 alternatif TR + 5 FR, bkz. [[wiki/brand/voice]] §"Disclaimer cümle bankası"):
  - **Standart:** "Bu içerik bilgilendirme amaçlıdır; bireysel tıbbi değerlendirmenin yerini almaz." / "Ce contenu est informatif. Il ne remplace pas une évaluation médicale individuelle."
  - **Hassas konu** (POI/POF/RIF/kayıp/kanser FP): "Bu video belirli bir tanı için bireysel öneri içermez. Durumunuzu hekiminizle değerlendirmeniz, ileriye dair en sağlıklı adımdır."
  - **IVF prognoz / başarı oranı:** "Klinik çalışmalardaki ortalama oranlar paylaşıldı; sizin bireysel sonucunuz yaş, sebep, kümülatif siklus dahil çok değişkene bağlıdır."
  - **Onaysız ürün eleştirisi:** "Bu içerik bilimsel kanıt durumunu özetler; klinik kullanım onayı olmayan ürünler için tedavi önerisi içermez."
  - **Davranışsal/yaşam tarzı:** "Bu yöntemler kanıt-temelli olsa da bireysel uygulama için ehil uzman desteği önerilir."
- "Daha fazla kaynak için açıklamada / sabitlenmiş yorumda" — nötr

#### ⛔ Yasak kapanış kontrolü

CTRL+F + içerik tarama:
- "Bana ulaşabilirsiniz / Contactez-moi" → F1+F11 → kullanma
- "Bizim klinikte / Dans notre clinique" → F11+F15 → kullanma
- "Sonuçlarımız başarılı / Nos résultats" → F1+F8+F10 → kullanma
- "İndirim / Forfait / Promotion" → F5 → kullanma
- "En iyi / Le meilleur" → F10 → kullanma
- "Garantili sonuç / Résultat garanti" → F1+F8 → kullanma
- "Hastalarıma X markasını öneririm / Je prescris X" → F11+F15 → kullanma
- "Şahsen ben uyguluyorum / Personnellement j'utilise" → F1+F11+F15 → kullanma

Tam yasak kapanış bankası + güvenli alternatifler: [[wiki/brand/voice]] §"Yasak kapanış bankası".

### Gövde ve kapanış kontrolü (2026-10-06)

> Master: `wiki/youtube/video-format.md` § "Araştırmaya dayalı gövde ve kapanış ilkeleri" · Ayrıntı: `.claude/skills/yt-script-shared/STRUCTURE.md`

- [ ] 3–5 ana mesaj; 2–4 anahtar terim erken ve sade tanıtıldı
- [ ] Bölümler 2–4 dk; her biri hasta sorusuyla açılıyor, ara özetle kapanıyor; geçişler "ama / bu yüzden"
- [ ] En pratik cevap ilk yarıda; 2–3 durup düşünme sorusu soruluyor ve cevaplanıyor
- [ ] Sayılar mutlak ve sabit paydalı; fayda ve zarar yan yana; belirsizlik sayısal
- [ ] Sayı bütçesi (2026-10-06): bölüm başına tek yıldız sayı (≤2–3 sesli sayı); tek format "10 kadından X"; önce anlam; çalışma büyüklüğü, yıl ve aralıklar ekranda; tek ana tablo; yıldız sayıdan önce tahmin sorusu; yuvarlama abartısız ve doğrulandı
- [ ] Hikâye varsayımsal ve genel oranla birlikte; her espri kavrama hizmet ediyor
- [ ] Kapanış: cevap → tek akılda kalacak cümle → doktora 2–3 soru → güvenlik cümlesi → tek sonraki video → dur
- [ ] Kapanışa yeni bilgi veya espri eklenmedi; "bugünlük bu kadar" yok
- [ ] Bitiş ekranı için son 5–20 sn boş; önemli görsel altında kalmıyor
- [ ] Shorts: değerden sonra duruluyor; ilgili video bağlı; uzun videonun ilk 5–10 sn'si Short'un sorusunu karşılıyor

### 5. End screen — son 20 saniye

- 1 ilgili video önerisi (Next Video Bridge ile eşleşen)
- Abone butonu
- Playlist önerisi (varsa)

### 6. Description metni

> **Tam description kütüphanesi:** [07-description-library.md](07-description-library.md) — K1-K5 iskeletleri (TR + FR), 4 konu tipi modifikasyonu (kavram açıklayıcı / pazarlama eleştirisi / kılavuz değerlendirme / hassas konu), hashtag bankası, UTM konvansiyonu, disclaimer eşleme tablosu, About blok, sabitlenmiş yorum şablonu, mevcut video backfill stratejisi.

Hızlı iskelet (K3 standart pillar; teslimde düz metne dönüştürülür):

```
[Snippet — ilk 150 karakter, anahtar kelime + yıl + vaat]

📌 Detaylı yazı: https://[domain]/[slug]?utm_source=youtube&utm_medium=description&utm_campaign=[pack-id]

⏱ İçindekiler (gerekiyorsa; `00:00` + en az 3 bölüm + bölüm başına 10 sn)
00:00 Hook
00:45 Bağlam
02:00 [Beat A]
05:00 [Beat B]
08:30 [Beat C]
11:00 [Beat D]

📚 Kaynaklar (izlenebilir referanslar: tam başlık + yıl + PMID/DOI/link)
ℹ️ Hakkında (07-library §"About blok" — sabit metin)
⚠️ [Disclaimer — konu tipine göre, 07-library §"Disclaimer eşleme tablosu"]

[Yalnızca alakalı hashtag'ler; opsiyonel]
```

### 7. Sabitlenmiş yorum

- Yanıt vaadi: "Genel sorularınızı yazabilirsiniz; kişisel test sonucu veya kimlik bilgisi paylaşmayın."
- Kanıt referansı: "ESHRE 2023 / NAMS 2023 / NICE NG23" — hangisi geçerliyse
- Kaynak: "Yazılı kaynak için tupbebek.com / draksoyivf.com"
- Disclaimer hatırlatma satırı (ilk kelimelerde `ℹ️ [Tıbbi Tavsiye Değildir | Bilgilendirme Amaçlıdır]` ibaresi — YT AI Topic Summaries uyumu)

### 8. Provenance, disclosure ve erişilebilirlik

- [ ] B-roll, grafik, müzik, fotoğraf ve ekran görüntülerinin kullanım hakkı/atfı kaydı var
- [ ] Hasta/konuk görseli veya hikâyesi için açık rıza ve kimlik gizleme kontrol edildi
- [ ] Sponsor, ücretsiz ürün, affiliate veya ticari ilişki varsa scriptte ve Studio’da disclosure alanı işaretlendi
- [ ] Gerçekçi sentetik/altered medya varsa YouTube Studio disclosure kararı kaydedildi
- [ ] Altyazı, grafik metni, telaffuz ve TR/FR/EN/AR yerelleştirmesi kontrol edildi
- [ ] On-screen metin konuşmayı tekrar etmek yerine onu işaretliyor veya açıklıyor

## Thumbnail brief checklist

- [ ] **Yasak:** ürün ambalajı, ilaç kutusu, kapsül yığını
- [ ] **Yasak:** "şaşkın yüz / büyük oklar / kırmızı çapraz" influencer estetiği
- [ ] **Yasak:** "before-after" kombinasyonu
- [ ] **Yasak:** lab/laboratuvar görseli (Estranova editorial _index uyumu)
- [ ] **Önerilen:** sade kompozisyon, marka paleti
- [ ] **Önerilen:** Dr. Aksoy nötr profil (yüz seçilirse)
- [ ] **Önerilen:** soru işareti / minimal şematik (organ, takvim, terazi, vb.)
- [ ] [[wiki/youtube/thumbnail-rules]] full liste için

## Kontrol — script tamamlandığında

### Format
- [ ] Süre kategorisi seçildi (K1-K5)
- [ ] Hedef süre içerik ihtiyacına ve benzer format retention verisine göre gerekçelendirildi
- [ ] Seçilen modül yapısı izleyici vaadini karşılıyor; 4 beat ve Beat D gerektiğinde kullanıldı
- [ ] Beat D (Dr. Aksoy yorumu) klinik gözlem + kanıt ayrımı net
- [ ] Her görsel/reji notunun bilgi taşıyan bir işlevi var
- [ ] İstatistikte payda, mutlak/göreli oran, belirsizlik ve gerekiyorsa per-cycle/per-transfer ayrımı var
- [ ] Her klinik iddia claim ledger’daki kaynakla eşleşiyor
- [ ] “Kim için değil / ne zaman hekime başvurmalı?” bölümü uygun
- [ ] CTA Next Video Bridge formatında (sonraki ilgili videoya yönlendirme)
- [ ] Disclaimer sesli + on-screen + description
- [ ] Chapter varsa `00:00` ile başlıyor, en az 3 sıralı timestamp ve her bölüm en az 10 saniye

### Ses (`01-voice-checklist.md` ile çapraz)
- [ ] Anchor son 4 videoda kullanıldı mı? Kullanılmadıysa burada uygun
- [ ] Aile üyesi 1 adet maksimum
- [ ] Tema-eşleşme uygun
- [ ] Hassas konu ise metafor yok

### Uyumluluk (`02-compliance-checklist.md` ile çapraz)
- [ ] CTRL+F: "garanti" / "mucize" / "tedavi eder" → 0 eşleşme
- [ ] Marka adı / belirli klinik adı → 0 eşleşme
- [ ] "%" geçtiği yerde "ortalama" / "değişir" eklendi
- [ ] Hasta öyküsü kimliklendirme yok

### Description + Sabitlenmiş yorum
- [ ] UTM linki var (campaign ID dahil)
- [ ] İçindekiler timestamp tam
- [ ] Yalnızca alakalı hashtag'ler seçildi; sabit sayı veya `#healthinfo` zorunluluğu yok
- [ ] Sabitlenmiş yorum başında AI uyumlu disclaimer ibaresi

### Thumbnail
- [ ] Yasak öğe yok
- [ ] Marka paleti
- [ ] Tıklanabilir + sade

### Yayın sonrası hipotez

- [ ] Başlık/thumbnail hipotezi yazıldı; test sonucu yalnızca CTR değil watch-time share ve retention ile okunacak

### Düz metin son kontrolü

- [ ] Son çıktı, başlık ve kontrol notları çıkarıldığında tek parça konuşma metni olarak okunabiliyor
- [ ] Mizah cümlesi ana tıbbi mesajı gölgelemiyor
- [ ] Hiçbir espri hastanın yaşı, kaybı, bedeni, bütçesi veya başarısız tedavisi üzerinden kurulmadı; hiçbir punchline kaybı ima etmiyor
- [ ] Varsa baba esprisi tek; sahneler somut ve kısa
- [ ] Benzetme ile teknik gerçek birbirine karıştırılmadı
- [ ] Son paragraf umut veriyor ama garanti veya kişisel sonuç vaadi vermiyor

## Shorts türeme (2026 Revizyonu)

Her 8-12 dk video → konuya göre 1-3 Short (20-180 sn) türeyebilir.

**Türetme şablonu:**

1. **Hook + Tek soru + Cevap + Related Video CTA**; süreyi 20-60 veya 60-180 sn alt tipine göre seç
2. Hook = ana videodaki güçlü cümle (anchor değil — Shorts'ta anchor sığ kalır)
3. Cevap = ana videonun 1 beat'i (genellikle Beat B = kanıt)
4. **CTA:** Shorts açıklaması ve yorumundaki URL’ler tıklanabilir değildir; ana videoyu YouTube Studio’da **"İlişkili Video (Related Video)"** olarak ekle.
5. Sesli/Görsel Yönlendirme: *"Bu konunun tüm bilimsel detaylarını izlemek için ekrandaki ilişkili videoya tıklayın."*

## Cross-reference policy

`wiki/youtube/cross-reference-policy.md` uyumlu:

- Description CTA → tek domain (TR kanal: tupbebek.com; FR kanal: draksoyivf.com)
- Sabitlenmiş yorum → kanıt kaynağı + ek ilgili video link
- "Senaiaksoy.net" YouTube içeriklerinde **referans verilmez** (statik kimlik sitesi politikası)
- Estranova kanalı kurulduğunda menopoz videoları → estranova.com (mevcut IVF kanallarından menopoz videosu yapılmaz, bkz. site-kanal mimarisi kararı)
