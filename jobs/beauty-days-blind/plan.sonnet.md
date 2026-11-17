# plan.sonnet rationale (blind, draft)

Length: 38.0 s body + 3.5 s end card = 41.5 s (inside the requested 30-45 s; longer than the pilot's 15-30 s guideline in CLAUDE.md, so flag this).

## Clip order logic
All nine clips are one talking-head setup; analysis gives no visual hook/process/result roles and speech is unknown. Order is therefore a placeholder, not a story:
c01 (longest, clean, speaking from 0 s) opens 0-8 s; then c03, c09, c04, c06, c02; c05 closes (closed-lip smile ~3 s, so trimmed to 4.0 s as a soft ending). Trims stay inside sampled, seen ranges; starts of c04/c06 set to 1.0 s to skip the opening blink. Alternating zoom 1.0 / 1.07 on adjacent same-framing clips disguises jump cuts. c07 (different framing) and c08 (blink start, unclear end) are held back as spares. No b-roll exists, so the "max three distinct shots" pilot rule cannot be met; the footage is effectively one shot.

## Captions, overlay, end card
Captions are one per segment, all "[PLACEHOLDER n - ტექსტი გადასაწერია]" (<=7 words). One overlay: hook box 0-2.5 s, walnut/tanned_leather (approved pairing), text "[HOOK - PLACEHOLDER]", placed over the logo wall at the top. End card: charcoal_noir, tanned_leather Georgian wordmark, address/phone/email taken from brands/verve.json. audio.loudnorm = -16. status stays draft.

## Assumptions
- Durations/specs from the brief; durations re-checked with ffprobe, and all trims validate against them.
- Speech is Georgian and on-topic: UNVERIFIED. No claims, prices or results are written.
- Presenter is consented and the VERVE wall is fine to show: UNVERIFIED.

## Risks
- Cuts at sampled-frame boundaries may chop words or sentences; order may contradict the spoken script.
- Hook overlay may sit on top of her head if framing differs; zoom 1.07 crops the logo wall further.
- Held round object is unidentified; if it is a product, claims rules apply.
- Long static placeholder captions per segment: real captions need re-timing to speech.
- Not rendered; no --preview run, so layout and font glyphs are untested.

## Human must supply
1. Transcript or listen-through of c01-c09 (language, claims, audio quality); confirm order and which takes to keep.
2. Georgian caption text and hook line, verified against speech; max 7 words per caption.
3. What the held object is, and whether it may be shown or named.
4. Presenter consent/release; OK to show the logo wall.
5. Any extra footage (space, process); whether 41.5 s is acceptable vs 15-30 s pilot scope; confirm contact lines on the end card.
