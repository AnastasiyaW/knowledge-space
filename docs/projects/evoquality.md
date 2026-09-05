---
title: EvoQuality
category: projects
date: 2026-06-11
tags: [bytedance-evoquality, bytedance-evoquality-development, evoquality, project]
aliases: ["EvoQuality"]
---

# EvoQuality

**Development line:** `project:evoquality` · thread `bytedance-evoquality-development`  
**Last event:** 2026-06-11 · 1 dated since 2026-06-11 · **Researched:** 2026-09-05 · confidence: high

## What it is

EvoQuality is a no-reference image-quality VLM for researchers and image-pipeline teams. It scores one image, compares two images, and gives a voting-based ranking signal for filtering or data cleaning. The released BF16 checkpoint has 8B parameters and covers one self-evolution round. Use it as a perceptual proxy with spot checks, not as an objective or high-stakes decision-maker.

## Development line

- **2026-06-11 — ByteDance published an EvoQuality resource on Hugging Face.** On 2026-06-11, ByteDance published an EvoQuality resource on Hugging Face. We have the public link, but the source does not give the artifact type, version, capabilities, or announcement details.

## What changed

2026-06-11 — EvoQuality weights became available at ByteDance/EvoQuality. The release exposes an 8B BF16 checkpoint trained from Qwen2.5-VL-7B through self-supervised pairwise voting and GRPO.

2025-09-30 — The paper appeared on arXiv. It describes the label-free voting-and-ranking method and reports a 31.8% PLCC improvement over its base VLM in zero-shot IQA evaluation.

## How to use this

From 2026-06-11, use ByteDance/EvoQuality on Hugging Face as the dated public reference point, and confirm artifact type and usage details before adoption.

1. Load `ByteDance/EvoQuality` with Transformers as an image-text-to-text model, submit an image plus the model-card scoring prompt, and parse the final boxed numeric score.
  — <https://huggingface.co/ByteDance/EvoQuality>
2. For a local ranking batch, run the repository pairwise-voting inference script with your checkpoint, image directory, pair CSV, and an explicit voting count.
  — <https://github.com/bytedance/EvoQuality>
3. For serving, start the model with vLLM or SGLang and send image-plus-text chat-completions requests.
  — <https://huggingface.co/ByteDance/EvoQuality>

## Best practices

- Use it for ranking, filtering, data cleaning, and pre-production assessment; combine the score with business signals and manual spot checks.
  — <https://huggingface.co/ByteDance/EvoQuality>
- For pairwise inference, randomize image order to reduce positional bias and keep prompts, sampling count, and decoding settings fixed when comparing runs.
  — <https://huggingface.co/ByteDance/EvoQuality>
- Do not use the output as the sole criterion for moderation, medical imaging, legal evidence, or other high-stakes decisions; domain shift and pseudo-label bias remain stated limitations.
  — <https://huggingface.co/ByteDance/EvoQuality>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The Hugging Face card documents the checkpoint and current use paths, but gives no versioned release-note history; we found no later official EvoQuality checkpoint in the reviewed sources.
- The repository installation snippet uses a placeholder clone URL (`your-organization/evoquality`); use the public repository URL above when cloning.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/ByteDance/EvoQuality | ByteDance/EvoQuality model card | 2026-09-05 |
| https://github.com/bytedance/EvoQuality | bytedance/EvoQuality repository | 2026-09-05 |
| https://arxiv.org/abs/2509.25787 | Self-Evolving Vision-Language Models for Image Quality Assessment via Voting and Ranking | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:evoquality`, thread `bytedance-evoquality-development`, 1 dated events 2026-06-11 → 2026-06-11.
- **Practical note:** From 2026-06-11, use the ByteDance/EvoQuality Hugging Face resource as the dated public reference point for project artifacts, and confirm artifact type and usage details before adoption.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
