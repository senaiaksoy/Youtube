# -*- coding: utf-8 -*-
"""Read-only channel verification and video listing."""

from __future__ import annotations

import argparse
from typing import Any

from yt_common import get_service, verify_channel, write_json


def cmd_whoami(yt, channel: str, out: str | None) -> None:
    live = verify_channel(yt, channel, quiet=True)
    stats = live.get("statistics", {})
    uploads = live.get("contentDetails", {}).get("relatedPlaylists", {}).get("uploads")
    data = {
        "id": live["id"],
        "title": live["snippet"].get("title"),
        "customUrl": live["snippet"].get("customUrl"),
        "subscriberCount": stats.get("subscriberCount"),
        "videoCount": stats.get("videoCount"),
        "viewCount": stats.get("viewCount"),
        "uploadsPlaylist": uploads,
    }
    print(f"channel: {data['title']} ({data['id']})")
    print(f"subscribers={data['subscriberCount']} videos={data['videoCount']} views={data['viewCount']}")
    if out:
        print(f"wrote: {write_json(out, data)}")


def cmd_list(yt, max_count: int, out: str | None) -> None:
    ch = yt.channels().list(part="contentDetails", mine=True).execute()["items"][0]
    uploads = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    videos: list[dict[str, Any]] = []
    page = None
    while len(videos) < max_count:
        resp = yt.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=uploads,
            maxResults=min(50, max_count - len(videos)),
            pageToken=page,
        ).execute()
        for item in resp.get("items", []):
            videos.append(
                {
                    "videoId": item["contentDetails"]["videoId"],
                    "title": item["snippet"]["title"],
                    "publishedAt": item["contentDetails"].get("videoPublishedAt"),
                }
            )
        page = resp.get("nextPageToken")
        if not page:
            break

    for video in videos:
        print(f"{video['videoId']}  {video['publishedAt']}  {video['title']}")
    if out:
        print(f"wrote: {write_json(out, videos)}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--channel", required=True, choices=["fr", "tr"])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("whoami")
    p.add_argument("--out")
    p = sub.add_parser("list")
    p.add_argument("--max", type=int, default=25)
    p.add_argument("--out")
    args = ap.parse_args()

    yt = get_service(args.channel)
    if args.cmd == "whoami":
        cmd_whoami(yt, args.channel, args.out)
    elif args.cmd == "list":
        cmd_list(yt, args.max, args.out)


if __name__ == "__main__":
    main()
