---
title: Image Upscaler Evaluation
category: tools
tags: [upscaling, super-resolution, real-esrgan, hat, swinir, vae, comfyui, batch-processing]
---

# Image Upscaler Evaluation

Practical comparison of image upscalers for LoRA training data preparation and production pipelines. Key constraint: for training data, **fidelity > perceptual quality** - hallucinated detail = poisoned training samples.

## Regression-Based Upscalers (No Hallucinations)

These learn a direct LR-to-HR mapping without generative sampling. Cannot hallucinate by design.

| Model | Architecture | Scale | Speed (512px, H200 est.) | PSNR (Set14) | Best For |
|-------|-------------|-------|--------------------------|-------------|----------|
| **Real-ESRGAN x2plus** | RRDBNet (GAN) | 2x | ~0.08-0.15s | ~28-30 dB | Photos, JPEG artifacts, batch |
| SwinIR-L | Swin Transformer | 2x/4x | ~0.4-0.6s | ~30.9 dB | High quality, moderate speed |
| HAT-L | Hybrid Attention | 4x | ~1.5-2.0s | ~31.3 dB | Best PSNR, very slow |
| DAT2 | Dual Aggregation | 4x | ~1.5s | ~31.1 dB | Good PSNR/speed balance |
| **4xRealWebPhoto_v4** | DAT2-based | 4x | ~1.5s | N/A | Web-compressed JPEGs specifically |

### Real-ESRGAN x2plus (Recommended Default)

- **Model size**: ~67 MB
- **License**: BSD
- **ComfyUI**: native support, no custom nodes needed
- **Batch throughput**: 430K images at ~2.5 hours on H200 with batching
- **JPEG handling**: trained with degradation pipeline including JPEG compression
- **Why default**: zero hallucinations, handles artifacts, battle-tested at scale, tiny model

```python
from realesrgan import RealESRGANer
from basicsr.archs.rrdbnet_arch import RRDBNet

model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64,
                num_block=23, num_grow_ch=32, scale=2)
upsampler = RealESRGANer(
    scale=2,
    model_path='RealESRGAN_x2plus.pth',
    model=model,
    tile=0,        # no tiling for 512px
    half=True      # fp16
)
```

### 4xRealWebPhoto_v4_dat2

Specifically trained on web-downloaded, re-compressed images. Ideal for CDN-served content (Pinterest, social media) where images go through multiple JPEG compression cycles.

## Diffusion-Based Upscalers (Avoid for Training Data)

These models ADD detail that wasn't in the original - hallucination by design.

| Model | Hallucination | Why Avoid for Training |
|-------|---------------|----------------------|
| SUPIR | HIGH | Invents textures, skin details |
| StableSR | MEDIUM-HIGH | SD-based generative sampling |
| CCSR v2 | MEDIUM | Reduced but not zero |
| PiSA-SR | ADJUSTABLE | Dual LoRA: pixel (faithful) + semantic (hallucination). At `semantic_scale=0` becomes regression, but overhead of loading SD model |

### PiSA-SR Exception (CVPR 2025)

Uses dual LoRA on Stable Diffusion: pixel-level (l2-loss) + semantic-level (LPIPS + distillation). Guidance scales set independently. At `semantic_scale=0` it becomes pure regression - technically usable but Real-ESRGAN is simpler for this purpose.

## SDXS-1B VAE Upscaler

Asymmetric VAE (8x encoder / 16x decoder = built-in 2x upscale). 1.6B param UNet + 32-channel VAE (200MB).

**Not recommended for production use:**
- Alpha quality, development halted due to funding
- Trained on anime/illustrations (~90%), not photos
- `trust_remote_code=True` required - security risk
- No ComfyUI integration
- While technically "hallucination-free" (VAE encode/decode), latent space biased toward training domain

VAE reconstruction quality (37.83 PSNR) is close to FLUX.2 VAE (38.33) but this measures reconstruction, not super-resolution performance.

## Batch Processing Optimization

### Speed Tips

1. `torch.compile(model)` gives ~1.5-2x speedup
2. Always fp16 on modern GPUs
3. No tiling needed for 512px images
4. I/O is the bottleneck - use 4-8 data loading workers
5. Filter images already >= target resolution before processing

### Mixed Resolution Strategy

For datasets with 512-768px images:
- **<512px**: upscale 2x with Real-ESRGAN x2plus
- **512-767px**: upscale 2x, center-crop to target (or use as-is if training supports variable resolution)
- **768px+**: crop/resize to target, no upscaling needed

### ComfyUI Integration

Real-ESRGAN, 4xRealWebPhoto, HAT, SwinIR: download `.pth` to `ComfyUI/models/upscale_models/`, use "Load Upscale Model" + "Upscale Image (Using Model)" nodes. Works out of the box.

## Gotchas

- **JPEG artifacts amplify during upscaling** if the upscaler wasn't trained on compressed input. Real-ESRGAN handles this; SwinIR has a JPEG-specific variant (SwinIR-JPEG) for preprocessing.
- **Save upscaled images as PNG** for training data - re-compressing to JPEG after upscaling defeats the purpose and introduces new artifacts.
- **HAT-L is impractical at scale** - 430K images would take ~36 hours vs ~2.5 hours for Real-ESRGAN. Only justified for small high-value datasets.
- **"Hallucination-free" claims need scrutiny** - VAE encode/decode is technically deterministic but lossy compression introduces domain bias from training data.

## See Also

- [[FLUX Klein 9B Inference]] - tiled upscale pipelines with Klein
- [[Diffusion LoRA Training]] - dataset preparation for LoRA training
- [[Image Restoration Survey]] - broader restoration techniques
