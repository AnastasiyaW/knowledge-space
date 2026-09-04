---
title: AuraFlow — AuraFlow model releases
category: projects
tags: [auraflow, auraflow-model-releases, auraflow_release, project]
aliases: ["AuraFlow"]
---

# AuraFlow — AuraFlow model releases

**Development line:** `project:auraflow` · thread `auraflow-model-releases`  
**Events:** 3 dated, 2024-07-12 → 2024-08-15 · **Researched:** 2026-09-04 · confidence: medium

## What it is

AuraFlow — a flow-based text-to-image model for local Diffusers/ComfyUI work or hosted fal inference. - Generates images from text through AuraFlowPipeline. - Exposes a hosted `fal-ai/aura-flow` endpoint. - v0.3 supports varied aspect ratios up to 1536 pixels per dimension. Limit: v0.3 remains labelled beta and the 7B-scale model is costly on consumer hardware. Verdict: use the explicit v0.3 checkpoint for this public line; do not assume a newer successor or production-stability guarantee.

## Development line

- **2024-07-12 — AuraFlow's initial public project references were recorded.** On 2024-07-12, the supplied links recorded AuraFlow through a fal blog page, an official model page, and a playground. This marks the first documented event in the sealed AuraFlow development line. The supplied links alone do not establish its technical claims or capabilities.
- **2024-07-29 — AuraFlow v0.2 was recorded as a new model version.** On 2024-07-29, the supplied official Hugging Face link identified AuraFlow-v0.2. As a distinct versioned reference after the initial AuraFlow event, it is a material step in the project's development line. The supplied links do not establish what changed in v0.2.
- **2024-08-15 — AuraFlow v0.3 was recorded as a subsequent model version.** On 2024-08-15, the supplied official Hugging Face link identified AuraFlow-v0.3. It follows the v0.2 reference in the sealed line and is a further material versioned release. The supplied links do not establish its contents, compatibility, or performance.

## What changed

AuraFlow — development line: - 2024-07-12: v0.1 launched as a fully open flow-based text-to-image model; fal documented native Diffusers and ComfyUI support and a 6.8B architecture. - 2024-07-29: v0.2 was documented as a v0.1 successor trained with more compute. The official collection records its model update as 2024-07-27, so this may distinguish model publication from announcement. - 2024-08-15: v0.3 added more compute, aesthetic-data fine-tuning, and aspect-ratio support up to 1536 pixels per dimension. - Found today: fal’s official collection lists only the unversioned model, v0.2, and v0.3; the live fal endpoint identifies AuraFlow as v0.3 and still labels it beta. Limit: that collection cannot prove no unpublished or differently named successor exists. Verdict: v0.3 is the current documented public mainline, not a confirmed actively evolving release train.

## How to use this

As of 2024-08-15, practitioners should treat AuraFlow as a versioned model line and select the specific official AuraFlow, AuraFlow-v0.2, or AuraFlow-v0.3 reference needed for their workflow rather than assuming releases are interchangeable.

1. Pin `fal/AuraFlow-v0.3` for a new local build; it is the documented current checkpoint in the official collection.
  — <https://huggingface.co/fal/AuraFlow-v0.3>
2. Install current `diffusers`, `transformers`, and `accelerate`, then load `AuraFlowPipeline.from_pretrained("fal/AuraFlow-v0.3", torch_dtype=torch.float16, variant="fp16").to("cuda")`.
  — <https://huggingface.co/fal/AuraFlow-v0.3>
3. Generate with explicit dimensions, 50 inference steps, CFG 3.5, and a fixed generator seed; save the resulting image.
  — <https://huggingface.co/fal/AuraFlow-v0.3>
4. For hosted inference, install `@fal-ai/client`, set `FAL_KEY` in the server environment, call `fal.subscribe("fal-ai/aura-flow", { input: { prompt } })`, and retain the returned request ID.
  — <https://fal.ai/models/fal-ai/aura-flow/api>

## Best practices

- Set steps and CFG explicitly. Start from the v0.3 recipe of 50 steps and CFG 3.5 instead of relying on a library default.
  — <https://huggingface.co/fal/AuraFlow-v0.3>
- When local VRAM is constrained, use the documented 8-bit quantization and balanced device mapping, then compare outputs before adopting the lower-precision path.
  — <https://huggingface.co/docs/diffusers/api/pipelines/aura_flow>
- Keep `FAL_KEY` server-side; use queue status and webhooks rather than blocking for slow requests, and retain the returned seed and expanded prompt for reproducibility.
  — <https://fal.ai/models/fal-ai/aura-flow/api>
- Do not import the published v0.3 ComfyUI workflow unchanged: it currently names `aura_flow_0.2.safetensors`; replace the checkpoint deliberately and validate a test generation.
  — <https://huggingface.co/fal/AuraFlow-v0.3/blob/main/comfy_workflow.json>
- For SimpleTuner fine-tuning, treat its AuraFlow-specific Lycoris LoKr route as the starting point rather than casual full-rank tuning; its guide calls for substantial VRAM/DeepSpeed for full tuning and starts validation at 1024², 30–50 steps, and CFG 3.5–4.0.
  — <https://github.com/bghira/SimpleTuner/blob/main/documentation/quickstart/AURAFLOW.md>

## Superseded by this

- 2024-07-29: AuraFlow v0.2 supersedes the v0.1 checkpoint for the official mainline because it was trained with more compute; retain v0.1 only for legacy reproducibility.
- 2024-08-15: AuraFlow v0.3 supersedes v0.2 as the documented starting checkpoint, adding aesthetic fine-tuning and variable aspect ratios up to 1536 pixels per dimension.
- Current: unversioned `fal/AuraFlow` and v0.2 loading snippets are legacy for a new build; pin `fal/AuraFlow-v0.3` instead. This is a usage recommendation, not a formal deprecation notice.

## Still unknown

- fal’s collection lists three v0.x checkpoints, but that absence cannot prove no unpublished or differently named successor exists.
- The public model and API pages still call v0.3 beta; no current supported-GPU matrix or owned v0.3 run was found, so VRAM and latency are not generalized.
- The current Diffusers reference is internally inconsistent: its call signature shows CFG 3.5 while parameter prose says 5.0. Set CFG explicitly from the v0.3 card/API recipe.
- The v0.3 repository’s published `comfy_workflow.json` names a v0.2 checkpoint, so it is not verified as a v0.3 workflow without local replacement and a test run.
- The Simplified-Chinese lane found a SimpleTuner translation and one community ComfyUI workflow, but no independent, version-locked v0.3 operating measurement; it does not change the documented starting recipe.

## Sources

| source | title | read |
|---|---|---|
| https://blog.fal.ai/auraflow/ | Introducing AuraFlow v0.1, an Open Exploration of Large Rectified Flow Models | 2026-09-04 |
| https://huggingface.co/fal/AuraFlow | fal/AuraFlow · Hugging Face | 2026-09-04 |
| https://huggingface.co/fal/AuraFlow-v0.2 | fal/AuraFlow-v0.2 · Hugging Face | 2026-09-04 |
| https://huggingface.co/fal/AuraFlow-v0.3 | fal/AuraFlow-v0.3 · Hugging Face | 2026-09-04 |
| https://huggingface.co/collections/fal/auraflow | AuraFlow — a fal Collection | 2026-09-04 |
| https://fal.ai/models/fal-ai/aura-flow/api | AuraFlow Text to Image API Docs | fal | 2026-09-04 |
| https://huggingface.co/docs/diffusers/api/pipelines/aura_flow | AuraFlow — Hugging Face Diffusers | 2026-09-04 |
| https://huggingface.co/fal/AuraFlow-v0.3/blob/main/comfy_workflow.json | comfy_workflow.json · fal/AuraFlow-v0.3 | 2026-09-04 |
| https://github.com/bghira/SimpleTuner/blob/main/documentation/quickstart/AURAFLOW.md | Auraflow Quickstart — SimpleTuner | 2026-09-04 |
| https://github.com/bghira/SimpleTuner/blob/main/documentation/quickstart/AURAFLOW.zh.md | Auraflow Quickstart, Simplified Chinese — SimpleTuner | 2026-09-04 |
| https://comfyui.nomadoor.net/zh/basic-workflows/auraflow/ | AuraFlow | Comfy with ComfyUI, Simplified Chinese | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:auraflow`, thread `auraflow-model-releases`, 3 dated events 2024-07-12 → 2024-08-15.
- **Practical note:** As of 2024-08-15, practitioners should treat AuraFlow as a versioned model line and select the specific official AuraFlow, AuraFlow-v0.2, or AuraFlow-v0.3 reference needed for their workflow rather than assuming releases are interchangeable.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
