"""
YouTube Video Metadata Updater — Doç. Dr. Senai Aksoy Kanalı
YouTube Data API v3 ile video başlık, açıklama ve etiketlerini günceller.

Kullanım:
  1. Google Cloud Console'da OAuth 2.0 kurulumu yap (README.md'ye bak)
  2. client_secret.json dosyasını youtube-api/ klasörüne koy
  3. python youtube-api/update_metadata.py --dry-run   (önizleme)
  4. python youtube-api/update_metadata.py              (uygula)
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Google API imports
# ---------------------------------------------------------------------------
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("❌ Gerekli paketler yüklü değil. Şunu çalıştırın:")
    print("   pip install google-api-python-client google-auth-oauthlib")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Sabitler
# ---------------------------------------------------------------------------
SCOPES = ["https://www.googleapis.com/auth/youtube"]
API_SERVICE = "youtube"
API_VERSION = "v3"
CHANNEL_ID = "UCbO5qpAnmaQPBJlGMM9ITiw"

BASE_DIR = Path(__file__).resolve().parent
TOKEN_FILE = BASE_DIR / "token.json"
CLIENT_SECRET = BASE_DIR / "client_secret.json"
FIXES_FILE = BASE_DIR / "video_fixes.json"
LOG_FILE = BASE_DIR / "update_log.json"

# ---------------------------------------------------------------------------
# Standart Disclaimer (Format B — uzun)
# ---------------------------------------------------------------------------
DISCLAIMER = """⚕️ ÖNEMLİ TIBBİ UYARI
Bu videoda sunulan bilgiler yalnızca eğitim ve bilgilendirme amaçlıdır. Bu içerik hiçbir koşulda tıbbi tavsiye, tanı veya kişiselleştirilmiş tedavi önerisi niteliği taşımamaktadır.
Her hastanın tıbbi durumu kendine özgüdür. Bu videoda ele alınan konular; bir hekim, kadın doğum uzmanı veya üreme tıbbı uzmanı ile yapılacak konsültasyonun yerini tutmaz.
Bu videodaki bilgilere dayanarak mevcut tedavinizi değiştirmeyin, yeni bir tedaviye başlamayın veya herhangi bir tıbbi karar almayın. Her türlü tıbbi karar öncesinde mutlaka aile hekiminize veya uzman doktorunuza danışınız.
Üreme sağlığınız veya IVF tedavi sürecinizle ilgili sorularınız için lütfen yetkili bir sağlık profesyoneline başvurunuz.
© Doç. Dr. Senai Aksoy — Tüm hakları saklıdır."""

# ---------------------------------------------------------------------------
# İletişim bloğu
# ---------------------------------------------------------------------------
CONTACT_BLOCK = """Dr. Senai Aksoy ile İletişime Geçin:

🩺 Randevu ve Bilgi İçin:
📞 Telefon & WhatsApp: +90 533 254 60 40
📧 E-posta: contact@draksoyivf.com
🌐 Web Sitesi: www.tupbebek.com

📍 Muayenehane Adresi:
Lotus Nişantaşı, Halaskargazi Mah., Halaskargazi Cad. No: 38-66, Kat 5, Ofis 92, Şişli / İstanbul

👇 Sosyal Medyada Bizi Takip Edin:
YouTube: https://www.youtube.com/c/SenaiAksoy
Instagram: @drsenaiaksoy"""


# ═══════════════════════════════════════════════════════════════════════════
# Kimlik Doğrulama
# ═══════════════════════════════════════════════════════════════════════════
def authenticate():
    """OAuth 2.0 ile YouTube API'ye bağlan."""
    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Token yenileniyor...")
            creds.refresh(Request())
        else:
            if not CLIENT_SECRET.exists():
                print(f"❌ {CLIENT_SECRET} bulunamadı!")
                print("   Google Cloud Console'dan OAuth 2.0 istemci kimliği indirin.")
                print("   Detaylar: youtube-api/README.md")
                sys.exit(1)
            print("🔐 Tarayıcıda Google hesabınızla oturum açın...")
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES)
            creds = flow.run_local_server(port=8090, open_browser=True)

        TOKEN_FILE.write_text(creds.to_json())
        print("✅ Token kaydedildi:", TOKEN_FILE)

    return build(API_SERVICE, API_VERSION, credentials=creds)


# ═══════════════════════════════════════════════════════════════════════════
# Video Metadata Okuma
# ═══════════════════════════════════════════════════════════════════════════
def get_video(youtube, video_id: str) -> dict:
    """Tek bir videonun snippet bilgisini çek."""
    resp = youtube.videos().list(
        part="snippet,statistics",
        id=video_id
    ).execute()
    items = resp.get("items", [])
    if not items:
        raise ValueError(f"Video bulunamadı: {video_id}")
    return items[0]


def get_all_channel_videos(youtube) -> list[dict]:
    """Kanaldaki tüm videoları listele."""
    videos = []
    request = youtube.search().list(
        part="id",
        channelId=CHANNEL_ID,
        maxResults=50,
        order="date",
        type="video"
    )
    while request:
        resp = request.execute()
        for item in resp.get("items", []):
            vid = item["id"].get("videoId")
            if vid:
                videos.append(vid)
        request = youtube.search().list_next(request, resp)
    return videos


# ═══════════════════════════════════════════════════════════════════════════
# Video Metadata Güncelleme
# ═══════════════════════════════════════════════════════════════════════════
def update_video(youtube, video_id: str, fix: dict, dry_run: bool = True) -> dict:
    """
    Bir videonun metadata'sını güncelle.

    fix dict yapısı:
    {
      "video_id": "abc123",
      "title": "Yeni Başlık",               # null → değiştirme
      "description_hook": "İlk 2 satır...",  # null → değiştirme
      "hashtags": ["#tüpbebek", "#ivf"],     # null → değiştirme
      "tags": ["tüp bebek", "ivf"]           # null → değiştirme
    }
    """
    current = get_video(youtube, video_id)
    snippet = current["snippet"]
    changes = {}

    # --- Başlık ---
    new_title = fix.get("title")
    if new_title and new_title != snippet["title"]:
        changes["title"] = {"old": snippet["title"], "new": new_title}
        snippet["title"] = new_title

    # --- Açıklama (hook + hashtag) ---
    current_desc = snippet.get("description", "")
    new_desc = current_desc

    # Hook değişimi: ilk paragrafı (timestamp öncesi) değiştir
    hook = fix.get("description_hook")
    if hook:
        new_desc = _replace_hook(current_desc, hook)

    # Hashtag ekleme: açıklama sonuna
    hashtags = fix.get("hashtags")
    if hashtags:
        new_desc = _ensure_hashtags(new_desc, hashtags)

    # Disclaimer standardizasyonu
    if fix.get("standardize_disclaimer", False):
        new_desc = _standardize_disclaimer(new_desc)

    if new_desc != current_desc:
        changes["description"] = {
            "old_first_200": current_desc[:200],
            "new_first_200": new_desc[:200],
            "old_length": len(current_desc),
            "new_length": len(new_desc)
        }
        snippet["description"] = new_desc

    # --- Tags ---
    new_tags = fix.get("tags")
    if new_tags:
        old_tags = snippet.get("tags", [])
        merged = list(dict.fromkeys(old_tags + new_tags))  # dedupe, preserve order
        if merged != old_tags:
            changes["tags"] = {"old": old_tags, "new": merged}
            snippet["tags"] = merged

    if not changes:
        print(f"  ⏭️  {video_id}: Değişiklik yok")
        return {"video_id": video_id, "status": "no_change"}

    # --- Rapor ---
    print(f"\n  📝 {video_id}:")
    for key, val in changes.items():
        if key == "title":
            print(f"     Başlık: \"{val['old'][:60]}...\"")
            print(f"          → \"{val['new'][:60]}\"")
        elif key == "description":
            print(f"     Açıklama: {val['old_length']} → {val['new_length']} karakter")
            print(f"     Hook: \"{val['new_first_200'][:100]}...\"")
        elif key == "tags":
            added = set(val["new"]) - set(val["old"])
            if added:
                print(f"     Tag eklendi: {', '.join(added)}")

    if dry_run:
        print(f"     🔍 DRY RUN — güncelleme yapılmadı")
        return {"video_id": video_id, "status": "dry_run", "changes": changes}

    # --- Gerçek güncelleme ---
    try:
        youtube.videos().update(
            part="snippet",
            body={
                "id": video_id,
                "snippet": {
                    "title": snippet["title"],
                    "description": snippet["description"],
                    "tags": snippet.get("tags", []),
                    "categoryId": snippet.get("categoryId", "26"),  # 26 = Howto & Style
                }
            }
        ).execute()
        print(f"     ✅ Güncellendi!")
        return {"video_id": video_id, "status": "updated", "changes": changes}
    except HttpError as e:
        print(f"     ❌ Hata: {e}")
        return {"video_id": video_id, "status": "error", "error": str(e)}


# ═══════════════════════════════════════════════════════════════════════════
# Açıklama Yardımcıları
# ═══════════════════════════════════════════════════════════════════════════
def _replace_hook(desc: str, hook: str) -> str:
    """
    Açıklamanın ilk kısmını (timestamps veya bölümler başlamadan önceki metin)
    yeni hook ile değiştir. Timestamps'i korur.
    """
    lines = desc.split("\n")
    # İlk timestamp satırını bul
    ts_start = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if (stripped and len(stripped) > 2 and
            (stripped[0].isdigit() and ":" in stripped[:5]) or
            stripped.startswith("⏱") or
            stripped.startswith("00:") or
            stripped.startswith("0:")):
            ts_start = i
            break

    if ts_start is not None and ts_start > 0:
        # Hook + boş satır + timestamp bloğundan itibaren geri kalan
        remaining = "\n".join(lines[ts_start:])
        return hook.rstrip() + "\n\n" + remaining
    elif ts_start == 0:
        # İlk satır timestamp — hook'u başa ekle
        return hook.rstrip() + "\n\n" + desc
    else:
        # Timestamp yok — ilk paragrafı değiştir
        # Çift newline'a kadar olan kısım = ilk paragraf
        parts = desc.split("\n\n", 1)
        if len(parts) > 1:
            return hook.rstrip() + "\n\n" + parts[1]
        return hook.rstrip() + "\n\n" + desc


def _ensure_hashtags(desc: str, hashtags: list[str]) -> str:
    """Açıklamada hashtag yoksa sona ekle. Varsa dokunma."""
    existing_tags = [w for w in desc.split() if w.startswith("#")]
    if len(existing_tags) >= 3:
        return desc  # Zaten yeterli hashtag var

    tag_line = " ".join(hashtags)

    # Disclaimer'dan önce mi, sonra mı? → Disclaimer'dan ÖNCE
    disclaimer_markers = ["⚕️ ÖNEMLİ", "TIBBİ UYARI", "*Bu videodaki bilgiler"]
    for marker in disclaimer_markers:
        idx = desc.find(marker)
        if idx > 0:
            before = desc[:idx].rstrip()
            after = desc[idx:]
            return before + "\n\n" + tag_line + "\n\n" + after

    # Disclaimer bulunamadı → en sona ekle
    return desc.rstrip() + "\n\n" + tag_line


def _standardize_disclaimer(desc: str) -> str:
    """Kısa disclaimer'ı uzun Format B ile değiştir."""
    short_marker = "*Bu videodaki bilgiler yalnızca genel bilgilendirme amaçlıdır"
    if short_marker in desc:
        # Kısa disclaimer bloğunu bul ve değiştir
        idx = desc.find(short_marker)
        # Satır sonunu bul
        end = desc.find("\n---", idx)
        if end == -1:
            end = len(desc)
        else:
            end += 4  # "---" dahil
        old_block = desc[idx:end]
        return desc.replace(old_block, DISCLAIMER)
    return desc


# ═══════════════════════════════════════════════════════════════════════════
# Ana Çalışma
# ═══════════════════════════════════════════════════════════════════════════
def load_fixes() -> list[dict]:
    """video_fixes.json dosyasından düzeltmeleri yükle."""
    if not FIXES_FILE.exists():
        print(f"❌ {FIXES_FILE} bulunamadı!")
        sys.exit(1)
    with open(FIXES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="YouTube video metadata güncelleyici")
    parser.add_argument("--dry-run", action="store_true", default=False,
                        help="Değişiklikleri göster ama uygulamama (önizleme)")
    parser.add_argument("--video", type=str, default=None,
                        help="Sadece belirtilen video ID'yi güncelle")
    parser.add_argument("--list", action="store_true", default=False,
                        help="Kanal videolarını listele")
    parser.add_argument("--backup", action="store_true", default=False,
                        help="Güncellemeden önce mevcut metadata'yı yedekle")
    args = parser.parse_args()

    print("=" * 60)
    print("  YouTube Metadata Updater — Dr. Senai Aksoy")
    print("=" * 60)

    youtube = authenticate()
    print("✅ YouTube API bağlantısı kuruldu\n")

    # --- Liste modu ---
    if args.list:
        print("📋 Kanal videoları:")
        video_ids = get_all_channel_videos(youtube)
        for vid in video_ids:
            info = get_video(youtube, vid)
            title = info["snippet"]["title"]
            views = info["statistics"].get("viewCount", "?")
            print(f"  {vid}  |  {views:>6} view  |  {title[:60]}")
        return

    # --- Düzeltmeleri yükle ---
    fixes = load_fixes()
    if args.video:
        fixes = [f for f in fixes if f["video_id"] == args.video]
        if not fixes:
            print(f"❌ video_fixes.json'da {args.video} bulunamadı")
            return

    print(f"📦 {len(fixes)} video güncellenecek")
    if args.dry_run:
        print("🔍 DRY RUN modu — değişiklikler UYGULANMAYACAK\n")
    else:
        print("⚡ CANLI mod — değişiklikler UYGULANACAK\n")
        confirm = input("Devam etmek istiyor musunuz? (evet/hayır): ").strip().lower()
        if confirm not in ("evet", "e", "yes", "y"):
            print("İptal edildi.")
            return

    # --- Backup ---
    if args.backup or not args.dry_run:
        backup_file = BASE_DIR / f"backup_{int(time.time())}.json"
        backups = []
        print("💾 Yedekleniyor...")
        for fix in fixes:
            try:
                vid_data = get_video(youtube, fix["video_id"])
                backups.append({
                    "video_id": fix["video_id"],
                    "snippet": vid_data["snippet"]
                })
            except Exception as e:
                print(f"  ⚠️ Yedek alınamadı {fix['video_id']}: {e}")
        with open(backup_file, "w", encoding="utf-8") as f:
            json.dump(backups, f, ensure_ascii=False, indent=2)
        print(f"✅ Yedek: {backup_file}\n")

    # --- Güncelle ---
    results = []
    for fix in fixes:
        result = update_video(youtube, fix["video_id"], fix, dry_run=args.dry_run)
        results.append(result)
        if not args.dry_run:
            time.sleep(1)  # API rate limit'e saygı

    # --- Log ---
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # --- Özet ---
    print("\n" + "=" * 60)
    updated = sum(1 for r in results if r["status"] == "updated")
    dry = sum(1 for r in results if r["status"] == "dry_run")
    no_change = sum(1 for r in results if r["status"] == "no_change")
    errors = sum(1 for r in results if r["status"] == "error")
    print(f"  ✅ Güncellendi: {updated}")
    print(f"  🔍 Dry run: {dry}")
    print(f"  ⏭️  Değişiklik yok: {no_change}")
    print(f"  ❌ Hata: {errors}")
    print(f"  📄 Log: {LOG_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    main()
