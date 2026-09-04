---
title: "Step1X-Edit: Release-Specific Image Editing"
description: "Step1X-Edit is a StepFun multimodal image-editing family with release-specific pipelines; pair each checkpoint with its documented Diffusers branch and verify model and artifact terms independently."
category: models
tags: [image-editing, step1x, stepfun, multimodal, diffusion, lora, gedit-bench]
aliases: ["Step1X-Edit"]
---

# Step1X-Edit: Release-Specific Image Editing

**Scope checked: 2026-09-04.** Step1X-Edit is StepFun's open image-editing research and model family. Its published approach uses a multimodal language model to process a reference image and editing instruction, then couples the resulting latent representation to a diffusion image decoder. It is an image-editing stack, not a generic compatibility layer for every image model.

## Treat Each Release as Its Own Integration Target

The current upstream repository documents the original model alongside newer `v1p1` and `v1p2` releases. The local runtime is explicitly release-dependent: upstream names different pipeline classes and different Diffusers branches for different checkpoints. Select the model card, repository revision, dependency branch, and example for one release as a single compatibility unit.

Do not infer that another vendor's image-editing model is a Step1X-Edit variant merely because both use multimodal conditioning or diffusion. In particular, Qwen image-editing releases are separate artifacts with their own pipelines and terms.

## What the Official Project Provides

The official repository supplies:

- local inference examples for documented releases;
- model artifacts and a GEdit-Bench evaluation resource;
- fine-tuning scripts and an example LoRA path for the original model;
- optional performance integrations and community integrations, each with its own compatibility boundary.

The project also distinguishes a newer reasoning-oriented release from earlier variants. That makes a version-free inference recipe unsafe: a pipeline that imports or runs for one checkpoint is not evidence that it is correct for another.

## Safe Integration Contract

1. Choose one exact Step1X-Edit checkpoint and read its current model card and matching upstream example.
2. Build the environment from the corresponding documented dependency branch; record the repository commit and package versions.
3. Start with a small, rights-cleared image and an explicit edit instruction. Preserve the untouched input.
4. Retain the checkpoint digest, pipeline class, prompt, seed where available, input/output digests, and any enabled optional module.
5. Test a held-out fixture for both the requested change and the features that must remain unchanged.

When fine-tuning or loading a LoRA, keep it tied to the exact base release, target modules, and loading path used to produce it. A successful file load is not proof of semantic compatibility or preservation quality.

## Evaluate Editing, Not a Demo Claim

Use separate acceptance checks:

| Question | Evidence |
|---|---|
| Did the requested edit occur? | task-specific visual review against the instruction |
| Did protected content remain intact? | side-by-side comparison of faces, text, logos, geometry, and product details |
| Is the result reproducible? | immutable environment, model revision, prompt, seed, and input/output receipt |
| Does a benchmark apply? | the declared GEdit-Bench protocol, not a score copied to another task |

For source-faithful work such as product identity, documents, evidence, or measurements, an edited image is a derived artifact. Keep the original as the authority.

## Terms and Deployment Boundary

The repository license, checkpoint license, hosted service terms, base dependencies, training data, and input-image rights can differ. Confirm the current terms for every artifact actually used before commercial or hosted deployment; no family-level label is a substitute for that check.

## References

- [Step1X-Edit official repository](https://github.com/stepfun-ai/Step1X-Edit)
- [Step1X-Edit technical report](https://arxiv.org/abs/2504.17761)
- [Step1X-Edit model collection](https://huggingface.co/stepfun-ai/Step1X-Edit)
