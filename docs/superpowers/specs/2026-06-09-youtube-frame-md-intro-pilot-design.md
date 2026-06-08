# YouTube Frame.md Intro Pilot Design

## Status
- Date: 2026-06-09
- Scope: 15-second YouTube/Shorts intro motion pilot
- Decision: one shared motion structure with two brand skins
- Approval: user approved the shared structure plus TR/FR skin direction

## Goal
Create a compact motion design pilot for channel intros that can prove whether a
Frame.md / HyperFrames-style workflow is useful for this YouTube system.

The pilot should produce a reusable 15-second intro specification that:
- works for both the TR and FR channels
- keeps one shared animation structure
- switches visual skin by channel and linked site
- avoids the old burgundy/gold/cream assumption
- can later be implemented as HyperFrames HTML/video output

## Current Context
The repository already contains YouTube operational memory for scripts,
thumbnails, channel metadata, and production workflows. Earlier thumbnail notes
mention a burgundy/gold/cream palette, but the user clarified that the current
channel linkage should instead follow the live site identities:

- FR channel: connected to `https://draksoyivf.com`
- TR channel: connected to `https://tupbebek.com`

The intro system must respect this distinction instead of forcing one color
palette across both channels.

## Source References
- `https://draksoyivf.com/`
- `https://tupbebek.com/`
- `youtube-content/01-voice-checklist.md`
- `youtube-content/10-thumbnail-production-library.md`
- `youtube-content/channel-operations-memory-2026-05-01.md`
- `youtube-content/senaiaksoy-fr-channel-operations-summary-2026-05-02.md`

## Brand Findings

### FR Skin: draksoyivf.com
The FR-facing clinic site reads as an international clinical care experience:
structured, calm, patient-oriented, and connected to IVF treatment in Istanbul.

Observed visual cues:
- primary deep blue: `#094183`
- rose accent: `#e8578a`
- white and pale grey clinical surfaces
- restrained form and CTA styling
- tone: clinic, trust, multilingual care, Istanbul

### TR Skin: tupbebek.com
The TR site reads more like an educational fertility information portal:
article-led, structured, accessible, and search/intention oriented.

Observed visual cues:
- primary blue: `#2563a8`
- deeper blue: `#1a4d7a`
- supporting green: `#3a8a66`
- light blue surface: `#f0f7ff`
- tone: education, evidence, patient understanding

## Approaches Considered

### 1. Shared motion structure with two skins
Use one timing model and composition logic, then apply channel-specific colors,
copy, and final identity line.

Pros:
- efficient pilot
- easy to maintain
- clearly respects both site identities
- lets future videos swap text without rebuilding the whole animation

Cons:
- each skin still needs separate visual QA

### 2. Fully neutral Dr. Aksoy intro
Use mostly white/grey plus Dr. Aksoy identity, with minimal site color.

Pros:
- lowest visual risk
- easiest to reuse everywhere

Cons:
- weaker connection to each channel's actual web identity
- less useful as a Frame.md brand-system test

### 3. Two separate intros
Design completely separate TR and FR intro systems.

Pros:
- maximum channel differentiation

Cons:
- too much scope for the first pilot
- harder to maintain
- weakens the test of a reusable Frame.md workflow

## Recommended Approach
Use approach 1: shared motion structure with two skins.

This is the best pilot because it tests the real value proposition of Frame.md:
stable motion rules with channel-specific brand interpretation. It also keeps
the first implementation small enough to verify visually.

## Intro Structure

### 0-3 seconds: Brand Field
Open with a clean, calm background field. Subtle line motifs suggest fertility,
laboratory precision, education, and care without using literal baby imagery or
sensational medical visuals.

TR behavior:
- light blue or white base
- primary blue accents
- optional green micro-accent
- more educational/information-portal feel

FR behavior:
- white or deep-blue base depending on contrast needs
- rose accent used sparingly
- more clinic/international patient-care feel

### 3-8 seconds: Main Title
Large title text enters with measured motion. It should feel precise and calm,
not like a loud social-media splash screen.

Default TR example:
`Tup Bebekte Dogru Bilgi`

Default FR example:
`Comprendre la FIV avec clarte`

The title is a variable. For per-video use, it can be replaced with a specific
topic title.

### 8-12 seconds: Identity Line
Show the Dr. Aksoy identity line and channel/site context.

Default TR:
`Dr. Senai Aksoy | Ureme Sagligi`

Default FR:
`Dr. Senai Aksoy | FIV a Istanbul`

### 12-15 seconds: Transition Out
Resolve into a title-card-like final frame, then transition to the main video
with a soft wipe or fade. The end state should be useful as a paused frame and
should not obscure the first spoken beat of the video.

## Motion Direction
The approved tone is calm clinical editorial with a small amount of Shorts
energy.

Motion rules:
- moderate pacing, no frantic cuts
- title entrance should be clear within mobile view
- no clickbait bounce, shake, alarm, warning, or red-circle visual language
- line motifs may draw in, drift, or wipe gently
- transitions should feel intentional and quiet
- final frame should hold long enough to read

## Components

### `DESIGN.md`
The brand reference document for the pilot.

Responsibilities:
- describe shared Dr. Aksoy motion identity
- define TR skin colors, typography, surfaces, and tone
- define FR skin colors, typography, surfaces, and tone
- define forbidden visual language
- define reusable copy slots

### `FRAME.md`
The motion-specific document for the pilot.

Responsibilities:
- define the 15-second timing model
- define composition zones for 16:9 output
- define title, identity, accent, and transition behavior
- define mobile-safe text limits
- define how TR and FR skins map onto the same sequence

### Optional Future HyperFrames Composition
After the spec is approved, implementation can create an HTML composition that
uses the `DESIGN.md` and `FRAME.md` documents as source guidance.

Potential output path:
`youtube-content/motion/intro-pilot/`

## Data Flow
The intended workflow is:

```text
channel choice + title text
  -> DESIGN.md skin rules
  -> FRAME.md motion rules
  -> HyperFrames/HTML composition
  -> preview snapshots
  -> rendered intro video
```

For the pilot, TR and FR should use the same title slots and timing. Only skin,
language, and identity line change.

## Safety And Compliance
The intro must not include:
- success-rate claims
- guarantee language
- before/after imagery
- baby imagery used as emotional leverage
- patient faces or patient stories
- clinic address, price, discount, or promotional offer
- sensational words such as miracle, guaranteed, shocking, or secret
- aggressive red/orange warning graphics

The intro may include:
- Dr. Aksoy identity
- site-aligned colors
- general fertility/IVF educational framing
- abstract or clinical line motifs
- evidence-oriented tone

## Testing And Verification
The implementation plan should require:
- preview at 16:9 desktop resolution
- mobile readability check by viewing the intro at thumbnail/small player scale
- color check against the two live site skins
- text overflow check for long TR and FR titles
- final-frame screenshot for both TR and FR variants
- visual check that motion is calm, readable, and non-clickbait

## Open Constraints
No logo or portrait asset has been approved for use in this pilot. The first
implementation should therefore use text identity and abstract visual motifs
unless the user supplies or approves assets later.

## Out Of Scope
- full video editing
- long-form YouTube episode production
- voiceover generation
- thumbnail redesign
- YouTube upload automation
- separate TR and FR motion systems

## Success Criteria
The pilot is successful if it produces:
- one approved `DESIGN.md`
- one approved `FRAME.md`
- two clear skin variants: TR and FR
- a path to render a 15-second intro prototype
- no reliance on the rejected burgundy/gold/cream palette
