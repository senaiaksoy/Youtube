"""Read-only audit: which PUBLIC videos on the FR channel have no channel-authored 'yt-fr-pin' comment."""
import json, re, sys, time
from pathlib import Path

sys.path.insert(0, r"D:\A-klasör\Youtube\.claude\skills\yt-pipeline\scripts")
import yt_common as c
from googleapiclient.errors import HttpError

c.configure_output()
CH = "UC51eCoXFnN1DiBd1dWcJpPQ"
yt = c.get_service("fr", quiet=True)
items = json.loads(Path(r"D:\A-klasör\Youtube\youtube-api\all-fr3.json").read_text(encoding="utf-8-sig"))
items = items if isinstance(items, list) else items.get("videos", items.get("items", []))
ids = [i.get("id") or i.get("video_id") or i.get("videoId") for i in items]
ids = [i for i in ids if isinstance(i, str)]
vids = []
for k in range(0, len(ids), 50):
    for v in yt.videos().list(part="snippet,contentDetails,status,statistics", id=",".join(ids[k:k + 50])).execute()["items"]:
        m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", v["contentDetails"]["duration"])
        sec = int(m.group(1) or 0) * 3600 + int(m.group(2) or 0) * 60 + int(m.group(3) or 0)
        vids.append(dict(id=v["id"], title=v["snippet"]["title"], sec=sec, privacy=v["status"]["privacyStatus"],
                         views=int(v["statistics"].get("viewCount", 0)), pub=v["snippet"]["publishedAt"][:10],
                         audio=v["snippet"].get("defaultAudioLanguage", "?"), lang=v["snippet"].get("defaultLanguage", "?")))
pub = [v for v in vids if v["privacy"] == "public"]
print(len(vids), "videos;", len(pub), "public")
res = {}
for n, v in enumerate(pub):
    state, found = "none", False
    page = None
    for _ in range(3):
        try:
            r = yt.commentThreads().list(part="snippet", videoId=v["id"], maxResults=100, order="relevance",
                                         textFormat="plainText", pageToken=page).execute()
        except HttpError as e:
            state = "comments-disabled" if "commentsDisabled" in str(e) or e.resp.status == 403 else f"error-{e.resp.status}"
            break
        for it in r.get("items", []):
            top = it["snippet"]["topLevelComment"]["snippet"]
            if (top.get("authorChannelId") or {}).get("value") == CH:
                if "yt-fr-pin" in top.get("textDisplay", ""):
                    state, found = "has-ref", True; break
                state = "channel-comment-no-ref"
        page = r.get("nextPageToken")
        if found or not page:
            break
    res[v["id"]] = state
    if n % 40 == 39:
        print("...", n + 1, flush=True)
Path(r"D:\A-klasör\Youtube\youtube-api\audit-pinned.json").write_text(json.dumps([dict(v, state=res[v["id"]]) for v in pub], ensure_ascii=False, indent=1), encoding="utf-8")
from collections import Counter
print("states:", dict(Counter(res.values())))
for kind, cond in (("LONG (>3 min)", lambda v: v["sec"] > 180), ("SHORTS (<=3 min)", lambda v: v["sec"] <= 180)):
    sub = [v for v in pub if cond(v)]
    miss = [v for v in sub if res[v["id"]] != "has-ref"]
    print(f"\n{kind}: {len(sub)} public, {len(miss)} without ref comment")
    for fa in ("fr", "other"):
        mm = [v for v in miss if (v["audio"].startswith("fr")) == (fa == "fr")]
        print(f"  audio {fa}: {len(mm)}")
