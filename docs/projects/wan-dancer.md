---
title: Wan-Dancer
category: projects
date: 2026-07-14
tags: [project, wan-dancer, wan-dancer-development, wan_dancer]
aliases: ["Wan-Dancer"]
---

# Wan-Dancer

**Development line:** `project:wan-dancer` · thread `wan-dancer-development`  
**Last event:** 2026-07-14 · 1 dated since 2026-07-14 · **Researched:** 2026-09-06 · confidence: medium

## What it is

Wan-Dancer is a 14B music-to-dance video system for creators who need a long choreographed clip from a portrait, music track and style prompt rather than manually stitching short clips.

- Global keyframe planning from the complete track.
- Local refinement for temporal continuity.
- Style prompts for Chinese Classical, K-Pop, Street, Tap and Latin dance.

Claimed output runs at 720p and 30fps for more than one minute. The authors tested their code on 8 × NVIDIA A800 80GB GPUs. We use the author pipeline for controlled long-form work, not as a validated single-GPU or raw-demo workflow.

## Development line

- **2026-07-14 — Wan-Dancer project resources were publicly linked.** On 2026-07-14, public links appeared for the Wan-Dancer project website, source repository, Hugging Face model page, and ModelScope studio. This marked a distribution milestone for the project. The links do not establish technical claims, version details, or original announcement wording.

## What changed

Wan-Dancer — development line.

- 2026-05-09 — ComfyUI merged core WanDancer support before the public model release; this reflects implementation history rather than public artifact availability.
- 2026-07-10 — arXiv v1 published the hierarchical music-to-dance method.
- 2026-07-13 — Wan-AI announced the release of Wan-Dancer-14B weights and inference code.
- 2026-07-14 — The official repository pushed an update-links commit, and a ModelScope Community post documented a Studio portrait-and-music route.
- 2026-07-17 — arXiv published v3 without describing behavioral or weight changes in its metadata.

## How to use this

As of 2026-07-14, check the linked project page for source code and official model distributions, then verify access, licensing, and instructions before adopting it.

1. Clone Wan-Video/Wan-Dancer, create the virtual environment and install the pinned dependency set from the README. The reference platform is Ubuntu 22.04, Python 3.10.14 and CUDA 12.4.
  — <https://github.com/Wan-Video/Wan-Dancer>
2. Download Wan-AI/Wan-Dancer-14B with huggingface-cli into a controlled local model directory.
  — <https://huggingface.co/Wan-AI/Wan-Dancer-14B>
3. Prepare image_path, music_path and a global prompt_path; prompt families cover Chinese Classical, K-Pop, Street, Tap and Latin dance.
  — <https://huggingface.co/Wan-AI/Wan-Dancer-14B>
4. Run gen_video_global.sh and save the generated global video with its seed and settings.
  — <https://github.com/Wan-Video/Wan-Dancer>
5. Pass that result as global_video_path to gen_video_local.sh with the matching local prompt so local refinement has its base video.
  — <https://huggingface.co/Wan-AI/Wan-Dancer-14B>
6. For ComfyUI, update ComfyUI, open its Wan-Dancer template, and place global/local models, LoRA, text encoder, CLIP-Vision model and VAE in named template folders. This template changes upstream and is not locally verified here.
  — <https://raw.githubusercontent.com/Comfy-Org/workflow_templates/main/templates/video_wan_dancer.json>

## Best practices

- Fix the seed across comparisons so runs remain reproducible.
  — <https://huggingface.co/Wan-AI/Wan-Dancer-14B>
- Treat global and local generation as one pipeline, and never replace the required global_video_path with an unrelated clip.
  — <https://huggingface.co/Wan-AI/Wan-Dancer-14B>
- Raise inference steps for longer videos; the authors suggest 48 steps rather than treating the 24-step local example as universal.
  — <https://huggingface.co/Wan-AI/Wan-Dancer-14B>
- Do not evaluate raw quality against the project gallery, because displayed videos underwent post-processing.
  — <https://humanaigc.github.io/wan-dancer-project/>
- Start at the 5-second default in the ComfyUI template and monitor VRAM, because sampling 149 frames at once demands heavy memory.
  — <https://raw.githubusercontent.com/Comfy-Org/workflow_templates/main/templates/video_wan_dancer.json>
- Do not treat the authors' 8 × A800 80GB test system as a single-GPU minimum, because it serves as a reference environment rather than a hardware floor.
  — <https://github.com/Wan-Video/Wan-Dancer>

## Superseded by this

- Treating 2026-07-14 as the first public release date for Wan-Dancer weights and inference code; the official model card dates that release to 2026-07-13.

## Still unknown

- The direct ModelScope Studio page did not expose live controls, leaving its current fields, defaults, access policy, and limits unverified.
- No author source published a single-GPU minimum VRAM, runtime, or end-to-end reproduction; the only reported setup is 8 × A800 80GB.
- Displayed videos had post-processing and lack independent reproduction, so reported duration and quality are not production guarantees.
- Checkpoint lineage and compatibility between Wan-Dancer-14B and the wan2.2_dancer assets in the ComfyUI template remain unverified.
- ComfyUI support status remains unresolved: the official model card marks integration incomplete, while ComfyUI merged a working template.
- Checked sources show no official Wan-Dancer feature or weight update after 2026-07-17, though unindexed releases may exist.

## Sources

| source | title | read |
|---|---|---|
| https://humanaigc.github.io/wan-dancer-project/ | Wan-Dancer project page | 2026-09-06 |
| https://github.com/Wan-Video/Wan-Dancer | Wan-Video/Wan-Dancer official repository | 2026-09-06 |
| https://github.com/Wan-Video/Wan-Dancer/commits/main/ | Wan-Video/Wan-Dancer commit history | 2026-09-06 |
| https://huggingface.co/Wan-AI/Wan-Dancer-14B | Wan-AI/Wan-Dancer-14B model card | 2026-09-06 |
| https://arxiv.org/abs/2607.09581 | Wan-Dancer: A Hierarchical Framework for Minute-scale Coherent Music-to-Dance Generation | 2026-09-06 |
| https://modelscope.csdn.net/6a55a9d210ee7a33f28d3bfc.html | ModelScope Community: Wan-Dancer open-source announcement | 2026-09-06 |
| https://github.com/Comfy-Org/ComfyUI/pull/13813 | ComfyUI pull request #13813: Support Wan-Dancer | 2026-09-06 |
| https://raw.githubusercontent.com/Comfy-Org/workflow_templates/main/templates/video_wan_dancer.json | Comfy-Org Wan-Dancer workflow template on main | 2026-09-06 |

## Agent brief {#agent-brief}

- **Subject:** `project:wan-dancer`, thread `wan-dancer-development`, 1 dated events 2026-07-14 → 2026-07-14.
- **Practical note:** As of 2026-07-14, practitioners can use the linked project page to find Wan-Dancer's source and official model-distribution resources, then verify current access, licensing, and usage instructions before adopting it.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.