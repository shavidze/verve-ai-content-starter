# Rationale: plan.fable.json (blind draft, needs_review)

Status: `draft`. Not approved, not rendered. Made without hearing the audio and without reading any other plan for this job.

## What the plan is
A 35.75 s vertical Reel: five talking-head segments (32.75 s) plus a 3 s brand end card.

| # | Clip | Source trim (s) | Timeline (s) | Zoom | Why |
|---|---|---|---|---|---|
| 1 | c01 | 0.80-11.60 | 0.00-10.80 | 1.00 | Longest clean take; opens the piece |
| 2 | c02 | 0.85-6.05 | 10.80-16.00 | 1.08 | Punch-in hides the same-framing jump cut |
| 3 | c03 | 0.70-5.90 | 16.00-21.20 | 1.00 | Back out |
| 4 | c04 | 0.00-7.95 | 21.20-29.15 | 1.06 | Natively slightly tighter; mild punch-in |
| 5 | c05 | 0.00-3.60 | 29.15-32.75 | 1.00 | Ends on the closed-lip smile, then end card |

- Captions: 11 slots, all placeholder (`[ტექსტი NN — ჩასანაცვლებელია]`, flagged `"placeholder": true`). Slot timings split each segment evenly and are provisional.
- Overlay (one): placeholder hook title, 0.3-3.0 s, Smoked Moss box with Cream Silk text (approved large-text pairing), placed below the face and above the caption band.
- End card: Charcoal Noir background, Tanned Leather latin wordmark, address and phone exactly as in `brands/verve.json`. No CTA wording, offer, price or claim.
- Audio: loudnorm -16 LUFS.

## Treatments considered
1. **Chronological first five (chosen).** c01 to c05 in file order, tightened to the speech windows. Least complicated; if the clips are consecutive parts of one script, adjacent clips keep sentences in order.
2. **c07 cold open.** Start on c07 (mouth-closed start, different framing reads as a deliberate first shot), then c01, c02, c04, c05. Rejected for now: reordering speech I cannot hear risks a nonsensical script.
3. **All nine, hard-tightened.** About 53 s of body before the end card; exceeds the 30-45 s brief. Rejected.

## Clip order logic
- Every clip is the same locked-off setup, so no order is better visually. File order is the only evidence of intended sequence, so I kept it.
- c01 to c05 is the longest contiguous run that lands inside 30-45 s with an end card, and c05 gives a visible end-of-statement smile to close on.
- Zoom alternates at each cut (1.00 / 1.08 / 1.00 / 1.06 / 1.00) so cuts read as intentional. Kept low because the 576x1024 sources are already upscaled to 1080x1920.
- Optional extension: adding c06 (0.75-7.75, zoom 1.07) after c05 gives about 42.75 s total, still inside the brief.

## Assumptions
- Clips are consecutive parts of one script, not alternate takes of the same lines.
- Trim points sit in silence. I used ffmpeg `silencedetect` (-35 dB, 0.25 s) on the raw clips for level only; it tells where sound is, not what is said. Durations and 576x1024 / 29.97 fps were confirmed with ffprobe.
- The 0.43 s of sound at the head of c01 and 0.52 s at the head of c02 (each followed by about 0.5 s of silence) are not needed speech. They may be a short word.
- The task brief (30-45 s, five segments) overrides the pilot scope in CLAUDE.md (15-30 s, max three shots).

## Risks
- If the clips are alternate takes, the Reel repeats itself; if sequential, stopping at c05 may drop the ending or call to action in c06-c09.
- The speech may contain statements that fall under `do_not_claim` (guaranteed results, zero risk, medical advice, reviews, before/after). I cannot check this.
- Placeholder captions and overlay will appear in a preview render as placeholders; they must be replaced or removed before approval.
- c04 opens on a blink and cannot be head-trimmed because sound starts at 0.0 s.
- Punch-ins soften an already low-resolution source. The overlay box may partly cover the hand-held object.
- Georgian headers should be mtavruli per the brand book; the overlay text is a mkhedruli placeholder.

## Open questions for the human
1. What is said in each clip, and are they sequential or alternate takes? Which takes are preferred?
2. Verified Georgian text for the 11 caption slots, and the hook title (or delete the overlay)?
3. What is the round object she holds; may it be shown or named?
4. Is presenter consent on record, and is the logo wall fine as framed (cropped letters)?
5. Does anything spoken need cutting under `do_not_claim`?
6. Keep or drop the sounds at the heads of c01 and c02?
7. Is 35.75 s right, or add c06 for about 42.75 s? Any must-keep line in c06-c09?
8. Is a contact-only end card wanted, or a specific approved CTA line?
