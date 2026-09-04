---
title: FLUX.1-Kontext-dev-onnx — FLUX.1 Kontext ONNX and editing
category: projects
tags: [black-forest-labs, black_forest_labs, flux-kontext, flux_kontext, project]
aliases: ["FLUX.1-Kontext-dev-onnx", "Kontext Komposer"]
---

# FLUX.1-Kontext-dev-onnx — FLUX.1 Kontext ONNX and editing

**Development line:** `project:black-forest-labs` · thread `flux-kontext`  
**Events:** 1 dated, 2025-07-03 → 2025-07-03 · **Researched:** 2026-09-04 · confidence: medium

## What it is

FLUX.1-Kontext-dev-onnx is the ONNX distribution of FLUX.1 Kontext [dev] for builders with an existing compatible local runtime. - edits an input image from a text instruction; - supports local and global changes, iterative work, and character or style preservation; - provides BF16, FP8, and FP4 (SVDQuant) exports. 12B parameters; downloads require accepting the FLUX.1 [dev] Non-Commercial License, and the Kontext family is fixed at 1MP. Verdict: use it only when ONNX is a hard deployment requirement; the official card has no model-specific runtime recipe, and BFL recommends FLUX.2 for new high-resolution or multi-reference work.

## Development line

- **2025-07-03 — FLUX.1 Kontext dev ONNX repository entered the development record.** On 2025-07-03, a Hugging Face repository for FLUX.1-Kontext-dev-onnx was recorded under Black Forest Labs. The link establishes an ONNX-oriented distribution artifact for the project, a material deployment path distinct from a general editing interface.

## What changed

2025-07-03 — FLUX.1-Kontext-dev-onnx: the official ONNX distribution route surfaced BF16, FP8, and FP4 (SVDQuant) exports for the already public Kontext [dev] base model. This is a packaging/runtime route, not evidence of a separate base-model release that day. 2025-07-11 — BFL Playground and Kontext Komposer presets: the browser editor offered a no-code way to try text-guided edits, while the community post documented prompt-generator presets. Neither source documents an ONNX weight, API, or model revision. Found today (2026-09-04) — BFL still keeps the Kontext family available, but calls it previous-generation: outputs are fixed at 1MP and FLUX.2 is the recommended route for new work needing up to 4MP output, multi-reference editing, or more control.

## How to use this

From 2025-07-03, practitioners evaluating this line should start with the linked ONNX repository as its deployment artifact and separately verify the model revision and runtime support before integration.

1. Open the official ONNX repository, sign in, and accept the gated FLUX.1 [dev] Non-Commercial License before downloading files.
  — <https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev-onnx>
2. Choose BF16, FP8, or FP4 (SVDQuant) for a runtime that already supports this export. The card provides no model-specific code snippet, so do not assume the files are plug-and-play in a generic Diffusion Single File workflow.
  — <https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev-onnx>
3. If ONNX is not required, use BFL’s documented local route for the canonical Kontext [dev] weights: install Diffusers, load the pipeline, then pass an input image and edit prompt. This changes the deployment format, not the editing task.
  — <https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev/tree/main>
4. For a hosted evaluation, open the original Playground edit route and sign in; when checked today, it redirects through BFL authentication to the dashboard Playground.
  — <https://playground.bfl.ai/image/edit>
5. For a new production project that needs more than 1MP output or multiple references, choose FLUX.2 instead of beginning a new Kontext integration.
  — <https://help.bfl.ai/articles/5186006235-what-is-flux-1-kontext>

## Best practices

- Write one explicit visual change at a time, such as “Change the car color to red,” then inspect the result before the next edit.
  — <https://docs.bfl.ai/kontext/kontext_image_editing>
- For text inside an image, quote both the source and replacement text; use bright annotation boxes when a text edit also needs targeted repositioning or resizing.
  — <https://docs.bfl.ai/kontext/kontext_image_editing>
- Keep edit chains short and checkpoint good outputs. BFL documents visible degradation after six iterative edits, so branch from a clean image instead of endlessly continuing one chain.
  — <https://bfl.ai/blog/flux-1-kontext>
- Treat the dev weights as non-commercial and non-production by default; deploy filtering or manual review and meet applicable provenance requirements.
  — <https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev-onnx>
- Community practice: make a preset an editable prompt template that explicitly preserves the subject while changing only the requested context, scene, style, clothing, or background. It is not an official model control.
  — <https://www.reddit.com/r/StableDiffusion/comments/1lx8lot/kontext_presets_all_system_prompts/>

## Superseded by this

- 2025-05-29 private-beta access by emailing BFL is obsolete after the 2025-06-26 public open-weight release; access is now through the gated Hugging Face license flow.
- 2025-07-11 guidance that the direct Playground edit URL is an unauthenticated entry point is stale: observed on 2026-09-04, it redirects through BFL authentication to the dashboard.
- 2025-era guidance to start a new high-resolution or multi-reference image-editing build on Kontext is superseded by BFL’s current recommendation to start with FLUX.2. Kontext remains available; it is not removed.

## Still unknown

- The 2025-07-03 ONNX artifact and the 2025-07-11 browser/preset material are related by the Kontext family but are not proven to be one product: the first is a local model distribution, the second covers a hosted editor and community prompt layer.
- Kontext Komposer appears in the community post as a preset label, such as “Komposer: Teleport”; no first-party source establishes it as an official BFL product, version, or component of the ONNX repository.
- The official ONNX model card still has no end-to-end, model-specific runtime example. A compatible custom ONNX pipeline is therefore required, or the documented non-ONNX Diffusers route should be used.
- The original dated source text is unavailable, so its exact claim, BFL endorsement status, and whether it announced a new export revision cannot be reconstructed from the links alone.

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
