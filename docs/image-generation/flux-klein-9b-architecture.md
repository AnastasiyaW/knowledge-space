---
title: FLUX.2 [klein] Architecture: Release-Bound Interface
description: "FLUX.2 [klein] architecture claims must be tied to the named official release and artifact; the public family supports text-to-image and reference editing, but internal block layouts, encoder wiring, quantization, and adapter compatibility are not safe to infer across variants or runtimes."
category: reference
tags: [flux, klein, architecture, model-contract, adapters, inference, provenance]
aliases: ["Klein Architecture", "FLUX2 Klein Architecture"]
---

# FLUX.2 [klein] Architecture: Release-Bound Interface

FLUX.2 [klein] is a model family, not one interchangeable architecture file.
Use the named checkpoint, official model card, source revision, and runtime as
the authority for any internal claim. Parameter-count labels, a family name,
or a third-party workflow do not establish block counts, text-encoder wiring,
latent layout, quantization support, or adapter compatibility.

## What the official family declaration supports

The [official FLUX.2 repository](https://github.com/black-forest-labs/flux2)
lists [klein] 4B, 9B, 9B KV, 4B Base, and 9B Base variants, and describes
text-to-image plus single- and multi-reference image editing for the family.
It distinguishes distilled variants from Base variants and recommends Base
models for fine-tuning/LoRA work.

That supports a release-selection decision. It does not make a fixed internal
transformer diagram, Qwen layer extraction recipe, VAE channel count, RoPE
offset, sequence limit, or inference setting true for every artifact bearing
the [klein] name.

## Bind the executable interface

For a specific deployment or training job, retain:

- official model identifier, revision/digest, license notice, and all required
  components;
- runtime source/version, tokenizer/text encoder, VAE/decoder, scheduler and
  image/reference input schema;
- dtype/quantization and device/back-end support as documented for that exact
  release;
- exposed generation/editing entry point, required preprocessing, and output
  metadata; and
- a baseline receipt proving the selected text, single-reference, or
  multi-reference path actually executes.

Reference images are inputs with their own ownership, preprocessing, count,
order, and failure policy. Do not infer a common latent-sequence layout or
reuse state from a different variant because a UI accepts multiple images.

## Base, distilled, and compatibility boundary

Base and distilled releases have different stated purposes. The current BFL
[klein training guide](https://docs.bfl.ai/flux_2/flux2_klein_training)
describes Base models as undistilled starting points for fine-tuning, while
the public model overview lists family-level runtime/usage distinctions. Pin
the chosen artifact instead of presenting that guidance as a blanket
conversion or inference guarantee.

An adapter is compatible only after the target base checkpoint, architecture,
loader, adapter configuration, and output behavior have been tested together.
Never load a FLUX.1, 4B, 9B, community, or quantized adapter based solely on
its filename, parameter count, or presumed hidden shape. A failed or
unverified adapter must return a visible incompatibility result, not a silent
partial merge.

## License and output boundary

The local-weight license attaches to the named artifact, not to the generic
word “FLUX.” The [official model table](https://github.com/black-forest-labs/flux2)
currently lists Apache-2.0 for [klein] 4B/4B Base and the FLUX
Non-Commercial License for 9B variants. Verify the attached license and
current commercial path before any deployment or distribution; a fine-tuned
adapter may be a derivative with additional obligations.

Generated or edited output also needs its own provenance, rights, and visual
review. A model capability does not prove that a particular edit preserved
facts, identity, product geometry, text, or protected regions.

## Related pages

- [[flux-klein-capability-map]]
- [[flux-klein-9b-inference]]
- [[diffusion-lora-training]]
- [[lora-fine-tuning-for-editing-models]]
