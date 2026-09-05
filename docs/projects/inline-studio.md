---
title: Inline Studio
category: projects
date: 2026-08-16
tags: [inline-studio, inline-studio-development, inlineresearch/inline-studio, project]
aliases: ["Inline Studio"]
---

# Inline Studio

**Development line:** `project:inline-studio` · thread `inline-studio-development`  
**Last event:** 2026-08-16 · 1 dated since 2026-08-16 · **Researched:** 2026-09-05 · confidence: high

## What it is

Inline Studio is an open-source workspace for character-led image and video generation. It combines a node canvas, portable `.char` files, local LoRA training, model nodes, and take history.

Abilities:
- Consistent character generation across shots.
- Local GPU and API-node generation.
- LoRA training on local hardware.
- Reusable graph workflows.
- Versioned render takes with continuity history.

Documented local training peaks range from about 8.6 GB to 13.4 GB VRAM for several 512 px model paths, while LTX-2.5 is documented as wanting 48 GB.

Use it when character continuity and a local graph workflow matter more than the simpler one-shot experience of an image generator.

## Development line

- **2026-08-16 — Inline Studio published the v1.2.71 release.** On 2026-08-16, Inline Studio published its GitHub release v1.2.71. The dated link established the characters page as a version checkpoint without detailing release contents.

## What changed

2026-08-16 — Inline Studio’s v1.2.71 character workflow made a portable `.char` file selectable on FLUX.2 generation nodes without LoRA training or an adapter.

2026-08-21 — v1.3.0 merged training into generation, refactored the node graph, and made one `.char` carry model-specific payloads for FLUX.2 and Krea 2.

2026-08-25 — v1.3.11 added `.char` support to MiniMax H3 text-to-video, image-to-video, and reference-to-video nodes.

2026-08-30 — v1.3.13 added body and clothing references to characters and protected take history from stale browser writes.

2026-09-03 — v1.3.15 extended character support to API nodes including MiniMax, Seedance, and Nano Banana.

## How to use this

From 2026-08-16, we treat Inline Studio v1.2.71 as a version checkpoint. Consult the characters page for character tools, because the supplied links provide no migration guidance.

1. Install Python 3.11+, clone the repository, run `webui.bat --install --extra all` on Windows or `./webui.sh --install --extra all` on macOS/Linux, then start the local UI.
  — <https://github.com/inlineresearch/Inline-Studio/blob/main/README.md>
2. Create a character from a photo or an existing take in the Characters panel; Inline Studio writes a portable `.char` file under `models/characters`.
  — <https://inlinestudio.art/characters>
3. Select that character in a compatible generation node, run the graph, and inspect the continuity score recorded for each take.
  — <https://inlinestudio.art/characters>

## Best practices

- Use varied reference angles rather than many frontal images; references match independently and each adds inference tokens.
  — <https://inlinestudio.art/characters>
- Keep character workflows to shots centred on one person: in multi-person scenes identity can spread to other faces while the score still reports a match.
  — <https://github.com/inlineresearch/Inline-Studio/releases/tag/v1.2.71>
- Treat the continuity score as a diagnostic, not proof of a correct crowd scene; it is 0.8 face similarity plus 0.2 subject similarity and falls back to subject-only when no face is visible.
  — <https://github.com/inlineresearch/Inline-Studio/releases/tag/v1.2.71>

## Superseded by this

- 2026-08-21 — v1.3.0 superseded the FLUX.2-only character state of v1.2.71 with a unified `.char` format for FLUX.2 and Krea 2.
- 2026-08-25 — v1.3.11 superseded the image-only character workflow by adding MiniMax H3 node support.
- 2026-09-03 — v1.3.15 superseded local-only character nodes by adding supported API nodes.

## Still unknown

- The linked v1.2.71 release tag is dated 2026-08-15, while the recorded event date is 2026-08-16.
- The official character page describes FLUX.2 and Krea 2, while current release notes add MiniMax H3 and selected API-node support; character parity across other models remains unverified.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/inlineresearch/Inline-Studio/releases/tag/v1.2.71 | Release v1.2.71 - Consistent characters, without training a LoRA (Flux only) | 2026-09-05 |
| https://inlinestudio.art/characters | Portable characters: one file for FLUX.2 and Krea 2 | 2026-09-05 |
| https://github.com/inlineresearch/Inline-Studio/releases | Inline Studio releases | 2026-09-05 |
| https://github.com/inlineresearch/Inline-Studio/blob/main/README.md | Inline Studio README | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:inline-studio`, thread `inline-studio-development`, 1 dated events 2026-08-16 → 2026-08-16.
- **Practical note:** From 2026-08-16, practitioners should treat Inline Studio v1.2.71 as a recorded version checkpoint and consult the characters page for the project’s character-facing surface; the supplied links do not support feature-specific migration guidance.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
