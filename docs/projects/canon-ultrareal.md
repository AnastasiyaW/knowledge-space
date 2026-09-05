---
title: Canon UltraReal
category: projects
date: 2026-07-19
tags: [canon-ultrareal, canon-ultrareal-public-model-listing, project]
aliases: ["Canon UltraReal"]
---

# Canon UltraReal

**Development line:** `project:canon-ultrareal` · thread `canon-ultrareal-public-model-listing`  
**Last event:** 2026-07-19 · 1 dated since 2026-07-19 · **Researched:** 2026-09-05 · confidence: high

## What it is

Canon UltraReal is an Apache-2.0 LoRA for Krea-2-Raw text-to-image workflows, trained on Canon 1Ds photographs. It tunes color rendering, subject separation, and bokeh. Training images cover 28 mm, 50 mm, 100 mm, and 500 mm lenses. The file size is 114 MB. It is a narrow camera-look adapter rather than a standalone checkpoint or a general realism replacement.

## Development line

- **2026-07-19 — Canon UltraReal was publicly listed on Civitai and Hugging Face.** On 2026-07-19, public model pages for Canon UltraReal went live on Civitai and Hugging Face. That listing marks a public milestone for the project. The available evidence does not show a version number, weight changes, release notes, or original message text.

## What changed

2026-07-19 — Canon UltraReal became available as a Krea-2-Raw LoRA. The primary model card names the repository, base model, Canon 1Ds training source, and recommended 0.8 strength.

We found no separately dated successor release. The hosted weight file is canon_krea2.safetensors (114 MB; SHA-256 3295dec59ab1195631fe9b3dd3493ba9c1546056da86179cc3119c4b029420ce).

## How to use this

From 2026-07-19, use the linked Civitai and Hugging Face pages to find Canon UltraReal, and verify versions and usage instructions there.

1. Install or update Diffusers, Transformers, and Accelerate, then load Danrisi/Canon_UltraReal with DiffusionPipeline on CUDA; use bfloat16 if supported.
  — <https://huggingface.co/Danrisi/Canon_UltraReal>
2. Use Krea-2-Raw as the base model and apply the LoRA at strength 0.8.
  — <https://huggingface.co/Danrisi/Canon_UltraReal>
3. Start prompts with c2n0n, then describe the scene and optionally add focal-length cues such as 28mm or 50mm.
  — <https://huggingface.co/Danrisi/Canon_UltraReal>

## Best practices

- Treat 0.8 as the starting LoRA strength; adjust only after comparing outputs against the intended subject and composition.
  — <https://huggingface.co/Danrisi/Canon_UltraReal>
- Use focal-length language deliberately: the training set spans 28 mm, 50 mm, 100 mm, and 500 mm, so output character can change with composition and lens cues.
  — <https://huggingface.co/Danrisi/Canon_UltraReal>
- Keep the workflow on Krea-2-Raw; compatibility with other base models is not established by the model card.
  — <https://huggingface.co/Danrisi/Canon_UltraReal>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- We could not retrieve the Civitai mirror URL for the 2026-07-19 event, so its version metadata, publication timestamp, and workflow guidance were not used.
- No first-party source matches the 2026-07-19 timestamp. The primary model card confirms the model and scope, but not the exact launch date.
- The schema lacks event_findings or new_events fields, so event evidence sits in what_changed and unknowns.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/Danrisi/Canon_UltraReal | Danrisi/Canon_UltraReal · Hugging Face | 2026-09-05 |
| https://huggingface.co/Danrisi/Canon_UltraReal/blob/main/canon_krea2.safetensors | canon_krea2.safetensors · Danrisi/Canon_UltraReal | 2026-09-05 |
| https://huggingface.co/Danrisi/Canon_UltraReal/commit/847c2a1cc7e191f5b3d4451deec984044f4ceabc | Update model via HuggingFace Uploader · Danrisi/Canon_UltraReal | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:canon-ultrareal`, thread `canon-ultrareal-public-model-listing`, 1 dated events 2026-07-19 → 2026-07-19.
- **Practical note:** From 2026-07-19, use the linked Civitai and Hugging Face pages to locate Canon UltraReal, and verify version and usage details directly from those sources.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
