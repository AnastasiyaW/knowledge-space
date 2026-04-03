---
title: ATI (Any Trajectory Instruction)
category: models
tags: [video-generation, trajectory-control, camera-motion, object-motion, wan2.1, bytedance, gaussian-injector, apache-2.0]
aliases: ["Any Trajectory Instruction"]
---

# ATI (Any Trajectory Instruction)

Trajectory-based motion control for I2V generation. Lightweight Gaussian motion injector module for pretrained video DiT. Controls camera and object motion with the same unified representation.

Paper: arXiv:2505.22944 (May 2025). Authors: ByteDance.

## Architecture

Adds a module **between preprocessing and patchify** of frozen I2V DiT:

```
Input image → VAE encode → latent L_I (H×W×C)
                                ↓
For each trajectory point: bilinear interpolation → C-dim feature vector
                                ↓
Gaussian distribution across frames:
  P = exp(-||position_t - (i,j)||^2 / 2σ)   σ=1/440
                                ↓
Soft spatial guidance signals → injected into latent space
                                ↓
Frozen Wan2.1-I2V-14B → generated video following trajectories
```

### Unified Representation

Camera motion = coordinated point trajectories (radial expansion=zoom, uniform translation=pan).
Object motion = point trajectories anchored to objects.
**Same mechanism for both.** No separate encoders per motion type.

## Training

- 2.4M video clips (filtered from 5M), TAP-Net tracked 120 points/frame
- 50K iterations on 64 GPUs (80GB each)
- 1-20 random points per video during training
- "Tail Dropout Regularizer" (p=0.2): randomly truncates trajectories to prevent occlusion hallucination

## Base Model

**Wan2.1-I2V-14B-480P** (primary). Also validated on Seaweed-7B (internal ByteDance). Model-agnostic injector.

## License

**Apache 2.0** — fully commercial.

## Gotchas

- Output 480P only
- Very rapid movements (half image width in 2 frames) → failure
- Requires full Wan2.1 14B model + ATI weights + VAE/T5/CLIP copied manually
- No confirmed Wan 2.2 support yet
- Trajectory editor = localhost only (security risk on remote)
- ComfyUI nodes available via Kijai (ComfyUI-WanVideoWrapper)

## Key Links

- GitHub: github.com/bytedance/ATI
- HF: huggingface.co/bytedance-research/ATI
- ComfyUI: docs.comfy.org/tutorials/video/wan/wan-ati
