---
title: Ideogram 4
category: projects
tags: [ideogram, ideogram-4, ideogram-4-development, ideogram_4, project]
aliases: ["Ideogram 4"]
---

# Ideogram 4

**Development line:** `project:ideogram-4` · thread `ideogram-4-development`  
**Events:** 2 dated, 2026-06-04 → 2026-07-14 · **Researched:** 2026-09-04 · confidence: medium

## What it is

Ideogram 4 is a structured-JSON image model for designers and developers who need controlled text, composition, and palette. It replaces generic flat-prompt workflows.

- renders literal in-image text and multilingual typography
- places objects and text with normalized bounding boxes
- controls palettes, lighting, style and composition through JSON
- runs through gated quantized weights, the Ideogram API, ComfyUI, and distinct fal speed derivatives

## Development line

- **2026-06-04 — Ideogram 4 source, model variants, and ComfyUI integration were recorded.** Inference code and gated FP8/NF4 weights became public. The release introduced structured JSON control for text, palettes, and bounding-box layout. ComfyUI announced day-zero support.
- **2026-07-14 — Ideogram v4 Instant and Fast variants were recorded.** `ideogram-v4-instant` is an 8-step BF16 pre-QAD checkpoint. `ideogram-v4-fast` is a 20-step FP4/QAD checkpoint. Both are fal-developed from Ideogram’s FP8 base and remove runtime CFG.

## What changed

2026-06-04 — Ideogram 4.0 entered the local workflow. The official release was dated 2026-06-03. Inference code and gated FP8/NF4 weights became public. They provide structured JSON control for text, palettes, and bounding-box layout. ComfyUI announced day-zero support.

2026-07-14 — fal added two separate speed-distilled derivatives rather than a new canonical Ideogram release. `ideogram-v4-instant` is an 8-step BF16 pre-QAD checkpoint. `ideogram-v4-fast` is a 20-step FP4/QAD checkpoint. Both are fal-developed from Ideogram’s FP8 base and remove runtime CFG.

Found today, 2026-09-04 — official documentation still names the canonical endpoint Ideogram 4.0. It accepts either `text_prompt` or `json_prompt`. It supports 1K/2K output and Default/Turbo/Quality speeds. `FLASH` is listed but currently returns HTTP 400. Current licensing separates non-commercial public weights, commercial API use, licensed self-hosting and Enterprise terms.

## How to use this

We evaluate Ideogram 4 through the linked source, model-variant, and ComfyUI paths after 2026-06-04. We separately compare the Instant and Fast variants after 2026-07-14 when selecting an Ideogram 4 route.

1. Choose the deployment and licence lane first. Use the hosted API for commercial generation. Use public quantized weights only for research, evaluation, prototyping or personal work unless you obtain commercial self-hosting rights.
  — <https://ideogram.ai/licensing/>
2. For hosted generation, call `POST /v1/ideogram-v4/generate` with an `Api-Key` and exactly one of `text_prompt` or `json_prompt`. Select 1K or 2K and Default, Turbo or Quality, then download the returned image promptly.
  — <https://developer.ideogram.ai/api-reference/generate-images/generate-v4>
3. Start exploration with `text_prompt`, which enables Magic Prompt. Switch to `json_prompt` when palette, layout or literal text must follow your specification.
  — <https://developer.ideogram.ai/api-reference/generate-images/generate-v4>
4. For controlled designs, construct `high_level_description`, `style_description` and `compositional_deconstruction`. Use typed `text` elements, literal `text` values and normalized `bbox` coordinates where needed.
  — <https://github.com/ideogram-oss/ideogram4/blob/main/docs/prompting.md>
5. For local base-model inference, accept the Hugging Face gate and authenticate with `hf auth login`. Install the official repository, choose the NF4 or FP8 checkpoint, and run the supplied inference entry point.
  — <https://github.com/ideogram-oss/ideogram4>
6. For a node workflow, use ComfyUI’s Ideogram 4 support and its JSON prompt structure rather than flattening layout into a prose prompt.
  — <https://blog.comfy.org/p/ideogram-4-day-0-support-in-comfyui>
7. For an explicitly latency-oriented fal route, configure `FAL_KEY` server-side and call `ideogram/v4/instant`. Keep its results identified as a fal derivative rather than base Ideogram 4.0 output.
  — <https://fal.ai/models/ideogram/v4/instant/api>

## Best practices

- For exact rendered copy, put literal text in a JSON `text` element or quote it in prose. Keep each string to roughly 5–7 words and prefer words to small numeric symbols.
  — <https://ideogram.ai/blog/ideogram-4-json-prompting/>
- Preserve the required JSON key order, use uppercase `#RRGGBB` palette values, and run the CaptionVerifier before committing a local prompt recipe.
  — <https://github.com/ideogram-oss/ideogram4/blob/main/docs/prompting.md>
- Keep a composition to five or fewer elements. Treat bounding boxes as guides with margin rather than crops, and describe floor or ground as `background`.
  — <https://ideogram.ai/blog/ideogram-4-json-prompting/>
- Use `V4_QUALITY_48` for final local renders. Compare the 20-step Default and 12-step Turbo presets against your own acceptance images before trading quality for speed.
  — <https://github.com/ideogram-oss/ideogram4/blob/main/docs/inference.md>
- Do not deploy the public checkpoints commercially by assumption. The current terms reserve that for the hosted API or a self-serve/Enterprise licence.
  — <https://ideogram.ai/licensing/>
- Keep base-model and fal-derivative outputs in separate evaluation sets. Instant is a fal-developed 8-step, single-branch derivative, not a checkpoint-identical base-model run.
  — <https://huggingface.co/fal/ideogram-v4-instant>

## Superseded by this

- 2026-06-03/04 — Guidance that Ideogram must be used only as a closed hosted service is obsolete for research and prototyping. Official inference code and gated public quantized weights made local use possible. This does not grant commercial self-hosting rights.
- 2026-06-18 — Flat, adjective-heavy prompt recipes are no longer the precision default for Ideogram 4. Structured JSON is the preferred route for typography, palette and layout control.
- 2026-07-14 — Treating fal Instant or Fast as a canonical Ideogram 4.1-style successor is obsolete. They are fal speed-distilled derivatives, not a replacement for the base 4.0 checkpoint.

## Still unknown

- The two dated entries refer to one base Ideogram family. The July items are fal-authored speed derivatives rather than an official Ideogram core-model release.
- No reviewed source provides an independent evaluation showing that the fal 8-step or 20-step variants preserve base 4.0 typography and layout fidelity for production workloads.
- The reviewed public official pages do not identify a versioned Ideogram 4.1 or later base checkpoint. Absence from those pages does not prove that no private or unannounced revision exists.

## Sources

| source | title | read |
|---|---|---|
| https://ideogram.ai/news/ideogram-4.0/ | Ideogram 4.0 Press Release | Ideogram | 2026-09-04 |
| https://ideogram.ai/blog/ideogram-4.0/ | Ideogram 4.0 Technical Details: Open model at the forefront of design | 2026-09-04 |
| https://github.com/ideogram-oss/ideogram4 | GitHub - ideogram-oss/ideogram4: Ideogram 4: Open image model at the forefront of design | 2026-09-04 |
| https://huggingface.co/ideogram-ai/ideogram-4-nf4 | ideogram-ai/ideogram-4-nf4 · Hugging Face | 2026-09-04 |
| https://blog.comfy.org/p/ideogram-4-day-0-support-in-comfyui | Ideogram 4.0 Day-0 Support in ComfyUI: Open Weights and Structured Control | 2026-09-04 |
| https://huggingface.co/fal/ideogram-v4-instant | fal/ideogram-v4-instant · Hugging Face | 2026-09-04 |
| https://huggingface.co/fal/ideogram-v4-fast | fal/ideogram-v4-fast · Hugging Face | 2026-09-04 |
| https://developer.ideogram.ai/api-reference/generate-images/generate-v4 | Generate with Ideogram 4.0 | Ideogram | Documentation | 2026-09-04 |
| https://ideogram.ai/blog/ideogram-4-json-prompting/ | How to JSON prompt for Ideogram 4.0 | 2026-09-04 |
| https://ideogram.ai/licensing/ | Licensing | Ideogram | 2026-09-04 |
| https://github.com/ideogram-oss/ideogram4/blob/main/docs/prompting.md | ideogram4/docs/prompting.md at main · ideogram-oss/ideogram4 · GitHub | 2026-09-04 |
| https://github.com/ideogram-oss/ideogram4/blob/main/docs/inference.md | ideogram4/docs/inference.md at main · ideogram-oss/ideogram4 · GitHub | 2026-09-04 |
| https://fal.ai/models/ideogram/v4/instant/api | V4.0q [instant] Text to Image API Docs | fal | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:ideogram-4`, thread `ideogram-4-development`, 2 dated events 2026-06-04 → 2026-07-14.
- **Practical note:** Evaluate Ideogram 4 through the linked source, model-variant, and ComfyUI paths after 2026-06-04. Separately compare the Instant and Fast variants after 2026-07-14 when selecting an Ideogram 4 route.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
