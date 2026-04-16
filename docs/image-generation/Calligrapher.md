---
title: Calligrapher
category: models
tags: [text-editing, font-style, flux-fill, siglip, qformer, self-distillation, multilingual, non-commercial]
---

# Calligrapher (Freestyle Text Image Customization)

Text generation and editing on images with style reference. Built on [[flux-kontext|FLUX.1-Fill-dev]] + SigLIP style encoder. Takes font/style sample from image, generates new text in same style.

Paper: arXiv:2506.24123 (June 2025).

## Architecture

```sql
Style reference image → SigLIP (ViT, siglip-so400m-patch14-384)
                           → Qformer (learnable queries)
                           → Linear projection → K_E, V_E
                                                    ↓
Input image + mask → FLUX.1-Fill-dev denoising ← cross-attention:
                                         Q from denoiser, K/V from style encoder
                                                    ↓
                                         Output with styled text
```

**Style injection:** encoder output **replaces** K and V matrices in style attention module (not concatenation — replacement).

### Self-Distillation Training

No manual annotation needed:
1. LLM generates prompts with typographic style descriptors
2. Pretrained FLUX synthesizes stylized text images
3. Neural text detection locates text regions
4. Strategic cropping → style reference + transfer target
5. Model trains on self-generated pairs

## Modes

- **Self-reference:** change text content, preserve original style
- **Cross-reference:** apply style from different image
- **Non-text reference:** transfer from arbitrary images (fire, water, etc.)
- **Multilingual:** Chinese, Korean, Japanese via TextFLUX

## Results

FID: 38.09 vs 66-70 (baselines). OCR accuracy: 0.84 vs 0.45-0.81. 72% user preference.

## VRAM / Speed

~4s per image on A6000 at 10 steps. **Recommended resolution: 512px** (trained at this). 768px acceptable, higher → spelling errors.

## License

Inherits **FLUX.1-Fill-dev Non-Commercial License**. Outputs can be used commercially.

## Key Links

- GitHub: github.com/Calligrapher2025/Calligrapher
- HF: huggingface.co/Calligrapher2025/Calligrapher
