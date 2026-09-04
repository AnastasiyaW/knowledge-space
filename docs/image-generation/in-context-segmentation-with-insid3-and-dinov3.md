---
title: INSID3 with DINOv3: Candidate-Mask Contract
description: "INSID3 with DINOv3 transfers a supplied reference mask through a named frozen-backbone release as a candidate segmentation, not ground truth; bind the repository and model revisions, license and access, reference/mask provenance, preprocessing and resolution, positional-bias configuration, uncertainty policy, and source-disjoint review before use."
category: reference
tags: [segmentation, insid3, dinov3, candidate-masks, provenance, review]
aliases: ["In-Context Segmentation with INSID3 and DINOv3", "INSID3 DINOv3 Segmentation"]
---

# INSID3 with DINOv3: Candidate-Mask Contract

The upstream [INSID3 repository](https://github.com/visinf/INSID3) describes
a training-free in-context segmentation method operating with one frozen
DINOv3 backbone and a supplied reference image/mask. The
[DINOv3 reference repository](https://github.com/facebookresearch/dinov3)
publishes the backbone artifacts. Together they justify testing the named
release; they do not turn a predicted mask into ground truth, consent
evidence, identity evidence, a medical conclusion, or an automatic training
label.

## Bind the exact release

For every candidate mask, retain:

- INSID3 repository and code revision, DINOv3 model/weight identifier,
  artifact digest, license/access terms, and environment/dependency record;
- reference image and mask digests, author/rights record, class/part
  definition, crop/orientation/preprocessing, and reference-quality review;
- target asset digest, target-domain identifier, preprocessing, input
  resolution, color/orientation policy, and output mapping to source pixels;
- documented positional-bias/debiasing, refinement, threshold, and
  post-processing configuration, including changes from the upstream default;
- output mask, uncertainty/failure signals when available, reviewer decision,
  correction artifact, and provenance link; and
- source-disjoint validation split and task-specific quality/preservation
  evidence.

Do not substitute a local adapter, inferred internal feature layout, or
monkey-patch for the upstream interface unless that integration has its own
versioned implementation and evaluation receipt.

## Review candidate masks before use

Inspect thin structures, small or repeated objects, occlusion, reflections,
transparent materials, blur, shadows, difficult boundaries, and protected
regions in the source coordinate system. A plausible boundary can still be
semantically wrong or unsafe for the intended edit or dataset.

Keep source assets and derivatives together when splitting evaluation data.
The reference image, near-duplicate crops, the same subject, or related
derivatives must not leak between tuning and holdout review. Report transfer
quality, failure detection, domain shift, reviewer correction, and operational
escalation separately.

## Failure boundary

If the reference/mask provenance is incomplete, the model release or license
is unknown, preprocessing differs from the declared run, the target is
out-of-distribution, or review cannot validate a protected region, keep the
mask in visible review state and request manual annotation. Do not silently
accept, relabel, or use it as a source of factual, identity, medical, or
release-ready truth.

## Related pages

- [[in-context-segmentation]]
- [[rights-first-text-to-mask-training]]
- [[defect-detection-small-objects]]
- [[paired-training-for-restoration]]
