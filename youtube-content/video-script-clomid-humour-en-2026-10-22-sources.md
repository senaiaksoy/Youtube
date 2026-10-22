# Clomid (humour) EN dub script: notes, 2026-10-22

Files:
- EN target transcript: `video-script-clomid-humour-en-2026-10-22.txt` (28 paragraphs, body only)
- FR recording script, paragraph-aligned: `video-script-clomid-humour-en-2026-10-22-fr-recording.txt` (the approved FR script with stage directions removed and the recorded ad-lib "Allez, ciao !" added)
- Claim registry and fact-check: `video-script-clomid-humour-fr-2026-10-21-sources.md` (C01–C15, clinical approval 2026-10-21). The EN text makes the same claims; no new claim was added.

## How it was aligned

Source of truth is what Dr. Aksoy actually said: `openmontage/projects/2026-10-21-clomid-humour-fr-recut/analysis/segments.txt` (Whisper medium, cut-timeline seconds, 570.77 s). I compared it with the FR script before translating. The recording follows the script sentence by sentence, with these differences:

| Recording | Script | Handling |
|---|---|---|
| 16.2 s "Oui et non ?" | "oui ou non ?" | Almost certainly an ASR error (it contradicts the next sentence). EN uses "yes or no". **Check against the audio before TTS.** |
| 570.1 s "Allez, ciao !" | not in script | Ad-lib at the very end. EN: "Alright, ciao!". Drop it if you cut it from the dub. |
| 64.5 s "ce fameux calendrier est mort sous le frigo" | (not in script) | ASR artifact for the "Imaginez la table de la cuisine…" passage (note in segments.txt says this was confirmed by a second pass). EN follows the script. |
| Rest | | Same wording, minus ASR noise. |

## Length alignment (characters, EN / FR)

Total 0.88 (EN is about 12% shorter, normal for FR to EN). 21 of 28 paragraphs are within 0.80–1.01; the outliers are the very short ones (para 8 0.77, 23 0.69, 24 0.76) and para 7, 10, 13, 22 at 0.78–0.82. Character count is only a proxy. Speaking time decides, and ElevenLabs dubbing time-stretches to the FR audio. Estimated EN read time 3.5 to 8.4 min at 130–150 wpm (script_timing), against 570 s for the recording, so expect the EN voice to sit slightly relaxed. Padding the EN text to force parity was not done.

Readability: Kandel-Moles 83, FK grade 7.1, 12.7 words per sentence, 15% of sentences over 20 words (at the limit).

## Localization choices (US + UK shared EN)

- "pharmacie de garde" → "late-night pharmacy"; "frein à main" → "parking brake" (a "handbrake" is UK-only); "stabilo fluo" → "neon highlighter"; "les amis" → "folks"; "salon de thé" → "tea-and-gossip crowd"; "opération bikini" → "get bikini-ready diet"; "carte de fidélité" → "loyalty card".
- "La notice française" → "The French prescribing information". Kept French-specific on purpose: the claim (maximum of six cycles, three courses without ovulation) comes from the French RCP, not from a US or UK label. Do not generalize it to the US or UK.
- No regional slang, no sarcasm, no hype words. US spelling in subtitles and description (estrogen, ultrasound).
- Interjections as words: "Okay", "Oh no", "Come on". Not listened to after dubbing yet.

## Decisions for Dr. Aksoy

1. **Emergency numbers.** The EN checklist asks for "call your local emergency number — 911 in the US, 999 in the UK". The FR recording says only "c'est une urgence médicale, n'attendez pas votre prochain rendez-vous". Adding the numbers to the audio would break sync with the recording. Proposed: keep the dub aligned and put "911 (US) · 999 (UK)" in the on-screen text of that scene and the first lines of the description. Say if you would rather add the sentence to the audio.
2. **"Sister-in-law had triplets / take two pills" joke.** Kept as in the approved FR (framed as bad advice). The 2026-10-20 sober version had removed it.
3. **Dub disclosure.** Add the AI dubbing note to the description and enable the Studio disclosure (EN channel rule). Lip-sync not planned yet.

## Medical content: inherited checks

The EN text keeps these as the FR does: letrozole first-line only for anovulatory PCOS with no other infertility factor (2023 international guideline §5.3.1); six cycles maximum and three courses without ovulation (French RCP §4.2); clomiphene alone in unexplained infertility with timed intercourse has not shown benefit (Hughes 2010 Cochrane, NICE NG257 §1.38.2); permanent stop and full eye exam if visual symptoms have no other cause (RCP §4.4); endometrial thinning (RCP §4.8); multiple pregnancy (RCP §4.4).

EN-specific review done: negation, hedges ("nothing shows", "hasn't been shown", "can thin", "several follicles") and numbers match the FR line by line. Done by the writing agent only; no independent EN re-check yet.

## Status

Draft. Scientific check: inherited from the FR registry (2026-10-21, clinical approval by Dr. Aksoy), EN wording compared by the same agent, not independently. Native-speaker check: not done. Read aloud: not done. Dub interjections: not listened to.

## Production update (2026-10-22)

- Dub generated with ElevenLabs (senai1, Eleven v4, English, WAV 48 kHz) in four chunks; two paragraph-seam bugs found and fixed after the first mux (a "parking brake" echo at 0:44, "All right" split across two paragraphs). Re-transcription of the corrected track: 1,093 script words vs 1,110 heard, similarity 0.977, no repeated syllables at seams.
- The EN voice is about 25% shorter than the FR recording. The final cut removes the silent gaps (7:11, 430.63 s) instead of keeping the 570.77 s FR timing; each paragraph start is still synced to the FR picture.
- Open: 1:55 "estrogen sensors" pronunciation (second ASR heard "senses"), listening pass, native-speaker check, AI-dub disclosure in the description. Emergency numbers 911/999 are on screen in s38 (not in the audio).
- Graphics, QC and measurements: `openmontage/projects/2026-10-22-clomid-humour-en-recut/final/KALITE-KONTROL-EN.md`. Final video: `Downloads\Clomid-EN-grafikli-tight.mp4`.
