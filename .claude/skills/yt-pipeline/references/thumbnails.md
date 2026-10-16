# FR long-video thumbnails — channel style (learned 2026-10-16, GLP-1 video U-ophcWNOro)

Master rules stay in `youtube-content/10-thumbnail-production-library.md` (1280×720, ≤ 2 MB, 120×68
mobile test) and compliance F13 (`youtube-content/02-compliance-checklist.md`). This file records what
Dr. Aksoy actually accepted on @SenaiAksoy and how it was produced.

## Look before you design
Download the channel's recent thumbnails first and copy their style; do not invent a new one.
`yt_channel.py --channel fr list --max 50`, then `yt_metadata.py get` per video and read
`snippet.thumbnails.maxres.url`. Contact-sheet them and look.

Channel long-video style (2026-06 → 10, best performers bêta-hCG 3,258 views, FIV à l'étranger 8,300):
- Dr. Aksoy on the RIGHT third, chest-up, navy medical scrubs (or white shirt), calm slight smile,
  mouth closed, looking at camera, professional studio light.
- Deep navy/teal scientific backdrop: blurred cells, a few molecule models, soft bokeh.
- Left 55 %: big white condensed bold CAPS keyword, gold accent line (usually the question),
  gold rounded pill with a short label ("LES PREUVES", "CE QUE DISENT LES ÉTUDES").
- Text complements the title; it does not repeat it.

## Rejected by Dr. Aksoy (do not reuse)
- The burgundy/cream "premium" layout with the dark-suit portrait cut from the DHEA thumbnail
  ("seçtiğin Dr Aksoy fotosu güzel değil").
- Frames grabbed from the talking-head footage: mouth open mid-word, webcam look.

## Production
1. Identity references: upload 1–2 approved channel thumbnails with Higgsfield `media_upload` → curl PUT →
   `media_confirm`. Best: `pUq5UJ3PEH4` (bêta-hCG, scrubs, hand on chin), `SD3CKpN6VS0` (Compléments).
2. Base image: Higgsfield `generate_image`, model `gpt_image_2_5`, `quality: high`, `resolution: 2k`,
   `aspect_ratio: 16:9`, `count: 2` (≈ 2.75 credits for both; preflight with `get_cost`).
   Prompt essentials: same man as the references, keep identity exactly, natural skin, no beautification;
   navy scrubs; right third; calm warm slight smile, mouth closed; navy/teal backdrop with blurred cells
   and a few ball-and-stick molecules; LEFT 55 % calm and dark for text; STRICTLY no text, letters,
   numbers, logos, syringe/injection pen, pills, pregnant belly, baby, arrows, warning signs, red.
3. Never let the image model write the words. Add type with
   `py -3.12 scripts\yt_thumb_compose.py --base base.png --out fr-thumb-00-<slug>-A.jpg --line1 "KEYWORD" --line2 "QUESTION ?" --pill "LABEL"`
   (Bahnschrift condensed, white / gold #F0BE50 / navy pill text, French non-breaking spaces).
4. Check: identity matches the references, hands/glasses not deformed, mobile proof readable
   (`*-mobile.png`), ≤ 2 MB. Show both variants to Dr. Aksoy and recommend one.
5. Upload the chosen one: `yt_thumbnail.py --channel fr set --video ID --file X.jpg` (dry-run) → `--go`
   after approval → `yt_metadata.py get` and check `snippet.thumbnails`. The second variant is for
   Studio "Test & Compare" (Studio UI only).

## Hard no (F13 + library)
Pen strikes, stamps, red circles, arrows, ⚠ signs, "%" claims, shocked faces, injector close-ups,
pregnant belly, baby, drug brand names, clinic logo/name. The Outsider Inside red-pen vocabulary
lives inside the video only.
