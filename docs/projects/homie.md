---
title: HOMIE
category: projects
date: 2026-07-22
tags: [homie, homie-public-project-release, project]
aliases: ["HOMIE"]
---

# HOMIE

**Development line:** `project:homie` · thread `homie-public-project-release`  
**Last event:** 2026-07-22 · 1 dated since 2026-07-22 · **Researched:** 2026-09-05 · confidence: medium

## What it is

HOMIE is an open-source local video generation pipeline driven by reference images of people, products, logos, OCR maps, and multi-view shots.

- Multi-subject composition: combines multiple distinct subjects in one video clip.
- Multi-reference alignment: uses several references of one subject for text accuracy or viewpoint consistency.

Running it requires Wan2.1-T2V-14B, separate HOMIE weights at 37.1 GB, and Qwen3-VL-2B-Thinking.

This is a research inference release, not a cloud service.

## Development line

- **2026-07-22 — HOMIE public project resources appeared.** On 2026-07-22, the project linked its website, GitHub repository, and Hugging Face model page homie-r2v-wan2.1 together. These links provide public documentation, source code, and model distribution in one place. Precise release claims, version details, capabilities, and license are not stated.

## What changed

2026-07-20 — The HOMIE technical report appeared on arXiv, establishing a unified method for inter- and intra-subject video personalization.

2026-07-21 — Inference code and checkpoints fine-tuned on Wan2.1-T2V-14B were published.

2026-07-22 — The project page, code, and weights described a single local workflow, with no separate version change found on this day.

## How to use this

From 2026-07-22, start with the linked project page, source repository, and Hugging Face model page. Verify the project documentation, requirements, and license before use.

1. Install the environment using `set_env.sh`. This requires PyTorch 2.4.0 or newer with a compatible CUDA build.
  — <https://github.com/YIYANGCAI/HOMIE>
2. Download Wan-AI/Wan2.1-T2V-14B-Diffusers, `yychai/homie-r2v-wan2.1` weights, and Qwen/Qwen3-VL-2B-Thinking into the specified directories.
  — <https://github.com/YIYANGCAI/HOMIE>
3. Create a JSONL file: outer lists in `reference_paths` separate subjects, and `prompt` describes the video.
  — <https://github.com/YIYANGCAI/HOMIE>
4. Run `generate_mllm_feature.py`, then pass the generated JSONL with `mllm_feature` paths to `generate.py`.
  — <https://github.com/YIYANGCAI/HOMIE>

## Best practices

- Do not skip feature extraction with Qwen3-VL-2B-Thinking: inference expects a JSONL with added `mllm_feature` paths.
  — <https://github.com/YIYANGCAI/HOMIE>
- Start with the documented single-GPU mode: 832×480, 97 frames, 24 fps, and a fixed `base_seed`. Apply FSDP and context parallel only on a suitable multi-GPU node.
  — <https://github.com/YIYANGCAI/HOMIE>
- For context parallel, use the documented 8×A100 example with `ULYSSES_SIZE=8` and `RING_SIZE=1`. This is a sample configuration, not a stated hardware minimum.
  — <https://github.com/YIYANGCAI/HOMIE>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The repository lacks versioned releases or a changelog: the exact commit or weight corresponding to the 2026-07-22 entry is not established.
- Official minimum VRAM, generation time, and tested configurations beyond the 8×A100 example are not published.
- The current README includes a context-parallel scenario, but the source does not date its addition, so it is not listed as a separate dated event.

## Sources

| source | title | read |
|---|---|---|
| https://yiyangcai.github.io/homie-page.github.io/ | HOMIE Demo Page | 2026-09-05 |
| https://github.com/YIYANGCAI/HOMIE | YIYANGCAI/HOMIE — code and inference instructions | 2026-09-05 |
| https://huggingface.co/yychai/homie-r2v-wan2.1 | yychai/homie-r2v-wan2.1 | 2026-09-05 |
| https://arxiv.org/abs/2607.18217 | HOMIE: Human-object Centric Video Personalization via Multimodal Intelligent Enhancement | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:homie`, thread `homie-public-project-release`, 1 dated events 2026-07-22 → 2026-07-22.
- **Practical note:** From 2026-07-22, practitioners evaluating HOMIE should begin with the linked project page, source repository, and Hugging Face model page, then validate the project documentation, requirements, and license before use.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
