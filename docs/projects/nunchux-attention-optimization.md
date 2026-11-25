---
title: "Nunchux Attention Optimization: vc-attention-optimization — Vc Attention Optimization"
category: "projects"
date: 2026-09-17
tags: ["nunchux-attention-optimization", "project", "vc-attention-optimization"]
aliases: ["Nunchux Attention Optimization: vc-attention-optimization"]
---

# Nunchux Attention Optimization: vc-attention-optimization — Vc Attention Optimization

**Development line:** project:nunchux-attention-optimization · thread vc-attention-optimization  
**Last event:** 2026-09-17 · 2 dated since 2026-09-16 · **Researched:** 2026-11-25 · confidence: medium

## What it is

VC-Attention is a training-free low-bit attention kernel for diffusion-transformer video models, from Nunchux AI.

- V-Smooth cuts value-quantization error.
- ExpCast-FP8 removes the FP32 softmax bottleneck.
- Nunchux Attention is the company's proprietary extension.

## Development line

- **2026-09-16 — Nunchux Attention Optimization: vc-attention-optimization update.** Nunchux AI published its research blog post introducing VC-Attention, V-Smooth and ExpCast-FP8, along with the proprietary Nunchux Attention extension. (found in research)
- **2026-09-17 — VC-Attention accelerates video generation up to 1.7x.** VC-Attention reduces FP32 overhead and unnecessary operations in diffusion transformers without model re-training. Combined with V-Smooth and ExpCast-FP8, RTX 5090 achieves 3.58x attention speedup and 1.7x full generation speedup across Wan2.2, LongCat-Video, HunyuanVideo-1.5, and MiniMax-H3.
  - On MiniMax-H3 \(243 frames at 1344×768\), attention speedup over BF16 FlashAttention-4 is 1.59x for VC-Attention on B200 and 1.51x on B300. Attn-QAT gets 1.40x and 1.34x. The proprietary Nunchux Attention gets 1.91x and 1.83x. Across 100 prompts, VC-Attention reaches 20.2 dB mean PSNR against the BF16 reference, versus 19.9 dB for SageAttention2. About two thirds of each denoising step on a B200 with BF16 FlashAttention-4 is attention. V-Smooth groups value tokens with a lightweight k-means, subtracts each block's mean and quantizes only the residual. Across the four models in the report this adds 1.1 to 2.8 dB PSNR over SageAttention2. ExpCast-FP8 replaces the FP32 exponential and the E4M3 cast with one linear map that writes the FP8 probability code directly. (2026-09-16) — <https://www.nunchux.ai/blog/attention-is-the-video-bottleneck>

## What changed

Nunchux AI introduced VC-Attention as a faster and more faithful 8-bit attention than SageAttention2, with no model retraining. On the MiniMax-H3 workload it runs about 1.6x faster than BF16 FlashAttention-4 on a B200. The proprietary Nunchux Attention reaches 1.91x on B200 and 1.83x on B300. The announcement also reports a 3.58x attention speedup and a 1.7x full-generation speedup on an RTX 5090 for Wan2.2; the benchmark page excerpt does not show those RTX 5090 numbers.

## How to use this

1. Join the Nunchux AI waitlist to get access to the proprietary Nunchux Attention. Free access for MiniMax-H3 is said to be opening soon.
  — <https://www.nunchux.ai/waitlist>

## Best practices

- Run V-Smooth only on part of the denoising schedule. The B200 benchmark used it for the first quarter of the denoising steps and turned it off for the rest, and its speedup is time-weighted accordingly.
  — <https://www.nunchux.ai/blog/attention-is-the-video-bottleneck>
- Judge low-bit attention by fidelity to the BF16 reference \(PSNR, higher is closer\) as well as by speed, as the benchmark does against SageAttention2.
  — <https://www.nunchux.ai/blog/attention-is-the-video-bottleneck>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The retrieved blog text was truncated, so the RTX 5090 results \(3.58x attention, 1.7x full generation\) and the per-model results for Wan2.2, LongCat-Video and HunyuanVideo-1.5 could not be checked against it.
- The algorithm and kernel optimizations in the proprietary Nunchux Attention are not described in the retrieved text.
- No date is given for opening free MiniMax-H3 access, and the waitlist page shows only a sign-up form.

## Sources

| source | title | read |
|---|---|---|
| https://www.nunchux.ai/blog/attention-is-the-video-bottleneck | VC-Attention: Faster Low-Bit Attention Without Retraining - Nunchux AI | 2026-09-17 |
| https://www.nunchux.ai/waitlist | Sign up - Nunchux AI | 2026-09-17 |

## Agent brief {#agent-brief}

- **Subject:** project:nunchux-attention-optimization, thread vc-attention-optimization, 2 dated events 2026-09-16 → 2026-09-17.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.