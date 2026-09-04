---
title: Synthetic Detection Data: Evidence and Review Pipeline
description: Synthetic detection data is a labeled candidate corpus, not automatic ground truth; preserve generator and source provenance, review annotations, prevent split leakage, and validate on real held-out data.
category: pipelines
tags: [synthetic-data, object-detection, annotations, provenance, review, dataset-quality, validation]
aliases: ["Synthetic Dataset Pipeline for Object Detection", "Synthetic Detection Dataset"]
---

# Synthetic Detection Data: Evidence and Review Pipeline

Synthetic images and model-generated annotations can accelerate dataset
creation, but they are candidate evidence, not automatic ground truth. A
detector trained only on a generator's patterns can appear strong in a
synthetic validation set and fail on the real images it is intended to serve.

## Source and generator manifest

For every source or generated image, retain:

- input/reference digest and rights/license decision;
- generator, base model, checkpoint, prompt/control inputs, seed, and output
  digest;
- intended object classes and taxonomy revision;
- annotation producer/model revision and raw candidate output; and
- provenance label distinguishing captured, rendered, transformed, and
  generated material.

Do not claim that an image depicts a real object, a real defect, or a product
fact merely because a generator or auto-labeler named it that way.

## Candidate creation and annotation

Use automatic detectors, segmenters, captions, or render metadata to propose
boxes, masks, and classes. Preserve the raw proposal and present it in a
review tool that supports correction, rejection, missing-object addition, and
ambiguous-label escalation.

The final annotation record needs the reviewer/policy version, source
digest, taxonomy version, geometry, confidence or uncertainty, and decision
reason. Do not use a universal confidence, similarity, or image-quality
threshold; calibrate each rule against locally reviewed examples.

## Split without leakage

Split by source scene, product, subject, template, generator recipe, or
capture session—not merely by file. Near-identical synthetic variants, shared
backgrounds, or generated descendants must stay on one side of a train/holdout
boundary. Retain the split logic and exceptions in the dataset manifest.

Keep a real, source-disjoint test set whenever the intended deployment handles
real images. A synthetic-only score is a generator-alignment measurement, not
a field-performance claim.

## Train and validate

Bind the dataset version to the detector architecture, training configuration,
class mapping, and evaluation fixtures. Review:

- annotation coverage and false positives on a representative audited sample;
- small-object, occlusion, lighting, material, and background conditions;
- performance on real held-out data and on source groups unseen in training;
- calibration of confidence versus actual error; and
- failure cases that need data collection rather than synthetic expansion.

Publish metrics with the exact dataset manifest and test split. Do not
generalize a result from one object taxonomy to another.

## Release gate

Promote a dataset only when rights, provenance, annotation review, split
integrity, real-data validation, and rollback/removal obligations are
receipted. If the generator or annotation model changes, create a new dataset
version and repeat validation.

## Related pages

- [[face-detection-filtering-pipeline]]
- [[rights-first-text-to-mask-training]]
- [[flux-klein-jewelry-photography]]
- [[diffusion-lora-training]]
