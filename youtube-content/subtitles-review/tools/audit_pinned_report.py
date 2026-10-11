import json
from collections import Counter

r = json.load(open(r"D:\A-klasör\Youtube\youtube-api\audit-pinned.json", encoding="utf-8"))
miss = [v for v in r if v["state"] != "has-ref"]
print("missing", len(miss), "| by audio:", dict(Counter(v["audio"][:2] for v in miss)))
print("missing by state:", dict(Counter(v["state"] for v in miss)))
print("\n--- FR-audio videos WITHOUT ref comment ---")
for v in sorted([v for v in miss if v["audio"].startswith("fr")], key=lambda x: x["pub"]):
    print(v["id"], v["pub"], f"{v['sec']}s", v["views"], "views", v["state"], "|", v["title"][:70])
print("\n--- audio language unknown (?) without ref comment ---")
q = [v for v in miss if v["audio"] == "?"]
print(len(q))
for v in sorted(q, key=lambda x: -x["views"])[:8]:
    print(v["id"], v["pub"], f"{v['sec']}s", v["views"], "views", v["state"], "|", v["title"][:70])
print("\n--- top missing by views (any audio) ---")
for v in sorted(miss, key=lambda x: -x["views"])[:8]:
    print(v["id"], v["audio"][:2], v["pub"], f"{v['sec']}s", v["views"], "views", v["state"], "|", v["title"][:60])
print("\n--- languages of videos WITH ref comment ---")
print(dict(Counter(v["audio"][:2] for v in r if v["state"] == "has-ref")))
