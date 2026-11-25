---
title: PixelSmile: Release-Bound Expression Editing
description: "PixelSmile is a release-bound facial-expression editing project; pin its published human preview, base model, patched runtime, consented source image, and expression review rather than treating benchmark numbers or adapters as general guarantees."
category: models
tags: [facial-expression, image-editing, lora, qwen-image-edit, provenance, consent, evaluation]
aliases: ["PixelSmile"]
---

# PixelSmile: Release-Bound Expression Editing

[PixelSmile](https://github.com/Ammmob/PixelSmile) is a research and software
project for fine-grained facial-expression editing. Its upstream repository
describes a Qwen-Image-Edit-2511 base model, a published human-preview
PixelSmile weight, inference and benchmark artifacts, a demo, and released
training code. The repository separately lists a future stable model, so each
run must be tied to the exact published artifact it uses.

The associated [paper](https://arxiv.org/abs/2603.25728) reports continuous
expression control through textual latent interpolation. It is evidence for the
paper's checkpoint, data, and evaluation protocol—not a guarantee that every
face, expression, prompt, or downstream integration will behave linearly.

## Release contract

Before running or evaluating PixelSmile, record:

- repository revision and the model/adapter file digest;
- the exact Qwen base-model revision, installed runtime, and required local
  patch status;
- source-image authority, consent, allowed edit scope, and protected regions;
- requested expression and tested control range; and
- seed, input/output hashes, reviewer result, and failure status.

The upstream setup contains model-specific dependency and patch instructions.
Follow those instructions for the pinned release, then run a small
reproducible smoke test before a broader batch. A different Diffusers, base
model, adapter, or community node is a new compatibility target, not an
implicit fallback.

## Facial-editing boundary

PixelSmile changes the depiction of a face. It must not be used to infer a
person's actual emotional state, medical condition, identity, age, or intent.
Use only authorized source images, respect the agreed editing scope, and make
the derived result reviewable.

For each output, review separately:

| Review | Question |
|---|---|
| Requested edit | Does the visible expression match the approved request? |
| Preservation | Are identity-relevant appearance, pose, scene, accessories, and protected regions preserved to the agreed scope? |
| Artifact check | Did the edit introduce changed teeth, eyes, skin texture, background geometry, text, or duplicate features? |
| Provenance | Can a reviewer recover source, adapter/base versions, parameters, and approval? |

Visual identity preservation is a release criterion, not a biometric proof.
When the edit changes an important source fact or cannot be reviewed, hold the
output rather than presenting it as a faithful correction.

## Training and reuse

The upstream project now publishes training material, but a local training run
needs its own data and rights contract. Do not assume that a public paper
dataset, a face collection, generated labels, or a released repository grants
rights to reuse person images in another product.

Keep training data, annotations, consent/provenance records, base model,
adapter, and evaluation split bound together. Validate on held-out,
source-disjoint examples and preserve a manual review path for sensitive
edits.

The repository is published under Apache-2.0, but code licensing is not a
substitute for checking the base model, adapter/model-card terms, community
integration terms, or source-image rights.

## Related pages

- [[textual-latent-interpolation]]
- [[face-beautify-edit-lora]]
- [[style-reference-ux]]
