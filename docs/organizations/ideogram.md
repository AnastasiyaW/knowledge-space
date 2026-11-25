---
title: Ideogram
category: projects
date: 2025-07-31
tags: [ideogram, ideogram_3_0, model-and-product-releases, project]
aliases: ["Ideogram"]
---

# Ideogram

**Development line:** `project:ideogram` · thread `model-and-product-releases`  
**Last event:** 2025-07-31 · 3 dated since 2024-03-01 · **Researched:** 2026-09-04 · confidence: medium

## What it is

Ideogram is an image-generation platform for designers, content teams, and developers who need legible text, composition control, and iterative edits.

- Ideogram 4.0: 2K generation, layout control, editable elements, and open weights.
- Web and API: generation, Remix, inpainting, background and object manipulation, upscaling, and Custom Models.

The hosted API for 4.0 lists $0.03 / $0.06 / $0.10 per image across Turbo / Default / Quality tiers. Use it for design assets that need fixing, scaling, and revision rather than single-prompt generation.

## Development line

- **2024-03-01 — Ideogram announced Ideogram 1.0.** Public text-to-image model focused on typography in images, prompt adherence, and Magic Prompt; the official release page is dated 2024-02-28.
- **2025-03-26 — Ideogram announced Ideogram 3.0.** Style Reference up to three images, Style Code to reapply styles, Batch Generation, and improved graphic text and layout handling.
- **2025-07-31 — Ideogram published its Character feature page.** One reference image to preserve character identity across scenes; masking, Magic Fill, and Remix joined the character workflow.

## What changed

- 2024-03-01 — Ideogram 1.0: public text-to-image model focused on typography in images, prompt adherence, and Magic Prompt; the official release page is dated 2024-02-28.
- 2024-08-21 — Ideogram 2.0: added Realistic, Design, 3D, and Anime styles, palette control, an iOS app, a beta API, and public image search.
- 2025-03-26 — Ideogram 3.0: Style Reference up to three images, Style Code to reapply styles, Batch Generation, and improved graphic text and layout handling.
- 2025-07-31 — Ideogram Character: one reference image to preserve character identity across scenes; masking, Magic Fill, and Remix joined the character workflow.
- 2026-06-03 — Ideogram 4.0 shifted the active line to an open-weight model with JSON scene descriptions, palette control, and optional bounding boxes.
- 2026-06-18 — Official documentation confirmed older free-form prompts may behave differently in 4.0; structured JSON is required for exact color, text, and layout.

## How to use this

As of 2025-07-31, practitioners should check Ideogram's current Character workflow when evaluating its image-generation options; the supplied dated links establish version milestones and a Character product area, but not implementation details.

1. Open Ideogram, sign in, and start in Creative with Ideogram 4.0; Studio and utility tools are available there too.
  — <https://ideogram.ai/>
2. For an initial concept, describe the scene in detailed natural text: live Ideogram 4.0 Magic Prompt expands plain text into a structured description automatically.
  — <https://ideogram.ai/blog/ideogram-4-json-prompting/>
3. If color, composition, or typography must be exact, use JSON with high_level_description, style_description, background, and elements; specify literal text and bbox for lettering.
  — <https://ideogram.ai/blog/ideogram-4-json-prompting/>
4. After a good result, save style_code and seed: the first locks the visual style, and the second gives controlled composition variations.
  — <https://ideogram.ai/blog/ideogram-4-json-prompting/>
5. For a series with one consistent subject, open Character, upload a clear portrait, describe the scene, and adjust the mask, Magic Fill, or Remix as needed.
  — <https://ideogram.ai/features/character/>
6. For product integration, configure an API key and call POST /v1/ideogram-v4/generate; Character reference in the current quickstart runs as a separate v3 call.
  — <https://developer.ideogram.ai/ideogram-api/api-overview>

## Best practices

- In 4.0, replace vague mood descriptions with specifics: light source, medium, palette, objects, and their arrangement.
  — <https://ideogram.ai/blog/ideogram-4-json-prompting/>
- Follow the cycle: plain text to explore ideas, style_code to lock a successful style, and JSON for strict brand requirements.
  — <https://ideogram.ai/blog/ideogram-4-json-prompting/>
- Put requested lettering in double quotes, keep each text snippet within 5–7 words, and choose Quality tier for error-critical typography.
  — <https://ideogram.ai/blog/ideogram-4-json-prompting/>
- Do not build production workflows on Random Style: the documentation marks it as deprecated; use a saved Style Code or a custom Style Reference for repeatable results.
  — <https://docs.ideogram.ai/using-ideogram/generation-settings/styles>
- For Character, use a clear, well-lit portrait facing forward or at three-quarters, and adjust the mask to keep or replace hair, clothing, and accessories.
  — <https://ideogram.ai/features/character/>

## Superseded by this

- 2024-03-01 — treating Ideogram 1.0 as the active flagship model is obsolete: the current line is Ideogram 4.0.
- 2025-03-26 — browsing styles via Random or "4.3 billion presets" is obsolete: current documentation marks Random mode as deprecated.
- 2025-03-26 — relying on long free-form prompts for exact typography and layout is obsolete in Ideogram 4.0: strict output requires structured JSON, text elements, and bounding boxes.

## Still unknown

- The 2024-08-21 entry contains only the root homepage URL: the official release page confirms the date and contents of Ideogram 2.0, but the original entry wording is unavailable.
- Older official URLs /1.0, /2.0, and /3.0 now redirect to new pages; long-term verification of historical claims requires separate archival captures.
- The current API documents base generation on v4 while the Character Reference example still uses v3; public documentation does not confirm a dedicated v4 Character endpoint.

## Sources

| source | title | read |
|---|---|---|
| https://about.ideogram.ai/1.0 | Ideogram 1.0, Feb 2024 | 2026-09-04 |
| https://about.ideogram.ai/2.0 | Ideogram 2.0 | 2026-09-04 |
| https://about.ideogram.ai/3.0 | Ideogram 3.0 | 2026-09-04 |
| https://about.ideogram.ai/character | Ideogram Character | 2026-09-04 |
| https://ideogram.ai/ | Ideogram | AI apps and models in one platform | 2026-09-04 |
| https://ideogram.ai/models/3.0/ | Ideogram 3.0 — Realism, design, and consistent styles | 2026-09-04 |
| https://ideogram.ai/models/4.0/ | Ideogram 4.0 | Ideogram | 2026-09-04 |
| https://ideogram.ai/blog/ideogram-4.0/ | Ideogram 4.0 Technical Details: Open model at the forefront of design | 2026-09-04 |
| https://ideogram.ai/blog/ideogram-4-json-prompting/ | How to JSON prompt for Ideogram 4.0 | 2026-09-04 |
| https://ideogram.ai/features/character/ | Character Consistency from One Photo: Free AI Headshot Generator | Ideogram | 2026-09-04 |
| https://docs.ideogram.ai/using-ideogram/generation-settings/styles | Style Reference | Ideogram | 2026-09-04 |
| https://developer.ideogram.ai/ideogram-api/api-overview | API Overview | Ideogram | Documentation | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:ideogram`, thread `model-and-product-releases`, 3 dated events 2024-03-01 → 2025-07-31.
- **Practical note:** As of 2025-07-31, practitioners should check Ideogram's current Character workflow when evaluating its image-generation options; the supplied dated links establish version milestones and a Character product area, but not implementation details.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
