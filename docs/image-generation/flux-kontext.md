---
title: FLUX Kontext
category: models
tags: [image-editing, flux, bfl, dit, flow-matching, sequence-concatenation, character-consistency, multi-turn, non-commercial-dev]
aliases: ["FLUX.1-Kontext-dev", "Kontext"]
---

# FLUX Kontext

Image editing model from Black Forest Labs (BFL). Extends FLUX.1 architecture with **sequence concatenation** for context image conditioning. Best-in-class for text editing, character consistency, and multi-turn editing.

Paper: arXiv:2506.15742 (June 2025).

## Architecture

Same 12B DiT as FLUX.1-dev:
- 19 double-stream blocks (separate image/text weights, joint attention)
- 38 single-stream blocks (fused FFN)
- Hidden: 3072, heads: 24, 16-channel latent VAE
- Text: CLIP (768d) + T5 (4096d)

### Key Innovation: Sequence Concatenation

Context images encoded by FLUX VAE → latent tokens **appended to target image tokens** in visual stream:
```text
Target tokens:  position (0, h, w)
Context image:  position (1, h, w)   ← "virtual timestep" via 3D RoPE
Context image 2: position (2, h, w)  ← architecturally supported, not yet released
```

**Channel concatenation was tested and performed worse.** Sequence concat preserves independent resolution/aspect ratio for input vs output.

When context is empty → falls back to pure text-to-image.

### vs [[Step1X-Edit]]

| Aspect | FLUX Kontext | Step1X-Edit / Qwen-Edit |
|--------|-------------|------------------------|
| Base | FLUX.1 12B DiT | Custom MMDiT |
| Text encoder | CLIP + T5 | Qwen 2.5 VL (vision-language) |
| Conditioning | Sequence concat (latent tokens) | Joint attention (image + text) |
| Mask support | No explicit mask (text-driven) | DiffSynth pipeline supports masks |
| Speed | 3-5s at 1024×1024 | Slower (~40 GB VRAM) |

## Variants

| Variant | Access | License |
|---------|--------|---------|
| Kontext [dev] | Open weights (HF) | **Non-commercial** (BFL dev license) |
| Kontext [pro] | API only | Commercial via BFL |
| Kontext [max] | API only | Commercial via BFL |

**Dev is I2I only** (no T2I). T2I only in pro/max.

## Training

- Starts from FLUX.1 T2I checkpoint
- Joint fine-tune on I2I + T2I with rectified flow loss
- Data: millions of relational pairs (not disclosed)
- FSDP2, Flash Attention 3, selective activation checkpointing

## VRAM

~24 GB minimum (transformer in bf16). Full pipeline ~32-40 GB. FP8/FP4 quantization available for 24 GB GPUs.

## Gotchas

- **Modifies entire image**, not just edited region. Use flux-kontext-diff-merge node for selective merging via LAB color space detection + Poisson blending
- Multi-turn editing degrades after ~6 iterations
- Dev model has distillation artifacts
- Non-commercial license for open weights — commercial requires BFL licensing
- [[ACE++]] development **suspended on FLUX base** due to training instability

## Key Links

- GitHub: github.com/black-forest-labs/flux
- HF: huggingface.co/black-forest-labs/FLUX.1-Kontext-dev
- Diff-merge: github.com/safzanpirani/flux-kontext-diff-merge
