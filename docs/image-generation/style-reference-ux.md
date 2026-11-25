---
title: Style Reference UX: Authority, Strength, and Provenance
description: Style-reference UX must separate temporary influence from saved training, style from content/structure, and local data from third-party processing, while making strength and provenance visible to the user.
category: systems
tags: [style-reference, ux, provenance, privacy, lora, content-reference, strength-control]
aliases: ["Style Reference UX", "Style Reference Workflow"]
---

# Style Reference UX: Authority, Strength, and Provenance

A style-reference control changes visual output, but users need to understand
what it may borrow, what it will preserve, where their reference is sent, and
whether the choice is temporary or creates a reusable trained asset. Those
facts are product requirements, not optional help text.

## Separate the user’s intents

Expose distinct controls for:

- **style:** palette, texture, mood, medium, and visual language;
- **content:** subject, object identity, product geometry, and scene facts;
- **structure:** pose, layout, camera/framing, or spatial constraints; and
- **preservation:** reference features that an edit must leave unchanged.

Do not present these as one vague “reference strength” dial. If a workflow
cannot technically separate them, say so and show the expected conflict rather
than implying that all reference properties will be preserved.

## Temporary versus durable choices

Offer two clearly labelled paths:

1. **Session reference:** applied only to the current job and removable with
   the job record.
2. **Saved style or trained adapter:** a durable asset with a name, owner,
   source/provenance, model binding, retention policy, and deletion path.

A saved style must never be created implicitly from an upload. Training,
sharing, or reuse needs a separate affirmative action and a visible statement
of what data will be retained.

## Strength controls that communicate risk

Use a reversible strength control with plain-language effects and a preview
that compares against the no-reference baseline. The UI should show when
increasing style influence also weakens content/structure preservation. Avoid
pretending that numeric weights are comparable across different models,
adapters, or image references.

For complex requests, provide an explicit conflict summary before generation:
which source controls color, which controls composition, which controls object
facts, and which has priority when they disagree.

## Data and provider boundary

Before accepting a reference, disclose whether it remains local or is sent to
a captioning, embedding, generation, or training provider. Record the
provider, model/revision, retention/access terms, and user authority in the
job receipt. Sensitive portraits, products under NDA, and third-party artwork
need an explicit allowed-use decision.

## Acceptance and reuse

Show a source panel with thumbnails/digests, model and adapter binding,
reference scope, prompt, output, and feedback. User ratings are useful
preference signals, but they do not prove rights, factual product accuracy, or
identity preservation. A reusable adapter must follow the release contract in
[[flux-klein-style-lora-system]].

## Related pages

- [[flux-klein-style-lora-system]]
- [[megastyle-flux-style-transfer]]
- [[flux-klein-jewelry-photography]]
- [[face-beautify-edit-lora]]
