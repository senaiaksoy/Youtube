# How Many Eggs Do You Need for One Baby? (By Age) — EN script package (stand-up + sayı bütçesi versiyonu)

**Kanal:** @DrAksoyFertility · **Tarih:** 6 Ekim 2026 · **Skill:** `yt-script-en` (+ CORE, HOOK, STRUCTURE, yt-script-factcheck)

> **⛔ PROJE İPTAL EDİLDİ — 6 Ekim 2026 (Dr. Aksoy'un kararı).** EN dublaj çalışması durduruldu, hiçbir dosya silinmedi.
> - **Bu iş için yapılmış hiçbir dublaj sürümü (v1–v6) yayına hazır değil.**
> - Sebep: Klonlanan sesler bazı İngilizce ifadeleri bozuk telaffuz etti ("record deal", "Freeze twenty. Done."). Telefon kaydı ve Voice Changer da sorunu çözmedi.
> - Son denemede dublaj parçaları "senai ucuz ses" sesiyle, Dynamic Duration modunda yeniden üretildi; bazı parçaları ElevenLabs kırptı. Bu sürüm (`Downloads\how-many-eggs-EN-dub-2026-10-06-v6-ucuzses.mp3`) kontrol edilmedi.
> - Kalanlar:
>   - ElevenLabs dublaj projesi (id `QKTtzpvI9Ludi5EvPAUJ`)
>   - `Downloads` içindeki dublaj MP3'leri, kaynak MP4 ve CSV
>   - Bu klasördeki script dosyaları
> - Projeye yeniden başlanırsa aşağıdaki kayıt nerede kalındığını gösteriyor.

> **✅ YENİ YOL — EN Text to Speech (6 Ekim 2026).** Dublaj yerine onaylı EN script ElevenLabs Text to Speech ile baştan okutuldu. Fransızca kayıtla senkron yok.
> - Ayarlar:
>   - Ses: "senai ucuz ses" (IVC)
>   - Model: Eleven v3, varsayılan Stability
>   - Auto-tag kullanılmadı
>   - Script iki parçaya bölündü (≤5.000 karakter); her parça 2 üretim verdi.
> - Seçilenler: `part1-gen1` + `part2-gen1`. Gen2'lerde gerçek kelime kayıpları vardı, örneğin "dad joke"tan "joke".
> - Whisper karşılaştırması: part 1 %99,3, part 2 %99,8. Kalan farklar Whisper hatası; "a guarantee of" yakından dinlendi, seste var.
> - "record deal" ve "Freeze twenty. Done." net.
> - Çıktı:
>   - `Downloads\how-many-eggs-EN-TTS\how-many-eggs-EN-TTS-full.mp3` (9:55): orijinal 128 kbps MP3 kareleri yeniden kodlanmadan art arda eklendi.
>   - Aynı adla 24-bit `.wav`.
>   - İkisi de orijinal parçalarla bit düzeyinde aynı.
>   - Not: İlk birleştirmede ffmpeg sessizlik kaynağı yüzünden ses 8-bit'e düştü ve cızırtı yaptı (Dr. Aksoy fark etti). Düzeltildi, eski dosyanın üzerine yazıldı.
>   - parçalar ve gen2'ler aynı klasörde
> - Henüz yapılmadı: Dr. Aksoy'un kulak kontrolü ve İngilizce anadil kontrolü.

**Dosyalar**
- Konuşma gövdesi (EN hedef transkript): [video-script-how-many-eggs-en-2026-10-06.txt](video-script-how-many-eggs-en-2026-10-06.txt)
- FR kayıt metni (EN ile paragraf paragraf hizalı; espriler Fransızcada yeniden kuruldu): [video-script-how-many-eggs-en-2026-10-06-fr-recording.txt](video-script-how-many-eggs-en-2026-10-06-fr-recording.txt)

**Format:** K2/K3 sınırında. 1.324 kelime, tahmini 8:50–10:10 (130–150 wpm; sesli okumayla doğrulanmadı). İlk doğrulanmış sayı ~30. saniyede. Sesli istatistik ~30'dan ~10'a indirildi; hepsi "10 kadından X" (ya da "10 yumurtadan X") formatında.

---

## DURUM
- **Bilimsel doğrulama: geçti** (2026-10-06). Dört bağımsız tur yapıldı:
  - ilk tam metin: 36 iddia
  - benzetme turu: 6 iddia
  - stand-up turu: 17 iddia
  - sayı bütçesi turu: 9 madde
  - Sonuç: ❌ ve 🕒 yok. Son turdaki tek ❓ (Cascante Tablo 2 hücreleri) daha önce başka bir alt ajanın NCBI tam metin XML'inden birebir alıntısıyla doğrulanmıştı. Tüm ⚠️ düzeltmeler iki dilde uygulandı.
- **Açılış anısı** (akşam yemeği): Dr. Aksoy'un gerçek deneyimi; C seçeneğini seçerek onayladı (2026-10-06).
- **"My take" paragrafı (EN + FR): Dr. Aksoy onayladı (2026-10-06).** Bütün script için "klinik onaylı" etiketi verilmedi; o etiketi yalnızca Dr. Aksoy verir.
- **FR metin onayı (Dr. Aksoy): onaylandı (2026-10-06).** İki düzeltmeyle birlikte onaylandı: « je vais vraiment le justifier » (eskisi « la mériter ») ve « plus tôt, c'est en général mieux pour vos chances » (eskisi « plus tôt est en général plus favorable »).
- **Sesli okuma: yapılmadı.**
- **Anadil (EN) kontrolü:** Yapay zekâ ile kulak okuması yapıldı; insan anadil kontrolü yapılmadı (2026-10-06). Dr. Aksoy'un onayıyla üç düzeltme uygulandı:
  - "In one large egg-freezing clinic" → "At one large…"
  - "So here's one." → "So here's an actual statistic."
  - Sunkara cümlesi ikiye bölündü; anlam ve "mature or not" uyarısı korundu.
  - Bu düzeltmeler yalnızca EN metne uygulandı; FR karşılıkları zaten açık olduğu için FR metin değişmedi.
- **Yayın ön koşulu:** EP01 (supplements) herkese açık olmalı; bitiş ekranı ona yönlendiriyor.
- **Dublaj kararı (2026-10-06):** Dr. Aksoy İngilizce kayıt yapmayacak; akşam yemeği sahnesi dahil tüm video FR kayıttan ElevenLabs ile dublajlanacak. Bunun için iki şey gerekiyor:
  - **Kayıt sırasında:** Komik zamanlama için FR kayıtta « Ça dépend » demeden önce gerçek bir duraklama bırakılmalı. Aynı şekilde « … Oui, c'était une blague Carambar » ve « elle date de quand, la photo ? » öncesinde de duraklama olmalı.
  - **Dublaj sırasında:** ElevenLabs'e çeviri metni olarak onaylı EN script verilmeli, otomatik çeviri kullanılmamalı. Aksi hâlde uyarlamalar kelimesi kelimesine çevrilir: « blague Carambar » → "dad joke" ve « omelette » → "breakfast plate" kaybolur. Dublajdan sonra bu iki espri ve sayı cümleleri ("X out of 10") EN metinle karşılaştırılmalı.
  - **Uygulama (2026-10-06):**
    - FR kayıt dosyası: `Downloads\oosit eleven icin.mp3` (12:08).
    - Kayıt faster-whisper ile yazıya döküldü ve script ile hizalandı. Sonuç 105 satırlık bir CSV: `video-script-how-many-eggs-en-2026-10-06-manual-dub.csv`. Her satırda konuşmacı, başlangıç, bitiş, FR (söylenen hâl) ve EN (onaylı script) var.
    - CSV, ElevenLabs Dubbing'in Manual mode'una yükleniyor. Bu mod yalnızca video kabul ettiği için ses, siyah ekranlı bir MP4'e sarıldı.
    - Kayıttaki sapmalar:
      - « on commence » eklenmiş → "let's get started"
      - « Le total. » söylenmemiş → EN'den çıkarıldı
      - kapanışa « Voilà l'adresse. / Allez, ciao ! » eklenmiş → "Here's the link." / "Alright — ciao!"
      - « la mériter » ve « plus tôt est… plus favorable » eski hâliyle kaydedilmiş; EN karşılığı aynı kaldı.
    - **Dublaj sonucu (2026-10-06):**
      - ElevenLabs projesi: "how-many-eggs-FR-dublaj-kaynak.mp4" (dubbing id `QKTtzpvI9Ludi5EvPAUJ`), yaklaşık 36.400 kredi.
      - Britanya analizi parçası (29 sn) 25 sn sınırını aştığı için Dynamic Duration ile üretildi.
      - Çıktı: `Downloads\how-many-eggs-EN-dub-2026-10-06.mp3` (12:08).
    - **Whisper karşılaştırması:**
      - Onaylı EN metinle benzerlik %97. Bütün espriler ve kapanış seste var.
      - Telaffuz şüpheli yerler (insan kulağıyla dinlenmeli): 3:38–3:58 ("record deal", "Bottom line… babies… and age"), 10:44–10:54 ("Freeze twenty, done, just ask him"), 11:22–11:33 ("And if… fewer eggs… a second cycle"), 11:48–11:56 ("And… egg quality").
    - **v2 (2026-10-06):**
      - 5 parça Fixed Duration ile yeniden üretildi; proje kredisinden 524 kredi gitti.
      - Çıktı: `Downloads\how-many-eggs-EN-dub-2026-10-06-v2.mp3` (17:21 render). v1 dosyası duruyor.
      - Whisper'a göre düzelenler: 11:22 ("fewer eggs… second cycle") ve 11:48 ("egg quality").
      - Hâlâ şüpheli olanlar: 3:38–3:58 ("record deal: a chromosomally…", "and babies… all three") ve 10:44–10:54 ("Freeze twenty, done, just ask him"). Kulakla dinlenmeli.
    - **v3 (2026-10-06):**
      - Dr. Aksoy'un onayıyla yalnızca noktalama değişti, kelimeler aynı:
        - "record deal: a chromosomally" → "record deal. A chromosomally"
        - `"Freeze twenty, done," just ask him` → `"Freeze twenty. Done." Just ask him`
      - Aynı değişiklik EN script'e ve CSV'ye de işlendi.
      - İki parça yeniden üretildi; 196 kredi gitti, proje kredisinde 28.753 kaldı.
      - Çıktı: `Downloads\how-many-eggs-EN-dub-2026-10-06-v3.mp3` (17:29 render).
      - Whisper'a göre:
        - "A chromosomally normal embryo doesn't always implant" artık net.
        - "record deal" ve "Freeze twenty. Done." hâlâ net çözülemiyor; aksan ya da Whisper hatası olabilir.
        - "Bottom line" parçasına bu turda dokunulmadı.
      - Son karar Dr. Aksoy'un kulak kontrolüne bağlı. ElevenLabs'te her parçanın "Clip History"si v1–v3 üretimlerini tutuyor.
    - **v4 (2026-10-06):**
      - Dr. Aksoy iki ifadeyi kendi sesiyle EN kaydetti:
        - `Documents\Ses Kayıtları\Kayıt (22).m4a` = "record deal"
        - `Kayıt (24).m4a` = "Freeze twenty. Done."
      - Kayıtlar v3'e yerel olarak eklendi, ElevenLabs kullanılmadı:
        - "record deal" → 221.80–222.62 sn penceresi, 0,81 sn konuşma
        - "Freeze twenty. Done." → 648.10–649.80 sn penceresi, 1,51 sn konuşma
        - 80 Hz high-pass, konuşma RMS'i dublajla eşitlendi (+8,5 / +5,0 dB), 12 ms fade; süre değişmedi (12:07.8).
      - Çıktı: `Downloads\how-many-eggs-EN-dub-2026-10-06-v4.mp3`. Betik: oturum scratchpad'indeki `splice.py`.
      - ElevenLabs projesi v3 hâlinde kaldı; v4 yalnızca yerel dosya.
      - Dr. Aksoy dinledi: telefon kaydının ses kalitesi dublajdan farklı, yapay duruyor.
    - **Voice Changer denemesi (başarısız):**
      - Kayıtlar ElevenLabs Voice Changer'da "Senai aksoy" PVC sesine çevrildi (Eleven English v2, iki deneme).
      - Whisper girdiyi net duyuyor ("Record deal. First 20, done."), çıktıyı duyamıyor ("Lack of deal. Finish duality dong.").
      - PVC sesi İngilizce kelimeleri bozuyor; kullanılmadı.
    - **v5 (2026-10-06):**
      - Aynı iki kayıt yerelde işlendi:
        - dublajın çevresindeki 40 sn konuşmasına göre spektral EQ eşleme (±12 dB)
        - hafif sıkıştırma ve seviye eşleme
        - pencereye dublajın kendi oda tonu eklendi
      - Çıktı: `Downloads\how-many-eggs-EN-dub-2026-10-06-v5.mp3`. Betik: scratchpad'deki `splice_eq.py`.
      - Kulak onayı bekleniyor. Olmazsa yedek plan: iki ifadeyi FR kaydın yapıldığı mikrofon ve odada yeniden kaydetmek.

---

## AÇILIŞ ALTERNATİFLERİ
- **C (seçilen, scriptteki):** Akşam yemeği sahnesi: "Being a fertility doctor at a dinner party goes like this…"
- **A (Dr. Google):** "You type one question into Google: 'How many eggs do I need for one baby?' Google answers in half a second. Twenty. No — fifteen. No, wait — 'it depends.' And then it shows you an ad for a vitamin…"
- **B (her şeyi bilen amca):** "Every family has one. The uncle with a number. 'Eggs? Freeze twenty. Done.' … Your uncle has never seen an egg that wasn't on a breakfast plate. But he did ask the right question…" (Amca şu an gövdede, 2. bölümde kullanılıyor.)

---

## BÖLÜMLER (açıklama için; 140 wpm tahmini, kayıttan sonra düzeltilir)
```
00:00 Intro
01:01 Eggs, embryos, babies
03:04 The numbers by age
04:39 Does doubling your eggs double your chance?
05:39 IVF is different
06:47 Before you decide
07:33 My take
08:06 Back to the dinner party + questions for your doctor
```

---

## STAND-UP HARİTASI
| Bölüm | Sahne (bit) | Kavrama hizmeti | Geri dönüş |
|---|---|---|---|
| Giriş | Akşam yemeği: "how many eggs should I freeze?" → "It depends." | Ana soruyu ve "neye bağlı" vaadini kurar | Kapanış: "So, back to the dinner party…" |
| Yumurta → bebek | "It depends… diplomalarımıza basılmalı" + **fotoğraf** benzetmesi + **yetenek yarışması** turları | Eleme basamakları ve yaş etkisi | Fotoğraf: "Before you decide" ve kapanış |
| Yaşa göre sayılar | Her şeyi bilen amca ("breakfast plate") + sepet baba esprisi | Bir hikâye istatistik değildir; toplam yumurta önemlidir | Kapanış: "ask him: how old is the photo?" |
| Tüp bebek | "I'll spare you the spreadsheet" | Tablo ekranda, söyleyişte yalnızca anlam | — |
| Risk | "not a personal record" (risk cümlesinin kendisi mizahsız) | Güvenli sayı | — |
| Hassas yerler | Mizah yok: 40 yaş üstü sayılar, güven aralıkları, hiperstimülasyon | | |

---

## SAYI BÜTÇESİ: SESLİ KALANLAR / EKRANA GİDENLER

| Bölüm | Sesli yıldız sayı | Ekrana (tam değer + kaynak) |
|---|---|---|
| Giriş | ≤35 yaşta 10 kadından ~5'i; ≥40 yaşta ~2'si | Hirsch 2024 · 10 çalışma · 1.517 geri dönen kadın · %52 (41–63) / %19 (13–29) |
| Yumurta → bebek | <38 yaşta 10 çözülen yumurtadan 2–3'ü normal embriyo; ≥38 yaşta 10'da 1'den az | Yaşama: büyük derlemelerde ~%78–81, deneyimli klinikte %90,7. Örnek hesap: 20 yumurta, 34 yaş → ~4–6; 40 yaş → ~1–2 (Klein 2025). Grafik etiketi **"eggs"** (kadın değil). |
| Yaşa göre (ana tablo) | Tahmin sorusu → 20+ yumurta: 7–8 / 5 / 3–4 (10 kadından) | Cascante 2024 · NYU · 731 kadın · bebek veya >12 hafta süren gebelik. Tam tablo: <10 yumurta 33/32 · 21 · 10; ≥20: 71/78 · 53 · 36. ≥41 hücresinde güven aralığı %13–65. |
| İki kat yumurta | 34 yaş, 10→20 yumurta: 10 kadından ~5 → 7'ye yakın | Cascante modeli ~%49 → ~%66 |
| Tüp bebek | Sözle: ~15'e kadar artıyor, 15–20 düz, >20 düşüyor | Sunkara 2011 · İngiltere · 400.135 döngü · model tahmini · 2006–07 değerleri · toplanan tüm yumurtalar: 15 yumurtada <35: 40 · 35–37: 36 · 38–39: 27 · 40+: 16 (100 kadından). Polyzos 2018 · ~15.000 kadın · ≥25 yumurtada kümülatif ~%70 · eğri tepede yavaşlıyor, düzleşmiyor. |
| Karar öncesi | 10 kadından ~1'i geri dönüyor | Hirsch %11,1; Klein %10,4 |

## REJİ NOTLARI
- **Akşam yemeği sahnesi:** Hafif öne eğilme, sola-sağa bakış, fısıltı tonu. "It depends." öncesinde 1 saniye sus, kameraya düz bakış. İsteğe bağlı: yakınlaşma.
- **"printed on our diplomas":** Ekranda bir diploma üzerinde "IT DEPENDS" damgası (görsel espri).
- **Fotoğraf benzetmesi:** Fotoğraf karesi, üzerinde "age on the day you froze"; yanında üstü çizili zaman makinesi. Kapanıştaki geri dönüşte aynı kare.
- **Yetenek yarışması:** 20 yumurta ikonu sahnede. Her turda (Thaw → Fertilization → Day-5 embryo → Chromosomes) bir kısmı "go home" ile solar. Kısa jüri zili sesi isteğe bağlı. Etiketler ikonların üzerinde.
- **"record deal":** Kısa bir altın plak görseli, ardından ciddi tona dönüş.
- **Amca:** Konuşurken ses tonu değişir (kendinden emin amca sesi). "breakfast plate" sözünde ekranda sahanda yumurta.
- **Tahmin sorusu (ana tablodan önce):** Ekranda "Your guess: __ out of 10?" ve 10 boş kadın ikonu, 1–2 sn sus. Cevapta ikonların 7–8'i dolar.
- **Cascante tablosu (videonun tek ana tablosu):** 10'luk kadın ikon dizisi. Satırlar <38 / 38–40 / ≥41; sütunlar <10 / ≥20 olgun yumurta. Sesli yalnızca ≥20 sütunu okunur; <10 sütunu ekranda. Altında "NYU, 731 women · baby or ongoing pregnancy". ≥41 hücresinde aralık çubuğu. **Mizahsız sunulur.**
- **Sepet esprisi:** Ekranda bir sepet; kısa gülümseme.
- **"I'll spare you the spreadsheet":** Ekranda Sunkara tablosu: "UK, 2006–07 · fresh cycle · predicted · 15 eggs collected (mature or not)". Değerler: <35: 40 in 100 · 35–37: 36 · 38–39: 27 · 40+: 16. Yanında "rises to ~15 → flat 15–20 → down >20" eğrisi.
- **"Now, the serious part":** Ton değişimi; müzik varsa kesilir.
- **"My take":** Kameraya yakın plan, grafik yok.
- **Kapanış geri dönüşleri:** Akşam yemeği masası ve fotoğraf karesi kısa süre geri gelir.
- **Doktora sorulacak 3 soru:** Ekranda madde madde; açıklamaya ve sabitlenmiş yoruma da eklenir.
- **Disclaimer:** Ekranda ve sesli.
- **Son 20 sn:** Bitiş ekranı (EP01 + abone). Önemli grafik altında kalmaz.

---

## AÇIKLAMA İÇİN: DOKTORA SORULACAK SORULAR
1. How many mature eggs would you expect me to get per cycle, at my age and with my test results?
2. What's your lab's survival rate after thawing, and how many women my age have had a baby from their frozen eggs here?
3. If one cycle gives fewer eggs than we hoped, what would a second cycle realistically add?

---

## BİLİMSEL DOĞRULAMA RAPORU (özet)

Üç bağımsız alt ajan turu yapıldı; yazarın gerekçesi doğrulayıcıya verilmedi. Ana ajan uzlaştırmayı yaptı. Kaynaklar bu oturumda PubMed'den alındı. Cascante 2024 ve Klein 2025 tam metinden, diğerleri abstract'tan okundu. Geri çekilmiş kaynak yok.

**Ana kaynaklar**
- Hirsch 2024 [DOI](https://doi.org/10.1093/humupd/dmae009): geri dönen kadın başına canlı doğum ≤35 yaşta %52, ≥40 yaşta %19; çözülme sonrası yaşama %78,5; geri dönüş oranı %11,1.
- Klein 2025 [DOI](https://doi.org/10.1016/j.fertnstert.2025.12.003): yaşama %90,7; döllenme %77,2; blastulasyon ~%50; çözülen olgun yumurtanın öploid embriyoya dönüşme oranı <38 yaşta ~%20–30, 38–42 yaşta ~%8–9.
- Cascante 2024 [DOI](https://doi.org/10.1007/s10815-024-03175-w): Tablo 2 (yaş × çözülen olgun yumurta); 34 yaşta 10→20 yumurta ile ~%49→~%66; döngü sayısı tek başına bağımsız belirleyici değil.
- Sunkara 2011 [DOI](https://doi.org/10.1093/humrep/der106): taze döngüde ~15 yumurtaya kadar artış, 15–20 arası düz, >20 düşüş; 15 yumurtada 40/36/27/16.
- Polyzos 2018 [DOI](https://doi.org/10.1016/j.fertnstert.2018.04.039): ≥25 yumurtada kümülatif canlı doğum %70.
- Steward 2014 [DOI](https://doi.org/10.1016/j.fertnstert.2013.12.026): OHSS riski yumurta sayısıyla artıyor.
- ASRM 2021 [DOI](https://doi.org/10.1016/j.fertnstert.2021.02.024): yenidoğan sonuçları benzer.
- Roger 2025 [DOI](https://doi.org/10.1007/s10815-024-03350-z) ve Torra-Massana 2023 [DOI](https://doi.org/10.1016/j.rbmo.2023.04.019): saklama süresi sonuçları değiştirmedi (~8–11 yıl).
- Barrett 2024 [DOI](https://doi.org/10.1007/s10815-024-03149-y): sonucu toplama yaşı belirliyor, transfer yaşı değil.
- Franasiak 2014 [DOI](https://doi.org/10.1016/j.fertnstert.2013.11.004): anöploidi yaşla artıyor.
- Vaiarelli 2020 [DOI](https://doi.org/10.1093/humrep/deaa203): öploid embriyo her zaman tutunmuyor.
- Kirubarajan 2024 [DOI](https://doi.org/10.1016/j.fertnstert.2024.06.025): geri dönüş %10,8; yaşama %81,4.

**Stand-up turunda düzeltilenler (⚠️ → düzeltildi)**
| Cümle | Sorun | Düzeltme |
|---|---|---|
| "strictest judge in the whole competition" | <38 yaşta embriyo gelişimi turu kromozom turu kadar ya da daha çok eliyor | "A tough judge — and the older the eggs, the tougher it gets" |
| Sunkara "then leveled off" | >20 yumurtadaki düşüş eksikti | "leveled off between 15 and 20, and went down beyond 20" |
| "It improves your odds later" | Fazla kesin | "It can improve your odds later — mostly when the eggs are frozen younger" |
| "very experienced labs" | ~9/10 tek bir kliniğe ait | "some very experienced labs" |
| FR « D'après les études » | "so far" çekincesi düşmüştü | « Jusqu'ici, les études montrent… » |
| Giriş zamanlaması | İlk sayı ~35–40 sn'de geliyordu | İki dolgu cümlesi çıkarıldı → ~30 sn |
| "growing into an embryo" | Döllenmiş yumurta zaten embriyo | "a day-five embryo" |
| "It depends" iki kez tekrar | Yapısal tekrar | 1. bölüm girişi kısaltıldı |

**Sayı bütçesi turu (2026-10-06):** Değişen 9 maddenin hepsi ✅. Uygulanan küçük düzeltmeler:
- Polyzos için "kept climbing — more slowly at the top, but with no flattening".
- Tahmin sorusu "froze before 38 and later thawed 20 or more" yapıldı; veri çözülen yumurtaya göre gruplanmış.
- Sunkara cümlesine "mature or not" eklendi.
- Sayı formatı taraması: "%", "1 in" ve "half" kalmadı.

**Hekim onayı gereken maddeler:** "My take" paragrafı ve doktora sorulacak üç soru.
