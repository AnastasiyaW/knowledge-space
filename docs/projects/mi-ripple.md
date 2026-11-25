---
title: "Mi Ripple: mi-ripple — Mi Ripple"
category: "projects"
date: 2026-09-12
tags: ["mi-ripple", "project"]
aliases: ["Mi Ripple: mi-ripple"]
---

# Mi Ripple: mi-ripple — Mi Ripple

**Development line:** project:mi-ripple · thread mi-ripple  
**Last event:** 2026-09-12 · 1 dated since 2026-09-12 · **Researched:** 2026-11-25 · confidence: medium

## What it is

Mi-Ripple is MIYANG's open-source (MIT) workflow to restore grid and scale artifacts from iterative AI image editing.

It avoids blunt filtering across the whole image by sorting damage into three classes:
- Periodic lattice artifacts (1): isolated spectral peaks, removed by selective notching.
- Granular artifacts in unstructured regions (2): 3-8 px textures, reduced behind a structure-protection mask.
- Content-entangled artifacts (3): textures overlapping hair, foliage or fabric, routed to human review or cleaned-reference regeneration.

The project also ships an AI-agent skill file that describes the whole workflow.

## Development line

- **2026-09-12 — Mi-Ripple image restoration method published on 2026-09-12.** A technical approach for iterative AI image restoration that separates periodic artifacts from content-integrated noise, using spectral notching and structure-dependent smoothing. In 14 runs, residual deviation reached 0.08-0.44 CIELAB lightness units; reference-based regeneration reduced noise density by 45%.
  - The repository describes Mi-Ripple as a reference implementation of MIYANG's diagnosis-guided workflow for grid-like and scale-like artifacts from iterative, reference-conditioned AI image editing. It names the three artifact classes: periodic lattice (selectively notched), granular 3-8 px texture in unstructured regions (reduced behind a structure-protection mask), and content-entangled texture (human review or optional cleaned-reference regeneration). It states this is a research implementation, not a universal artifact detector. It requires Python 3.11+, is MIT-licensed, and links to a MIYANG Lab web tool. Cleaned-reference regeneration is not pixel-aligned restoration and can change fine semantic details. (undated (repository page, no explicit date)) — <https://github.com/miyang-ai/Mi-Ripple>
  - The bundled agent skill (skills/mi-ripple/SKILL.md, version 0.1.0) sets out the workflow: run the deterministic local pipeline first, read the generated JSON and diagnostic boards, and treat paid or content-changing regeneration as optional and allowed only with the user's explicit approval. A 'pipeline passed' result only confirms measured filtering damage stayed within configured limits, not human acceptance. (undated (repository file, no explicit date)) — <https://github.com/miyang-ai/Mi-Ripple/blob/main/skills/mi-ripple/SKILL.md>

## What changed

On 2026-09-12 the method was published with code, an agent skill and a web demo. Reported results show 14 runs with a residual deviation of 0.08-0.44 CIELAB lightness units, and a 45% reduction in residual artifact density for a paired regeneration run using a cleaned reference. The repository notes this is a research implementation rather than a universal artifact detector, and automatic scores serve only as triage signals.

## How to use this

1. Install with Python 3.11+: clone the repository, create a virtual environment, and run `pip install -e .`. Optional extras are `.[face]` for OpenCV face protection and `.[dev]` for development.
  — <https://github.com/miyang-ai/Mi-Ripple>
2. Run the default local deterministic pipeline: `mi-ripple input.png output/`. It writes diagnosis JSON, visual inspection boards, masks, candidate images, an XML decision trace, and a final image when delivering a local result.
  — <https://github.com/miyang-ai/Mi-Ripple>
3. Read the outputs: `<stem>_restored.json` for outcome and actions, `<stem>_input_diag.json` for measurements, `<stem>_input_diag_board.png` for native-pixel diagnostic crops, `<stem>_input_scaleheat.png` for flagged tiles, `<stem>_verify_board.png` when filtering was applied, and `<stem>_restored.png` for the final local result.
  — <https://github.com/miyang-ai/Mi-Ripple/blob/main/skills/mi-ripple/SKILL.md>
4. Load the skill in AI coding agents from skills/mi-ripple/SKILL.md. The agent installs the tool in an isolated environment, processes the image, inspects the evidence, and returns the actual output files.
  — <https://github.com/miyang-ai/Mi-Ripple/blob/main/skills/mi-ripple/SKILL.md>

## Best practices

- Work on the original image at native resolution. Do not resize, recompress, or screenshot it before diagnosis, and prefer PNG for intermediate and final files.
  — <https://github.com/miyang-ai/Mi-Ripple/blob/main/skills/mi-ripple/SKILL.md>
- Do not conclude an artifact is removed just because a numeric score dropped. Inspect the heat maps and comparison boards directly, and keep JSON sidecars and the XML trace with the output.
  — <https://github.com/miyang-ai/Mi-Ripple/blob/main/skills/mi-ripple/SKILL.md>
- Run the local deterministic pipeline before considering regeneration. Never run paid or content-changing regeneration without the user's explicit approval. Set the API key as the MIYANG_API_KEY environment variable and never paste it into a conversation. Files containing _refclean are model references, not deliverables.
  — <https://github.com/miyang-ai/Mi-Ripple/blob/main/skills/mi-ripple/SKILL.md>
- Expect to review content-entangled artifacts like hair or foliage by hand. Cleaned-reference regeneration is not pixel-aligned and can change fine semantic details.
  — <https://github.com/miyang-ai/Mi-Ripple>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The linked pages do not show the figures of 14 runs, 0.08-0.44 CIELAB lightness deviation, or the 45% reduction in artifact density, so they come from the reviewed summary only.
- The web demo page's content was not available beyond its title, so its features and limits remain undescribed.
- No explicit release date or version history is visible on the fetched repository pages beyond skill version 0.1.0.
- No independent evaluation or community feedback was linked.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/miyang-ai/Mi-Ripple | GitHub - miyang-ai/Mi-Ripple: MIYANG diagnosis-guided restoration for digital ripple artifacts in iteratively edited AI images | 2026-09-12 |
| https://github.com/miyang-ai/Mi-Ripple/blob/main/skills/mi-ripple/SKILL.md | Mi-Ripple/skills/mi-ripple/SKILL.md at main · miyang-ai/Mi-Ripple | 2026-09-12 |

## Agent brief {#agent-brief}

- **Subject:** project:mi-ripple, thread mi-ripple, 1 dated events 2026-09-12 → 2026-09-12.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
