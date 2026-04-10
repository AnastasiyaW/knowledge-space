---
title: "Face Beautify Edit LoRA"
description: "Training before/after edit LoRAs on FLUX Klein 9B and Qwen-Image-Edit for facial correction - dataset strategies, PixelSmile degradation, SplitFlux training"
---

# Face Beautify Edit LoRA

Training an edit LoRA to fix facial issues (closed eyes, scrunched faces, unpleasant expressions) using before/after paired data on FLUX.2 Klein 9B.

## Approach: Before/After Edit LoRA

Paired files: `_start.png` (degraded face) + `_end.png` (good face) + caption instruction. Works with ai-toolkit, fal.ai API, SimpleTuner.

**Requirements:**
- 200-500+ quality pairs for solid results
- `content_or_style: content` (preserves identity)
- `flip_x: false` (faces are asymmetric - flipping creates artifacts)
- No trigger word needed for edit LoRAs

## Dataset Strategy - Synthetic Generation

Generate degraded "before" images from good "after" portraits using PixelSmile or inpainting.

### PixelSmile for Degradation

[[PixelSmile]] adds controllable expressions to face images via Qwen-Image-Edit-2511.

**ComfyUI workflow requirements:**

| Model | Size | Path |
|-------|------|------|
| Qwen-Image-Edit-2511 FP8 | 20 GB | `diffusion_models/qwen/` |
| Qwen 2.5 VL 7B FP8 | 8 GB | `text_encoders/` |
| Qwen VAE | 243 MB | `vae/` |
| PixelSmile LoRA | 811 MB | `loras/qwen-edit/` |
| Lightning 8-step LoRA | 811 MB | `loras/qwen-edit/` |

**Sampler settings:** `res_multistep`, 8 steps, cfg=1, shift=3.1

**Score parameter:** 1.0-1.5 for visible expression change. Score=0 produces no change. Formula: `V_neutral + score * (V_target - V_neutral)` (linear interpolation in embedding space).

**12 base expressions** with intensity control. Use sleepy/confused/sad/disgust to generate degraded "before" from good "after" portraits.

### Alternative: Inpainting Pipeline (No Training)

YOLOv8 face detect -> Florence2 mask -> Klein inpaint. Limitation: Klein "listens too well" to text prompts and may change the entire face identity rather than just fixing the expression.

### Data Sources

- FFHQ, CelebA-HQ (public face datasets)
- Curated portrait collections
- Batch degradation: 3 GPUs parallel via ComfyUI API, ~29 images/min

## Training Variants

| Variant | Rank | Target Layers | Rationale |
|---------|------|---------------|-----------|
| v1 baseline | 64 | all | Standard full coverage |
| v2 highrank | 128 | all | More capacity for eye detail |
| v3 splitflux | 128 | single-stream only | Freeze double_blocks, train single_blocks |

### SplitFlux Architecture Insight

FLUX/Klein uses double-stream blocks (joint image+text) and single-stream blocks (image detail/texture). Freezing double_blocks while training only single_blocks gave significantly better loss in testing:

- **SplitFlux loss**: 0.632
- **Baseline loss**: 1.225

This preserves composition understanding (double_blocks) while adapting texture/detail generation (single_blocks).

## Training Configuration

```yaml
# Key parameters from testing
optimizer: adamw8bit
learning_rate: 9e-5
dtype: bf16
caption_dropout_rate: 0.1    # 10% dropout for robustness
content_or_style: content    # preserves identity
ema: true                    # stabilizes edit quality
```

**EMA** (Exponential Moving Average) on LoRA weights is critical for edit quality stability. Enable in all configs.

## Gotchas

- **Qwen CLIP version matters**: PixelSmile requires `qwen_2.5_vl_7b_fp8_scaled.safetensors`, NOT `qwen_3_8b`. Dimension mismatch (3584 vs 12288) causes silent failures or crashes. The CLIP model must match the Qwen-Image-Edit-2511 architecture, not the Klein 9B architecture.
- **PixelSmile node path uses dash**: the custom node directory must be `qwen-edit/` (with dash), not `qwen_edit/` (with underscore). ComfyUI node resolution is case-sensitive on Linux.
- **Forward slashes in workflow JSON**: when sending workflows to Linux ComfyUI servers via API, all file paths must use `/` not `\`. Windows paths in JSON will fail silently or produce wrong model loads.

## See Also

- [[PixelSmile]] - expression control LoRA for Qwen-Image-Edit
- [[Diffusion LoRA Training]] - general LoRA training parameters
- [[LoRA Fine-Tuning for Editing Models]] - MMDiT-specific LoRA patterns
- [[face-detection-filtering-pipeline]] - dataset quality filtering tools
- [[anatomy-correction-diffusion]] - fixing anatomy mutations in generated images
