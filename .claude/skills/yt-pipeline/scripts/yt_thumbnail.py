# -*- coding: utf-8 -*-
"""Set a custom thumbnail on one video. Dry-run by default; --go uploads.

YouTube's "Test & Compare" thumbnail experiment is Studio-only and cannot be driven from the API.
"""

from __future__ import annotations

import argparse
import mimetypes
import sys
from pathlib import Path

from googleapiclient.http import MediaFileUpload

from yt_common import get_service, write_json

MAX_BYTES = 2 * 1024 * 1024


def cmd_set(yt, video_id: str, file: str, go: bool) -> None:
    path = Path(file)
    if not path.is_file():
        sys.exit(f"missing file: {path}")
    size = path.stat().st_size
    mime = mimetypes.guess_type(str(path))[0] or ""
    if mime not in ("image/jpeg", "image/png"):
        sys.exit(f"unsupported type {mime!r}; use JPG or PNG")
    if size > MAX_BYTES:
        sys.exit(f"{size} bytes exceeds the 2 MB limit")
    items = yt.videos().list(part="snippet", id=video_id).execute().get("items", [])
    if not items:
        sys.exit(f"video not found on this channel: {video_id}")
    print(f"video: {video_id}  {items[0]['snippet']['title']}")
    print(f"file: {path.name}  {size // 1024} KB  {mime}")
    if not go:
        print("dry-run only. Re-run with --go after explicit user approval.")
        return
    resp = yt.thumbnails().set(videoId=video_id, media_body=MediaFileUpload(str(path), mimetype=mime)).execute()
    urls = resp.get("items", [{}])[0]
    print("thumbnail set:", {k: v.get("url") for k, v in urls.items() if isinstance(v, dict)})


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--channel", required=True, choices=["fr", "tr", "en"])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("set")
    p.add_argument("--video", required=True)
    p.add_argument("--file", required=True)
    p.add_argument("--go", action="store_true")
    args = ap.parse_args()
    yt = get_service(args.channel)
    if args.cmd == "set":
        cmd_set(yt, args.video, args.file, args.go)


if __name__ == "__main__":
    main()
