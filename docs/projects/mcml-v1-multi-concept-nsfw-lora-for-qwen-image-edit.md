---
title: "Qwen"
category: "projects"
date: 2026-09-06
tags: ["mcml-v1-multi-concept-nsfw-lora-for-qwen-image-edit", "project", "qwen", "qwen-model-and-capability-releases", "qwen-video", "qwen_model_updates"]
aliases: ["Qwen", "Qwen3.5-122B-A10B-FP8"]
---

# Qwen

**Development line:** project:mcml-v1-multi-concept-nsfw-lora-for-qwen-image-edit · thread qwen-model-and-capability-releases  
**Last event:** 2026-09-06 · 3 dated since 2026-03-03 · **Researched:** 2026-11-25 · confidence: medium

## What it is

MCNL v1 (Multi Concept NSFW LoRA) is a community LoRA adapter for the Qwen Image Edit image-editing model, aimed at users of the 2511 version (QIE2511).

The Hugging Face repository carries tags for image-to-image, diffusers, lora, nsfw, image-editing, and qwen-image-edit, marked Not-For-All-Audiences. Its license is openrail++. A separate Hugging Face Space hosts a demo.

## Development line

- **2026-03-03 — Qwen3.5-122B-A10B-FP8 checkpoint reference.** On 2026-03-03, a link pointed to the Hugging Face repository Qwen/Qwen3.5-122B-A10B-FP8. It marks a distinct checkpoint, without release notes, capabilities, or licensing terms.
- **2026-06-30 — Qwen3-ASR-1.7B-hf checkpoint reference.** On 2026-06-30, a link pointed to the Hugging Face repository Qwen/Qwen3-ASR-1.7B-hf. The name extends Qwen into speech recognition, with no further claims in the link.
- **2026-09-06 — MCNL v1 — Multi Concept NSFW LoRA for Qwen Image Edit released.** MCNL v1 was released as an uncensored multi-concept LoRA for Qwen Image Edit, with demo links and community distribution via VK and MAX.
  - The model repository is ScottzillaSystems/qwen-image-edit-plus-nsfw-lora, a duplicate of aiunivers/qwen-image-edit-plus-nsfw-lora with 633 likes when observed. Its Diffusers snippet uses Qwen/Qwen-Image-Edit-2511 as the base model, matching the announced QIE2511 version. The repository is flagged for sensitive content. (undated) — <https://huggingface.co/ScottzillaSystems/qwen-image-edit-plus-nsfw-lora>
  - The demo is a Hugging Face Space named Ivan1617/qwen-image-edit-plus-nsfw-demo. It ran on Zero with 46 likes and carries a Not-For-All-Audiences flag. (undated) — <https://huggingface.co/spaces/Ivan1617/qwen-image-edit-plus-nsfw-demo>

## What changed

An uncensored LoRA for Qwen Image Edit 2511 arrived with a public demo Space. The repository snippet loads it over the Qwen/Qwen-Image-Edit-2511 base model through Diffusers.

## How to use this

1. Install the libraries: pip install -U diffusers transformers accelerate.
  — <https://huggingface.co/ScottzillaSystems/qwen-image-edit-plus-nsfw-lora>
2. Load the base pipeline with DiffusionPipeline.from_pretrained("Qwen/Qwen-Image-Edit-2511", dtype=torch.bfloat16, device_map="cuda"). On Apple devices, use "mps".
  — <https://huggingface.co/ScottzillaSystems/qwen-image-edit-plus-nsfw-lora>
3. Apply the adapter with pipe.load_lora_weights("ScottzillaSystems/qwen-image-edit-plus-nsfw-lora"). Load an input image with load_image, write an edit prompt, and call pipe(image=input_image, prompt=prompt).images[0].
  — <https://huggingface.co/ScottzillaSystems/qwen-image-edit-plus-nsfw-lora>
4. To test without local setup, use the hosted demo Space. Acknowledge the sensitive content warning to proceed.
  — <https://huggingface.co/spaces/Ivan1617/qwen-image-edit-plus-nsfw-demo>

## Best practices

- Pair the LoRA with the Qwen/Qwen-Image-Edit-2511 base model as shown in the repository example, rather than another version.
  — <https://huggingface.co/ScottzillaSystems/qwen-image-edit-plus-nsfw-lora>
- Keep usage and outputs out of shared settings, since both repository and demo are marked Not-For-All-Audiences. Review the openrail++ license before use.
  — <https://huggingface.co/ScottzillaSystems/qwen-image-edit-plus-nsfw-lora>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The linked pages do not use the name "MCNL v1", leaving the exact release unconfirmed.
- The pages state neither release date nor version history for the LoRA.
- The pages give no training details, no list of supported concepts, and no recommended prompts or LoRA strength.
- The repository duplicates aiunivers/qwen-image-edit-plus-nsfw-lora without identifying the original author.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/ScottzillaSystems/qwen-image-edit-plus-nsfw-lora | ScottzillaSystems/qwen-image-edit-plus-nsfw-lora · Hugging Face | 2026-09-06 |
| https://huggingface.co/spaces/Ivan1617/qwen-image-edit-plus-nsfw-demo | Qwen Image Edit Plus NSFW LoRA Demo - a Hugging Face Space by Ivan1617 | 2026-09-06 |

## Agent brief {#agent-brief}

- **Subject:** project:mcml-v1-multi-concept-nsfw-lora-for-qwen-image-edit, thread qwen-model-and-capability-releases, 3 dated events 2026-03-03 → 2026-09-06.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
