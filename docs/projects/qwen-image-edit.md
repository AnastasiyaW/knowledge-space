---
title: MCNL v1 for Qwen-Image-Edit-2511
category: projects
date: 2026-09-03
tags: [qwen-image-edit, mcnl-v1, lora, community-adapter]
aliases: ["MCNL v1", "ScottzillaSystems Qwen Image Edit adapter"]
---

# MCNL v1 for Qwen-Image-Edit-2511

**Development line:** `project:qwen-image-edit` · thread `qwen-image-edit-development`  
**Last event:** 2026-09-03 · 1 dated event · **Researched:** 2026-09-05 · confidence: medium

## What it is

MCNL v1 is a community LoRA for `Qwen-Image-Edit-2511` from the ScottzillaSystems repository. The card labels it as a duplicate of `aiunivers/qwen-image-edit-plus-nsfw-lora`. [Distributor model card](https://huggingface.co/ScottzillaSystems/qwen-image-edit-plus-nsfw-lora?not-for-all-audiences=true)

The card lists an approximately 563 MB safetensors adapter, not a complete model installation. [Distributor model card](https://huggingface.co/ScottzillaSystems/qwen-image-edit-plus-nsfw-lora?not-for-all-audiences=true)

## Practical handling

1. Treat the download as an adapter dependency of `Qwen-Image-Edit-2511`, not a standalone 563 MB installation.
   — <https://huggingface.co/ScottzillaSystems/qwen-image-edit-plus-nsfw-lora?not-for-all-audiences=true>

2. Keep the exact base checkpoint and adapter identity in the workflow record.
   — <https://huggingface.co/ScottzillaSystems/qwen-image-edit-plus-nsfw-lora?not-for-all-audiences=true>

## Limits and open questions

No controlled operation test or hardware minimum was established for this adapter.

No qualified Simplified-Chinese source or independent operating report was found for this exact adapter.

A card-linked alternate page returned HTTP 401 during the check. No successor availability or migration claim follows.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/ScottzillaSystems/qwen-image-edit-plus-nsfw-lora?not-for-all-audiences=true | MCNL v1 distributor model card | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:qwen-image-edit`, thread `qwen-image-edit-development`, one dated event on 2026-09-03.
- **Exact artifact:** `ScottzillaSystems/qwen-image-edit-plus-nsfw-lora`, MCNL v1; base identity: `Qwen-Image-Edit-2511`; adapter file: approximately 563 MB.
- **Use rule:** Treat the download as an adapter dependency, not a standalone installation. Keep the exact base checkpoint and adapter identity in the workflow record.
- **Limits:** No controlled operation test or hardware minimum was established; no qualified Simplified-Chinese source was found; no successor availability or migration claim follows from the alternate page.

<!-- live-update:8ebd51fc50821659c37d56ba96bf8290f1e696af34d325b42c1533992faf43f8 -->
## 2026-09-03 — Qwen-Image-Edit-2511 LoRA adapter published

A third-party Not-For-All-Audiences LoRA adapter appeared for Qwen-Image-Edit-2511 with a local Diffusers recipe. The public card marks it as a duplicate repository rather than an official Qwen release.

## 2026-09-06 — Qwen Image Edit demo Space

A Hugging Face Space hosts a Qwen Image Edit demo.

### Usage and practices

- Install a current Diffusers stack and compatible Transformers before loading the model. [Source](https://github.com/QwenLM/Qwen-Image)
- Load Qwen/Qwen-Image-Edit-2511 with QwenImageEditPlusPipeline on CUDA, then pass an image list and an explicit edit prompt. [Source](https://github.com/QwenLM/Qwen-Image)
- For the third-party adapter, load its LoRA weights only after loading the 2511 base model, and apply its separate access and content restrictions. [Source](https://huggingface.co/ScottzillaSystems/qwen-image-edit-plus-nsfw-lora)
- For difficult text corrections, mark the target area and make small successive fixes instead of expecting one edit to repair every detail. [Source](https://qwenlm.github.io/zh/blog/qwen-image-edit/)
- Use the 2511 model when an edit needs multiple source images; keep image inputs in a list, even for a single-image call when the implementation expects a list. [Source](https://github.com/QwenLM/Qwen-Image)
- State preservation constraints plainly: list what must stay untouched, such as identity, pose, lighting, typography or background. [Source](https://www.reddit.com/r/StableDiffusion/comments/1n1n81o/qwenimageedit_prompt_guide_the_complete_playbook/)
- Split complex transformations into two or three smaller edits so output drift stays low. [Source](https://www.reddit.com/r/StableDiffusion/comments/1n1n81o/qwenimageedit_prompt_guide_the_complete_playbook/)
- Do not expect a heavily quantized 20B model plus text encoder to run well on 6 GB VRAM; practitioners suggest higher precision or heavier hardware for demanding edits. [Source](https://www.reddit.com/r/StableDiffusion/comments/1tusm8l/new_to_qwen_image_edit_it_seems_to_fail_a_lot_of/)

### What practitioners say

- One practitioner reports low-VRAM quantization finishes under five minutes, but others blame failed pose and multi-subject edits on running a 20B model and 7B text encoder on 6 GB VRAM. (6 months before observation) [Source](https://www.reddit.com/r/StableDiffusion/comments/1tusm8l/new_to_qwen_image_edit_it_seems_to_fail_a_lot_of/)
- A community prompt guide suggests preservation words, negative constraints and chained small edits to curb drift, though this remains user advice rather than an official guarantee. (undated) [Source](https://www.reddit.com/r/StableDiffusion/comments/1n1n81o/qwenimageedit_prompt_guide_the_complete_playbook/)

### Additional evidence

- 2026-09-03: The public card tags the release for image editing and Qwen Image Edit as a Not-For-All-Audiences LoRA adapter, with a Diffusers recipe on top of Qwen/Qwen-Image-Edit-2511. It notes the repository is duplicated from aiunivers/qwen-image-edit-plus-nsfw-lora, so we should not treat it as an official Qwen checkpoint. [Source](https://huggingface.co/ScottzillaSystems/qwen-image-edit-plus-nsfw-lora)
- 2026-09-06: The demo runs as a Hugging Face Space, but the landing page is marked Not-For-All-Audiences and only shows the Space name and Zero runtime status; it does not confirm the MCNL v1 name or any multi-concept scope. [Source](https://huggingface.co/spaces/Ivan1617/qwen-image-edit-plus-nsfw-demo)

### Subsequent developments

- 2025-12-23: Qwen released Qwen-Image-Edit-2511 weights, documenting it for multi-image editing with improved consistency. [Source](https://github.com/QwenLM/Qwen-Image)

### Superseded guidance (retained for history)

- 2025-12-23: For multi-image edits, the 2509-or-later line replaces the original single-image Qwen-Image-Edit workflow; 2511 is the current documented choice in this development line. [Source](https://github.com/QwenLM/Qwen-Image)

### Limits and open questions

- The labels describe two releases, but public evidence shows only a sensitive third-party LoRA and a sensitive demo; nothing confirms that MCNL v1 is the adapter's canonical name or that the September 6 demo is a separate adapter release.
- Neither the adapter nor the demo page publishes a release date, so public metadata cannot date the two events on its own.
- The adapter repository marks itself as a duplicate of another Hugging Face repository; the public card shows nothing about its training data, policy scope, or relation to any named MCNL version.

<!-- Retained base: b499a7b71aef3b3ef3cc25a3ac6fd5795b6ae5d4; article blob: ee4e995bc6bb595c028d40b34ba32338d5802ab7 -->
