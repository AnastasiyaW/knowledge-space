---
title: Penguin-VL
category: projects
date: 2026-03-09
tags: [penguin-vl, penguin-vl-public-release, project, tencent-ailab]
aliases: ["Penguin-VL"]
---

# Penguin-VL

**Development line:** `project:penguin-vl` · thread `penguin-vl-public-release`  
**Last event:** 2026-03-09 · 1 dated since 2026-03-09 · **Researched:** 2026-09-05 · confidence: high

## What it is

Penguin-VL is a Qwen3-based VLM family for local multimodal inference rather than a hosted vision API.

- Image, document, chart, multi-image, and video prompts
- Transformers, Gradio, and vLLM serving paths
- 2B and 8B checkpoints, plus a 0.4B vision encoder

## Development line

- **2026-03-09 — Penguin-VL public project resources were shared.** On 2026-03-09, a dated message linked the project website, source repository, Hugging Face collection, and Hugging Face Space. We can inspect published assets and test the demo. The dated links do not establish the exact model version, technical claims, license, or release scope.

## What changed

- 2026-03-09 — Tencent released Penguin-VL-2B, Penguin-VL-8B, Penguin-Encoder, inference code, a vLLM plugin, and a Gradio demo.
- 2026-03-17 — training code was released.
- 2026-03-20 — Penguin-Recap-I, the accompanying reconstructed image-training data, was released.
- 2026-03-26 — lmms-eval gained Penguin-VL benchmark support.
- 2026-03-30 — Penguin-Recap-V, video data with dense time-, paragraph-, and video-level annotations, was released.

## How to use this

As of 2026-03-09, we can evaluate Penguin-VL through the linked website, source repository, Hugging Face collection, and demo. Check capabilities, versions, licensing, and deployment requirements in the primary sources before production use.

1. Set up a clean environment with Python 3.11.13, PyTorch 2.5 or later, and CUDA 11.8 or later. Install repository requirements, then run the Transformers example with `tencent/Penguin-VL-2B` or `tencent/Penguin-VL-8B`.
  — <https://github.com/tencent-ailab/Penguin-VL>
2. For direct Python integration, load `tencent/Penguin-VL-8B` through `AutoModelForCausalLM` and `AutoProcessor` with `trust_remote_code=True`. Pass image, video, or text inputs to the processor.
  — <https://huggingface.co/tencent/Penguin-VL-8B>
3. For an internal visual test UI, run `inference/launch_gradio_demo.py --model-path tencent/Penguin-VL-2B` or the 8B checkpoint. Use the local interface.
  — <https://github.com/tencent-ailab/Penguin-VL>
4. For an OpenAI-compatible serving endpoint, install the separate vLLM stack and run `python -m penguinvl.plugin.vllm serve tencent/Penguin-VL-8B`.
  — <https://github.com/tencent-ailab/Penguin-VL>

## Best practices

- Keep Transformers inference and vLLM inference in separate environments so dependencies do not clash. The documented vLLM 0.11.0 path requires PyTorch 2.8, while the standard path recommends PyTorch 2.5 or later.
  — <https://github.com/tencent-ailab/Penguin-VL>
- Install vLLM before Flash Attention on the vLLM path. The project documents this order to avoid dependency conflicts.
  — <https://github.com/tencent-ailab/Penguin-VL>
- Test representative OCR, document, chart, and video inputs in the inference notebook before routing production traffic on benchmark claims.
  — <https://github.com/tencent-ailab/Penguin-VL>

## Superseded by this

- 2026-03-17 — the 2026-03-09 inference-only release is incomplete for training or fine-tuning; training code is now available.
- 2026-03-20 — guidance that Penguin-VL training data was unavailable is obsolete for images; Penguin-Recap-I is available.
- 2026-03-30 — image-only training data guidance is incomplete for video work; Penguin-Recap-V adds multi-granularity video annotations.

## Still unknown

- The hosted Hugging Face Space threw a configuration error on 2026-09-05; use local Gradio for demos.
- Independent deployment and cost measurements are missing from first-party sources.
- We skipped the hf.ru redirect because its destination and publication context were unverified.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/tencent-ailab/Penguin-VL | Tencent AI Lab Penguin-VL repository and release history | 2026-09-05 |
| https://huggingface.co/tencent/Penguin-VL-8B | tencent/Penguin-VL-8B model card | 2026-09-05 |
| https://huggingface.co/collections/tencent/penguin-vl | Tencent Penguin-VL collection | 2026-09-05 |
| https://huggingface.co/spaces/tencent/Penguin-VL | Tencent Penguin-VL Space | 2026-09-05 |
| https://arxiv.org/abs/2603.06569 | Penguin-VL: Exploring the Efficiency Limits of VLM with LLM-based Vision Encoders | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:penguin-vl`, thread `penguin-vl-public-release`, 1 dated events 2026-03-09 → 2026-03-09.
- **Practical note:** As of 2026-03-09, evaluate Penguin-VL via the linked site, repository, Hugging Face collection, and demo. Verify capabilities, versions, licensing, and deployment needs before production use.
- **Confidence:** high. Dated supersedes above define what is obsolete.
