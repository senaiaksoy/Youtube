"""Fill metadata for the two DHEA FR Shorts already uploaded as private drafts
on Dr. Senai Aksoy (UC51eCoXFnN1DiBd1dWcJpPQ). Privacy is NOT changed.

Usage: python update_dhea_fr_shorts_2026_10_04.py [--live]
"""
from __future__ import annotations

import sys
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding="utf-8")

BASE = Path(__file__).resolve().parent
TOKEN = BASE / "token.senaiaksoy.20260510-193158.json"
SCOPES = ["https://www.googleapis.com/auth/youtube"]
EXPECTED_CHANNEL = "UC51eCoXFnN1DiBd1dWcJpPQ"
LONG_VIDEO = "https://youtu.be/dYF3NWf4Nw8"
PLAYLISTS = [
    "PL21Sr5bmkPJWpeRf3_x5A_YhrLkkLOXIS",  # Questions fréquentes en FIV et PMA
    "PL21Sr5bmkPJXmf7cJMbIW8p_VQ910IWf2",  # Tout comprendre sur la FIV
]

FOOTER = (
    "Pour plus amples informations :  \n"
    "📱 WhatsApp : +90 507 380 28 05  \n"
    "🌐 Web site : www.draksoyivf.com\n\n"
    "⚕️ AVERTISSEMENT MÉDICAL IMPORTANT\n\n"
    "Les informations présentées dans cette vidéo sont fournies à titre éducatif et informatif uniquement. "
    "Elles ne constituent en aucun cas un avis médical, un diagnostic ou une recommandation de traitement personnalisée.\n\n"
    "Chaque situation médicale est unique. Les contenus abordés ici ne remplacent pas une consultation avec un médecin "
    "qualifié, un gynécologue ou un spécialiste en médecine de la reproduction.\n\n"
    "Ne modifiez jamais votre traitement médical en cours, ne commencez pas un nouveau traitement et ne prenez aucune "
    "décision médicale sur la base des informations contenues dans cette vidéo, sans avoir préalablement consulté votre "
    "médecin traitant ou votre spécialiste.\n\n"
    "Si vous avez des questions concernant votre santé reproductive ou votre prise en charge en FIV, veuillez consulter "
    "un professionnel de santé qualifié.\n\n"
    "© Assoc. Prof. Dr. Senai Aksoy — Tous droits réservés."
)

COCHRANE = "https://doi.org/10.1002/14651858.CD009749.pub3"

VIDEOS = {
    "SF5Dx95TTGg": {
        "title": "DHEA et FIV : 28 essais… mais combien sur la DHEA ? #Shorts",
        "description": (
            "« 28 essais randomisés » : ce chiffre circule souvent à propos de la DHEA en FIV. "
            "En ouvrant la revue Cochrane 2024, on découvre que 14 essais portent sur la DHEA et 14 sur la "
            "testostérone. Le Dr Senai Aksoy explique pourquoi les résultats de la testostérone ne peuvent pas "
            "être attribués à la DHEA.\n\n"
            f"▶ Analyse complète : {LONG_VIDEO}\n\n"
            "Étude présentée :\n"
            f"Revue Cochrane 2024 (androgènes en AMP) : {COCHRANE}\n\n"
            "#FIV #DHEA #Fertilité\n\n" + FOOTER
        ),
        "tags": [
            "DHEA", "FIV", "DHEA FIV", "DHEA fertilité", "testostérone FIV",
            "revue Cochrane", "essais randomisés", "faible réponse ovarienne",
            "réserve ovarienne basse", "compléments FIV", "fertilité", "PMA",
            "Dr Senai Aksoy",
        ],
    },
    "FZPzp7OWAzM": {
        "title": "DHEA en FIV : plus d’ovocytes = plus de naissances ? #Shorts",
        "description": (
            "Plus d’ovocytes ne signifie pas automatiquement plus de naissances vivantes. "
            "Chez les femmes répondant peu à la stimulation, la revue Cochrane 2024 conclut que la DHEA "
            "fait probablement peu ou pas de différence sur les naissances vivantes et les grossesses "
            "évolutives (niveau de confiance modéré). Le Dr Senai Aksoy explique cette nuance essentielle.\n\n"
            f"▶ Analyse complète : {LONG_VIDEO}\n\n"
            "Étude présentée :\n"
            f"Revue Cochrane 2024 (androgènes en AMP) : {COCHRANE}\n\n"
            "#FIV #DHEA #Fertilité\n\n" + FOOTER
        ),
        "tags": [
            "DHEA", "FIV", "DHEA FIV", "naissance vivante", "nombre d'ovocytes",
            "faible répondeuse", "faible réponse ovarienne", "revue Cochrane",
            "AMH basse", "compléments FIV", "fertilité", "PMA", "Dr Senai Aksoy",
        ],
    },
}


def main() -> None:
    live = "--live" in sys.argv
    creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)
    yt = build("youtube", "v3", credentials=creds)
    ch = yt.channels().list(part="id", mine=True).execute()["items"][0]["id"]
    if ch != EXPECTED_CHANNEL:
        sys.exit(f"DUR: yanlış kanal {ch}")

    for vid, meta in VIDEOS.items():
        assert len(meta["title"]) <= 100 and len(meta["description"]) <= 5000
        assert sum(len(t) + 1 for t in meta["tags"]) < 500
        cur = yt.videos().list(part="snippet,localizations,status", id=vid).execute()["items"][0]
        snip = cur["snippet"]
        snip.update(
            title=meta["title"],
            description=meta["description"],
            tags=meta["tags"],
            categoryId="27",
            defaultLanguage="fr",
            defaultAudioLanguage="fr",
        )
        snip.pop("thumbnails", None)
        snip.pop("localized", None)
        locs = cur.get("localizations", {})
        locs["fr"] = {"title": meta["title"], "description": meta["description"]}
        print(f"{vid}: {meta['title']} (privacy={cur['status']['privacyStatus']})")
        if not live:
            continue
        yt.videos().update(
            part="snippet,localizations",
            body={"id": vid, "snippet": snip, "localizations": locs},
        ).execute()
        print("  OK meta güncellendi")
        for pl in PLAYLISTS:
            exists = yt.playlistItems().list(
                part="id", playlistId=pl, videoId=vid
            ).execute()["items"]
            if not exists:
                yt.playlistItems().insert(
                    part="snippet",
                    body={"snippet": {"playlistId": pl,
                                      "resourceId": {"kind": "youtube#video", "videoId": vid}}},
                ).execute()
                print(f"  OK playlist {pl}")
    if not live:
        print("DRY-RUN. Uygulamak için --live")


if __name__ == "__main__":
    main()
