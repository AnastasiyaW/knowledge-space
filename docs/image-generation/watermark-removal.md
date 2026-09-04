---
title: "Visible Watermark Restoration: Authorized-Asset Contract"
description: "Visible-watermark restoration is permitted only for assets the operator is authorized to modify; bind ownership or written authorization, source asset and overlay type, detection/mask and restoration releases, protected regions and provenance handling, output disclosure, and human review, and never treat a plausible reconstruction as recovered original content."
category: techniques
tags: [watermark, restoration, authorized-assets, provenance, inpainting, review]
aliases: ["Visible Watermark Detection and Removal", "Authorized Watermark Restoration"]
---

# Visible Watermark Restoration: Authorized-Asset Contract

This page concerns restoration of a visible overlay only when the operator
owns the asset or has explicit authority to modify it: for example, correcting
an accidental overlay on an in-house export or preparing an authorized
derivative. The [AAAI visible-watermark research](https://ojs.aaai.org/index.php/AAAI/article/view/28080)
describes separation of overlay localization from background restoration; a
restored area remains a reconstruction, not recovered evidence of what was
originally hidden.

Do not use this workflow to remove marks from third-party previews, licensed
stock, platform-delivered media, or any asset whose terms prohibit alteration.
It also does not cover evading invisible watermarks or deleting provenance
controls. [C2PA Content Credentials](https://spec.c2pa.org/specifications/)
are a separate provenance system and require their own policy-aware handling.

## Establish authorization and scope

Before processing, retain:

- source-asset digest, owner, license/contract or written authorization,
  authorized purpose, destination, retention/deletion policy, and reviewer;
- overlay classification and placement record: own export mark, approved
  publisher mark, accidental compositing artifact, or another explicitly
  permitted case;
- an explicit protected-region list for people, identity, text, products,
  safety labels, factual records, legal notices, and content that must not be
  reconstructed or changed; and
- a refusal record for unknown-origin assets, third-party previews, or any
  request that would remove ownership/provenance evidence without authority.

Permission to view, download, or edit a copy is not permission to remove a
visible ownership mark. When authority is unclear, obtain it or use the
original clean asset instead.

## Bind restoration and disclosure

For each authorized attempt, record the detector/mask source and revision,
mask coordinate system and reviewer correction, restoration model or tool
release, input preprocessing, output artifact digest, and every transformed
region. Preserve the original asset and mask with the result. Do not present
a generated fill as recovered pixels, an authentic product record, or an
unchanged original.

Evaluate mask coverage separately from restoration quality. Inspect boundaries,
semi-transparent overlay edges, text, repeated patterns, fine factual detail,
lighting, reflection, and surrounding geometry. If training is involved, keep
source assets and derivatives group-disjoint across train, validation, and
review sets, and evaluate on authorized held-out data.

Publish only after a reviewer confirms the authorization, protected-region
handling, output disclosure, and intended use. Record whether provenance
metadata or Content Credentials must be retained, regenerated, or marked
invalid under the applicable asset policy; this is not generic metadata
cleanup.

## Gotchas

- **Issue:** A licensed preview is treated as an editable source because it is
  publicly visible -> **Fix:** require the original asset or explicit written
  authority before any restoration attempt.
- **Issue:** A plausible fill is represented as recovered original content ->
  **Fix:** label it as a restoration/reconstruction, retain the source and
  mask, and prohibit factual or evidentiary use without independent support.
- **Issue:** Overlay removal changes provenance expectations while only pixels
  are reviewed -> **Fix:** review the applicable provenance/Content
  Credentials policy and preserve a visible transformation record.

## Failure boundary

If ownership/authorization, source provenance, allowed overlay scope,
protected-region review, restoration release, or final disclosure is missing,
do not process or publish the result. Escalate to the asset owner or request a
clean authorized source; do not silently erase, crop around, or bypass the
mark.

## Related pages

- [[object-removal-inpainting]]
- [[LaMa]]
- [[in-context-segmentation]]
- [[paired-training-for-restoration]]
- [[segmentation-dataset-preparation]]
