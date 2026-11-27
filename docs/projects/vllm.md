---
title: "Vllm: v0-29-0rc5 — V0 29 0Rc5"
category: "projects"
date: 2026-10-05
tags: ["project", "v0-29-0rc5", "vllm"]
aliases: ["Vllm: v0-29-0rc5"]
---

# Vllm: v0-29-0rc5 — V0 29 0Rc5

**Development line:** project:vllm · thread v0-29-0rc5  
**Last event:** 2026-10-05 · 10 dated since 2026-09-08 · **Researched:** 2026-11-25 · confidence: high

## What it is

vLLM is an open-source engine for teams serving language and multimodal models through Python or an OpenAI-compatible HTTP API.

- Offline batched inference and online serving.
- Continuous batching and paged KV-cache management.
- Speculative decoding and distributed deployment paths.

Model support, attention backends, and package installation vary by accelerator and release.

Use a pinned stable release for production, and validate upgrades against the exact model, driver, and serving configuration.

## Development line

- **2026-09-08 — vllm v0.29.0rc5 release.** Core changes set default prefix_cache_retention_interval to dense for Mamba, alongside other model improvements.
- **2026-09-08 — v0.29.0rc6 Release.** Release candidate v0.29.0rc6 of the vllm generative AI library fixes core hybrid models to apply dense prefix cache default.
- **2026-09-08 — other reporting on this date.**
  - The rc5 tag resolves to commit 7074c53, providing a fixed source identity for the Mamba prefix-cache-default change. (2026-09-08) — <https://github.com/vllm-project/vllm/releases/tag/v0.29.0rc5>
  - The rc6 tag resolves to commit 2cd1644, separating the hybrid-model dense-default repair from the preceding rc5 change. (2026-09-08) — <https://github.com/vllm-project/vllm/releases/tag/v0.29.0rc6>
- **2026-09-10 — vLLM v0.29.0 Release Notes.** v0.29.0 released with 594 commits from 277 contributors. Highlights include Model Runner V2 as default, new models (Hy4-preview, Tencent 770B/49B MoE, Qwen3.8-Flash-Next, GraniteSWA, NemotronH_Omni_Reasoning_V3, Kimi K3), speculative decoding metrics, RL weight sync with sharded_rdt P2P backend, Mamba prefix caching improvements, FlashInfer all-reduce enabled by default, and removal of ten deprecated model architectures.
  - The stable release records 594 commits from 277 contributors; Model Runner V2 became the default for all models, while Model Runner V1 remained for some ROCm models and unsupported features. (2026-09-10) — <https://github.com/vllm-project/vllm/releases/tag/v0.29.0>
- **2026-09-12 — vLLM v0.29.1rc0 Release with Dual-key Gumbel-max Watermarking.** Release candidate v0.29.1rc0 of the vLLM library adds dual-key Gumbel-max watermarking for speculative decoding.
  - The rc0 tag resolves to commit 74e48d9, fixing the exact code identity for the dual-key Gumbel-max watermarking candidate. (2026-09-12) — <https://github.com/vllm-project/vllm/releases/tag/v0.29.1rc0>
- **2026-09-17 — v0.30.0rc1: Isolate supplemental FlashInfer BF16 autotuning.** Release candidate v0.30.0rc1 includes a bugfix isolating supplemental FlashInfer BF16 autotuning (#57285), signed off by jiahanc and co-authored by OpenAI Codex.
  - The release title identifies the change as issue #57285 and confines it to supplemental FlashInfer BF16 autotuning. (2026-09-17) — <https://github.com/vllm-project/vllm/releases/tag/v0.30.0rc1>
- **2026-09-18 — vllm v0.30.0rc2 release.** Release candidate v0.30.0rc2 for the vllm project adds bugfixes and development updates.
  - The rc2 tag resolves to commit 4de8478, providing a fixed source identity for this pre-release step; the release page does not provide further user-facing detail. (2026-09-18) — <https://github.com/vllm-project/vllm/releases/tag/v0.30.0rc2>
- **2026-09-22 — vLLM v0.30.0 release highlights 762 commits from 315 contributors.** Release v0.30.0 introduces new models (DeepSeek-V4.1-Flash, DeepGEMM Mega-mHC, async Engram prefetch), Fast Start persistent weight-cache daemon, Gumbel-max watermarking, Model Runner V2 with MTP/EAGLE3 speculative decoding, HiSparse host-resident KV tier, and performance kernels for Qwen3.8-Flash-Next and Kimi K3.
  - The stable release records 762 commits from 315 contributors and identifies Fast Start as a per-GPU daemon that keeps post-quantized, tensor-parallel-sharded weights in GPU memory for CUDA-IPC remapping. (2026-09-22) — <https://github.com/vllm-project/vllm/releases/tag/v0.30.0>
- **2026-09-29 — v0.31.0rc1: [CI/Build] Skip the snapshot runtime on CUDA 12.x images (#59118).** Skip the snapshot runtime on CUDA 12.x images in the CI build pipeline.
  - The rc1 tag resolves to commit ee09ef4; the change is explicitly a CUDA 12.x image CI/build adjustment, not a serving-runtime behavior change. (2026-09-29) — <https://github.com/vllm-project/vllm/releases/tag/v0.31.0rc1>
- **2026-09-30 — vLLM v0.31.0rc2 Released.** vLLM published release candidate v0.31.0rc2, featuring a bugfix for Mamba to keep the prompt-end prefill checkpoint under sparse runtime conditions.
  - The rc2 tag resolves to commit 7a7283a and identifies the affected path as Mamba sparse-runtime handling of the prompt-end prefill checkpoint. (2026-09-30) — <https://github.com/vllm-project/vllm/releases/tag/v0.31.0rc2>
- **2026-10-05 — Vllm: v0-29-0rc5 update.** vLLM v0.31.0 became stable with 717 commits from 307 contributors; its highlights include DeepSeek-V4.1-Flash performance work and additional Mamba/cache-related execution changes.

## What changed

Model Runner V2 became the default. The line expanded model and speculative-decoding support, refined Mamba and prefix-cache behavior, added Gumbel-max watermarking, introduced persistent GPU weight caching and host-resident KV storage, and fixed CUDA-image builds and Mamba checkpoints.

## How to use this

1. Choose an accelerator-supported installation route and create an isolated Python environment before installing vLLM.
  — <https://docs.vllm.ai/en/latest/getting_started/quickstart/>
2. For offline work, load a supported model through the Python API and submit a batch of prompts.
  — <https://docs.vllm.ai/en/latest/getting_started/quickstart/>
3. For online work, launch the documented OpenAI-compatible server and use the matching client API endpoint.
  — <https://docs.vllm.ai/en/latest/getting_started/quickstart/>
4. Pin the release image or wheel for deployment instead of relying on an unversioned artifact.
  — <https://github.com/vllm-project/vllm/releases/tag/v0.30.0>

## Best practices

- Match the installation path to the target accelerator; vLLM documents separate paths for NVIDIA CUDA, AMD ROCm, Intel XPU, Apple Silicon, CPU, and plugins.
  — <https://docs.vllm.ai/en/latest/getting_started/installation/>
- Pre-download compiled kernels on newer NVIDIA GPUs when startup latency matters, because otherwise vLLM may download and compile them during startup.
  — <https://docs.vllm.ai/en/latest/getting_started/quickstart/>
- Treat runner, cache, and environment-variable changes as upgrade work: v0.30.0 removed previously deprecated environment variables and changed several serving interfaces.
  — <https://github.com/vllm-project/vllm/releases/tag/v0.30.0>

## Superseded by this

- v0.29.0 release candidates are superseded as a production baseline by v0.29.0 stable.
  — <https://github.com/vllm-project/vllm/releases/tag/v0.29.0>
- v0.30.0 release candidates are superseded as a production baseline by v0.30.0 stable.
  — <https://github.com/vllm-project/vllm/releases/tag/v0.30.0>
- The deprecated VLLM_PREFIX_CACHE_RETENTION_INTERVAL and VLLM_MM_HASHER_ALGORITHM environment variables were removed in v0.30.0.
  — <https://github.com/vllm-project/vllm/releases/tag/v0.30.0>
- v0.31.0 release candidates are superseded as a production baseline by v0.31.0 stable.
  — <https://github.com/vllm-project/vllm/releases/tag/v0.31.0>

## Still unknown

- The subject key is named for v0.29.0rc5, while the included sequence extends through v0.31.0rc2; the evidence supports treating it as one continuous vLLM release-development line.
- No qualified Simplified-Chinese release analysis or practitioner report for these exact core releases was found. English evidence was not substituted for the Chinese lane.
- No qualified community page was found that discussed one of these exact release steps with a dated practitioner assessment.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/vllm-project/vllm/releases/tag/v0.29.0rc5 | Release v0.29.0rc5 | 2026-11-25 |
| https://github.com/vllm-project/vllm/releases/tag/v0.29.0rc6 | Release v0.29.0rc6 | 2026-11-25 |
| https://github.com/vllm-project/vllm/releases/tag/v0.29.0 | Release v0.29.0 | 2026-11-25 |
| https://github.com/vllm-project/vllm/releases/tag/v0.29.1rc0 | Release v0.29.1rc0 | 2026-11-25 |
| https://github.com/vllm-project/vllm/releases/tag/v0.30.0rc1 | Release v0.30.0rc1: Isolate supplemental FlashInfer BF16 autotuning | 2026-11-25 |
| https://github.com/vllm-project/vllm/releases/tag/v0.30.0rc2 | Release v0.30.0rc2 | 2026-11-25 |
| https://github.com/vllm-project/vllm/releases/tag/v0.30.0 | Release v0.30.0 | 2026-11-25 |
| https://github.com/vllm-project/vllm/releases/tag/v0.31.0rc1 | Release v0.31.0rc1: Skip the snapshot runtime on CUDA 12.x images | 2026-11-25 |
| https://github.com/vllm-project/vllm/releases/tag/v0.31.0rc2 | Release v0.31.0rc2 | 2026-11-25 |
| https://github.com/vllm-project/vllm/releases/tag/v0.31.0 | Release v0.31.0 | 2026-11-25 |
| https://docs.vllm.ai/en/latest/getting_started/quickstart/ | Quickstart | 2026-11-25 |
| https://docs.vllm.ai/en/latest/getting_started/installation/ | Installation | 2026-11-25 |

## Agent brief {#agent-brief}

- **Subject:** project:vllm, thread v0-29-0rc5, 10 dated events 2026-09-08 → 2026-10-05.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
