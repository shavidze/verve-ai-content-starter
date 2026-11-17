---
name: storyboard
description: Propose a brand-aligned Instagram Reel shot list from inspected source footage and a brand profile; human approval required before rendering.
---
# Storyboard
1. Read `brands/example-esthetic-center.json` and any provided reference material.
2. Ask `creative-director` for 2-3 **distinct** concepts within available footage.
3. Select or recommend the strongest one, with a hook in the first 2 seconds and total 15-30 seconds.
4. Create or update `jobs/pilot/plan.json` (sample in `jobs/demo/plan.json`), keeping `status: draft`.
5. Put exact source time segments and caption words in the plan. Do not fabricate a transcript.
6. Present the plan for user approval; don't render until the human explicitly approves it.
Input clip: $ARGUMENTS

## Caption position (owner rule, always)
Captions always go at the BOTTOM of the frame, in the lower third, above the platform UI (brand `caption.margin_bottom`, default 400). Never place captions above the head or at the top of the frame, even if a held prop is partly covered. If a per-job tweak is needed, only `caption_style.margin_bottom` between 330 and 480 is allowed. Top-of-frame space is for the single overlay badge, not captions.
(ტიტრები ყოველთვის ქვემოთ, ქვედა მესამედში. არასდროს თავს ზემოთ ან ეკრანის ზედა ნაწილში.)
