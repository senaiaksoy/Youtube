# -*- coding: utf-8 -*-
"""Upload videos (e.g. Shorts) as private + scheduled (status.publishAt). Dry-run by default; --go uploads.

Manifest JSON: list of {file, title, description, tags, publishAt (UTC ISO, e.g. 2026-11-11T17:00:00Z),
categoryId (default 27), language (default fr)}. Quota: videos.insert costs ~1600 units per video.
Never publishes immediately: privacyStatus is always private; YouTube flips it public at publishAt.
Idempotent: a video whose exact title already exists in the latest uploads is skipped.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from googleapiclient.http import MediaFileUpload

from yt_common import get_service, read_json, write_json


def probe(path: Path) -> dict:
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                        "-show_entries", "format=duration", "-of", "json", str(path)], capture_output=True, text=True)
    d = json.loads(r.stdout)
    return {"w": d["streams"][0]["width"], "h": d["streams"][0]["height"], "dur": float(d["format"]["duration"])}


def existing_titles(yt, limit: int = 50) -> dict[str, str]:
    ch = yt.channels().list(part="contentDetails", mine=True).execute()["items"][0]
    up = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    resp = yt.playlistItems().list(part="snippet,contentDetails", playlistId=up, maxResults=limit).execute()
    return {i["snippet"]["title"]: i["contentDetails"]["videoId"] for i in resp.get("items", [])}


def validate(item: dict) -> list[str]:
    errs = []
    if not Path(item["file"]).is_file():
        errs.append(f"missing file {item['file']}")
    if len(item["title"]) > 100:
        errs.append("title > 100 chars")
    if len(item["description"].encode("utf-8")) > 5000:
        errs.append("description > 5000 bytes")
    if sum(len(t) + 1 for t in item.get("tags", [])) > 480:
        errs.append("tags too long")
    try:
        when = datetime.fromisoformat(item["publishAt"].replace("Z", "+00:00"))
        if when <= datetime.now(timezone.utc):
            errs.append("publishAt is in the past")
    except Exception:
        errs.append("bad publishAt")
    return errs


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--channel", required=True, choices=["fr", "tr", "en"])
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--only", help="only the manifest entry whose file name contains this text")
    ap.add_argument("--go", action="store_true")
    ap.add_argument("--out", help="write results JSON here")
    args = ap.parse_args()

    items = read_json(args.manifest)
    if args.only:
        items = [i for i in items if args.only in Path(i["file"]).name]
    yt = get_service(args.channel)
    have = existing_titles(yt)
    bad = False
    for it in items:
        errs = validate(it)
        pr = probe(Path(it["file"])) if Path(it["file"]).is_file() else {}
        print(f"\n{Path(it['file']).name}  {pr.get('w')}x{pr.get('h')}  {pr.get('dur', 0):.1f}s")
        print(f"  title:     {it['title']}")
        print(f"  publishAt: {it['publishAt']} (private until then)")
        print(f"  tags:      {', '.join(it.get('tags', []))}")
        print(f"  desc:      {it['description'][:120].replace(chr(10), ' / ')}...")
        if it["title"] in have:
            print(f"  SKIP: a video with this exact title already exists: {have[it['title']]}")
        elif errs:
            bad = True
            print("  ERRORS:", "; ".join(errs))
    if bad:
        sys.exit("fix the errors above first")
    if not args.go:
        print("\ndry-run only. Re-run with --go after explicit user approval (quota ~1600 units per video).")
        return
    results = []
    for it in items:
        if it["title"] in have:
            continue
        lang = it.get("language", "fr")
        body = {
            "snippet": {"title": it["title"], "description": it["description"], "tags": it.get("tags", []),
                        "categoryId": it.get("categoryId", "27"), "defaultLanguage": lang, "defaultAudioLanguage": lang},
            "status": {"privacyStatus": "private", "publishAt": it["publishAt"], "selfDeclaredMadeForKids": False,
                       "embeddable": True, "publicStatsViewable": True},
        }
        media = MediaFileUpload(it["file"], mimetype="video/mp4", chunksize=8 * 1024 * 1024, resumable=True)
        req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
        resp = None
        while resp is None:
            st, resp = req.next_chunk()
            if st:
                print(f"  {Path(it['file']).name}: {int(st.progress() * 100)}%")
        print(f"uploaded {resp['id']}  {it['title']}  publishAt={it['publishAt']}")
        results.append({"videoId": resp["id"], "title": it["title"], "publishAt": it["publishAt"]})
    if args.out:
        print(f"wrote: {write_json(args.out, results)}")


if __name__ == "__main__":
    main()
