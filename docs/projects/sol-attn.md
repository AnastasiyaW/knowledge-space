---
title: Sol-Attn
category: projects
date: 2026-08-03
tags: [project, sana, sol-attn, sol-attn-development]
aliases: ["Sol-Attn"]
---

# Sol-Attn

**Development line:** `project:sol-attn` · thread `sol-attn-development`  
**Last event:** 2026-08-03 · 1 dated since 2026-08-03 · **Researched:** 2026-09-05 · confidence: high

## What it is

Sol-Attn — NVIDIA’s inference-time block-sparse attention method for pretrained diffusion transformers.

- routes key/value blocks during online softmax rather than building a separate proxy map;
- computes selected blocks exactly and approximates skipped-block contribution;
- is used for visual-generation self-attention, while cross-attention can remain dense.

Limit: the published B200 implementation supports forward inference only and was evaluated on bidirectional diffusion visual generation, not autoregressive video. Verdict: use it as a model- and hardware-specific acceleration option, not as a drop-in guarantee of the published speedups.

## Development line

- **2026-08-03 — Sol-Attn project page and implementation branch referenced.** 3.95× is the whole stack, while adding Sol-Attn after kernel fusion changed the cumulative result from 1.394× to 1.534×. The model is MiniMax-H3, a 33B omni-modal video-and-audio generator.

## What changed

2026-07-27 — the Sol-Attn paper was posted, defining query-dependent threshold routing, single-pass online-softmax sparse computation, and proxy-score correction. 2026-07-28 — NVIDIA released Sol-Attn code with SM89, SM90, SM100, and SM120 kernels; the then-reported Sol-Engine end-to-end results included about 5.03× for HunyuanVideo-13B and 3.48× for Wan2.1-T2V-14B. 2026-08-03 — MiniMax-H3 support became a measured Sol-Engine recipe on eight GB200 GPUs: 3.95× is the whole stack, while adding Sol-Attn after kernel fusion changed the cumulative result from 1.394× to 1.534×. The model is MiniMax-H3, a 33B omni-modal video-and-audio generator. 2026-08-06 — MiniMax-H3 recipes expanded to DGX Spark and RTX 5090, with reported full-stack results of 3.92× and 4.52× respectively. 2026-08-13 — LTX-2.5 recipes added Sol-Attn across B200, RTX 5090, and DGX Spark; NVIDIA reported up to 4.68× for its multi-step pipeline and 1.90× for its distilled pipeline. 2026-08-17 — an optimized SM89 CuTe DSL Sol-Attn kernel was added for RTX 4090; NVIDIA reported 4.44× end-to-end for the complete MiniMax-H3 recipe. 2026-08-22 — MiniMax-H3 Super Acceleration combined a four-step H3 draft with three LTX-2.5 refinement steps; NVIDIA reported 22.2× for five-second 768p and 27.7× for ten-second video on one GB200.

## How to use this

From 2026-08-03, practitioners should treat Sol-Attn as a distinct Sana development line and consult the linked project page and `sol-engine` branch before evaluating or adopting it; its release status and technical claims require further verification.

1. Confirm the target self-attention is BF16 with head dimension 128 and that the intended runtime is CUDA; SGLang documents Sol-Attn as CUDA-only in its diffusion backend.
  — <https://github.com/sgl-project/sglang/blob/main/docs/docs/sglang-diffusion/attention_backends.mdx>
2. Install the upstream package from the NVlabs Sana `sol-engine` branch.
  — <https://github.com/sgl-project/sglang/blob/main/docs/docs/sglang-diffusion/attention_backends.mdx>
3. Select `sol_attn` explicitly and configure `tau`, dense warm-up steps and layers, exact prefix sinks where conditioning tokens require them, and `kv_splits=auto` for long sequences.
  — <https://github.com/sgl-project/sglang/blob/main/docs/docs/sglang-diffusion/attention_backends.mdx>
4. Run the exact target model, resolution, duration, prompt mix, and GPU against a dense baseline; compare output quality and end-to-end latency before adopting the configuration.
  — <https://nvlabs.github.io/Sana/Sol-Engine/H3-OnDevice/>

## Best practices

- Keep the first denoising steps and selected early layers dense; preserve text or audio prefix tokens as exact KV sinks when the model needs them.
  — <https://github.com/sgl-project/sglang/blob/main/docs/docs/sglang-diffusion/attention_backends.mdx>
- Increase `tau` cautiously: a higher threshold selects fewer exact KV blocks and increases approximation.
  — <https://github.com/sgl-project/sglang/blob/main/docs/docs/sglang-diffusion/attention_backends.mdx>
- Tune for the deployed model, hardware, resolution, duration, and acceleration stack; NVIDIA states that settings do not reliably transfer across combinations.
  — <https://nvlabs.github.io/Sana/Sol-Engine/H3-OnDevice/>

## Superseded by this

- 2026-08-03 — treating the reported 3.95× MiniMax-H3 result as Sol-Attn alone is obsolete: NVIDIA’s breakdown attributes 1.394× to kernel fusion/graph capture, 1.534× after adding Sol-Attn, and 3.95× only after cross-step caching.
- 2026-08-03 — assuming an acceleration recipe is quality-preserving merely because it is training-free is obsolete: NVIDIA’s super-efficient preset enables Sol-Attn for a further 1.25× but reports a larger perceptual distance than its quality-preserving preset.

## Still unknown

- The source event’s two links are undated current pages, so the exact content visible to readers on 2026-08-03 cannot be reconstructed from them alone. NVIDIA’s dated MiniMax-H3 page supplies the event-specific correction and scope.
- The current SGLang documentation describes its `sol_attn` integration as CUDA-only; it does not establish the hardware coverage of every direct or community integration of the upstream package.

## Sources

| source | title | read |
|---|---|---|
| https://nvlabs.github.io/Sana/Sol-Attn/ | Sol-Attn | On-the-Fly Attention Sparsification | 2026-09-05 |
| https://github.com/NVlabs/Sana/tree/sol-engine | NVlabs/Sana — sol-engine branch | 2026-09-05 |
| https://arxiv.org/abs/2607.24027 | Sol-Attn: Accelerating Video Generation Inference via On-the-Fly Attention Sparsification | 2026-09-05 |
| https://nvlabs.github.io/Sana/Sol-Engine/H3/ | Deploy MiniMax-H3 with Sol Engine achieving 3.95× acceleration in 4.5 hours of optimization | 2026-09-05 |
| https://nvlabs.github.io/Sana/Sol-Engine/H3-OnDevice/ | Deploy MiniMax-H3 on DGX Spark and RTX 5090 with Sol Engine: 4.52× Acceleration | 2026-09-05 |
| https://github.com/sgl-project/sglang/blob/main/docs/docs/sglang-diffusion/attention_backends.mdx | SGLang diffusion attention backends | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:sol-attn`, thread `sol-attn-development`, 1 dated events 2026-08-03 → 2026-08-03.
- **Practical note:** From 2026-08-03, practitioners should treat Sol-Attn as a distinct Sana development line and consult the linked project page and `sol-engine` branch before evaluating or adopting it; its release status and technical claims require further verification.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
