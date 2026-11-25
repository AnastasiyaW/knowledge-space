---
title: "FLUX.2"
category: "projects"
date: 2026-09-13
tags: ["flux", "flux-2-development", "flux-2-klein-9b-refmods", "project"]
aliases: ["1.58-bit FLUX", "FLUX", "FLUX.1", "FLUX.2", "FLUX.2 [dev] Turbo"]
---

# FLUX.2

**Development line:** project:flux-2-klein-9b-refmods · thread flux-2-development  
**Last event:** 2026-09-13 · 6 dated since 2024-11-07 · **Researched:** 2026-11-25 · confidence: medium

## What it is

FLUX.2 RefMods (Reference Latent Adapters) are personalization adapters for Klein 9B using 2D RoPE reference latent injection.

They replace legacy pixel encoding. The release provides a hub of 1,400+ open-weight RefMods and Prodigy LoRAs, a ComfyUI custom node, ready-made workflows and a CLI extraction script.

## Development line

- **2024-11-07 — FLUX 1.1 Ultra was publicly documented.** On 2024-11-07, Black Forest Labs documented FLUX 1.1 Ultra alongside the fal.ai model route, marking a public availability milestone before FLUX.2.
- **2024-12-30 — A FLUX research-paper record entered the development line.** On 2024-12-30, Hugging Face listed research paper 2412.18653 for the FLUX lineage. The text does not establish the paper's precise contribution to a specific release.
- **2025-11-25 — A FLUX.2 development model repository was linked.** On 2025-11-25, a Comfy-Org repository named flux2-dev was linked from Hugging Face as a public distribution point for FLUX.2.
- **2025-11-27 — FLUX.2 prompting guidance was documented.** On 2025-11-27, Black Forest Labs published the FLUX.2 prompting guide alongside a source reference.
- **2025-12-30 — FLUX.2-dev-Turbo was linked with a hosted demo.** On 2025-12-30, Hugging Face hosted the FLUX.2-dev-Turbo model page and a hosted demo space, marking a Turbo development variant for FLUX.2.
- **2026-09-13 — FLUX.2 & Klein 9B RefMods Release.** Announcement of RefMods for Klein 9B, introducing personalization capabilities for the FLUX.2 model family.
  - The project documentation lists the release contents. These are the model weights hub (malcolmrey/klein9, 1,400+ open-weight RefMods and Prodigy LoRAs), an interactive model browser, the ComfyUI-Flux2Klein9Mod custom node, and two workflows: workflow_klein9_refmod.json for pure RefMod text-to-image and workflow_klein9_refmod_lora.json for a hybrid RefMod + LoRA stack aimed at maximum facial likeness and micro-texture fidelity. It also covers a CLI generator and batch extractor script and visual benchmarks on six celebrity datasets. (undated (file page shows last commit about 2 months before observation)) — <https://huggingface.co/datasets/malcolmrey/various/blob/main/klein9/docs/README.md>

## What changed

RefMods for Klein 9B provide a documented toolkit: pre-extracted weights, an interactive model browser, the ComfyUI custom node, two ComfyUI workflows (pure RefMod and hybrid RefMod + LoRA) and a batch extraction script.

## How to use this

1. Install and configure the ComfyUI-Flux2Klein9Mod custom node (github.com/malcolmamal/ComfyUI-Flux2Klein9Mod), as described in the guide.
  — <https://huggingface.co/datasets/malcolmrey/various/blob/main/klein9/docs/README.md>
2. Download a pre-extracted RefMod from the malcolmrey/klein9 hub, or search for one in the interactive model browser (malcolmrey/browser).
  — <https://huggingface.co/datasets/malcolmrey/various/blob/main/klein9/docs/README.md>
3. Drag workflow_klein9_refmod.json into ComfyUI for pure RefMod text-to-image generation with FLUX.2 / Klein 9B, or workflow_klein9_refmod_lora.json for the hybrid RefMod + LoRA stack.
  — <https://huggingface.co/datasets/malcolmrey/various/blob/main/klein9/docs/README.md>
4. To create your own RefMod, curate a dataset and extract it with the generator script generate_flux2_klein9_refmod.py. It supports single-dataset extraction, custom token budgets, dry-run inspection and mass batch extraction.
  — <https://huggingface.co/datasets/malcolmrey/various/blob/main/klein9/docs/README.md>

## Best practices

- Use the hybrid RefMod + LoRA workflow when maximum facial likeness and micro-texture fidelity are needed. Use the pure RefMod workflow for plain text-to-image generation.
  — <https://huggingface.co/datasets/malcolmrey/various/blob/main/klein9/docs/README.md>
- Follow the dataset curation guidance in the guide before extracting a RefMod. Use the script's dry-run inspection to check an extraction first.
  — <https://huggingface.co/datasets/malcolmrey/various/blob/main/klein9/docs/README.md>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The exact release date is not stated on the documentation page; the date comes from the reviewed event.
- Benchmark results and VRAM figures are referenced but not shown in the retrieved page text.
- The license terms for individual RefMod weights are not stated; the dataset repository lists WTFPL.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/datasets/malcolmrey/various/blob/main/klein9/docs/README.md | klein9/docs/README.md · malcolmrey/various (Hugging Face) | 2026-09-13 |

## Agent brief {#agent-brief}

- **Subject:** project:flux-2-klein-9b-refmods, thread flux-2-development, 6 dated events 2024-11-07 → 2026-09-13.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.