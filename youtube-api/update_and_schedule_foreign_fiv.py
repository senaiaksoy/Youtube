import sys
import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

BASE = Path(__file__).resolve().parent
TOKEN = BASE / "token.senaiaksoy.20260510-193158.json"
if not TOKEN.exists():
    TOKEN = BASE / "token.json"

VIDEO_ID = "zhcapjJhxzA"
SRT_PATH = r"C:\Users\KC3\Downloads\final-draft-v5-dedup-opening-7a.srt"

TITLE = "FIV à l’étranger : Pourquoi commencer par le dossier (et non la valise) ?"

DESCRIPTION = """Quand un couple commence à envisager une FIV à l'étranger, la première étape n'est pas de réserver un vol ou de choisir une clinique uniquement parce qu'elle se trouve dans un autre pays. La vraie priorité absolue est de faire évaluer correctement son dossier médical par un médecin spécialiste. 

Dans cette vidéo, le Doç. Dr. Senai Aksoy, gynécologue-obstétricien et spécialiste de l'infertilité et de la FIV à Istanbul avec plus de 30 ans d'expérience, vous explique comment bien préparer votre projet parental à l'étranger, les étapes du protocole FIV/ICSI, ainsi que les spécificités légales en Turquie (FIV réalisée exclusivement avec vos propres gamètes, don de sperme/ovocytes et GPA interdits).

📲 Une question sur votre parcours FIV ? Écrivez-nous directement sur WhatsApp :
👉 https://wa.me/905073802805?text=Bonjour%20Dr%20Aksoy%2C%20j%27ai%20vu%20votre%20vid%C3%A9o%20YouTube%20et%20j%27aimerais%20des%20informations%20sur%20un%20parcours%20de%20FIV.
🌐 Site Web : www.draksoyivf.com

⏱ Sommaire de la vidéo (Zaman Damgaları) :
00:00 Introduction du Dr. Senai Aksoy
00:15 La vraie question : votre dossier a-t-il été bien évalué ?
00:30 L'erreur courante : choisir la clinique avant d'analyser le dossier
01:25 Qu'est-ce que la FIV et l'ICSI ? (Démystification du cycle)
02:47 Législation en Turquie : ce qui est autorisé et ce qui est interdit
03:23 Réponses à vos questions (Durée du séjour, accompagnement en français, échecs)
04:12 Règle d'or : commencez par votre dossier, pas par votre valise !
04:54 Conclusion et avertissement médical

Dr. Senai Aksoy ile İletişime Geçin:

🩺 Randevu ve Bilgi İçin:
📞 Telefon & WhatsApp: +90 533 254 60 40
📧 E-posta: contact@draksoyivf.com
🌐 Web Sitesi: www.tupbebek.com

📍 Muayenehane Adresi:
Lotus Nişantaşı, Halaskargazi Mah., Halaskargazi Cad. No: 38-66, Kat 5, Ofis 92, Şişli / İstanbul

👇 Sosyal Medyada Bizi Takip Edin:
YouTube: https://www.youtube.com/c/SenaiAksoy
Instagram: @drsenaiaksoy

⚕️ ÖNEMLİ TIBBİ UYARI
Bu videoda sunulan bilgiler yalnızca eğitim ve bilgilendirme amaçlıdır. Bu içerik hiçbir koşulda tıbbi tavsiye, tanı veya kişiselleştirilmiş tedavi önerisi niteliği taşımamaktadır.
Her hastanın tıbbi durumu kendine özgüdür. Bu videoda ele alınan konular; bir hekim, kadın doğum uzmanı veya üreme tıbbı uzmanı ile yapılacak konsültasyonun yerini tutmaz.
Bu videodaki bilgilere dayanarak mevcut tedavinizi değiştirmeyin, yeni bir tedaviye başlamayın veya herhangi bir tıbbi karar almayın. Her türlü tıbbi karar öncesinde mutlaka aile hekiminize veya uzman doktorunuza danışınız.
Üreme sağlığınız veya IVF tedavi sürecinizle ilgili sorularınız için lütfen yetkili bir sağlık profesyoneline başvurunuz.
© Doç. Dr. Senai Aksoy — Tüm hakları saklıdır."""

TAGS = [
    "FIV à l'étranger", "FIV en Turquie", "PMA à l'étranger", "FIV", "PMA",
    "fécondation in vitro", "ICSI", "préparer dossier FIV", "dossier médical FIV",
    "Dr Senai Aksoy", "clinique FIV Turquie", "infertilité", "loi FIV Turquie",
    "don d'ovocytes", "draksoyivf"
]

PINNED_COMMENT = """📲 Une question sur votre parcours FIV ? Écrivez-nous directement sur WhatsApp :
👉 https://wa.me/905073802805?text=Bonjour%20Dr%20Aksoy%2C%20j%27ai%20vu%20votre%20vidéo%20YouTube%20et%20j%27aimerais%20des%20informations%20sur%20un%20parcours%20de%20FIV.
🌐 www.draksoyivf.com

🇬🇧 Questions? Message us on WhatsApp (link above).
🇸🇦 للأسئلة، راسلونا على واتساب (الرابط أعلاه).

ℹ️ Ce canal est informatif et ne remplace pas une consultation médicale personnalisée."""

PUBLISH_TIME = "2026-06-30T15:00:00+03:00"

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

    if not TOKEN.exists():
        print(f"ERROR: Token file not found: {TOKEN}")
        sys.exit(1)

    creds = Credentials.from_authorized_user_file(str(TOKEN), [
        "https://www.googleapis.com/auth/youtube",
        "https://www.googleapis.com/auth/youtube.force-ssl"
    ])
    yt = build("youtube", "v3", credentials=creds)

    print(f"INFO: Fetching details for video {VIDEO_ID}...")
    try:
        vid_resp = yt.videos().list(part="snippet,status", id=VIDEO_ID).execute()
        items = vid_resp.get("items", [])
        if not items:
            print(f"ERROR: Video {VIDEO_ID} not found.")
            sys.exit(1)
        video = items[0]
        snippet = video["snippet"]
        status = video["status"]
    except HttpError as e:
        print(f"ERROR: Failed to fetch video details: {e}")
        sys.exit(1)

    # 1. Update snippet and status (scheduling)
    print("INFO: Updating metadata (title, description, tags) and scheduling publish time...")
    snippet["title"] = TITLE
    snippet["description"] = DESCRIPTION
    snippet["tags"] = TAGS
    snippet["defaultLanguage"] = "fr"
    snippet["defaultAudioLanguage"] = "fr"
    
    # Remove read-only localized block to prevent description reversion quirk in YouTube API
    if "localized" in snippet:
        del snippet["localized"]
    
    status["privacyStatus"] = "private"
    status["publishAt"] = PUBLISH_TIME

    try:
        update_resp = yt.videos().update(
            part="snippet,status",
            body={
                "id": VIDEO_ID,
                "snippet": snippet,
                "status": status
            }
        ).execute()
        print("SUCCESS: Video metadata updated and publish time scheduled successfully!")
        print(f"Scheduled Publish Time: {update_resp['status'].get('publishAt')}")
    except HttpError as e:
        print(f"ERROR: Failed to update video: {e}")
        sys.exit(1)

    # 2. Upload subtitles
    print(f"INFO: Checking if captions already exist for {VIDEO_ID}...")
    try:
        caps_resp = yt.captions().list(part="snippet", videoId=VIDEO_ID).execute()
        caps = caps_resp.get("items", [])
        for cap in caps:
            if cap["snippet"]["language"] == "fr":
                print(f"INFO: Found existing French caption track (ID: {cap['id']}). Deleting it first...")
                yt.captions().delete(id=cap["id"]).execute()
                print("SUCCESS: Existing French caption track deleted.")
    except HttpError as e:
        print(f"WARNING: Error listing/deleting captions: {e}")

    print(f"INFO: Uploading SRT file from {SRT_PATH}...")
    if not Path(SRT_PATH).exists():
        print(f"ERROR: SRT file not found at {SRT_PATH}")
        sys.exit(1)

    try:
        media = MediaFileUpload(SRT_PATH, mimetype="*/*", resumable=True)
        cap_insert = yt.captions().insert(
            part="snippet",
            body={
                "snippet": {
                    "videoId": VIDEO_ID,
                    "language": "fr",
                    "name": "Français",
                    "isDraft": False
                }
            },
            media_body=media
        ).execute()
        print("SUCCESS: Subtitles uploaded successfully!")
        print(json.dumps(cap_insert, ensure_ascii=False, indent=2))
    except HttpError as e:
        print(f"ERROR: Failed to upload subtitles: {e}")
        sys.exit(1)

    # 3. Post comment
    print("INFO: Posting comment...")
    try:
        comment_body = {
            "snippet": {
                "videoId": VIDEO_ID,
                "topLevelComment": {
                    "snippet": {
                        "textOriginal": PINNED_COMMENT
                    }
                }
            }
        }
        comment_resp = yt.commentThreads().insert(part="snippet", body=comment_body).execute()
        print("SUCCESS: Comment posted successfully!")
        print("NOTE: Please pin this comment manually in YouTube Studio as the API does not support programmatic pinning.")
    except HttpError as e:
        print(f"WARNING: Failed to post comment: {e}")

if __name__ == "__main__":
    main()
