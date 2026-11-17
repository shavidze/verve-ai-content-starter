# Verve Reel: blind plan (opus), status: draft / needs_review

Inputs: analysis.md, sheets/c01-c09.jpg (viewed c01), brands/verve.json, the plan.example.json schema, render.py. I could not hear the audio, so every caption is a marked placeholder.

## Concept (picked as the simplest one that works)
A single-presenter talking-head piece from the one setup in the footage: presenter in front of the VERVE wall, holding a small round object. There is no treatment, process or b-roll footage, so alternative treatments (process montage, before/after) are not feasible and were dropped. Structure: hook overlay (0-2.5 s) over the opening lines, then 4 more talking beats, a smiling closing beat, and a brand end card with contact details.

## Clip order logic
- Used c01 > c02 > c03 > c04 > c05 in filename order. Assumption: the filenames follow recording/script order. That is the only ordering signal available without audio.
- c01 opens because it is the longest clean take and the speaker looks straight at the camera from frame 0.
- c05 closes because its closed-lip smile at about 3 s reads visually as the end of a statement.
- c06-c09 are left out to keep the cut at about 40 s. They are alternatives if the transcript shows better lines. c07 has a different framing and would add a visible jump.
- Whole clips are kept where possible (clip boundaries are the most likely sentence boundaries). Only c04's blink at 0 s is trimmed (start at 0.6).
- Jump cuts: the zoom alternates 1.0 / 1.06 between clips that share the same framing (c01 > c02 > c03, c04 > c05). c04 is natively tighter, so it gets no zoom.

## Timeline (about 42.7 s)
| # | Source | Trim (s) | Zoom | Final (s) |
|---|---|---|---|---|
| 1 | c01 | 0.0-12.2 | 1.00 | 0.0-12.2 |
| 2 | c02 | 0.0-7.2 | 1.06 | 12.2-19.4 |
| 3 | c03 | 0.0-6.5 | 1.00 | 19.4-25.9 |
| 4 | c04 | 0.6-9.4 | 1.00 | 25.9-34.7 |
| 5 | c05 | 0.0-4.5 | 1.06 | 34.7-39.2 |
| End card | Charcoal Noir, Tanned Leather wordmark, address and phone from verve.json | | | 39.2-42.7 |

Overlay: one only, 0-2.5 s, Smoked Moss box with Cream Silk text (approved for large text), placed at y 200-380 over the logo wall above her head. Captions use the brand caption style (max 7 words, bottom margin 400). Audio: loudnorm -16 LUFS.

## Brand and claim compliance
- No efficacy, results, pricing, reviews or product claims. The end card uses only the contact facts from verve.json.
- Palette pairings come only from approved_pairings and approved_color_variations. Motion: no added effects beyond the renderer's fades.

## Assumptions
- Clips are sequential parts of one script, not alternate takes of the same lines.
- The audio is usable and is Georgian speech.
- The unseen tails (c01 after 10.5 s, c03 after 4.5 s, c04 after 7.5 s, c05 after 3.0 s) contain no bad moments.

## Risks
- **Order and trims may be wrong.** If the clips are alternate takes, this order repeats lines. A word can also be cut at a clip end, which loudness normalisation will not fix.
- **Placeholder text could ship.** The preview will show "[PLACEHOLDER ...]" text on screen. That is intentional, so it cannot be mistaken for final copy.
- **Upscale softness.** The source is 576x1024 upscaled to 1080x1920, plus a 6% punch-in.
- **Same visual for 39 s.** One unchanging shot may hurt retention, so captions and the hook carry the whole piece.
- **Length conflicts with the pilot scope.** CLAUDE.md sets the pilot at 15-30 s and 3 shots max. This brief asks for 30-45 s. A 25 s cut would be c01 + c02 + c05.
- **Overlay may touch her hair** if her head rises. Check on the preview.

## Human must supply / open questions
1. A verified transcript of c01-c05 (and c06-c09 if any are swapped in), split into 7-word-or-shorter Georgian captions on real phrase timings.
2. Hook text for the overlay, taken from what she actually says, or a decision to drop the overlay.
3. Are the clips sequential parts or alternate takes? Which takes does she prefer?
4. What is the round object, and may it or the product be named?
5. Presenter consent/release, and approval to show the logo wall.
6. Final length: 30-45 s (this brief) or 15-30 s (pilot scope).
