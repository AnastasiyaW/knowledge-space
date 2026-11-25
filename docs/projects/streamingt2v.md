---
title: StreamingT2V
category: projects
date: 2024-04-08
tags: [project, streamingt2v]
aliases: ["StreamingT2V"]
---

# StreamingT2V

**Development line:** `project:streamingt2v` · thread `streamingt2v`  
**Last event:** 2024-04-08 · 1 dated since 2024-04-08 · **Researched:** 2026-09-04 · confidence: high

## What it is

StreamingT2V is an autoregressive long-video method for researchers and GPU-equipped practitioners.

- CAM carries short-term chunk context.
- APM preserves scene appearance.
- Randomized blending refines overlapping chunks.

The repository runs 200-frame image-to-video inference at 60 GB VRAM by default or 24 GB in slower memory-optimized mode. The hosted Space currently reports a runtime error. Use the local repository for research and non-commercial image-to-video experiments, not the broken demo or a current production T2V service.

## Development line

- **2024-04-08 — StreamingT2V project materials were made publicly available.** On 2024-04-08, StreamingT2V released a project website, a public source repository, and a Hugging Face Space to provide research materials, implementation code, and an interactive entry point.

## What changed

- 2024-04-08 — The project was publicly linked as StreamingT2V, an autoregressive method for extending text-to-video generation with chunk memory and refinement.
- 2024-06-30 — A later reference was recorded, but no independently accessible technical release or model change could be tied to this date.
- 2024-08-30 — StreamingSVD code and model weights were released, making an SVD-based image-to-video implementation available.
- 2024-11-28 — A memory-optimized release reduced the documented 200-frame requirement from 60 GB to 24 GB VRAM, at roughly 50% lower speed.
- 2025-02-26 — The work was accepted to CVPR 2025.

## How to use this

We can evaluate the project through its website, source repository, and Hugging Face Space from 2024-04-08. The 2024-06-30 reference alone establishes no additional workflow change.

1. Clone the repository, create a Python 3.9 environment with CUDA 11.8 or newer, install its requirements, and install FFmpeg.
  — <https://github.com/Picsart-AI-Research/StreamingT2V>
2. Run `python inference_i2v.py --input <image-or-folder> --output <folder>` from `code`; inputs must be 16:9 images.
  — <https://github.com/Picsart-AI-Research/StreamingT2V>
3. Set `--num_frames` for length (200 by default), `--out_fps` for output rate (24 by default), or `--use_memopt` on 24 GB hardware.
  — <https://github.com/Picsart-AI-Research/StreamingT2V>

## Best practices

- Use the default path only when 60 GB VRAM is available for 200 frames; use `--use_memopt` for 24 GB VRAM and budget for about half the speed.
  — <https://github.com/Picsart-AI-Research/StreamingT2V>
- Use randomized blending only when memory pressure requires it; the maintainers recommend chunk size 38 and overlap 12 when it is enabled.
  — <https://github.com/Picsart-AI-Research/StreamingT2V>
- Treat the code as non-commercial research use because bundled SVD, EMA-VFI, and I2VGen-XL dependencies impose that restriction.
  — <https://github.com/Picsart-AI-Research/StreamingT2V>

## Superseded by this

- 2024-04-08 — Guidance to use the linked hosted demo is obsolete in practice: the PAIR Hugging Face Space currently reports a runtime error.
- 2024-04-08 — Describing the available implementation as a general text-to-video release is outdated: the maintained README documents StreamingSVD image-to-video inference and lists StreamingSVD text-to-video as a future plan.

## Still unknown

- The 2024-06-30 linked X and The source pages were not accessible with usable text, so their claimed product-level change cannot be verified.
- No newer maintained release after the repository's March 2025 update was found; current availability is inferred from the repository and Space state, not from a live successful local run.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/Picsart-AI-Research/StreamingT2V | Picsart-AI-Research/StreamingT2V repository and README | 2026-09-05 |
| https://streamingt2v.github.io/ | StreamingT2V project page | 2026-09-05 |
| https://arxiv.org/abs/2403.14773 | StreamingT2V: Consistent, Dynamic, and Extendable Long Video Generation from Text | 2026-09-05 |
| https://huggingface.co/spaces/PAIR/StreamingT2V | PAIR/StreamingT2V Hugging Face Space | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:streamingt2v`, thread `streamingt2v`, 1 dated events 2024-04-08 → 2024-04-08.
- **Practical note:** From 2024-04-08, practitioners could use the StreamingT2V project site, source repository, and Hugging Face Space to evaluate or try the project; the 2024-06-30 reference alone establishes no additional workflow change.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
