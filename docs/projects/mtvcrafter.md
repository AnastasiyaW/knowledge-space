---
title: MTVCrafter
category: projects
date: 2025-05-22
tags: [mtvcrafter, mtvcrafter-public-development, project]
aliases: ["MTVCrafter"]
---

# MTVCrafter

**Development line:** `project:mtvcrafter` · thread `mtvcrafter-public-development`  
**Last event:** 2025-05-22 · 1 dated since 2025-05-22 · **Researched:** 2026-09-04 · confidence: medium

## What it is

MTVCrafter is a local human-image animation pipeline for GPU users who supply a reference image and a driving video with recoverable SMPL motion.

- 4DMoT turns 3D joints over time into motion tokens.
- MV-DiT drives a CogVideoX or Wan2.1 image-to-video backbone.
- The Wan path adds text control.

The shipped scripts generate 49-frame units and target CUDA. Run the repository and checkpoints locally, because the official Space lacks a working GPU driver.

## Development line

- **2025-05-22 — MTVCrafter public resources were linked.** MTVCrafter established the 4DMoT-plus-MV-DiT approach. It animates a reference image directly from raw 3D motion instead of rendered 2D pose maps.

## What changed

- 2025-05-22: MTVCrafter established the 4DMoT-plus-MV-DiT approach. The pipeline animates a reference image directly from raw 3D motion rather than rendered 2D pose maps.
- 2025-08-15: The associated MV-DiT checkpoint tree separated the method into CogVideoX and Wan-2.1 local-inference paths.

## How to use this

From 2025-05-22 onward, start with the dated project page, repository, and Hugging Face model page when locating MTVCrafter. The 2025-08-15 link alone does not establish a new component, release, or workflow.

1. Clone the current implementation, create a clean Python 3.10+ environment, and install requirements.txt.
  — <https://github.com/DINGYANB/MTVCrafter>
2. Download the NLF pose estimator, a matching base model (CogVideoX-5B for 7B or Wan2.1 I2V-14B for 17B), and the MTVCrafter 4DMoT/MV-DiT weights.
  — <https://github.com/DINGYANB/MTVCrafter>
3. Start with data/sampled_data.pkl; for a driving video, run process_nlf.py to create the SMPL motion-video .pkl input.
  — <https://github.com/DINGYANB/MTVCrafter>
4. Run the CogVideoX route with infer_7b.py, a reference image, motion-data path, and --output_dir.
  — <https://github.com/DINGYANB/MTVCrafter/blob/main/infer_7b.py>
5. For Wan text direction, use infer_17b.py with the same paths and optional --prompt; it also accepts --output_dir.
  — <https://github.com/DINGYANB/MTVCrafter/blob/main/infer_17b.py>
6. For the 17B route, provide at least 89 input frames: the script joins two 49-frame clips with a nine-frame overlap.
  — <https://github.com/DINGYANB/MTVCrafter/blob/main/infer_17b.py>

## Best practices

- Install pinned project requirements in a clean environment instead of assembling a generic Diffusers stack.
  — <https://github.com/DINGYANB/MTVCrafter>
- Use --output_dir, the current documented and implemented output flag for both inference paths.
  — <https://github.com/DINGYANB/MTVCrafter>
- Check for a CUDA GPU before running; the official Space fails because its runtime has no NVIDIA driver.
  — <https://huggingface.co/spaces/yanboding/MTVCrafter>
- Validate a first run with the supplied sampled_data.pkl before debugging NLF extraction from custom footage.
  — <https://github.com/DINGYANB/MTVCrafter>
- Use the author scripts as the canonical path: the 7B script builds a custom MTVCrafterPipeline7B and separately loads CogVideoX and 4DMoT assets.
  — <https://github.com/DINGYANB/MTVCrafter/blob/main/infer_7b.py>
- Treat the optional Wan FusionX LoRA as a trade-off: maintainers note it can improve speed and detail but may worsen motion accuracy.
  — <https://github.com/DINGYANB/MTVCrafter>

## Superseded by this

- 2025-08-24: --output_path quick-start guidance is obsolete; current inference scripts use --output_dir.
- 2026-03-09: MTVCrafter is no longer the arXiv paper title; cite MTVCraft for the revised paper and MTVCrafter for the repositories.
- 2026-09-04: Guidance to use the official demo Space is obsolete; the Space fails before inference because its runtime lacks an NVIDIA driver.
- 2026-09-04: Treating DINGYANB/MTVCtafter as the code checkout is obsolete; it is the static project-page repository.

## Still unknown

- The 2025-08-15 MV-DiT tree omits an authored upload date, so its exact publication time cannot be independently verified.
- The maintainer links the static project page MTVCtafter and the runnable code repository MTVCrafter, but has not documented why the names differ.
- The revised arXiv paper is titled MTVCraft while the code and model repositories retain MTVCrafter; no maintainer note explains the naming change.
- No first-party Chinese documentation or independently reproducible Chinese operating report was found.
- No current first-party GPU-memory requirement or independently reproduced quality benchmark was found.
- The generic Diffusers snippet on the model page is not confirmed to reproduce the author-maintained inference scripts.

## Sources

| source | title | read |
|---|---|---|
| https://dingyanb.github.io/MTVCtafter/ | MTVCrafter project page | 2026-09-04 |
| https://github.com/dingyanb/MTVCtafter | DINGYANB/MTVCtafter project-page repository | 2026-09-04 |
| https://github.com/DINGYANB/MTVCtafter/blob/main/index.html | MTVCtafter static project-page source | 2026-09-04 |
| https://github.com/DINGYANB/MTVCrafter | DINGYANB/MTVCrafter implementation repository | 2026-09-04 |
| https://github.com/DINGYANB/MTVCrafter/commits/main | DINGYANB/MTVCrafter commit history | 2026-09-04 |
| https://github.com/DINGYANB/MTVCrafter/blob/main/infer_7b.py | MTVCrafter 7B inference script | 2026-09-04 |
| https://github.com/DINGYANB/MTVCrafter/blob/main/infer_17b.py | MTVCrafter 17B inference script | 2026-09-04 |
| https://huggingface.co/yanboding/MTVCrafter | yanboding/MTVCrafter model repository | 2026-09-04 |
| https://huggingface.co/yanboding/MTVCrafter/tree/main/MV-DiT | MTVCrafter MV-DiT checkpoint tree | 2026-09-04 |
| https://huggingface.co/yanboding/MTVCrafter/blob/main/README.md | MTVCrafter model-card README | 2026-09-04 |
| https://huggingface.co/spaces/yanboding/MTVCrafter | MTVCrafter Hugging Face Space runtime status | 2026-09-04 |
| https://arxiv.org/abs/2505.10238 | MTVCraft / MTVCrafter paper record | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:mtvcrafter`, thread `mtvcrafter-public-development`, 1 dated events 2025-05-22 → 2025-05-22.
- **Practical note:** From 2025-05-22 onward, practitioners should begin with the dated project page, repository, and Hugging Face model page when locating MTVCrafter. The 2025-08-15 link alone does not establish a new component, release, or workflow.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
