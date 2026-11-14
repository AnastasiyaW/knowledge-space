---
title: "Kimi K2"
category: "projects"
date: 2026-10-24
tags: ["kimi", "kimi-k2-development", "kimi-k3-1-pro", "project"]
aliases: ["Kimi", "Kimi K2"]
---

# Kimi K2

**Development line:** project:kimi-k3-1-pro · thread kimi-k2-development  
**Last event:** 2026-10-24 · 5 dated since 2025-07-13 · **Researched:** 2026-10-25 · confidence: medium

## What it is

Kimi K3.1 Pro is a mixture-of-experts multimodal foundation model from Moonshot AI. It competes with Claude 3.5 Sonnet in long-context coding, 3D engine integration and agentic workflows.

- 1M-token context processing
- multi-step tool execution
- CAD and game-engine scripting
- financial research analysis

2.8 trillion parameters in total, 104 billion active per token.

Cyber-offensive data was removed from reinforcement learning to keep the model from creating exploits on its own. The model is for engineering and research teams that need large context and 3D tooling. It runs through web interfaces and API endpoints, and open weights are scheduled to follow.

## Development line

- **2025-07-13 — Kimi K2 public availability references.** On 2025-07-13, Kimi K2 had official links to the project, its source code, the model publisher, web chat and mobile access. Together these dated links support a public-availability milestone. The exact release wording and version details still have to be checked against the sources.
- **2026-10-24 — Kimi K3.1 Pro released with Highspeed variant and planned open weights.** Kimi K3.1 Pro was released on 2026-10-24. The announcement cites benchmark strength among Chinese models and performance near Opus 5.5. It supports the Unreal, Unity and Godot engines and Blender/CAD modeling. Pricing is $2 per million input tokens and $10 per million output tokens. A Highspeed version is 2-3 times faster at twice the price. Open weights are expected by 4 November.
- **2026-10-24 — Kimi K3.1 Pro released with planned open weights.** Kimi K3.1 Pro was released with claimed benchmark performance near Opus 5.5 among Chinese models. It supports Unreal, Unity, Godot, Blender and CAD workflows. Pricing is $2 per million input tokens and $10 per million output tokens. The Highspeed variant runs at 2-3x speed for 2x the price. Open weights are promised by 4 November.
- **2026-10-24 — Kimi K3.1 Pro released with expanded post-training and Highspeed variant.** As of 2026-10-24, Moonshot's Kimi K3.1 Pro was reported as a post-training refinement of Kimi K3. The architecture is the same, with substantially more RL across hundreds of domains. Context goes up to 1M tokens, with 2.8T total parameters (104B active). The Highspeed variant is claimed to be 2-3x faster. Open weights are promised by 2026-11-04. It is available in Kimi, Kimi Work, Kimi Code and via API.
- **2026-10-24 — Moonshot releases Kimi K3.1 Pro, a post-training refresh of Kimi K3.** As of 2026-10-24, Moonshot's Kimi K3.1 Pro is available in Kimi, Kimi Work, Kimi Code and via API. It keeps the Kimi K3 architecture, with expanded post-training and RL across hundreds of domains. Context goes up to 1M tokens. The Highspeed variant is reported as 2-3x faster. The model is listed at 2.8T total parameters with 104B active. Open weights are promised by 4 November.
- **2026-10-24 — other reporting on this date.**
  - The model is a mixture-of-experts network with 2.8T total parameters and 104B active per token. It is served through the kimi-k3.1-pro API endpoint. (2026-10-24) — <https://platform.kimi.ai/>
  - The context window is up to 1M tokens. Developers get it in Kimi Code and through direct API access. (2026-10-24) — <https://platform.kimi.ai/>
  - Post-training RL focused on long-horizon tool execution, 3D spatial geometry and financial research. The base pre-training weights were left intact. (2026-10-24) — <https://www.kimi.ai/>
  - Cyber-offensive exploit generation was deliberately filtered out during RL alignment. This happened before the public release and the scheduled open-weight handoff. (2026-10-24) — <https://www.kimi.ai/>

## What changed

Moonshot AI scaled post-training reinforcement learning across hundreds of specialized domains. The base weights were not changed. The update added:

- native procedural support for Unreal Engine, Unity, Godot and Blender
- context handling expanded to 1M tokens
- a Highspeed variant, two to three times faster at double the price
- a timeline for the open-weight release

## How to use this

1. Use the model interactively in the Kimi web application, Kimi Work or Kimi Code.
  — <https://www.kimi.ai/>
2. Call the kimi-k3.1-pro endpoint through the Moonshot Open Platform API for standard inference. It costs $2 input and $10 output per million tokens.
  — <https://platform.kimi.ai/>
3. Pick the Highspeed API variant when a workload needs two to three times faster generation. Token rates are doubled.
  — <https://platform.kimi.ai/>

## Best practices

- Load entire multi-file codebases and complex CAD/3D asset configurations into the 1M-token context in a single session.
  — <https://platform.kimi.ai/>
- Name the target engine and its script conventions when prompting for Unreal Engine, Unity, Godot or Three.js procedural generation.
  — <https://www.kimi.ai/>
- Send high-throughput, latency-critical interactive tasks to the Highspeed endpoint. Keep complex offline reasoning on the standard tier so inference costs stay under control.
  — <https://platform.kimi.ai/>

## Superseded by this

- Kimi models need separate external tools for 3D engine script generation and CAD geometry tasks.
  — <https://platform.kimi.ai/>
- Moonshot API models run only on a single standard latency tier, with no dedicated high-throughput option.
  — <https://platform.kimi.ai/>

## Still unknown

- Secondary English and Chinese tech press reports had no permanent direct page URLs, so no external benchmark can be cited.
- Independent practitioner feedback from developer forums did not turn up in search results. Real-world production error rates and community benchmarks are unverified.

## Sources

| source | title | read |
|---|---|---|
| https://platform.kimi.ai/ | Kimi Open Platform - Kimi K3.1 Pro Model and API | 2026-10-25 |
| https://www.kimi.ai/ | Kimi - Moonshot AI | 2026-10-25 |

## Agent brief {#agent-brief}

- **Subject:** project:kimi-k3-1-pro, thread kimi-k2-development, 5 dated events 2025-07-13 → 2026-10-24.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.

<!-- live-update:48c530b3929b7caad0f982b611a702371e81a829c55ff767ba02727667334723 -->
## 2026-11-13 — NVIDIA releases NVFP4 quantized weights for Moonshot AI Kimi K3.1 Pro

NVIDIA published Moonshot AI's Kimi K3.1 Pro in NVFP4 on Hugging Face. It is a multimodal mixture-of-experts model, packaged with NVIDIA Model Optimizer for serving in vLLM and TensorRT-LLM.

### Usage and practices

- Weights: download the quantized repository from Hugging Face with huggingface-cli. [Source](https://huggingface.co/nvidia/Kimi-K3.1-Pro-NVFP4)
- Engine: start a serving cluster on an engine that supports NVFP4, such as vLLM or TensorRT-LLM. [Source](https://huggingface.co/nvidia/Kimi-K3.1-Pro-NVFP4)
- Input: send text prompts together with high-resolution images, within the one-million token context window. [Source](https://huggingface.co/nvidia/Kimi-K3.1-Pro-NVFP4)
- Hardware: run it on multi-GPU nodes with high NVLink bandwidth, so they can carry active expert routing and a large distributed KV cache. [Source](https://huggingface.co/nvidia/Kimi-K3.1-Pro-NVFP4)
- Speed: turn on native 4-bit floating point tensor core acceleration in engines that support it, such as vLLM or TensorRT-LLM. This gets the most throughput out of modern NVIDIA architectures. [Source](https://huggingface.co/nvidia/Kimi-K3.1-Pro-NVFP4)

### Additional evidence

- 2026-11-13: NVIDIA published the NVFP4 build, nvidia/Kimi-K3.1-Pro-NVFP4, prepared with NVIDIA Model Optimizer. The model is Moonshot AI's multimodal MoE: 2.8T parameters, 104B active. The build compresses multi-terabyte MXFP4 shards into a format for vLLM and TensorRT-LLM on modern GPU clusters. [Source](https://huggingface.co/nvidia/Kimi-K3.1-Pro-NVFP4)

### Superseded guidance (retained for history)

- 2026-11-13: Without FP4 compression built for the hardware, serving the 3T-class Kimi K3.1 Pro needed multi-terabyte raw weight storage and prohibitive memory bandwidth. [Source](https://huggingface.co/nvidia/Kimi-K3.1-Pro-NVFP4)

### Limits and open questions

- Chinese tech news outlets covered Moonshot AI's earlier base model announcements, but the exact article URLs sat behind search redirects. They are left out of the sources, so no link here fails to resolve.
- Independent enterprise benchmarks of latency and memory footprint, native MXFP4 against NVFP4 under full 1M context load, are not yet in verified primary documentation.


<!-- Retained base: 2ad0de93905b418f27c881816721b53a60120d4b; article blob: 72dc82c72af6f0840e851f11abbb72a883fe88df -->
