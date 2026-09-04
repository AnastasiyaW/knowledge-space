---
title: "FLUX.2 [klein] 9B Identity LoRA: Disentanglement Contract"
description: "A FLUX.2 [klein] 9B identity LoRA is a version-, data-, and rights-bound adapter experiment; bind the official base release and terms, adapter/runtime format, authorized identity references, label/caption and preservation policy, source-disjoint identity and non-target evaluation, and review before any use."
category: techniques
tags: [flux2-klein, lora, identity, disentanglement, provenance, evaluation]
aliases: ["LoRA Identity Disentanglement in FLUX.2 Klein 9B", "FLUX.2 Klein Identity LoRA"]
---

# FLUX.2 [klein] 9B Identity LoRA: Disentanglement Contract

An identity LoRA learns an adapter for a particular base-model release; it
does not isolate a person from every surrounding attribute by default.
“Disentanglement” is a preservation claim that needs evidence for the named
data, adapter, runtime, and prompt/edit workflow.

The official [FLUX.2 [klein] training documentation](https://docs.bfl.ai/flux_2/flux2_klein_training)
documents LoRA fine-tuning for the family, including character-consistency use
cases. It also distinguishes the 9B base model and its terms from other
variants. That supports an experiment on the exact compatible release, not a
claim that block choices, rank reduction, adapter arithmetic, or another
family's recipe transfers unchanged.

## Bind the adapter and its authority

For each run, retain:

- official base-model/checkpoint identifier, artifact digest, license and
  access terms, model runtime, and adapter serialization/loading path;
- authorized reference assets, consent or other usage authority, purpose,
  retention/deletion rules, captions, trigger vocabulary, and any excluded
  attributes or regions;
- training split, source/derivative grouping, preprocessing, crop/orientation,
  caption policy, augmentation policy, code/config revision, and seeds;
- proposed adapter file, merge/strength controls, output digest, and the
  exact workflow used for evaluation; and
- reviewer decision with identity-fit evidence, non-target preservation
  evidence, failure examples, and a permitted-use conclusion.

A 9B adapter must be paired with the model release and runtime it was trained
for. Do not infer compatibility from a similar FLUX variant, a file extension,
or a community UI label.

## Measure separation rather than assume it

Define which requested identity properties may transfer and which
non-target properties must remain controllable: pose, expression, age
presentation, clothing, background, lighting, style, body, and protected
attributes. Evaluate the requested transfer separately from preservation on
held-out, source-disjoint prompts and references. Keep authorized reviewer
corrections and negative cases, especially where an adapter repeats a
background, changes a protected region, or creates an unintended likeness.

Block targeting, rank selection, orthogonality losses, subtraction, merging,
and SVD truncation are model- and implementation-specific experiments. They
need a declared hypothesis, pinned implementation, comparison baseline, and
the same identity/preservation review; none is a universal cleanup step.

## Failure boundary

If the base release or terms are unknown, reference authority is incomplete,
the adapter/runtime format differs, source groups leak into evaluation, or a
reviewer cannot distinguish requested transfer from non-target change, keep
the adapter out of use. Do not silently load it on another variant, remove
evidence, or label a generated likeness as verified identity.

## Related pages

- [[flux-klein-character-lora]]
- [[diffusion-lora-training]]
- [[lora-auxiliary-losses]]
- [[face-beautify-edit-lora]]
