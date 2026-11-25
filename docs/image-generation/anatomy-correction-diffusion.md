---
title: "Anatomy Correction in Diffusion Models"
description: "Anatomy correction is a diagnose-mask-condition-inpaint workflow; use geometry-aware research methods and model-matched editing tools, then visually verify every edited hand or limb against the source."
category: workflows
tags: [anatomy, hands, inpainting, diffusion, image-editing, quality-control, comfyui]
aliases: ["Hand correction", "Diffusion anatomy repair"]
---

# Anatomy Correction in Diffusion Models

**Scope checked: 2026-09-04.** Anatomy correction is a local image-editing workflow for malformed hands, fingers, faces, or limbs. It is not a universal sampler preset and no detector, LoRA, or inpainting model can certify a generated anatomy as correct by itself.

## The Correction Loop

1. **Inspect the source at delivery size.** Identify exactly what is wrong: count, joint topology, occlusion, pose, silhouette, or a rendering artefact.
2. **Choose the smallest safe edit region.** Include the damaged anatomy and a narrow transition area; preserve untouched pixels and retain the original file.
3. **Provide structure when possible.** A hand mesh, pose, depth estimate, or carefully reviewed reference can constrain the correction more reliably than a generic positive prompt.
4. **Use a model-matched edit or inpainting workflow.** The checkpoint, text encoder, VAE, conditioning format, and node version must be compatible as a set.
5. **Review the result manually.** Check finger count, joints, contact with objects, perspective, skin/material continuity, shadows, and the edge of the edited region.
6. **Regenerate rather than repeatedly patching** when the error is global, the intended pose is ambiguous, or the local edit changes identity or geometry outside the target region.

## Structure-Aware Research Directions

HandRefiner and HandCraft are useful references for the principle behind a robust local repair: derive a hand structure, turn it into conditioning such as depth or masks, and use diffusion-based inpainting to integrate the corrected region. Their reported results apply to their declared research setups; they do not establish a drop-in compatible node for every current diffusion model.

The practical implication is simple: a geometry signal can make an edit more constrained, but it must be checked for alignment with the original image before it is used as conditioning.

## Current ComfyUI and Model Boundary

ComfyUI currently documents separate FLUX.2 [klein] base and distilled workflows for its supported model variants. Follow the official workflow and model locations for the exact 4B or 9B variant selected. Do not assume that a node, control model, LoRA, text encoder, or VAE built for FLUX.1, SDXL, or another release will be compatible with a FLUX.2 [klein] workflow.

Community nodes and third-party anatomy LoRAs can be useful experiments, but each needs a pinned source revision, its own license review, and a project-specific visual test. This page deliberately does not prescribe unverified community weights or universal numeric settings.

## Quality Gate

| Check | What must be observed |
|---|---|
| Anatomy | plausible count, joints, proportions, and pose |
| Interaction | fingers, tools, clothing, and other objects make physical contact correctly |
| Preservation | identity, typography, logos, jewellery, and non-target geometry remain unchanged |
| Compositing | lighting, shadow direction, texture, and edge transition match the source |
| Reproducibility | source digest, mask/conditioning, model revision, settings, output digest, and reviewer decision |

A detector score can help triage a batch, but it is not a pass condition. Any asset with person identity, product facts, medical relevance, or evidentiary value needs a human review before publication.

## Terms and Data

Code, models, adapters, mesh or pose estimators, input images, and generated outputs may be governed by different licenses and consent obligations. Verify the exact artifacts and the rights to edit the image before reuse or commercial deployment.

## References

- [HandRefiner paper](https://arxiv.org/abs/2311.17957)
- [HandCraft paper](https://arxiv.org/abs/2411.04332)
- [HandFixer repository](https://github.com/Xiangyu-CAS/HandFixer)
- [ComfyUI FLUX.2 [klein] documentation](https://docs.comfy.org/tutorials/flux/flux-2-klein)
