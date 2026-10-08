"""Post the standard FR pinned comment to all French-AUDIO videos.

SAFE BY DEFAULT: dry-run unless --go is passed.
Idempotent: skips a video if the channel already posted a comment containing
the Ref marker 'yt-fr-pin'.
Processes in batches of 5 with progress logging, writes a run log and a
manual-pin checklist (YouTube API cannot pin; you pin in Studio).

Usage:
  python post_fr_pinned.py                 # dry-run, all 103
  python post_fr_pinned.py --go            # really post, all
  python post_fr_pinned.py --go --limit 5  # really post first 5 only
  python post_fr_pinned.py --go --start 5 --limit 5
"""
import argparse
import json
import sys
import time
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

BASE = Path(__file__).resolve().parent
TOKEN = BASE / "token.json"           # must have youtube.force-ssl scope
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
CHANNEL_ID = "UC51eCoXFnN1DiBd1dWcJpPQ"
REF_MARKER = "yt-fr-pin"
BATCH = 5

VIDEOS_FILE = BASE / "fr_audio_videos.json"
COMMENT_FILE = BASE / "pinned_comment_fr.txt"


def get_yt():
    if not TOKEN.exists():
        sys.exit("token.json yok. Önce: python oauth_login_with_url.py")
    creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)
    return build("youtube", "v3", credentials=creds)


def find_existing(yt, video_id):
    """Return (comment_id, current_text) for channel's ref-marked comment, else (None, None)."""
    resp = yt.commentThreads().list(
        part="snippet", videoId=video_id, maxResults=100,
        textFormat="plainText").execute()
    for it in resp.get("items", []):
        top = it["snippet"]["topLevelComment"]["snippet"]
        acid = (top.get("authorChannelId") or {}).get("value")
        if acid == CHANNEL_ID and REF_MARKER in top.get("textDisplay", ""):
            return it["snippet"]["topLevelComment"]["id"], top.get("textDisplay", "")
    return None, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--go", action="store_true", help="actually post (else dry-run)")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--start", type=int, default=0)
    args = ap.parse_args()

    comment = COMMENT_FILE.read_text(encoding="utf-8")
    videos = json.loads(VIDEOS_FILE.read_text(encoding="utf-8"))
    sel = videos[args.start: (args.start + args.limit) if args.limit else None]

    yt = get_yt()
    mode = "LIVE" if args.go else "DRY-RUN"
    print(f"[{mode}] {len(sel)} video (start={args.start}) | comment {len(comment)} chars")

    log = {"mode": mode, "posted": [], "updated": [], "skipped": [], "errors": []}
    for n, v in enumerate(sel, 1):
        vid, title = v["id"], v["title"]
        try:
            cid, cur = find_existing(yt, vid)
            if cid and cur.strip() == comment.strip():
                log["skipped"].append({"id": vid, "title": title, "why": "already current"})
                print(f"  {n:3}/{len(sel)} SKIP (guncel) {vid}  {title[:48]}")
            elif cid:
                # exists but outdated -> update text (pin preserved)
                if not args.go:
                    print(f"  {n:3}/{len(sel)} WOULD UPDATE  {vid}  {title[:48]}")
                else:
                    yt.comments().update(
                        part="snippet",
                        body={"id": cid, "snippet": {"textOriginal": comment}}).execute()
                    log["updated"].append({"id": vid, "title": title})
                    print(f"  {n:3}/{len(sel)} UPDATED       {vid}  {title[:48]}")
            elif not args.go:
                print(f"  {n:3}/{len(sel)} WOULD POST    {vid}  {title[:48]}")
            else:
                yt.commentThreads().insert(
                    part="snippet",
                    body={"snippet": {"videoId": vid,
                                       "topLevelComment": {"snippet": {"textOriginal": comment}}}}
                ).execute()
                log["posted"].append({"id": vid, "title": title})
                print(f"  {n:3}/{len(sel)} POSTED        {vid}  {title[:48]}")
        except HttpError as e:
            log["errors"].append({"id": vid, "title": title, "err": str(e.status_code)})
            print(f"  {n:3}/{len(sel)} ERROR {e.status_code} {vid}  {title[:50]}")

        if n % BATCH == 0:
            print(f"  --- batch {n//BATCH} bitti ({n}/{len(sel)}) ---")
            if args.go:
                time.sleep(2)

    stamp = sel and "run" or "run"
    logfile = BASE / f"post_fr_pinned_log_{mode.lower()}.json"
    logfile.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")

    # manual-pin checklist (only for actually-posted in LIVE)
    if args.go and log["posted"]:
        lines = ["# Studio'da elle pinlenecek videolar (yorumu atıldı):", ""]
        for p in log["posted"]:
            lines.append(f"[ ] https://studio.youtube.com/video/{p['id']}/comments  — {p['title']}")
        (BASE / "pin_checklist.txt").write_text("\n".join(lines), encoding="utf-8")

    print(f"\nÖZET [{mode}] posted={len(log['posted'])} updated={len(log['updated'])} skipped={len(log['skipped'])} errors={len(log['errors'])}")
    print(f"Log: {logfile.name}")
    if args.go and log["posted"]:
        print("Pin checklist: pin_checklist.txt")


if __name__ == "__main__":
    main()
