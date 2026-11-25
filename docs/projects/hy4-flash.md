---
title: "Hy4 Flash: hy4-flash-release — Hy4 Flash Release"
category: "projects"
date: 2026-11-18
tags: ["hy4-flash", "hy4-flash-release", "project"]
aliases: ["Hy4 Flash: hy4-flash-release"]
---

# Hy4 Flash: hy4-flash-release — Hy4 Flash Release

Hy4 Flash is Tencent's open-weights multimodal mixture-of-experts model for document processing, visual analysis and agent workflows.

**Development line:** project:hy4-flash · thread hy4-flash-release  
**Last event:** 2026-11-18 · 4 dated since 2026-11-18 · **Researched:** 2026-11-20 · confidence: high

## What it is

Hy4 Flash is a multimodal mixture-of-experts foundation model from Tencent, released with open weights. It is a lower-latency alternative to dense large language models for high-throughput document processing, visual analysis and agent workflows. It offers:

- Text and image understanding natively, for document analysis, charts and image inputs.
- Context up to one million tokens, using hybrid attention and compressed KV cache structures.
- Fast generation through LatentMoE routing and Engram embedding lookups.
- Fewer output tokens, from self-distillation and reinforcement learning stages.
- Quantized deployment: an FP8 checkpoint and community GGUF formats down to IQ2 quantization.

The model has 224 billion total parameters, with 12 billion active per token. Quantized local runs need a multi-GPU setup or at least 126 GB of video memory. Throughput is high enough for resource-constrained enterprise and local deployments.

## Development line

- **2026-11-18 — Hy4 Flash model released with open weights.** Tencent released Hy4 Flash with open weights, including Hy4 Flash-FP8 and Hy4 Flash-Base. It has 224B total parameters (12B active), a context of up to 1M tokens and native multimodal input. The license is the Tencent Hy License. The announcement says Hy4 is expected next.
- **2026-11-18 — Hy4 Flash model weights released.** The Hy4 Flash weights were published on 2026-11-18, in the Hy4 flash, Hy4 flash-FP8 and Hy4 flash-Base variants. The release links to Hugging Face, GitHub and the Tencent research page.
- **2026-11-18 — Hy4 Flash model weights released.** A second announcement dated 2026-11-18 lists the same three variants: Hy4 Flash, Hy4 flash-FP8 and Hy4 flash-Base. It links to Hugging Face, GitHub and the project research page.
- **2026-11-18 — Hy4 flash open weights released.** On 2026-11-18 the open weights of Hy4 flash were published. The model has about 220B total parameters, about 12B active per token, text and image input, and a 1M-token context window. It was built by self-distillation from Hy4 plus an RL stage that halves output tokens. Quantized GGUF builds exist. The most aggressive one, IQ2, needs at least 126 GB VRAM.
- **2026-11-18 — other reporting on this date.**
  - The official Hugging Face repository says the 224B total includes about 64B parameters in Engram hash-based embedding tables. LatentMoE and hybrid attention cut the KV cache to 1/6 of Hy4. Decoding uses a DFly draft head and reaches over 150 tokens per second. (2026-11-18) — <https://huggingface.co/tencent/Hy4-flash>
  - The GitHub repository holds official deployment code and inference scripts for vLLM and Hugging Face Transformers. It lists the tencent/Hy4-flash (Instruct), tencent/Hy4-flash-FP8 and tencent/Hy4-flash-base repositories, all under the Tencent Hy License. (2026-11-18) — <https://github.com/Tencent-Hunyuan/Hy4-flash>
  - The repository documentation says the model is built for everyday office and agent workflows: deep search, document processing, PPT modification and computer use. It has a 1M context window and native text-image input. (2026-11-18) — <https://github.com/Tencent-Hunyuan/Hy4-flash>
  - Community GGUF quantizations from AngelSlim show that local runs need at least 126 GB VRAM for the `IQ2_XXS` format. Higher-precision quants such as `Q4_K_M` or Q8 need multi-GPU setups above 150-240 GB VRAM. (2026-11-18) — <https://huggingface.co/AngelSlim/Hy4-flash-GGUF>

## What changed

Tencent added Hy4 Flash to the Hunyuan model family. It was built by self-distillation from the larger Hy4 and by reinforcement learning that cuts output tokens. The release put out base, instruction-tuned and FP8 quantized weights, with community quantization formats alongside. It comes before the wider rollout of the flagship Hy4 system.

## How to use this

1. Clone the official repository, or install a supported runtime such as vLLM or Transformers.
  — <https://github.com/Tencent-Hunyuan/Hy4-flash>
2. Download the weights you need from Hugging Face. Use tencent/Hy4-flash for general instruction following, or tencent/Hy4-flash-FP8 to save memory.
  — <https://huggingface.co/tencent/Hy4-flash>
3. On consumer multi-GPU or high-memory local systems, download the quantized GGUF weights from AngelSlim/Hy4-flash-GGUF. Run them with llama.cpp or a compatible text-generation loader.
  — <https://huggingface.co/AngelSlim/Hy4-flash-GGUF>

## Best practices

- Use the FP8 checkpoint, or turn on speculative decoding with the DFly draft head, to keep throughput above 150 tokens per second while holding VRAM down.
  — <https://huggingface.co/tencent/Hy4-flash>
- Reserve enough GPU memory before loading the 1M context window. Hybrid attention already cuts the KV cache to 1/6 of Hy4.
  — <https://github.com/Tencent-Hunyuan/Hy4-flash>
- On local workstations, allocate at least 126 GB of VRAM across GPUs for the IQ2 format, so offload does not run out of memory.
  — <https://huggingface.co/AngelSlim/Hy4-flash-GGUF>

## Superseded by this

- Before the Hy4 Flash MoE release, Hunyuan models were limited to proprietary API endpoints or to dense architectures with high serving memory requirements.
  — <https://github.com/Tencent-Hunyuan/Hy4-flash>

## Still unknown

- Benchmark scores on third-party coding and reasoning leaderboards were not independently validated across all context lengths.
- Web searches for Chinese secondary media and community forums returned only opaque redirects, not permanent article paths, so no third-party commentary is cited.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/tencent/Hy4-flash | tencent/Hy4-flash · Hugging Face | 2026-11-20 |
| https://github.com/Tencent-Hunyuan/Hy4-flash | Tencent-Hunyuan/Hy4-flash: Official PyTorch implementation and deployment guidelines for Hy4-flash | 2026-11-20 |
| https://huggingface.co/AngelSlim/Hy4-flash-GGUF | AngelSlim/Hy4-flash-GGUF · Hugging Face | 2026-11-20 |

## Agent brief {#agent-brief}

- **Subject:** project:hy4-flash, thread hy4-flash-release, 4 dated events 2026-11-18 → 2026-11-18.
- **Practical note:** see the usage and practice sections above, with their limits.
- **Confidence:** high. The dated supersedes above decide what is obsolete.
