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

## Joint Attention Decomposition

The joint attention matrix decomposes into 4 quadrants:

| Quadrant | Direction | Function |
|----------|-----------|----------|
| **I2I** | Image-to-Image | Self-attention, preserves structure/geometry |
| **T2I** | Text-to-Image | Token-to-region alignment, PRIMARY for localization |
| **I2T** | Image-to-Text | Feedback to text representations |
| **T2T** | Text-to-Text | Near-identity, emphasizes boundary tokens |

To extract "cross-attention-like" signals from joint attention: slice out the T2I quadrant. ConceptAttention (ICML 2025) shows that output-space projections give sharper saliency maps than raw attention weights.

## Attention Manipulation Techniques

### Regional Prompting

**instantX Regional-Prompting-FLUX** (2411.02395): constructs attention masks controlling which image regions attend to which text prompts. Masks the T2I and I2T quadrants per region so each region only "sees" its own prompt. `base_ratio` controls base prompt influence. ComfyUI: `ComfyUI-FluxRegionAttention` (attashe).

**Stitch** (2509.26644, CVPR 2025): two-phase generation. Phase 1: LLM decomposes prompt into sub-prompts + bounding boxes, each object generated independently. Phase 2: objects extracted mid-generation and stitched. >200% improvement on FLUX GenEval Position task.

### Compositional Control

**Enhancing MMDiT** (2411.18301): closest equivalent to Attend-and-Excite for MMDiT. Test-time optimization at early steps with 3 loss functions: Block Alignment Loss, Text Encoder Alignment Loss, Overlap Loss. Addresses subject neglect/mixing with similar subjects.

**TACA** (2506.07986): temperature coefficient gamma > 1 on cross-modal Q-K interaction before softmax. Timestep-dependent: higher in early steps (layout), standard in later steps. Works with LoRA fine-tuning.

### Layer-Specific Roles

**FreeFlux** (2503.16153, ICCV 2025): discovered that positional vs content dependency does NOT correlate with layer depth. Categorizes edits into: position-dependent (object addition), content-similarity-dependent (non-rigid editing), region-preserved. Each type manipulates different layers.

**Unraveling MMDiT Blocks** (2601.02211): semantic info in earlier blocks, finer details in later blocks. Selectively enhancing text conditions per block improves T2I-CompBench++ from 56.9% to 63.0% on SD3.5 without quality loss - free boost.

### Semantic Editing

**FluxSpace** (2412.09611, CVPR 2025): leverages transformer block representations for disentangled editing. Training-free, no masks needed. Works on humans, animals, cars, complex scenes.

### Attention Visualization Tools

- **Aperture** (nathannlu/aperture): visualize FLUX attention maps across all 52 blocks
- **attention-map-diffusers** (wooyeolbaek): supports FLUX.1-dev, FLUX.1-schnell, SD3
- **ConceptAttention** (2502.04320, ICML 2025): repurposes DiT output projections for SOTA zero-shot segmentation

## Key Insight

MMDiT's joint attention is what makes instruction-following editing possible at high quality. Cross-attention (DiT-style) creates an information bottleneck - the model can only "ask" the text about specific queries. Joint attention lets the model freely mix both signals, discovering complex relationships between "what is" and "what should be."

## Gotchas

- **No attention-based anatomy fix exists** for FLUX/MMDiT. All current hand/body correction is post-generation (HandCraft, RHanDS). Research gap.
- **ComfyUI-FluxRegionAttention has memory leaks** - not optimized for production use. Monitor VRAM.
- **Traditional cross-attention tricks don't transfer directly** - Attend-and-Excite, prompt-to-prompt etc. assume separate cross-attention layers. Must be adapted for joint attention quadrant masking.

## See Also

- [[flux-klein-9b-inference]] - practical inference settings
- [[lora-fine-tuning-for-editing-models]] - LoRA targets for MMDiT
- [[in-context-segmentation]] - ConceptAttention for segmentation
