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

```php
[Prompt] -> Klein Base 9B, 1024x1024, 20 steps, CFG 5.0, euler/simple
         -> Upscale Latent 2x -> 2048x2048
         -> Klein Distilled 9B, 4-8 steps, CFG 1.0, euler/simple, denoise 0.4-0.6
         -> VAE Decode -> 2048x2048 output
```

### Fast Pipeline (Distilled Only)

```php
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

### LoRA Training Parameters (from 50+ runs)

| Parameter | Optimal Value | Notes |
|-----------|--------------|-------|
| Network dims | 128/64/64/32 | linear/linear_alpha/conv/conv_alpha, 4:2:1:1 ratio |
| Weight decay | 0.00001 | 1/10th default for balanced analog texture |
| Learning rate | DO NOT CHANGE | Even 0.005% deviation destroys the image on FLUX |
| Optimal steps | ~7,000 | 3K = too raw, beyond 7K = anatomical distortion |
| Trigger word | One per style | Define explicit trigger for each LoRA |

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

## Detail Enhancement LoRAs

Community-trained LoRAs specifically for increasing detail/realism in Klein 9B output.

### Tier 1: General Detail

| LoRA | Weight | Effect | Notes |
|------|--------|--------|-------|
| Realistic Enhanced Details | 0.5-0.75 | Skin texture, fabric, hair, material grain | Start at 0.65. CFG 3.5-5.0. 24GB VRAM |
| Klein Detail Slider | -10 to +10 | Adjustable detail amount via weight | Safe range -3 to +3, works in img2img |
| Elusarca's Detail Enhancer | 0.3-1.0 | Sharpness, color balance, microdetails | Trigger: "Enhance this image". 632 MB |
| Ultimate Upscaler Klein-9b | 0.5-0.8 | Removes soft edges, JPEG artifacts | Good for compression artifact removal |

### Tier 2: Skin-Specific

| LoRA | Weight | Focus |
|------|--------|-------|
| Ultra Real V3 (KL_9B_V3) | 0.6 (edit) / 0.75 (gen) | Subtle skin texture without freckles |
| Lust Skin Klein | 0.5-0.7 | Pores, irregular freckles, natural imperfections |
| Visceral | 0.5-0.7 | Pore detail, eliminates plastic look |
| Portrait Engine V2 | 1.0 (calibrated) | Photorealistic skin, decoupled from outfit |

### Stacking Strategy

For maximum detail: base realism LoRA (0.5-0.65) + detail slider (+2 to +5). For portraits: skin-specific (0.5-0.7) + general detail (0.4-0.5). Keep total combined influence moderate - artifacts appear when cumulative weight exceeds ~1.5.

## Latent Space Detail Manipulation

### Detail Daemon (ComfyUI-Detail-Daemon)

Modifies sigma schedule during sampling - keeps noise injection the same but lowers noise removal, effectively adding detail.

| Parameter | FLUX Range | Purpose |
|-----------|-----------|---------|
| detail_amount | 0.3-1.0+ | Main intensity. FLUX needs higher values than SDXL (<0.25) |
| start | 0.1-0.5 | When adjustment begins (0=first step) |
| end | 0.5-0.9 | When adjustment ends |
| bias | varies | Shifts peak adjustment location |
| exponent | 0-1 | Curve shape (0=linear, 1=smooth) |

Large features form early, fine details late. Set `start=0.3, end=0.8` to affect detail without breaking composition.

### ComfyUI-Latent-Modifiers (Fooocus Sharpness)

Single mega-node with chained techniques. Most useful combo for Klein detail: **Sharpness + Spectral Modulation**.

- **Sharpness**: Fooocus-based, sharpens noise mid-diffusion. Strength 2.0-4.0.
- **Spectral Modulation**: converts latent to frequencies, clamps high frequencies while boosting low ones. Fixes oversaturation from high CFG.
- **Divisive Norm**: pooling to reduce artifacts from sharpness. Add after Sharpness.
- **Tonemapping**: 6 methods (Reinhard, Arctan, Quantile, Gated, CFG-Mimic, Spatial-Norm) for clamping oversaturation.

### CFG Tuning for Detail

| CFG | Base 9B Effect | When to Use |
|-----|---------------|-------------|
| 3.5-4.5 | Sweet spot, natural detail | Default |
| 5.0 | Stronger prompt adherence, slightly more detail | When LoRA isn't applying enough |
| 6.0-7.0 | Oversaturation risk, use Spectral Modulation | Extreme prompt adherence |
| >7.0 | Quality degrades | Avoid |

Distilled model: CFG must be 1.0 - higher values break generation entirely.

## Tiled 4K+ Upscale Pipelines

### Klein + SeedVR2 (Proven Two-Stage)

```bash
Stage 1: Klein 9B img2img to 2048x2048
  Sampler: euler_ancestral_cfg++
  Scheduler: sgm_uniform (BasicScheduler)
  Denoise: 0.8 (range 0.75-0.85)
  eta: 1.0, s_noise: 1.0-1.2
  Prompt: add "8K, intricate details"

Stage 2: SeedVR2 tile upscale to 4096x4096
  Grid: 4x4 = 16 tiles (~256x256 each)
  Default SeedVR2 parameters
  Variants: 3B (realism), 7B Sharp (stylized)
```

### ControlNet Tile Upscale

For FLUX Klein, use `Flux.1-dev-Controlnet-Upscaler` as tile controlnet. ControlNet strength must stay below 0.7 - higher produces rough edge artifacts. Denoise 0.3-0.4. Tile size 1024x1024 (768x768 for low VRAM).

### Florence2 Smart Tiling

Auto-captions image before upscaling. Caption guides diffusion to respect context during tile processing. Reduces hallucinations at tile borders. Can reach 4K-8K (45MP).

## Prompt Engineering for Detail

### Structure (BFL Official)

**Subject -> Setting -> Details -> Lighting -> Atmosphere**. Natural language prose, NOT tag lists. Front-load important elements.

Lighting descriptions have the single greatest impact on output quality. Be specific: "soft, diffused natural light filtering through sheer curtains" >> "good lighting."

### Detail-Boosting Phrases

- "8K" + "intricate details" together: consistently produces strong results in upscale passes
- If too aggressive: remove "intricate details", keep only "8K"
- NEVER use the word "enhance" - model associates it with heavy AI upscaling artifacts
- Describe specific material properties: "silk with visible thread count", "leather with visible grain and patina"

### Prompt Length

| Length | Words | Use |
|--------|-------|-----|
| Short | 10-30 | Concept exploration |
| Medium | 30-80 | Production work |
| Long | 80-300+ | Complex editorial/product |

## Model Variants (Full Catalog)

| Variant | Size | VRAM | Speed | Notes |
|---------|------|------|-------|-------|
| FLUX.2-klein-4B (distilled) | 4B | ~16 GB | Fastest | 4-step, basic use |
| FLUX.2-klein-4B-base | 4B | ~16 GB | Fast | 20+ steps, better anatomy |
| FLUX.2-klein-9B (distilled) | 9B | ~24 GB | Fast | 4-8 steps, production default |
| FLUX.2-klein-base-9B | 9B | ~28 GB | Medium | 20-30 steps, LoRA training target |
| FLUX.2-klein-9B-kv | 9B | ~24 GB | **2.5× faster** | KV-cache for ref images |
| FLUX.2-klein-4B-fp8 | 4B | ~12 GB | Faster | fp8 quantized |
| FLUX.2-klein-9B-fp8 | 9B | ~18 GB | Faster | fp8 quantized, maintains grain |
| FLUX.2-klein-9B-nvfp4 | 9B | ~12 GB | Fastest | nvfp4 for Blackwell GPUs |

**KV variant (9B-kv):** caches key-value pairs for reference images during multi-image editing. 2.5× faster than vanilla 9B for reference-conditioned generation. Use when doing face swap, head swap, or reference-guided editing.

## Official BFL LoRAs

| LoRA | Function | Scale |
|------|---------|-------|
| Move LoRA | Relocate objects via bounding box conditioning | 1.0 (quality) / 1.25 (fast) |
| Relight LoRA (IC-Light V2) | Relighting with scene reference | 1.0 |
| Delight LoRA | Remove lighting → neutral diffuse | 1.0 |
| Face Swap LoRA | Identity-preserving face replacement | 0.8-1.0 |
| Consistency Edit LoRA | Maintain subject appearance during editing | 0.7-0.9 |

## Move LoRA: Visual Bounding Box Conditioning

Move objects by drawing red (source) and green (destination) rectangles directly on the image.

**How it works:**
1. Detection: Qwen3-VL-8B reads burned-in colored rectangles
2. Red rectangle = source location
3. Green rectangle = destination location
4. Klein 9B executes the move

```python
# Workflow in ComfyUI:
# 1. Load image
# 2. Draw red box around object to move (paint tool or overlay)
# 3. Draw green box at destination
# 4. Load Move LoRA at scale 1.25 (fast mode) or 1.0 (quality mode)
# 5. Generate

# Prompt template:
prompt = f"Move the {object_description} to {destination_description}"
```

**Two modes:**
- Fast mode: 8 steps, LoRA scale 1.25 - for quick iteration
- Quality mode: 30 steps, LoRA scale 1.0 - for final output

**Limitations:** complex scenes with overlapping objects. When multiple objects overlap, Qwen3-VL-8B sometimes misidentifies which object is in the red box. Add explicit object description to prompt.

## FLUX.1-Dev Adapter Incompatibility

ALL FLUX.1-dev adapters fail on Klein 9B due to dimension mismatch:

| Adapter | Error | Root Cause |
|---------|-------|-----------|
| Redux | dim mismatch | FLUX.1-dev hidden_dim=3072 |
| USO | dim 3072 vs 4096 | FLUX.1-dev only |
| IP-Adapter | Not trained | No Klein-native version exists |
| RES4LYF | dim mismatch | Redux-based |
| Realism LoRA (XLabs) | dim 3072 | FLUX.1-dev only |
| Shakker Add-Details LoRA | dim 3072 | FLUX.1-dev only |

**Klein 9B dimensions:** hidden_dim=4096, joint_attention_dim=12288. A Klein-native adapter would require training a SigLIP→MLP projector (~85M params) on 50K-200K style pairs from scratch.

## Gotchas

- **4B LoRA incompatible with 9B**: different text encoder sizes (Qwen 3-4B vs Qwen 3-8B). LoRAs are not interchangeable between Klein 4B and Klein 9B.
- **FP8 specifically benefits from 8 steps**: the FP8 quantized distilled model needs more steps than bf16 to match quality. Budget 8 steps minimum for FP8 inference.
- **Qwen-Image VAE artifacts**: the VAE decoder can introduce washed-out details and checkerboard noise. A dedicated fix LoRA exists (strength 1.0, trigger: "Remove compression artifacts. Restore the fine details of the photo."). Only works on Qwen-VAE artifacts - will degrade images from other VAEs.
- **Detail Daemon needs higher values on FLUX**: SDXL uses detail_amount <0.25, FLUX needs 0.3-1.0+. Using SDXL values produces no visible change.
- **"Enhance" in prompts causes artifacts**: Klein associates this word with aggressive AI upscaling look. Use "8K" and "intricate details" instead.
- **Steps above 50 degrade quality**: Klein Base 9B is designed for 25-50 steps. Going higher produces overcooked results. For more detail, use multi-pass or LoRAs, not more steps.
- **All FLUX.1-dev adapters incompatible with Klein 9B**: hidden_dim mismatch (3072 vs 4096). No IP-Adapter, Redux, or USO works on Klein. Check adapter's target architecture before downloading.

## See Also

- [[diffusion-inference-acceleration]] - Spectrum, Nunchaku quantization
- [[flow-matching]] - underlying generation framework
- [[MMDiT]] - transformer architecture used by FLUX
- [[tiled-inference]] - high-res output strategies
- [[diffusion-lora-training]] - training LoRAs for Klein
- [[lora-fine-tuning-for-editing-models]] - training custom edit LoRAs
