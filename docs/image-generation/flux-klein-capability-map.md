---
title: FLUX.2 Klein Capability Map
category: reference
tags: [flux, klein, lora, fal, api, endpoints, capability, operations]
aliases: ["Klein Operations Map", "Klein LoRA Catalog", "Klein fal.ai"]
---

# FLUX.2 Klein Capability Map

Reference for what FLUX.2 Klein 9B can do natively, via official LoRAs, via fal.ai LoRAs, and via community extensions. Updated April 2026.

## Model Variants Quick Reference

| Variant | VRAM | Steps | Use Case |
|---------|------|-------|----------|
| Klein Base 9B | ~28 GB | 20-30 | LoRA training, max quality |
| Klein Distilled 9B | ~24 GB | 4-8 | Production inference |
| Klein 9B KV | ~24 GB | 4-8 | Multi-reference (2.5× faster) |
| Klein 9B FP8 | ~18 GB | 4-8 | Reduced VRAM with good quality |
| Klein 9B nvfp4 | ~12 GB | 4-8 | Blackwell GPUs only |
| Klein 4B Distilled | ~16 GB | 4 | Commercial use (Apache 2.0) |
| Klein 4B Base | ~16 GB | 20 | Commercial fine-tuning |

**License**: Klein 9B = Non-Commercial. Klein 4B = Apache 2.0.

## Operations Map

| Operation | Native | Official LoRA | Community | Notes |
|-----------|--------|--------------|-----------|-------|
| Text-to-image | Yes | - | Style LoRAs | Core capability |
| Image editing | Yes (reference concat) | - | Character LoRAs | Architecture-level |
| Background removal | No | BFL Background Remove | - | LoRA required |
| Object removal | No | BFL Object Remove | LanPaint | |
| Object move | No | BFL Move LoRA | - | Qwen3-VL bbox detection |
| Relighting | No | BFL IC-Light V2 Relight | - | |
| Delighting | No | BFL Delight LoRA | - | Remove lighting artifacts |
| Face swap | No | BFL Face Swap | PuLID-Flux2 | |
| Virtual try-on | No | fal Virtual Try-On | - | Apparel focused |
| Outpainting | No | fal Outpaint LoRA | - | |
| Zoom / Unzoom | No | fal Zoom LoRA | - | Pan/zoom extension |
| Spritesheet | No | fal Spritesheet LoRA | - | Game asset generation |
| Anatomy correction | No | Community anatomy sliders | NAG node | |

## Official BFL LoRAs

Available from Black Forest Labs, non-commercial (same as base model):

| LoRA | Function | ComfyUI Scale |
|------|---------|--------------|
| Move LoRA | Relocate objects via colored bbox | 1.0 (quality) / 1.25 (fast) |
| IC-Light V2 Relight | Relighting with scene reference | 1.0 |
| Delight LoRA | Remove lighting → neutral diffuse | 1.0 |
| Face Swap LoRA | Identity-preserving face replacement | 0.8-1.0 |
| Consistency Edit LoRA | Preserve subject during editing | 0.7-0.9 |
| Background Remove LoRA | Image background removal | 1.0 |
| Object Remove LoRA | Erase specific objects | 1.0 |

## fal.ai Commercial LoRAs

Available via fal.ai API (commercial licensing):

| LoRA | fal.ai Endpoint | Notes |
|------|----------------|-------|
| Virtual Try-On | `fal-ai/virtual-try-on-flux` | Clothing; jewelry needs custom |
| Background Remove | `fal-ai/background-remove` | BiRefNet alternative |
| Object Remove | `fal-ai/object-remove-flux` | Mask-based erasure |
| Outpaint | `fal-ai/outpaint-flux` | Extend image edges |
| Zoom Out | `fal-ai/zoom-flux` | Zoom out from center |
| Spritesheet | `fal-ai/spritesheet-flux` | 2D game sprites |

### fal.ai API Usage

```python
import fal_client

# Text-to-image
result = fal_client.subscribe("fal-ai/flux-2/base", {
    "prompt": "...",
    "image_size": "landscape_4_3",
    "num_inference_steps": 4,  # distilled
    "guidance_scale": 1.0,
})

# Image editing (reference conditioning)
result = fal_client.subscribe("fal-ai/flux-2/edit", {
    "prompt": "change background to winter forest",
    "reference_image_url": "https://...",  # source image
    "num_inference_steps": 20,
})

# Move LoRA
result = fal_client.subscribe("fal-ai/flux-2-move", {
    "image_url": "https://...",  # image with colored bbox painted on
    "prompt": "Move the vase to the right side of the table",
    "lora_scale": 1.25,
    "num_inference_steps": 8,
})
```

## Community LoRA Categories

### Anatomy/Quality Control

| LoRA | Scale | Effect |
|------|-------|--------|
| klein_slider_anatomy v1.5 | 2-4 (NOT 0-1) | Fix limbs/body proportions |
| Flux2Klein-Enhancer | 1.0-2.0 | Boost text conditioning strength |
| Realistic Enhanced Details | 0.5-0.75 | Skin texture, fabric grain |
| Klein Detail Slider | -3 to +3 | Adjustable detail amount |

### Face/Portrait

| LoRA | Scale | Notes |
|------|-------|-------|
| Ultra Real V3 (KL_9B_V3) | 0.6 edit / 0.75 gen | Subtle skin without freckles |
| Lust Skin Klein | 0.5-0.7 | Pores, freckles, natural skin |
| Portrait Engine V2 | 1.0 | Photorealistic skin |
| Visceral | 0.5-0.7 | Pore detail |

### Style

Hundreds of community style LoRAs. Discovery via:
- CivitAI (Klein 9B filter)
- huggingface.co (search "flux2-klein")
- Standard loading: ComfyUI LoRA loader, strength 0.4-0.75

## Multi-LoRA Stacking Rules

```
Max concurrent LoRAs: 3 (practical limit before artifacts)
Total combined strength: <1.5-2.0
Stacking order: strongest-influence first

Example safe stack:
  Character LoRA: 0.6
  Anatomy Slider: 0.8 (effective, scale 2.0 not strength)
  Detail Enhancement: 0.5
  Total influence: moderate, compatible
```

## Inference Endpoints Comparison

| Service | Model | Latency | Cost | Notes |
|---------|-------|---------|------|-------|
| fal.ai | Klein 9B distilled | 2-8s | $/image | Production API |
| Replicate | Klein variants | 3-15s | $/second | Pay-as-go |
| Modal | Self-hosted | Variable | GPU cost | Serverless |
| RunPod | Self-hosted | Variable | GPU/hour | Full control |
| Local ComfyUI | Any variant | 5-60s | Hardware | No API costs |

## Gotchas

- **4B LoRAs incompatible with 9B**: different hidden dims, text encoders. Always verify model variant before loading LoRA.
- **Anatomy slider scale 2-4, NOT 0-1**: `klein_slider_anatomy v1.5` uses a wider scale range than typical LoRAs. Using standard 0-1 range produces no visible correction.
- **BFL LoRAs require base model for training**: if you need to fine-tune on top of an official LoRA effect, you must train on the base model — the LoRA itself is not a fine-tuneable checkpoint.
- **KV variant (9B-kv) for multi-reference only**: the KV cache variant provides 2.5× speedup specifically when conditioning on reference images. For standard text-to-image, there is no speedup.
- **fal.ai endpoint availability**: BFL periodically updates or renames endpoints. Check `fal.ai/models` for current endpoint IDs before hardcoding.

## See Also

- [[flux-klein-9b-architecture]] - block structure, Qwen3 encoder, 3D RoPE
- [[flux-klein-9b-inference]] - sampler settings, CFG values, multi-pass upscaling
- [[flux-klein-character-lora]] - character/identity LoRA training
- [[diffusion-lora-training]] - general LoRA training pipeline
- [[object-removal-inpainting]] - EraDiff, TurboFill, LanPaint
