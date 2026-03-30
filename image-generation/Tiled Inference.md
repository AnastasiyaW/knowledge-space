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

```
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
```
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
