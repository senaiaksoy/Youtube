# YouTube Data API v3 — Kurulum Rehberi

Bu araç, YouTube video başlıklarını, açıklamalarını ve etiketlerini
programatik olarak günceller.

## Ön Koşullar

- Python 3.10+
- Google hesabı (YouTube kanalının sahibi)

## 1. Google Cloud Console Kurulumu

### 1.1 Proje Oluştur
1. https://console.cloud.google.com adresine git
2. Üst menüden **"Select a project"** → **"New Project"**
3. Proje adı: `youtube-metadata-updater`
4. **Create** tıkla

### 1.2 YouTube Data API v3'ü Etkinleştir
1. Sol menü → **APIs & Services** → **Library**
2. "YouTube Data API v3" ara
3. **Enable** tıkla

### 1.3 OAuth 2.0 Kimlik Bilgisi Oluştur
1. Sol menü → **APIs & Services** → **Credentials**
2. **+ Create Credentials** → **OAuth client ID**
3. İlk kez yapıyorsan "Configure Consent Screen" isteyecek:
   - **User Type:** External → Create
   - **App name:** YouTube Metadata Updater
   - **User support email:** kendi e-postan
   - **Developer contact:** kendi e-postan
   - Scopes: Skip (boş bırak)
   - **Test users:** kendi Google hesabını ekle ← ÖNEMLİ
   - Save
4. Tekrar **Credentials** → **+ Create Credentials** → **OAuth client ID**
   - Application type: **Desktop app**
   - Name: `yt-updater`
   - **Create**
5. **Download JSON** tıkla → dosyayı `youtube-api/client_secret.json` olarak kaydet

> ⚠️ `client_secret.json` dosyasını Git'e commit ETME!

### 1.4 Test Kullanıcısı Ekleme
Consent screen "Testing" modundayken sadece test kullanıcıları oturum açabilir.
**APIs & Services → OAuth consent screen → Test users → Add Users** ile 
YouTube kanalınızın bağlı olduğu Google hesabını ekle.

## 2. Python Bağımlılıkları

```bash
pip install google-api-python-client google-auth-oauthlib
```

## 3. Kullanım

### Önizleme (DRY RUN — hiçbir şey değişmez)
```bash
python youtube-api/update_metadata.py --dry-run
```

### Videoları Listele
```bash
python youtube-api/update_metadata.py --list
```

### Tek Video Güncelle
```bash
python youtube-api/update_metadata.py --video b8wT1pAbX3A --dry-run
python youtube-api/update_metadata.py --video b8wT1pAbX3A
```

### Tüm Videoları Güncelle
```bash
python youtube-api/update_metadata.py
```
Onay isteyecek → `evet` yaz → otomatik yedek alır → günceller.

## 4. Dosya Yapısı

```
youtube-api/
├── README.md                  ← Bu dosya
├── client_secret.json         ← Google OAuth kimliği (GIT'E EKLEME!)
├── client_secret.json.example ← Örnek yapı
├── token.json                 ← Otomatik oluşur (GIT'E EKLEME!)
├── update_metadata.py         ← Ana script
├── video_fixes.json           ← Düzeltme tanımları
├── update_log.json            ← Son çalışma logu
└── backup_*.json              ← Otomatik yedekler
```

## 5. video_fixes.json Yapısı

```json
{
  "video_id": "abc123",
  "title": "Yeni Başlık",              // null → başlığı değiştirme
  "description_hook": "İlk 2 satır",   // null → hook değiştirme
  "hashtags": ["#tag1", "#tag2"],       // null → hashtag ekleme
  "tags": ["etiket1", "etiket2"],       // null → tag ekleme
  "standardize_disclaimer": true        // kısa disclaimer'ı uzun ile değiştir
}
```

## 6. Güvenlik Notları

- `client_secret.json` ve `token.json` dosyalarını asla paylaşma
- Script yalnızca `snippet` (başlık, açıklama, etiket) günceller — video içeriğine dokunmaz
- Her güncelleme öncesi otomatik yedek alınır (`backup_*.json`)
- YouTube API günlük kotası: 10.000 birim. Her `videos.update` = 50 birim. 15 video ≈ 750 birim.

## 7. Sorun Giderme

| Hata | Çözüm |
|------|-------|
| `client_secret.json bulunamadı` | Cloud Console'dan indirdiğin JSON'u `youtube-api/` klasörüne koy |
| `Access blocked: app not verified` | Consent Screen → Test Users'a hesabını ekle |
| `403: forbidden` | API etkinleştirilmemiş veya yanlış hesapla giriş yapılmış |
| `quota exceeded` | Günlük 10.000 birim kotası dolmuş. Yarın tekrar dene |
| `invalid_grant` | `token.json` sil, tekrar oturum aç |
