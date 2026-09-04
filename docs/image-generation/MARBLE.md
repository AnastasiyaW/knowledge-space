---
title: "MARBLE: Material Recomposition and Blending"
description: "MARBLE performs material transfer, blending, and parametric material edits through CLIP-space controls over a pretrained image generator; validate object geometry, illumination, and artifact licenses for each workflow."
category: models
tags: [material-editing, clip-space, stability-ai, sdxl, ip-adapter, roughness, metallic, transparency, pbr]
aliases: ["Material Recomposition and Blending"]
---

# MARBLE: Material Recomposition and Blending

**Scope checked: 2026-09-04.** MARBLE is Stability AI's published material-editing method. It derives material representations in CLIP space and uses them to guide a pretrained text-to-image system for three related operations: exemplar material transfer, blending between material references, and parametric adjustment of selected material attributes.

## What It Can Express

The paper demonstrates control over properties such as roughness, metallic appearance, transparency, and glow. The public implementation provides:

- a material-blending notebook;
- a parametric-control notebook;
- a Gradio demo;
- a ComfyUI extension and example workflow.

The method's goal is visual material editing, not a physically calibrated PBR solver. A result that looks more metallic or transparent may still have inconsistent reflections, altered geometry, or implausible illumination. Treat the output as an image-generation result that needs task-specific review.

## Architecture and Dependency Boundary

MARBLE builds its material blocks from the InstantStyle codebase and uses a pretrained image generator plus associated image-conditioning artifacts. Keep the full chain explicit:

1. MARBLE repository revision and its dependency lock;
2. selected base generator, image encoder, adapter, and checkpoint revisions;
3. source object image and material reference(s), with permission to process them;
4. operation type — transfer, blend, or parametric control — and every control value;
5. output and acceptance receipt.

Do not assume that a control tuned for one base model, object category, or lighting setup will transfer to another. The upstream code's tested Python version and notebook settings are compatibility evidence for that release, not a stable API contract.

## Acceptance Checks for Product Images

For product or jewelry use, review separately:

| Requirement | Check |
|---|---|
| object identity and silhouette | overlay or side-by-side comparison with the original |
| material appearance | inspect highlights, roughness, transparency, and edge behavior under the intended crop |
| color and exposure | compare against calibrated source targets where available |
| edit scope | confirm background, branding, and unrelated regions did not change |
| publication rights | retain authorization for the object photo and material exemplar |

Use physically based rendering or measured color-management workflows when a material attribute must be numerically true rather than visually plausible.

## Licensing

MARBLE, InstantStyle, the selected base generator, adapters, and any example assets can have different licenses and access terms. Read the current terms for every artifact before hosted, commercial, or redistributed use; the presence of a public repository does not grant a blanket right to the complete assembled workflow.

## References

- [MARBLE official repository](https://github.com/Stability-AI/marble)
- [MARBLE paper](https://arxiv.org/abs/2506.05313)
- [MARBLE project page](https://marblecontrol.github.io/)
