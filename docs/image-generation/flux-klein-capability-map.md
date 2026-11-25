---
title: FLUX.2 [klein] Capability Map: Attested Operation Contract
description: "A FLUX.2 [klein] capability is usable only when the exact variant, checkpoint, license, runtime or provider endpoint, input contract, and output review are attested at execution time; family-level generation and editing support does not authorize every adapter, service, commercial use, or editing result."
category: reference
tags: [flux, klein, capabilities, operations, licensing, adapters, provenance]
aliases: ["Klein Operations Map", "Klein Capability Map"]
---

# FLUX.2 [klein] Capability Map: Attested Operation Contract

Capability maps age quickly. A family announcement, a community adapter, or an
old provider endpoint cannot prove what is available, licensed, compatible, or
safe in a current job. Treat an operation as usable only after attesting the
exact release and execution path.

## Family support is not an operation receipt

The [official FLUX.2 repository](https://github.com/black-forest-labs/flux2)
states that the [klein] family supports text-to-image, single-reference image
editing, and multi-reference image editing. It also names 4B, 9B, 9B KV, and
Base releases with different stated purposes and licenses.

Those are family-level capabilities. They do not establish that:

- a particular LoRA, node, checkpoint conversion, quantization, or community
  workflow loads on the chosen variant;
- a hosted provider still exposes the same endpoint, input schema, price,
  retention policy, or commercial right;
- a reference image may be submitted to that provider; or
- a generated edit correctly removed, preserved, moved, relit, or identified
  a real subject.

## Attest the operation at execution time

For every job, store:

| Contract area | Required receipt |
|---|---|
| Model | exact variant, checkpoint digest, components, source, and license notice |
| Runtime | local code/node or provider endpoint revision, input/output schema, and error behavior |
| Adapter | adapter weights plus configuration, declared target base, loader test, author/source, and license |
| Inputs | asset authority, reference-image consent, preprocessing, masks/regions, and third-party disclosure |
| Policy | allowed purpose, commercial/distribution status, output provenance, and reviewer authority |
| Evidence | request/configuration digest, output digest, model/runtime receipt, and task-specific review |

The BFL [model overview](https://bfl.ai/models/flux-2-klein) publishes
current variant-specific information, including a release's described purpose.
The model card or provider documentation current at execution time remains the
source of truth; do not freeze volatile VRAM, speed, scale, endpoint, or
pricing tables into an operational promise.

## Adapter and provider boundary

Adapters are not native capabilities. Before use, verify exact base
compatibility, adapter format/configuration, target modules, license, and
load/output behavior. Community labels such as “remove,” “relight,”
“consistency,” or “character” describe an intended effect, not an approved
authority to alter protected content.

For a remote service, record the exact endpoint, region/retention terms,
request schema, response schema, commercial terms, and provider-visible
inputs. If any of these cannot be attested, keep the operation unavailable
instead of silently falling back to another model, endpoint, or local node.

## Review the output, not the label

Text-to-image, reference editing, and adapters can create plausible content.
They do not recover absent facts or prove an unchanged identity. Review the
declared protected regions, text, geometry, material/color evidence, and
rights before publishing. Treat uncertain outputs as proposals with visible
provenance, not as source-faithful results.

## Related pages

- [[flux-klein-9b-architecture]]
- [[flux-klein-9b-inference]]
- [[flux-klein-character-lora]]
- [[style-reference-ux]]
