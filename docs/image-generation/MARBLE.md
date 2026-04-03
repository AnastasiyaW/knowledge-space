---
title: MARBLE
category: models
tags: [material-editing, clip-space, stability-ai, sdxl, ip-adapter, roughness, metallic, transparency, pbr]
aliases: ["Material Recomposition and Blending"]
---

# MARBLE (Material Recomposition and Blending in CLIP-Space)

Material property editing via CLIP embedding manipulation on SDXL. Controls roughness, metallic, transparency, glow independently with continuous intensity. Very relevant for jewelry/product photography.

Paper: CVPR 2025. Authors: Oxford + MIT CSAIL + Stability AI. arXiv:2506.05313.

## Architecture

Built on SDXL + IP-Adapter + InstantStyle:

```
Material exemplar → CLIP encoder (ViT-bigG-14) → CLS token embedding z_m
                                                        ↓
z_m injected into single UNet block: up_blocks.0.attentions.1 (material block)
                                                        ↓
Source image → grayscale init → SDXL denoising → output with new material
```

### Key Innovation: Single-Block Injection

InstantStyle identified `up_blocks.0.attentions.1` as responsible for style/material. MARBLE injects ONLY into this block (vs ZeST which injects into all blocks). Result: material changes while preserving geometry, shading, identity.

### Material Operations

**Transfer:** inject CLIP features from exemplar material
**Blending:** `alpha * z_m1 + (1-alpha) * z_m2` — smooth interpolation between materials
**Parametric control:** 2-layer MLP predicts CLIP-space direction offsets:
```python
z_edited = CLIP(material_image) + MLP(material_image, delta)
# delta controls intensity, multiple attributes can be summed
```

MLPs trained on synthetic data: 300 Objaverse objects rendered in Blender with PBR shaders. **As few as 16 training objects** suffice.

## Results

| Attribute | PSNR | LPIPS | CLIP Score |
|-----------|------|-------|------------|
| Roughness | 26.56 | 0.056 | 0.931 |
| Metallic | 26.82 | 0.053 | 0.928 |
| Transparency | 26.99 | 0.070 | 0.905 |
| Glow | 19.73 | 0.111 | 0.890 |

Glow is hardest to control. User study: 87.5% preferred over Concept Sliders.

## VRAM

~10-12 GB (SDXL + IP-Adapter). ComfyUI workflow provided.

## Relevance for Jewelry

- Metallic property control → standardize metal appearance
- Roughness → polish vs matte surfaces
- Transparency → gemstone appearance
- Works across styles (photos, renders) without fine-tuning
- Color-agnostic grayscale init preserves illumination geometry

## License

**Stability AI Community License** — non-commercial free; commercial <$1M with registration; >$1M requires enterprise.

## Key Links

- GitHub: github.com/Stability-AI/marble
- Demo: stabilityai-marble.hf.space
