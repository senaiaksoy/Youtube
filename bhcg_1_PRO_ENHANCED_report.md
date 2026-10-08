# bhcg_1 görüntü iyileştirme raporu

## Kaynak ve yol doğrulaması

- İstekte verilen `C:\Users\KC3\Downloads\bhcg\_1.mp4` yolu mevcut değildi.
- Aynı Downloads klasöründeki 13:34.933 süreli güçlü eşleşme `C:\Users\KC3\Downloads\bhcg_1.mp4` kaynak olarak kullanıldı.
- Kaynak dosya değiştirilmedi veya üzerine yazılmadı.

## Kaynak ffprobe özeti

- Süre: 814.933333 saniye (13:34.933)
- Video: H.264 Main, 3840x2160, 30/1 fps, 24.448 kare
- Video bit hızı: 78.986976 Mb/sn
- Piksel biçimi / bit derinliği: yuv420p, 8-bit
- Color range / primaries / transfer / matrix: kaynak dosyada belirtilmemiş
- Ses: AAC-LC, 48 kHz, stereo, 317.368 kb/sn
- Toplam dosya bit hızı: 79.308158 Mb/sn
- Boyut: 8.078.857.749 bayt

## Görsel değerlendirme

Başlangıç, yaklaşık %25, %50, %75 ve son bölümden kareler incelendi.

- White balance ve ten rengi video boyunca tutarlı ve doğalydı; white balance düzeltmesi uygulanmadı.
- Görüntü hafif parlak/düz webcam karakterindeydi; beyaz duvar ve gömlek ayrıntıları korunuyordu.
- Belirgin gürültü görülmedi; ayrıntı kaybını önlemek için noise reduction uygulanmadı.
- Hafif dijital kenar sertliği vardı; yalnızca çok düşük negatif luma unsharp uygulandı.
- AI face enhancement, beauty filter, skin smoothing, LUT, vignette, blur, upscale veya frame interpolation kullanılmadı.

## FFmpeg filter chain

```text
eq=contrast=1.035:brightness=-0.012:saturation=0.99:gamma=1.0,
unsharp=luma_msize_x=5:luma_msize_y=5:luma_amount=-0.08:chroma_msize_x=5:chroma_msize_y=5:chroma_amount=0.0,
setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=limited
```

Gerekçe:

- `contrast=1.035`: çok hafif tonal derinlik.
- `brightness=-0.012`: parlak webcam görünümünü küçük ölçüde kontrol etme.
- `saturation=0.99`: ten ve tablodaki renkleri aşırı doygunlaştırmadan koruma.
- `unsharp ... luma_amount=-0.08`: halo/kenar sertliğini çok hafif azaltma; yüz rekonstrüksiyonu veya cilt yumuşatma değildir.
- `setparams`: kaynakta eksik olan SDR HD renk etiketlerini finalde açık Rec.709 limited range olarak yazma.

## Önizleme kalite kontrolü

- Orta bölümden 20 saniyelik 4K önizleme üretildi.
- Orijinal/işlenmiş kareler karşılaştırıldı.
- Ten rengi, yüz benzerliği, saç/sakal ayrıntısı ve gömlek dokusu korundu.
- Highlight clipping, plastik cilt, belirgin banding veya aşırı kontrast görülmedi.
- İşlem belirgin bir efekt gibi görünmediği için aynı zincir finale uygulandı.

## Final encode ayarları

- Video: libx264, H.264 High Profile
- Çözünürlük: 3840x2160 (korundu)
- Kare hızı: 30 fps CFR (korundu)
- Kare sayısı: 24.448 (korundu)
- Piksel biçimi: yuv420p, 8-bit
- Kalite: CRF 17
- Preset: slow
- Renk: Rec.709 SDR, limited range
- MP4: `+faststart`
- Ses: `-c:a copy`; hiçbir ses filtresi veya yeniden kodlama yok
- Kurgu: kesme, boşluk kaldırma, zoom, altyazı, logo, müzik ve transition yok

## Final ffprobe ve bütünlük doğrulaması

- Süre: 814.933333 saniye (kaynakla tam eşit)
- Video: H.264 High, 3840x2160, 30/1 fps, 24.448 kare
- Video bit hızı: 32.165256 Mb/sn
- Toplam bit hızı: 32.491454 Mb/sn
- Renk etiketleri: tv / bt709 / bt709 / bt709
- Ses: AAC-LC, 48 kHz, stereo, 317.368 kb/sn
- Boyut: 3.309.796.147 bayt
- Kaynak ses paket SHA-256: `7c0709608223453f08a9a6d95b05c4fbe043a3a1be33468c9d5a379383cf3d87`
- Final ses paket SHA-256: `7c0709608223453f08a9a6d95b05c4fbe043a3a1be33468c9d5a379383cf3d87`
- Ses paket hash'leri birebir eşit: stream-copy doğrulandı.
- Final dosya SHA-256: `A7ECEA2C64041AA4C9B7385276901C18B7496C0531A26F60AE5B0C6AB509A956`

## Çıktı

- Final: `D:\A-klasör\Youtube\bhcg_1_PRO_ENHANCED.mp4`
- Rapor: `D:\A-klasör\Youtube\bhcg_1_PRO_ENHANCED_report.md`

