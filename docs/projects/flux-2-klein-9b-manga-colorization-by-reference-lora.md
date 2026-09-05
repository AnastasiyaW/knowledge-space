---
title: FLUX.2 Klein 9B Manga Colorization LoRA — Manga Colorization by Reference LoRA
category: projects
date: 2026-06-10
tags: [flux-2-klein-9b-manga-colorization-by-reference-lora, flux-lora, manga-colorization-by-reference-lora, project]
aliases: ["FLUX.2 Klein 9B Manga Colorization LoRA"]
---

# FLUX.2 Klein 9B Manga Colorization LoRA — Manga Colorization by Reference LoRA

**Development line:** `project:flux-2-klein-9b-manga-colorization-by-reference-lora` · thread `manga-colorization-by-reference-lora`  
**Last event:** 2026-06-10 · 1 dated since 2026-06-10 · **Researched:** 2026-09-05 · confidence: high

## What it is

FLUX.2 Klein 9B Manga Colorization LoRA is a LoRA adapter for artists and ComfyUI or Diffusers users who transfer character palettes from a color reference onto line art or grayscale panels.

- Palette matching for hair, eye, clothing, and skin tones.
- Multi-character support on a single reference image.
- Prompt guidance for lighting and background tweaks.

## Development line

- **2026-06-10 — Hugging Face model reference recorded for the project.** We recorded the Hugging Face model repository for the FLUX.2 Klein 9B manga colorization by reference LoRA on 2026-06-10.

## What changed

2026-06-10 — The initial Apache-2.0 adapter repository was published for FLUX.2 Klein 9B Base; it sets trigger `mngclranm` and specifies the base model. 2026-07-05 — A third-party ComfyUI workflow showed batch colorization for a folder of pages against a separate color reference; this is a community integration, not a new LoRA version.

## How to use this

As of 2026-06-10, treat the linked Hugging Face LoRA as a reference workflow. Verify its capabilities, compatibility, licensing, and usage instructions before adoption.

1. Load `black-forest-labs/FLUX.2-klein-base-9B`, then connect the adapter weights with `load_lora_weights` or Load LoRA in ComfyUI.
  — <https://huggingface.co/thedeoxen/FLUX.2-klein-9B-manga-colorization-by-reference-LORA>
2. Provide the black-and-white page as the target image and a separate colored character sheet, cover, or splash page as the reference.
  — <https://huggingface.co/thedeoxen/FLUX.2-klein-9B-manga-colorization-by-reference-LORA>
3. Add `mngclranm` to the prompt; add lighting, mood, or background notes if needed.
  — <https://huggingface.co/thedeoxen/FLUX.2-klein-9B-manga-colorization-by-reference-LORA>
4. Start with a LoRA weight of 0.8–1.0; reduce it if color transfer becomes excessive.
  — <https://huggingface.co/thedeoxen/FLUX.2-klein-9B-manga-colorization-by-reference-LORA>

## Best practices

- Pick a clean reference where page characters are clearly visible; a cover or character sheet works for multiple figures.
  — <https://huggingface.co/thedeoxen/FLUX.2-klein-9B-manga-colorization-by-reference-LORA>
- If character colors blend, change the seed first; then clean the reference or split the page into smaller panels.
  — <https://www.reddit.com/r/comfyui/comments/1uo52jb/comfyui_manga_colorization_with_color_reference/>
- In ComfyUI, keep the target page larger than the reference: running about 1.5 MP against 0.5 MP reduced reference composition bleed in shared tests.
  — <https://www.reddit.com/r/comfyui/comments/1uo52jb/comfyui_manga_colorization_with_color_reference/>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The repository card describes a two-image reference workflow, but its generic Diffusers widget example shows only one input image; the exact public Diffusers call for supplying the second color-reference image is not documented there.
- No first-party changelog or later model revision was found after the initial 2026-06-10 commit; the 2026-07-05 item is community workflow evidence, not a LoRA release.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/thedeoxen/FLUX.2-klein-9B-manga-colorization-by-reference-LORA | thedeoxen/FLUX.2-klein-9B-manga-colorization-by-reference-LORA | 2026-09-05 |
| https://huggingface.co/thedeoxen/FLUX.2-klein-9B-manga-colorization-by-reference-LORA/commit/78d5314569e7fdc7fb14dabde2281fd82db61304 | initial commit · thedeoxen/FLUX.2-klein-9B-manga-colorization-by-reference-LORA at 78d5314 | 2026-09-05 |
| https://docs.bfl.ai/flux_2/flux2_klein_training | FLUX.2 [klein] Training — Black Forest Labs | 2026-09-05 |
| https://www.reddit.com/r/comfyui/comments/1uo52jb/comfyui_manga_colorization_with_color_reference/ | [ComfyUI] Manga Colorization with Color Reference | One-Click Batch Processing | Fast & Consistent Results | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:flux-2-klein-9b-manga-colorization-by-reference-lora`, thread `manga-colorization-by-reference-lora`, 1 dated events 2026-06-10 → 2026-06-10.
- **Practical note:** As of 2026-06-10, practitioners should treat the linked Hugging Face LoRA as a candidate reference for manga colorization workflows, while independently verifying its capabilities, compatibility, licensing, and usage instructions before adoption.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
