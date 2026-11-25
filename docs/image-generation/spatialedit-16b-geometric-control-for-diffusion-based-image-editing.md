---
title: "SpatialEdit-16B: Geometry and Evaluation Contract"
description: "SpatialEdit-16B is a research release for geometry-driven image editing; bind the exact code/model artifact and terms, source and target asset authority, object/camera transformation and coordinate contract, preprocessing/runtime, geometry-aware and preservation evaluation, and human review before use."
category: techniques
tags: [spatialedit, image-editing, geometry, camera-control, provenance, evaluation]
aliases: ["SpatialEdit-16B Geometric Control", "SpatialEdit Geometry Editing"]
---

# SpatialEdit-16B: Geometry and Evaluation Contract

The [SpatialEdit paper](https://arxiv.org/abs/2604.04911) presents a
geometry-driven image-editing benchmark, synthetic supervision, and a
SpatialEdit-16B baseline for object-centric and camera-centric edits. The
[official release](https://github.com/EasonXiao-888/SpatialEdit) publishes
code, checkpoints, benchmark assets, and separate external prerequisites.
This supports evaluation of the named release; it does not make a plausible
image proof that the requested geometry was followed.

## Bind the release and edit contract

For every evaluated or published edit, retain:

- repository revision, model/checkpoint identifier and digest, code and
  artifact terms, dependency/runtime record, and every external prerequisite
  used by the chosen configuration;
- source-asset digest, ownership or authorized-edit record, subject/object
  definition, protected regions, and any prohibited semantic changes;
- task class: object translation, scaling, canonical rotation, or camera
  viewpoint/framing change; source and target coordinate systems; target box,
  pose, crop, resolution, and orientation convention;
- input preprocessing, VAE/model paths, seed, scheduler/settings, output
  digest, and mapping from output pixels back to the source frame; and
- geometric-fidelity result, non-target preservation result, failure examples,
  reviewer decision, and permitted-use conclusion.

Code availability or a permissive repository license does not establish terms
for every checkpoint, base model, dataset, or source image. Keep each
authority record separate.

## Evaluate geometry and preservation separately

Use held-out, source-disjoint assets that cover the required subject classes,
occlusion, reflections, fine boundaries, background complexity, and target
camera/object transformations. Score the requested transformation in its
declared coordinate system, then independently inspect object identity,
background continuity, lighting/shadow consistency, text, logos, and factual
product detail.

Do not collapse a visual-preference score into geometric correctness. A result
may look coherent while its object location, scale, orientation, or view
change is wrong. Compare against a declared baseline and retain both successful
and failed cases rather than selecting only attractive outputs.

## Gotchas

- **Issue:** A prompt can yield a semantically plausible scene with the wrong
  spatial result -> **Fix:** validate the requested box, pose, framing, or
  camera relation in the stated source coordinate system.
- **Issue:** The official release includes placeholder/internal paths and
  external checkpoint prerequisites -> **Fix:** replace them only in a
  versioned local configuration and record every resolved artifact before
  treating a run as reproducible.
- **Issue:** A general editing result is assumed to transfer to a new
  object/camera operation -> **Fix:** evaluate that operation on an
  operation-specific held-out set; do not infer it from the model family.

## Failure boundary

If source authority, exact release/terms, coordinate definition, preprocessing
record, or geometry-and-preservation review is missing, keep the output in
review state. Do not silently substitute another model, reinterpret a
semantic-only edit as metric control, or publish it as a verified view or
factual reconstruction.

## Related pages

- [[MMDiT]]
- [[flow-matching]]
- [[tile-position-encoding]]
- [[diffusion-inference-acceleration]]
- [[flux-klein-capability-map]]
