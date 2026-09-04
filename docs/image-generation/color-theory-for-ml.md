---
title: Color for ML: Task and Evidence Contract
description: "Color guidance for ML is a task-specific representation and evidence contract: name the source encoding, illuminant or viewing assumptions, target transform, palette intent, and human-review purpose; artistic harmony, spectral labels, and psychological associations are hypotheses, not universal labels or model controls."
category: reference
tags: [color, machine-learning, colorimetry, palette, data-provenance, evaluation, color-management]
aliases: ["Color Theory", "Color Reference for Diffusion"]
---

# Color for ML: Task and Evidence Contract

Color in an ML workflow is not one universal feature. A palette description,
device RGB values, a calibrated colorimetric measurement, and an editorial
preference answer different questions. Name the representation and the target
task before turning color into a training signal, control, score, or quality
claim.

## Separate the evidence types

| Use | What it can support | What it cannot establish alone |
|---|---|---|
| Color-managed capture or target | a measured transform under declared conditions | a universal appearance under every illuminant or display |
| Palette or harmony brief | approved editorial intent | an objective quality or psychological truth label |
| Prompt or reference image | a requested visual direction | deterministic color control across model releases |
| Annotator preference | a bounded review decision with rubric and context | a universal human response or protected-trait inference |

[CIE Colorimetry](https://www.cie.co.at/publications/colorimetry-4th-edition)
describes standardized colorimetric foundations and references color-appearance
models. That supports explicit representation and viewing assumptions; it does
not make artistic wheel positions, wavelength names, or cultural associations
universal labels for a model.

## Bind the data representation

For every training or evaluation set, record:

- source file/profile, decode, transfer function, and working representation;
- illumination or viewing assumptions when measured appearance matters;
- any ICC, OpenColorIO, or other transform/configuration revision;
- crop, resize, tone mapping, gamut mapping, and color augmentation policy;
- palette/reference provenance, authorial intent, and rights; and
- label rubric, annotator context, uncertainty, and exclusion policy.

The [ICC profile architecture](https://www.color.org/getting-started/) and
[OpenColorIO configuration model](https://opencolorio.readthedocs.io/en/latest/guides/authoring/authoring.html)
make transforms explicit. Apply the same discipline to data ingestion:
unlabeled RGB values from mixed sources must not be treated as one calibrated
color domain.

## Design controls for the named task

A palette controller can be evaluated against an approved target palette or
reference image. A color-correction model can be evaluated against
source-aligned measurements. A generative model can be reviewed for whether
its output follows a permitted visual direction. Each needs a different
acceptance test.

Do not assume that a color name maps to a fixed device value, that a text
prompt controls a hue identically across checkpoints, or that a wide-gamut
intent survives an sRGB-only source/output path. Pin the model, tokenizer or
prompt processor, image pipeline, and output transform when making a
reproducible color claim.

## Evaluate without inventing human facts

Split data by original asset, capture session, derivative chain, and reference
palette so near-duplicates cannot leak color targets into holdouts. Test on
the actual delivery transform and review gradients, neutral/target regions,
gamut behavior, material identity, text, and protected areas.

Color may influence an editorial review, but do not use it to infer health,
emotion, ethnicity, attractiveness, or another sensitive trait. Psychological
or cultural color associations are contextual hypotheses that require their
own consent, study design, and bounded interpretation; they are not automatic
training labels.

## Release gate

Release a color-aware ML capability only with an identified representation,
traceable transforms, authorized data, source-disjoint evaluation, output
provenance, and task-specific human review. If the workflow cannot show
whether a result is a calibrated correction, a requested style, or plausible
generation, label it as a reviewable visual proposal rather than factual
color recovery.

## Related pages

- [[color-space-and-gamma-reference]]
- [[color-correction-by-numbers]]
- [[color-checker-and-white-balance]]
- [[style-reference-ux]]
