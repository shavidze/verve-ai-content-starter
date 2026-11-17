# Universal AI Content System — MVP Starter

A project-based Claude Code agents + skills setup, with an executable FFmpeg-based pilot editor. Built for a Georgian aesthetic-center Reels pilot and designed to generalize to other clients.

**Status:** Starter / proof of concept. The included pipeline can inspect video, cut selected intervals, reframe to 9:16 with center crop, add human-reviewed Georgian captions, render MP4, and run mechanical QA checks. It does **not** automatically transcribe, track faces, choose music, publish, or validate medical claims. Those require later implementation and human review.

## Requirements
- Claude Code (for orchestration; not required for direct Python scripts)
- Python 3.10+
- FFmpeg and FFprobe on PATH, with libass subtitles support
- No Python pip dependencies

## Try the demo

From this project's root:

```bash
python scripts/make_demo.py
python scripts/inspect.py jobs/demo/input.mp4
python scripts/render.py jobs/demo/plan.json
python scripts/quality_check.py jobs/demo/plan.json
```

This creates `jobs/demo/output.mp4` as a local synthetic test, with a small baseline quality report. **Synthetic footage is not an example of premium visual quality**; it verifies the media pipeline runs.

## Run with an actual aesthetic-center clip
1. Put a copy of an authorized raw clip at `jobs/pilot/input.mp4`. Do not commit it to Git.
2. Copy `jobs/pilot/plan.example.json` to `jobs/pilot/plan.json`. Change `segments` and `captions` to match the actual source. Caption times refer to the **final assembled timeline**, starting at zero. Leave `status: draft` until a person approves this specific plan; then change it to `approved`.
3. `python scripts/inspect.py jobs/pilot/input.mp4`
4. In Claude Code, run `/storyboard jobs/pilot/input.mp4` and review the proposed plan. Then `/edit-reel jobs/pilot/plan.json`.
5. Check the result yourself; run `/review-reel jobs/pilot/plan.json` and compare.
6. Publish manually **only after** brand owner and, when applicable, filmed people have approved the exact cut.

## Claude Code agent roles
- `creative-director`: hook, visual concept, script, brand consistency
- `footage-analyst`: source metadata, candidate cuts, transcript audit
- `video-editor`: execution with FFmpeg/Remotion, errors and render
- `quality-reviewer`: independent read-only technical and content audit

The **main Claude Code session** is the orchestrator. Skills encode repeated methods; agents execute focused work; scripts do deterministic processing.

## Skills
- `/ingest-video`: inspect source media and privacy status
- `/storyboard`: define one approved short-form plan
- `/edit-reel`: transform an approved plan into MP4 with scripts
- `/review-reel`: independent quality gate and approval checklist
- `brand-rules`: look-and-feel, business/medical claim restrictions

Note: `storyboard` and `review-reel` produce plans/reports; scripts do not hallucinate visual or transcript content. Do not mark generated assets as approved without a person reviewing them.

## Expected input/outputs
Input raw material -> inspect metadata -> storyboard/plan.json -> human approval -> FFmpeg rendering -> technical QA -> human content/consent approval -> MP4.

## Limitations of MVP
- Center cropping is not face tracking; keep subjects near center and verify crop manually.
- Captions are manually timed in plan.json. For professional captions add Whisper / a Georgian-capable transcription service plus manual correction.
- All source audio is retained; music mixing and sound design are future work.
- Text overlay currently uses ASS subtitles; for elaborate motion graphics migrate compositions to Remotion.
- Quality-check cannot judge aesthetics, legal consent or clinical accuracy.
- Rendering individual cuts and re-encoding is fine for short pilots, not yet optimized for production scale.
- Do not add automatic social publishing, external image downloading, or unrestricted shell permissions in MVP.

## Next iterations
- Phase 2: Transcription with word-level timecodes, face tracking, sound leveling, beat-aware edits, branded Remotion templates.
- Phase 3: Browser-based approval UI, per-client templates, job history and job queue.
- Phase 4: Hosted workers, storage, auditing, analytics, multi-tenant isolation and approved social scheduling.

For current documentation: https://code.claude.com/docs/en/sub-agents ; https://code.claude.com/docs/en/skills ; https://www.remotion.dev/docs/ai/skills
