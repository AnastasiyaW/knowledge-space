---
title: ML Plugin Inference UX: Host-State Contract
description: "ML plugin inference UX is an explicit host-and-job-state contract: pin the host API, document snapshot and model versions, cancellation and progress behavior, cache and invalidation keys, preview provenance, non-destructive commit, and measured latency rather than promising universal responsiveness."
category: techniques
tags: [plugin, inference, ux, caching, progress, cancellation, non-destructive, evidence]
aliases: ["ML Plugin Inference UX Patterns", "Inference UX"]
---

# ML Plugin Inference UX: Host-State Contract

An ML operation in a creative host is a job with document, model, and host
state. A spinner, cached result, or preview is trustworthy only when the user
can tell what source snapshot it represents, whether it can be cancelled, and
what will change on commit. Do not promise a universal latency threshold:
measure the exact model, device, document class, cold/warm state, and host
version instead.

## Define observable job states

Use a state model whose transitions are visible and auditable:

`Draft → queued → snapshot verified → preprocessing → inference → preview ready
→ user accepts → atomic non-destructive commit`

Terminal alternatives include `cancelled`, `invalidated`, `failed`, and
`review required`. A document edit, parameter change, model change, permission
change, or source mismatch must invalidate dependent previews rather than
silently applying them later.

For each job record the source digest/composite policy, document and layer
version, color/orientation/selection state, model/checkpoint/runtime version,
parameters, hardware/provider boundary, timestamps, result digest, and
terminal state.

## Respect the host boundary

Host APIs decide how document mutation, history, cancellation, and progress
work. In Photoshop UXP, document-changing commands require
[`executeAsModal`](https://developer.adobe.com/photoshop/uxp/ps_reference), and
the [modal execution API](https://developer.adobe.com/photoshop/uxp/2022/ps-reference/media/executeasmodal)
exposes cancellation and progress reporting. Those facts do not authorize a
plugin to hold a modal scope during remote inference or to apply a result after
the source has changed.

Perform safe preparation before obtaining exclusive mutation access when the
host permits it. Obtain the narrowest documented host transaction only for the
reviewed, explicit commit. Preserve undo/history semantics and leave the
original data intact.

## Cache only attributable intermediates

A cache key should include every input that can change the result: source
pixels or immutable composite digest, dimensions/crop/orientation, color
domain, selected region/mask, preprocessing version, model/checkpoint/runtime,
parameters, and provider policy. Store the output provenance with the cache
entry. A filename, active-document ID, or partial pixel sample is not enough.

Declare ownership, encryption/retention, size budget, eviction, and
invalidation. Never reuse an intermediate across documents or users merely
because it looks similar. Prefetch is optional work: give it a budget,
cancellation path, and explicit local/remote policy; it must not upload source
content or consume a remote quota without authorization.

## Make previews honest

Label a draft, tiled, downsampled, blended, stale, or approximate preview with
the property it lacks. A slider that blends source and output is a display
approximation unless the model was actually evaluated at that setting. Show
the source/result association and provide an explicit refresh when parameters
or source state differ.

Before commit, compare the accepted output with the recorded snapshot and
verify output dimensions, alpha/mask policy, color conversion, protected
regions, and model provenance. If any condition fails, retain the preview as
uncommitted and report the reason.

## Measure the claimed experience

Report cold and warm latency distributions, queue delay, cancellation response,
preview-to-final divergence, cache hit/miss rate, memory pressure, error rate,
and host recovery behavior for the actual release. Test large documents,
rapid parameter changes, undo/redo, source edits while queued, queue
reordering, offline/provider failure, and concurrent host actions.

Do not replace a failure with a different model, cache entry, cloud service,
or stale result. The fallback must be explicitly named, equivalent for the
requested operation, and visible to the user.

## Related pages

- [[tiled-inference]]
- [[low-vram-inference-strategies]]
- [[frequency-decomposition-editing]]
- [[diffusion-lora-training]]
