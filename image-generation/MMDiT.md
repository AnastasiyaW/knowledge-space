---
title: MMDiT (Multi-Modal Diffusion Transformer)
category: architectures
tags: [mmdit, transformer, diffusion, attention, architecture, dit, joint-attention]
aliases: ["Multi-Modal Diffusion Transformer", "MM-DiT"]
---

# MMDiT (Multi-Modal Diffusion Transformer)

Transformer architecture for diffusion models that processes multiple modalities (text, image) through **joint attention** in shared transformer blocks. Used in SD3, FLUX, [[Step1X-Edit]], and most modern diffusion models (2024-2026).

## Architecture

### vs Standard DiT

**DiT** (Peebles & Xie, 2023): text conditioning via cross-attention (separate Q from image, K/V from text). Text and image tokens live in different attention spaces.

**MMDiT**: text and image tokens concatenated into a single sequence, processed by the same self-attention layers. Both modalities attend to each other symmetrically.

```
DiT block:
  image_tokens → self_attn(Q=img, K=img, V=img) → cross_attn(Q=img, K=text, V=text) → FFN

MMDiT block:
  [image_tokens; text_tokens] → self_attn(Q=all, K=all, V=all) → split → img_FFN / txt_FFN
```

### Key Components per Block

| Component | Purpose | LoRA target? |
|-----------|---------|-------------|
| `to_q`, `to_k`, `to_v` | Image-stream QKV projections | Yes |
| `add_q_proj`, `add_k_proj`, `add_v_proj` | Text-stream QKV projections | Yes |
| `to_out.0` | Image attention output projection | Yes |
| `to_add_out` | Text attention output projection | Yes |
| `img_mlp` | Image-stream FFN (2 linear layers) | Yes |
| `txt_mlp` | Text-stream FFN (2 linear layers) | Yes |

Both streams share attention weights but have **separate FFN layers** — this lets the model learn modality-specific transformations while maintaining cross-modal attention.

### Attention Pattern

In joint attention, image tokens can attend to text tokens and vice versa. This creates bidirectional information flow:
- Text informs image generation ("make it red")
- Image informs text understanding (spatial context)

For editing models like [[Step1X-Edit]], this is critical: the model needs to understand BOTH what the image currently looks like AND what the text instruction asks to change.

## LoRA Application Pattern

For fine-tuning MMDiT (as demonstrated by [[PixelSmile]]):

```python
# Standard LoRA targets for MMDiT editing models
target_modules = [
    "to_q", "to_k", "to_v",           # image attention
    "add_q_proj", "add_k_proj", "add_v_proj",  # text attention
    "to_out.0", "to_add_out",          # output projections
    "img_mlp.net.0.proj", "img_mlp.net.2",     # image FFN
    "txt_mlp.net.0.proj", "txt_mlp.net.2",     # text FFN
]
# PixelSmile: rank=64, alpha=128, dropout=0 → 850 MB LoRA
```

Targeting all projections + both FFNs gives maximum expressivity. For lighter adaptation, attention-only (skip FFN) reduces LoRA size by ~40%.

## Models Using MMDiT

| Model | Variant | Notes |
|-------|---------|-------|
| Stable Diffusion 3 | Original MMDiT | First major adoption |
| FLUX.1 | Modified MMDiT | Adds RoPE, different conditioning |
| [[Step1X-Edit]] | MMDiT + Qwen VL encoder | Image editing |
| [[MACRO]] Bagel variant | MoT (Mixture of Transformers) | Multi-reference, related architecture |

## Performance Characteristics

- **Quadratic attention**: O(n^2) in total sequence length (image + text tokens). At 1024x1024 with VAE 8x downscale = 16384 image tokens + ~200 text tokens
- **Flash Attention**: critical for practical inference. Most implementations require flash-attn 2.x
- **Memory**: dominated by attention maps. Tiling/chunked attention helps for high-res

## Key Insight

MMDiT's joint attention is what makes instruction-following editing possible at high quality. Cross-attention (DiT-style) creates an information bottleneck — the model can only "ask" the text about specific queries. Joint attention lets the model freely mix both signals, discovering complex relationships between "what is" and "what should be."
