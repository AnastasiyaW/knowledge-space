---
title: "MMDiT: Multimodal Diffusion Transformer"
description: "MMDiT is the Stable Diffusion 3 multimodal transformer pattern: modality-specific representations participate in joint attention; implementation APIs and LoRA target names vary by model revision."
category: architectures
tags: [mmdit, transformer, diffusion, attention, architecture, dit, joint-attention, stable-diffusion-3]
aliases: ["Multi-Modal Diffusion Transformer", "MM-DiT"]
---

# MMDiT: Multimodal Diffusion Transformer

**Scope checked: 2026-09-04.** MMDiT is the multimodal diffusion-transformer architecture introduced with Stable Diffusion 3. It represents image and language inputs with modality-specific parameters, joins their token sequences for attention, and then continues modality-specific processing. That joint-attention boundary allows image and text representations to influence one another without treating every implementation as the same model or API.

## Core Design

The Stable Diffusion 3 paper describes MMDiT as two representation streams with separate weights whose token sequences meet at attention. This is different from treating a text encoder as a passive key/value source for a separate image-only transformer:

| Concern | MMDiT boundary |
|---|---|
| representation | image and text retain modality-specific parameters |
| attention | the streams can exchange information through joint attention |
| denoising | the multimodal transformer predicts over encoded image latents |
| implementation | configuration, text encoders, latent format, and block names belong to a specific model revision |

The architecture is relevant to Stable Diffusion 3. Other transformers may share ideas such as dual streams or joint attention, but a similar diagram or marketing label is not proof of parameter, checkpoint, or adapter compatibility.

## Integration Is Model-Specific

For the current Diffusers SD3 pipeline, the MMDiT component is exposed as `SD3Transformer2DModel` alongside the VAE, text encoders, scheduler, and pipeline configuration. Those class names and loader semantics are implementation details, not a portable specification.

Before adapting or operating an MMDiT-based model:

1. pin the model, pipeline, and library revision;
2. inspect the published configuration and state-dict/module names;
3. use the adapter or LoRA loader intended for that exact transformer;
4. record the text encoders, latent VAE, scheduler, precision, and prompt settings as part of the run identity;
5. validate output and failure behavior on a small fixture before a wider render batch.

Do not copy a static list of `to_q` or `add_q_proj` target modules from an unrelated MMDiT-like model. Module names, projections, dual-stream layers, and supported adapter formats change between releases.

## Performance and Editing Claims Need Measurement

Memory and latency depend on image-token count, text length, transformer configuration, attention implementation, precision, and hardware. Profile the exact pipeline instead of reusing a resolution/VRAM figure from another model. Likewise, joint attention can help model conditioning but does not guarantee exact text, region preservation, compositional correctness, or safe editing.

For a controllable editing workflow, keep separate evidence for:

- source-image preservation;
- requested local change;
- prompt and typography accuracy;
- adapter/model revision;
- output review and permitted publication use.

## References

- [Stable Diffusion 3 research paper](https://arxiv.org/abs/2403.03206)
- [Stability AI MMDiT architecture overview](https://stability.ai/news-updates/stable-diffusion-3-research-paper)
- [Diffusers SD3 transformer documentation](https://huggingface.co/docs/diffusers/main/en/api/models/sd3_transformer2d)
- [Diffusers Stable Diffusion 3 pipeline documentation](https://huggingface.co/docs/diffusers/main/en/api/pipelines/stable_diffusion/stable_diffusion_3)
