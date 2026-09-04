---
title: Ideogram
category: projects
tags: [ideogram, ideogram_3_0, model-and-product-releases, project]
aliases: ["Ideogram"]
---

# Ideogram

**Development line:** `project:ideogram` · thread `model-and-product-releases`  
**Events:** 3 dated, 2024-03-01 → 2025-07-31 · **Researched:** 2026-09-04 · confidence: medium

## What it is

Ideogram is an image-generation platform for designers, content teams, and developers who need readable text, composition control, and iterative editing.

- Ideogram 4.0: 2K generation, layout control, editable elements, and open weights.
- Web and API: generation, Remix, inpaint, background and object editing, upscale, and Custom Models.

Hosted API pricing for 4.0 is $0.03 / $0.06 / $0.10 per image across Turbo, Default, and Quality tiers. Choose Ideogram for design assets that require fixing, reproducing, and editing instead of single-prompt generation.

## Development line

- **2024-03-01 — Ideogram announced Ideogram 1.0.** Public text-to-image model focused on text in images, prompt adherence, and Magic Prompt; the official release page is dated 2024-02-28.
- **2025-03-26 — Ideogram announced Ideogram 3.0.** Style Reference supports up to three images, Style Code reapplies styles, Batch Generation arrives, with stronger graphic text and layout handling.
- **2025-07-31 — Ideogram published its Character feature page.** One reference preserves character identity across scenes; masking, Magic Fill, and Remix integrate into the character workflow.

## What changed

- **2024-03-01 — Ideogram 1.0:** Public text-to-image model focused on text in images, prompt adherence, and Magic Prompt; the official release page is dated 2024-02-28.
- **2024-08-21 — Ideogram 2.0:** Added Realistic, Design, 3D, and Anime modes, palette control, an iOS app, a beta API, and public image search; confirmed on the official release page.
- **2025-03-26 — Ideogram 3.0:** Style Reference up to three images, Style Code to reuse styles, Batch Generation, and stronger graphic text and layout handling.
- **2025-07-31 — Ideogram Character:** One reference image preserves character identity across scenes; masking, Magic Fill, and Remix became part of the character workflow.
- **2026-06-03:** Ideogram 4.0 shifted the active line to an open-weight model with JSON scene descriptions, color palettes, and optional bounding boxes.
- **2026-06-18:** The official guide confirmed that legacy freeform prompts can behave differently in 4.0; exact color, text, and placement require structured JSON.

## How to use this

As of 2025-07-31, practitioners should check Ideogram's current Character workflow when evaluating its image-generation options; the supplied dated links establish version milestones and a Character product area, but not implementation details.

1. Open Ideogram, sign in, and start in Creative with Ideogram 4.0; Studio and utility tools are in the same interface.
  — <https://ideogram.ai/>
2. Describe the scene in plain text for the initial concept; live Ideogram 4.0 uses Magic Prompt to expand plain text into a structured description.
  — <https://ideogram.ai/blog/ideogram-4-json-prompting/>
3. Use JSON with high_level_description, style_description, background, and elements for exact color, composition, or text; specify literal text and bbox for lettering.
  — <https://ideogram.ai/blog/ideogram-4-json-prompting/>
4. Save the style_code and seed after a good result: style_code locks the visual style, while seed provides controlled composition variations.
  — <https://ideogram.ai/blog/ideogram-4-json-prompting/>
5. For a series with the same character, open Character, upload a clear portrait, describe the scene, and adjust the mask, Magic Fill, or Remix as needed.
  — <https://ideogram.ai/features/character/>
6. For product integration, configure an API key and call POST /v1/ideogram-v4/generate; the current quickstart shows Character reference as a separate v3 call.
  — <https://developer.ideogram.ai/ideogram-api/api-overview>

## Best practices

- In 4.0, replace vague mood words with concrete details: light source, medium, palette, objects, and spatial placement.
  — <https://ideogram.ai/blog/ideogram-4-json-prompting/>
- Follow the cycle: plain text for initial concept search, style_code to lock a look, JSON for exact brand requirements.
  — <https://ideogram.ai/blog/ideogram-4-json-prompting/>
- Put requested lettering inside double quotes, keep each snippet to roughly 5–7 words, and select Quality for error-sensitive typography.
  — <https://ideogram.ai/blog/ideogram-4-json-prompting/>
- Do not build current workflows on Random Style because Ideogram marked it deprecated; use saved style codes or custom Style Reference instead.
  — <https://docs.ideogram.ai/using-ideogram/generation-settings/styles>
- For Character, use a clear, well-lit portrait facing forward or three-quarters, and edit the mask to preserve or swap hair, clothing, or accessories.
  — <https://ideogram.ai/features/character/>

## Superseded by this

- 2024-03-01 — Treating Ideogram 1.0 as the active main model is obsolete; the current release is Ideogram 4.0.
- 2025-03-26 — Finding styles through Random mode and its 4.3 billion presets is obsolete; current documentation marks Random mode as deprecated.
- 2025-03-26 — Relying on long freeform prompts for exact text and layout is obsolete for Ideogram 4.0; strict outputs require structured JSON, text elements, and bbox.

## Still unknown

- The 2024-08-21 entry contains only the main homepage address; the official release page confirms the date and contents of Ideogram 2.0, but the original post wording is unavailable.
- Legacy official URLs /1.0, /2.0, and /3.0 now redirect to new pages; long-term preservation of historical claims requires separate archived snapshots.
- The current API shows standard generation on v4, while the Character Reference example still uses v3; public documentation does not confirm a dedicated v4 Character endpoint.

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
