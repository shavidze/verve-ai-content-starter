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
