---
title: Tiled Inference for High-Resolution
category: techniques
tags: [tiled-inference, sahi, high-resolution, upscaling, stitching, gradient-continuity, overlap, production-photography]
---

# Tiled Inference for High-Resolution Processing

Techniques for processing images larger than model input size by splitting into overlapping tiles, processing individually, and stitching back. Critical for production photography where originals are 5000-15000px.

## Core Problem

Most models accept 512-1024px max. Production photography needs pixel-perfect results at 5000-15000px. Naive splitting → visible seams at tile boundaries, especially on:
- Smooth gradients (skin, sky, metal surfaces)
- Repeating patterns (textures, fabrics)
- Fine details crossing tile boundaries (jewelry edges, hair)

## SAHI (Slicing Aided Hyper Inference)

Standard tiled inference library for detection models (YOLO, etc.):
```python
from sahi.predict import get_sliced_prediction
result = get_sliced_prediction(image, model, slice_height=640, slice_width=640, overlap_height_ratio=0.2, overlap_width_ratio=0.2)
```
Docs: docs.ultralytics.com/guides/sahi-tiled-inference/

Works for **detection** (merges bounding boxes across tiles). For **generation/editing** tasks, stitching is more complex.

## Overlap-Based Stitching for Generation

From chat discussions (Vladimir's approach):

```bash
1. Take tiles with overlap (e.g., input 1000×1000, keep center 800×800)
2. For next tile, include edges from already-processed tiles as overlap
3. Model sees context from neighboring processed tiles
4. Crop to center, avoiding boundary artifacts
```

### Gradient-Aware Blending

For smooth gradients (jewelry metal surfaces):
- **Linear blend** in overlap zone: `output = alpha * tile_A + (1-alpha) * tile_B`
- **Poisson blending** at seams (laplacian-based, preserves gradients)
- **Latent-space stitching** (as in [[X-Dub]]): average latents at boundaries, then decode

## FLUX Kontext Diff-Merge Approach

flux-kontext-diff-merge detects changed regions in **LAB color space** and selectively merges only the diff back into original using Poisson blending. Applicable to tiled processing — process tile, merge only changed pixels.

## Known Issues (from team experience)

1. **Gradient discontinuity** — smooth backgrounds show tile boundaries after processing. Mitigation: larger overlap, gradient-aware blending
2. **Detail loss at boundaries** — fine elements (gemstone edges, chain links) crossing tiles get corrupted. Mitigation: tile grid aligned to segmentation masks, process objects wholly
3. **Color drift** — cumulative color shift across many tiles. Mitigation: per-tile color correction against reference (as in [[X-Dub]]'s sliding window)
4. **Segmentation across tiles** — models like SAM/ZIM eat max ~1200px per side; ideal edges need tiled segmentation with post-merge. Preliminary full-image seg at lower res → refine edges with high-res tiles

## Latent-Space Tiling (for diffusion models)

Alternative: tile in **latent space** (after VAE encode, before denoising):
```text
Full image → VAE encode → latent (H/8 × W/8 × C)
Tile latents → denoise each tile with overlap
Stitch latents → VAE decode full
```

Advantage: VAE decode of full stitched latent produces globally coherent output. This is how [[X-Dub]] handles long video.

## Solar Curves (Edge Visualization)

Non-standard technique from retouching: apply solar curve (tone inversion at midtones) to reveal subtle edges invisible at normal viewing. Can be used as auxiliary input for segmentation models to improve edge detection on white-on-white or low-contrast boundaries.

```python
# Solar curve: invert midtones to reveal hidden edges
# See solar-curves-saver.py, solar-1-effect.py, solar-2-effect.py (team scripts)
```

Discussed for: white jewelry on white background segmentation, metal edge detection, gradient quality verification after tiled processing.

## VRAM-Aware Tile Sizing

For low-VRAM GPUs, tile size must be calculated from available memory. See [[low-vram-inference-strategies]] for detailed adaptive tile selection.

Quick reference (FP16 U-Net restoration model, 20 MB weights):

| Tile Size | Total VRAM | Fits 2 GB GPU |
|-----------|------------|---------------|
| 128x128 | ~60 MB | Yes |
| 256x256 | ~140 MB | Yes |
| 512x512 | ~450 MB | Yes |
| 1024x1024 | ~1.6 GB | Tight |

**BatchNorm warning**: tiling with BatchNorm causes artifacts that overlap cannot fix (statistics computed per-tile, not per-image). Use LayerNorm/InstanceNorm, or train on tiles matching inference size.

## Global Context Conditioning

Standard tiling loses global context per-tile. Methods to inject scene-wide information:

### CMod (Channel-wise Modulation)

64-dimensional global context vector derived from the full image (downsampled or separately encoded). Injected at each tile via channel-wise multiplication in the feature space.

```python
# Global vector: encode downsampled image → 64d vector
global_ctx = encoder_small(image_resized)  # [B, 64]
# Inject per tile via FiLM-style modulation
for tile_features in tile_feature_list:
    scale, shift = proj_layer(global_ctx).chunk(2, dim=-1)
    tile_features = tile_features * (1 + scale) + shift
```

Advantage over cross-attention: 64d vector is extremely lightweight. Constant overhead regardless of image size.

### FiLM (Feature-wise Linear Modulation)

Learnable affine transform conditioned on global context at each normalization layer. More expressive than CMod, compatible with LayerNorm-based architectures.

### Bottleneck Attention (DehazeXL)

Tokenize full image at low resolution → encode to bottleneck → inject via cross-attention into each tile's processing. Tile attends to global semantic tokens while doing local processing.

```text
Full image (downsampled) → Tokenize → Encoder → [bottleneck tokens]
Each tile processing:
  Tile tokens (local) + bottleneck tokens (global) → cross-attention → tile output
```

### Taxonomy of Global Context Methods

| Method | Mechanism | Overhead | Best For |
|--------|-----------|---------|---------|
| CMod | 64d channel multiply | Minimal | Color/lighting consistency |
| FiLM | Affine at each norm layer | Low | Style consistency |
| Bottleneck attn (DehazeXL) | Cross-attn to global tokens | Medium | Semantic consistency |
| ConvGRU | Recurrent scanning | Medium | Sequential coherence |
| Mamba | State-space scanning | Medium | Long-range dependencies |
| Skip-residual (DemoFusion) | Add global image downsampled | Low | Structure consistency |

### Positional Encoding for Tiles

| Method | Global Awareness | Cost |
|--------|-----------------|------|
| None (no PosEnc) | Tile-local only | Zero |
| Learned tile position embedding | Knows grid position | Minimal |
| RoPE on full-image coords | Continuous position | Low |
| Spectral encoding of location | Frequency-based position | Low |

## 2025 Papers: Artifact Reduction

### STA (Sliding Tile Attention)

Tiles the attention computation itself (not just inference). 91% sparsity in attention mask, 3.53× speedup on long sequences. Applied to FLUX for high-res generation. Not inference-time only - built into the model's attention mechanism.

### FreeScale

Scale Fusion: separates self-attention into global (low-frequency structure) and local (high-frequency detail) branches. Local branch processes individual tiles, global branch processes downsampled full image. Merges at inference time without fine-tuning.

```python
# Conceptual:
global_attn = self_attention(downsample(full_image))  # structure
local_attn = self_attention(tile)  # detail
output = merge(global_attn, local_attn)
```

### ScaleDiff (NPA + LFM + SDEdit)

Three components:
- **NPA (Non-uniform Pixel Aggregation)**: weighted tile blending based on confidence scores instead of uniform averaging
- **LFM (Local Feature Matching)**: aligns features across tile boundaries before blending
- **SDEdit integration**: runs partial-noise SDEdit on boundary zones to smooth remaining artifacts

### APT (Adaptive Pattern Transfer)

Statistical matching at tile boundaries:
```python
# For each overlapping boundary region:
mu_left, sigma_left = target_region.mean(), target_region.std()
mu_right, sigma_right = neighbor_region.mean(), neighbor_region.std()
# Transfer statistics: align neighbor to match target's distribution
neighbor_normalized = (neighbor_region - mu_right) / sigma_right
neighbor_aligned = neighbor_normalized * sigma_left + mu_left
```

No learning required. Works as post-processing on any tiled output.

### AccDiffusion v2 (Patch-Content-Aware Prompting)

Generates per-tile prompts by querying a VLM about the tile content. Prevents object duplication: if left tile has "mountain", right tile prompt explicitly excludes "mountain" or specifies "continuation of mountain range."

```python
tile_caption = vlm_describe(tile_crop_from_low_res_guide)
unique_tile_prompt = base_prompt + " " + tile_caption
```

### SANA Compatibility Matrix

| Method | SANA Compatible | Notes |
|--------|----------------|-------|
| SyncDiffusion | No | UNet-based, incompatible |
| MultiDiffusion | Partial | Works but ignores linear attention structure |
| DemoFusion | No | UNet-specific skip connections |
| FreeScale | Yes | Architecture-agnostic |
| APT | Yes | Post-processing, model-agnostic |
| AccDiffusion v2 | Yes | Prompt-level, model-agnostic |
| DC-AE native tiling | Yes | `pipe.vae.enable_tiling(...)` |

## See Also

- [[low-vram-inference-strategies]] - adaptive tile sizing, memory management
- [[temporal-tiling]] - cross-tile context propagation
- [[diffusion-inference-acceleration]] - complementary acceleration techniques
- [[SANA]] - 32x compression reduces tiling need
