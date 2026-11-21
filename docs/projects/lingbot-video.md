---
title: LingBot-Video
category: projects
date: 2026-07-09
tags: [lingbot-video, lingbot-video-development, project]
aliases: ["LingBot-Video"]
---

# LingBot-Video

**Development line:** `project:lingbot-video` · thread `lingbot-video-development`  
**Last event:** 2026-07-09 · 1 dated since 2026-07-09 · **Researched:** 2026-11-21 · confidence: medium

## What it is

LingBot-Video is an Apache 2.0 open-source mixture-of-experts video generation model family aimed at embodied intelligence.

- Users: robotics and embodied-AI researchers who need video generation from text or from text plus an image.
- Key capability: text-to-image, text-to-video, and text-plus-image-to-video, with a 1.3B dense model, a 30B-A3B MoE model with a refiner, and an 8-step distilled MoE student.
- Limits: the DiT expects structured JSON captions, so a prompt rewriter is recommended; the README gives no minimum hardware, and the reported examples used a GPU with about 140 GiB of memory.

## Development line

- **2026-07-09 — LingBot-Video public project resources appeared.** Verified: the technical report, code, models, and rewriters were released on 2026-07-09 (repository README release history).

## What changed

- 2026-07-09 — Technical report, code, models, and prompt rewriters released.
- 2026-07-09 — Leaderboard ranking on the RBench evaluation stated "as of July 9th, 2026."
- 2026-08-05 — RBench evaluation released.
- 2026-09-18 — 8-step DMD student model released.

## How to use this

1. Read the README for the variant lineup and release history. — <https://github.com/robbyant/lingbot-video>
2. Create a Python 3.10+ virtual environment, run `pip install -r requirements.txt`, then `pip install -e .`. Optionally install SGLang dependencies with `pip install --no-deps -r requirements-sglang.txt`. The README pins transformers 5.8.1 and diffusers 0.39.0 and recommends a specific torch nightly build. — <https://github.com/robbyant/lingbot-video>
3. Download the model weights and set `MODEL_DIR` to the local model root. — <https://github.com/robbyant/lingbot-video>
4. For the fast path, run `scripts/single-gpu/run_moe_dmd_t2v.sh` (or the `ti2v` variant): 8 steps, guidance scale 1.0, shift 3.0, 121 frames at 832×480 and 24 fps. — <https://github.com/robbyant/lingbot-video>
5. For the full workflow, rewrite the prompt with `rewriter/inference.py`, generate a negative prompt with `rewriter/auto_negative.py`, then run `scripts/inference.py --prompt_json`. The README calls this the recommended path. — <https://github.com/robbyant/lingbot-video>

## Best practices

- Pass structured JSON captions or run the rewriter on plain prompts; the README says the DiT is designed for JSON captions, not casual prompts. — <https://github.com/robbyant/lingbot-video>
- Do not add Auto Negative to the DMD recipe at guidance scale 1.0; the ordinary MoE scripts use a different recipe. — <https://github.com/robbyant/lingbot-video>
- Plan memory for the workload: the observed single-GPU 5-second peak was about 82 GiB, which the README says is not a minimum. For multi-GPU FSDP, each rank builds the transformer in host memory first, so large system RAM is required. — <https://github.com/robbyant/lingbot-video>
- Pin the torch, transformers, and diffusers versions from the README to reproduce results. — <https://github.com/robbyant/lingbot-video>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- Minimum hardware requirements for each variant.
- Independent benchmark results beyond the RBench mention; the README gives no comparison table in the text read.
- The license of the Qwen3.6-27B-based rewriter was not checked.
- The Hugging Face collection and the separate project page were not read.
- Real embodied-AI use cases are not demonstrated in the sources read.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/robbyant/lingbot-video | LingBot-Video repository README (release history, license, usage) | 2026-11-21 |

## Agent brief {#agent-brief}

- **Subject:** `project:lingbot-video`, thread `lingbot-video-development`, 1 dated event 2026-07-09 (verified), plus releases 2026-08-05 and 2026-09-18.
- **Practical note:** As of 2026-11, use the DMD 8-step student for fast tests and the rewriter-plus-MoE path for full quality. Budget GPU and host memory from the README examples; the README gives no minimum.
- **Confidence:** medium. Single primary source (repository README) read; hardware minimums and independent benchmarks unverified. Dated supersedes above are the authority for what is obsolete.
