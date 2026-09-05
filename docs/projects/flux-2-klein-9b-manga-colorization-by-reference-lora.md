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

FLUX.2 Klein 9B Manga Colorization LoRA is an adapter for artists and ComfyUI or Diffusers users who transfer character palettes from a color reference onto line art or grayscale panels.

- Hair, eye, clothing, and skin colors: matches them across panels.
- Multiple characters: supports several on a single reference.
- Lighting and background: accepts short text prompts for adjustments.

## Development line

- **2026-06-10 — Hugging Face model reference recorded for the project.** On 2026-06-10, we linked the project to the Hugging Face model page for FLUX.2 Klein 9B manga colorization LoRA by reference. Technical details and release status remain unverified.

## What changed

- **2026-06-10** — The initial Apache-2.0 repository was published for FLUX.2 Klein 9B Base with trigger `mngclranm`.
- **2026-07-05** — A third-party ComfyUI workflow demonstrated batch colorization for page folders using a separate color reference. This was a community integration, not a new LoRA version.

## How to use this

As of 2026-06-10, treat the linked Hugging Face LoRA as candidate reference material. Check capabilities, compatibility, licensing, and usage instructions before adopting it.

1. Load `black-forest-labs/FLUX.2-klein-base-9B`, then attach adapter weights with `load_lora_weights` or Load LoRA in ComfyUI.
  — <https://huggingface.co/thedeoxen/FLUX.2-klein-9B-manga-colorization-by-reference-LORA>
2. Pass the black-and-white page as the target image and a separate color character sheet, cover, or splash page as the reference.
  — <https://huggingface.co/thedeoxen/FLUX.2-klein-9B-manga-colorization-by-reference-LORA>
3. Add `mngclranm` to the prompt; add notes for lighting, mood, or background tint if needed.
  — <https://huggingface.co/thedeoxen/FLUX.2-klein-9B-manga-colorization-by-reference-LORA>
4. Start with a LoRA weight of 0.8–1.0; lower it if color transfer becomes excessive.
  — <https://huggingface.co/thedeoxen/FLUX.2-klein-9B-manga-colorization-by-reference-LORA>

## Best practices

- Pick a clean reference where the required characters are distinct. A cover or character sheet works for multiple characters.
  — <https://huggingface.co/thedeoxen/FLUX.2-klein-9B-manga-colorization-by-reference-LORA>
- Change the seed first if character colors bleed together. If that fails, clean the reference image or split the page into smaller panels.
  — <https://www.reddit.com/r/comfyui/comments/1uo52jb/comfyui_manga_colorization_with_color_reference/>
- Keep the target page noticeably larger than the reference in ComfyUI. Tests showed about 1.5 MP against 0.5 MP reduced reference composition leakage.
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