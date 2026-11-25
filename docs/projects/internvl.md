---
title: InternVL
category: projects
tags: [internvl, internvl-model-releases, project]
aliases: ["InternVL", "InternVL 3.5"]
---

# InternVL

**Development line:** `project:internvl` · thread `internvl-model-releases`  
**Events:** 2 dated, 2024-12-11 → 2025-08-27 · **Researched:** 2026-09-04 · confidence: high

## What it is

InternVL is an open-weight vision-language model family for teams that need to analyse images, documents, multiple images, video and GUI states in a self-hosted workflow.

- Image, document, chart and OCR question answering
- Multi-image and video conversation
- Visual grounding, multilingual vision-language work, plus GUI and embodied tasks in 3.5

The current 3.5 line ranges from 1.1B to 240.7B total parameters; the official guide places models through 30B on one A100, 38B on two, and 241B on eight. Choose a complete no-suffix 3.5 checkpoint for new local work; use Flash when visual-token cost is the bottleneck.

## Development line

- **2024-12-11 — InternVL2.5-78B model and collection released.** On 2024-12-11, the project released InternVL2.5-78B with a model collection, repository, project site, and demo. The linked sources do not establish benchmark results or feature details.
- **2025-08-27 — InternVL3.5 paper and model collection released.** On 2025-08-27, the project published the InternVL3.5 paper, official collection, repository, and chat. The linked sources do not establish the paper's detailed claims, supported variants, or deployment guidance.

## What changed

On 2024-12-05 (recorded 2024-12-11), InternVL2.5 became a 1B–78B family. It kept the earlier core architecture but revised training, test-time scaling, and data-quality work. The 78B checkpoint paired a 6B vision encoder with Qwen2.5-72B.

On 2025-08-26 (recorded 2025-08-27), InternVL3.5 replaced that core line with 1B–241B checkpoints in both project-native and standard Hugging Face formats. It introduced CascadeRL, the Visual Resolution Router, decoupled vision-language deployment, Qwen3/GPT-OSS language backbones, and GUI/embodied capabilities.

On 2025-08-30, the project opened CascadeRL training code and data for its GPT-OSS 20B-A4B variant. After 2025-08-27, an official InternVL3.5-Flash checkpoint became available. Its card documents ViCO plus visual-resolution routing to reduce visual tokens by 50%; the reviewed sources did not establish its exact first release date.

## How to use this

On 2024-12-11, evaluate the official InternVL2.5-78B model page and collection when selecting an InternVL2.5 release. By 2025-08-27, review the linked InternVL3.5 paper and official collection before picking a newer InternVL line instead of assuming the earlier line remains the default.

1. Choose a complete no-suffix InternVL3.5 checkpoint for normal inference; choose the Flash variant when visual-token cost matters.
  — <https://huggingface.co/OpenGVLab/InternVL3_5-8B-Flash>
2. Use the format deliberately: the project-native checkpoint loads through AutoModel with remote code, while the HF format follows standard Transformers conventions. Install transformers >=4.52.1; the 20B-A4B variant needs >=4.55.0.
  — <https://huggingface.co/OpenGVLab/InternVL3_5-8B-Instruct>
3. For image chat, apply the supplied 448px dynamic tiling preprocessing, convert the tiles to bf16, and send the prompt with an <image> placeholder through model.chat.
  — <https://huggingface.co/OpenGVLab/InternVL3_5-8B-Instruct>
4. For video, sample a bounded number of frames, prefix each with FrameN: <image>, and pass the matching num_patches_list to the chat call.
  — <https://huggingface.co/OpenGVLab/InternVL3_5-8B-Instruct>
5. For a service, deploy through LMDeploy or vLLM with an OpenAI-compatible endpoint; use vLLM for the GPT-OSS 20B-A4B variant.
  — <https://huggingface.co/OpenGVLab/InternVL3_5-8B-Instruct>

## Best practices

- For deployment, prefer the no-suffix checkpoint: it is the version that completed the full pipeline, unlike Pretrained, Instruct and MPO stage checkpoints.
  — <https://huggingface.co/OpenGVLab/InternVL3_5-8B-Flash>
- Plan model size from the documented GPU envelope before downloading: through 30B on one A100, 38B on two, and 241B on eight.
  — <https://huggingface.co/OpenGVLab/InternVL3_5-8B-Instruct>
- Use the documented Transformers version floor; the 2.5-era dependency floor is not sufficient for 3.5.
  — <https://huggingface.co/OpenGVLab/InternVL3_5-8B-Instruct>
- For thinking mode, set do_sample=true and temperature=0.6; the project recommends this to limit repetition.
  — <https://huggingface.co/OpenGVLab/InternVL3_5-8B-Instruct>
- Increase the context window for multi-image prompts and number images in the prompt so the model can distinguish them.
  — <https://huggingface.co/OpenGVLab/InternVL3_5-8B-Instruct>

## Superseded by this

- 2024-12-05 / 2024-12-11: InternVL2.5 is no longer the default for a new core InternVL deployment; use a complete no-suffix InternVL3.5 checkpoint unless legacy compatibility is the deciding constraint.
- The InternVL2.5 transformers>=4.37.2 guidance is obsolete for InternVL3.5: use transformers>=4.52.1, or >=4.55.0 for 20B-A4B.
- 2025-08-26: the 3.5 card's guidance that Flash was still forthcoming is obsolete; an official InternVL3_5-8B-Flash checkpoint is now available.

## Still unknown

- The exact first publication date of InternVL3.5-Flash was not established; current availability is confirmed, but a model-page update date is not necessarily a launch date.
- The reported reasoning gains and token reduction are project-reported benchmark results, not an independent evaluation for a particular workload.
- The public chat frontend was reachable but did not expose an inspectable response to the fetcher, so live hosted-demo behaviour was not verified.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/OpenGVLab/InternVL | OpenGVLab/InternVL | 2026-09-04 |
| https://internvl.github.io/blog/2024-12-05-InternVL-2.5/ | InternVL2.5 | 2026-09-04 |
| https://huggingface.co/OpenGVLab/InternVL2_5-78B | OpenGVLab/InternVL2_5-78B | 2026-09-04 |
| https://internvl.github.io/blog/2025-08-26-InternVL-3.5/ | InternVL3.5 | 2026-09-04 |
| https://huggingface.co/papers/2508.18265 | InternVL3.5: Advancing Open-Source Multimodal Models in Versatility, Reasoning, and Efficiency | 2026-09-04 |
| https://huggingface.co/collections/OpenGVLab/internvl35-68ac87bd52ebe953485927fb | InternVL3.5 — OpenGVLab Collection | 2026-09-04 |
| https://huggingface.co/OpenGVLab/InternVL3_5-8B-Instruct | OpenGVLab/InternVL3_5-8B-Instruct | 2026-09-04 |
| https://huggingface.co/OpenGVLab/InternVL3_5-8B-Flash | OpenGVLab/InternVL3_5-8B-Flash | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:internvl`, thread `internvl-model-releases`, 2 dated events 2024-12-11 → 2025-08-27.
- **Practical note:** As of 2024-12-11, practitioners should evaluate the official InternVL2.5-78B model page and collection when selecting an InternVL2.5 release. As of 2025-08-27, they should review the linked InternVL3.5 paper and official collection before choosing a newer InternVL line, rather than assuming the earlier model line remains the appropriate default.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
