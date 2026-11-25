---
title: FLUX.1-Kontext-dev-onnx — FLUX.1 Kontext ONNX and editing
category: projects
date: 2025-07-03
tags: [black-forest-labs, black_forest_labs, flux-kontext, flux_kontext, project]
aliases: ["FLUX.1-Kontext-dev-onnx", "Kontext Komposer"]
---

# FLUX.1-Kontext-dev-onnx — FLUX.1 Kontext ONNX and editing

**Development line:** `project:black-forest-labs` · thread `flux-kontext`  
**Last event:** 2025-07-03 · 1 dated since 2025-07-03 · **Researched:** 2026-09-04 · confidence: medium

## What it is

FLUX.1-Kontext-dev-onnx is the ONNX export of FLUX.1 Kontext [dev] for local runtimes.

- Image editing from text instructions.
- Local and global modifications with character or style preservation across iterative work.
- Model exports in BF16, FP8, and FP4 (SVDQuant).

## Development line

- **2025-07-03 — Black Forest Labs published the FLUX.1 Kontext dev ONNX repository.** The official release surfaced BF16, FP8, and FP4 (SVDQuant) exports for the public Kontext [dev] base model. This is a packaging format for existing weights, not a new base-model release.

## What changed

2025-07-03 — FLUX.1-Kontext-dev-onnx: Black Forest Labs provided BF16, FP8, and FP4 (SVDQuant) exports for the public Kontext [dev] model. This is a runtime packaging option rather than a new base-model release.

2025-07-11 — BFL Playground and Kontext Komposer presets: the web editor added text-guided editing without code, and a community post documented prompt presets. Neither source introduced ONNX weights, an API, or a model revision.

Found today (2026-09-04) — BFL keeps Kontext available as a previous-generation tool. Outputs stay at 1MP. BFL recommends FLUX.2 for new work needing up to 4MP output, multi-reference edits, or tighter control.

## How to use this

From 2025-07-03, start evaluation with the ONNX repository. Verify model revisions and runtime support before integrating.

1. Open the official ONNX repository, sign in, and accept the gated FLUX.1 [dev] Non-Commercial License before downloading files.
  — <https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev-onnx>
2. Choose BF16, FP8, or FP4 (SVDQuant) for a supported runtime. The card provides no model-specific code snippet, so verify support before using a generic Diffusion Single File workflow.
  — <https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev-onnx>
3. Use canonical Kontext [dev] weights when ONNX is unnecessary. Install Diffusers, load the pipeline, then pass an input image and edit prompt.
  — <https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev/tree/main>
4. For hosted evaluation, open the original Playground edit route and sign in. When checked today, it redirects through BFL authentication to the dashboard Playground.
  — <https://playground.bfl.ai/image/edit>
5. Choose FLUX.2 instead of starting a new Kontext integration when a production project needs more than 1MP output or multiple references.
  — <https://help.bfl.ai/articles/5186006235-what-is-flux-1-kontext>

## Best practices

- Write one explicit visual change at a time, such as “Change the car color to red,” then inspect the result before the next edit.
  — <https://docs.bfl.ai/kontext/kontext_image_editing>
- Quote both source and replacement text for in-image text edits. Use bright annotation boxes when a text edit needs targeted repositioning or resizing.
  — <https://docs.bfl.ai/kontext/kontext_image_editing>
- Keep edit chains short and save good intermediate outputs. BFL documents visible degradation after six iterative edits, so restart from a clean image instead of endlessly continuing one chain.
  — <https://bfl.ai/blog/flux-1-kontext>
- Treat dev weights as non-commercial and non-production by default. Deploy filtering or manual review, and satisfy applicable provenance requirements.
  — <https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev-onnx>
- Community practice: build presets as editable prompt templates that preserve the subject while altering context, scene, style, clothing, or background. These are not official model controls.
  — <https://www.reddit.com/r/StableDiffusion/comments/1lx8lot/kontext_presets_all_system_prompts/>

## Superseded by this

- 2025-05-29 private-beta email access ended with the 2025-06-26 public open-weight release. Access now runs through the gated Hugging Face license flow.
- 2025-07-11 guidance describing the Playground edit URL as an unauthenticated entry point is stale. As observed on 2026-09-04, it redirects through BFL authentication to the dashboard.
- 2025-era guidance to build new high-resolution or multi-reference editing on Kontext is superseded by BFL's recommendation to use FLUX.2. Kontext remains available; it is not removed.

## Still unknown

- The 2025-07-03 ONNX artifact and the 2025-07-11 browser and preset materials share the Kontext family name but are not proven to be one product. The first is a local distribution; the second covers a hosted editor and a community prompt layer.
- Kontext Komposer appears in community posts as a preset label, such as “Komposer: Teleport”. No first-party source establishes it as an official BFL product, version, or component of the ONNX repository.
- The official ONNX model card provides no end-to-end runtime example. We must provide a compatible custom ONNX pipeline or use the documented Diffusers route.
- The original dated source text is unavailable, so we cannot reconstruct its exact claims, BFL endorsement status, or export revisions from the links alone.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev-onnx | black-forest-labs/FLUX.1-Kontext-dev-onnx · Hugging Face | 2026-09-04 |
| https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev/tree/main | black-forest-labs/FLUX.1-Kontext-dev at main · Hugging Face | 2026-09-04 |
| https://bfl.ai/blog/flux-1-kontext-dev | FLUX.1 Kontext [dev] - Open Weights for Image Editing | Black Forest Labs | 2026-09-04 |
| https://bfl.ai/blog/flux-1-kontext | Introducing FLUX.1 Kontext and the BFL Playground | Black Forest Labs | 2026-09-04 |
| https://docs.bfl.ai/kontext/kontext_image_editing | Image Editing | Black Forest Labs | 2026-09-04 |
| https://help.bfl.ai/articles/5186006235-what-is-flux-1-kontext | What is FLUX.1 Kontext? | Black Forest Labs Knowledge Base | 2026-09-04 |
| https://playground.bfl.ai/image/edit | Black Forest Labs - Frontier AI Lab | 2026-09-04 |
| https://www.reddit.com/r/StableDiffusion/comments/1lx8lot/kontext_presets_all_system_prompts/ | Kontext Presets - All System Prompts : r/StableDiffusion | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:black-forest-labs`, thread `flux-kontext`, 1 dated events 2025-07-03 → 2025-07-03.
- **Practical note:** From 2025-07-03, practitioners evaluating this line should start with the linked ONNX repository as its deployment artifact and separately verify the model revision and runtime support before integration.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
