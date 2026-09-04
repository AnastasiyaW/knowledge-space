---
title: FlowInOne: Release-Bound Research Contract
description: "FlowInOne is a research release for visual-prompt image-in/image-out flow matching; bind the exact paper, checkpoint, code/runtime, license, task and input rendering contract, and source-disjoint task/preservation evaluation, and do not generalize paper benchmarks into production capability or commercial-use claims."
category: reference
tags: [flow-matching, multimodal, visual-prompts, image-to-image, evaluation]
aliases: ["FlowInOne", "Unified Multimodal Generation via Image Flow"]
---

# FlowInOne: Release-Bound Research Contract

[FlowInOne](https://arxiv.org/abs/2604.06757) is a research framework that
recasts multimodal generation as a visual flow: inputs such as text,
layouts, and editing instructions are rendered as visual prompts, then handled
by an image-in/image-out flow-matching model. The paper establishes a
research direction and named evaluation results. It does not by itself provide
a production service, a stable runtime interface, or blanket commercial-use
permission.

## Bind the release and task

For an experiment or integration, retain:

- paper version, code revision, checkpoint/artifact identifier, license terms,
  access conditions, and model-card evidence;
- task definition, expected output, known unsupported inputs, and the
  acceptance decision this output may inform;
- renderer/version that turns text, boxes, labels, sketches, or other inputs
  into the visual prompt, including fonts, layout, resolution, colors, and
  rasterization policy;
- input and output asset digests, preprocessing/postprocessing, seed or
  deterministic controls, and runtime/device version; and
- source-disjoint evaluation data, task-quality result, preservation result,
  reviewer decision, and failure examples.

Because the approach uses rendered visual prompts, that rendering path is part
of the model interface. Altering a font, layout, crop, coordinate convention,
or image scale can alter the experiment; it is not a harmless presentation
change.

## Evaluate the requested outcome separately

Use a held-out source split that prevents the same asset or its near
derivatives from appearing in tuning and evaluation. Measure the requested
task separately from preservation of non-target regions, source facts, text,
geometry, and protected attributes. Human review may complement a defined
criterion, but a paper-level preference result is not proof of reliability for
another subject, workflow, or delivery requirement.

Generated outputs are candidates. They require task-appropriate review before
publication, dataset inclusion, commercial use, or any decision that assumes
the image is faithful to source evidence.

## Failure boundary

If the release, license, checkpoint, renderer, input mapping, or evaluation
split is unknown, keep the result in research/review state. Do not fill in a
missing artifact with a similarly named model, copy paper sampling values into
another runtime, or infer support for an untested modality from the family
name.

## Related pages

- [[flow-matching]]
- [[MMDiT]]
- [[paired-training-for-restoration]]
- [[in-context-segmentation]]
