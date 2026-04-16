---
title: FLUX.2 Klein 9B Architecture
category: reference
tags: [flux, klein, architecture, transformer, mmdit, qwen3, vae, rope, lora]
aliases: ["Klein Architecture", "FLUX2 Klein Architecture"]
---

# FLUX.2 Klein 9B Architecture

Deep reference for the FLUX.2 Klein 9B model internals: transformer structure, text encoding, VAE, and editing mechanism. Covers differences from FLUX.1 and implications for LoRA training.

## Model Variants

| Variant | Params | Text Encoder | License | Use Case |
|---------|--------|-------------|---------|----------|
| Klein Base 9B | 9B | Qwen3 8B | Non-Commercial | Training LoRAs, editing |
| Klein 4B | 4B | Qwen3 4B | Apache 2.0 | Commercial inference |
| Klein KV | 9B | Qwen3 8B | Non-Commercial | Reduced KV cache variant |
| Klein FP8 | 9B (quantized) | Qwen3 8B | Non-Commercial | Low-VRAM training |
| Klein nvfp4 | 9B (quantized) | Qwen3 8B | Non-Commercial | NVIDIA Blackwell inference |
| Klein Distilled | 9B | Qwen3 8B | Non-Commercial | Fast inference (4 steps) |

**Critical incompatibility**: 4B LoRAs cannot load on 9B and vice versa. Different hidden dims (4B uses smaller) and different text encoder shapes.

## Transformer Block Structure

Klein 9B uses a MMDiT-style architecture with two block types:

```
Input (noisy latent + reference images)
    ↓
8 × Double Blocks       ← process image+text jointly
    ↓
24 × Single Blocks      ← image-only refinement
    ↓
Output (denoised latent)
```

| Component | Value | Notes |
|-----------|-------|-------|
| hidden_dim | 4096 | vs FLUX.1's 3072 |
| double_blocks | 8 | joint image+text attention |
| single_blocks | 24 | image-only attention |
| rope_theta | 2000 | 3D RoPE for spatial+temporal |
| max_seq_len | 52000 | handles long reference sequences |

**FLUX.1 vs FLUX.2 comparison:**

| Aspect | FLUX.1 | FLUX.2 Klein |
|--------|--------|--------------|
| hidden_dim | 3072 | 4096 |
| double_blocks | varies by variant | 8 |
| single_blocks | varies | 24 |
| Text encoder | T5-XXL (4B) | Qwen3 8B |
| Edit mechanism | Separate Fill model | Unified (concat in sequence) |
| LoRA compatibility | Not compatible | Not compatible with FLUX.1 |

## Text Encoding (Qwen3 8B)

Klein uses Qwen3 8B as its sole text encoder (replacing T5 + CLIP in older FLUX):

```
Qwen3 8B (36 transformer layers)
Text → Hidden states at layers 9, 18, 27 → Concatenated
↓
Concatenated features → Projected → Cross-attention in double blocks
```

| Parameter | Value |
|-----------|-------|
| Encoder layers | 36 |
| Features extracted | Layers 9, 18, 27 (early/mid/late) |
| Hidden size | 4096 |
| Vocab | Qwen3 tokenizer |

The multi-layer extraction gives the model coarse semantic (early layers) + refined semantic (late layers) simultaneously.

## VAE

```
Image (3 channels, H×W)
↓ encode
Latent (32 channels, H/8 × W/8)
↓ patch packing (2×2 = 4× compression)
Token sequence (128 channels per patch)
```

| Aspect | Value |
|--------|-------|
| Latent channels | 32 |
| Spatial compression | 8× |
| Patch packing | 2×2 → 128 channels |
| Total compression | 32× (8× spatial × 4× patch) |

The 32-channel VAE (vs 4-channel in SDXL) enables richer latent representation but requires significantly more VRAM.

## Edit Mechanism (3D RoPE Time Offsets)

Klein's core editing innovation: reference images share the same sequence space as the output, differentiated only by temporal position encoding:

```
Sequence: [ref_image_1 | ref_image_2 | ... | output_tokens]
Time (t):      1/2           1/4              0
```

```python
# Simplified: reference tokens at t=0.5 (halfway through diffusion)
# Output tokens at t=0 (start of denoising)
# 3D RoPE encodes: (x_position, y_position, time)

rope_embed = RoPE3D(x=pos_x, y=pos_y, t=time_offset)
# ref_img1: t=0.5
# ref_img2: t=0.25 (if 2nd reference)
# output:   t=0.0
```

**Why this matters for training:**
- Training cost scales with reference count (each ref ~doubles sequence length)
- 1 reference: ~2.11× base training cost
- Multiple references: sequence fills `max_seq_len=52000` quickly
- `zero_cond_t`: parameter for ablating reference conditioning during training

### Training Cost Multipliers

| References | Approx. Cost Multiplier |
|-----------|------------------------|
| 0 (text-only) | 1.0× |
| 1 | ~2.11× |
| 2 | ~3.5× |
| 4+ | Approaches max_seq_len limit |

## LoRA Training Implications

**Where to target for different LoRA types:**

| LoRA Goal | Target Blocks | Rationale |
|-----------|--------------|-----------|
| Style only | double_transformer_blocks | Joint image+text attention = style |
| Structure/identity | single_transformer_blocks 0-12 | Early image-only = spatial structure |
| Full-quality | Both block types, all layers | 128/64/64/32 universal recipe |

**Why FLUX.1 adapters don't work on Klein:**
- hidden_dim 3072 (FLUX.1) vs 4096 (Klein): all weight shapes mismatch
- Different text encoder: T5 vs Qwen3
- Different attention heads and projection sizes

## Distilled vs Base

| Aspect | Base | Distilled |
|--------|------|-----------|
| Steps | 20-24 | 4 |
| CFG | 3.5-5.0 | 1.0 (CFG-free) |
| Training LoRA on | Required | Not recommended |
| Edit conditioning | Full | Simplified |
| Quality ceiling | Higher | Faster, lower ceiling |

Training LoRAs on distilled models: paired edit training breaks because distilled CFG-free inference path differs from training objective.

## Gotchas

- **FLUX.1 LoRAs are NOT compatible**: weight shapes differ (3072 vs 4096 hidden_dim). Loading a FLUX.1 LoRA on Klein will silently fail or produce corrupted output.
- **9B base required for training**: Klein-distilled lacks the full conditioning path needed for edit LoRA or character LoRA training. Always train on `flux-2-klein-base-9b.safetensors`.
- **32-channel VAE VRAM cost**: the richer VAE requires significantly more VRAM for encode/decode vs SDXL. Use `--cache_latents` to precompute and remove VAE from training GPU.
- **max_seq_len=52000 limit**: adding many reference images quickly exhausts the sequence limit, causing OOM. With 4+ references at 1024px, hit limit on sequences >50K tokens.

## See Also

- [[diffusion-lora-training]] - LoRA training recipes, hyperparameters, tool comparison
- [[flux-klein-9b-inference]] - inference settings (distilled vs base, CFG values)
- [[flux-klein-character-lora]] - character identity LoRA workflow
- [[lora-fine-tuning-for-editing-models]] - edit LoRA training with paired data
- [[flux-attention-manipulation]] - MMDiT attention mechanisms and regional control
