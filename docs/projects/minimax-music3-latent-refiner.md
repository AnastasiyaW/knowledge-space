---
title: MiniMax Music 3 Latent Refiner
category: projects
date: 2026-08-23
tags: [minimax-music3-latent-refiner, minimax_music3_latent_refiner, project]
aliases: ["MiniMax Music 3 Latent Refiner"]
---

# MiniMax Music 3 Latent Refiner

**Development line:** `project:minimax-music3-latent-refiner` · thread `minimax-music3-latent-refiner`  
**Last event:** 2026-08-23 · 1 dated since 2026-08-23 · **Researched:** 2026-09-05 · confidence: medium

## What it is

MiniMax Music 3 Latent Refiner is a community checkpoint to restore existing audio rather than generate music from text.

- Audio repair: cleans damaged audio while preserving performance, timing, vocals, and arrangement.
- Engine: operates through MiniMax Music 3 DAV.
- Integration: available through CLI, Python, Diffusers attachment, and ComfyUI.

Tested only on CUDA and FP32; severe corruption outside the training pipeline can destroy unrecoverable data.

Use it as post-processing for MiniMax Music 3 audio and audition the output first, not as a replacement for original recordings or a text-to-music pipeline.

## Development line

- **2026-08-23 — MiniMax Music 3 Latent Refiner v0.10 was linked on Hugging Face.** On 2026-08-23, a Hugging Face link for BornSaint/minimax-music3-latent-refiner-v0.10 was recorded. The versioned artifact link indicates a concrete v0.10 step in the MiniMax Music 3 Latent Refiner development line, although its capabilities and changes were not established from the available evidence.

## What changed

- 2026-08-23 — Hugging Face listed `BornSaint/minimax-music3-latent-refiner-v0.10`, but the saved link does not confirm a working release or its specifications.
- 2026-09-01 — v0.10 released under `terminusresearch/minimax-music3-latent-refiner-v0.10` as a 137,253,888-parameter bridge-hybrid checkpoint-1000 for audio restoration in DAV latents.

## How to use this

As of 2026-08-23, treat the linked v0.10 artifact as a candidate version to inspect and evaluate, rather than assuming an earlier latent-refiner version remains current.

1. Clone the repository with Git LFS, create a Python environment, and install the package in editable mode.
  — <https://github.com/bghira/minimax-music3-latent-refiner>
2. Run `minimax-music3-refine input.wav refined.wav` for basic file processing.
  — <https://github.com/bghira/minimax-music3-latent-refiner>
3. For Python, load `MiniMaxMusic3RefinerPipeline`, pass waveform and sample rate, then save the returned audio tensor.
  — <https://github.com/bghira/minimax-music3-latent-refiner>
4. For ComfyUI, connect the custom node, restart ComfyUI, and open the included workflow; use the refiner loader, DAV encoder loader, and latent refine node.
  — <https://github.com/bghira/minimax-music3-latent-refiner>

## Best practices

- Use overlapping 30-second windows with two-second latent overlap: the checkpoint was trained on 30-second windows, and that is the stated quality baseline.
  — <https://github.com/bghira/minimax-music3-latent-refiner>
- Prefer CUDA and FP32: this is the verified release precision; do not treat the bfloat16 example in the auto-generated Hub instructions as a confirmed mode for this audio pipeline.
  — <https://github.com/bghira/minimax-music3-latent-refiner>
- Check results by ear and do not expect recovery of information removed by heavy corruption outside the training pipeline.
  — <https://github.com/bghira/minimax-music3-latent-refiner>

## Superseded by this

- 2026-08-23 — the instructions on `BornSaint/minimax-music3-latent-refiner-v0.10` showing an image prompt and `pipe(prompt).images[0]` are not a valid way to run an audio refiner.
- 2026-09-01 — the active release repository in the source code and model card is `terminusresearch/minimax-music3-latent-refiner-v0.10`; do not substitute the BornSaint page of the same name.

## Still unknown

- `BornSaint/minimax-music3-latent-refiner-v0.10` currently contains mismatched image-generation instructions, though it points to `terminusresearch` in the ComfyUI section. Without a historical snapshot, we cannot confirm what was published there on 2026-08-23.
- The v0.10 release is confirmed by a commit shown as four days old during the 2026-09-05 check; 2026-09-01 is inferred from that relative timestamp.
- We found no independent quality benchmarks, no tests across corruption types, and no VRAM measurements.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/BornSaint/minimax-music3-latent-refiner-v0.10 | BornSaint/minimax-music3-latent-refiner-v0.10 — Hugging Face | 2026-09-05 |
| https://github.com/bghira/minimax-music3-latent-refiner | bghira/minimax-music3-latent-refiner — GitHub | 2026-09-05 |
| https://huggingface.co/terminusresearch/minimax-music3-latent-refiner-v0.10/commit/8806b37005e090f1b3443759aa03563a5105d4d9 | Release MiniMax Music 3 latent refiner v0.10 — Hugging Face commit 8806b37 | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:minimax-music3-latent-refiner`, thread `minimax-music3-latent-refiner`, 1 dated events 2026-08-23 → 2026-08-23.
- **Practical note:** As of 2026-08-23, practitioners should treat the linked v0.10 artifact as a candidate version to inspect and evaluate, rather than assuming an earlier latent-refiner version remains current.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
