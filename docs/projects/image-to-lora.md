---
title: Image-to-LoRA
category: projects
date: 2026-06-17
tags: [image-to-lora, image-to-lora-v2-release, image_to_lora, project]
aliases: ["Image-to-LoRA"]
---

# Image-to-LoRA

**Development line:** `project:image-to-lora` · thread `image-to-lora-v2-release`  
**Last event:** 2026-06-17 · 1 dated since 2026-06-17 · **Researched:** 2026-09-05 · confidence: high

## What it is

Image-to-LoRA is DiffSynth-Studio’s i2L method for producing explicit style-LoRA weights from one or more reference images instead of optimizing a new LoRA per style.

- Style transfer: generates explicit style-LoRA weights from reference images.
- Multi-reference fusion: combines style features across several reference images.
- Controlled composition: pairs target style with generation controls.

The released V2 family targets three backbone-specific models, and each i2L model works only with its matching base architecture. Use it for fast style instantiation inside DiffSynth-Studio, not as a drop-in LoRA generator for arbitrary UIs or backbones.

## Development line

- **2026-06-17 — Image-to-LoRA V2 collection became a public project milestone.** On 2026-06-17, Image-to-LoRA published a public ModelScope collection for Image-to-LoRA V2. That collection serves as the public distribution point for the project at that date. The available sources do not state technical changes, authorship, or release status beyond that linked collection.

## What changed

- 2025-12-09 — Qwen-Image-i2L introduced the earlier image-to-LoRA model, with maintainer notes on generalization and detail-preservation limits.
- 2026-06-11 — the i2L technical report described predicting explicit LoRA weights from one or more references in one forward pass.
- 2026-06-15 — Image-to-LoRA V2 was open-sourced for Z-Image, FLUX.2-klein-base-4B, and HiDream-O1-Image.
- 2026-06-17 — Image-to-LoRA V2 was collected as a released model family across three backbone-specific models, not one universal LoRA.

## How to use this

From 2026-06-17, use the linked ModelScope collection as the dated reference point when locating and evaluating Image-to-LoRA V2, and verify its documentation and technical behavior separately.

1. Install DiffSynth-Studio from source, then select the international ModelScope endpoint or Hugging Face download source if needed.
  — <https://github.com/modelscope/DiffSynth-Studio>
2. Choose the V2 checkpoint that matches the generation backbone; for Z-Image, load `DiffSynth-Studio/ZImage-i2L-v2` with the Z-Image pipeline and enable LoRA hot loading.
  — <https://github.com/modelscope/DiffSynth-Studio/blob/main/examples/z_image/model_inference/ZImage-i2L-v2.py>
3. Provide the reference-image list, a generation prompt, and matching negative template inputs; run the template through the base pipeline to generate the styled image.
  — <https://github.com/modelscope/DiffSynth-Studio/blob/main/examples/z_image/model_inference/ZImage-i2L-v2.py>
4. For FLUX.2-klein-base-4B, use the separate `KleinBase4B-i2L-v2` example and its matching FLUX.2 pipeline rather than the Z-Image checkpoint.
  — <https://github.com/modelscope/DiffSynth-Studio/blob/main/examples/flux2/model_inference/KleinBase4B-i2L-v2.py>

## Best practices

- Pair the i2L checkpoint and base architecture exactly; V2 ships separate checkpoints for Z-Image, FLUX.2-klein-base-4B, and HiDream-O1-Image.
  — <https://github.com/modelscope/DiffSynth-Studio>
- Use one or more reference images that consistently express the target style, then use the text prompt for the new scene or composition; i2L separates appearance from reference content.
  — <https://arxiv.org/abs/2606.13809>
- Start from the maintained inference example, including its LoRA hot-loading and negative-template-input setup, before changing prompts, reference count, or sampling settings.
  — <https://github.com/modelscope/DiffSynth-Studio/blob/main/examples/z_image/model_inference/ZImage-i2L-v2.py>

## Superseded by this

- 2025-12-09 — the earlier Qwen-Image-i2L state is superseded for the V2-supported backbones by the V2 family; do not treat its generalization and detail-preservation limits as a V2 benchmark.
- 2026-06-15 — guidance that treats Image-to-LoRA as a single Qwen-only model is obsolete: V2 is a three-checkpoint, backbone-specific release.

## Still unknown

- The ModelScope collection was reachable but exposed no readable metadata, leaving its publication timestamp and per-checkpoint license terms unverified.
- No first-party evidence establishes a supported ComfyUI workflow or guarantees that weights can be exported and used outside DiffSynth-Studio.
- For 2026-06-17, repository updates dated 2026-06-15 add the exact V2 scope: `ZImage-i2L-v2`, `KleinBase4B-i2L-v2`, and `HidreamO1-i2L-v2`; the technical report was submitted on 2026-06-11. Earlier events: 2025-12-09, Qwen-Image-i2L released with stated limits; 2026-06-11, the i2L technical report submitted; 2026-06-15, V2 open-sourced. All derive from sources listed above.

## Sources

| source | title | read |
|---|---|---|
| https://modelscope.ai/collections/DiffSynth-Studio/Image-to-LoRA-V2 | ModelScope — DiffSynth-Studio/Image-to-LoRA-V2 collection | 2026-09-05 |
| https://github.com/modelscope/DiffSynth-Studio | DiffSynth-Studio — repository and update history | 2026-09-05 |
| https://arxiv.org/abs/2606.13809 | Compressing Image Style Training into a Single Model Forward | 2026-09-05 |
| https://github.com/modelscope/DiffSynth-Studio/blob/main/examples/z_image/model_inference/ZImage-i2L-v2.py | ZImage-i2L-v2 inference example | 2026-09-05 |
| https://github.com/modelscope/DiffSynth-Studio/blob/main/examples/flux2/model_inference/KleinBase4B-i2L-v2.py | KleinBase4B-i2L-v2 inference example | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:image-to-lora`, thread `image-to-lora-v2-release`, 1 dated events 2026-06-17 → 2026-06-17.
- **Practical note:** From 2026-06-17, use the linked ModelScope collection as the dated reference point when locating and evaluating Image-to-LoRA V2, while separately verifying its documentation and technical behavior.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
