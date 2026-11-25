---
title: "Strata engine: strata-inference-engine — Strata Inference Engine"
category: "projects"
date: 2026-11-21
tags: ["project", "strata", "strata-inference-engine"]
aliases: ["Strata engine: strata-inference-engine"]
---

# Strata engine: strata-inference-engine — Strata Inference Engine

Strata is a C\+\+ inference engine that runs large Mixture-of-Experts models on consumer hardware, an alternative to vLLM and llama.cpp.

**Development line:** project:strata · thread strata-inference-engine  
**Last event:** 2026-11-21 · 1 dated since 2026-11-21 · **Researched:** 2026-11-22 · confidence: medium

## What it is

Strata is a C\+\+ inference engine developed by Niko Veit. It is a consumer-hardware alternative to vLLM and llama.cpp for large Mixture-of-Experts models.

Abilities:

- Tiered offload: model layers are spread across GPU VRAM, host system RAM and NVMe SSD storage.
- Sparse MoE execution: active expert weights are fetched per token.
- Quantization profiles: SQ-64, SQ-96 and SQ-128.
- Native pipelines for architectures such as Tencent Hy4-Flash.

Speed is capped by PCIe transfer bandwidth and host memory bus saturation while expert weights swap. Acceptable generation speed needs fast NVMe storage and enough host RAM.

Developers and researchers can run high-parameter MoE models locally on desktop hardware, without a multi-GPU data center server.

## Development line

- **2026-11-21 — Strata 0.2.18 adds native Tencent Hy4-Flash support.** Strata released version 0.2.18 with native Tencent Hy4-Flash support. It reports roughly 90-111 tokens/s on RTX 5090 and up to 240 tokens/s on RTX PRO 6000.
  - The v0.2.18 release targets the 220B parameter Tencent Hy4-Flash, a multimodal MoE model that activates 12B parameters per token. It adds storage tiers: SQ-64 for 64 GiB host RAM setups, SQ-96 and SQ-128. A three-tier VRAM-RAM-SSD streaming pipeline runs the model on consumer GPUs. (2026-11-21) — <https://github.com/Niko1221/Strata/releases/tag/v0.2.18>

## What changed

First came multi-tier memory paging across GPU VRAM, system RAM and SSD storage, so consumer machines could run large sparse models. Later updates added optimized quantization formats and expert caching layers to cut PCIe latency during token generation. Support then grew to multimodal Mixture-of-Experts checkpoints, with dedicated runtime kernels and tailored memory profiles for high-parameter sparse networks.

## How to use this

1. Download and extract the Strata v0.2.18 binary release, or build the C\+\+ engine from the repository source.
  — <https://github.com/Niko1221/Strata/releases/tag/v0.2.18>
2. Get the model weights and the Strata quantization pack that matches your RAM, such as SQ-64 for 64 GiB or SQ-128 for 128 GiB.
  — <https://github.com/Niko1221/Strata/releases/tag/v0.2.18>
3. Set the storage tier paths so offloaded expert layers spread across NVMe SSD, system RAM and GPU VRAM.
  — <https://github.com/Niko1221/Strata/releases/tag/v0.2.18>
4. Launch the runtime with the model configuration file, then run inference through the local CLI or API endpoint.
  — <https://github.com/Niko1221/Strata/releases/tag/v0.2.18>

## Best practices

- Keep offloaded expert weights on a PCIe 4.0 or PCIe 5.0 NVMe SSD, so I/O does not bottleneck swaps into RAM and VRAM.
  — <https://github.com/Niko1221/Strata/releases/tag/v0.2.18>
- Pick the quantization tier (SQ-64, SQ-96, SQ-128) that leaves headroom in system memory for operating system buffers and runtime overhead.
  — <https://github.com/Niko1221/Strata/releases/tag/v0.2.18>

## Superseded by this

- Running 200B\+ Mixture-of-Experts models like Tencent Hy4-Flash used to need multi-GPU enterprise server clusters or datacenter-class VRAM.
  — <https://github.com/Niko1221/Strata/releases/tag/v0.2.18>

## Still unknown

- No independent third-party check of the reported 90-111 tokens/s on RTX 5090 and 240 tokens/s on RTX PRO 6000 could be established from unredirected public benchmarks.
- Reddit and developer forum threads showed up in search snippets. They are left out of the citations because their exact unredirected URLs could not be verified.
- Chinese-language documentation and articles from Chinese portals could not be cited, because search redirects masked them. That leaves a gap in the evidence.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/Niko1221/Strata/releases/tag/v0.2.18 | Release Strata v0.2.18 · Niko1221/Strata | 2026-11-22 |

## Agent brief {#agent-brief}

- **Subject:** project:strata, thread strata-inference-engine, 1 dated events 2026-11-21 → 2026-11-21.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
