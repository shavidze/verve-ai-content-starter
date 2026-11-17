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
