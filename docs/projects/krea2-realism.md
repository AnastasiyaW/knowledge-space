---
title: Krea2-realism — Krea2 LoRAs
category: projects
date: 2026-07-04
tags: [krea2-loras, krea2-realism, project]
aliases: ["Krea2-realism"]
---

# Krea2-realism — Krea2 LoRAs

**Development line:** `project:krea2-realism` · thread `krea2-loras`  
**Last event:** 2026-07-04 · 1 dated since 2026-07-04 · **Researched:** 2026-09-05 · confidence: medium

## What it is

Krea2-realism is a community LoRA line for the gated Krea 2 Turbo text-to-image model.

- V1 targets SFW and NSFW photorealistic subjects.
- V2 targets facial expression, texture, lighting, composition, and compatibility with character LoRAs.
- Generation and image-to-image aid, not an image-editing model.

The maintained V2 guidance recommends a 4–5 sentence natural-language prompt and LoRA strength 1.5–2.0.

We use V2 for new Krea 2 work, particularly when a character LoRA must retain its face. Keep V1 only to reproduce an existing setup.

## Development line

- **2026-07-04 — Krea2 Realism v1 version-specific model references recorded.** On 2026-07-04, the Krea2-realism development line recorded two version-specific Civitai references for Krea2 Realism v1. The links identify distinct model-version artifacts, 3066973 and 3090634, so we track available versions in project history.

## What changed

- 2026-06-24 — Krea2-realism-V1, model version 3066973, arrived as a Krea 2 realism LoRA for SFW and NSFW generation.
- 2026-07-02 — Krea2-realism-V2, model version 3090634, replaced V1 as the active revision. It brought more natural faces, improved texture, lighting, composition, and better coexistence with character LoRAs.
- 2026-07-04 — Both V1 and V2 model-version links were collected together. This was not an independently dated release.

## How to use this

From 2026-07-04, we pin Krea2 Realism v1 by its exact Civitai modelVersionId and record which of the two referenced versions was used, rather than treating the model page as a single unversioned artifact.

1. Request access to Krea 2 Turbo and accept its community licence before downloading or running the base model.
  — <https://huggingface.co/krea/Krea-2-Turbo>
2. Download Krea2-realism-V2, the current revision of this LoRA line.
  — <https://huggingface.co/RudySen/Krea2-realism-V2>
3. In ComfyUI, place the LoRA file in `ComfyUI/models/loras/` and select it with a Load LoRA node in a Krea 2 workflow.
  — <https://note.com/yasashii_maou/n/naf58ef9a48fb?hl=en>
4. Start from the V1 workflow if available, replacing only the LoRA with V2. Use image-to-image rather than treating it as a dedicated editor.
  — <https://www.reddit.com/r/StableDiffusion/comments/1ulonm8/krea2realismv2_is_finally_here_things_got_a/>
5. Describe the scene in a short natural-language paragraph. Render and tune LoRA weight against the chosen subject and character LoRA.
  — <https://huggingface.co/RudySen/Krea2-realism-V2>

## Best practices

- Prefer V2 over V1 when stacking a character LoRA: V2 does not alter faces supplied by other character LoRAs.
  — <https://www.reddit.com/r/StableDiffusion/comments/1ulonm8/krea2realismv2_is_finally_here_things_got_a/>
- Use a 4–5 sentence scene description instead of tag stacking. Begin around strength 1.0 for a controlled comparison, then test 1.5–2.0 if the result needs more effect.
  — <https://huggingface.co/RudySen/Krea2-realism-V2>
- Treat V2 as an image-generation or image-to-image component, not as a semantic image editor.
  — <https://www.reddit.com/r/StableDiffusion/comments/1ulonm8/krea2realismv2_is_finally_here_things_got_a/>

## Superseded by this

- 2026-06-24 — Krea2-realism-V1 (model version 3066973) is superseded for new work by Krea2-realism-V2 (model version 3090634, released 2026-07-02). The V1 workflow remains usable by swapping the LoRA.

## Still unknown

- Original Civitai endpoints were inaccessible, so model metadata, download availability, and licence terms on those pages could not be verified.
- The Hugging Face V2 mirror declares MIT, while the Krea 2 base model has the Krea 2 Community License. Applicable distribution and use terms for the combined workflow need confirmation from the original model page.
- No source documents a release on 2026-07-04 itself. That date records both version links rather than a new model change.

## Sources

| source | title | read |
|---|---|---|
| https://civitai.red/models/2728365/krea2-realism-v1?modelVersionId=3066973 | Krea2-realism-V1, model version 3066973 | 2026-09-05 |
| https://civitai.red/models/2728365/krea2-realism-v1?modelVersionId=3090634 | Krea2-realism-V2, model version 3090634 | 2026-09-05 |
| https://www.reddit.com/r/StableDiffusion/comments/1ueq9au/one_lora_for_krea_2_sfw_and_not_sfw_realism/ | One LoRA for Krea 2. SFW and Not SFW Realism. | 2026-09-05 |
| https://www.reddit.com/r/StableDiffusion/comments/1ulonm8/krea2realismv2_is_finally_here_things_got_a/ | Krea2-realism-V2 is finally here! Things got a little wild (in the best way possible) | 2026-09-05 |
| https://huggingface.co/RudySen/Krea2-realism-V2 | RudySen/Krea2-realism-V2 | 2026-09-05 |
| https://huggingface.co/krea/Krea-2-Turbo | krea/Krea-2-Turbo | 2026-09-05 |
| https://note.com/yasashii_maou/n/naf58ef9a48fb?hl=en | [ComfyUI] A memo on using the realistic LoRA 'realism-V2' for Krea 2. With images | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:krea2-realism`, thread `krea2-loras`, 1 dated events 2026-07-04 → 2026-07-04.
- **Practical note:** From 2026-07-04, we pin Krea2 Realism v1 by its exact Civitai modelVersionId and record which of the two referenced versions was used, rather than treating the model page as a single unversioned artifact.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
