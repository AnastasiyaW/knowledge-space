---
title: "MegaStyle: Release-Bound Style-Transfer Contract"
description: "MegaStyle is a research code, model, and dataset release for image style transfer; bind the exact repository/artifact revision and license, base-model/runtime dependency, reference and prompt provenance, rendering and output contract, source-disjoint style/content/preservation evaluation, and human review before publishing or training on results."
category: reference
tags: [megastyle, style-transfer, flux, provenance, licensing, evaluation]
aliases: ["MegaStyle FLUX Style Transfer", "MegaStyle Style Transfer"]
---

# MegaStyle: Release-Bound Style-Transfer Contract

[Tencent MegaStyle](https://github.com/Tencent/MegaStyle) is a research
repository covering a style-data pipeline and named MegaStyle artifacts. The
repository evolves: it publishes code, data, checkpoints, demos, and
ComfyUI-related material across MegaStyle and MegaStyle++ releases. Treat a
style-transfer result as a release-specific experiment, not as a generic
single-reference capability or a stable product API.

## Pin the effective release

For every experiment or workflow, retain:

- repository commit, model/checkpoint and dataset artifact identifiers/digests,
  base-model dependency, runtime/dependency versions, and license terms for
  every code, weight, dataset, and reference asset;
- the exact invocation path, including local code modifications, UI/workflow
  JSON, input preprocessing, encoder/adapter selection, prompt rendering, and
  output encoding;
- source/reference asset digests, rights/consent record, intended style
  property, protected content, prompt, and whether the input or output may be
  retained, shared, or used for further training; and
- generated output, reviewer decision, correction path, and reproduction
  receipt.

The repository's named FLUX, encoder, demo, or custom-node material does not
establish compatibility with a different base model, checkpoint, ComfyUI
version, or host. Verify the current release's own dependencies instead of
copying an earlier workflow or file size as a portable requirement.

## Evaluate style and preservation independently

Separate the requested style effect from preservation of subject, geometry,
text, product details, colors, composition, and protected regions. Use
source-disjoint evaluation assets and compare a declared baseline against the
same prompt/rendering contract. A style-similarity score or visually pleasing
sample does not establish factual accuracy, identity preservation, legal
authority, or suitability for a production delivery.

If outputs are candidates for dataset construction, record their generator
release and reviewer decision. Do not relabel derived images as source
photographs or mix them with approved data without a lineage boundary.

## Failure boundary

If artifact/release terms, base-model compatibility, source authority,
rendering path, or review evidence is missing, keep the result in research
state. Do not substitute another adapter, reference image, checkpoint, or
license while reporting it as the same MegaStyle run.

## Related pages

- [[style-reference-ux]]
- [[flux-klein-style-lora-system]]
- [[diffusion-lora-training]]
- [[paired-training-for-restoration]]
