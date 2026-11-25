---
title: Realism_Engine_Ideogram_4 — Ideogram LoRA
category: projects
date: 2026-06-11
tags: [ideogram-lora, project, realism-engine-ideogram-4]
aliases: ["Realism_Engine_Ideogram_4"]
---

# Realism_Engine_Ideogram_4 — Ideogram LoRA

**Development line:** `project:realism-engine-ideogram-4` · thread `ideogram-lora`  
**Last event:** 2026-06-11 · 1 dated since 2026-06-11 · **Researched:** 2026-09-07 · confidence: medium

## What it is

Realism_Engine_Ideogram_4 is a user-hosted set of LoRA weight files and ComfyUI workflow JSON for local Ideogram 4 inference.

- includes V1, beta, V2, V3, V4, and V5 safetensors;
- its V2 workflow applies the V2 weight through model-only LoRA loaders to Ideogram 4 branches.

Limit: the repository is 21.5 GB, has an empty README, an unknown adapter license, and no hosted inference provider. Treat it as a locally tested community asset, not a documented or commercially cleared Ideogram 4 release.

## Development line

- **2026-06-11 — Hugging Face project resource recorded for Realism_Engine_Ideogram_4.** On 2026-06-11, this development line included a link to a Hugging Face resource for Realism_Engine_Ideogram_4. The dated link establishes an identifiable project resource associated with the line at that time. The available evidence does not establish its release status, contents, training method, or compatibility.

## What changed

- 2026-06-09 — The repository was initialized and early assets/workflows were uploaded.
- 2026-06-11 — Realism_Engine_Ideogram_V2.safetensors and rei4_v2_workflow.json were added.
- 2026-06-12 — Realism_Engine_Ideogram_V3.safetensors was added.
- 2026-06-14 — Realism_Engine_Ideogram_V4.safetensors was added.
- 2026-06-19 — Realism_Engine_Ideogram_V5.safetensors was added; it is the latest named weight in the visible history.

## How to use this

1. Check the adapter page before downloading: its README is empty and its license is unknown, so it is not commercially cleared by its own documentation.
  — <https://huggingface.co/RazzzHF/Realism_Engine_Ideogram_4>
2. Install the ComfyUI Ideogram 4 components in the documented diffusion_models, text_encoders, and vae folders.
  — <https://huggingface.co/Comfy-Org/Ideogram-4>
3. For the documented V2 path, download Realism_Engine_Ideogram_V2.safetensors, import rei4_v2_workflow.json, and point its two ModelOnly LoRA loaders to that exact weight.
  — <https://huggingface.co/RazzzHF/Realism_Engine_Ideogram_4/blob/main/rei4_v2_workflow.json>
4. Pin the tested weight and workflow together: V3–V5 are later uploads, but the repository does not document their changes or workflow compatibility.
  — <https://huggingface.co/RazzzHF/Realism_Engine_Ideogram_4/commits/main>

## Best practices

- Keep the V2 tuning scoped to V2: the supplied workflow says 0.50–0.90 is its sweet spot and warns against going above 0.90.
  — <https://huggingface.co/RazzzHF/Realism_Engine_Ideogram_4/blob/main/rei4_v2_workflow.json>
- Use both conditional and unconditional Ideogram weights for the intended quality path; the Comfy-Org maintainer says omitting the unconditional branch usually loses quality, while a lower-precision unconditional model can reduce memory use.
  — <https://huggingface.co/Comfy-Org/Ideogram-4/discussions/1>
- Use Ideogram 4's structured JSON captions for controlled tests and retain the seed for reproducibility.
  — <https://huggingface.co/docs/diffusers/main/api/pipelines/ideogram4>
- Keep commercial use on hold until rights are cleared: the ComfyUI base package is under the Ideogram non-commercial model agreement.
  — <https://huggingface.co/Comfy-Org/Ideogram-4>

## Superseded by this

- None documented as of 2026-09-07: the 2026-06-19 V5 upload does not state that it supersedes V1, beta, V2, V3, or V4, which remain available.

## Still unknown

- The adapter's training data, training method, intended use, and license are undocumented.
- No release notes, benchmarks, or workflow mapping establish which of V3–V5 should replace V2.
- No first-party Chinese-language documentation or usable independent Chinese operating evidence was found.
- No independent local run was performed; the V2 settings are workflow-author guidance, not a verified recipe for later weights.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/RazzzHF/Realism_Engine_Ideogram_4 | RazzzHF/Realism_Engine_Ideogram_4 — model page | 2026-09-07 |
| https://huggingface.co/RazzzHF/Realism_Engine_Ideogram_4/tree/main | RazzzHF/Realism_Engine_Ideogram_4 — current file tree | 2026-09-07 |
| https://huggingface.co/RazzzHF/Realism_Engine_Ideogram_4/commits/main | RazzzHF/Realism_Engine_Ideogram_4 — commit history, entries dated 2026-06-09 to 2026-06-19 | 2026-09-07 |
| https://huggingface.co/RazzzHF/Realism_Engine_Ideogram_4/blob/main/rei4_v2_workflow.json | rei4_v2_workflow.json — V2 workflow, uploaded 2026-06-11 | 2026-09-07 |
| https://huggingface.co/Comfy-Org/Ideogram-4 | Comfy-Org/Ideogram-4 — ComfyUI package and license | 2026-09-07 |
| https://huggingface.co/Comfy-Org/Ideogram-4/discussions/1 | Comfy-Org Ideogram-4 discussion — paired-model and sampler guidance | 2026-09-07 |
| https://huggingface.co/docs/diffusers/main/api/pipelines/ideogram4 | Hugging Face Diffusers — Ideogram 4 pipeline documentation | 2026-09-07 |

## Agent brief {#agent-brief}

- **Subject:** `project:realism-engine-ideogram-4`, thread `ideogram-lora`, 1 dated events 2026-06-11 → 2026-06-11.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
