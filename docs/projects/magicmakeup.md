---
title: MagicMakeup Transfer
category: projects
date: 2026-07-28
tags: [magicmakeup, magicmakeup-transfer, project]
aliases: ["MagicMakeup Transfer"]
---

# MagicMakeup Transfer

**Development line:** `project:magicmakeup` · thread `magicmakeup-transfer`  
**Last event:** 2026-07-28 · 1 dated since 2026-07-28 · **Researched:** 2026-09-05 · confidence: high

## What it is

MagicMakeup Transfer is an image-to-image makeup-transfer system with region control for research users who prepare face crops and masks.

- Reference transfer: transfers full-face, eye, and lip appearance from a reference portrait.
- Model checkpoint: uses a MagicMakeup checkpoint on FLUX.1-Kontext-dev.
- Output resolution: produces 1024 × 1024 crops and supports single-pair or all-to-all batch inference.

## Development line

- **2026-07-28 — MagicMakeup Transfer public project resources linked.** A region-controllable diffusion-transformer pipeline with face, eye, and lip transfer, built on FLUX.1-Kontext-dev.

## What changed

2026-07-28 — The official code and checkpoint release arrived. MagicMakeup became usable as a region-controllable diffusion-transformer pipeline with face, eye, and lip transfer, built on FLUX.1-Kontext-dev.

## How to use this

Start with the project page, repository, and hosted model resource as of 2026-07-28. Check those primary materials so exact versions and usage details stay verified.

1. Clone the official repository and create its recommended Python 3.10 environment with PyTorch 2.6.0/CUDA 12.4 and the listed dependencies.
  — <https://github.com/vivoCameraResearch/Magic-Makeup>
2. Accept the FLUX.1-Kontext-dev license, download that base model, then download the Anyou/MagicMakeup checkpoint.
  — <https://github.com/vivoCameraResearch/Magic-Makeup>
3. Place source and makeup-reference portraits in separate directories. Crop primary faces to centered 1024 × 1024 images and retain the preprocessing log.
  — <https://github.com/vivoCameraResearch/Magic-Makeup>
4. Generate matching face, eye, or lip masks for both images. Run test_single.py with the desired --label value: eyes, lip, or eyes,lip,face.
  — <https://github.com/vivoCameraResearch/Magic-Makeup>
5. Confirm filename-stem matches for every image and mask before running test_dir.py. The script pairs every source with every reference and skips unmatched masks.
  — <https://github.com/vivoCameraResearch/Magic-Makeup>

## Best practices

- Start with a single pair and inspect the comparison panel before an all-to-all batch. Batch mode skips pairs when crop and mask mismatches occur.
  — <https://github.com/vivoCameraResearch/Magic-Makeup>
- Use the default model-offload mode first. Choose sequential CPU offload only when GPU memory is constrained, because it slows inference.
  — <https://github.com/vivoCameraResearch/Magic-Makeup>
- Keep use within the stated non-commercial academic cosmetics-research scope. Do not repurpose it for face swapping, identity recognition, impersonation, or deceptive edits.
  — <https://github.com/vivoCameraResearch/Magic-Makeup>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- We found no versioned GitHub release or dated checkpoint publication, so the exact publication time of the code and checkpoint cannot be separated from the 2026-07-28 release event.
- The Hugging Face page exposes a generic Diffusers example that omits MagicMakeup’s mask-conditioned pipeline. The official repository remains the authoritative inference route.

## Sources

| source | title | read |
|---|---|---|
| https://vivocameraresearch.github.io/magicmakeup/ | MagicMakeup: A Region-Controllable Diffusion Transformer for High-Fidelity Makeup-Transfer | 2026-09-05 |
| https://github.com/vivoCameraResearch/Magic-Makeup | vivoCameraResearch/Magic-Makeup | 2026-09-05 |
| https://huggingface.co/Anyou/MagicMakeup | Anyou/MagicMakeup model card | 2026-09-05 |
| https://arxiv.org/abs/2607.20924 | MagicMakeup: A Region-Controllable Diffusion Transformer for High-Fidelity Makeup-Transfer | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:magicmakeup`, thread `magicmakeup-transfer`, 1 dated events 2026-07-28 → 2026-07-28.
- **Practical note:** Start with the project page, repository, and hosted model resource as of 2026-07-28. Verify exact versions and usage details from those primary materials.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.