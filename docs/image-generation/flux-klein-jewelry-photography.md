---
title: FLUX.2 [klein] Jewelry Imagery Workflow
description: Jewelry imagery is a source-controlled product workflow: preserve the approved asset, material and geometry evidence, color pipeline, and rights boundary, then release only after visual and factual QA.
category: workflows
tags: [flux, flux2, klein, jewelry, product-photography, compositing, color-management, quality-control]
aliases: ["FLUX Klein Jewelry Photography", "Jewelry Product Imagery"]
---

# FLUX.2 [klein] Jewelry Imagery Workflow

Jewelry imagery is a product-fidelity task, not merely a photorealism task. An
image can look convincing while changing a stone count, prong layout, metal
finish, engraving, logo, or product geometry. Treat the approved asset and
product record as the authority throughout the workflow.

## Source and rights gate

Create a source packet before any generation or edit:

- approved product image/3D asset and a content digest;
- product identifier, approved views, material/stone/finish facts, and
  prohibited claims;
- color reference, capture/rendering space, and any physical-chart receipt;
- rights to use the source, references, marks, and derivative output; and
- a declared allowed-use scope for the final image.

No model output can establish missing product facts or rights. If the product
record is incomplete, route it to review rather than asking a generative model
to fill the gap.

## Choose an evidence-preserving route

Use the least generative route that can satisfy the brief:

1. **Source-preserving cleanup:** remove an allowed background defect or
   presentation artifact while protecting the product mask.
2. **Controlled composite:** place an approved product asset into a separately
   approved scene with declared geometry, contact-shadow, reflection, and
   color constraints.
3. **Reference-guided edit:** when using FLUX.2 image editing, bind the exact
   model/API route and every input reference to the job receipt. The
   [official editing guide](https://docs.bfl.ai/flux_2/flux2_image_editing)
   describes reference-based editing, but the output still requires
   product-fidelity review.
4. **Concept illustration:** label this separately from catalog imagery. It
   must not be used to imply an existing product feature or SKU.

Keep the original asset, mask, prompt/edit instruction, and output connected
in the job record. Never silently flatten an AI-edited product into a new
source of truth.

## Color and material controls

Apply a declared color-management workflow before creative grading. For a
physical capture, a measured chart can support calibration; a learned or
generated color estimate cannot replace that measurement. See
[[color-checker-and-white-balance]].

Review metal hue, gemstone color, edge highlights, specular reflections,
shadow direction, and contact support at the final delivery size. Reject an
image if its material appearance conflicts with the approved product evidence,
even when it is aesthetically stronger.

## Product-fidelity QA

Every candidate needs a human or deterministic comparison against approved
references. Check at least:

- silhouette, proportions, chain/link count, stone count, setting/prong shape,
  engraving, and readable marks;
- metal and gemstone appearance under the declared color pipeline;
- physically plausible support, reflections, occlusion, and shadow direction;
- background, crop, typography, and claims allowed by the brief; and
- model, adapter, prompt/reference, and output provenance.

Record a reason for rejection. Re-running an image with a different seed is
not a correction unless the factual acceptance checks pass.

## Model and license boundary

The [official FLUX.2 repository](https://github.com/black-forest-labs/flux2)
lists FLUX.2 [klein] 9B under non-commercial terms. Do not use those weights
for commercial product imagery without a separate current license decision.
Hosted API terms, third-party adapters, source assets, and product marks each
need their own review.

## Related pages

- [[flux-klein-9b-inference]]
- [[color-checker-and-white-balance]]
- [[perspective-calibration-for-compositing]]
- [[retouch-patch-harmonization]]
