---
title: FLUX.2 [klein] Identity LoRA: Consent and Evaluation Contract
description: "An identity LoRA is a sensitive, version-bound adapter trained only from authorized images under a defined purpose; bind consent, base checkpoint and adapter format, data and deletion policy, and source-disjoint likeness and preservation review, and never treat a generated identity match as verified identity."
category: techniques
tags: [lora, identity, consent, provenance, flux, klein, evaluation, privacy]
aliases: ["Klein Character LoRA", "Klein Identity LoRA", "Klein Person LoRA"]
---

# FLUX.2 [klein] Identity LoRA: Consent and Evaluation Contract

An identity or character LoRA is not an ordinary style preset. It is a
sensitive adapter that can make a person appear in new contexts. Train or use
one only for an authorized purpose with a clear withdrawal/deletion path and
with review that distinguishes a visual resemblance from verified identity.

## Establish authority before data preparation

Record:

- the depicted person's authorization, allowed purpose, duration, disclosure,
  and revocation contact;
- source-image ownership, acquisition context, and permitted derivative uses;
- retention/deletion policy for originals, captions, crops, masks, adapters,
  checkpoints, previews, and provider copies;
- whether any input leaves the approved environment and the provider's
  applicable data/retention terms; and
- prohibited uses, including identification, authentication, impersonation,
  sensitive-trait inference, or publication without the agreed review.

Do not build an identity dataset from scraped portraits, unverifiable
references, or image embeddings that lack this authority. A trigger word,
caption, face crop, or generated example is not consent.

## Pin model and adapter compatibility

Bind the exact Base checkpoint, runtime, text/image components, adapter
method/configuration, target modules, trainer versions, and inference loader.
BFL's [klein training guide](https://docs.bfl.ai/flux_2/flux2_klein_training)
describes Base variants as fine-tuning starting points, but it does not make a
generic optimizer, image count, rank, caption placement, or “identity”
adapter compatible across every tool and release.

Preserve both adapter weights and configuration. The
[PEFT checkpoint format](https://huggingface.co/docs/peft/developer_guides/checkpoint)
is one example of why a configuration is needed alongside weights. Test the
exact training/inference pair with a non-sensitive approved baseline before
accepting any personal-data run.

## Build an honest evaluation set

Separate training, tuning, and holdout material by original capture, session,
pose/framing, clothing/background, and derivative chain. The evaluation
policy should name what must remain intact and what may change:

- requested context/style/edit;
- likeness judged by authorized reviewers under the stated purpose;
- protected facial/body features, age cues, marks, text, accessories, and
  other regions; and
- failures such as unintended resemblance, sexualization, demeaning context,
  false association, or loss of factual product/background detail.

Do not use an automated similarity score as identification or as the sole
release decision. Do not claim that a generated image proves who a person is,
what they did, or their consent to the output.

## Release and revocation

Keep every approved output traceable to its base, adapter, input policy, and
review receipt. Label AI modification where policy or law requires it. If
authorization expires or is withdrawn, disable new inference, remove the
adapter and derived data according to the agreed deletion policy, and record
the completion without exposing personal material.

If the project cannot meet these controls, do not train an identity adapter;
use a non-identifying character/style workflow or keep the request blocked.

## Related pages

- [[diffusion-lora-training]]
- [[lora-fine-tuning-for-editing-models]]
- [[style-reference-ux]]
- [[flux-klein-9b-architecture]]
