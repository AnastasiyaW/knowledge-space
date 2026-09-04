---
title: Skin Retouching: Consent-Aware Correction Workflow
description: Skin retouching is a consent-aware, scope-limited correction workflow; preserve identity, texture, and protected traits, keep every mask and edit auditable, and require review of all changed skin.
category: workflows
tags: [skin-retouch, inpainting, consent, privacy, masks, texture-preservation, quality-control]
aliases: ["Skin Retouch Pipeline", "Blemish Correction Workflow"]
---

# Skin Retouching: Consent-Aware Correction Workflow

Skin retouching should correct a specifically approved visual issue without
silently changing identity, age presentation, complexion, body characteristics,
or health-related appearance. It is not a general “beautify” operation and
must never be used to infer or classify medical or sensitive personal traits.

## Intake and consent

For each source image, retain the image digest, authority to edit, approved
purpose, requested correction scope, access/retention policy, and any
prohibited changes. Treat portraits as sensitive material even when the
intended edit is cosmetic.

Describe requests in bounded visual terms, such as a temporary visible
artifact in a named region. If a request is ambiguous, potentially medical, or
changes protected appearance, route it to human review rather than automated
retouch.

## Mask-first workflow

1. Create or review a mask for the approved issue.
2. Mark protected regions, including eyes, lips, hairline, facial contours,
   tattoos, jewelry, and any content the request says to preserve.
3. Select the least generative correction that can satisfy the mask.
4. Keep the original, mask, operation parameters, and edited result together.
5. Review every changed region at delivery resolution and beside the source.

Automatic detection or segmentation can propose masks but cannot decide which
skin feature should be altered. Never allow a detector confidence score to
replace consent, intent, or a human acceptance decision.

## Texture and identity preservation

Use a representative validation set to check pore/texture continuity, edge
transitions, lighting, color, and facial geometry. A blurred or overly smooth
area is a failure even if the requested artifact disappeared. When an
inpainting model is used, distinguish its generated area from observed source
detail and reject outputs that change identity, protected traits, or adjacent
objects.

For a larger edit or an edit model, validate the requested correction
separately from preservation; see [[face-beautify-edit-lora]]. For background
or object cleanup around a person, use the constrained mask contract in
[[object-removal-inpainting]].

## Release record

An approved retouch needs the source/output digests, mask version, model or
tool revision, instruction, reviewer, scope decision, and a reversible
delivery path. Do not replace the original asset with an edited image without
retaining both.

## Related pages

- [[face-beautify-edit-lora]]
- [[object-removal-inpainting]]
- [[face-detection-filtering-pipeline]]
- [[retouch-patch-harmonization]]
