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

- Consistent-character generation across model nodes.
- Local GPU and API-node generation.
- LoRA training on local hardware.
- Reusable workflows on a node canvas.
- Take history with versioned render takes.

Documented local training peaks at 8.6 GB to 13.4 GB VRAM for several 512 px model paths; LTX-2.5 needs 48 GB.

Use it when character continuity and a local graph workflow matter more than a one-shot image generator.

## Development line

- **2026-08-16 — Inline Studio published the v1.2.71 release.** On 2026-08-16, Inline Studio published GitHub release v1.2.71. The release linked the characters page as a version checkpoint without detailing specific release contents.

## What changed

2026-08-16 — Release v1.2.71 lets FLUX.2 generation nodes select portable `.char` files without LoRA training or an adapter.

2026-08-21 — Release v1.3.0 merged training into generation and refactored the node graph. One `.char` file now carries model payloads for FLUX.2 and Krea 2.

2026-08-25 — Release v1.3.11 added `.char` support to MiniMax H3 text-to-video, image-to-video, and reference-to-video nodes.

2026-08-30 — Release v1.3.13 added body and clothing references to characters, and protected take history from stale browser writes.

2026-09-03 — Release v1.3.15 extended character support to API nodes, including MiniMax, Seedance, and Nano Banana.

## How to use this

Treat Inline Studio v1.2.71 as a version checkpoint from 2026-08-16. Check the characters page for character features, because the links give no migration guidance.

1. Install Python 3.11+ and clone the repository. Run `webui.bat --install --extra all` on Windows or `./webui.sh --install --extra all` on macOS/Linux, then start the local UI.
  — <https://github.com/inlineresearch/Inline-Studio/blob/main/README.md>
2. Create a character from a photo or an existing take in the Characters panel. Inline Studio saves a portable `.char` file under `models/characters`.
  — <https://inlinestudio.art/characters>
3. Select that character in a compatible generation node. Run the graph and inspect the continuity score recorded for each take.
  — <https://inlinestudio.art/characters>

## Best practices

- Use varied reference angles rather than many frontal images. References match independently, and each adds inference tokens.
  — <https://inlinestudio.art/characters>
- Keep character workflows to shots centred on one person. In multi-person scenes, identity can spread to other faces while the score still reports a match.
  — <https://github.com/inlineresearch/Inline-Studio/releases/tag/v1.2.71>
- Treat the continuity score as a diagnostic, not proof of a correct crowd scene. The score is 0.8 face similarity plus 0.2 subject similarity. It falls back to subject-only when no face is visible.
  — <https://github.com/inlineresearch/Inline-Studio/releases/tag/v1.2.71>

## Superseded by this

- 2026-08-21 — Release v1.3.0 replaced the FLUX.2-only format of v1.2.71 with a unified `.char` format for FLUX.2 and Krea 2.
- 2026-08-25 — Release v1.3.11 superseded the image-model-only character workflow for MiniMax H3 nodes.
- 2026-09-03 — Release v1.3.15 superseded character support limited to local model nodes by expanding to supported API nodes.

## Still unknown

- GitHub dates the v1.2.71 release 2026-08-15, while our event date is 2026-08-16. We keep 2026-08-16 as the event date and record 2026-08-15 for context.
- The character page covers FLUX.2 and Krea 2, while release notes add MiniMax H3 and selected API nodes. Parity across other models is unverified.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/inlineresearch/Inline-Studio/releases/tag/v1.2.71 | Release v1.2.71 - Consistent characters, without training a LoRA (Flux only) | 2026-09-05 |
| https://inlinestudio.art/characters | Portable characters: one file for FLUX.2 and Krea 2 | 2026-09-05 |
| https://github.com/inlineresearch/Inline-Studio/releases | Inline Studio releases | 2026-09-05 |
| https://github.com/inlineresearch/Inline-Studio/blob/main/README.md | Inline Studio README | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:inline-studio`, thread `inline-studio-development`, 1 dated events 2026-08-16 → 2026-08-16.
- **Practical note:** Treat Inline Studio v1.2.71 as a version checkpoint from 2026-08-16. Consult the characters page for character features; the links give no migration guidance.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.