---
title: Object Removal and Inpainting Models
category: techniques
tags: [inpainting, object-removal, erasure, flux-fill, brushnet, lama, comfyui, klein]
---

# Object Removal and Inpainting Models

Comparative reference for object removal/erasure models (2024-2026). Covers specialized erasure models, general inpainting, and FLUX Klein 9B native approaches.

## Specialized Erasure Models

### EraDiff (SOTA Erasure, 2025)

Specifically trained for object erasure (not just inpainting). Handles complex backgrounds that confuse general inpainting models.

```python
# HuggingFace: SachinG/EraDiff
from diffusers import StableDiffusionInpaintPipeline
pipe = StableDiffusionInpaintPipeline.from_pretrained("SachinG/EraDiff")
result = pipe(
    prompt="",  # empty prompt = pure erasure
    image=image,
    mask_image=mask
).images[0]
```

**Key difference from general inpainting**: trained on pairs where the "before" has an object and "after" is the clean background, so it understands scene completion rather than content filling.

**Best for**: outdoor scenes, backgrounds with repeating patterns, product photography backgrounds.

### TurboFill (CVPR 2025, 4-Step Erasure)

4-step consistency model distilled from a larger erasure model. Production-grade speed.

```python
# 4 steps = ~5x faster than EraDiff at 20 steps
# Quality matches EraDiff at 20 steps on most objects
pipe = TurboFillPipeline.from_pretrained("turbofill/TurboFill-v1")
result = pipe(image=image, mask=mask, num_inference_steps=4).images[0]
```

**When to use**: batch processing, real-time preview, latency-sensitive pipelines. Trade-off: complex backgrounds or large objects may need more steps.

### LanPaint (Language-Guided Inpainting)

Uses natural language to guide what fills the masked region, without providing a reference image.

```python
prompt = "smooth leather sofa fabric matching the surrounding area"
result = lanpaint(image=image, mask=mask, prompt=prompt)
```

**Unique capability**: explicit semantic guidance for fills. Alternative to empty-prompt erasure when you want a specific replacement rather than background completion.

## General Inpainting Models

### Klein 4B Object Remove LoRA (CivitAI)

Dedicated LoRA trained for object removal on FLUX Klein 4B. Works as the model's conditioning pipeline with the LoRA guiding it toward erasure behavior.

```yaml
Model: FLUX Klein 4B
LoRA: "Object Remove LoRA" (CivitAI)
Prompt: "clean background, no objects" (or empty)
```

**Advantage over vanilla Klein**: much less hallucination of replacement content. Without the LoRA, Klein tends to invent new content.

### BrushNet (Tencent, 2024)

Dual-branch inpainting: one branch handles masked region, another preserves unmasked. Better boundary handling than single-branch models.

```python
from brushnet import BrushNetPipeline
pipe = BrushNetPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    brushnet_model_path="Tencent-Hunyuan/HunyuanDiT-BrushNet"
)
```

**Best for**: fine-grained boundary preservation. Superior to vanilla FLUX Fill when the mask boundary intersects complex detail (hair, foliage, jewelry chain).

### PowerPaint V2

Multi-task inpainting model (object removal, text-guided replacement, outpainting, shape-guided inpainting) unified in one model.

```python
# Select task type:
# "object-removal": background completion
# "context-replacement": fill with text description
# "shape-guided": use rough shape as guidance
# "outpainting": extend image boundaries
task = "object-removal"
```

**When to use**: when you need multiple inpainting modes in the same pipeline without switching models.

### Token Painter (AAAI 2026)

Attention token manipulation for inpainting. Directly modifies the cross-attention between mask tokens and text tokens, allowing finer semantic control than CFG-based approaches.

## LaMa for Background Completion

LaMa (Large Mask inpainting, ICCV 2021) remains the best option for pure background completion within 2 GB VRAM.

```python
from iopaint import run_model_inference
result = run_model_inference(
    model_name="lama",  # or "big-lama", "lama-dilated"
    image=image,
    mask=mask
)
```

**VRAM requirements:**

| Model | VRAM | Best for |
|-------|------|---------|
| LaMa | **2 GB** | Small/medium masks, solid backgrounds |
| Big-LaMa | 2-3 GB | Larger textures, better quality |
| LaMa-Dilated | 3 GB | Irregular masks |
| MAT (CVPR 2022) | 4-6 GB | Complex textures, large masks |

**Why LaMa fits 2 GB:** pure CNN (no diffusion), model weights ~50 MB, no KV cache. Ideal for skin blemish removal on low-VRAM setups.

## IOPaint: Swiss Army Knife

IOPaint (iopaint.com) unifies all major inpainting models under one API/CLI/UI:

```bash
# Install
pip install iopaint

# Run any model via CLI
iopaint run --model=lama --device=cpu --image ./input.png --mask ./mask.png --output ./out.png

# Supported models: lama, mat, fcf, cv2, migan, ldm, zits, paint_by_example,
#                   instruct_pix2pix, kandinsky, powerpaint, anytext, brushtnet
# FLUX/diffusion models require --device=cuda
```

**ComfyUI integration:** IOPaint nodes available via custom node manager.

## Comparison: When to Use What

| Scenario | Best Model | Notes |
|----------|-----------|-------|
| Remove object, seamless background | EraDiff | Trained for erasure specifically |
| Fast batch object removal | TurboFill (4 steps) | 5x faster, comparable quality |
| Replace with specific material/content | LanPaint or PowerPaint V2 | Language-guided fill |
| Fine boundaries (hair, jewelry) | BrushNet | Dual-branch boundary preservation |
| 2 GB VRAM constraint | LaMa | Only viable option at 2 GB |
| Klein 9B pipeline (maintain style) | Klein 4B Object Remove LoRA + Klein inpaint | Same model = no style mismatch |
| Any model, unified interface | IOPaint | Multi-model wrapper |

## ComfyUI Workflow

```php
[Load Image] + [Create Mask] -> [EraDiff/LaMa node] -> [Poisson Blend output]
                             -> For quality check: compare SSIM with original unmasked region
```

**Key nodes:**
- `ComfyUI-Impact-Pack`: auto-masking via YOLO detection
- `ComfyUI-Segment-Anything`: SAM-based mask creation
- `iopaint-comfyui`: IOPaint integration node (all models)
- `comfyui-brushnet`: BrushNet integration

## Frequency Separation Hybrid (for Skin)

For skin blemish removal specifically, frequency separation before inpainting outperforms direct inpainting:

```python
# 1. Separate high and low frequency components
low_freq = gaussian_blur(image, sigma=3)
high_freq = image - low_freq + 128  # texture/detail

# 2. Inpaint ONLY low_freq (no textures → LaMa handles it perfectly)
low_freq_fixed = lama_inpaint(low_freq, mask)

# 3. Recombine: original high_freq + fixed low_freq
result = high_freq + low_freq_fixed - 128
```

Why this works: LaMa inpaints solid color gradients nearly perfectly. High-frequency skin texture is preserved from surrounding non-masked areas. Net result: original pore structure survives.

## Gotchas

- **Empty prompt vs "background" prompt**: EraDiff and most erasure models perform best with empty `""` prompt. Adding "background" or "clean" sometimes triggers content generation rather than completion.
- **Klein 4B and 9B LoRAs are not interchangeable**: Object Remove LoRA for Klein 4B will NOT work on Klein 9B (different Qwen encoder dimensions). Verify model variant before downloading.
- **BrushNet mask dilation matters**: BrushNet requires 5-15px mask expansion around the object. Too small = artifacts at object edge visible in output. Use `cv2.dilate(mask, kernel_5px)`.
- **TurboFill at 4 steps fails on semi-transparent objects**: glass, smoke, shadows partially overlapping with background. Use EraDiff at 10-20 steps for these.
- **LaMa repeats patterns from training**: large masks on regular patterns (brick wall, tile floor) sometimes produce visible repetition artifacts. MAT handles these better.

## See Also

- [[skin-retouch-pipeline]] - full blemish detection + LaMa pipeline
- [[flux-klein-9b-inference]] - Klein inpainting settings
- [[anatomy-correction-diffusion]] - anatomy-specific inpainting patterns
- [[tiled-inference]] - large image inpainting via tiling
