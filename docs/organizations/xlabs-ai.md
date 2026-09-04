---
title: XLabs AI — FLUX conditioning and ComfyUI integrations
category: organizations
date: 2024-08-21
tags: [flux-conditioning-and-comfyui-integrations, organization, xlabs-ai, xlabs_flux_controlnet, xlabs_flux_ip_adapter]
aliases: ["XLabs AI"]
---

# XLabs AI — FLUX conditioning and ComfyUI integrations

**Development line:** `organization:xlabs-ai` · thread `flux-conditioning-and-comfyui-integrations`  
**Last event:** 2024-08-21 · 3 dated since 2024-08-14 · **Researched:** 2026-09-04 · confidence: medium

## What it is

XLabs AI publishes FLUX.1-dev add-ons for ComfyUI. They provide structural and image-reference control when prompting alone is not enough.

- ControlNet: Canny edges, Midas depth, and HED line maps.
- IP-Adapter v2: reference-image conditioning.
- x-flux-comfyui: nodes and example workflows.

## Development line

- **2024-08-14 — XLabs AI connected a FLUX ControlNet collection to ComfyUI.** On 2024-08-14, XLabs AI paired a FLUX ControlNet collection on Hugging Face with its x-flux-comfyui codebase. This opened a ControlNet integration path for FLUX in ComfyUI. The links do not detail individual models or release notes.
- **2024-08-19 — XLabs AI documented three FLUX ControlNet v3 variants.** On 2024-08-19, XLabs AI linked FLUX ControlNet HED v3, Depth v3, and Canny v3 model pages. This expanded the collection into three named conditioning variants. The pages provide no benchmarks, version lineage, or workflow specifics.
- **2024-08-21 — XLabs AI added a FLUX IP-Adapter integration path.** On 2024-08-21, XLabs AI combined a FLUX IP-Adapter model page, the x-flux-comfyui repository, and an OpenArt workflow. This added reference-image conditioning alongside ControlNet. The evidence does not confirm runtime settings or operational results.

## What changed

On 2024-08-14, XLabs AI added a FLUX.1-dev ControlNet collection and custom nodes for ComfyUI.
On 2024-08-19, the line split into dedicated Canny v3, Depth v3, and HED v3 checkpoints for ComfyUI at 1024×1024.
On 2024-08-21, XLabs AI added FLUX IP-Adapter v1 for reference-image conditioning in the same stack.
We checked the repositories on 2026-09-04. The v1 card points to flux-ip-adapter-v2 as newer. That v2 model has more training steps, keeps aspect ratio, and is the current XLabs starting point. The custom-node repository shows no main-branch changes after 2024-10-30.

## How to use this

Treat ControlNet variants and IP-Adapter reference conditioning as separate paths as of 2024-08-21. Start from the ComfyUI integration instead of expecting one shared workflow.

1. Install x-flux-comfyui through ComfyUI Manager, or clone it under ComfyUI/custom_nodes, run python setup.py, and restart ComfyUI.
  — <https://github.com/XLabs-AI/x-flux-comfyui/blob/main/Guide.md>
2. For structural conditioning, install the ControlNet preprocessor dependency. Put the chosen Canny, Depth, or HED v3 weights in ComfyUI/models/xlabs/controlnets and refresh the model list.
  — <https://github.com/XLabs-AI/x-flux-comfyui>
3. Start with canny_workflow.json, depth_workflow.json, or hed_workflow.json at 1024×1024.
  — <https://huggingface.co/XLabs-AI/flux-controlnet-collections>
4. For reference images, use flux-ip-adapter-v2. Put Clip-L in ComfyUI/models/clip_vision and the adapter in ComfyUI/models/xlabs/ipadapters, then use Load Flux IPAdapter and Apply Flux IPAdapter.
  — <https://huggingface.co/XLabs-AI/flux-ip-adapter-v2>
5. Tune IP strength if reference adherence is weak. Use CUDA for the CLIP-ViT loader only when VRAM allows.
  — <https://github.com/XLabs-AI/x-flux-comfyui/blob/main/Guide.md>

## Best practices

- Match the condition to the task: Canny for edges, Depth for geometry, and HED for line structure. Do not treat them as interchangeable generic ControlNets.
  — <https://huggingface.co/XLabs-AI/flux-controlnet-collections>
- Test ControlNet at 1024×1024 first, which is the documented training and working resolution for v3 models.
  — <https://huggingface.co/XLabs-AI/flux-controlnet-depth-v3>
- Build new reference-image workflows on IP-Adapter v2 instead of v1. The v1 card marks v2 as the newer model.
  — <https://huggingface.co/XLabs-AI/flux-ip-adapter>
- Treat IP-Adapter as a tuning workflow rather than a fixed transfer. The v2 card still labels it beta and suggests adjusting IP strength when results are poor.
  — <https://huggingface.co/XLabs-AI/flux-ip-adapter-v2>
- Pin and test custom nodes before production use. The main-branch history ends on 2024-10-30, so setup guides do not guarantee current compatibility.
  — <https://github.com/XLabs-AI/x-flux-comfyui/commits/main>

## Superseded by this

- 2024-08-14 — for new ComfyUI ControlNet work, the initial collection is superseded by the 2024-08-19 Canny v3, Depth v3, and HED v3 checkpoints and workflows.
- 2024-08-21 — do not start new work from flux-ip-adapter v1. Its card marks flux-ip-adapter-v2 as newer.
- 2024-era installation guidance does not guarantee current compatibility. The x-flux-comfyui main-branch history stops at 2024-10-30, so test it against your installed ComfyUI release.

## Still unknown

- ControlNet and IP-Adapter are separate lines from XLabs AI. One conditions FLUX with structural maps and the other with reference images; neither replaces the other.
- We found no first-party Simplified-Chinese documentation or release notes in the Chinese research lane.
- No source checked today proves compatibility between x-flux-comfyui and current ComfyUI or a FLUX successor.
- Commercial terms remain unconfirmed. The v2 page shows Apache-2.0 metadata, but the license text restricts weights to the FLUX.1-dev Non-Commercial License.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/XLabs-AI/flux-controlnet-collections | XLabs-AI/flux-controlnet-collections · Hugging Face | 2026-09-04 |
| https://huggingface.co/XLabs-AI/flux-controlnet-hed-v3 | XLabs-AI/flux-controlnet-hed-v3 · Hugging Face | 2026-09-04 |
| https://huggingface.co/XLabs-AI/flux-controlnet-depth-v3 | XLabs-AI/flux-controlnet-depth-v3 · Hugging Face | 2026-09-04 |
| https://huggingface.co/XLabs-AI/flux-controlnet-canny-v3 | XLabs-AI/flux-controlnet-canny-v3 · Hugging Face | 2026-09-04 |
| https://huggingface.co/XLabs-AI/flux-ip-adapter | XLabs-AI/flux-ip-adapter · Hugging Face | 2026-09-04 |
| https://huggingface.co/XLabs-AI/flux-ip-adapter-v2 | XLabs-AI/flux-ip-adapter-v2 · Hugging Face | 2026-09-04 |
| https://github.com/XLabs-AI/x-flux-comfyui | GitHub - XLabs-AI/x-flux-comfyui | 2026-09-04 |
| https://github.com/XLabs-AI/x-flux-comfyui/blob/main/Guide.md | x-flux-comfyui Guide.md · GitHub | 2026-09-04 |
| https://github.com/XLabs-AI/x-flux-comfyui/commits/main | Commits · XLabs-AI/x-flux-comfyui · GitHub | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `organization:xlabs-ai`, thread `flux-conditioning-and-comfyui-integrations`, 3 dated events 2024-08-14 → 2024-08-21.
- **Practical note:** Treat ControlNet conditioning and IP-Adapter reference conditioning as separate paths as of 2024-08-21. Start from the linked ComfyUI integration rather than assuming a single shared workflow.
- **Confidence:** medium. The dated supersedes list above marks what is obsolete.
