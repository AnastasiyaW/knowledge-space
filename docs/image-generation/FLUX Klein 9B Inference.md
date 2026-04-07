---
title: FLUX Klein 9B Inference
category: models
tags: [flux, klein, 9b, inference, sampler, scheduler, lora-stacking, upscale, anatomy, prompting, comfyui]
aliases: ["Klein 9B", "FLUX.2 Klein", "Klein Distilled"]
---

# FLUX Klein 9B Inference

Practical reference for FLUX.2 Klein 9B image generation. Covers optimal sampler settings, multi-pass upscaling, LoRA stacking, anatomy fixes, and prompting patterns.

## Distilled 9B (4-Step Model)

### Recommended Settings

| Parameter | Value | Notes |
|-----------|-------|-------|
| Steps | **4** | Designed for 4-step inference |
| CFG | **1.0** | Official recommendation. Never exceed 2.0 |
| Sampler | **euler** | Most stable for edges and text sharpness |
| Scheduler | **simple** | Alternative: Flux2Scheduler (resolution-aware) |
| Denoise | **1.0** | For txt2img |

CFG above 2.0 produces "deep-fried" artifacts - the distilled model has guidance baked in. Using 50+ steps wastes compute and actively degrades quality.

### Anatomy Fix: Use 8 Steps

At 4 steps, complex poses (seated, two-person) often produce extra limbs. **8 steps** shows dramatic improvement for anatomy without excessive slowdown. Beyond 8 steps on distilled: diminishing returns.

## Base 9B (Non-Distilled)

### Recommended Settings

| Parameter | Value | Notes |
|-----------|-------|-------|
| Steps | **20-24** | Sweet spot. Below 15 loses detail. |
| CFG | **3.5-5.0** | 5.0 gives best prompt adherence |
| Sampler | **euler** | Most stable overall |
| Scheduler | **simple** | sgm_uniform for upscale passes |
| Denoise | **1.0** | For txt2img |

### Why Base Over Distilled

- Higher output diversity
- Configurable quality/speed tradeoff
- Better for LoRA training and custom pipelines
- Better input for downstream upscalers

## Sampler Deep-Dive

| Sampler | Scheduler | Use Case |
|---------|-----------|----------|
| euler | simple | Default gold standard |
| euler | Flux2Scheduler | Resolution-aware, adapts to aspect ratio |
| res_2s | simple | Better anatomy (2x compute/step) |
| res_2m | ddim_uniform | High quality general purpose |
| dpmpp_2m_ancestral | sgm_uniform | Analog grain, cinematic/film texture |
| euler_ancestral_cfg++ | sgm_uniform | Detail enhancement in upscale passes |

**Key insight**: `res_2s` at 4 steps equals `euler` at 8 steps in compute. Fixes anatomy without increasing step count explicitly.

## Multi-Pass Upscaling

### Base (Stage 1) + Distilled (Stage 2)

```
[Prompt] -> Klein Base 9B, 1024x1024, 20 steps, CFG 5.0, euler/simple
         -> Upscale Latent 2x -> 2048x2048
         -> Klein Distilled 9B, 4-8 steps, CFG 1.0, euler/simple, denoise 0.4-0.6
         -> VAE Decode -> 2048x2048 output
```

### Fast Pipeline (Distilled Only)

```
[Prompt] -> Klein Distilled 9B, 1024x1024, 8 steps, CFG 1.0, euler/simple
         -> Image Resize -> 2048 longest side
         -> Klein Distilled upscale, 4 steps, euler_ancestral_cfg++,
            sgm_uniform, denoise 0.8, s_noise 1.2
         -> 2048x2048 output
```

### Denoise Values for Second Pass

| Goal | Denoise | Effect |
|------|---------|--------|
| Tight fidelity | 0.3-0.4 | Structure lock, minimal change |
| Balanced | 0.5-0.6 | Good detail, some creativity |
| Creative upscale | 0.7-0.8 | More prompt-driven |
| Detail enhancement | 0.8 | Best for realistic fine detail |

### 4K+ Output

Add tiled upscale stage: 4x4 grid, 256px tiles with 128px overlap, seam_fix_denoise=1.0, seam_fix_width=32-128px. Florence2 auto-caption before upscale reduces hallucinations at tile borders.

### Seam Artifacts

Causes: tile boundary context loss, latent space discontinuity, high denoise in second pass.

Fixes: 128px overlap padding, mask blur 12-16px, half-tile reprocessing at boundaries, band-pass filtering (retain high-freq detail, blend low-freq).

## LoRA Stacking

### Capacity and Strength

Up to **3 LoRAs** simultaneously, each with individual weight (0-4).

| Strength | Effect |
|----------|--------|
| 0.0-0.3 | Subtle, barely visible |
| 0.4-0.75 | **Sweet spot** - balanced texture + coherence |
| 0.73 | Recommended default for single LoRA |
| 0.8-1.0 | Maximum texture, starts pulling apart |
| 1.0+ | Coherence loss, visible artifacts |

### Multi-LoRA Rules

- Stack strongest-influence LoRA first (processed sequentially)
- Total combined strength should stay under 1.5-2.0
- If artifacts appear, reduce weakest LoRA first
- Watch for style conflicts (two different color grading LoRAs)

### Klein vs Dev LoRA Behavior

Same LoRA settings produce fundamentally different results:
- **Klein**: heavier grain structure (16mm film look)
- **Dev**: cleaner, more like 35mm film
- **FP8 Klein**: maintains desirable grain; non-FP8 is cleaner

## Anatomy Problem Hierarchy

From most to least effective:

1. **Increase steps** (4 -> 8): strongest lever for complex poses
2. **Simplify pose**: standing > seated, single > multi-person, front > twisted
3. **Adjust CFG carefully**: 1.0 baseline, 1.2 can fix fused fingers, >1.5 risks new problems
4. **Use res_2s sampler**: doubles compute per step, fixes anatomy implicitly
5. **Negative prompting**: "distorted features, unnatural proportions, extra limbs"
6. **Use Base model**: 20 steps rarely has anatomy issues (much slower)

### Face Blur Fix

- Increase steps (most effective)
- Higher resolution (1536x1920 for portraits)
- Flux2Klein-Enhancer node to boost text conditioning magnitude

## Flux2Klein-Enhancer Node

Custom node for stronger prompt adherence:

| Parameter | Range | Default | Purpose |
|-----------|-------|---------|---------|
| Magnitude | 0.0-3.0 | 1.0 | Text embedding scaling |
| Contrast | -1.0-2.0 | 0.0 | Token difference amplification |
| Normalize Strength | 0.0-1.0 | 0.0 | Token magnitude equalization |
| Edit Weight | 0.0-3.0 | 1.0 | Preservation vs prompt following |
| Ref Strength | 0.0-5.0 | 1.0 | Reference structure lock (0=txt2img) |
| Blend with Noise | 0.0-1.0 | 0.0 | Reference-noise interpolation |

Dampening 1.20-1.30 recommended for precise preservation.

## Prompting Guide

### Structure

**Subject -> Setting -> Details -> Lighting -> Atmosphere**

Write as flowing prose, not keyword lists. Front-load important elements.

### Lighting (Highest Impact)

Specify: source type, quality, direction, temperature, surface interaction.
"Soft, diffused natural light filtering through sheer curtains" >> "good lighting"

### Prompt Length

| Length | Words | Use |
|--------|-------|-----|
| Short | 10-30 | Concept exploration |
| Medium | 30-80 | Production work |
| Long | 80-300+ | Complex editorial/product shots |

### Style Annotations (End of Prompt)

- "Style: Country chic meets luxury lifestyle editorial"
- "Shot on 35mm film with shallow depth of field"
- "Mood: Serene, romantic, grounded"

## Native Resolutions

Both 4B and 9B support 11 aspect ratios up to 4MP (2048x2048 square). Range from 1:1 to 21:9.

## Gotchas

- **4B LoRA incompatible with 9B**: different text encoder sizes (Qwen 3-4B vs Qwen 3-8B). LoRAs are not interchangeable between Klein 4B and Klein 9B.
- **FP8 specifically benefits from 8 steps**: the FP8 quantized distilled model needs more steps than bf16 to match quality. Budget 8 steps minimum for FP8 inference.
- **Qwen-Image VAE artifacts**: the VAE decoder can introduce washed-out details and checkerboard noise. A dedicated fix LoRA exists (strength 1.0, trigger: "Remove compression artifacts. Restore the fine details of the photo."). Only works on Qwen-VAE artifacts - will degrade images from other VAEs.

## See Also

- [[Diffusion Inference Acceleration]] - Spectrum, Nunchaku quantization
- [[Flow Matching]] - underlying generation framework
- [[MMDiT]] - transformer architecture used by FLUX
- [[Tiled Inference]] - high-res output strategies
- [[Diffusion LoRA Training]] - training LoRAs for Klein
