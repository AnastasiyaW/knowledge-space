---
title: FLUX.2
category: projects
date: 2025-12-30
tags: [flux, flux-2-development, project]
aliases: ["1.58-bit FLUX", "FLUX", "FLUX.1", "FLUX.2", "FLUX.2 [dev] Turbo"]
---

# FLUX.2

**Development line:** `project:flux` · thread `flux-2-development`  
**Last event:** 2025-12-30 · 5 dated since 2024-11-07 · **Researched:** 2026-09-07 · confidence: medium

## What it is

FLUX.2 is Black Forest Labs' model family for API teams, local developers, and ComfyUI pipelines running generation and editing through one pipeline.
- Text-to-image, text-guided editing, and multi-reference composition.
- [max], [pro], and [flex] for API use, with [dev] and [klein] for local deployment.
- Typography, structured prompting, and color control for production layouts.

[pro] caps the budget at 9 MP across inputs and output combined; local weights [dev] and [klein] 9B carry a non-commercial license, while [klein] 4B is Apache 2.0.

Choose FLUX.2 when one workflow needs references and image editing together; do not automatically replace standalone FLUX.1.1 API endpoints.

## Development line

- **2024-11-07 — FLUX 1.1 Ultra was publicly documented.** On 2024-11-07, this development line linked the Black Forest Labs page for FLUX 1.1 Ultra and the corresponding fal.ai model route. Together, the dated links mark a public FLUX 1.1 Ultra documentation and availability milestone in the lineage preceding FLUX.2.
- **2024-12-30 — A FLUX research-paper record entered the development line.** On 2024-12-30, Hugging Face paper 2412.18653 was linked in this lineage. This preserves a dated research reference in the FLUX lineage; the supplied evidence does not establish the paper's precise contribution to a particular release.
- **2025-11-25 — A FLUX.2 development model repository was linked.** BFL released FLUX.2 [pro] and [flex], introducing a unified generation and editing pipeline, up to 4 MP resolution, multi-reference input, structured prompts, and typography.
- **2025-11-27 — FLUX.2 prompting guidance was documented.** On 2025-11-27, the Black Forest Labs FLUX.2 prompting guide was linked alongside a source reference. This makes prompting guidance a dated part of the public FLUX.2 development line; the linked source text was not supplied.
- **2025-12-30 — FLUX.2-dev-Turbo was linked with a hosted demo.** fal linked a hosted demo claiming 8 steps instead of typical 50, supporting text-to-image and editing.

## What changed

FLUX.2 separates legacy FLUX.1 models, core FLUX.2 releases, and third-party adapters.
- **2024-11-07**: FLUX1.1 [pro] Ultra added up to 4 MP output and RAW mode as a FLUX.1 release line, not a FLUX.2 release.
- **2024-12-30**: 1.58-bit FLUX demonstrated 1.58-bit quantization for FLUX.1-dev as a research method, not a FLUX.2 weight format.
- **2025-11-25**: BFL released FLUX.2 [pro] and [flex] with a unified generation and editing pipeline, up to 4 MP, multiple references, structured prompts, and typography.
- **2025-11-25**: Comfy-Org packaged quantized FLUX.2-dev components for ComfyUI as a community distribution, not a base BFL release.
- **2025-11-27**: BFL guidance established prompting for [pro] and [max] without negative prompts, using structured JSON prompts and multi-reference editing.
- **2025-12-30**: fal/FLUX.2-dev-Turbo added a third-party LoRA adapter for FLUX.2-dev, claiming 8 steps instead of typical 50 and text-to-image plus editing support.
- **2026-01-15**: BFL released [klein] 4B and 9B Base variants for local interactive runs, licensing 4B under Apache 2.0 and 9B under FLUX NCL.
- **2026-02-17**: The API webhook success status changed from SUCCESS to Ready.
- **2026-03-03**: Quality improvements for [pro] deploy to flux-2-pro-preview, while flux-2-pro remains a pinned snapshot for reproducibility.
- **2026-04-23**: Public beta managed LoRA inference opened for [klein] through -finetuned endpoints.
- **2026-07-31**: No verified change was recorded because the linked publication was unreadable.

## How to use this

1. Match the variant to the task: [max] for highest quality and grounding search, [pro] for commercial pipelines, [flex] for in-frame typography, [klein] for low latency, and [dev] for non-commercial customization. Check the weight license before running models locally.
  — <https://help.bfl.ai/articles/6122710168-which-flux-2-model-should-i-choose>
2. Send requests to the chosen BFL API endpoint, retain the returned polling_url, and fetch the generated asset from it. Status Ready marks success; Error and Failed are terminal errors.
  — <https://docs.bfl.ai/quick_start/generating_images>
3. Use the preview endpoint to evaluate model improvements. Select a pinned non-preview endpoint for reproducible production output, and do not mix endpoints within one generation run.
  — <https://docs.bfl.ai/quick_start/generating_images>
4. Accept repository terms on Hugging Face to use FLUX.2-dev locally, load weights via Diffusers in bfloat16 on CUDA, and pass an image with the prompt for editing.
  — <https://huggingface.co/black-forest-labs/FLUX.2-dev/tree/main>
5. Update ComfyUI to run [klein] 4B locally, select an existing text-to-image or editing workflow, and place the text encoder, diffusion model, and VAE into their specified models directories.
  — <https://docs.comfy.org/zh/tutorials/flux/flux-2-klein>
6. Attach fal's third-party Turbo LoRA to FLUX.2-dev if latency is the primary bottleneck, using its dedicated 8-step sigmas. The published example specifies 8 steps and guidance_scale 2.5.
  — <https://huggingface.co/fal/FLUX.2-dev-Turbo>

## Best practices

- Structure prompts for [pro] and [max] as Subject + Action + Style + Context. Place key details first and keep descriptions between 30 and 80 words.
  — <https://docs.bfl.ai/guides/prompting_guide_flux2>
- Avoid negative prompts entirely. Describe the target result directly, such as sharp focus throughout instead of no blur.
  — <https://docs.bfl.ai/guides/prompting_guide_flux2>
- Use JSON prompts for structured automation, starting with basic schema structures. Assign HEX color codes to individual objects rather than the whole image.
  — <https://docs.bfl.ai/guides/prompting_guide_flux2>
- Assign explicit roles to each input image during multi-reference editing. Keep within the 9 MP total budget on [pro], which permits at most 8 reference images alongside a 1 MP output image.
  — <https://docs.bfl.ai/guides/prompting_guide_flux2>
- Keep endpoints consistent during evaluation runs. Select preview for current model changes, and choose pinned endpoints when reproducible output is required.
  — <https://docs.bfl.ai/quick_start/generating_images>
- Train LoRA adapters on undistilled Klein Base, but deploy distilled Klein for interactive image generation. Verify licenses separately: 4B is Apache 2.0, while 9B remains under FLUX NCL.
  — <https://bfl.ai/blog/flux2-klein-towards-interactive-visual-intelligence>

## Superseded by this

- 2026-02-17: Webhook handling using status=SUCCESS is obsolete; check status=Ready.
- 2026-03-03: The assumption that flux-2-pro automatically tracks model updates is obsolete; use flux-2-pro-preview for new updates, and retain flux-2-pro for repeatable output.
- 2026-04-23: The FLUX.1-era Finetuning API was deprecated in October 2025; BFL directs self-serve LoRA training to FLUX.2 [klein] -finetuned endpoints with finetune_id and finetune_strength.
- 2024-12-30: 1.58-bit FLUX cannot serve as a setup guide for FLUX.2; the paper quantizes FLUX.1-dev.

## Still unknown

- The content of the 2026-07-31 publication could not be read via the provided mirror or the canonical X URL; no change is claimed.
- The 2024-11-07 and 2024-12-30 milestones describe FLUX.1.1 and FLUX.1-dev rather than FLUX.2; they represent a related lineage rather than a single release track.
- FLUX.2 [dev] Turbo quality and compatibility rely solely on the fal model card; we have not verified independent benchmarks.
- Official Chinese documentation exists for ComfyUI, but we have not verified local execution on specific hardware.

## Sources

| source | title | read |
|---|---|---|
| https://blackforestlabs.ai/flux-1-1-ultra/ | Introducing FLUX1.1 [pro] Ultra and Raw Modes | Black Forest Labs | 2026-09-04 |
| https://huggingface.co/papers/2412.18653 | 1.58-bit FLUX | Hugging Face Papers | 2026-09-04 |
| https://huggingface.co/Comfy-Org/flux2-dev | Comfy-Org/flux2-dev | Hugging Face | 2026-09-04 |
| https://bfl.ai/blog/flux-2 | FLUX.2: Frontier Visual Intelligence | Black Forest Labs | 2026-09-04 |
| https://docs.bfl.ai/guides/prompting_guide_flux2 | Prompting Guide - FLUX.2 [pro] & [max] | Black Forest Labs | 2026-09-04 |
| https://huggingface.co/fal/FLUX.2-dev-Turbo | FLUX.2 [dev] Turbo LoRA | fal | 2026-09-04 |
| https://bfl.ai/blog/flux2-klein-towards-interactive-visual-intelligence | FLUX.2 [klein]: Towards Interactive Visual Intelligence | Black Forest Labs | 2026-09-04 |
| https://docs.bfl.ai/release-notes | Release Notes | Black Forest Labs | 2026-09-04 |
| https://docs.bfl.ai/quick_start/generating_images | Image Generation with Text Prompts | Black Forest Labs | 2026-09-04 |
| https://help.bfl.ai/articles/6122710168-which-flux-2-model-should-i-choose | Which FLUX.2 model should I choose? | Black Forest Labs Knowledge Base | 2026-09-04 |
| https://huggingface.co/black-forest-labs/FLUX.2-dev/tree/main | black-forest-labs/FLUX.2-dev at main | Hugging Face | 2026-09-04 |
| https://docs.comfy.org/zh/tutorials/flux/flux-2-klein | ComfyUI Flux.2 Klein 4B 指南 | ComfyUI | 2026-09-04 |
| https://bfl.ai/models/flux-2 | FLUX.2 - Next Generation Image Generation | Black Forest Labs | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:flux`, thread `flux-2-development`, 5 dated events 2024-11-07 → 2025-12-30.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
