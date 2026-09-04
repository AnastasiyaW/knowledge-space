---
title: Qwen-Image-Edit-Rapid-AIO
category: projects
date: 2025-12-29
tags: [project, qwen-image-edit-rapid-aio, qwen_image_edit_rapid_aio]
aliases: ["Qwen-Image-Edit-Rapid-AIO"]
---

# Qwen-Image-Edit-Rapid-AIO

**Development line:** `project:qwen-image-edit-rapid-aio` · thread `qwen-image-edit-rapid-aio`  
**Last event:** 2025-12-29 · 2 dated since 2025-10-07 · **Researched:** 2026-09-04 · confidence: high

## What it is

Qwen-Image-Edit-Rapid-AIO merges speed accelerators, VAE, and CLIP for Qwen-Image-Edit into one checkpoint for ComfyUI users.

- Text-to-image without an input image
- Text-guided image editing with multiple input images
- SFW and NSFW variants

The workflow runs in 4 steps at CFG 1; v18 weighs 28.4 GB per variant.

It works for fast local editing and text-to-image, but this is not an official Qwen release and the author will not publish new versions.

## Development line

- **2025-10-07 — Public repository reference for Qwen-Image-Edit-Rapid-AIO.** The original v1 combined Qwen-Image-Edit-2509 and 4-step Lightning v2.0.
- **2025-12-29 — v18 resources and workflow references for Qwen-Image-Edit-Rapid-AIO.** On 2025-12-29, the repository recorded links to its v18 directory, a Qwen-Rapid-AIO JSON workflow, and a related GGUF distribution. These dated links confirm a later distribution and workflow reference, but they do not prove the exact changes, compatibility, or performance of v18.

## What changed

- 2025-10-07: The early Rapid-AIO checkpoint appeared; original v1 combined Qwen-Image-Edit-2509 and 4-step Lightning v2.0.
- 2025-12-29: v18 split into separate SFW and NSFW variants; the GGUF mirror added SFW quantizations Q4_K and Q5_K.
- 2026-01-08: v19 released.
- 2026-01-24: v23 released. The author later stated that v19 offers better editing consistency and v23 follows complex prompts better, then stopped further updates.

## How to use this

As of 2025-12-29, start evaluation from the v18 repository resources and the JSON workflow, and check the sources before relying on GGUF availability, compatibility, or quality claims.

1. Download the chosen Rapid-AIO checkpoint and put it in the ComfyUI checkpoints folder.
  — <https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO>
2. Import the bundled JSON workflow; it uses CheckpointLoaderSimple, TextEncodeQwenImageEditPlus, KSampler, and VAE Decode.
  — <https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO/blob/main/Qwen-Rapid-AIO.json>
3. Connect one or two source images to optional image inputs, or leave them empty for text-to-image; set the prompt in TextEncodeQwenImageEditPlus.
  — <https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO/blob/main/Qwen-Rapid-AIO.json>
4. Run with 4 steps, CFG 1, sampler sa_solver, and scheduler beta from the workflow.
  — <https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO/blob/main/Qwen-Rapid-AIO.json>
5. For a smaller download, use the matching GGUF variant and a compatible GGUF loader instead of the standard checkpoint loader.
  — <https://huggingface.co/Novice25/Qwen-Image-Edit-Rapid-AIO-GGUF/tree/main>

## Best practices

- Start with the bundled workflow and its 4-step/CFG 1 settings; do not copy standard Qwen-Image-Edit parameters blindly.
  — <https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO/blob/main/Qwen-Rapid-AIO.json>
- For edits, describe the specific change and pass the source into the image input; for text-to-image, leave the image input empty.
  — <https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO/blob/main/Qwen-Rapid-AIO.json>
- Downscale large inputs first if issues appear: the official Qwen-Image-Edit workflow scales input down to roughly one million pixels to prevent quality loss on oversized images.
  — <https://docs.comfy.org/tutorials/image/qwen/qwen-image-edit>
- Choose v19 over v23 for consistent edits; v23 is useful when following complex instructions matters more.
  — <https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO>

## Superseded by this

- 2025-12-29: v18 SFW GGUF Q4_K/Q5_K expanded the earlier v18 NSFW quantizations.
- 2026-01-24: v23 was the final published release, but it does not replace v19 when edit consistency matters more.

## Still unknown

- Rapid-AIO is a community checkpoint, not an official Qwen-Image-Edit release; base model capabilities cannot be assumed for every Rapid-AIO merge.
- The repository log for the 2025-10-07 event does not preserve the original commit date of the first v1 commit; the model card confirms the v1 description, but its historical date remains the event date.
- The Hugging Face URL for GGUF redirects from Arunk25 to Novice25; this looks like an account rename or transfer, but the reason is unconfirmed.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO | Phr00t/Qwen-Image-Edit-Rapid-AIO model card | 2026-09-05 |
| https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO/commits/main | Phr00t/Qwen-Image-Edit-Rapid-AIO commit history | 2026-09-05 |
| https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO/tree/main/v18 | Phr00t/Qwen-Image-Edit-Rapid-AIO v18 files | 2026-09-05 |
| https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO/blob/main/Qwen-Rapid-AIO.json | Qwen-Rapid-AIO ComfyUI workflow | 2026-09-05 |
| https://huggingface.co/Novice25/Qwen-Image-Edit-Rapid-AIO-GGUF/tree/main | Novice25/Qwen-Image-Edit-Rapid-AIO-GGUF files | 2026-09-05 |
| https://huggingface.co/Novice25/Qwen-Image-Edit-Rapid-AIO-GGUF/commits/main/v18 | Novice25 Qwen-Image-Edit-Rapid-AIO-GGUF v18 commit history | 2026-09-05 |
| https://docs.comfy.org/tutorials/image/qwen/qwen-image-edit | Qwen-Image-Edit ComfyUI Native Workflow Example | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:qwen-image-edit-rapid-aio`, thread `qwen-image-edit-rapid-aio`, 2 dated events 2025-10-07 → 2025-12-29.
- **Practical note:** As of 2025-12-29, evaluate v18 repository resources and the JSON workflow first, and check sources before trusting GGUF availability, compatibility, or quality claims.
- **Confidence:** high. Dated supersedes above determine what is obsolete.
