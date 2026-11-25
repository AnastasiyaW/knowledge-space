---
title: Defect and Small-Object Detection: Evidence Contract
description: "Defect and small-object detection produces reviewable candidates, not automatic quality truth; bind the model, capture protocol, annotation or normal-reference policy, slicing or merge mapping, thresholds, and source-disjoint evaluation before any inspection or workflow decision."
category: reference
tags: [defect-detection, anomaly-detection, small-objects, inspection, provenance, evaluation, tiling]
aliases: ["Anomaly Detection", "Defect Detection Models", "Small Object Detection"]
---

# Defect and Small-Object Detection: Evidence Contract

Detection and anomaly systems identify candidates for inspection. A box, mask,
heatmap, or score is not proof that a product is defective, that a visual
change was introduced, or that an image is safe to publish. Bind the capture
conditions, task definition, model, and review policy before using a result in
an operational decision.

## Choose the task explicitly

| Task | Required supervision or reference | Output meaning |
|---|---|---|
| Supervised detection or segmentation | approved class taxonomy and source-linked annotations | candidate class/region |
| Anomaly detection | a defined normal-reference policy and known exclusions | deviation from that reference distribution |
| Before/after comparison | aligned, authorized paired captures and change policy | candidate difference |

[EfficientAD](https://anomalib.readthedocs.io/en/v2.0.0/markdown/guides/reference/models/image/efficient_ad.html)
is documented in Anomalib as a student-teacher anomaly method. Its paper
evaluates a particular model family on named datasets. Neither source makes an
anomaly map a universal defect label, sets a safe threshold for every material,
or guarantees a fixed latency or memory budget on another runtime.

## Bind capture and training evidence

For each sample or normal reference, retain:

- original asset/capture identity, rights, and product or scene scope;
- camera, lens, distance, focus, illumination, background, and processing
  conditions that affect visible texture;
- task taxonomy, inclusion/exclusion examples, annotation revision, and
  reviewer provenance;
- model/checkpoint, preprocessing, input resolution, runtime, and threshold
  policy; and
- uncertainty, rejected candidates, and known confounders.

Specular highlights, compression, dust on the capture path, focus changes,
background reflections, and geometry changes can look anomalous. Keep real
observations separate from synthetic defects and do not use an augmentation as
proof that a real-world defect detector is validated.

## Treat slicing as a coordinate contract

[SAHI](https://obss.github.io/sahi/guides/sliced-inference/) documents
overlapping slices, per-slice detection, and merging back into full-image
coordinates. If a high-resolution inspection uses tiles, record tile geometry,
overlap, input transform, coordinate mapping, merge/suppression rule, and
edge handling with the prediction. A detector's tile merge does not validate
an anomaly heatmap or a pixel-editing seam.

Evaluate candidates on the original image. A downsampled preview can conceal
the very small object or surface artifact the system claims to flag.

## Validate for the target environment

Split train, tuning, and test data by original asset, product/subject,
capture session, and derivative chain. Holdouts must include the material,
scale, lighting, and capture variations expected at release. Report
task-specific error analysis, including false candidate burden and missed
critical cases, instead of transferring AUROC, mAP, VRAM, or latency values
from a benchmark or another device.

Review predicted regions against the source image and the approved task
definition. Keep threshold changes versioned, and revalidate when camera,
lighting, preprocessing, tile plan, model, or runtime changes.

## Release gate

Publish only reviewable candidates with model/configuration provenance and a
visible uncertainty/failure state. Do not automatically reject inventory,
erase retouching details, or make a safety/quality verdict solely from a
detector score. If the policy requires an automatic action, define its
bounded authority, counter-check, audit receipt, and rollback path before
activation.

## Related pages

- [[tiled-inference]]
- [[low-vram-inference-strategies]]
- [[skin-retouch-pipeline]]
- [[synthetic-dataset-pipeline]]
