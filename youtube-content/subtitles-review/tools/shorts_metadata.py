"""FR Shorts metadata (title/description/tags) following the channel's recent Shorts pattern. -> shorts-metadata.json + shorts-metadata.md"""
import json
from pathlib import Path

OUT = Path(r"D:\A-klasör\openmontage\projects\premiere-echographie-fr-motion-2026-10-09\shorts")
FULL = "https://youtu.be/MoApIs3-WwE"
BLOCK = """Pour plus amples informations :
📱 WhatsApp : +90 507 380 28 05
🌐 Web site : www.draksoyivf.com

⚕️ AVERTISSEMENT MÉDICAL IMPORTANT

Les informations présentées dans cette vidéo sont fournies à titre éducatif et informatif uniquement. Elles ne constituent en aucun cas un avis médical, un diagnostic ou une recommandation de traitement personnalisée.

Chaque situation médicale est unique. Les contenus abordés ici ne remplacent pas une consultation avec un médecin qualifié, un gynécologue ou un spécialiste en médecine de la reproduction.

Ne modifiez jamais votre traitement médical en cours, ne commencez pas un nouveau traitement et ne prenez aucune décision médicale sur la base des informations contenues dans cette vidéo, sans avoir préalablement consulté votre médecin traitant ou votre spécialiste.

Si vous avez des questions concernant votre santé reproductive ou votre prise en charge en FIV, veuillez consulter un professionnel de santé qualifié.

© Assoc. Prof. Dr. Senai Aksoy — Tous droits réservés."""
BASE_TAGS = ["FIV", "échographie FIV", "première échographie", "activité cardiaque", "PMA", "fertilité", "Dr Senai Aksoy"]
S = [
 ("s1-signes-alerte", "Après l’échographie de FIV : 4 signes à ne jamais ignorer #Shorts",
  "Douleur vive au bas-ventre, douleur à la pointe de l’épaule, malaise, saignements abondants : le Dr Senai Aksoy rappelle les signes qui ne doivent jamais attendre le prochain rendez-vous. En cas de doute : urgences, 15 / 112 ou le numéro d’urgence de votre pays.",
  None, ["grossesse extra-utérine", "signes d'alerte", "urgences grossesse"]),
 ("s2-silence-medecin", "Le silence du médecin à l’échographie de FIV : que fait-il ? #Shorts",
  "Pendant l’échographie, le médecin se tait… et ce n’est le plus souvent pas inquiétant : il place un curseur au millimètre près sur un embryon minuscule. Le Dr Senai Aksoy raconte la scène.",
  None, ["échographie endovaginale", "embryon"]),
 ("s3-coeur-pas-visible", "Pas de cœur visible à l’échographie de FIV : mauvais signe ? #Shorts",
  "Pas d’activité cardiaque visible à une échographie très précoce ? Ce n’est pas forcément mauvais signe : parfois, c’est simplement trop tôt, et un contrôle permet de conclure. Le Dr Senai Aksoy explique.",
  None, ["pas de battement de coeur", "6 SA", "contrôle échographie"]),
 ("s4-combien-continuent", "Cœur vu à l’échographie de FIV : combien de grossesses continuent ? #Shorts",
  "Sur dix grossesses de FIV où l’on a vu le cœur battre, combien continuent ? Le Dr Senai Aksoy présente des repères statistiques issus d’études, par âge : des groupes, pas votre situation individuelle.",
  "Études présentées : Spandorfer, Fertil Steril 2004 · Yi et al., Reprod Biol Endocrinol 2016", ["statistiques FIV", "fausse couche", "âge maternel"]),
 ("s5-pourquoi-5-sa", "Pourquoi « 5 SA » alors que le transfert date de 16 jours ? #Shorts",
  "Transfert d’un blastocyste il y a 16 jours… et « félicitations, vous êtes à 5 semaines » ? Le Dr Senai Aksoy explique pourquoi les semaines d’aménorrhée (SA) se comptent depuis le premier jour des dernières règles.",
  None, ["semaines d'aménorrhée", "SA", "transfert blastocyste"]),
 ("s6-trois-reperes", "Échographie de FIV : les 3 repères que cherche le médecin #Shorts",
  "Quels repères le médecin cherche-t-il à l’échographie après FIV, et dans quel ordre : sac gestationnel, vésicule vitelline, embryon avec activité cardiaque. Le Dr Senai Aksoy détaille ce que l’on voit, et quand.",
  None, ["sac gestationnel", "vésicule vitelline", "embryon"]),
 ("s7-echo-5-sa", "Échographie à 5 SA après FIV : ce qu’elle peut (et ne peut pas) dire #Shorts",
  "Une échographie vers 5 SA après FIV : à quoi sert-elle, et pourquoi risque-t-elle surtout de laisser une réponse incomplète ? Le Dr Senai Aksoy donne son avis clinique.",
  None, ["échographie précoce", "5 SA"]),
]
rows = []
for cid, title, summary, extra, tags in S:
    parts = [title.replace(" #Shorts", "") + " " + summary, f"▶ Vidéo complète : {FULL}"]
    if extra:
        parts.append(extra)
    parts.append("#FIV #Échographie #Fertilité")
    desc = "\n\n".join(parts) + "\n\n" + BLOCK
    assert len(title) <= 100 and len(desc.encode()) < 5000
    rows.append(dict(file=f"{cid}.mp4", title=title, description=desc, tags=BASE_TAGS + tags, categoryId="27", defaultLanguage="fr"))
(OUT / "shorts-metadata.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
md = ["# Shorts FR — première échographie (7 vidéos)", ""]
for r in rows:
    md += [f"## {r['file']}", f"**Titre :** {r['title']}", "", r["description"].split("\n\nPour plus amples")[0], "", f"Tags : {', '.join(r['tags'])}", ""]
(OUT / "shorts-metadata.md").write_text("\n".join(md), encoding="utf-8")
print(len(rows), "shorts; titles:", [len(r["title"]) for r in rows])
