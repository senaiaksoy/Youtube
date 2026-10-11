# -*- coding: utf-8 -*-
"""Post the channel's standard (ref-marked) comment on specific videos. Dry-run by default; --go posts.

YouTube's API cannot pin a comment: pin it in Studio afterwards. Idempotent: skips a video that already has a
channel-authored comment containing the marker.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from googleapiclient.errors import HttpError

from yt_common import CHANNELS, get_service

CHANNEL_IDS = {k: v["id"] for k, v in CHANNELS.items()}


def existing(yt, video_id: str, channel_id: str, marker: str):
    page = None
    for _ in range(3):
        r = yt.commentThreads().list(part="snippet", videoId=video_id, maxResults=100, order="relevance",
                                     textFormat="plainText", pageToken=page).execute()
        for it in r.get("items", []):
            top = it["snippet"]["topLevelComment"]
            sn = top["snippet"]
            if (sn.get("authorChannelId") or {}).get("value") == channel_id and marker in sn.get("textDisplay", ""):
                return top["id"]
        page = r.get("nextPageToken")
        if not page:
            break
    return None


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--channel", required=True, choices=["fr", "tr", "en"])
    ap.add_argument("--videos", required=True, help="comma-separated video ids")
    ap.add_argument("--text-file", required=True)
    ap.add_argument("--marker", default="yt-fr-pin")
    ap.add_argument("--go", action="store_true")
    a = ap.parse_args()
    text = Path(a.text_file).read_text(encoding="utf-8").strip()
    if a.marker not in text:
        sys.exit(f"marker {a.marker!r} not found in the comment text")
    yt = get_service(a.channel)
    cid = CHANNEL_IDS[a.channel]
    print(f"comment text ({len(text)} chars):\n---\n{text}\n---")
    for vid in [v.strip() for v in a.videos.split(",") if v.strip()]:
        v = yt.videos().list(part="snippet,status", id=vid).execute().get("items", [])
        if not v:
            print(f"{vid}: not found on this channel"); continue
        title, priv = v[0]["snippet"]["title"], v[0]["status"]["privacyStatus"]
        if priv != "public":
            print(f"{vid}: SKIP ({priv}) {title}"); continue
        try:
            ex = existing(yt, vid, cid, a.marker)
        except HttpError as e:
            print(f"{vid}: SKIP comments unavailable ({e.resp.status}) {title}"); continue
        if ex:
            print(f"{vid}: already has marked comment {ex}  {title}"); continue
        if not a.go:
            print(f"{vid}: dry-run: would post  {title}"); continue
        r = yt.commentThreads().insert(part="snippet", body={"snippet": {"videoId": vid, "topLevelComment": {
            "snippet": {"textOriginal": text}}}}).execute()
        print(f"{vid}: posted {r['id']}  {title}  (now pin it in Studio)")


if __name__ == "__main__":
    main()
