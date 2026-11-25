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

Canon UltraReal is an Apache-2.0 LoRA for Krea-2-Raw text-to-image workflows, trained on Canon 1Ds photographs. At 114 MB, it adjusts color rendering, subject separation, and bokeh across 28 mm, 50 mm, 100 mm, and 500 mm focal lengths. It acts as a narrow camera-look adapter rather than a standalone checkpoint or general realism model.

## Development line

- **2026-07-19 — Canon UltraReal was publicly listed on Civitai and Hugging Face.** Civitai and Hugging Face added public model pages on 2026-07-19. This marks a public distribution listing milestone for the project, though the source does not list a version, weight change, release notes, or original message text.

## What changed

2026-07-19 — Canon UltraReal became available as a LoRA for Krea-2-Raw; the primary model card defines the repository, base model, Canon 1Ds training source, and recommended 0.8 strength.

No separately dated successor release was verified. The single hosted weight file is canon_krea2.safetensors (114 MB; SHA-256 3295dec59ab1195631fe9b3dd3493ba9c1546056da86179cc3119c4b029420ce).

## How to use this

From 2026-07-19, use the linked Civitai and Hugging Face pages to discover Canon UltraReal, and verify version and usage details directly from those resources.

1. Install or update Diffusers, Transformers, and Accelerate, then load Danrisi/Canon_UltraReal with DiffusionPipeline on CUDA; use bfloat16 if supported.  
  — <https://huggingface.co/Danrisi/Canon_UltraReal>
2. Set Krea-2-Raw as the base model and set the LoRA strength to 0.8.  
  — <https://huggingface.co/Danrisi/Canon_UltraReal>
3. Start prompts with c2n0n, describe the scene, and add focal-length cues like 28mm or 50mm.  
  — <https://huggingface.co/Danrisi/Canon_UltraReal>

## Best practices

- Start at 0.8 LoRA strength, adjusting only after comparing outputs against the intended subject and composition.  
  — <https://huggingface.co/Danrisi/Canon_UltraReal>
- Choose focal lengths intentionally: training images span 28 mm, 50 mm, 100 mm, and 500 mm, so character shifts with lens cues and framing.  
  — <https://huggingface.co/Danrisi/Canon_UltraReal>
- Stay on Krea-2-Raw; the model card does not establish compatibility with other base models.  
  — <https://huggingface.co/Danrisi/Canon_UltraReal>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- Civitai mirror URL for the 2026-07-19 event failed to load, leaving version metadata, publication timestamp, and workflow guidance unverified.
- No first-party source matches the 2026-07-19 publication timestamp directly. The primary model card confirms technical scope and base model, but not the exact release-day record.
- The output schema lacks event_findings and new_events fields, so event evidence appears under what_changed and unknowns.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/Danrisi/Canon_UltraReal | Danrisi/Canon_UltraReal · Hugging Face | 2026-09-05 |
| https://huggingface.co/Danrisi/Canon_UltraReal/blob/main/canon_krea2.safetensors | canon_krea2.safetensors · Danrisi/Canon_UltraReal | 2026-09-05 |
| https://huggingface.co/Danrisi/Canon_UltraReal/commit/847c2a1cc7e191f5b3d4451deec984044f4ceabc | Update model via HuggingFace Uploader · Danrisi/Canon_UltraReal | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:canon-ultrareal`, thread `canon-ultrareal-public-model-listing`, 1 dated events 2026-07-19 → 2026-07-19.
- **Practical note:** From 2026-07-19, practitioners should use the linked Civitai and Hugging Face pages as the recorded public discovery points for Canon UltraReal, while verifying the exact version and usage details directly from those resources.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.