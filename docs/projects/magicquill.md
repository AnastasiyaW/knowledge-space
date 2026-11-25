---
title: MagicQuill
category: projects
date: 2024-11-18
tags: [magicquill, magicquill-development, magicquill_pinokio, project]
aliases: ["MagicQuill"]
---

# MagicQuill

**Development line:** `project:magicquill` · thread `magicquill-development`  
**Last event:** 2024-11-18 · 1 dated since 2024-11-18 · **Researched:** 2026-09-04 · confidence: medium

## What it is

MagicQuill is a research image editor for artists who need local control beyond prompt-only inpainting.

- V2 controls content, placement, structure, and color through visual layers, adding a local-edit brush, foreground props, and SAM segmentation.
- V1 controls additions, subtractions, and color brush edits, with Draw&Guess suggesting prompts from sketches.

## Development line

- **2024-11-18 — MagicQuill's public demo, source repository, and hosted Space were linked.** Project page, source code, and Hugging Face demo formed the public practitioner entry points.

## What changed

- 2024-11-14 — MagicQuill V1: the arXiv preprint defined the three-brush editor and Draw&Guess prompt assistant.
- 2024-11-18 — MagicQuill V1: project page, source code, and Hugging Face demo formed the public practitioner entry points.
- 2024-11-21 — MagicQuill V1: Windows path handling, save behavior, and `.bat`/`.sh` setup helpers were updated.
- 2024-11-25 — MagicQuill V1: drag-and-drop image upload and a download button were added.
- 2024-12-06 — MagicQuill V1: auto-save and resolution controls were added.
- 2024-12-07 — MagicQuill V1: a ComfyUI custom node was released.
- 2024-12-16 — MagicQuill V1: a ModelScope deployment was added.
- 2025-01-02 — MagicQuill V1: a Docker container path was added.
- 2025-02-24 — MagicQuill: a Pinokio launcher route was referenced; its historical package state cannot be reconstructed from the supplied endpoint.
- 2025-02-27 — MagicQuill V1: the paper was accepted to CVPR 2025.
- 2025-12-02 — MagicQuill V2: the layered-visual-cues paper was submitted to arXiv.
- 2025-12-03 — MagicQuill V2: the released system moved from V1’s brush-only interaction to content, spatial, structural, and color layers on Flux Kontext.

## How to use this

From 2024-11-18, practitioners could evaluate MagicQuill through its public demo and hosted Space, while using the linked repository to inspect the implementation before adoption.

1. Use the running V2 Hugging Face Space when a local GPU with about 40 GB VRAM is unavailable.
  — <https://huggingface.co/spaces/AI4Editing/MagicQuillV2>
2. For local V2, use the active `zliucz/MagicQuillV2` repository, create a Python 3.10 environment, and install its requirements.
  — <https://github.com/zliucz/MagicQuillV2>
3. Download `LiuZichen/MagicQuillV2-models` into `models/`, then start the UI with `python app.py`.
  — <https://huggingface.co/LiuZichen/MagicQuillV2-models>
4. In V2, isolate a foreground prop with SAM, place it through the Visual Cue Manager, then use local-edit, edge, color, or removal controls for the relevant layer.
  — <https://magicquill.art/v2/>
5. For an 8GB GPU, use V1: clone recursively so the LLaVA submodule is present, fetch the checkpoints, then run `python gradio_run.py`.
  — <https://github.com/magic-quill/magicquill>

## Best practices

- Treat Draw&Guess as a suggestion and replace its prompt when a sketch is ambiguous.
  — <https://arxiv.org/abs/2411.09703>
- For V1, lower Edge Strength when a rough scribble conflicts with the prompt; reduce color opacity/strength when colorization removes too much detail.
  — <https://arxiv.org/abs/2411.09703>
- Choose V1 rather than forcing V2 onto low-memory hardware: V2’s stated requirement is about 40 GB VRAM, while V1 is the documented lower-resource option.
  — <https://github.com/zliucz/MagicQuillV2>
- Clone V1 with `--recursive`; otherwise its required LLaVA submodule is absent.
  — <https://github.com/magic-quill/magicquill>
- Treat the Pinokio installer as third-party code and inspect it before use: its current script clones `6Morpheus6/MagicQuill`, not the canonical repository.
  — <https://raw.githubusercontent.com/pinokiofactory/MagicQuill/main/install.js>
- Confirm that CC BY-NC 4.0 fits the intended use before using either implementation in commercial work.
  — <https://github.com/zliucz/MagicQuillV2>

## Superseded by this

- 2025-12-03 — MagicQuill V2 supersedes V1 as the active capability line, but V1 remains the documented lower-VRAM path rather than being universally obsolete.
- 2026-09-04 — The V2 README’s old clone target is stale: the observed `magic-quill/MagicQuillV2` route returns 404; use the active `zliucz/MagicQuillV2` repository.
- 2026-09-04 — Pinokio should not be treated as official MagicQuill model guidance; its current installer is a third-party wrapper around a noncanonical fork.

## Still unknown

- The original 2025-02-24 Pinokio page content is not recoverable from the supplied URL today: it redirects to Pinokio’s general site, leaving installer revision and behavior on that date unconfirmed.
- The V1 `/demo/` route returned no inspectable page body, and its Hugging Face Space shows “Running on Zero”; live edit completion was not independently tested.
- Pinokio is a launcher path rather than a second MagicQuill model, leaving its precise connection to the 2025-02-24 event unconfirmed.
- V1 and V2 GitHub pages show no immutable software releases, so README update-log dates serve as the available release evidence.
- The stated V1 and V2 hardware figures are author-reported requirements, not independent benchmarks.

## Sources

| source | title | read |
|---|---|---|
| https://magicquill.art/demo/ | MagicQuill demo | 2026-09-04 |
| https://github.com/magic-quill/magicquill | MagicQuill V1 repository | 2026-09-04 |
| https://huggingface.co/spaces/AI4Editing/MagicQuill | MagicQuill V1 Hugging Face Space | 2026-09-04 |
| https://pinokio.computer/ | Pinokio | 2026-09-04 |
| https://arxiv.org/abs/2411.09703 | MagicQuill: An Intelligent Interactive Image Editing System | 2026-09-04 |
| https://github.com/pinokiofactory/MagicQuill | Pinokio MagicQuill repository | 2026-09-04 |
| https://raw.githubusercontent.com/pinokiofactory/MagicQuill/main/install.js | Pinokio MagicQuill installer script | 2026-09-04 |
| https://github.com/magic-quill/MagicQuillV2 | MagicQuillV2 legacy GitHub clone route | 2026-09-04 |
| https://github.com/zliucz/MagicQuillV2 | MagicQuill V2 repository | 2026-09-04 |
| https://arxiv.org/abs/2512.03046 | MagicQuillV2: Precise and Interactive Image Editing with Layered Visual Cues | 2026-09-04 |
| https://magicquill.art/v2/ | MagicQuill V2 project page | 2026-09-04 |
| https://huggingface.co/LiuZichen/MagicQuillV2-models | MagicQuill V2 model card | 2026-09-04 |
| https://huggingface.co/spaces/AI4Editing/MagicQuillV2 | MagicQuill V2 Hugging Face Space | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:magicquill`, thread `magicquill-development`, 1 dated events 2024-11-18 → 2024-11-18.
- **Practical note:** From 2024-11-18, practitioners could evaluate MagicQuill through its public demo and hosted Space, while using the linked repository to inspect the implementation before adoption.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
