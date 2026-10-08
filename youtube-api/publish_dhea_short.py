"""DHEA Short'unu @docentdrsenaiaksoy kanalına yükler (public).
Token: token.json (doğrulandı: UCbO5... = @docentdrsenaiaksoy)."""
import sys
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

BASE = Path(__file__).resolve().parent
TOKEN = BASE / "token.json"
VIDEO = Path(r"D:/A-klasör/Youtube/remotion-graphics/out/dhea-short.mp4")
SCOPES = ["https://www.googleapis.com/auth/youtube"]

EXPECTED_CHANNEL = "UCbO5qpAnmaQPBJlGMM9ITiw"  # @docentdrsenaiaksoy

TITLE = "Tüp bebekte DHEA ve büyüme hormonu gerçekten gerekli mi?"
DESCRIPTION = (
    "Düşük yumurta rezervi öğrendiğinizde her yerde iki isim çıkar: DHEA ve büyüme hormonu. "
    "Forumlarda \"mucize\", kliniklerde otomatik reçete… Peki gerçekten gerekli mi, yoksa pazarlama mı? "
    "Doç. Dr. Senai Aksoy 55 saniyede özetliyor.\n\n"
    "⚠️ Bilgilendirme amaçlıdır; bireysel tıbbi değerlendirmenin yerine geçmez.\n"
    "🌐 tupbebek.com\n\n"
    "#tüpbebek #DHEA #büyümehormonu #yumurtarezervi #infertilite #kısırlık #FIV #drsenaiaksoy #Shorts"
)
TAGS = ["tüp bebek", "DHEA", "büyüme hormonu", "yumurta rezervi", "düşük yumurta rezervi",
        "infertilite", "kısırlık", "FIV", "tüp bebek tedavisi", "Senai Aksoy"]
CATEGORY_ID = "27"  # Education

def main():
    if not VIDEO.exists():
        print(f"HATA: video yok: {VIDEO}"); sys.exit(1)
    creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)
    yt = build("youtube", "v3", credentials=creds)

    # GÜVENLİK: yüklemeden önce token'ın kanalını doğrula
    ch = yt.channels().list(part="snippet", mine=True).execute()["items"][0]
    print(f"INFO: hedef kanal = {ch['id']} ({ch['snippet']['title']})")
    if ch["id"] != EXPECTED_CHANNEL:
        print(f"DUR: token beklenen kanala ait değil ({EXPECTED_CHANNEL}). İptal."); sys.exit(1)

    body = {
        "snippet": {
            "title": TITLE,
            "description": DESCRIPTION,
            "tags": TAGS,
            "categoryId": CATEGORY_ID,
            "defaultLanguage": "tr",
            "defaultAudioLanguage": "tr",
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False,
        },
    }
    media = MediaFileUpload(str(VIDEO), chunksize=8 * 1024 * 1024, resumable=True, mimetype="video/mp4")
    req = yt.videos().insert(part="snippet,status", body=body, media_body=media)

    print("INFO: yükleniyor...")
    resp = None
    while resp is None:
        status, resp = req.next_chunk()
        if status:
            print(f"  %{int(status.progress()*100)}")
    vid = resp["id"]
    print("SUCCESS: yüklendi (public).")
    print(f"SUCCESS: https://youtube.com/shorts/{vid}")
    print(f"SUCCESS: video_id={vid}")

if __name__ == "__main__":
    main()
