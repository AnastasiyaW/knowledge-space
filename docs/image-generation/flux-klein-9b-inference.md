---
title: FLUX.2 [klein] 9B Inference
description: FLUX.2 [klein] 9B inference must follow the published model variant, checkpoint, scheduler, and license; benchmark the exact text or edit workflow instead of copying generic sampler, VRAM, or LoRA rules.
category: models
tags: [flux, flux2, klein, 9b, inference, editing, lora, reproducibility, licensing]
aliases: ["Klein 9B", "FLUX Klein 9B", "Klein Distilled"]
---

# FLUX.2 [klein] 9B Inference

FLUX.2 [klein] is a model family. FLUX.2 [klein] 9B is a named distilled
release, but it is still not a complete inference configuration without its
checkpoint revision and runtime assets. The [official FLUX.2
repository](https://github.com/black-forest-labs/flux2) distinguishes 9B, 9B
KV, and 9B Base variants; its guidance positions distilled variants for
interactive workflows and base variants for fine-tuning and maximum
flexibility. Treat the named checkpoint and its published runtime assets as
one contract.

## Identify the exact contract

Record before an inference or editing run:

- model and checkpoint revision, including distilled/base or KV variant;
- pipeline, scheduler, text encoder, decoder/VAE, adapter loader, and runtime;
- prompt or image-reference fixture, seed, dimensions, and output format;
- all adapters and their source/base-model compatibility; and
- the applicable weights, API, and derivative-use terms.

The official project lists FLUX.2 [klein] 9B under a non-commercial license.
That does not authorize a product workflow by itself: verify the current terms
for the selected weights and separately verify any hosted-service or
third-party component terms.

## Text-to-image and editing are separate tests

For text-to-image, use a small, versioned prompt suite that includes
composition, material, typography, and negative fixtures. For image editing,
retain the source asset and declare the requested changes and protected
properties before generation.

The [FLUX.2 image-editing documentation](https://docs.bfl.ai/flux_2/flux2_image_editing)
describes text-directed single- and multi-reference editing. It does not mean
that every local wrapper, checkpoint, or adapter preserves all details. Check
the exact route with source/edited comparisons, not with a general claim about
model capability.

## Tune by measurement, not folklore

Do not copy a universal step count, guidance value, sampler, denoise strength,
VRAM figure, or LoRA-weight range from another workflow. Instead:

1. run the published baseline for the chosen checkpoint;
2. vary one supported setting at a time on the same fixtures;
3. measure cold and warm latency, peak memory, reproducibility, and visual
   acceptance;
4. evaluate source preservation separately for an edit workflow; and
5. publish the selected version tuple and known limits with the job.

Quantization, compilation, and memory offloading are runtime trade-offs. See
[[diffusion-inference-acceleration]] for the receipt required before they are
combined with an image workflow.

## Adapter compatibility

An adapter must name the exact base checkpoint and loader it was trained
against. Similar parameter counts or a shared “FLUX” label are not evidence of
compatibility. Test an adapter alone before testing a combination, keep its
scale and load order in the run receipt, and reject an output if its protected
content drifts.

For training a new adapter, use the current model-specific guidance such as
the [FLUX.2 [klein] training documentation](https://docs.bfl.ai/flux_2/flux2_klein_training),
then validate the resulting artifact under the same inference pipeline that
will serve it.

## Release record

Store the model manifest, prompt/reference fixture, output hash, acceptance
review, license decision, and any output-marking metadata with each approved
run. This makes a later runtime or model upgrade observable instead of
silently changing image behavior.

## Related pages

- [[flux-klein-9b-architecture]]
- [[flux-klein-style-lora-system]]
- [[diffusion-inference-acceleration]]
- [[flow-matching]]
