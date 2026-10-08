"""Upload FIV complements Short to French channel Dr. Senai Aksoy (public)."""
from __future__ import annotations

import sys
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

BASE = Path(__file__).resolve().parent
TOKEN = BASE / "token.senaiaksoy.20260510-193158.json"
VIDEO = Path(
    r"D:/A-klasör/openmontage/projects/fiv-complements-short/renders/final.mp4"
)
SCOPES = ["https://www.googleapis.com/auth/youtube"]
EXPECTED_CHANNEL = "UC51eCoXFnN1DiBd1dWcJpPQ"  # Dr. Senai Aksoy (FR)

TITLE = "Compléments miracles FIV : science ou placement de produit ?"

DESCRIPTION = (
    "Vous ouvrez Instagram et c’est le Festival du Miracle : CoQ10, peptides, "
    "vitamines… Trois influenceuses, trois « preuves ». Qui a raison ?\n\n"
    "Ce n’est pas la bonne question. La vraie question, c’est comment faire le "
    "tri entre la science et le placement de produits sponsorisés.\n\n"
    "Dans cette Short, le Dr Senai Aksoy pose le cadre critique pour les "
    "compléments miracles en fertilité et en FIV.\n\n"
    "📖 Articles et ressources : https://www.draksoyivf.com\n"
    "💬 Dites en commentaire quel complément on a essayé de vous vendre "
    "cette semaine.\n\n"
    "⚠️ Contenu informatif. Ne remplace pas une consultation personnalisée "
    "et ne constitue pas une prescription médicale.\n\n"
    "#FIV #fertilité #compléments #PMA #infertilité #drsenaiaksoy #Shorts "
    "#science #Instagram"
)

TAGS = [
    "FIV",
    "fertilité",
    "compléments alimentaires",
    "PMA",
    "infertilité",
    "add-on FIV",
    "Dr Senai Aksoy",
    "science",
    "Instagram",
    "Shorts",
    "procréation assistée",
    "ovaires",
]

CATEGORY_ID = "27"  # Education

PINNED_COMMENT = (
    "Quel complément « miracle » on a essayé de vous vendre cette semaine "
    "sur Instagram ? Écrivez-le en commentaire — je passe régulièrement "
    "répondre.\n\n"
    "📖 Lecture complète : https://www.draksoyivf.com\n"
    "⚠️ Information générale, pas un avis médical personnalisé."
)


def main() -> None:
    if not VIDEO.exists():
        print(f"HATA: video yok: {VIDEO}")
        sys.exit(1)
    if not TOKEN.exists():
        print(f"HATA: token yok: {TOKEN}")
        sys.exit(1)

    creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)
    yt = build("youtube", "v3", credentials=creds)

    ch = yt.channels().list(part="snippet", mine=True).execute()["items"][0]
    print(f"INFO: hedef kanal = {ch['id']} ({ch['snippet']['title']})")
    if ch["id"] != EXPECTED_CHANNEL:
        print(f"DUR: beklenen FR kanal değil ({EXPECTED_CHANNEL}). İptal.")
        sys.exit(1)

    body = {
        "snippet": {
            "title": TITLE,
            "description": DESCRIPTION,
            "tags": TAGS,
            "categoryId": CATEGORY_ID,
            "defaultLanguage": "fr",
            "defaultAudioLanguage": "fr",
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False,
        },
    }
    media = MediaFileUpload(
        str(VIDEO),
        chunksize=8 * 1024 * 1024,
        resumable=True,
        mimetype="video/mp4",
    )
    req = yt.videos().insert(part="snippet,status", body=body, media_body=media)

    print("INFO: yükleniyor (public)...")
    resp = None
    while resp is None:
        status, resp = req.next_chunk()
        if status:
            print(f"  %{int(status.progress() * 100)}")

    vid = resp["id"]
    print("SUCCESS: yüklendi (public).")
    print(f"SUCCESS: https://youtube.com/shorts/{vid}")
    print(f"SUCCESS: video_id={vid}")

    try:
        yt.commentThreads().insert(
            part="snippet",
            body={
                "snippet": {
                    "videoId": vid,
                    "topLevelComment": {
                        "snippet": {"textOriginal": PINNED_COMMENT}
                    },
                }
            },
        ).execute()
        print("SUCCESS: yorum gönderildi (Studio'dan pinleyebilirsiniz).")
    except Exception as e:
        print(f"WARNING: yorum atılamadı: {e}")


if __name__ == "__main__":
    main()
