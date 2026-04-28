---
type: readme
domain: youtube-patient-responses
owner: Dr. Senai Aksoy
created: 2026-04-24
---

# YouTube Hasta Cevap Sistemi

Bu klasör, YouTube kanalınıza gelen hasta yorumlarına hızlı, profesyonel ve hukuki açıdan güvenli cevap vermek için kullanılır.

## Klasör Yapısı

```
youtube-responses/
├── README.md                ← bu dosya
├── editorial-rules.md       ← AI'ın takip ettiği kurallar
├── disclaimer.md            ← 4 dilde sabit disclaimer
├── templates/               ← 12 kategori şablonu (TR/FR/EN/AR)
│   ├── 01-genel.md
│   ├── 02-hamile-kalamiyorum.md
│   ├── 03-tup-bebek-gerekir-mi.md
│   ├── 04-amh-dusuk.md
│   ├── 05-tupler-kapali.md
│   ├── 06-embriyo-kalitesi.md
│   ├── 07-transfer-sonrasi.md
│   ├── 08-tekrarlayan-basarisizlik.md
│   ├── 09-kisa-guvenli.md
│   ├── 10-erkek-faktoru.md
│   ├── 11-pcos.md
│   └── 12-endometriozis.md
└── archive/                 ← gönderilmiş cevaplar (YYYY-MM/ altında)
```

## Kullanım Workflow'u

### 1. Manuel kullanım (Obsidian içinden)
- Hasta yorumunu oku
- Uygun şablonu `templates/` klasöründen aç
- Dili seç (TR/FR/EN/AR)
- Kişisel dokunuş ekle (%30)
- YouTube Studio'ya yapıştır
- `archive/YYYY-MM/` klasörüne kaydet

### 2. AI destekli kullanım (React uygulaması)
- YouTube Studio yanında uygulamayı aç
- Yorumu yapıştır → AI kategoriyi tespit eder
- Dili seç → AI ilgili şablonu kişiselleştirir
- Kopyala → YouTube'a yapıştır
- "Arşivle" butonu → Obsidian vault'a markdown olarak indir
- Dosyayı `archive/YYYY-MM/` klasörüne sürükle

## Arşiv İsimlendirme

Format: `YYYY-MM-DD-kategori-videoid-kisaaciklama.md`

Örnek: `2026-04-24-04-amh-dusuk-xyz123-amh-0.8-36yas.md`

## Editoryal Güncelleme

Şablonlar düzenli güncellenir. Değişiklik olduğunda:
1. İlgili şablonun `updated:` tarihini değiştir
2. Git commit mesajında neyin değiştiğini belirt
3. CLAUDE.md'de değişiklik olursa AI davranışı da güncellenir

## Hukuki Notlar

- Türkiye Sağlık Bakanlığı R.G. 12.11.2025 reklam kurallarına uygun
- TTB etik kurallarına uygun
- Draksoyivf.com (uluslararası) ve senaiaksoy.net (Türkiye) standartlarıyla tutarlı
- Hiçbir cevap kesin teşhis veya tedavi önerisi içermez
- Her cevap muayeneye/uzman görüşüne yönlendirir
