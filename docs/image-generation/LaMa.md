---
title: LaMa (Large Mask Inpainting)
category: models
tags: [inpainting, ffc, fourier, large-mask, samsung, feed-forward, resolution-robust, apache-2.0]
aliases: ["Large Mask Inpainting", "Big-LaMa"]
---

# LaMa (Large Mask Inpainting)

Feed-forward inpainting model using Fast Fourier Convolution (FFC) for image-wide receptive field from the first layer. Excels at filling large masks with coherent textures. Resolution-robust: trained at 256x256, infers up to ~2000x2000.

Paper: WACV 2022. Authors: Samsung AI Moscow / AIRI. arXiv:2109.07161.

## Architecture

U-Net-like fully-convolutional network:
```hcl
Input (4ch: masked_image + mask) → Encoder → 9-18 FFC Residual Blocks → Decoder → Output (3ch)
```

### Fast Fourier Convolution (FFC)

The key innovation. Each FFC block splits channels into two parallel branches:

```sql
Feature map
    ├─ Local branch (standard convolutions) → high-frequency local details
    └─ Global branch:
         → channel-wise Real FFT (spatial → frequency domain)
         → 1×1 conv in frequency domain
         → inverse Real FFT (frequency → spatial domain)
         → image-wide receptive field from layer 1
```

**Why this matters for inpainting:** standard CNNs need many layers to propagate information across large masked gaps. FFC's spectral branch covers the entire spatial extent in a single layer — information from opposite sides of the mask is immediately available.

## Variants

| Variant | Params | Size | Training Data |
|---------|--------|------|--------------|
| Big-LaMa | ~51M | ~410 MB | Places365-Challenge |
| Standard LaMa | ~27M | smaller | Places365-Standard |
| CelebA variant | ~27M | smaller | CelebA-HQ (faces) |

## Training

- Resolution: 256×256
- Masks: on-the-fly random polygonal chains + rectangles (deliberately large)
- Loss: adversarial (non-saturating) + feature matching + High Receptive Field perceptual loss (ResNet50-dilated)
- Discriminator: patch-level, "fake" labels only for mask-intersecting areas

## Performance

- **VRAM: 2-4 GB** at 512×512 — runs on consumer GPUs
- **Speed:** ~2s GPU (HD), ~25s CPU, 26-45ms mobile (Qualcomm NPU)
- **Resolution generalization:** trains 256px → infers to ~2000px without retraining (FFC property)
- 20% slower but **3-4x fewer params** than competing baselines

## Relation to Diffusion-Based Inpainting

LaMa is a **feed-forward** model (single pass, deterministic). Diffusion-based inpainting ([[flux-kontext]], [[Step1X-Edit]]) is iterative (20-50 steps) but better at semantic content (faces, complex objects). LaMa excels at textures and patterns.

**Practical combination:** use LaMa for fast background/texture inpainting, diffusion for semantic regions.

## License

**Apache 2.0** — fully commercial.

## Key Links

- GitHub: github.com/advimman/lama
- Widely adopted: IOPaint, cleanup.pictures, ComfyUI nodes
