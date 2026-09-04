---
title: Segmentation Dataset Preparation: Lineage and Supervision Contract
description: "Segmentation dataset preparation is a lineage and supervision contract: bind source/rights, annotation policy and mask semantics, group-disjoint splits, augmentation and interpolation behavior, class coverage, and release metrics, and fail closed on leakage, unreviewed labels, or incompatible targets."
category: techniques
tags: [segmentation, dataset, annotations, masks, augmentation, splits, provenance, evaluation]
aliases: ["Binary Small-Object Segmentation Dataset", "Segmentation Data Preparation"]
---

# Segmentation Dataset Preparation: Lineage and Supervision Contract

A segmentation dataset is not just images and masks. It is a versioned
supervision system: source assets, rights, annotation policy, mask semantics,
sampling rules, split units, transformations, and evaluation must agree. A
model can produce attractive overlays while training on leakage, mismatched
masks, or labels that do not represent the intended task.

## Define the sample and annotation contract

For every source asset and derived crop, retain a stable source/group ID,
asset digest, rights and permitted purpose, acquisition and preprocessing
lineage, annotation version/reviewer status, class taxonomy, geometry, mask
encoding, ignore/unknown semantics, and any confidence or exclusion reason.
Specify whether a mask is binary, multiclass, instance-aware, soft, or
partially labeled. Never infer class meaning from an 8-bit value alone.

Inspect source image, mask, overlay, metadata, and class counts together.
Quarantine unreadable, duplicate, ambiguous, or unreviewed labels rather than
silently converting them to background.

## Split by the real leakage unit

All crops, augmentations, frames, near-duplicates, and repeated views that
share a causal source must remain in one split group. The appropriate group
may be a source image, subject, product, scene, session, time window, or
capture device; document why it represents the expected deployment boundary.

[scikit-learn's GroupKFold](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html)
provides non-overlapping groups, but it cannot choose the right group
definition or prove that two assets are not duplicates. After every split,
retain manifests and assert no group, asset digest, or derivative lineage
crosses train, validation, or test. Review per-class coverage after grouping;
do not repair a rare-class split by leaking related crops.

## Keep images and supervision synchronized

Every spatial transform must update every relevant target with the same sampled
geometry. Every pixel-only transform must be checked against target semantics.
[Albumentations' target documentation](https://albumentations.ai/docs/2-core-concepts/targets/)
distinguishes image-like and mask-like targets and explains why categorical
masks normally need mask-safe interpolation. The exact library version and
pipeline configuration still belong in the dataset release.

Record crop/pad/resize interpolation, rotation, mask-value handling, ignored
pixels, transforms enabled per split, and any target routing for boxes,
instances, depth, or metadata. A transform that is unsupported for the
declared target must fail rather than generate plausible but misaligned
supervision.

## Evaluate the released dataset, not a convenient crop

Freeze a source-disjoint test set before tuning thresholds or losses. Report
class-wise and group-aware metrics, sample counts, uncertainty/coverage, and
qualitative overlays at the delivery resolution. Choose model, resolution,
loss, class weighting, threshold, and augmentation from this versioned
experiment; there is no universal binary-output setup or loss weight for rare
objects.

For small or safety-relevant targets, inspect false negatives, false
positives, boundaries, and empty-mask cases by source group. Keep an error
taxonomy so future annotations and data collection can be improved without
rewriting historical labels.

## Failure and release boundary

Block a dataset release when source rights or label policy are missing, group
overlap is detected, transformations are incompatible, class/mask semantics
are ambiguous, test examples were used for tuning, or annotations lack the
required review. Do not silently drop records, relabel unknown pixels,
substitute a split, or collapse instances into background to make a metric
look better.

## Related pages

- [[in-context-segmentation]]
- [[rights-first-text-to-mask-training]]
- [[defect-detection-small-objects]]
- [[paired-training-for-restoration]]
