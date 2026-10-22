# -*- coding: utf-8 -*-
"""Clomid videolarinin aciklamasina yeni Clomid videosuna baglanti ekler (yalnizca metin ekleme)."""
import json

INV = r"D:\A-klasör\Youtube\youtube-api\audit-2026-10-22\inventory-fr-after3.json"
OUT = r"D:\A-klasör\Youtube\youtube-api\audit-2026-10-22\clomid-link-fixes.json"
LINE = "▶ À voir aussi : Clomid et pas de grossesse : quand changer de plan ? https://youtu.be/97g8_8_Wcmc"

inv = {v["videoId"]: v for v in json.load(open(INV, encoding="utf-8"))}
fixes = []
for vid in ("rz4zt7mXY-o", "7bU-f3uE6pQ"):
    desc = inv[vid]["description"]
    assert "97g8_8_Wcmc" not in desc
    marker = "\n\nChapitres :"
    assert desc.count(marker) == 1
    new = desc.replace(marker, "\n\n" + LINE + marker, 1)
    fixes.append({"video_id": vid, "description": new})
json.dump(fixes, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for f in fixes:
    i = f["description"].index("▶ À voir")
    print(f["video_id"], "inserted at char", i, "| length", len(f["description"]))
