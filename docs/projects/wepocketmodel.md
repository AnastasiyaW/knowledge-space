---
title: "Wepocketmodel: wepocketmodel-release-line — Wepocketmodel Release Line"
category: "projects"
date: 2026-11-23
tags: ["project", "wepocketmodel", "wepocketmodel-release-line"]
aliases: ["Wepocketmodel: wepocketmodel-release-line"]
---

# Wepocketmodel: wepocketmodel-release-line — Wepocketmodel Release Line

**Development line:** project:wepocketmodel · thread wepocketmodel-release-line  
**Last event:** 2026-11-23 · 2 dated since 2026-11-23 · **Researched:** 2026-11-24 · confidence: high

## What it is

WePocketModel is an on-device multimodal model family from Tencent WeChat AI. It runs locally on edge CPUs and mobile hardware, as an alternative to cloud APIs like OpenAI GPT-4o-mini.

One shared vision-language backbone does three jobs:

- Multimodal text generation for optical character recognition and visual question answering
- Matryoshka representation learning embeddings, with variable dimensions from 64 to 2048
- Structured decision scoring for application state evaluation

Weights come in 2B and 4B sizes under the Apache 2.0 license. The Q4\_K\_M GGUF build needs about 3.42 GB RAM, and unquantized BF16 needs roughly 8 GB. One model replaces several discrete edge models. GGUF on CPU still needs a custom C\+\+ runtime wrapper compiled against pinned llama.cpp sources.

## Development line

- **2026-11-23 — Tencent releases WePocketModel on-device multimodal model.** Tencent WeChat published WePocketModel, a compact multimodal model that runs on-device without cloud calls. It does text generation, Matryoshka embeddings \(64 to 2048 dimensions\) and structured decisions. It comes in 4B and 2B sizes with GGUF builds, and runs on CPU as well as GPU.
- **2026-11-23 — Tencent WeChat releases WePocketModel on-device multimodal model.** WePocketModel is a small multimodal model from Tencent WeChat for on-device apps. It does text and image understanding, Matryoshka embeddings \(64 to 2048 dimensions\) and structured decisions. It comes in 4B and 2B sizes with GGUF files, and runs on CPU as well as GPU.
- **2026-11-23 — also on this date.**
  - WeChat AI released the 2B and 4B model repositories under the Apache 2.0 license. They describe the Multi-Granularity Visual Budgeting \(MGVB\) mechanism, which is meant to remove interference between the representation, generation and decision heads in one vision-language backbone. (2026-11-23) — <https://github.com/Tencent/WePocketModel>
  - Hugging Face added split GGUF packages: language-Q4\_K\_M.gguf \(~3.42 GB\) apart from multimodal-BF16.gguf. A custom C\+\+ runtime build script \(build\_gguf.py\) comes with them, compiled against a pinned llama.cpp revision for local CPU execution. (2026-11-23) — <https://huggingface.co/tencent/WePocketModel1.0-4B-GGUF>

## What changed

On-device vision-language systems moved from several models to one set of parameters. Tencent WeChat introduced WePocketModel in two sizes. A shared vision-language backbone plus multi-granularity visual budgeting reconciles the conflicts between generative output, vector retrieval and discrete decision routing.

Delivery grew from PyTorch transformer checkpoints to cross-platform GGUF files. The 4-bit quantized language weights are now separate from the 16-bit multimodal projection modules, and a dedicated native runtime library supports them.

## How to use this

1. Clone the repository. Install the PyTorch CPU dependencies and the GGUF runtime requirements from inference/requirements-gguf.txt.
  — <https://github.com/Tencent/WePocketModel>
2. Compile the native C\+\+ runtime library \(libwepm\_gguf\) with CMake and the bundled pinned llama.cpp submodule. Run python inference/build\_gguf.py.
  — <https://github.com/Tencent/WePocketModel>
3. Download the quantized bundle with the Hugging Face CLI. It holds language-Q4\_K\_M.gguf and multimodal-BF16.gguf.
  — <https://huggingface.co/tencent/WePocketModel1.0-4B-GGUF>
4. Set the WEPM\_MODEL environment variable to the model directory. Then run a task script such as examples/cpu/generation/run.sh.
  — <https://huggingface.co/tencent/WePocketModel1.0-4B-GGUF>

## Best practices

- Pair the Q4\_K\_M language quantization with BF16 multimodal weights. Resident memory stays near 3.42 GB, and the visual projector calculations stay stable.
  — <https://huggingface.co/tencent/WePocketModel1.0-4B-GGUF>
- Truncate Matryoshka embeddings to 256 or 512 dimensions for high-throughput mobile vector indexes. Keep the full 2048 dimensions for precise re-ranking.
  — <https://huggingface.co/tencent/WePocketModel1.0-4B>
- Use Multi-Granularity Visual Budgeting \(MGVB\) to split visual token budgets between coarse and fine regions, according to how complex the text query is.
  — <https://github.com/Tencent/WePocketModel>

## Superseded by this

- Separate on-device models for visual question answering, dense vector retrieval and structured decision control flows.
  — <https://github.com/Tencent/WePocketModel>

## Still unknown

- Inference latency and memory use on specific mobile SoCs, such as Apple Silicon and Qualcomm Snapdragon. The initial open-source release documentation does not cover them.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/Tencent/WePocketModel | Tencent/WePocketModel: Official Repository for WePocketModel \(WePM\) | 2026-11-24 |
| https://huggingface.co/tencent/WePocketModel1.0-4B | tencent/WePocketModel1.0-4B on Hugging Face | 2026-11-24 |
| https://huggingface.co/tencent/WePocketModel1.0-4B-GGUF | tencent/WePocketModel1.0-4B-GGUF on Hugging Face | 2026-11-24 |
| https://huggingface.co/tencent/WePocketModel1.0-2B | tencent/WePocketModel1.0-2B on Hugging Face | 2026-11-24 |

## Agent brief {#agent-brief}

- **Subject:** project:wepocketmodel, thread wepocketmodel-release-line, 2 dated events 2026-11-23 → 2026-11-23.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. The dated supersedes above are the authority on what is obsolete.
