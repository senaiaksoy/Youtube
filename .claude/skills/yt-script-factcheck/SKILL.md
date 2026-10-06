---
name: yt-script-factcheck
description: Dr. Senai Aksoy'un YouTube scriptlerindeki bilimsel ve tıbbi iddiaları yazımdan sonra bağımsız ve ayrıntılı biçimde yeniden doğrular. Her iddiayı cümle cümle çıkarır, PubMed, kılavuz ve Cochrane kaynağıyla birincil metinden kontrol eder; popülasyon, sonuç, payda, kesinlik ve güncellik çarpıtmalarını, geri çekilmiş çalışmaları ve çeviri kaymasını arar. Rapor üretir ve yanlışlar düzeltilmeden "kaynak kontrollü" etiketine izin vermez. yt-script-tr/fr/en ile yazılan her scriptin sonunda zorunludur. Ayrıca "iddiaları kontrol et", "fact-check", "bilimsel doğrulama", "bu scriptte yanlış bilgi var mı" taleplerinde tek başına kullanılır.
---

# yt-script-factcheck — Yazım sonrası bilimsel doğrulama

Amaç: İzleyiciye yanlış veya çarpıtılmış tıbbi bilgi gitmemesi. Yazım sırasında tutulan iddia kaydı (CORE Adım 3) başlangıç noktasıdır. Bu skill o kaydı **sorgular**; olduğu gibi onaylamaz.

Üst kural: `C:\Users\KC3\.codex\skills\youtube-script-senai-aksoy\references\medical-evidence.md` (kanıt eşleştirme, güncellik, IVF sonuç ayrımları, sayılar). Bu skill o kuralları yazım sonrası denetime çevirir.

---

## Ne zaman
- `yt-script-tr`, `yt-script-fr` veya `yt-script-en` ile yazılan **her** script için. Konuşma doğallığı geçişinden (CORE §6) **sonra** çalışır, çünkü cümleler değiştirilirken anlam kayabilir.
- Revizyon sonrası: yalnızca değişen cümleler ve onlara bağlı iddialar yeniden doğrulanır.
- Kullanıcının verdiği veya eski bir script için tek başına (denetim modu).

## Değişmez kurallar
1. **Hafızadan kaynak yok.** Her PMID, DOI ve kılavuz bu oturumda bir araç sonucundan gelmeli (PubMed MCP, WebFetch). Gelmediyse iddia ❓ olur.
2. **Özet değil kaynak metin.** Abstract, tam metin veya kılavuz bölümü okunur. Basın bülteni, blog ve ikincil haber yalnızca ipucudur. Erişim kapsamı yazılır: tam metin / yalnızca abstract / ikincil.
3. **Bağımsızlık.** Doğrulamayı scripti yazan bağlam yapmaz. Yazarın gerekçeleri değil yalnızca metin ve iddia kaydı verilerek ayrı bir alt ajan çalıştırılır (bkz. Adım 3).
4. **Sessiz düzeltme yok.** Her değişiklik raporda görünür.
5. **Belirsizlik saklanmaz.** Doğrulanamayan iddia ya çıkarılır ya da belirsizliğiyle birlikte söylenir. Kesin bilgi gibi bırakılmaz.

---

## Adım 1 — İddiaları çıkar
Konuşma gövdesini cümle cümle tara. Şunlar iddiadır:

| Tür | Ne | Örnek |
|---|---|---|
| **S** Sayı / istatistik | Oran, yüzde, eşik, süre, doz, kesme değeri | "48 saatte en az %49 artış" |
| **E** Etkinlik / nedensellik | X, Y'yi artırır / azaltır / işe yaramaz | "DHEA canlı doğumu artırmıyor" |
| **K** Kılavuz / düzenleyici durum | ESHRE önerir, FDA onaylı, HFEA kırmızı | "ESHRE rutin kullanımı önermiyor" |
| **M** Mekanizma / fizyoloji | Biyolojik açıklama | "hCG'yi plasentayı oluşturacak hücreler üretir" |
| **G** Güvenlik / acil | Kırmızı bayrak belirtiler, yan etki | "tek taraflı şiddetli ağrı acil değerlendirme gerektirir" |
| **Z** Zamanlama | Kaçıncı gün, ne kadar sürede | "transferden 9–11 gün sonra" |
| **Ö** Örtük iddia | Espri, benzetme, iç ses içindeki gerçek iddia | "Çay implantasyona yardım etmez." |
| **T** Mutlak dil | asla, her zaman, kanıtlanmış, hiçbir anlamı yok, tamamen işe yaramaz | "totally useless" (EP01 dersi) |

Espri ve benzetmelerdeki **örtük iddialar** atlanmaz. Mutlak dil ayrıca işaretlenir.

Her iddiaya ID ver (C01, C02…) ve gövdedeki **tam cümleyi** yaz.

## Adım 2 — Kaynağa git
Her iddia için doğru kanıt tipi aranır (medical-evidence.md "Match the question"):
- **Araçlar:**
  - PubMed MCP: `search_articles`, `get_article_metadata`, `get_full_text_article`, `find_related_articles`
  - Consensus araması (keşif için; sonuç PubMed'de doğrulanır)
  - ClinicalTrials.gov
  - Kılavuz sayfaları için WebSearch ve WebFetch: ESHRE, ASRM, ACOG, NICE, HFEA, Cochrane Library
  - Vault master kılavuz dosyaları: `D:\A-klasör\obsidian-vaults\draksoyivf-knowledge\wiki\medical\guidelines\`
- **Güncellik:**
  - Kılavuzun son sürümü ve güncelleme tarihi kontrol edilir.
  - Son 3 yılda konuyu değiştiren sistematik derleme veya büyük RCT aranır.
  - Bir derlemenin yayın tarihiyle tarama tarihi farklı olabilir.
- **Geri çekilme:**
  - `get_article_metadata` sonucundaki makale türünde "Retracted Publication", "Retraction of Publication" veya "Expression of Concern" var mı bakılır.
  - Şüphede "<başlık> retraction" diye aranır.
- **Vault kaydı:** Vault'ta aynı konu varsa (`wiki/medical/...`) iddianın vault'la çelişip çelişmediği ayrıca not edilir.

## Adım 3 — Bağımsız doğrulayıcı (alt ajan)
Agent aracıyla `general-purpose` alt ajan başlat. Prompt'a yalnızca şunları ver:
- konuşma gövdesinin tam metni (EN için FR kayıt metni de),
- Adım 1 iddia listesi,
- yazarın iddia kaydı (kaynak listesi), ama gerekçeleri değil,
- bu SKILL.md'nin Adım 2, 4 ve 5 talimatları.

Alt ajandan her iddia için Adım 5 tablosunu doldurmasını iste. Kaynakları kendisi bulmalı; yazarın kaynağını da açıp iddiayı gerçekten destekleyip desteklemediğine bakmalı.

Alt ajan sonucu geldikten sonra ana ajan iki işi yapar:
- **Uyuşmazlık:** Yazar kaydıyla alt ajan arasında fark varsa kaynağı kendisi açar ve kanıta göre karar verir. "Çoğunluk" değil kanıt belirler.
- **Aynı kaynak sorunu:** İki taraf da aynı tek kaynağa dayanıyorsa, merkezi iddialar için en az bir bağımsız ikinci kaynak aranır.

Agent aracı yoksa doğrulama ana bağlamda yapılır ve raporda "bağımsız alt ajan kullanılamadı" yazılır.

## Adım 4 — Çarpıtma kontrolü (her iddia için)
İddia "kaynakta var" diye doğru sayılmaz. Şu kaymalara tek tek bakılır:
- **Popülasyon:** Semptomlu kadınlar mı, IVF hastaları mı? Yaş grubu? Düşük rezerv mi? İddia kaynağın kapsamından geniş mi?
- **Sonuç:** Oosit sayısı, fertilizasyon, embriyo, implantasyon, klinik gebelik, düşük ve canlı doğum ayrı sonuçlardır. "Daha fazla yumurta" "daha fazla bebek" diye söylenmemiş olmalı.
- **Payda:** Başlanan siklus, toplama, transfer, hasta ya da kümülatif?
- **Oran:** Göreli oran mutlak gibi söylenmiş mi? Mutlak fark, desteklenen bir taban oran olmadan hesaplanmış mı?
- **Kesinlik:** Kaynak "düşük kesinlik" diyor, script "işe yarıyor" diyor mu? "Kanıt yetersiz" ile "etkisi yok" karıştırılmış mı? "Zarar bildirilmemiş" ile "güvenli" karıştırılmış mı?
- **Nedensellik:** İlişki neden-sonuç gibi söylenmiş mi?
- **Mekanizmadan sonuca sıçrama:** Laboratuvar ya da hayvan verisinden klinik fayda çıkarılmış mı?
- **Sayı ve aritmetik:** Hesap yeniden yapılır. Yuvarlama anlamı değiştirmiş mi? Birim doğru mu (mIU/mL, IU/L)? FR'de ondalık virgül doğru mu?
- **Güncellik:** Eşik ya da öneri eskimiş mi? (Örnek: hCG için eski "%66 artış" eşiği yerine başlangıç değerine göre değişen eşikler; Barnhart 2016.)
- **Mutlak dil:** "Asla" ve "her zaman" kaynak tarafından destekleniyor mu?
- **Çeviri kayması:** Gövdede FR kayıt + EN hedef ya da TR'den uyarlama varsa iki metindeki iddia aynı mı? Olumsuzluk, kesinlik derecesi ve sayı aynı mı?
- **Espri ve benzetme:** Benzetme yanlış bir biyolojik çıkarıma yol açıyor mu? Örtük iddia doğru mu? Gerekiyorsa sınırı söylenmiş mi? Açıklayan benzetmelerin her biri ayrı bir iddia olarak tabloya girer (ör. "yumurta dondurucuda yaşlanmaz").

## Adım 5 — Rapor
Raporu scriptin `-sources.md` dosyasına "BİLİMSEL DOĞRULAMA RAPORU" başlığıyla yaz. Dosya istenmediyse yanıtta ayrı blok olarak ver.

```
Tarih: YYYY-MM-DD · Doğrulayıcı: bağımsız alt ajan + ana ajan uzlaştırması
Toplam iddia: N · ✅ a · ⚠️ b · ❌ c · ❓ d · 🕒 e

| ID | Gövdedeki cümle | Tür | Kaynak (yazar, yıl, dergi/kurum; PMID/DOI linki; erişim) | Kaynak ne diyor (popülasyon, sonuç, etki, kesinlik) | Karar | Düzeltme |
```

Karar kodları:
- ✅ **Doğrulandı:** Kaynak cümleyi bu haliyle destekliyor.
- ⚠️ **Nüans eksik:** Doğru ama aşırı genel, kesinliği yüksek veya bir koşul eksik. Ek ya da yumuşatma gerekli.
- ❌ **Yanlış:** Kaynak tersini veya başka bir şeyi söylüyor.
- ❓ **Doğrulanamadı:** Kaynak bulunamadı veya erişilemedi.
- 🕒 **Eskimiş:** Daha yeni kılavuz ya da kanıt farklı söylüyor.

Raporda ayrıca şunlar bulunur:
- **Hekim onayı gereken maddeler:** Dr. Aksoy'un klinik görüşü (Beat D), uygulama önerisi, ülkeye özgü yasal durum. Bunlar kanıtla "doğrulanmaz"; hekim onayına gider.
- **Geri çekilme kontrolü:** Yapıldı / sonuç.
- **Bağımsızlık:** Alt ajan kullanıldı mı?

## Adım 6 — Düzeltme ve kapı
- **Kendi yazdığımız taslakta:**
  - ❌ ve 🕒 düzeltilir.
  - ⚠️ için nüans konuşmaya eklenir; belirsizlik iddianın yanında, aynı cümlede ya da hemen ardından söylenir.
  - ❓ ya çıkarılır ya da belirsizliği açıkça söylenerek yeniden kurulur.
  - Değişen her cümle raporda "önce → sonra" olarak gösterilir ve Adım 2–4'ten yeniden geçer.
- **Kullanıcının veya başkasının metninde:** Düzeltme yalnızca önerilir; onay gelmeden uygulanmaz.
- **Kapı:** Gövdede ❌, ❓ veya 🕒 kalırken DURUM alanına "kaynak kontrollü" yazılamaz. Bu skill hiçbir zaman "klinik onaylı" etiketi vermez; o etiketi yalnızca Dr. Aksoy verir.
- **DURUM satırı:** `Bilimsel doğrulama: geçti (YYYY-MM-DD, N iddia, bağımsız alt ajan) · Klinik onay: bekliyor`
- Konuşma, düzeltmeden sonra yeniden CORE §6 doğallık kontrolünden geçer. Bu sırada anlam değişirse ilgili iddia tekrar doğrulanır.

## Sık yakalanan hatalar (kontrol listesi)
- [ ] "Daha fazla yumurta / embriyo" → "daha yüksek canlı doğum" sıçraması
- [ ] Cochrane veya derlemede "low/very low certainty" sonucunun "işe yarıyor" ya da "tamamen işe yaramaz" diye söylenmesi
- [ ] Eski eşik ve kesme değerleri (hCG, AMH, endometrium kalınlığı)
- [ ] Göreli risk mutlak risk gibi
- [ ] Kaynağın gücünden daha sert sıfat ("fabricated", "kanıtlanmış", "mucize")
- [ ] Ülkeye özgü yasal ve onay durumunun her izleyiciye genellenmesi
- [ ] Espri içinde doğrulanmamış biyoloji
- [ ] FR ve EN metinlerde farklı sayı ya da farklı kesinlik
- [ ] Evidence Score ataması (EN kanal) tek yönlü ölçeğin tanımıyla ve kaynakla uyumsuz; 0 ("test edildi, işe yaramadı") ile 1 ("insanda test edilmedi") karışmış; skoru taşıyan çalışmalardan biri geri çekilmiş; aynı skora farklı hüküm dili kullanılmış. Ölçek: `yt-script-en` SKILL.md "Format: Evidence Score"
