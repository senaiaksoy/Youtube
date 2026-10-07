# YT Script — Ortak Çekirdek (tüm dil skill'leri bunu okur)

Bu dosya `yt-script-tr`, `yt-script-fr` ve `yt-script-en` skill'lerinin ortak kuralıdır. Kendi başına skill değildir.

---

## 1. Yetki sırası (çelişkide üstteki kazanır)

1. Kullanıcının o videoya dair güncel talimatı. Hassasiyet sınırları her zaman en dar olan haliyle korunur.
2. **Onaylı persona** (15 Eylül 2026; "komik abi/baba" katmanıyla 6 Ekim 2026'da genişletildi, Codex skill v2.1.0):
   `C:\Users\KC3\.codex\skills\youtube-script-senai-aksoy\references\senai-aksoy-persona.md`
3. Yerel kontrol listeleri: `D:\A-klasör\Youtube\youtube-content\`
   - `00-INDEX.md`: konu tipi, metafor ve hassasiyet eşlemesi
   - `01-voice-checklist.md`: metafor ailesi, en fazla 1 metafor kuralı, mizah yasak temalar
   - `02-compliance-checklist.md`: TR ve FR ifade taraması (hukuki referanslar arama ipucudur; güncel kural yayından önce doğrulanır)
   - `03-script-format-checklist.md`: K1–K5 süre, 4 beat, düz metin teslimi
4. Bu çekirdek ve dil skill'inin ses katmanı.
5. Araştırma arka planı (komedyen referansları, kaynaklar):
   `D:\A-klasör\Youtube\cem-yilmaz-tarzi-script-rehberi.md`
   `D:\A-klasör\Youtube\script-ses-rehberi-FR-US-UK.md`

Persona veya yerel dosyalar okunamazsa: bilinen kurallarla devam et, eksik olanı açıkça söyle. İçeriklerini uydurma.

---

## 2. Persona: "İşini çok iyi bilen, komik, içimizden biri"

Onaylı persona sakin, sıcak, gözlemci bir hekim sesidir. 6 Ekim 2026'da persona dosyasına bir katman eklendi ("İşini bilen komik abi/baba katmanı"): abi/baba sıcaklığı ve izleyicinin **gözünde canlanan** sahneler. Kanonik metin persona dosyasındadır; özeti:

- **Sahne kurma:** Genel ifade yerine somut an. "Endişelenirsiniz" yerine "gece ikide, telefon elinizde, eşiniz uyuyor".
- **İç ses:** İzleyicinin kafasından geçeni kısa bir cümleyle seslendirmek ("Bu ne? Bu bir işaret mi?"). Bu, kişiyi değil, herkesin yaptığı insani bir davranışı gösterir. Hemen ardından bu davranışı normalleştir.
- **Kendine dönük sıcaklık:** Doktorun kendi meslek alışkanlıklarıyla hafifçe dalga geçmesi. Kişisel olay, hasta hikâyesi veya klinik deneyim **uydurulmaz**. Genel ve doğrulanabilir alışkanlıklar kullanılır (ör. doktorların ultrason ekranına bakarken sessizleşmesi).
- **Baba esprisi ve kendini yakalama:** Bilerek hafif bir kelime oyunu yapıp kendin fark etmek. Videoda en fazla bir kez. Kalıbı dil skill'inde.
- **Callback:** Baştaki sahneye sonda gerçekten yeni bir anlam katarak dönmek.

Değişmeyenler: espri kotası yok, bağıran veya alkış bekleyen ton yok, gerçek bir komedyenin personası, imza sözleri veya bilinen esprileri taklit edilmez, komedyen adı scriptte geçmez.

**Sohbet havasında stand-up (kullanıcı onayı, 2026-10-06):** Videolar ders gibi değil, sahnesi olan bir sohbet gibi duyulur. Bağıran, gösterişli ya da alkış bekleyen ton hâlâ yok.
- **Açılış:** Konu hassas değilse bir sahneyle açılır (kişisel an, aile tipi, Dr. Google, gündelik durum). Başlığın sorusu en geç ~10. saniyede tanınır; doğrulanmış ilk değer ~30. saniye civarında gelir.
- **Gövde:** Her bölüm başında bir küçük sahne (bit) olur: kurulum, büyüme, punch, ardından bilgiye dönüş. Bölüm başına en fazla bir sahne ve bir tek satırlık espri.
- **Sahnenin işi:** Sahne kavrama ya da bölüm geçişine hizmet eder. Örnek: eleme basamaklarını yetenek yarışması turları gibi anlatmak.
- **Tekrar eden karakter:** Her şeyi bilen amca, Dr. Google ve benzerleri kullanılabilir. Sonda 1–2 geri dönüş (callback) yapılır.
- **Doktorun kendisi:** Dr. Aksoy'un kendi onayladığı gerçek kişisel anlar kullanılabilir (ör. "akşam yemeğinde 'kaç yumurta dondurmalıyım?' sorusu"). Uydurma anı yasağı sürer.
- **Sayı yoğunluğu:** Uzun tablolar okunmaz, ekrana taşınır ("tabloyu size okumayacağım, ekranda"). Söze yalnızca anlamı ve gerekli çekinceler girer.
- **Ciddi yerler:** Yaşa bağlı düşük sayılar, risk ve güvenlik cümleleri mizahsız kalır. Geçiş açıkça yapılır ("Şimdi işin ciddi kısmı").
- **Dublaj:** Komik zamanlama dublajda düzleşebilir. Esprileri kısa cümlelerle kur ve Fransızca kayıtta duraklamaları gerçekten bırak. Önemli videolarda ilk 30 saniyenin Dr. Aksoy tarafından İngilizce kaydedilmesi değerlendirilir.

---

## 3. İş akışı

### Adım 1 — Brief
İzleyicinin ana sorusu, tek cümlelik çıkarım, kanal ve dil, format (03'teki K1–K5), yaklaşık süre, tedavi aşaması. Bağlamdan çıkarılabilenleri çıkar. Yalnızca sonucu gerçekten değiştirecek eksik bilgiyi sor.

### Adım 2 — Hassasiyet kapısı
Konuyu `00-INDEX.md` tablosunda ve `01-voice-checklist.md` "Anti-pattern" listesinde bul.
- **Mizah yasak konular:** gebelik kaybı, tekrarlayan kayıp, POI/POF, donör kararı, kanser sonrası fertilite, ileri yaşta düşük şans, kötü genetik sonuç, azoospermi tanısı, ciddi kötü haber; ayrıca Afrika frankofon IVF stigması ve Mağrip'te donasyon/cinsiyet seçimi.
- Bu konularda espri, komik benzetme ve sahne mizahı **kapalıdır**. Sade, doğrudan, empatik dil kullanılır ve `01`'deki hassas kapanış bankası uygulanır. Dil skill'i yalnızca dil ve kültür uyarlaması için kullanılır.
- **Acil durum ve güvenlik bilgisi** (kırmızı bayrak belirtiler, ne zaman acile gidilir) her videoda mizahsız ve net yazılır.

### Adım 3 — İddia kaydı (konuşmadan önce)
Her klinik iddia için şunları kaydet: iddia, kaynak (PMID/DOI/kılavuz ve tarihi), popülasyon, sonuç, payda, mutlak/göreli oran, belirsizlik ve videoda kullanılan cümle. Kaynak bulmak için PubMed MCP araçlarını ve Obsidian master kılavuz dosyalarını (`00-INDEX.md` "Master vault referansları") kullan. Ayrıntılı kural: `...\youtube-script-senai-aksoy\references\medical-evidence.md`.

Kaynaksız kesin iddia yazılmaz. Mizahi abartı (ör. "dört yüz yıl gibi gelen on gün") bulgu gibi sunulmaz.

### Adım 4 — Malzeme avı ve tekrar kontrolü
- Aynı dildeki son 3 scripti tara (`youtube-content\video-script-*-<dil>-*.txt`). Kullanılmış motifleri (hesap makinesi, sözleşme, internet kesinliği, forum vb.) aynı biçimde tekrarlama.
- **İmza kalıplar da bu taramaya girer (2026-10-06):** baba esprisinden sonraki kendini yakalama cümlesi, Beat D'deki görüş girişi ("bu benim klinik görüşüm…") ve ciddiyete dönüş cümlesi. Son 3 scriptte kullanılmış bir varyant aynı biçimde tekrar kullanılmaz; dil skill'indeki bankadan başka biri seçilir ya da yeni kurulur. Espriyi adıyla anan varyant ("baba esprisi", *blague Carambar*, *dad joke*) en fazla 3–4 videoda bir kullanılır. Ders: "Oui, c'était une blague Carambar" ve "this is my clinical view, not a study result" how-many-eggs ve EP01 supplements scriptlerinde birebir tekrar etti.
  - EN videoların FR kayıt metinleri (`video-script-*-en-*-fr-recording.txt`) Fransızca tarama kapsamına girer; izleyici o cümleyi dublajda duymasa da Dr. Aksoy kayıtta söyler.
- `06-anchor-rotation-tracker.md` dosyasında son anchor ve metafor kullanımına bak.
- Konunun içinde gerçek bir gözlem ara: bekleme süreleri, sayılara takılmak, internetteki kesinlik, pazarlama dili, bürokrasi, laboratuvar ve portal deneyimi, doktorların kendi alışkanlıkları.
- Doğal bir gözlem yoksa espri ekleme. Bilgi yoğun bir video sesi tek başına taşıyabilir.

### Adım 5 — Bit testi (her espri için)
1. Hedef ne? Durum, internet, pazarlama, sistem veya doktorun kendisi olmalı. Hastanın bedeni, yaşı, kaygısı, bilgisizliği, bütçesi, tedavi sonucu, kimliği veya kaybı **asla** hedef olmaz.
2. Bu satır tek başına dinlenince yanlış bir tavsiye ya da alay gibi duyuluyor mu? Duyuluyorsa yeniden kur.
3. Espri bilgiyi açıklıyor ya da akılda tutturuyor mu? Yoksa çıkar.
4. Espriyi silince bilgi hâlâ eksiksiz mi? Değilse bilgi esprinin içine gömülmüş demektir; ayır.
5. Punchline ima yoluyla bir kayba, kötü sonuca veya utanca mı dayanıyor? (Ör. "…ve sonra bir daha hiç yazmadı" kaybı ima eder.) Öyleyse at.
6. Din, cinsellik, argo veya marka adı içeriyor mu? İçeriyorsa at.
7. Aile ya da kültür esprisi mi? Aşağıdaki kurala uyuyor mu?

**Aile ve kültür mizahı (2026-10-06'da gevşetildi):**
- ✅ **Aile tipleri** (Cem Yılmaz tarzı): "her şeyi bilen kayın", abi, baba, teyze gibi herkesin tanıdığı tipler. Genel tip olarak kurulur ("hani her ailede bir kayın vardır"). Dr. Aksoy'un gerçek akrabası hakkında olay uydurulmaz.
- ✅ **"Ne zaman çocuk?" sorusu:** Hedef, soruyu soran akrabanın davranışıdır; hasta değil. Espri bir empati cümlesiyle kapanır ("Bu soruyu duyan tek kişi siz değilsiniz. Cevabını da kimseye borçlu değilsiniz.").
- ✅ **Kendi kültürüyle şakalaşma** (Türk aile hayatı) ve evrensel aile sahneleri.
- ⚠️ **Başka toplumlar hakkında klişe** (özellikle Mağrip ve Sahra altı Afrika): Dışarıdan bir hekimin ağzında aşağılayıcı duyulabilir. Tek tip genelleme yapılmaz; şüphede çıkarılır.
- ❌ **Kesin yasaklar:** din; ağır aile baskısı (boşanma tehdidi, kısırlığın kadına yüklenmesi, "kusur kimde" söylemi); kayıp, RIF, POI ve kötü prognoz gibi hassas konularda aile esprisi; konusu aile baskısının kendisi olan videolarda mizah.

### Adım 6 — Yazım
**Giriş (hook):** `HOOK.md` uygulanır. Özet:
- İlk cümle başlığın sorusunu tanınır kılar.
- İlk 30 saniyede doğrulanmış bir ilk değer verilir.
- Plan cümlesi 30. saniye civarında söylenir; kimlik hook'tan sonra ve kısa tutulur.
- Tek ana soru açılır ve erken kapatılır.
- Klikbeyt, korku ve vaat yoktur.
- 2–3 açılış alternatifi ayrı blokta verilir.

**Gövde ve kapanış:** `STRUCTURE.md` uygulanır. Özet:
- 3–5 ana mesaj; 2–4 anahtar terim erken tanıtılır.
- Bölümler 2–4 dakika; her biri bir hasta sorusuyla açılır ve tek cümlelik ara özetle kapanır; geçişler "ama / bu yüzden".
- En pratik cevap ilk yarıda; 2–3 gerçek "durup düşünme" sorusu sorulur ve cevaplanır.
- Sayılar mutlak ve sabit paydalı; fayda ve zarar yan yana.
- **Sayı bütçesi:** bölüm başına tek yıldız sayı (≤2–3 sesli sayı); tek format "10 kadından X"; önce anlam; karar değiştirmeyen sayılar ekrana; tek ana tablo; yıldız sayıdan önce tahmin sorusu. Ayrıntı: `STRUCTURE.md` ilke 8.
- Kapanış sırası: cevap → tek cümlelik akılda kalacak mesaj → doktora sorulacak 2–3 soru → güvenlik cümlesi → bitiş ekranı üstünde tek bir sonraki video → dur. "Bugünlük bu kadar" yok.

Bit anatomisi (esnek, her bitte hepsi gerekmez):

```
ZEMİN      herkesin tanıdığı durum (1 cümle)
DETAY      küçük, spesifik, yaşanmış an
SAHNE      iç ses / somut nesne / saat ve yer
TIRMANMA   1–2 basamak, gerçekçi abartı
DÖNÜŞ      sakin bir cümlenin sonunda küçük ters köşe
KÖPRÜ      en geç 1–2 cümle içinde klinik bilgiye geçiş
CALLBACK   (opsiyonel) sonda gerçekten yeni anlam katan geri dönüş
```

Sahne kurma teknikleri:
1. **Somut nesne ver** ("buzdolabında yoğurdun yanında duran iğne kalemleri").
2. **Saat ve yer ver** ("gece ikide, mutfak ışığı açık").
3. **Kısa iç ses** (en fazla 1 cümle).
4. **Kişileştir** (embriyo, folikül, test sonucu konuşabilir). Ama biyolojik olarak yanlış bir çıkarıma yol açmamalı.
5. **Aşırı kesin gündelik abartı** ("yaklaşık dört yüz yıl"). Araştırma bulgusu gibi sunulmaz.
6. **Kısa sus:** Düz metinde kısa cümle ve paragraf kırılmasıyla verilir. Açık sus, SFX veya canlandırma notu varsa REJİ NOTLARI'na yazılır.
7. **Açıklayan benzetme (Cem Yılmaz tarzı, 2026-10-06):** Soyut bir kavramı (olasılık, eleme basamakları, zaman) izleyicinin gözünde beliren tek bir gündelik sahneye çevirir. Örnek: "Yumurta dondurmak fotoğraf çekmeye benzer, zaman makinesi almaya değil."
   - **Test:** Benzetme çıkarılınca izleyici daha az mı anlıyor? Anlamıyorsa kalır; fark yoksa çıkarılır (süs benzetme, öğrenmeyi bozan "ilginç ayrıntı" sayılır).
   - **Sayı ve yer:** Videoda 1–2 tane, kavramın ilk anlatıldığı yerde. Bunlar eklenince diğer küçük imgeler sadeleştirilir. Kapanışta yeni benzetme olmaz; yalnızca geri dönüş (callback) yapılabilir.
   - **Sınır:** Yanlış bir biyolojik çıkarıma yol açabilecekse sınırı bir cümleyle söylenir.
   - **Doğrulama:** İçindeki örtük bilgi `yt-script-factcheck`'ten geçer.
   - **Dil:** Her dilde yeniden kurulur; kelime kelime çevrilmez.
   - **Hassasiyet:** Hassas bölümlerde (kayıp, ileri yaşta düşük şans, kötü haber) kullanılmaz.
   - **İmza metaforla ilişki:** İmza metafor ailesindeki (buzdolabı vb.) "videoda en fazla 1" kuralı bundan ayrıdır. İkisi aynı videoda olabilir. Görüntü dozu stand-up kuralına bağlıdır: bölüm başına en fazla bir sahne ve bir tek satırlık espri; açıklayan benzetme videoda en fazla 2.

Teknik terim ilk geçtiğinde konuşma içinde sadeleştirilir. Benzetmenin sınırı gerekiyorsa söylenir.

Taslak bitince **§6 Konuşma doğallığı** geçişi yapılır: metin yazı dili gibi duyulan yerlerde konuşma diline çevrilir.

### Adım 7 — Teslim biçimi
> Teslimden önce **Adım 9 (bilimsel doğrulama)** tamamlanır. Doğrulamadan geçmemiş script "taslak" olarak teslim edilir ve bu açıkça söylenir.

- **Konuşma gövdesi:** Düz metin paragraflar. İçinde başlık, liste, zaman kodu, köşeli parantezli reji, kaynak numarası ve emoji bulunmaz.
- Gövdeden ayrı verilenler:
  - **AÇILIŞ ALTERNATİFLERİ** (en fazla 3, yeni tam scriptte)
  - **REJİ NOTLARI** (sus, SFX, canlandırma, ekran metni; hangi cümleye ait olduğu tırnakla belirtilir)
  - **İDDİA KAYDI / KAYNAKLAR** (sidecar)
  - **DURUM:** taslak / kaynak kontrollü / klinik onaylı / anadil kontrollü / sesli okundu. Yalnızca gerçekten yapılmış olanı yaz.
- Dosya istenirse mevcut düzeni izle:
  - `D:\A-klasör\Youtube\youtube-content\video-script-<slug>-<dil>-<YYYY-MM-DD>.txt` (yalnızca gövde)
  - `...-<YYYY-MM-DD>-sources.md` (iddia kaydı, açılış alternatifleri, reji notları, durum)
  - Dil kodları: `tr`, `fr`, `en` (İngilizce tek ortak sürüm; ABD ve UK için ayrı script yok)
- **Süre tahmini:** Yalnızca gövde sayılır.
  `python C:\Users\KC3\.codex\skills\youtube-script-senai-aksoy\scripts\script_timing.py <gövde.txt> --wpm-low 130 --wpm-high 150`
  Bu bir tahmindir; gerçek süre sesli okumayla doğrulanır.

### Adım 8 — Son kontrol
- `02-compliance-checklist.md` hızlı taraması (garanti, mucize, "tedavi eder", marka/klinik adı, hasta öyküsü, fiyat, "kullanıyorum").
- `03` sonundaki "Düz metin son kontrolü".
- Mizah tıbbi mesajı gölgeliyor mu? Acil bilgi mizahsız mı? Son paragraf umut veriyor ama garanti vermiyor mu?
- Persona son okuması: ses doğal mı, benzetme doğru mu, callback gerçekten kurulmuş mu? İşlevsiz espri ve dolgu cümleleri çıkarılır.
- §6 doğallık kontrolü: sesli okununca konuşma gibi mi? Ünlemler ve belirleyiciler tik'e dönüşmüş mü?

### Adım 9 — Bilimsel doğrulama (zorunlu, yazım ve doğallık geçişinden sonra)
- `D:\A-klasör\Youtube\.claude\skills\yt-script-factcheck\SKILL.md` uygulanır:
  - iddialar cümle cümle çıkarılır (espri içindeki örtük iddialar dahil),
  - kaynak metinden doğrulanır,
  - bağımsız bir alt ajan ikinci kez kontrol eder,
  - çarpıtma kontrolü yapılır (popülasyon, sonuç, payda, kesinlik, güncellik, çeviri),
  - rapor `-sources.md` dosyasına yazılır.
- ❌, ❓ veya 🕒 iddia kalırken script "kaynak kontrollü" sayılmaz. Düzeltilen cümleler yeniden doğrulanır.
- "Klinik onaylı" etiketini yalnızca Dr. Aksoy verir. Rapordaki "hekim onayı gereken" maddeler ona sunulur.

---

## 4. Yetki sınırları
- Yazmak yayınlama, YouTube Studio değişikliği, yükleme veya commit yetkisi vermez.
- FR metinler yayından önce Dr. Aksoy'a gösterilir.
- Site metni için `humanize` yalnızca kullanıcı isterse uygulanır (`C:\Users\KC3\.codex\skills\senai-humanize\SKILL.md`).
- Yerel kontrol dosyaları bu skill kullanılırken değiştirilmez.

---

## 5. Yerelleştirilmiş acil durum cümlesi
Güvenlik cümlesi her dilde mizahsız yazılır ve yerel acil numarasıyla verilir:
- TR: 112
- FR (Fransa): 15 (SAMU) veya 112. Frankofon kitle karışık olduğu için "le numéro d'urgence de votre pays" eklenir.
- EN (ABD + UK ortak sürüm): "call your local emergency number — 911 in the US, 999 in the UK"

---

## 6. Konuşma doğallığı (kulak için yazım)

Script okunmak için değil, **söylenmek** için yazılır. İzleyici metni gözüyle değil kulağıyla alır. Hedef: Dr. Aksoy kameraya bakıp anlatırken metin "okuyor" gibi değil "konuşuyor" gibi duyulsun. Dile özgü hazır listeler her dil skill'inin "Konuşma doğallığı bankası" bölümündedir.

### 6.1 Öğeler

| # | Öğe | Ne işe yarar | Örnek (TR) |
|---|---|---|---|
| 1 | **Ünlem** | Şaşkınlık, fark etme, empati, hafif sitem | "Aa!", "Of…", "Hah!" |
| 2 | **Söylem belirleyici** | Geçiş, dikkat çekme, toparlama | "Bakın,", "Şimdi…", "Neyse,", "Gelelim asıl meseleye." |
| 3 | **İzleyiciye kısa soru** | Muhatap alma, onay | "değil mi?", "Tanıdık geldi mi?" |
| 4 | **Soru-cevap** | Merakı canlı tutar | "Kötü bir şey mi? Değil." |
| 5 | **Kendini düzeltme** | Düşünerek konuşma hissi | "Aslında… hayır, şöyle diyeyim:" |
| 6 | **Vurgu için tekrar** | Ağırlık verir | "On gün. On. Gün." / "Çok, çok önemli." |
| 7 | **Yarım cümle** | Doğal ritim | "Peki sonuç? Belirsiz." |
| 8 | **Yansıtılmış iç konuşma** | Sahneyi canlandırır | "'Ya olmadıysa?' diyorsunuz kendi kendinize." |
| 9 | **Ses yansımalı kelime** | Görüntü ve hız katar | "telefon dıt dıt", "pat diye" |
| 10 | **Gösterme + betimleme** | Ekranla bağ kurar | "Şu çizgiye bakın: yukarı çıkıyor ama yavaş." (Görsel, sesle de anlatılır; erişilebilirlik) |
| 11 | **Doğrudan hitap ve "biz"** | Yakınlık | "Gelin birlikte bakalım", "biz doktorlar…" |

### 6.2 Ölçü (kota değil, üst sınır)
- **Anlam taşımalı:** Her ünlem veya belirleyici bir duyguyu ya da geçişi taşır. Çıkarılınca hiçbir şey kaybolmuyorsa dolgudur; çıkarılır.
- **Ünlem:** Paragraf başına en fazla 1. Aynı ünlem videoda en fazla 2 kez.
- **Belirleyici:** Ardışık iki paragraf aynı belirleyiciyle başlamaz ("Bakın… Bakın…" olmaz).
- **İzleyiciye soru:** Tik olmaması için 1 dakikada en fazla 1–2.
- **Üç nokta:** Yalnızca gerçek duraksama için; paragrafta en fazla 1.
- **Ünlem işareti:** Tek "!". "!!!" yalnızca ekranda gösterilen forum alıntısında.
- **Yazılmayacaklar:** Duraksama sesleri ("eee", "ııı", "euh", "um"). Bunlar kayıtta doğal olarak çıkar, yazılmaz.
- **Yasak ünlemler:** Dini çağrışımlı olanlar ("Allah Allah", "Maşallah", "Vallahi", « Mon Dieu », "Oh my God", "Jesus"), argo, kaba sözcükler.
- **Hassas konu ve acil cümlesi:** Komik ünlem, iç ses ve ses yansımalı kelime yok. Yalnızca yumuşak belirleyiciler kullanılır ("Bakın,", "Şunu bilmenizi isterim:").

### 6.3 Yazım ve noktalama
- Prozodi noktalama ve paragrafla verilir: kısa cümle, tire (—), tek üç nokta, paragraf kırılması.
- Gövdede parantezli yönerge yok. "(gülerek)", "(sus)" gibi notlar REJİ NOTLARI'na yazılır.
- Kayıt standart yazımla okunur. Ağız taklidi yazım ("napıyoruz", "chais pas", "gonna") kullanılmaz. Dile özgü istisnalar dil skill'indedir: EN'de standart kısaltmalar (it's, don't) zorunlu; FR'de konuşma Fransızcası ölçülü.

### 6.4 Dublaj ve TTS
- FR kayıt EN'ye dublajlanıyorsa ünlemler EN hedef metinde **kelime olarak** karşılanır: « Bon. » → "Okay.", « Ah ! » → "Oh!", « Ouf. » → "Phew." Saf ses ünlemleri ("Hmm", "Pfff") TTS'te tutarsız çıkabilir. Dublajdan sonra dinlenip kontrol edilir; bu kontrol yapılmadıysa "yapıldı" yazılmaz.
- Ünlemin yeri iki metinde aynı paragraf noktasına düşmeli (yüz ifadesi uyumu).

### 6.5 Sesli okuma testi
- Mümkünse metin yüksek sesle okunur ya da okutulur. Takılınan cümle bölünür, dil sürçtüren kelime değiştirilir.
- Sesli okuma yapılmadıysa DURUM alanına "sesli okunmadı" yazılır; okunmuş gibi raporlanmaz.
