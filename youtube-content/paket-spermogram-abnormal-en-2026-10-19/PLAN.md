# Abnormal Semen Analysis — EN yayın paketi (@DrAksoyFertility) · 2026-10-19

Video: **TluWIqqgQiw** (`C:\Users\KC3\Downloads\spermogram-EN-motion-4k.mp4` · 10:42 · 4K30 · 19.260 kare · 1,70 GB · −14,1 LUFS).
Kurgu: Outsider Inside EN recut (`D:\A-klasör\openmontage\projects\2026-10-19-spermogram-abnormal-en-recut`, rapor `final\KALITE-KONTROL-EN.md`): 27 kaynaklı grafik, 6 AI espri klibi (ILLUSTRATION), LatentSync dudak senkronu, bitiş ekranı 10:22–10:42.
Eski düz dublaj (`spermogram-EN-dub-4K.mp4`, 10:33) yerine bu dosya yüklenir. Zaman çizelgesi aynı olduğu için bölümler ve EN altyazı geçerli; video yalnızca sonda 9,9 sn sessiz kâğıt kuyruğuyla uzadı.
Kanal canlı doğrulandı (2026-10-19): `UCo3ZeBXk0ng-OigXd9jqJqQ` · "Dr. Aksoy — Fertility, No Hype" · @draksoyfertility · 6 video.
Ses kararı (2026-10-19, Dr. Aksoy): dublaj olduğu gibi kalıyor; FR kayıttan farklı 7 iddia için bkz. `EN-vs-FR-iddia-farklari.md`. Açıklama ve ekran metinleri bu iddiaları tekrar etmiyor.

## 1. Yükleme (Studio, elle — API upload betiği yok, 1,7 GB)
Studio → @DrAksoyFertility seçili olduğunu kontrol et → Oluştur → Video yükle → dosya → **Özel** olarak kaydet. Başlık geçici olabilir; metadata API ile yazılacak.
Studio'da elle: Çocuklara özel değil · Ücretli tanıtım: Hayır · Değiştirilmiş/sentetik içerik: **Evet** önerilir (AI ses klonu + dudak senkronu + 6 AI klip; açıklamada beyan var).

## 2. API ile (2026-10-20 uygulandı ve doğrulandı — `TluWIqqgQiw`)
| İş | Dosya / değer |
|---|---|
| Başlık | Abnormal Semen Analysis: Does It Mean You're Infertile? (55 karakter) |
| Açıklama | `description.en.txt` — 13 bölüm, WHO 2021 değerleri + NICE yol haritası, 3 soru, acil uyarısı (911/999/112), 9 kaynak, beyan: AI dublaj + dudak senkronu + ILLUSTRATION klipleri |
| Etiketler / dil | 18 etiket · kategori 27 · en-US / en-US (`fixes-metadata.json`, `VIDEO_ID` yer tutucu) |
| EN altyazı | `spermogram-abnormal.en.srt` — 172 cue, satır ≤ 42 karakter, metin scriptten birebir, zamanlar large-v3 ASR'den (script↔ASR uyumu %97,7). Bölüm saatleri bu zamanlardan alındı |
| Kapak | `en-thumb-spermogram-A.jpg` (BELOW NORMAL = INFERTILE? · SEMEN ANALYSIS), FR A kapağının taban görseli |
| Oynatma listesi | "IVF & Fertility: Evidence Explained" (mevcut) — ya da yeni "Male Infertility" listesi (karar) |
| Yayın | **Çarşamba 2026-11-04 16:00 UTC** (17:00 Paris, 19:00 TSİ, 11:00 New York) |

Neden 4 Kasım: EN uzun videolar Çarşamba 16:00 UTC (21 Eki queLygimeS8, 28 Eki Q7aCrXhG_E8). GLP-1 EN Shorts 29 ve 31 Ekim'de. FR spermogramme 3 Kasım'da çıkıyor; EN bir gün sonra.

## 3. Studio'da elle (API yapamıyor)
- **Bitiş ekranı 10:22–10:42**: öğeleri videodaki boş yuvalara oturt (sol üst ve sol alt video, sağda abone). Öneri: sol üst "IVF Supplements: What Really Helps?" (2hjpsL0bwhM), sol alt "How Many Eggs Should You Freeze?" (J21RLRUE1g8) ya da "En iyi eşleşme". Sesin söz ettiği sperm kalitesi videosu EN kanalda yok. Yeni kanalda "belirli video seç" listesi daha önce boş geliyordu.

## QC (2026-10-19, qa_final.py, motion final)
3840×2160 30 fps · 19.260 kare = beklenen · video ve ses 0'dan başlıyor, ikisi de 642,000 sn · çözme hatası 0 · siyah 0 · donmaların hepsi duran kâğıt sahneler · −14,1 LUFS, true peak −3,0 dBFS, stereo AAC 320k · yüz %21,7 · en uzun görselsiz konuşma 23 sn. Ayrıntı: `KALITE-KONTROL-EN.md`.

## Gözle ve kulakla kontrol
- Dudak senkronu, yüz bölümündeki jump cut'lar: 0:12,2 · 4:25,8 · 4:31,2 · 5:49,0 · 5:53,0 · 5:56,7 · 6:46,2 · 7:07,2 · 7:48,9 · 7:52,0 · 9:52,5 · 10:15,9.
- ASR şu kelimeleri iki kez duydu; ikinci kopya 0,1–0,2 sn, büyük olasılıkla ASR hatası: 1:45 "calls" · 3:33 "declaring" · 5:43 "Thousands" · 6:10 "July" · 7:31 "sperm". Ayrıca 8:51 "slow… low".

## Açık konular
- Ses ↔ ekran farkı (bilerek): 6:58 "the average" ↔ "Both, read with your medical history"; 8:09 "one out of two" ↔ ≈ 45%.
- Sesin "on screen" dediği değerler (4:03) ve eşikler (8:19) artık ekranda; açıklamada da duruyor.
