---
title: SAMA
category: projects
date: 2026-03-20
tags: [project, sama]
aliases: ["SAMA"]
---

# SAMA

**Development line:** `project:sama` · thread `sama`  
**Last event:** 2026-03-20 · 1 dated since 2026-03-20 · **Researched:** 2026-09-05 · confidence: high

## What it is

An open-source instruction-guided video editing model for Wan users who change objects, style, or text in a video while keeping motion.

- Semantic anchoring plans edits across keyframes.
- Motion alignment preserves temporal dynamics.
- SAMA-14B checkpoint and an official ComfyUI workflow are available.

Requires Linux, an NVIDIA GPU, Python 3.10, a CUDA 12.1-compatible environment, and Wan2.1-T2V-14B. This is a local inference stack on top of Wan, not a hosted service.

## Development line

- **2026-03-20 — SAMA public project, source, and model resources were linked.** On 2026-03-20, a dated SAMA message linked the project's public website, source repository, and the Hugging Face page for SAMA-14B. These links establish that the three public resources were associated with SAMA on that date, without establishing further claims about the model or project.

## What changed

- **2026-03-20** — SAMA paper published; preprint submitted on 2026-03-19 with 24 pages and 12 figures.
- **2026-03-21** — SAMA-14B checkpoint released; SAMA-5B still marked as Coming soon.
- **2026-03-24** — Official SAMA-ComfyUI workflow opened.
- **2026-06-20** — SAMA accepted to ECCV 2026.
- **2026-06-26** — SAMA-edit-filtered-1M metadata set published.

## How to use this

As of 2026-03-20, we use the linked SAMA website, source repository, and SAMA-14B model page as starting points for evaluation, verifying capabilities, licensing, and usage requirements from those resources before adoption.

1. Clone the repository, create a Python 3.10 environment, and install dependencies.
  — <https://github.com/Cynthiazxy123/SAMA>
2. Download SAMA-14B and prepare the full local Wan2.1-T2V-14B directory.
  — <https://huggingface.co/syxbb/SAMA-14B>
3. Set MODEL_ROOT, STATE_DICT, SRC_VIDEO, PROMPT, and OUTPUT_DIR in infer_sh/run_sama.sh, then run the script.
  — <https://github.com/Cynthiazxy123/SAMA>
4. For a node-based workflow, use the official ComfyUI integration with the Wan base model and SAMA-14B.
  — <https://github.com/Cynthiazxy123/SAMA>

## Best practices

- Verify the base Wan2.1-T2V-14B directory is complete: the script intentionally stops if files are missing.
  — <https://github.com/Cynthiazxy123/SAMA>
- Use the source FPS; set --fps explicitly when it is missing.
  — <https://github.com/Cynthiazxy123/SAMA>
- Account for automatic padding of input frames to the Wan 4k+1 requirement.
  — <https://github.com/Cynthiazxy123/SAMA>

## Superseded by this

- 2026-03-20 — paper-only state: SAMA-14B is available as of 2026-03-21, and the official ComfyUI workflow is available as of 2026-03-24.

## Still unknown

- Official materials do not provide measured VRAM, inference speed, or supported resolutions. Hardware planning requires separate testing of the configuration and workflow.

## Sources

| source | title | read |
|---|---|---|
| https://cynthiazxy123.github.io/SAMA/ | SAMA: Factorized Semantic Anchoring and Motion Alignment for Instruction-Guided Video Editing | 2026-09-05 |
| https://github.com/Cynthiazxy123/SAMA | Cynthiazxy123/SAMA — official inference code | 2026-09-05 |
| https://huggingface.co/syxbb/SAMA-14B | syxbb/SAMA-14B | 2026-09-05 |
| https://arxiv.org/abs/2603.19228 | SAMA: Factorized Semantic Anchoring and Motion Alignment for Instruction-Guided Video Editing | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:sama`, thread `sama`, 1 dated events 2026-03-20 → 2026-03-20.
- **Practical note:** As of 2026-03-20, practitioners can use the linked SAMA website, source repository, and SAMA-14B model page as the primary starting points for evaluation, while verifying capabilities, licensing, and usage requirements from those resources before adoption.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.