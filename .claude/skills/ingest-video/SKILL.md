---
name: ingest-video
description: Ingest and inspect a local raw video before any editing, including source media technical checks and consent review.
---
# Video ingestion
1. Check clip is local and legally usable. Do not upload it.
2. `python scripts/inspect.py $ARGUMENTS`.
3. Verify resolution, FPS, audio, duration, orientation, visual safety and who is visible.
4. Use the `footage-analyst` agent if detailed analysis is useful.
5. Deliver a brief shot inventory with limitations; never invent what is in a frame.
