# Translation brief — pUaFBOSrAO8 "Spermogramme anormal : est-ce que ça veut dire infertile ?"

Channel @SenaiAksoy (FR). Source approved by Dr. Aksoy 2026-10-18. Audience: couples/men reading a
semen analysis report. Tone: warm doctor with dense stand-up humour in the non-sensitive parts, sober in
the sensitive parts (azoospermia, testicular lump/pain, the doctor's opinion, the closing disclaimer).

## Input
- `source.json` in this folder: `title_fr`, `description_fr`, `cues` = [{i, fr}] (182 cues).
- Cue i is a fragment of a running sentence (cues were cut by timing, a sentence often spans 2–3 cues).
- Reference examples (format/tone only, different topic): `D:\A-klasör\Youtube\youtube-api\glp1-recut-2026-10-16\i18n\<lang>.json`
  and live DHEA localisations in `..\i18n-check\dhea-meta.json` (field `localizations`).

## Output — one file per language: `<lang>.json` in this folder, UTF-8, no BOM
```json
{"lang": "tr", "title": "...", "description": "...", "cues": [{"i": 1, "text": "..."}, ... {"i": 182, "text": "..."}]}
```

## Cue rules (subtitles)
1. Exactly 182 cues, i = 1..182 in order. Cue i renders ONLY what FR cue i says; none empty. When a sentence
   spans cues, split your translation at a natural point so each cue carries roughly the same content as
   its FR cue (word order may differ by language; keep the split close, never move a whole clause 2 cues away).
2. Each cue ≤ 84 characters (hard). Shorten wording, never meaning.
3. Every digit number in the FR cue appears as digits in your cue: 28 (cues 35, 46), 2021 (41), 100 (77),
   27 (109), 2026 (115), 1990 (130), 15 and 112 (163). Words like "quatre/cinq/trois/deux/six sur dix"
   stay as words or digits, but the value must be identical ("cinq sur cent" = 5 out of 100, "quatre sur cent" = 4 out of 100,
   "près de six sur dix" = nearly 6 in 10, "près d'un couple infertile sur deux" = nearly 1 in 2 infertile couples).
4. Never drop or strengthen qualifiers: "idéalement", "peut", "près de", "presque aucun", "ne montre pas de
   baisse nette", "ce sont des études d'observation", "on envisage", "on peut proposer", "ce n'est pas
   toujours possible, personne ne peut le promettre", "c'est un avis, pas une preuve", "à lui seul",
   "pour un homme donné", "petite étude", "trois à cinq jours". No new claims, no added advice.
5. Medical terms in the target language's standard patient vocabulary: spermogram/semen analysis,
   oligo-/astheno-/teratozoospermia (keep the 3 prefixes "oligo", "asthéno", "térato" recognisable — the
   video explains them; cue 36 is the long word, render it in the target language's medical form),
   concentration, motility, progressive, morphology, azoospermia, epididymis, testicle, urologist,
   andrologist, Y chromosome, chromosome analysis (karyotype), hormonal blood test, clinical examination,
   abstinence period, IVF and ICSI (local acronyms: TR tüp bebek / ICSI, AZ EKO / ICSI, AR أطفال الأنابيب / الحقن المجهري,
   FA آی‌وی‌اف / ای‌سی‌اس‌آی, RU/UK ЭКО/ЕКЗ + ИКСИ/ІКСІ, BG инвитро / ICSI, DE IVF/ICSI, ES FIV/ICSI, IT FIVET/ICSI,
   RO FIV/ICSI, others the usual local term + ICSI). OMS = WHO in the local form (TR DSÖ, DE WHO, ES/IT OMS,
   RU/BG ВОЗ, UK ВООЗ, AR منظمة الصحة العالمية, FA سازمان جهانی بهداشت, etc.).
6. "les recommandations britanniques" = the UK (NICE) guidelines — keep "British/UK guidelines", do not add "NICE"
   inside cues. "une grande étude américaine", "une petite étude danoise" keep nationality.
7. Humour: keep every gag, adapt idioms naturally (e.g. "taper une belote" → a local card game/backgammon,
   "au ras des pâquerettes" → local idiom for "rock-bottom", "endocrinologues du développé-couché" → gym
   "bench-press endocrinologists", "progressifs vs progressistes" → keep the word-play if possible, else a
   close pun on "progressive" in politics). Never joke more than the source, never at patients.
   Keep proper nouns: Genève, Brad Pitt, Fashion Week de Paris, Louvre, Wi-Fi.
8. Cue 163: keep "15" and "112" as in FR (French emergency number + 112); do not invent other numbers.
9. Doctor's name (cue 11 and description): AR سيناي أكسوي · FA سنای آکسوی · BG/RU/UK Сенай Аксой ·
   MK/SR Сенај Аксој · all Latin-script languages "Senai Aksoy". SR and MK are written in Cyrillic; BS in Latin.
10. No drug brand names (there are none in the source; "testostérone" stays the generic word).

## Title
≤ 100 characters, patient-language question meaning "Abnormal semen analysis: does it mean infertile?",
natural in the target language, no clickbait, no added promise.

## Description (keep the FR structure exactly, same emoji headers, same order)
- Intro paragraph translated (name per rule 9; "spécialiste de la fertilité").
- "⏱️ <CHAPTERS>" with IDENTICAL timestamps (00:00, 01:11, 03:05, 03:33, 04:39, 06:00, 07:18, 08:11, 10:04,
  11:05, 13:15, 13:39, 14:20), each line `MM:SS <translated chapter>`; first line must start with 00:00.
- "❓ <THE THREE QUESTIONS TO ASK YOUR DOCTOR>" 1./2./3. translated.
- "🚨" urgent line translated; keep "15" and "112"; you may write "15 (France)".
- "📚 <REFERENCES>" header translated, the 9 reference lines copied UNCHANGED from French (byte-identical).
- 💬 comment line and 🔔 subscribe line translated.
- Replace "Sous-titres français disponibles." with ONE line: "🌍 <Language> subtitles available; the original
  audio of the video is French." (see GLP-1 examples).
- "Pour plus amples informations :" translated; `📱 WhatsApp: +90 507 380 28 05` and `🌐 <Website>: www.draksoyivf.com`
  values unchanged.
- "⚕️ <IMPORTANT MEDICAL DISCLAIMER>" — 4 paragraphs translated faithfully (reuse the wording of the same
  disclaimer in the GLP-1 `<lang>.json` description where it matches; adapt "FIV" to the local IVF term).
- "© <Assoc. Prof. Dr. in local form> Senai Aksoy — <All rights reserved>." (copy the GLP-1 `<lang>.json` line).
- Last line: 3 local hashtags (e.g. TR #Spermiyogram #ErkekKısırlığı #TüpBebek) — no spaces inside a hashtag.
- ≤ 5000 characters.

## Self-check before handing back (Python 3.12, read files as UTF-8, print to a UTF-8 file, not the console)
- 182 cues, i 1..182, none empty, each ≤ 84 chars; digit numbers present per rule 3.
- Title ≤ 100; description contains all 13 timestamps and the 9 reference lines byte-identical; WhatsApp and site present.
- Then run: `py -3.12 "D:\A-klasör\Youtube\.claude\skills\yt-pipeline\scripts\yt_i18n.py" build --dir "<this folder>" --video pUaFBOSrAO8 --langs <your langs> --stem spermogramme-anormal`
  and make it exit 0 (it also rewrites qa.json/fixes-localizations.json — that is fine, the lead re-runs it for all languages).
- Never call the YouTube API, never upload anything.
