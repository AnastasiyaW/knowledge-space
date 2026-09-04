---
title: XLabs AI — FLUX conditioning and ComfyUI integrations
category: organizations
tags: [flux-conditioning-and-comfyui-integrations, organization, xlabs-ai, xlabs_flux_controlnet, xlabs_flux_ip_adapter]
aliases: ["XLabs AI"]
---

# XLabs AI — FLUX conditioning and ComfyUI integrations

**Development line:** `organization:xlabs-ai` · thread `flux-conditioning-and-comfyui-integrations`  
**Events:** 3 dated, 2024-08-14 → 2024-08-21 · **Researched:** 2026-09-04 · confidence: medium

## What it is

XLabs AI publishes FLUX.1-dev add-ons for ComfyUI users who need image-reference or structural control beyond prompting. - ControlNet: Canny edges, Midas depth, and HED line maps. - IP-Adapter v2: reference-image conditioning. - x-flux-comfyui: nodes and example workflows. Limit: v3 ControlNets target 1024×1024; IP-Adapter v2 remains labelled beta; the bridge’s latest displayed main-branch commit is 2024-10-30. Verdict: use it for an existing FLUX.1-dev ComfyUI workflow, with a compatibility test on the installed ComfyUI version.

## Development line

- **2024-08-14 — XLabs AI connected a FLUX ControlNet collection to ComfyUI.** On 2024-08-14, XLabs AI's dated links paired a FLUX ControlNet collection on Hugging Face with its x-flux-comfyui codebase. This marks a material ControlNet integration path for FLUX-related work in ComfyUI. The supplied links do not establish individual model contents or release details.
- **2024-08-19 — XLabs AI documented three FLUX ControlNet v3 variants.** On 2024-08-19, XLabs AI's dated links identified FLUX ControlNet HED v3, Depth v3, and Canny v3 model pages. This was a material expansion from a collection-level ControlNet entry to three named conditioning variants. The evidence provides no benchmark, version-lineage, or workflow details beyond the URLs.
- **2024-08-21 — XLabs AI added a FLUX IP-Adapter integration path.** On 2024-08-21, XLabs AI's dated links combined a FLUX IP-Adapter model page, the x-flux-comfyui repository, and an OpenArt workflow. This added a separate reference-image conditioning route alongside the ControlNet work. The supplied evidence does not confirm implementation settings or operational results.

## What changed

2024-08-14 — XLabs AI added a FLUX.1-dev ControlNet collection and its ComfyUI custom-node path. 2024-08-19 — the line split into dedicated Canny v3, Depth v3, and HED v3 checkpoints, each documented for direct ComfyUI use at 1024×1024. 2024-08-21 — XLabs AI added the original FLUX IP-Adapter v1 for reference-image conditioning in the same node stack. Found today, 2026-09-04 — the v1 card explicitly points to flux-ip-adapter-v2 as newer; v2 has more training steps, retains aspect ratio, and is the current XLabs starting point, while the custom-node repository shows no displayed main-branch changes after 2024-10-30.

## How to use this

As of 2024-08-21, practitioners evaluating XLabs AI's FLUX tooling should treat ControlNet conditioning variants and IP-Adapter reference conditioning as distinct paths, and begin from the linked ComfyUI integration rather than assuming a single interchangeable workflow.

1. Install x-flux-comfyui through ComfyUI Manager, or clone it under ComfyUI/custom_nodes and run python setup.py; restart ComfyUI.
  — <https://github.com/XLabs-AI/x-flux-comfyui/blob/main/Guide.md>
2. For structural conditioning, install the ControlNet preprocessor dependency, put the chosen Canny, Depth, or HED v3 weight in ComfyUI/models/xlabs/controlnets, and refresh the model list.
  — <https://github.com/XLabs-AI/x-flux-comfyui>
3. Begin with the supplied canny_workflow.json, depth_workflow.json, or hed_workflow.json at 1024×1024.
  — <https://huggingface.co/XLabs-AI/flux-controlnet-collections>
4. For a reference image, use flux-ip-adapter-v2; place Clip-L in ComfyUI/models/clip_vision and the adapter in ComfyUI/models/xlabs/ipadapters, then use Load Flux IPAdapter and Apply Flux IPAdapter.
  — <https://huggingface.co/XLabs-AI/flux-ip-adapter-v2>
5. If reference adherence is poor, tune IP strength; use CUDA for the CLIP-ViT loader only when VRAM permits it.
  — <https://github.com/XLabs-AI/x-flux-comfyui/blob/main/Guide.md>

## Best practices

- Choose the condition by task: Canny for edges, Depth for geometry, and HED for line structure; do not treat them as interchangeable generic ControlNets.
  — <https://huggingface.co/XLabs-AI/flux-controlnet-collections>
- Start ControlNet tests at 1024×1024, the documented training and working resolution for the v3 models.
  — <https://huggingface.co/XLabs-AI/flux-controlnet-depth-v3>
- Start new reference-image workflows from IP-Adapter v2, not v1: the v1 card identifies v2 as the newer model.
  — <https://huggingface.co/XLabs-AI/flux-ip-adapter>
- Treat IP-Adapter as a tuning workflow rather than a deterministic transfer: the v2 card still labels it beta and recommends adjusting IP strength when results are poor.
  — <https://huggingface.co/XLabs-AI/flux-ip-adapter-v2>
- Pin and test the custom-node version before production use; the displayed main-branch history ends on 2024-10-30, so installation instructions are not present-day compatibility proof.
  — <https://github.com/XLabs-AI/x-flux-comfyui/commits/main>

## Superseded by this

- 2024-08-14 — for new ComfyUI ControlNet work, the initial collection-level starting point is superseded by the 2024-08-19 task-specific Canny v3, Depth v3, and HED v3 checkpoints and workflows.
- 2024-08-21 — do not start new work from flux-ip-adapter v1: its model card explicitly marks flux-ip-adapter-v2 as newer.
- 2024-era installation guidance is not a current compatibility guarantee: the x-flux-comfyui main branch’s latest displayed commit is 2024-10-30, so validate it against the installed ComfyUI release.

## Still unknown

- The ControlNet and IP-Adapter threads are distinct product lines under the same XLabs AI publisher: one conditions FLUX from structural maps, the other from a reference image; neither is a version of the other.
- No first-party Simplified-Chinese documentation or release record was found in the Chinese research lane.
- No source read today proves compatibility between x-flux-comfyui and a current ComfyUI release or a current FLUX successor.
- Commercial-use status needs direct confirmation: the v2 page displays Apache-2.0 metadata while its own licence section says the weights fall under the FLUX.1-dev Non-Commercial License.

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
- **Practical note:** As of 2024-08-21, practitioners evaluating XLabs AI's FLUX tooling should treat ControlNet conditioning variants and IP-Adapter reference conditioning as distinct paths, and begin from the linked ComfyUI integration rather than assuming a single interchangeable workflow.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
