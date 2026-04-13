---
title: FLUX Klein Jewelry Photography Pipeline
category: pipelines
tags: [jewelry, product-photography, klein, ic-light, delight, birefnet, compositing, pipeline]
---

# FLUX Klein Jewelry Photography Pipeline

Production pipeline for generating and compositing jewelry product photography using FLUX.2 Klein 9B. Covers cutout extraction, lighting manipulation, scene generation, and compositing.

## Full 7-Step Pipeline

```
1. Original jewelry photo (client)
2. BiRefNet cutout → transparent PNG
3. IC-Light V2 Delight LoRA → remove original lighting
4. Klein 9B scene generation → background scene
5. Manual composite in Photoshop/Figma → rough placement
6. Klein 9B inpaint + Consistency LoRA → seamless blend
7. IC-Light V2 → final relighting to match scene
```

## Step 1-2: BiRefNet Cutout

BiRefNet provides state-of-art transparent background extraction for jewelry. Handles thin chains, prongs, and edge detail better than older U^2Net.

```python
from transformers import AutoModelForImageSegmentation
import torch

model = AutoModelForImageSegmentation.from_pretrained("ZhengPeng7/BiRefNet", trust_remote_code=True)
model.eval()

# Returns RGBA with alpha = foreground mask
```

**Jewelry-specific challenges:**
- Thin chains: use highest resolution model variant
- Diamond prongs: edges are sub-pixel thin at normal viewing distance
- White gold on white background: pre-enhance contrast before segmentation

## Step 3: IC-Light V2 Delight

Remove existing lighting to get a diffuse/ambient-only version before recompositing.

**IC-Light V2 (ICLR 2025):**
- Flux-based relighting model (not SD 1.5 original)
- Uses 16-channel VAE for light-aware latents
- Non-commercial license (research and personal use only)
- VRAM: ~18 GB for full-quality inference

```python
from diffusers import FluxControlPipeline
from ic_light_v2 import ICLightV2Processor

# Delight mode: use fg-only model
pipe = FluxControlPipeline.from_pretrained("lllyasviel/ic-light-v2-fg")
delighted = pipe(
    prompt="product photo, neutral lighting",
    image=jewelry_cutout,
    num_inference_steps=20
).images[0]
```

**API alternative (production):**
```python
import fal_client
result = fal_client.run(
    "fal-ai/iclight-v2",
    arguments={
        "image_url": jewelry_cutout_url,
        "prompt": "product jewelry photo, uniform soft studio lighting",
        "lighting_preference": "neutral"
    }
)
```

## Step 4: Klein 9B Scene Generation

Generate background scene matching jewelry style and brand mood.

**Prompt structure for jewelry scenes:**
```
[Surface material] with [texture detail], [lighting type] from [direction],
[depth of field], [atmosphere], shot on [camera/film type]
```

**Example prompts by jewelry type:**
```
# Fine jewelry:
"dark velvet surface with subtle fabric texture, soft diffused studio lighting
 from above left, shallow depth of field with bokeh background, luxury editorial
 atmosphere, shot on medium format"

# Fashion/statement:
"rustic marble surface with grey veining, dramatic single-source rim lighting,
 deep black background gradient, high-contrast editorial, 35mm film grain"

# Bridal:
"white silk fabric draped softly, natural window light from right, cream tones,
 ethereal out-of-focus floral background, romantic editorial"
```

## Step 5-6: Compositing + Inpaint Blend

After rough Photoshop composite:

**Klein 9B inpainting settings for seamless blend:**
```
Model: FLUX.2 Klein 9B (base or distilled)
LoRA: Consistency LoRA (consistency-edit-lora)
Denoise: 0.5-0.7 (higher = more creative blend)
Mask: expanded 20-30px around jewelry edges
Prompt: describe the shadow and reflection that should appear
```

**Why Consistency LoRA**: maintains the jewelry's original appearance while harmonizing its integration with the generated scene. Without it, Klein sometimes "redesigns" the jewelry during the inpainting pass.

**VAE color shift warning**: FLUX Klein's VAE decoder sometimes shifts jewelry metal colors (gold → slightly greenish, silver → slightly blue). Correct in Photoshop after compositing: use Curves on affected channel, +5-10 on warm tones for gold.

## Step 7: IC-Light V2 Relighting

Remap lighting to match the scene's light source.

```python
# Use fg+bg model for relighting with scene background
pipe = FluxControlPipeline.from_pretrained("lllyasviel/ic-light-v2-fg-bg")
result = pipe(
    prompt="jewelry product photo with [scene lighting description]",
    fg_image=composited_jewelry,   # jewelry on background
    bg_image=background_scene,     # reference for light direction
    num_inference_steps=20
).images[0]
```

**Lighting prompts that work well:**
- "Soft window light from left, warm afternoon sun, slight shadows"
- "Studio three-point lighting, soft fill, cool-toned background light"
- "Candlelight from below, warm orange rim light, dark romantic"

## Jewelry-Specific Challenges

| Challenge | Solution |
|-----------|---------|
| Specular highlights (diamonds, metals) | IC-Light V2 handles naturally; don't over-inpaint over sparkle areas |
| VAE color shift on gold/silver | Correct via Curves after pipeline; +channel adjustment for metal tones |
| Thin chain detail loss | Use BiRefNet at 2048px+; don't downscale before cutout |
| Stone color accuracy | Include stone color in generation prompts; VAE tends to desaturate subtle gemstone colors |
| Shadow plausibility | Use real jewelry shadow reference; Klein 9B generates implausible shadows without guidance |

## Official FLUX.2 Klein LoRAs for Jewelry

| LoRA | Type | Use in Pipeline |
|------|------|----------------|
| IC-Light V2 Relight LoRA | Relighting | Step 7 relighting |
| IC-Light V2 Delight LoRA | Delighting | Step 3 original lighting removal |
| Consistency Edit LoRA | Style preservation | Step 6 seamless blend |
| Face Swap LoRA | Reference conditioning | N/A for jewelry |

These are BFL official LoRAs, not community-made. Load via standard ComfyUI LoRA loader.

## Dataset Considerations

For training a domain-specific jewelry generation LoRA:

| Dataset Size | Quality | Training |
|-------------|---------|---------|
| <10 images | Too small | LoRA fails to generalize |
| 15-30 images | Minimal viable | rank32, 1000 steps |
| 50-100 images | Sweet spot | rank32, 1500 steps |
| 100-200 images | Diminishing returns | rank32-64, 2000 steps |
| >500 images | Rarely helps | Potential content leakage |

**Caption strategy for jewelry**: trigger word + scene description + material description. NEVER include lighting or style descriptors (those go into LoRA weights).

## Comparison with SaaS Tools

| Tool | Quality | Speed | Cost | Custom Style |
|------|---------|-------|------|-------------|
| Klein 9B Pipeline | High | Slow (7 steps) | Self-hosted | Full control |
| Freepik/Magnific | High | Fast | $/image | Limited |
| Adobe Firefly | Medium | Fast | Subscription | Limited |
| Picsart AI | Medium | Fast | $/image | None |
| Canva AI | Low-medium | Fast | Subscription | None |

## Gotchas

- **IC-Light V2 is non-commercial**: the model weights are research-use only. For commercial product photography pipelines, use via fal.ai API which handles licensing.
- **BiRefNet requires minimum 512px input**: at lower resolutions, edge quality degrades significantly for thin jewelry elements. Upscale input if needed before running BiRefNet.
- **Klein 9B edit model vs generation model**: for Steps 4 and 6, use the BASE (non-distilled) Klein 9B. Distilled performs poorly for scene generation at the quality level needed for product photography.
- **Consistency LoRA scale**: the Consistency Edit LoRA is calibrated for scale 0.7-0.9. At 1.0, it over-constrains and prevents the model from adapting the jewelry to the scene.
- **Manual composite is not optional**: automated placement in Step 5 produces unnatural positioning 40-60% of the time. Human judgment for placement angle and position is still required.

## See Also

- [[FLUX Klein 9B Inference]] - Klein settings and LoRA stacking
- [[skin-retouch-pipeline]] - frequency separation for texture preservation
- [[object-removal-inpainting]] - background cleanup
- [[Tiled Inference]] - high-res output for product photography
- [[synthetic-dataset-pipeline]] - building training datasets for domain LoRAs
