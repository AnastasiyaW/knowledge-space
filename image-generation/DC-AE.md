---
title: DC-AE (Deep Compression Autoencoder)
category: architectures
tags: [vae, autoencoder, compression, 32x, sana, latent-space, dc-ae, efficient-vit, mit-han-lab]
aliases: ["DC-AE", "Deep Compression Autoencoder", "AE-F32C32"]
---

# DC-AE - Deep Compression Autoencoder

32x spatial compression autoencoder from MIT Han Lab, core component of [[SANA]]. Replaces standard 8x VAE (SD/FLUX) with 4x fewer tokens at any resolution.

## Configuration: AE-F32C32P1

- **F32** - 32x spatial downsampling (vs 8x in SD/FLUX)
- **C32** - 32 latent channels (vs 4 in SD)
- **P1** - patch size 1 (no patchification in DiT)

## Token Count Comparison

| Resolution | SD/FLUX (F8, P2) | SANA (F32, P1) | Reduction |
|-----------|------------------|----------------|-----------|
| 512x512 | 1024 | 256 (16x16) | 4x |
| 1024x1024 | 4096 | 1024 (32x32) | 4x |
| 2048x2048 | 16384 | 4096 (64x64) | 4x |
| 4096x4096 | 65536 | 16384 (128x128) | 4x |

## Reconstruction Quality (ImageNet)

| Metric | DC-AE F32C32 | SD VAE F8C4 |
|--------|-------------|-------------|
| rFID | 0.34 | 0.31 |
| PSNR | 29.29 | — |
| SSIM | 0.84 | — |
| LPIPS | 0.05 | — |

Near-identical to 8x VAE quality despite 4x more compression.

## Key Techniques

1. **Residual Autoencoding** - learns residuals on space-to-channel features, stabilizes training at high compression
2. **Decoupled High-Resolution Adaptation** - 3-phase training to avoid generalization penalty on high-res
3. **Tiling support** - `pipe.vae.enable_tiling(tile_sample_min_height=1024, tile_sample_min_width=1024)` enables 4K decode within 22GB VRAM

## Variants

- `dc-ae-f32c32-sana-1.0` - original
- `dc-ae-f32c32-sana-1.1` - improved reconstruction
- `dc-ae-lite-f32c32` - lighter, faster inference, smaller memory

## Impact on Diffusion

The 4x token reduction compounds with [[SANA]]'s linear attention O(N): fewer tokens AND linear complexity = orders of magnitude faster at high resolution. At 4K the combined effect makes generation feasible where quadratic attention models cannot run.

## Latent Space Properties

- Scaling factor and shift factor applied during encode/decode (see VAE config)
- `latents_mean` and `latents_std` normalization for stable training
- BF16 precision recommended for encode/decode

## Code

- GitHub: [mit-han-lab/efficientvit](https://github.com/mit-han-lab/efficientvit) (applications/dc_ae/)
- Diffusers PR: #10510, #10583 (tiling support)
- HuggingFace: `Efficient-Large-Model/dc-ae-f32c32-sana-1.1`
