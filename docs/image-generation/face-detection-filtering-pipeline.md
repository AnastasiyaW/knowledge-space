---
title: Face Detection and Filtering: Candidate Review Pipeline
description: Face filtering is a provenance-preserving candidate-selection pipeline; detector boxes and landmarks support review, but they do not establish identity, consent, image realism, or training suitability.
category: workflows
tags: [face-detection, dataset-curation, provenance, quality-control, privacy, review]
aliases: ["Face Detection & Filtering Pipeline", "Face Dataset Review"]
---

# Face Detection and Filtering: Candidate Review Pipeline

Face detection should produce review candidates and structured evidence, not an
automatic statement that an image is a real person, has usable consent, or is
suitable for training. Keep the filtering decision traceable to an input and
to a declared policy.

## Inventory before inference

Create an immutable input manifest with a digest, source location, license or
consent evidence, ingestion time, and access class for every asset. Do not
replace this manifest with a detector score. It remains the authority for
rights, retention, and downstream audit.

## Candidate-detection stage

Run a versioned detector and save the input digest, model revision, box,
confidence, crop coordinates, and error state. The
[MediaPipe Face Detector](https://ai.google.dev/edge/mediapipe/solutions/vision/face_detector/python)
supports image and video inputs and returns face locations with six keypoints:
the eyes, nose tip, mouth, and ear-tragion points. Those outputs can support
crop and orientation review.

They do not establish a person's identity, consent, age, emotion, or whether
the depicted face is photographic rather than synthetic. Treat model
confidence as a ranking signal whose threshold is calibrated locally, not as a
universal acceptance criterion.

## Quality and relevance gates

Define the target use first, then measure only relevant properties:

1. **Framing:** sufficient visible area and a crop compatible with the intended
   training or edit task.
2. **Image quality:** focus, compression damage, clipping, occlusion, and
   resolution reviewed against locally labeled examples.
3. **Editability:** only when the declared task requires it; retain the
   reviewer rationale rather than inferring it from a generic face score.
4. **Rights and privacy:** consent/license evidence, retention class, and
   approval for the intended derivative use.

Automated scores may triage the queue, but uncertain cases should stay in
review rather than being silently accepted or discarded.

## Similarity, duplicates, and splits

Use perceptual or embedding similarity to propose duplicate and near-duplicate
groups. Preserve each source record, record the grouping model and threshold,
and ask a reviewer or a clear policy rule to decide which representation may
be used. Never use a similarity score as proof that two images show the same
person.

For model evaluation, split by source, capture session, or known subject group
where available. This prevents near-identical images from leaking across train
and validation partitions. Record the split rule and its exceptions.

## Output schema and release decision

Each result should include:

- input digest and provenance pointer;
- detector/quality-model revisions and raw outputs;
- decision (accept, review, or reject) with a reason code;
- reviewer or policy version; and
- downstream restrictions, including deletion/retention obligations.

Only an accept record with rights evidence and a declared use scope may enter
a face-edit training set. The rest remains traceable for correction or audit.

## Related pages

- [[face-beautify-edit-lora]]
- [[rights-first-text-to-mask-training]]
- [[diffusion-lora-training]]
