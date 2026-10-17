"""TR GLP-1 recut (8ZtwHFtF0Io) metadata taslağı → fixes-tr-metadata.json + METADATA-TR.md (Dr. Aksoy onayı için).
Bölüm zamanları kaynak saniyesinden TR zaman çizelgesine çevrilir (tek kesim 627,30–631,133 sn).
Run: py -3.12 -I build_fixes.py"""
import json, math, pathlib
D = pathlib.Path(__file__).parent
CUT = (627.30, 18934 / 30)
tl = lambda s: s if s <= CUT[0] else s - (CUT[1] - CUT[0])
mmss = lambda t: f"{int(t) // 60:02d}:{int(t) % 60:02d}"
CH = [  # (kaynak saniyesi, başlık) — sahne sınırları analysis/scenes.json, kelime zamanları words-large.json
    (0.0, 'Telefonda iki video: iğne ve "sürpriz gebelik"'),
    (72.60, 'GLP-1 nedir?'),
    (131.60, 'PKOS: insülin direnci ve yumurtlama'),
    (181.70, '"Bende PKOS var, bana bu iğne lazım" mı?'),
    (208.70, 'Çalışmalar ne diyor?'),
    (245.95, '2026 kayıt çalışması'),
    (294.00, 'Adet, yumurtlama, test, canlı doğum: dört ayrı sonuç'),
    (319.70, 'Tüp bebekte canlı doğum: kanıt var mı?'),
    (331.30, '2023 PKOS kılavuzu ve letrozol'),
    (377.70, 'Seyrek adet gebelikten korur mu?'),
    (435.00, 'Gebelikten ne kadar önce bırakılmalı?'),
    (481.70, 'Tirzepatid ve doğum kontrol hapı'),
    (531.56, 'İlaç kullanırken gebelik testi pozitif çıkarsa'),
    (585.45, 'Tüp bebek öncesi: kilo, yaş ve zaman'),
    (CUT[1], 'Yumurta toplama ve anestezi'),
    (681.84, 'Peki erkekler?'),
    (723.60, 'Yan etkiler ve kilo geri alımı'),
    (750.50, 'Hekiminize soracağınız üç soru'),
]
chapters = '\n'.join(f'{mmss(tl(s))} {t}' for s, t in CH)
title = 'Zayıflama iğnesi ve gebelik: Hamile kalmaya gerçekten yardım eder mi?'
desc = f'''“Vurdum, iştahım kesildi” bir videoda, “bu iğneyi kullandım, sürpriz hamile kaldım” bir sonrakinde. Sosyal medyada zayıflama iğnesiyle gebelik arasındaki bağ çok kolay kuruluyor. Doç. Dr. Senai Aksoy, GLP-1 ilaçları (semaglutid, liraglutid, tirzepatid) ile doğurganlık konusunda çalışmaların gerçekte ne gösterdiğine bakıyor.

Kısaca: Bu ilaçlar bazı kadınlarda, özellikle polikistik over sendromunda (PKOS), gebelik şansına dolaylı katkı sağlayabilir. Doğrudan bir kısırlık tedavisi değiller ve gebelikte kullanılmazlar. Videoda ilacın gebelikten ne kadar önce bırakılacağını, korunmayı, yumurta toplama ve anesteziyi, erkeklerde bilinenleri de konuşuyoruz.

📖 Adet düzensizliği ve PKOS: https://tupbebek.com/makaleler/adet-duzensizligi-pcos/
📖 Beslenme, yaşam tarzı ve takviyeler: https://tupbebek.com/beslenme-yasam/
▶️ Tüp bebekte takviyeler işe yarar mı?: https://youtu.be/U8vAciGqvSU

⏱ Video İçeriği ve Zaman Damgaları:
{chapters}

❓ Hekiminize soracağınız üç soru:
1. Bu ilaca tıbben neden ihtiyacım var?
2. Gebelik denemesinden ne kadar önce bırakmalıyım, bu süreçte nasıl korunmalıyım?
3. Bu ilaç doğurganlık tedavimin takvimini nasıl etkiler?

📚 Videoda Anılan Bilimsel Kaynaklar:
- Zhou L ve ark. Effects of GLP1RAs on pregnancy rate and menstrual cyclicity in women with polycystic ovary syndrome: a meta-analysis and systematic review. BMC Endocr Disord, 2023. https://doi.org/10.1186/s12902-023-01500-5
- Wu YC ve ark. Impact of semaglutide pretreatment on reproductive outcomes in women with overweight and obesity with infertility: a real-world multicenter cohort study. Reprod Biol Endocrinol, 2026. https://doi.org/10.1186/s12958-026-01549-6
- Teede HJ ve ark. Uluslararası kanıta dayalı PKOS kılavuzu, 2023 (§ 5.3.1, § 5.9.1).
- EMA. Semaglutid (kilo yönetimi) kısa ürün bilgisi, § 4.6; Tirzepatid kısa ürün bilgisi (Birleşik Krallık), § 4.5–4.6.
- MHRA (Birleşik Krallık). GLP-1 ilaçları: bilmeniz gerekenler; Drug Safety Update, Ocak 2025 (anestezide aspirasyon).
- Lau KGY ve ark. Glucagon-Like Peptide-1 Receptor Agonists in Pregnancy: Periconception Exposure and Perinatal Outcomes. BJOG, 2026. https://doi.org/10.1111/1471-0528.70339
- Dao K ve ark. Use of GLP1 receptor agonists in early pregnancy and reproductive safety. BMJ Open, 2024. https://doi.org/10.1136/bmjopen-2023-083550
- Andersen E ve ark. Sperm count is increased by diet-induced weight loss and maintained by exercise or GLP-1 analogue treatment: a randomized controlled trial. Hum Reprod, 2022. https://doi.org/10.1093/humrep/deac096
- Peel A ve ark. The effect of obesity interventions on male fertility: a systematic review and meta-analysis. Hum Reprod Update, 2026. https://doi.org/10.1093/humupd/dmaf025

Dr. Senai Aksoy ile İletişime Geçin:

🩺 Randevu ve Bilgi İçin:
📞 Telefon & WhatsApp: +90 533 254 60 40
📧 E-posta: contact@draksoyivf.com
🌐 Web Sitesi: www.tupbebek.com

📍 Muayenehane Adresi:
Lotus Nişantaşı, Halaskargazi Mah., Halaskargazi Cad. No: 38-66, Kat 5, Ofis 92, Şişli / İstanbul

👇 Sosyal Medyada Bizi Takip Edin:
YouTube: https://www.youtube.com/@DocentDrSenaiAksoy
Instagram: @drsenaiaksoy

⚕️ ÖNEMLİ TIBBİ UYARI

Bu videoda sunulan bilgiler yalnızca eğitim ve bilgilendirme amaçlıdır. Bu içerik hiçbir koşulda tıbbi tavsiye, tanı veya kişiselleştirilmiş tedavi önerisi niteliği taşımamaktadır.

Her hastanın tıbbi durumu kendine özgüdür. Bu videoda ele alınan konular; bir hekim, kadın doğum uzmanı veya üreme tıbbı uzmanı ile yapılacak konsültasyonun yerini tutmaz.

Bu videodaki bilgilere dayanarak mevcut tedavinizi değiştirmeyin, yeni bir tedaviye başlamayın veya herhangi bir tıbbi karar almayın. Her türlü tıbbi karar öncesinde mutlaka aile hekiminize veya uzman doktorunuza danışınız.

Üreme sağlığınız veya IVF tedavi sürecinizle ilgili sorularınız için lütfen yetkili bir sağlık profesyoneline başvurunuz.

Videodaki stok görüntüler (Pexels) ve yapay zekâ ile üretilmiş görseller temsilidir; gerçek hasta görüntüsü değildir.

© Doç. Dr. Senai Aksoy — Tüm hakları saklıdır.

#tüpbebek #PKOS #kısırlık #GLP1 #drsenaiaksoy'''
tags = ['zayıflama iğnesi', 'zayıflama iğnesi gebelik', 'GLP-1', 'GLP-1 gebelik', 'semaglutid', 'tirzepatid', 'liraglutid',
        'PKOS', 'polikistik over sendromu', 'insülin direnci', 'kısırlık', 'infertilite', 'tüp bebek', 'gebelik planlama',
        'letrozol', 'kilo verme ve gebelik', 'dr senai aksoy', 'Senai Aksoy']
assert len(desc) < 5000 and len(title) <= 100 and sum(len(t) + 2 for t in tags) < 500
fix = {'video_id': '8ZtwHFtF0Io', 'title': title, 'description': desc, 'tags': tags, 'categoryId': '27',
       'defaultLanguage': 'tr', 'defaultAudioLanguage': 'tr'}
json.dump(fix, open(D / 'fixes-tr-metadata.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
(D / 'METADATA-TR.md').write_text(f'# 8ZtwHFtF0Io — metadata taslağı (onay için)\n\n## Başlık ({len(title)} karakter)\n{title}\n\n## Açıklama ({len(desc)} karakter)\n```\n{desc}\n```\n\n## Etiketler\n{", ".join(tags)}\n', encoding='utf-8')
print(title); print(chapters); print(len(desc), 'karakter')
