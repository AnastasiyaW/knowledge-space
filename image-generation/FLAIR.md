---
title: FLAIR
category: models
tags: [image-restoration, flow-matching, variational, training-free, super-resolution, deblur, inpainting, sd3.5]
aliases: ["Flow-Based Latent Alignment for Image Restoration"]
---

# FLAIR (Flow-Based Latent Alignment for Image Restoration)

Training-free variational posterior sampling framework for image restoration. Uses SD 3.5 Medium as flow-matching prior. No training/fine-tuning needed — works out of the box for SR, inpainting, deblurring.

Paper: arXiv:2506.02680 (2025). Authors: ETH Zurich + Max Planck Institute.

## Architecture

**Not a new model** — a framework that wraps an existing flow-matching generative model:

```
Degraded image (y) → Forward model A → Variational posterior sampling:
    Prior: SD 3.5 Medium velocity field v(x_t, t)
    Likelihood: consistency with observed pixels
    → DTA + HDC + CRW mechanisms
    → Restored image (x)
```

### Three Mechanisms

1. **DTA (Deterministic Trajectory Adjustment):** Reparameterizes variational distribution to recover atypical modes that pure sampling would miss
2. **HDC (Hard Data Consistency):** Exact pixel-level consistency with observed (non-degraded) regions
3. **CRW (Calibrated Regularizer Weights):** Time-dependent weighting calibrated by offline accuracy estimates

### vs Diffusion-Based Restoration ([[RealRestorer]])

| Aspect | RealRestorer | FLAIR |
|--------|-------------|-------|
| Approach | Fine-tuned editing model | Training-free posterior sampling |
| Base model | Step1X-Edit (40 GB) | SD 3.5 Medium (2B) |
| Training | Requires fine-tuning | Zero training |
| Tasks | 9 degradation types (prompted) | SR, inpainting, deblur (mathematical) |
| Speed | 28 steps, fast | Full SD3.5 loop + optimization, slow |

## Tasks

- Super-resolution (tested up to 12× upscaling)
- Inpainting (with mask)
- Motion blur removal
- Text-guided editing (via prompt during inpainting)

## VRAM

**~24 GB** (RTX 4090). Inherits SD 3.5 Medium requirements.

## License

**Unclear** — no LICENSE file. SD 3.5 Medium uses Stability AI Community License (non-commercial or revenue < $1M).

## Key Links

- GitHub: github.com/prs-eth/FLAIR
- Demo: huggingface.co/spaces/prs-eth/FLAIR
