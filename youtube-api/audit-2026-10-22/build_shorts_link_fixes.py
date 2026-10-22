# -*- coding: utf-8 -*-
"""FR Shorts aciklamalarina ilgili uzun videoya '▶ Vidéo complète' baglantisi ekler (yalnizca metin ekleme)."""
import json
import re

D = r"D:\A-klasör\Youtube\youtube-api\audit-2026-10-22"
inv = {v["videoId"]: v for v in json.load(open(D + r"\inventory-fr-after3.json", encoding="utf-8"))}

# kisa video -> ilgili uzun video (ayni soru/konu, FR, herkese acik)
MAP = {
    "rH1AGfNIYpE": "cFK8TkopaKM",  # SHO
    "N_5WKEHI7g4": "2z2x98boWpQ",  # transfer agri mi
    "UopPTX_LAt0": "MyyY30lUCew",  # ikizler
    "zzz5CvVolCY": "6E59NQslyiQ",  # tek tup
    "cZJulovEuD4": "BOUENdTTIHs",  # PCOS ovulasyon
    "qVems6A0aC8": "xffSrbGxIFg",  # aciklanamayan infertilite
    "mImL0vIdijU": "L7cfmcaIxOk",  # IUI sonrasi IVF
    "ZqPvEO3UwB8": "P3-K-M9hJug",  # hidrosalpinks
    "ehclsbqGMCo": "4FNpxKs_Imk",  # IUI sperm sayisi
    "hRMedadsG-M": "z6o4sYJwWxo",  # hipotiroidi
    "knaO5bPXSSw": "gG5ma2YRIkk",  # erkek fertilitesi / sperm kalitesi
    "OojCB6GdB50": "aX4XIEcjxVg",  # kac oosit dondurulmeli
    "i43rdWVf5tY": "upmSJEeoqNQ",  # laparoskopik miyomektomi
    "jeWc9oqP_hU": "K85iW-jsjOg",  # azospermi ikinci deneme
    "a3yB02Sc2yA": "Z4TWjY-rZ2s",  # donmus transfer dogal/yapay
    "8E_PJmiDIaE": "y6Fe2xYb0y8",  # mantar/vajinoz
    "tjMDUKMfprE": "y6Fe2xYb0y8",
    "VEaE8TD9rMM": "Uw2xfxw7N48",  # endometriyum kalinligi
    "EzZD9uMGXzc": "ibyu5gWtfQY",  # DHEA/GH
    "8BzQtYcesDU": "IahtBeIzkyo",  # takviyeler
    "1yaT_G_bhK8": "2QpLE_wST1s",  # 40 yas sonrasi FIV
    "3aqQA66Xy7M": "Ks0Cwpy_a4A",  # dusuk AMH
    "tVAgF6CIJzY": "-EG4Q9AsWLU",  # dusuk sonrasi bekleme
    "uEexFyDOzLo": "pUq5UJ3PEH4",  # beta-hCG
}

fixes, report = [], []
for short, long_ in MAP.items():
    s, l = inv[short], inv[long_]
    assert s["privacyStatus"] == "public" and l["privacyStatus"] == "public", (short, long_)
    desc = s["description"]
    assert long_ not in desc and "Vidéo complète" not in desc, short
    line = f"▶ Vidéo complète : https://youtu.be/{long_}"
    if "\n\n" in desc:
        head, tail = desc.split("\n\n", 1)
        new = head + "\n\n" + line + "\n\n" + tail
    else:
        m = re.search(r"\s#", desc)
        if m:
            new = desc[:m.start()].rstrip() + "\n\n" + line + "\n\n" + desc[m.start():].lstrip()
        else:
            new = desc.rstrip() + "\n\n" + line
    fixes.append({"video_id": short, "description": new})
    report.append(f"{short} ({s['title'][:42]}) -> {long_} ({l['title'][:48]})")

json.dump(fixes, open(D + r"\shorts-link-fixes.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(D + r"\shorts-link-map.txt", "w", encoding="utf-8").write("\n".join(report) + "\n")
print(len(fixes), "fixes")
