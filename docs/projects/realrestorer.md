---
title: RealRestorer
category: projects
date: 2026-03-27
tags: [project, realrestorer]
aliases: ["RealRestorer"]
---

# RealRestorer

**Development line:** `project:realrestorer` · thread `realrestorer`  
**Last event:** 2026-03-27 · 1 dated since 2026-03-27 · **Researched:** 2026-09-05 · confidence: high

## What it is

RealRestorer is a Step1X-Edit fine-tune for image restoration rather than general image generation.

- Removes blur, noise, haze, rain, moiré, reflections, flare, and compression artifacts.
- Preserves scene structure and semantic content through an image-and-instruction pipeline.
- Ships code, weights, synthetic-degradation tooling, and RealIR-Bench.

## Development line

- **2026-03-27 — RealRestorer project resources were linked.** On 2026-03-27, the RealRestorer development line was recorded with links to a project page, source repository, model page, and The source reference. This is material to the project history because it establishes a dated public reference point for its associated code and model resources. The supplied links alone do not establish the exact release status, capabilities, or versions.

## What changed

2026-03-26 — RealRestorer released its model weights, synthetic-degradation pipeline, and RealIR-Bench; the paper describes nine degradation categories and a 464-image benchmark. 2026-03-27 — The project’s public reference set connected the project page, code, model card, and paper; the official release record corrects the underlying launch date to 2026-03-26. 2026-03-29 — A Hugging Face demo became available, adding a browser-accessible trial route.

## How to use this

From 2026-03-27, practitioners should treat RealRestorer as a project with linked code and model resources, while verifying exact versions, capabilities, and usage terms from the linked primary sources before adoption.

1. Clone the official repository, install its bundled patched diffusers checkout with Python 3.12, then install the project and benchmark requirements.
  — <https://github.com/yfyang007/RealRestorer>
2. Download the RealRestorer/RealRestorer weights and load them with RealRestorerPipeline using BF16; supply an RGB input image and a restoration instruction.
  — <https://huggingface.co/RealRestorer/RealRestorer>
3. Run 28 denoising steps, guidance scale 3.0, seed 42, and size level 1024; save the returned image.
  — <https://huggingface.co/RealRestorer/RealRestorer>

## Best practices

- Use the repository’s patched local diffusers checkout rather than assuming a stock Diffusers installation implements RealRestorerPipeline.
  — <https://github.com/yfyang007/RealRestorer>
- Start with CUDA, BF16, 28 steps, guidance 3.0, seed 42, and about 1024×1024 input; budget roughly 34 GB peak GPU memory at that setting.
  — <https://github.com/yfyang007/RealRestorer>
- Treat the released model and benchmark assets as non-commercial academic-research material, even though the code is intended for Apache-2.0 release.
  — <https://huggingface.co/RealRestorer/RealRestorer>

## Superseded by this

- 2026-03-29 — A command-line-only access assumption is obsolete: the official repository records release of a Hugging Face demo.

## Still unknown

- The available evidence does not establish that 2026-03-27 introduced a separate technical release rather than documenting the 2026-03-26 release.
- The paper’s top-open-source benchmark result has not been independently replicated in the sources reviewed.
- event_findings:[{"event_date":"2026-03-27","finding":"Correction: the official repository dates the releases of RealRestorer weights, the degradation pipeline, and RealIR-Bench to 2026-03-26, one day before this dated record.","source_url":"https://github.com/yfyang007/RealRestorer","source_date":"2026-03-26"},{"event_date":"2026-03-27","finding":"The exact released model is RealRestorer/RealRestorer: a 12B BF16 model fine-tuned from stepfun-ai/Step1X-Edit; its model card distinguishes Apache-2.0-intended code from non-commercial academic-research model and benchmark assets.","source_url":"https://huggingface.co/RealRestorer/RealRestorer","source_date":"2026-03-26"}]
- new_events:[{"date":"2026-03-26","finding":"The paper, weights, synthetic degradation pipeline, and RealIR-Bench launch were documented. The benchmark contains 464 real degraded images across nine common degradation types.","source_url":"https://arxiv.org/abs/2603.25502","source_date":"2026-03-26"},{"date":"2026-03-29","finding":"The official repository announced release of a Hugging Face demo for RealRestorer.","source_url":"https://github.com/yfyang007/RealRestorer","source_date":"2026-03-29"}]

## Sources

| source | title | read |
|---|---|---|
| https://yfyang007.github.io/RealRestorer/ | RealRestorer: Towards Generalizable Real-World Image Restoration | 2026-09-05 |
| https://github.com/yfyang007/RealRestorer | yfyang007/RealRestorer | 2026-09-05 |
| https://huggingface.co/RealRestorer/RealRestorer | RealRestorer/RealRestorer model card | 2026-09-05 |
| https://arxiv.org/abs/2603.25502 | RealRestorer: Towards Generalizable Real-World Image Restoration with Large-Scale Image Editing Models | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:realrestorer`, thread `realrestorer`, 1 dated events 2026-03-27 → 2026-03-27.
- **Practical note:** From 2026-03-27, practitioners should treat RealRestorer as a project with linked code and model resources, while verifying exact versions, capabilities, and usage terms from the linked primary sources before adoption.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
