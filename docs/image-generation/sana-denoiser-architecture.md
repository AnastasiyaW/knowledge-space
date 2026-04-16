---
title: SANA-Denoiser Architecture
category: architectures
tags: [sana, denoiser, img2img, restoration, temporal-tiling, channel-concat, our-design]
aliases: ["SANA Denoiser", "happyin-denoiser"]
---

# SANA-Denoiser - Our Architecture Design

Repurposing [[SANA]] 1.6B DiT as an image restoration model. Combines efficient linear attention with [[paired-training-for-restoration]] and [[temporal-tiling]] via [[block-causal-linear-attention]].

## Why SANA for Restoration

| Property | SANA 1.6B | Step1X-Edit (RealRestorer) | FLUX-dev |
|----------|-----------|---------------------------|----------|
| Params | 1.6B | ~15B | 12B |
| Attention | Linear O(N) | Quadratic O(N^2) | Quadratic O(N^2) |
| VAE compression | 32x ([[DC-AE]]) | 8x | 8x |
| Tokens at 1024px | 1024 | 16384 | 4096 |
| Tokens at 4K | 16384 | 262144 (!) | 65536 |
| Speed (1024px) | 1.2s | ~15s | 23s |

SANA is 10x smaller, 4x fewer tokens, linear complexity. For restoration where we need high-res processing, this is decisive.

## Architecture Changes (Minimal)

### 1. Input Conditioning: Channel Concat

```toml
degraded → DC-AE.encode → condition_latents [B, 32, H, W]
target   → DC-AE.encode → latents           [B, 32, H, W]

x_t = (1-σ)*noise + σ*latents               [B, 32, H, W]
model_input = concat([x_t, condition_latents], dim=1)  [B, 64, H, W]

projection = Conv2d(64, 32, 1)               # 1x1 conv, ~1K params
# Identity init for noise channels, zero init for condition channels
# At step 0: model = pretrained T2I behavior
# Condition signal learned gradually during fine-tuning

model(projection(model_input), timestep, text_embeddings)
```

Total new parameters: **1,024** (32 x 32 x 1 x 1 conv kernel). Compare: ControlNet = ~800M.

### 2. Text Conditioning for Degradation Type

Prompt describes what to restore:
- "Remove gaussian noise, restore sharp details"
- "Remove JPEG compression artifacts"
- "Enhance this low-light image"
- "Clean and restore this image"

Leverages SANA's Gemma-2-2B text encoder for degradation-type understanding.

### 3. Temporal Tiling for High-Resolution

For images > training resolution (e.g., 4K product photos):

```sql
4096x4096 image
  ↓ split into overlapping 1024px tiles (raster scan)
  ↓ each tile: DC-AE encode → 32x32x32 latent
  ↓ denoise with Block Causal Linear Attention
  ↓    (running sum S, Z from previous tiles = global context)
  ↓ stitch latents with linear blending in overlap
  ↓ DC-AE decode full stitched latent
4096x4096 restored image
```

Memory: constant O(D^2) cache + one tile latent. Processes any resolution.

## Training Strategy

### Phase 1: LoRA (fast iteration)
- Rank 32, target: attn.to_q/k/v/out + input projection conv
- 512px, 10K steps, DIV2K + Flickr2K synthetic degradation
- Evaluate: does it learn to denoise at all?

### Phase 2: Full Fine-Tune (if LoRA insufficient)
- Unfreeze all transformer params + projection
- VAE stays frozen
- Gradient checkpointing for memory
- Curriculum: 512px → 1024px

### Phase 3: Temporal Tiling (inference-only first)
- No retraining needed - causal attention is native to linear attention
- Just implement the tile loop + S, Z accumulation
- If quality insufficient: fine-tune with multi-tile samples

## Dataset

Source: DIV2K (800) + Flickr2K (2650) = 3450 clean images
Degradation: 5-8 variants per image = **17K-28K pairs**

| Degradation | Params | Prompt |
|------------|--------|--------|
| Gaussian noise | σ=10,15,25,35,50 | "Remove gaussian noise sigma {σ}" |
| JPEG | q=15,25,40 | "Remove JPEG artifacts quality {q}" |
| Blur | k=3,5,7,9 | "Remove blur, restore sharpness" |
| Downscale | 2x,3x,4x | "Upscale and restore details" |
| Combined | 2-3 random | "Restore this degraded image" |

## Evaluation Targets

| Benchmark | Metric | Target | SOTA Reference |
|-----------|--------|--------|---------------|
| SIDD val | PSNR | > 38 dB | NAFNet: 40.3 |
| SIDD val | SSIM | > 0.95 | NAFNet: 0.96 |
| DIV2K (σ=25) | PSNR | > 30 dB | SwinIR: 30.9 |
| Urban100 (σ=25) | PSNR | > 29 dB | SwinIR: 29.5 |
| Temporal tiling | Seam PSNR | > 40 dB | MultiDiffusion baseline |

## Project Files

```python
happyin-research/
├── sana-fm/
│   ├── data/paired_dataset.py      ← paired loader
│   ├── data/degradation.py         ← degradation functions
│   ├── configs/img2img_denoise.yaml
│   └── train_flowmatching.py       ← modified compute_loss
├── sana-denoiser/
│   ├── prepare_dataset.py          ← DIV2K + Flickr2K + degradations
│   ├── train.py                    ← wrapper
│   ├── temporal_tiling.py          ← tile-as-sequence inference
│   └── eval/benchmark.py           ← vs SwinIR, NAFNet
```

## Risk Assessment

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| DC-AE 32x compression loses fine details | Medium | Compare DC-AE reconstruction vs 8x VAE on jewelry textures |
| Linear attention insufficient for restoration | Low | SANA matches quadratic models on generation; restoration is simpler |
| Temporal tiling adds latency | High | Acceptable: quality > speed for product photography |
| 1.6B too small for complex degradations | Medium | Scale to 4.8B if needed; depth-pruning from 4.8B as fallback |
