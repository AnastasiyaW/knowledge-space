---
title: z-image-turbo-sda — Hugging Face model release
category: projects
date: 2026-03-26
tags: [hugging-face-model-release, project, z-image-turbo-sda, z_image_turbo_sda]
aliases: ["z-image-turbo-sda"]
---

# z-image-turbo-sda — Hugging Face model release

**Development line:** `project:z-image-turbo-sda` · thread `hugging-face-model-release`  
**Last event:** 2026-03-26 · 1 dated since 2026-03-26 · **Researched:** 2026-09-06 · confidence: medium

## What it is

Z-Image-Turbo-SDA is a third-party LoKr/LyCORIS adapter for people running Tongyi-MAI/Z-Image-Turbo, not a standalone Z-Image checkpoint.

- Loads into the Turbo pipeline to vary pose, camera angle, and layout between seeds.
- Retains an 8-step workflow, with a reported diversity-versus-anatomy trade-off.

## Development line

- **2026-03-26 — z-image-turbo-sda was linked to a Hugging Face model repository.** Z-Image-Turbo-SDA was referenced as an already-published adapter. No repository commit is recorded on this date.

## What changed

- 2026-03-11: The repository uploaded `zit_sda_v1.safetensors` and documented a LoKr adapter for Tongyi-MAI/Z-Image-Turbo.
- 2026-03-26: Z-Image-Turbo-SDA was referenced as an already-published adapter; no repository commit is recorded on this date.
- 2026-04-09: Two commits labelled `Update README.md` changed documentation, not the public weight artifact.
- 2026-05-12: The maintainer acknowledged compatibility issues with some derivative ZIT models and pointed to a separate code-only alternative.

## How to use this

From 2026-03-26, we treat the Hugging Face repository F16/z-image-turbo-sda as the distribution reference for z-image-turbo-sda. Check its model card, files, license, and compatibility before use.

1. Start with the exact `Tongyi-MAI/Z-Image-Turbo` base. SDA is an adapter, not a checkpoint to load by itself.
  — <https://huggingface.co/F16/z-image-turbo-sda>
2. In a CUDA Diffusers setup, load the base in float16, then load `F16/z-image-turbo-sda` with `pipeline.load_lora_weights(..., adapter_name="sda_diversity")`. The card calls for current `diffusers` plus `peft`.
  — <https://huggingface.co/F16/z-image-turbo-sda>
3. First reproduce the supplied reference run: 8 inference steps, CFG 1.0, and a fixed grid of seeds. Assess variation across the grid rather than from one output.
  — <https://huggingface.co/F16/z-image-turbo-sda>

## Best practices

- Validate SDA alone before stacking other Z-Image-Turbo LoRAs. If stacking is needed, the maintainer suggests reducing SDA weight to 0.5–0.7 and accepting less diversity.
  — <https://huggingface.co/F16/z-image-turbo-sda>
- Use a fixed multi-seed A/B test with simple and spatially constrained prompts, then inspect complex poses for anatomy errors. The card notes that constrained prompts leave less room for composition changes.
  — <https://huggingface.co/F16/z-image-turbo-sda>
- Keep the adapter card's 8-step, CFG-1.0 preset separate from the official base recipe. The official recipe specifies ZImagePipeline, bf16, 9 scheduler steps for 8 DiT forwards, and CFG 0.0.
  — <https://huggingface.co/Tongyi-MAI/Z-Image-Turbo>
- Treat the reported LPIPS improvement and diversity-recovery percentages as maintainer results, not independently reproduced benchmarks.
  — <https://huggingface.co/F16/z-image-turbo-sda>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- No public training code, dataset provenance, immutable training-checkpoint digest, minimum `diffusers`/`peft` version, or supported ComfyUI workflow was found.
- The model card's LPIPS values and claimed 70.2%/58% diversity recovery are maintainer-reported and were not independently validated.
- No public repository activity establishes a new SDA release exactly on 2026-03-26. The date identifies an existing artifact rather than a demonstrated weight update.
- No evidence was found that Tongyi-MAI created, endorsed, or maintains this adapter.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/F16/z-image-turbo-sda | F16/z-image-turbo-sda model card | 2026-09-06 |
| https://huggingface.co/F16/z-image-turbo-sda/commits/main | Commit History · F16/z-image-turbo-sda | 2026-09-06 |
| https://huggingface.co/F16/z-image-turbo-sda/blob/2557329bb6c6b23fdf846f3f21ab42d4f8df523e/README.md | README.md · F16/z-image-turbo-sda at revision 2557329 | 2026-09-06 |
| https://huggingface.co/F16/z-image-turbo-sda/blob/main/zit_sda_v1.safetensors | zit_sda_v1.safetensors · F16/z-image-turbo-sda | 2026-09-06 |
| https://huggingface.co/F16/z-image-turbo-sda/discussions/5 | Why does applying this LoRA to certain ZIT models cause the image to break? | 2026-09-06 |
| https://huggingface.co/Tongyi-MAI/Z-Image-Turbo | Tongyi-MAI/Z-Image-Turbo model card | 2026-09-06 |

## Agent brief {#agent-brief}

- **Subject:** `project:z-image-turbo-sda`, thread `hugging-face-model-release`, 1 dated events 2026-03-26 → 2026-03-26.
- **Practical note:** From 2026-03-26, we treat the Hugging Face repository F16/z-image-turbo-sda as the distribution reference for z-image-turbo-sda. Check its model card, files, license, and compatibility before use.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
