---
title: Image Restoration Survey
category: techniques
tags: [restoration, denoising, deblurring, super-resolution, jpeg-artifacts, diffusion-based, swinir, nafnet, realrestorer]
aliases: ["Image Restoration", "Image Enhancement", "Denoising Survey"]
---

# Image Restoration - Approaches and Models

Overview of image restoration approaches: from classical to diffusion-based. Key insight: diffusion models bring generalization across degradation types but at higher compute cost.

## Classical / CNN-Based

### SwinIR (ICCV 2021)
- Swin Transformer blocks for image restoration
- Strong baseline for denoise, super-res, JPEG artifact removal
- Lightweight (~12M params), fast inference
- Limitation: task-specific training, one model per degradation

### NAFNet (ECCV 2022)
- "Nonlinear Activation Free Network" - removes GELU/Softmax
- SOTA on SIDD (40.30 dB PSNR) and GoPro deblurring
- Very efficient: ~67M params, simple architecture
- Uses SimpleGate + Simplified Channel Attention

### Restormer (CVPR 2022)
- Multi-scale Transformer for high-res restoration
- Transposed attention: key/value along channel dim (not spatial)
- Strong on real noise removal, motion deblur, defocus deblur

## Diffusion-Based

### [[RealRestorer]] (March 2026)
- 9 degradation types on [[Step1X-Edit]] backbone
- Prompt-driven: specify degradation type in text
- #1 open-source on RealIR-Bench (FS=0.146), close to GPT-Image-1.5
- ~34 GB VRAM, 28 steps
- Weights: non-commercial academic only

### Palette (Google, 2022)
- First diffusion model for image-to-image restoration
- Concatenates degraded image with noise as conditioning
- Showed diffusion can match/beat task-specific models

### IR-SDE (NeurIPS 2023)
- Treats restoration as SDE reverse process
- Mean-reverting SDE: starts from degraded image, not pure noise
- Better than starting from noise for restoration tasks

## Degradation Types

| Type | Classical SOTA | Diffusion SOTA |
|------|---------------|----------------|
| Gaussian noise | NAFNet (40.3 dB) | RealRestorer |
| Real noise (SIDD) | NAFNet / Restormer | RealRestorer |
| JPEG artifacts | SwinIR | RealRestorer |
| Motion blur | NAFNet / Restormer | RealRestorer |
| Low light | RetinexNet / SNR-Net | RealRestorer |
| Rain removal | MPRNet | RealRestorer |
| Haze removal | DehazeFormer | RealRestorer |
| Super-resolution | SwinIR / Real-ESRGAN | StableSR |
| Moire | DMCNN | RealRestorer |

## SANA-Denoiser Approach

Our approach: repurpose [[SANA]] 1.6B DiT as restoration model via [[Paired Training for Restoration]]:
- Channel concat conditioning (degraded latent + noise)
- [[DC-AE]] 32x compression keeps token count low
- Linear attention O(N) enables high-res processing
- [[Temporal Tiling]] for context-aware tile processing at 4K+

Advantages over RealRestorer:
- 10x fewer params (1.6B vs ~15B Step1X-Edit backbone)
- Linear attention vs quadratic (much faster at high-res)
- 32x VAE compression vs 8x (4x fewer tokens)

## Standard Benchmarks

| Benchmark | Images | Degradation | Notes |
|-----------|--------|-------------|-------|
| SIDD | 320 val patches | Real smartphone noise | Gold standard for denoising |
| DND | 50 images | Real camera noise | No GT, online submission |
| DIV2K | 100 val | Synthetic (for super-res) | 2K resolution |
| Urban100 | 100 | Synthetic | Repetitive structures |
| Set14 | 14 | Synthetic | Quick sanity check |
| RealIR-Bench | 464 | 9 real degradation types | RealRestorer benchmark |
