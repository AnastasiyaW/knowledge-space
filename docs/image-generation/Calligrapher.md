---
title: "Calligrapher: Reference-Guided Text Image Customization"
description: "Calligrapher customizes text imagery from style references through FLUX.1-Fill-dev, SigLIP, masks, and project weights; treat typography accuracy and licensing as separate acceptance checks."
category: models
tags: [text-editing, typography, style-reference, flux-fill, siglip, self-distillation, multilingual]
aliases: ["Calligrapher"]
---

# Calligrapher: Reference-Guided Text Image Customization

**Scope checked: 2026-09-04.** Calligrapher is a diffusion-based project for generating or editing text imagery while transferring a visual style from a reference. Its documented modes include self-reference, cross-reference, and non-text-reference customization. It is useful for typography experiments and art-direction prototypes, but generated spelling, composition, and rights must be reviewed independently.

## What the Workflow Uses

The published setup combines:

- a permitted local copy of `FLUX.1-Fill-dev`;
- the SigLIP image encoder;
- Calligrapher project weights and test assets;
- an input image and an editable mask;
- a text instruction and a style reference where the task calls for one.

The repository offers a basic Gradio demo with a manually drawn mask and a version that accepts a custom inpainting mask. Mask placement and aspect ratio materially affect the result: the model fills the requested region and harmonizes it with the surrounding image rather than acting like a deterministic text renderer.

## Choose the Reference Mode Deliberately

| Mode | Intended use | Review focus |
|---|---|---|
| Self-reference | replace text while retaining style from the same image | source text region and local background preservation |
| Cross-reference | apply typography from a separate reference | style transfer without unintended content copying |
| Non-text reference | derive a typographic treatment from a visual reference | whether the style is recognizable and the text remains legible |
| Multilingual path | use the documented TextFLUX-assisted demo | language-specific glyph quality and spelling |

The multilingual demo is optional and uses a different base-model path. The project cautions that its quality can vary; do not reuse a positive English-language result as proof for another script or language.

## Resolution, Text, and Human Review

The authors train at 512 pixels and recommend 512 or 768 pixels as a practical balance. Very high resolutions can introduce spelling errors. Treat this as a starting point for a fixture, not a universal output requirement.

For a publishable asset, evaluate separately:

1. exact text and punctuation;
2. glyph order, language/script support, and legibility at delivery size;
3. fidelity to the requested style without copying protected content;
4. mask boundary, background, lighting, and visual artifacts;
5. the source, prompt, model revision, mask, and output needed to reproduce a review.

Use an ordinary typography/layout tool when the requirement is exact deterministic lettering. Diffusion output is best treated as an image candidate that may need correction or compositing.

## Access and Rights Boundary

The base FLUX model requires its own access and terms, while the Calligrapher project and any auxiliary weights have their own distributions. Check every current model card and license before commercial deployment, redistribution, or using a third party's visual reference. Availability of a demo does not grant permission to use all references or outputs for every purpose.

## References

- [Calligrapher official repository](https://github.com/EzioBy/Calligrapher)
- [Calligrapher paper](https://arxiv.org/abs/2506.24123)
- [Calligrapher weights and test assets](https://huggingface.co/Calligrapher2025/Calligrapher)
