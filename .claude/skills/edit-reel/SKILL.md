---
name: edit-reel
description: Render an already-approved short vertical video plan into an MP4 with local FFmpeg tooling.
---
# Render approved Reel
1. Read plan: `$ARGUMENTS`.
2. Confirm `status` is `approved` and that approval came from a person, not an agent.
3. Run `python scripts/render.py $ARGUMENTS`.
4. Run `python scripts/quality_check.py $ARGUMENTS`.
5. Record file location and issues; route to independent reviewer.
6. Never auto-publish or assume client consent.

## Caption position (owner rule, always)
Captions always go at the BOTTOM of the frame, in the lower third, above the platform UI (brand `caption.margin_bottom`, default 400). Never place captions above the head or at the top of the frame, even if a held prop is partly covered. If a per-job tweak is needed, only `caption_style.margin_bottom` between 330 and 480 is allowed. Top-of-frame space is for the single overlay badge, not captions.
(ტიტრები ყოველთვის ქვემოთ, ქვედა მესამედში. არასდროს თავს ზემოთ ან ეკრანის ზედა ნაწილში.)
