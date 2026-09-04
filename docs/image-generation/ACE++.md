---
title: "ACE++: Reference-Driven Image Creation and Editing"
description: "ACE++ provides reference-driven image creation and editing through task-specific LoRA workflows and a general FFT model; use the published base-model pairing and verify its terms."
category: models
tags: [image-editing, alibaba, flux, reference-image, inpainting, lora, comfyui]
aliases: ["ACE Plus", "FuseAnyPart"]
---

# ACE++: Reference-Driven Image Creation and Editing

**Scope checked: 2026-09-04.** ACE++ is Alibaba Tongyi Lab's post-training system for reference-image generation and editing. It combines reference images, edit images or masks when needed, and a text instruction. The official repository provides several task-specialized LoRA routes and a broader fully fine-tuned (FFT) model rather than one interchangeable checkpoint for every workflow.

## Select the Published Model Route

| Route | Intended scope | Operational note |
|---|---|---|
| Portrait LoRA | identity and portrait-reference generation or editing | use the accompanying reference workflow |
| Subject LoRA | object, logo, pattern, and subject consistency | use the accompanying reference workflow |
| Local Editing LoRA | mask- or control-guided local changes | may need the documented preprocessing route |
| FFT model | broader reference and editing tasks | the authors note less stable results than the specialized LoRA routes |

The repository recommends the LoRA workflows where a specialized route exists. A general model can be convenient, but it should not be treated as the quality baseline for a task that has a dedicated adapter.

## Base Model and Workflow Boundary

The published LoRA examples pair ACE++ with `FLUX.1-Fill-dev`; some workflows also use FLUX.1 Redux or documented preprocessing components. The FFT route has its own configuration. Keep the following as one versioned unit:

- ACE++ weights and selected workflow;
- base-model revision and any companion model;
- preprocessing model and mask/control convention;
- image dimensions, sequence-length setting, sampling controls, and prompt;
- output artifact and source-reference authorization.

Do not load an ACE++ adapter into an arbitrary FLUX checkpoint because the filenames look compatible. The repository's `max_seq_length` option is a memory-versus-detail control for the supplied workflow, not a universal quality setting.

## Practical Acceptance Checks

Test the exact editing class before relying on it:

1. confirm the reference subject/object is retained where required;
2. inspect the edit boundary, mask leakage, hands, typography, and small logos at delivery size;
3. check that unrelated regions remain unchanged when preservation is required;
4. retain input image, mask, prompt, seed, model revisions, and output for a reproducible review;
5. fall back to a controlled manual or compositing path when the result changes the wrong object.

The upstream project lists limitations in instruction following for some add/remove operations and notes possible artifacts. A visually plausible result is not evidence that the requested local edit was performed correctly.

## Licensing and Distribution

ACE++ is built on external base-model artifacts. Review the current license and access terms for the selected base model, the ACE++ weights, and every companion checkpoint before commercial use, redistribution, or exposing a hosted service. Do not promote a workflow as commercially cleared solely because its code is visible on GitHub.

## References

- [ACE++ official repository](https://github.com/ali-vilab/ACE_plus)
- [ACE++ paper](https://arxiv.org/abs/2501.02487)
- [ACE++ Hugging Face collection](https://huggingface.co/ali-vilab/ACE_Plus)
