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


def cmd_scheduled(yt, max_count: int, out: str | None) -> None:
    """Read-only: non-public (private/unlisted/scheduled) videos among the latest uploads, with status.publishAt."""
    ch = yt.channels().list(part="contentDetails", mine=True).execute()["items"][0]
    uploads = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    ids: list[str] = []
    page = None
    while len(ids) < max_count:
        resp = yt.playlistItems().list(part="contentDetails", playlistId=uploads,
                                       maxResults=min(50, max_count - len(ids)), pageToken=page).execute()
        ids += [i["contentDetails"]["videoId"] for i in resp.get("items", [])]
        page = resp.get("nextPageToken")
        if not page:
            break
    rows: list[dict[str, Any]] = []
    for k in range(0, len(ids), 50):
        for v in yt.videos().list(part="snippet,status", id=",".join(ids[k:k + 50])).execute().get("items", []):
            st = v["status"]
            if st.get("privacyStatus") != "public" or st.get("publishAt"):
                rows.append({"videoId": v["id"], "title": v["snippet"]["title"],
                             "privacyStatus": st.get("privacyStatus"), "publishAt": st.get("publishAt")})
    rows.sort(key=lambda r: r["publishAt"] or "")
    for r in rows:
        print(f"{r['videoId']}  {r['privacyStatus']}  publishAt={r['publishAt']}  {r['title']}")
    print(f"non-public among latest {len(ids)}: {len(rows)}")
    if out:
        print(f"wrote: {write_json(out, rows)}")


def cmd_inventory(yt, out: str) -> None:
    """Read-only: every upload with date, duration, views/likes, privacy, tags and description (for validity reviews)."""
    ch = yt.channels().list(part="contentDetails", mine=True).execute()["items"][0]
    uploads = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    ids: list[str] = []
    page = None
    while True:
        resp = yt.playlistItems().list(part="contentDetails", playlistId=uploads, maxResults=50, pageToken=page).execute()
        ids += [i["contentDetails"]["videoId"] for i in resp.get("items", [])]
        page = resp.get("nextPageToken")
        if not page:
            break
    rows: list[dict[str, Any]] = []
    for k in range(0, len(ids), 50):
        resp = yt.videos().list(part="snippet,status,statistics,contentDetails", id=",".join(ids[k:k + 50])).execute()
        for v in resp.get("items", []):
            sn, st, ss = v["snippet"], v["status"], v.get("statistics", {})
            rows.append({"videoId": v["id"], "title": sn["title"], "publishedAt": sn.get("publishedAt"),
                         "duration": v["contentDetails"].get("duration"), "views": int(ss.get("viewCount", 0)),
                         "likes": int(ss.get("likeCount", 0)), "comments": int(ss.get("commentCount", 0)),
                         "privacyStatus": st.get("privacyStatus"), "publishAt": st.get("publishAt"),
                         "tags": sn.get("tags", []), "description": sn.get("description", "")})
    rows.sort(key=lambda r: r["publishedAt"] or "")
    print(f"inventory: {len(rows)} videos -> {write_json(out, rows)}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--channel", required=True, choices=["fr", "tr", "en"])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("whoami")
    p.add_argument("--out")
    p = sub.add_parser("list")
    p.add_argument("--max", type=int, default=25)
    p.add_argument("--out")
    p = sub.add_parser("scheduled")
    p.add_argument("--max", type=int, default=200)
    p.add_argument("--out")
    p = sub.add_parser("inventory")
    p.add_argument("--out", required=True)
    args = ap.parse_args()

    yt = get_service(args.channel)
    if args.cmd == "whoami":
        cmd_whoami(yt, args.channel, args.out)
    elif args.cmd == "list":
        cmd_list(yt, args.max, args.out)
    elif args.cmd == "inventory":
        cmd_inventory(yt, args.out)
    elif args.cmd == "scheduled":
        cmd_scheduled(yt, args.max, args.out)


if __name__ == "__main__":
    main()
