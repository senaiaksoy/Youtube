# EN kanal: küçük resim testi planı (22 Ekim 2026)

Kanal: @DrAksoyFertility (UCo3ZeBXk0ng-OigXd9jqJqQ)

## Neden
Son 28 gün, uzun videolar (Studio): 1,5 bin gösterim, **TO %0,9**, 96 izlenme, ortalama izlenme 2:35.
Gösterim var, tıklama yok. Eşik: %6+ iyi, %4 altı test.

## Mevcut küçük resimler (kontrol edildi)
| Video | ID | Mevcut kapak | Sorun |
|---|---|---|---|
| How Many Eggs Should You Freeze? Real Numbers by Age | J21RLRUE1g8 | "EGGS / How many by age?" | Bordo/krem, koyu takım kesik fotoğraf, arka planda konu yok, ikinci satır küçük |
| IVF Supplements: What Really Helps? | 2hjpsL0bwhM | "BOTTLES / Did they count babies?" | Aynı fotoğraf ve düzen. **Metin başlıkla eşleşmiyor** (Short'un kapağı gibi duruyor). |

- İki kapak da aynı fotoğraf ve aynı şablon. `references/thumbnails.md` § 3 bu kalıbı zaten "Rejected" listesine almış ("DHEA dark-suit cut-out on flat burgundy/cream").
- Hard rule (konuya özel arka plan) ve çeşitlilik kuralı bu iki kapakta uygulanmamış (thumb-log'da kaydı yok).
- Not: Studio'daki analizle, "BOTTLES / Did they count babies?" metninin 12 dk'lık video için doğru kapak olup olmadığını Dr. Aksoy'un teyit etmesi gerekir.

## Önerilen varyantlar (her video için 3, Studio "Test & Compare")
Kurallar: varyantlar birbirinden şablon ve kompozisyonla ayrılır; F13 yasakları (kırmızı daire/ok, % iddiası, şırınga, marka, klinik adı) geçerli; yapay zekâ görselinde yazı yok, yazı `yt_thumb_compose.py` ile eklenir; 120×68 mobil kanıtı zorunlu.

### 1) J21RLRUE1g8: yumurta dondurma
Başlık (şimdiki iyi, 52 kr): "How Many Eggs Should You Freeze? Real Numbers by Age". Başlık testi ayrı yapılacaksa alternatif: "Freezing Eggs at 38: How Many Do You Actually Need?" (51 kr).

| | Şablon | Taraf | Kıyafet | Poz | Arka plan | Metin |
|---|---|---|---|---|---|---|
| A | yellow-focus | left | white-coat | open-hands | chart-data (yaşla azalan eğri, çizgi) | satır1 "HOW MANY EGGS?" · satır2 "BY AGE" · pill "FREEZING" |
| B | coral-contrast | right | shirt | pointing | light-editorial | satır1 "FREEZE AT 38?" · satır2 "HOW MANY EGGS" · chip "38 → ?" |
| C | amber-eyebrow | left | coat-blue-shirt | calm-clasped | clinic-warm (embriyoloji laboratuvarı, bokeh) | eyebrow "EGG FREEZING" · satır "HOW MANY" "EGGS?" |

### 2) 2hjpsL0bwhM: takviyeler
Başlık alternatifleri (strateji § 6): "IVF Supplements: Which Ones Actually Work?" (42 kr) ya da "I Ranked 8 Egg Quality Supplements by Evidence" (46 kr). "8" sayısını videodaki takviye sayısıyla doğrula.

| | Şablon | Taraf | Kıyafet | Poz | Arka plan | Metin |
|---|---|---|---|---|---|---|
| A | yellow-focus | left | white-coat | open-hands | bottles-props (etiketsiz beyaz/amber şişeler) | satır1 "WHICH ONES" · satır2 "WORK?" · pill "IVF SUPPLEMENTS" |
| B | coral-contrast | right | shirt | pointing | bottles-props | satır1 "SUPPLEMENTS" · satır2 "WORTH IT?" |
| C | light-card | left | coat-blue-shirt | calm-clasped | light-editorial | satır1 "RANKED" · satır2 "BY EVIDENCE" · pill "0 TO 4" |

## Uyarı: ölçüm hacmi
Uzun videolarda toplam yaklaşık 1,5 bin gösterim / 28 gün. Video başına birkaç yüz gösterimle Studio testi anlamlı sonuca günler/haftalar sonra varabilir, hatta varamayabilir.
Öneri: A/B'yi yine açın, ama sonuç gelmezse en az kötü görünen varyantı kalıcı yapın; Short'lardan gelen trafik (Shorts akışı %66) kapağı beslemez.

## Sonraki adım (onay bekliyor)
- Higgsfield ile 6 taban görsel (varyant başına 1) üretimi: kredi harcar. Onay ve kredi tavanı Dr. Aksoy'dan.
- Üretimden sonra `yt_thumb_compose.py --check-variety --log-variety`, mobil kanıt, Dr. Aksoy onayı, ardından Studio testi. Yükleme ve test açma, mutasyon kapısı gereği dry-run + onayla.
