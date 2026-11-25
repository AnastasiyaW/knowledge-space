---
title: SenseNova — U1 MoT model and infographic artifacts
category: projects
date: 2026-08-01
tags: [project, sensenova, u1-mot-model-and-infographic]
aliases: ["SenseNova"]
---

# SenseNova — U1 MoT model and infographic artifacts

**Development line:** `project:sensenova` · thread `u1-mot-model-and-infographic`  
**Last event:** 2026-08-01 · 1 dated since 2026-08-01 · **Researched:** 2026-09-06 · confidence: high

## What it is

SenseNova U1 is an Apache-2.0 OpenSenseNova model family for practitioners running visual creation locally.

Abilities:
- Text-to-image.
- Image editing.
- Interleaved image-text generation.
- Visual understanding.

The current U1.5-8B-MoT card lists 18B BF16 parameters and no Hugging Face Inference Provider. Use U1.5 for general creation and editing, and Infographic-V3 only for infographic-specific work.

## Development line

- **2026-08-01 — SenseNova linked U1 MoT preview and infographic artifacts on Hugging Face.** On 2026-08-01, SenseNova added links to Hugging Face pages and Spaces for SenseNova-U1.5-8B-MoT-Preview and SenseNova-U1-8B-MoT-Infographic-V3. These links mark a model and demo milestone. They do not establish release status, technical changes, or artifact capabilities.

## What changed

- 2026-07-16 — SenseNova-U1-8B-MoT-Infographic-V3 added integrated infographic generation and editing: local text/content plus global style/layout edits.
- 2026-08-01 — SenseNova-U1.5-8B-MoT-Preview was a July 31 Preview for broader generation and editing; it was paired with the earlier V3 card, not released together with it.
- 2026-08-04 — A community-maintained 19.9 GB Q8 GGUF made the Preview easier to run but did not change official weights.
- 2026-08-20 — SenseNova-U1.5-8B-MoT became the current official release; its matching 8-step LoRA added a faster path.
- 2026-09-01 — A community 21.2 GB Q8 GGUF appeared for the final U1.5 checkpoint.

## How to use this

1. For a no-install evaluation, open the current U1.5 card's linked SenseNova-Studio playground; treat it as a workflow trial rather than production performance evidence.
  — <https://huggingface.co/sensenova/SenseNova-U1.5-8B-MoT>
2. For local use, clone OpenSenseNova/SenseNova-U1, run uv sync in its environment, and use the U1.5-8B-MoT model path with the text-to-image or image-editing entrypoint.
  — <https://huggingface.co/sensenova/SenseNova-U1.5-8B-MoT>
3. Choose a trained resolution bucket and configure device_map or the project VRAM mode before scaling resolution or batch size.
  — <https://github.com/OpenSenseNova/SenseNova-U1/blob/main/examples/README.md>
4. For infographic generation or editing, select SenseNova-U1-8B-MoT-Infographic-V3 rather than assuming the general U1.5 checkpoint has the same task specialization; the sensenova Space is an interactive V3 route.
  — <https://huggingface.co/spaces/sensenova/sensenova-u1-infographic-v3>

## Best practices

- Use a direct prompt for a clear task with few constraints. Use Image PE for complex composition, copy, counts, layout, or reference planning, and vary seeds when diversity matters.
  — <https://github.com/OpenSenseNova/SenseNova-U1/blob/main/docs/u1.5_best_practices.md>
- For a complex edit, state the requested change and everything that must remain unchanged. Order multiple reference images deliberately and describe each image's role.
  — <https://github.com/OpenSenseNova/SenseNova-U1/blob/main/docs/u1.5_best_practices.md>
- Prefer the documented approximately 2K resolution buckets. Arbitrary width-height combinations can reduce quality.
  — <https://github.com/OpenSenseNova/SenseNova-U1/blob/main/examples/README.md>
- Inspect dense text, exact count/layout, anatomy, and broad multi-reference edits manually. Lower cfg_scale when detail or colour is over-emphasized.
  — <https://huggingface.co/sensenova/SenseNova-U1.5-8B-MoT>

## Superseded by this

- 2026-08-20 — Treating SenseNova-U1.5-8B-MoT-Preview as the current general-purpose U1.5 checkpoint is obsolete.

## Still unknown

- SenseNova is a broader SenseTime brand; the verified material identifies the OpenSenseNova U1 family but does not establish that U1.5 is the same product as commercial SenseNova 6.x or U1 Pro.
- The Preview demo is owned by hugging-apps rather than sensenova; its accessible page does not prove which checkpoint it currently runs, its uptime, or a production service commitment.
- The sources claim native 4K, but the checked examples document approximately 2K trained buckets and no independent 3840x2160 quality result for a specified production workload.
- No current hosted API pricing, SLA, or Hugging Face Inference Provider was verified for the final U1.5 checkpoint.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/sensenova/SenseNova-U1.5-8B-MoT-Preview | sensenova/SenseNova-U1.5-8B-MoT-Preview | 2026-09-06 |
| https://huggingface.co/spaces/hugging-apps/sensenova-sensenova-u1-5-8b-mot-preview | SenseNova-U1.5-8B-MoT (Preview) - a Hugging Face Space by hugging-apps | 2026-09-06 |
| https://huggingface.co/sensenova/SenseNova-U1-8B-MoT-Infographic-V3 | sensenova/SenseNova-U1-8B-MoT-Infographic-V3 | 2026-09-06 |
| https://huggingface.co/spaces/sensenova/sensenova-u1-infographic-v3 | SenseNova U1 Infographic V3 - a Hugging Face Space by sensenova | 2026-09-06 |
| https://github.com/OpenSenseNova/SenseNova-U1 | OpenSenseNova/SenseNova-U1: SenseNova-U series with NEO-unify | 2026-09-06 |
| https://huggingface.co/sensenova/SenseNova-U1.5-8B-MoT | sensenova/SenseNova-U1.5-8B-MoT | 2026-09-06 |
| https://github.com/OpenSenseNova/SenseNova-U1/blob/main/docs/u1.5_best_practices.md | SenseNova-U1.5 Cookbook | 2026-09-06 |
| https://github.com/OpenSenseNova/SenseNova-U1/blob/main/examples/README.md | SenseNova-U1 reference inference examples | 2026-09-06 |

## Agent brief {#agent-brief}

- **Subject:** `project:sensenova`, thread `u1-mot-model-and-infographic`, 1 dated events 2026-08-01 → 2026-08-01.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
