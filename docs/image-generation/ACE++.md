---
title: ACE++
category: models
tags: [image-editing, alibaba, flux, lcu, try-on, face-swap, inpainting, lora, non-commercial]
aliases: ["ACE Plus", "FuseAnyPart"]
---

# ACE++ (Alibaba / Tongyi Lab)

Unified multi-task image editing model built on [[FLUX Kontext|FLUX.1-Fill-dev]]. Supports try-on, face swap, inpainting, style transfer, super-resolution, logo placement — all through LoRA adapters or full fine-tune.

Paper: arXiv:2501.02487. GitHub: ali-vilab/ACE_plus.

## Architecture

### LCU++ (Long-context Condition Unit++)

Key change from original ACE: **channel concatenation** instead of sequence concatenation.

```
Original LCU:  [cond_image; mask] + [noise; mask]  → sequence concat (2× attention cost)
LCU++:         [cond_image; mask; noise]            → channel concat (efficient)
```

For N-ref tasks: multiple references concat along sequence, but each unit uses channel concat internally.

**FFT model specifics:**
- IN_CHANNELS: **448** (vs 384 for FLUX.1-Fill-dev) — 64 extra for edit image latent
- Same transformer: 3072 hidden, 24 heads, 19+38 blocks
- REDUX_DIM: 1152 for image embedding

## Model Variants

**3 LoRA models (recommended):**

| LoRA | Rank | Task |
|------|------|------|
| Portrait | 64 | Face/identity consistency |
| Subject | 16 | Object/logo/pattern |
| Local Editing | 16 | Mask-based region editing |

**1 FFT model** (fully fine-tuned): all tasks but less stable. Authors explicitly recommend LoRA over FFT.

## Training

Two-stage:
1. Pre-train on 0-ref tasks (T2I, inpainting) starting from FLUX.1-Fill-dev
2. Fine-tune on all tasks (0-ref + N-ref) from ACE dataset

## Critical Warning

> **Development on FLUX base is SUSPENDED.** Authors found "high degree of heterogeneity between training data and FLUX model" causing highly unstable training. Future ACE versions will use Alibaba's **Wan** foundation models instead.

## License

Inherits **FLUX.1-dev Non-Commercial License** — non-commercial only without BFL licensing.

## Gotchas

- FFT model quality **worse than LoRA models** — use LoRA variants
- FLUX.1-dev is guidance-distilled → negative prompts have uncertain effect
- Requires FLUX.1-Fill-dev as base (not plain FLUX.1-dev)
- No quantitative benchmarks published — qualitative results only

## Key Links

- GitHub: github.com/ali-vilab/ACE_plus
- HF: huggingface.co/ali-vilab/ACE_Plus
- Demo: huggingface.co/spaces/scepter-studio/ACE-Plus
