---
name: review-reel
description: Check a produced vertical video for mechanical quality and flag human review needs before publishing.
---
# QA
1. Run `python scripts/quality_check.py $ARGUMENTS`.
2. Ask `quality-reviewer` for independent audit based on actual accessible evidence.
3. Compare exported captions with approved plan, verify visible subjects/crop manually, and verify social-safe margin.
4. Confirm actual consent, soundtrack usage rights and no misleading aesthetic/health claims.
5. Produce PASS / FAIL / NEEDS HUMAN REVIEW. Never publish automatically.

## Caption position (owner rule, always)
Captions always go at the BOTTOM of the frame, in the lower third, above the platform UI (brand `caption.margin_bottom`, default 400). Never place captions above the head or at the top of the frame, even if a held prop is partly covered. If a per-job tweak is needed, only `caption_style.margin_bottom` between 330 and 480 is allowed. Top-of-frame space is for the single overlay badge, not captions.
(ტიტრები ყოველთვის ქვემოთ, ქვედა მესამედში. არასდროს თავს ზემოთ ან ეკრანის ზედა ნაწილში.)
