# Subtitles and localisations — FR channel long videos (learned 2026-10-16, GLP-1 video U-ophcWNOro)

## Language set
- Default = the set used on the DHEA video `dYF3NWf4Nw8`, 15 languages:
  `ar, az, bg, bs, de, es, fa, it, mk, ro, ru, sq, sr, tr, uk`.
- English (`en`) is decided per video: on GLP-1 Dr. Aksoy first said "no EN", then asked to add it.
  Ask when unclear. Mention that the EN channel @DrAksoyFertility may carry its own version.
- Each language gets BOTH a localisation (title + description in `localizations`) AND a caption track.
- Before adding languages to a new video, read the reference video live
  (`yt_captions.py list`, `yt_metadata.py get`) to confirm the set has not changed.

## French SRT (source of every translation)
1. Transcribe the final audio with faster-whisper `large-v3` (`~/.claude/skills/yt-video-postprod/scripts/asr_words.py
   --model large-v3 --lang fr`; default Python, not 3.12). Medium-model ASR garbles drug names.
2. Correct per segment in a JSON (drug INNs, homophones such as satiété/rassasiés/hâtive/report,
   words lost in the edit restored only where grammar needs them). Check doubtful words against the script
   or the EN dub script; when still unsure, ask Dr. Aksoy (e.g. "létrozole" was confirmed by him).
3. Align corrected words to ASR word times; cues ≤ 2 lines × 42 chars, ≤ ~7 s, break at punctuation,
   French non-breaking space before ? ! : ; and inside « ».
4. Show the FR text to Dr. Aksoy (hard rule 5), upload as a standard `fr` track named "Français".
5. Delete YouTube's automatic `fr` ASR track (`trackKind: asr`) when he asks — he did on GLP-1.

## Translation (quality bar)
- Do NOT use `yt_captions.py translate` (GoogleTranslator) for these channels; translate with Claude
  subagents, 3 languages per agent, in parallel.
- Workspace: `py -3.12 scripts\yt_i18n.py prep --srt fr.srt --title "..." --desc description-fr.txt --dir i18n`
  → agents write `i18n/<lang>.json` = `{lang, title, description, cues:[{i,text}]}`.
- Brief every agent with: cue i renders only FR cue i (exact count/order, none empty); ≤ 84 chars per cue;
  never drop qualifiers ("chez certaines femmes", "au moins", "peut", "associé", "pas de preuves solides",
  "observationnel"); numbers identical; GLP-1/GIP unchanged; INN drug names in the target language; no brand
  names; local terms for PCOS/IVF (e.g. TR PKOS + tüp bebek, AZ PKYS + EKO, AR متلازمة تكيس المبايض +
  أطفال الأنابيب, RU/UK СПКЯ + ЭКО/ЕКЗ, BG СПКЯ + инвитро, DE PCOS + IVF, ES SOP + FIV, IT PCOS + FIVET,
  RO SOPC + FIV); title ≤ 100 chars, patient-language question, no clickbait; description keeps the FR
  structure, IDENTICAL chapter timestamps, the reference lines copied unchanged from French, WhatsApp
  number and www.draksoyivf.com unchanged, translated disclaimer, one line "subtitles available,
  original audio French", 3 local hashtags; self-check in Python before handing back.
- Doctor's name must match the DHEA localisations: AR سيناي أكسوي, FA سنای آکسوی,
  BG/RU/UK Сенай Аксой, MK/SR Сенај Аксој, Latin "Senai Aksoy" elsewhere.

## QA and upload
1. `py -3.12 scripts\yt_i18n.py build --dir i18n --video ID --langs <list> --stem <slug>` must exit 0
   (cue count/order, digits incl. Persian digits, brands, title/description limits, timestamps).
   It writes `i18n/srt/<slug>.<lang>.srt` with the FR timings and `i18n/fixes-localizations.json`.
2. Spot-read the safety-critical cues (stop delays, contraception, pregnancy on treatment) in TR and one
   more language; Dr. Aksoy can read TR.
3. Dry-run, show, then `--go` on approval:
   `yt_metadata.py --channel fr update --fixes i18n\fixes-localizations.json` (merges; French snippet untouched)
   and one `yt_captions.py upload --lang <code> --name "<native name>"` per language.
   Native names: العربية, Azərbaycan dili, Български, Bosanski, Deutsch, English, Español, فارسی, Italiano,
   Македонски, Română, Русский, Shqip, Српски, Türkçe, Українська.
4. Quota: each caption insert ≈ 400 units; 16 tracks ≈ 6,400 of the 10,000 daily units. Verify with
   `yt_captions.py list` + `yt_metadata.py get` (cheap); avoid caption downloads for verification.
5. Report honestly that translations had no native-speaker review.
