 # YouTube Manager

YouTube kanalını yönetmek için Next.js 14 + TypeScript uygulaması. Google OAuth 2.0, otomatik token yenileme ve canlı ilerleme takibi ile çoklu dil çeviri yönetimi içerir.

## ✨ Özellikler

- 📊 **Dashboard** — Kanal istatistikleri, en çok izlenen videolar, animasyonlu sayaçlar
- 🎥 **Video Yönetimi** — Video listesi, arama, inline düzenleme (başlık / açıklama / gizlilik)
- 🌐 **Toplu Çeviri (Canlı İlerleme)** — NDJSON streaming ile her video için anlık durum takibi
- 🔐 **Google OAuth 2.0** — Refresh token ile otomatik yenileme
- 🎨 **Modern UI** — TailwindCSS + shadcn/ui + Framer Motion, Türkçe arayüz

## 🛠 Teknoloji

- Next.js 14 (App Router)
- TypeScript
- TailwindCSS + shadcn/ui
- Framer Motion
- Lucide icons
- NDJSON streaming API
- Google OAuth 2.0 + YouTube Data API v3

## � Masaüstü Uygulaması (Electron)

### Hazır `.exe` ile kurulum (yeni bilgisayar)

Eğer elinde hazır `YouTube Manager Setup 1.0.0.exe` ve `.env` dosyası varsa:

1. **`YouTube Manager Setup 1.0.0.exe`** → çift tıkla → kurulumu tamamla
2. Explorer adres çubuğuna `%APPDATA%\youtube-manager` yaz → Enter
3. **`.env`** dosyasını bu klasöre kopyala
4. Masaüstündeki **YouTube Manager** kısayoluna tıkla
5. **"Google ile Bağlan"** → Google hesabınla giriş yap → izinleri kabul et
6. Uygulama hazır!

> **Not:** "This app isn't verified" uyarısı çıkarsa: **Advanced → Go to YouTube Manager (unsafe)** tıkla. Bu senin kendi uygulamanın.

### Sıfırdan kurulum (kaynak koddan)

#### 1. Gereksinimler

- [Node.js v20+](https://nodejs.org/)
- [Git](https://git-scm.com/)
- Yarn (Node.js kurulumundan sonra: `corepack enable`)

#### 2. Google OAuth Credentials oluştur

1. [Google Cloud Console](https://console.cloud.google.com/apis/credentials) → yeni proje oluştur
2. **APIs & Services → Library** → şu API'leri aktif et:
   - **YouTube Data API v3**
   - **YouTube Analytics API**
3. **APIs & Services → Credentials → Create Credentials → OAuth client ID** → *Web application*
4. **Authorized redirect URIs** listesine ekle:
   ```
   http://localhost:3000/api/auth/google/callback
   ```
5. Client ID ve Client Secret'ı kaydet
6. **OAuth consent screen → Audience → Test users** → kendi Gmail adresini ekle

#### 3. Projeyi klonla ve bağımlılıkları yükle

```bash
git clone https://github.com/senaiaksoy/Youtube.git
cd Youtube
yarn install
```

#### 4. `.env` dosyası oluştur

`.env.example` dosyasını kopyalayıp kendi değerlerini yaz:

```bash
cp .env.example .env
```

`.env` içeriği:
```
YOUTUBE_CHANNEL_ID=UCXXXXXXXXXXXXXX
GOOGLE_CLIENT_ID=XXXXXXXX.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-XXXXX
```

#### 5. Geliştirme modunda çalıştır

```bash
yarn desktop:dev
```

Electron penceresi açılır → **Google ile Bağlan** → Google hesabınla yetki ver.

#### 6. `.exe` installer oluştur

```bash
yarn desktop:dist
```

Çıktı: `dist-electron/YouTube Manager Setup X.X.X.exe`

### Web modunda çalıştırma (opsiyonel)

```bash
yarn dev          # development
yarn build        # production build
yarn start        # production server
```

http://localhost:3000 adresini aç.

## 📁 Dizin Yapısı

```
nextjs_space/
├── app/
│   ├── api/
│   │   ├── auth/google/         # OAuth akışı (authorize + callback + status + disconnect)
│   │   └── youtube/             # YouTube API proxy endpoint'leri
│   │       ├── videos/          # Video listesi
│   │       ├── video/[id]/      # Video update (PUT)
│   │       ├── translations/    # Streaming translations (POST/DELETE)
│   │       └── analytics/       # Kanal stats + top videos
│   ├── layout.tsx
│   └── page.tsx
├── components/
│   ├── app-shell.tsx            # Ana layout + tab navigation
│   ├── auth-banner.tsx          # OAuth durum bandı
│   ├── translation-progress.tsx # Canlı ilerleme modalı (streaming UI)
│   ├── tabs/
│   │   ├── dashboard-tab.tsx
│   │   ├── videos-tab.tsx
│   │   └── translations-tab.tsx
│   └── ui/                      # shadcn/ui componentleri
├── lib/
│   ├── youtube-token.ts         # OAuth + refresh token + youtubeApiFetch helper
│   ├── languages.ts             # 40 desteklenen dil tanımı
│   └── utils.ts
└── .env                         # (gitignore'da — commit etme!)
```

## ⚠️ Önemli Notlar

- `data/google-tokens.json` dosyası **gitignore'da** — kullanıcı OAuth token'larını içerir, asla commit edilmemelidir.
- `.env` dosyası **gitignore'da** — Client ID / Secret içerir.
- Production'a deploy ederken redirect URI'yi Google Console'daki OAuth ayarlarına eklemeyi unutma.
- `YOUTUBE_CHANNEL_ID` değeri kendi kanalınızın ID'si olmalı (YouTube Studio → Settings → Channel → Advanced).

## 🧪 API Uç Noktaları

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| GET | `/api/auth/google` | OAuth başlatma (redirect to Google) |
| GET | `/api/auth/google/callback` | OAuth callback — tokenleri kaydeder |
| GET | `/api/auth/status` | Bağlantı durumu |
| POST | `/api/auth/disconnect` | Hesabı ayır (tokenleri sil) |
| GET | `/api/youtube/analytics` | Kanal istatistikleri + top videolar |
| GET | `/api/youtube/videos` | Video listesi (search + pagination destekli) |
| PUT | `/api/youtube/video/[id]` | Video güncelle |
| POST | `/api/youtube/translations` | Toplu çeviri ekle (NDJSON stream) |
| DELETE | `/api/youtube/translations` | Çeviri sil |

## Lisans

MIT
