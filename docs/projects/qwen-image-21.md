---
title: "Qwen"
category: "projects"
date: 2026-09-30
tags: ["project", "qwen", "qwen-image-21", "qwen-model-and-capability-releases", "qwen-video", "qwen_model_updates"]
aliases: ["Qwen", "Qwen3.5-122B-A10B-FP8"]
---

# Qwen

**Development line:** project:qwen-image-21 · thread qwen-model-and-capability-releases  
**Last event:** 2026-09-30 · 5 dated since 2026-03-03 · **Researched:** 2026-11-28 · confidence: medium

## What it is

Qwen Image 2.1 is an image-generation base model for practitioners using Diffusers, VideoX-Fun, llama.cpp, or ComfyUI. Its ecosystem includes text-to-image and image editing, few-step LoRAs, structural controls, prompt rewriting, and workflow files. Acceleration adapters range from 4 to 8 sampling evaluations depending on the component. The grounded verdict is that it is a modular ecosystem: select a base model and only the adapter or control component that matches the intended workflow.

## Development line

- **2026-03-03 — Qwen3.5-122B-A10B-FP8 checkpoint reference.** On 2026-03-03, the Qwen development line included a link to the Hugging Face repository named Qwen/Qwen3.5-122B-A10B-FP8. This is a material dated reference to a distinct Qwen model checkpoint; the supplied evidence does not establish release notes, capabilities, or licensing terms.
- **2026-06-30 — Qwen3-ASR-1.7B-hf checkpoint reference.** On 2026-06-30, the Qwen development line included a link to the Hugging Face repository named Qwen/Qwen3-ASR-1.7B-hf. Its ASR-oriented model name makes this a material extension of the recorded Qwen line into speech recognition; no additional claim is drawn from the accompanying the recorded link.
- **2026-09-25 — Qwen Image 2.1 development updates: new LoRAs, workflows, and optimization tools released.** Announcements include turbo LoRAs for faster generation \(5-8 steps\), a prompt enhancer improving speed by 1.4-1.7x, new ControlNet-Union and Acc LoRAs, and a character design sheet maker workflow. These represent incremental development progress for the Qwen Image 2.1 project.
  - The Viggle material identifies the contemporaneous v0.2.1 adapter as a 6-step LoRA release dated 2026-09-24; it is distinct from the later v0.3 release and from merged single-file ComfyUI transformers. (2026-09-24) — <https://huggingface.co/Viggle/Qwen-Image-2.1-viggle-turbo>
  - The Pruna ComfyUI conversion supplies two separate adapters: 8-step and 5-step. The model card recommends the 8-step adapter as the starting point and requires that each adapter use its matching sigma schedule. (undated) — <https://huggingface.co/NidAll/pruna-image-2.1-comfyui-loras>
  - The Fun Acc release is specifically a rank-64 Qwen-Image-2.1 LoRA using Parallel Decoding Distillation at 4 NFE for both text-to-image and instruction-based editing; it is not a replacement base checkpoint. (undated) — <https://huggingface.co/alibaba-pai/Qwen-Image-2.1-Fun-Acc-LoRAs>
  - The Fun ControlNet-Union checkpoint is a roughly 7 GB control branch loaded on top of the base transformer. One checkpoint covers Canny, Depth, Grayscale, HED, Lineart, MLSD, Pose, Scribble, and inpainting rather than providing one file per condition. (undated) — <https://huggingface.co/alibaba-pai/Qwen-Image-2.1-Fun-Controlnet-Union>
  - The Prompt Enhancer node runs Qwen Image 2.1 prompt rewriting with multi-token prediction. Its ComfyUI backend is documented at about 1.4× for text-to-image prompt generation and 1.7× for editing, while the NVIDIA llama.cpp backend is documented separately at about 2× to 3.5×. (undated) — <https://github.com/mozophe/ComfyUI-Qwen-Image-2.1-PromptEnhancer-MTP>
- **2026-09-29 — Qwen update.** Viggle released v0.3: a 6-step Turbo LoRA and a 9-step mode that returns to the base model for its final two steps. The repository retains v0.2.1 rather than presenting v0.3 as a strict replacement. (found in research)
- **2026-09-30 — Qwen update.** Prompt Enhancer MTP 1.2.0 added a llama.cpp backend recommended for NVIDIA GPUs; the existing ComfyUI backend remained the compatibility default. (found in research)

## What changed

Qwen Image 2.1 now has separately maintained acceleration LoRAs, prompt-rewriter integrations, and a union ControlNet integration alongside the base image model. These components have different loading paths, licenses, compatibility requirements, and quality trade-offs; they are not a single interchangeable release.

## How to use this

1. For a few-step ComfyUI workflow, install recent native Qwen Image 2.1 support, place the base transformer, text encoder, and VAE in the listed model folders, add one Pruna adapter to the LoRA folder, then load its matching workflow JSON.
  — <https://huggingface.co/NidAll/pruna-image-2.1-comfyui-loras>
2. For the Viggle Turbo LoRA in Diffusers, load Qwen/Qwen-Image-2.1, load the specified LoRA weights and scheduler, then use its supplied six-step sigma sequence with CFG 1.0.
  — <https://huggingface.co/Viggle/Qwen-Image-2.1-viggle-turbo>
3. For accelerated text-to-image or editing, keep the Fun PDD helper scripts with the prediction scripts, then run the text-to-image or editing entry point; VideoX-Fun is the alternative supported path.
  — <https://huggingface.co/alibaba-pai/Qwen-Image-2.1-Fun-Acc-LoRAs>
4. For structural control, download the base Qwen Image 2.1 model and the Fun ControlNet-Union checkpoint into the documented VideoX-Fun model folders, select a control image, configure the supplied control script, and run text-to-image control or image inpainting.
  — <https://huggingface.co/alibaba-pai/Qwen-Image-2.1-Fun-Controlnet-Union>
5. For prompt rewriting in ComfyUI, install the Prompt Enhancer MTP custom node through ComfyUI Manager or by cloning it under custom\_nodes, restart ComfyUI, load the text-to-image or image-editing preset, and connect its rewritten prompt to the image workflow.
  — <https://github.com/mozophe/ComfyUI-Qwen-Image-2.1-PromptEnhancer-MTP>

## Best practices

- Use one Pruna adapter at a time and preserve its exact matching sigma schedule; start with the 8-step adapter when image quality matters more than the smallest step count.
  — <https://huggingface.co/NidAll/pruna-image-2.1-comfyui-loras>
- Treat acceleration LoRAs as quality-speed trade-offs: the Fun 4-NFE card warns that dense small text can become less legible and some edits can look blurrier or darker than teacher outputs.
  — <https://huggingface.co/alibaba-pai/Qwen-Image-2.1-Fun-Acc-LoRAs>
- Keep the Prompt Enhancer reasoning mode enabled and use the official presets unless deliberately replacing their system prompt; the node documents reduced answer-format reliability without reasoning.
  — <https://github.com/mozophe/ComfyUI-Qwen-Image-2.1-PromptEnhancer-MTP>
- For Viggle Turbo, use six steps and CFG 1.0 as specified, and test the base model when small dense text or complex multi-reference edits are important.
  — <https://huggingface.co/Viggle/Qwen-Image-2.1-viggle-turbo>

## What practitioners say

- One ComfyUI tester reported that the 8-step Pruna setup gave strong character consistency at 1024×1280, but rewrote prompt-enhancer instructions after finding the defaults weak for reference-image compositing. (2026-09-26)
  — <https://www.reddit.com/r/StableDiffusion/comments/1wq3lga/qwen_image_21_experimentation_results/>
- One ControlNet tester found pose errors when reference and target images had different dimensions; matching their sizes and reducing control strength from 1.0 to 0.8 improved a difficult pose. (2026-09-25)
  — <https://www.youtube.com/watch?v=JNLbghoDCuc>

## Superseded by this

- “The newest Viggle adapter is an unconditional upgrade.”
  — <https://huggingface.co/Viggle/Qwen-Image-2.1-viggle-turbo>
- “The Prompt Enhancer can only run through ComfyUI’s native text-generation backend.”
  — <https://github.com/mozophe/ComfyUI-Qwen-Image-2.1-PromptEnhancer-MTP>

## Still unknown

- Qwen Image 2.1 is the base model, but the reviewed date groups releases from independent authors and organizations; the evidence does not establish a single upstream release bundle.
- Several model cards do not expose a publication date in the rendered public page, so their current documentation confirms scope but not an exact release-day timestamp.
- The reviewed character-design-sheet workflow URL was inaccessible to the research tool and is not relied on here.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/Viggle/Qwen-Image-2.1-viggle-turbo | Viggle/Qwen-Image-2.1-viggle-turbo | 2026-11-28 |
| https://huggingface.co/NidAll/pruna-image-2.1-comfyui-loras | Pruna Image 2.1 LoRAs for ComfyUI | 2026-11-28 |
| https://huggingface.co/alibaba-pai/Qwen-Image-2.1-Fun-Controlnet-Union | Qwen-Image-2.1-Fun-Controlnet-Union | 2026-11-28 |
| https://huggingface.co/alibaba-pai/Qwen-Image-2.1-Fun-Acc-LoRAs | Qwen-Image-2.1-Fun-Acc-LoRAs | 2026-11-28 |
| https://github.com/mozophe/ComfyUI-Qwen-Image-2.1-PromptEnhancer-MTP | ComfyUI Qwen-Image 2.1 Prompt Enhancer \(MTP\) | 2026-11-28 |
| https://www.reddit.com/r/StableDiffusion/comments/1wq3lga/qwen_image_21_experimentation_results/ | Qwen Image 2.1 Experimentation Results | 2026-11-28 |
| https://www.youtube.com/watch?v=JNLbghoDCuc | Qwen Image 2.1 Finally Has ControlNet: Pose, Depth and Inpainting Tested | 2026-11-28 |
| https://github.com/xiaowuapple-pixel/ComfyUI-Prompt-Enhancer/blob/main/README.md | ComfyUI Prompt Enhancer README | 2026-11-28 |
| https://comfyuimodels.com/zh/qwen-image-2-1/install | ComfyUI 安装 Qwen Image 2.1 教程：版本与文件 | 2026-11-28 |

## Agent brief {#agent-brief}

- **Subject:** project:qwen-image-21, thread qwen-model-and-capability-releases, 5 dated events 2026-03-03 → 2026-09-30.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
