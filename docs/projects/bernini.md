---
title: Bernini — Model availability and ComfyUI integration
category: projects
date: 2026-06-02
tags: [bernini, model-availability-and-comfyui-integration, project]
aliases: ["Bernini"]
---

# Bernini — Model availability and ComfyUI integration

**Development line:** `project:bernini` · thread `model-availability-and-comfyui-integration`  
**Last event:** 2026-06-02 · 1 dated since 2026-06-02 · **Researched:** 2026-09-07 · confidence: medium

## What it is

Bernini is a ByteDance video generation and editing framework for practitioners who need a local alternative to a renderer-only Wan workflow.

- Full Bernini / v2: Qwen2.5-VL 7B semantic planning plus a Wan2.2-T2V-A14B renderer for t2i, i2i, t2v, v2v, rv2v, and r2v.
- Bernini-R: the renderer-only Wan line for simpler inference and the maintained ComfyUI templates.

The official reference environment is H100, CUDA 12.6, and Python 3.11.2. Video scripts default to eight processes and 480p, 16 fps, 81 frames. Use full v2 for complex multi-step edits; use Bernini-R only when its narrower renderer scope or ComfyUI path is the goal.

## Development line

- **2026-06-02 — Bernini model and ComfyUI workflow resources linked.** On 2026-06-02, a dated Bernini entry linked the project website and the ByteDance/Bernini model repository on Hugging Face. It also linked a Bernini testing workflow JSON and a Bernini directory in Kijai's WanVideo Comfy FP8 scaled repository. Together, these resources mark a step toward model access and ComfyUI use.

## What changed

- 2026-05-22 — Bernini paper introduced the semantic-planner-plus-DiT-renderer architecture.
- 2026-06-01 — Bernini-R code and weights opened as the renderer-only line.
- 2026-06-02 — Diffusers-format, config-only loading guidance landed for the initial renderer release.
- 2026-06-09 — Bernini-R gained a Wan2.1-based 1.3B variant for simpler edits.
- 2026-06-11 — full Bernini inference code and weights added the Qwen planner to the Wan renderer.
- 2026-06-12 — R2V gained SA3D RoPE interpolation for more than five reference images.
- 2026-06-13 — the early Kijai ComfyUI conversion directory was deleted.
- 2026-07-13 — Bernini-R training code was released.
- 2026-08-13 — Bernini-Diffusers-v2 appeared with a warmed-up planner connector and revised vendor-reported reference-editing results.

## How to use this

1. Choose the artifact first. Use full `Bernini-Diffusers-v2` for semantic planning and complex edits; use `Bernini-R-Diffusers` only for renderer-only work.
  — <https://github.com/bytedance/Bernini/blob/main/docs/bernini.md>
2. Clone the official repository and install its pinned dependencies. Install the required VeOmni package without dependencies so it cannot replace the pinned PyTorch build.
  — <https://github.com/bytedance/Bernini>
3. Download `ByteDance/Bernini-Diffusers-v2`, pass that directory through `--config`, and begin with a bundled image case before moving to video or reference-guided cases.
  — <https://huggingface.co/ByteDance/Bernini-Diffusers-v2>
4. Use the maintained task scripts and case JSONs for t2i, i2i, t2v, v2v, rv2v, or r2v. The full-pipeline scripts carry the task-specific sampling defaults.
  — <https://github.com/bytedance/Bernini/blob/main/docs/bernini.md>
5. For ComfyUI, use the maintained Bernini-R video workflow and the Comfy-Org Bernini-R repack. It is a renderer-only route, not evidence of full-v2 support.
  — <https://github.com/Comfy-Org/workflow_templates/blob/main/templates/video_bernini_r_video_editing.json>

## Best practices

- Prefer the self-contained Diffusers directory with `--config`. Only use separate high- and low-noise checkpoint flags when deliberately using that older layout.
  — <https://github.com/bytedance/Bernini/blob/main/docs/bernini_r.md>
- Keep the repository’s pinned PyTorch/CUDA environment intact when adding VeOmni by installing VeOmni with `--no-deps`.
  — <https://github.com/bytedance/Bernini>
- Start from the supplied scripts and case files rather than inventing sampling settings. Their video default is 480p, 16 fps, and 81 frames.
  — <https://github.com/bytedance/Bernini/blob/main/docs/bernini.md>
- In the ComfyUI template, use Turbo only for prompt iteration, disable it for final output, and state both the intended edit and the elements that must remain unchanged.
  — <https://github.com/Comfy-Org/workflow_templates/blob/main/templates/video_bernini_r_image_editing.json>

## Superseded by this

- 2026-06-11 — treating all of Bernini as the renderer-only June release is obsolete. Full Bernini added an MLLM semantic planner.
- 2026-06-13 — the Kijai `WanVideo_comfy_fp8_scaled/tree/main/Bernini` download path is obsolete. Its history records deletion of that directory.
- 2026-08-13 — the original full `Bernini-Diffusers` checkpoint is no longer the sole current full-pipeline recommendation for reference-guided work. v2 describes a changed connector-training recipe, not a compatibility guarantee.

## Still unknown

- We could not fetch the original `https://huggingface.co/ByteDance/Bernini` address, so its relationship to the current Bernini-R repositories is not proven.
- We could not retrieve the supplied GitHub workflow attachment. Its node graph, exact model files, and runtime result remain unverified.
- The direct Kijai Bernini folder now returns 404. Its history proves the early high/low FP8 conversion and deletion, but not current compatibility or checksums.
- We found no first-party dated v2 launch announcement. A same-day repository update and a dated secondary report corroborate the 2026-08-13 date; the official model card confirms v2 contents but does not announce that date.
- The inspected ComfyUI material has maintained Bernini-R templates, while full-v2 support was still an open request. This does not rule out unreviewed community v2 workflows.
- We found no independent current performance run for the exact v2 environment. Vendor benchmark numbers are not a deployment guarantee.

## Sources

| source | title | read |
|---|---|---|
| https://bernini-ai.github.io/ | Bernini: Latent Semantic Planning for Video Diffusion | 2026-09-07 |
| https://github.com/bytedance/Bernini | GitHub - bytedance/Bernini | 2026-09-07 |
| https://github.com/bytedance/Bernini/blob/main/docs/bernini.md | Bernini — full pipeline | 2026-09-07 |
| https://github.com/bytedance/Bernini/blob/main/docs/bernini_r.md | Bernini-R — renderer only | 2026-09-07 |
| https://github.com/bytedance/Bernini/blob/main/docs/bernini_r_train.md | Bernini-R training guide | 2026-09-07 |
| https://github.com/bytedance/Bernini/commits/main | Commits · bytedance/Bernini | 2026-09-07 |
| https://huggingface.co/ByteDance/Bernini-Diffusers-v2 | ByteDance/Bernini-Diffusers-v2 · Hugging Face | 2026-09-07 |
| https://huggingface.co/Kijai/WanVideo_comfy_fp8_scaled/commits/main/Bernini | Commits · Kijai/WanVideo_comfy_fp8_scaled — Bernini | 2026-09-07 |
| https://huggingface.co/Comfy-Org/Bernini-R | Comfy-Org/Bernini-R · Hugging Face | 2026-09-07 |
| https://github.com/Comfy-Org/workflow_templates/blob/main/templates/video_bernini_r_video_editing.json | Comfy-Org Bernini-R video-editing workflow template | 2026-09-07 |
| https://github.com/Comfy-Org/workflow_templates/blob/main/templates/video_bernini_r_image_editing.json | Comfy-Org Bernini-R image-editing workflow template | 2026-09-07 |
| https://github.com/Comfy-Org/ComfyUI/issues/15702 | Consider support for ByteDance Bernini-Diffusers-v2 · Issue #15702 | 2026-09-07 |
| https://www.orcarouter.ai/blog/bernini-diffusers-v2-shipped-quietly | Bernini-Diffusers-v2: ByteDance's Quiet Checkpoint Drop | 2026-09-07 |

## Agent brief {#agent-brief}

- **Subject:** `project:bernini`, thread `model-availability-and-comfyui-integration`, 1 dated events 2026-06-02 → 2026-06-02.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
