import sys
import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

BASE = Path(__file__).resolve().parent
TOKEN = BASE / "token.json"
VIDEO_ID = "u16jZmYwB5w"
SRT_PATH = r"C:\Users\KC3\Downloads\dhea türkçescript 1_temiz.srt"

TITLE = "Yumurta Kalitesini Artırır mı? DHEA ve Büyüme Hormonu"

DESCRIPTION = """Düşük yumurta rezervi veya yetersiz yumurtalık cevabı olan kadınlarda DHEA ve büyüme hormonu (growth hormone) sıkça öneriliyor. Peki bu takviyeler gerçekten yumurta kalitesini ve gebelik şansını artırıyor mu? Yoksa bilimsel kanıtı olmayan bir pazarlama stratejisinden mi ibaret? Doç. Dr. Senai Aksoy, Cochrane incelemeleri ve meşhur LIGHT çalışması gibi en güncel klinik verileri analiz ediyor.

📌 Detaylı Bilgi ve Kaynaklar: https://www.tupbebek.com

🎬 İlgili Video: Tüp Bebekte En İyi Sperm Nasıl Seçilir? (IMSI, PICSI, MACS) → https://www.youtube.com/watch?v=FI2kj2cDe8k

⏱️ Videodaki Bölümler (Zaman Damgaları):
00:00 Giriş: DHEA ve Büyüme Hormonu Gerçekten İşe Yarıyor mu?
01:29 Bu Konu Neden Bu Kadar Gündemde?
03:02 DHEA Nedir? Yumurta Kalitesine Etkisi ve Biyolojik Mantığı
04:06 Büyüme Hormonu (Growth Hormone) Nedir? Tüp Bebekte Nasıl Kullanılır?
05:00 Bilim ve Klinik Çalışmalar Ne Diyor? (Cochrane ve LIGHT Çalışması)
07:04 DHEA ve Büyüme Hormonu Hangi Özel Durumlarda Kullanılabilir?
09:28 Hekim Gözüyle Süreç: İlaç Desteği mi, Yoksa Havuz Yöntemi mi?
11:46 Özet ve Kapanış (Doğru Bilgide Kalın)

📚 Bilimsel Kaynaklar:
- Cochrane Database of Systematic Reviews: Androgens (DHEA or testosterone) for women undergoing assisted reproduction.
- Norman RJ et al., LIGHT trial (2019): Human growth hormone for poor responders - Çift kör randomize kontrollü çalışma.
- ESHRE (2023): Good practice recommendations on add-ons in reproductive medicine (Tüp bebekte ek tedaviler kılavuzu).
- ESHRE Guideline: Ovarian stimulation for IVF/ICSI.

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
    "DHEA", "büyüme hormonu", "tüp bebek", "tüp bebek tedavisi", "düşük yumurta rezervi",
    "yumurta kalitesi", "growth hormone tüp bebek", "DHEA tüp bebek",
    "yumurta kalitesini artıran ilaçlar", "tüp bebek takviyeleri", "infertilite",
    "kısırlık tedavisi", "Doç. Dr. Senai Aksoy", "tüp bebek başarı oranları",
    "Cochrane tüp bebek", "LIGHT çalışması", "tüp bebek havuz yöntemi", "AMH düşüklüğü"
]

PINNED_COMMENT = """Tüp bebek tedavinizde size de DHEA veya Büyüme Hormonu (Growth Hormone) önerildi mi? Süreçte bu takviyeleri kullandınız mı ve deneyimleriniz neler oldu? Yorumlarda paylaşın, fırsat buldukça bizzat cevaplıyorum. 

🔬 Bilimsel Kaynaklar: Cochrane İncelemesi (2020) + LIGHT Çalışması (2019) + ESHRE Ek Tedaviler Rehberi (2023).
🎬 Tüp Bebekte Sperm Seçimi Yöntemleri (IMSI, PICSI, MACS) Videomuz: https://www.youtube.com/watch?v=FI2kj2cDe8k
📖 Detaylı Rehberler: www.tupbebek.com"""

PUBLISH_TIME = "2026-06-30T17:00:00+03:00"

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
    snippet["defaultLanguage"] = "tr"
    snippet["defaultAudioLanguage"] = "tr"
    
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
            if cap["snippet"]["language"] == "tr":
                print(f"INFO: Found existing Turkish caption track (ID: {cap['id']}). Deleting it first...")
                yt.captions().delete(id=cap["id"]).execute()
                print("SUCCESS: Existing caption track deleted.")
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
                    "language": "tr",
                    "name": "Türkçe",
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

    # 3. Post pinned comment
    print("INFO: Posting pinned comment...")
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
        
        # Pin the comment
        comment_id = comment_resp["snippet"]["topLevelComment"]["id"]
        print("INFO: Pinned comment posted. (Note: YouTube API does not allow programmatically pinning comments; it is posted as the owner).")
    except HttpError as e:
        print(f"WARNING: Failed to post comment: {e}")

if __name__ == "__main__":
    main()
