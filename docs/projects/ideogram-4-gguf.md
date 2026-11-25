---
title: ideogram-4-GGUF — Ideogram 4
category: projects
date: 2026-06-11
tags: [ideogram-4, ideogram-4-gguf, project]
aliases: ["ideogram-4-GGUF"]
---

# ideogram-4-GGUF — Ideogram 4

**Development line:** `project:ideogram-4-gguf` · thread `ideogram-4`  
**Last event:** 2026-06-11 · 1 dated since 2026-06-11 · **Researched:** 2026-09-05 · confidence: medium

## What it is

ideogram-4-GGUF is a pair of Q4_0 GGUF weights for the main and unconditional diffusion components of Ideogram 4.0, built for local runs instead of the API.

- Base model: Ideogram 4.0, 9.3B DiT.
- Runtime: stable-diffusion.cpp.
- Dependencies: Qwen3-VL-8B-Instruct in GGUF and Flux2 AE VAE.

The main Q4_0 file takes 5.64 GB. This is neither an official Ideogram checkpoint nor a ready ComfyUI setup.

It works for a CLI experiment with stable-diffusion.cpp. For reproducible production, verify the exact versions of all four components and the base model license.

## Development line

- **2026-06-11 — Ideogram 4 GGUF repository linked on Hugging Face.** Q4_0 GGUF conversions of two diffusion components of Ideogram 4.0 for stable-diffusion.cpp.

## What changed

2026-06-11 — The link records the availability of leejet/ideogram-4-GGUF: Q4_0 GGUF conversions of two diffusion components of Ideogram 4.0 for stable-diffusion.cpp.

## How to use this

As of 2026-06-11, practitioners can use the linked Hugging Face repository as a candidate source for Ideogram 4 GGUF artifacts, while independently verifying its files, license, provenance, and runtime compatibility before use.

1. Download both linked Q4_0 files: conditional `ideogram4-Q4_0.gguf` and unconditional `ideogram4_uncond-Q4_0.gguf`.
  — <https://huggingface.co/leejet/ideogram-4-GGUF>
2. Build or download compatible `sd-cli` from stable-diffusion.cpp; the project claims support for Ideogram4 and GGUF format.
  — <https://github.com/leejet/stable-diffusion.cpp>
3. Pass both diffusion files, the GGUF version of Qwen3-VL-8B-Instruct, and `flux2_ae.safetensors` into `sd-cli`; the prompt must be valid JSON following the model card example.
  — <https://huggingface.co/leejet/ideogram-4-GGUF>

## Best practices

- Write structured JSON prompts instead of plain strings, because the source pipeline was trained on and validates that schema.
  — <https://ideogram.ai/blog/ideogram-4.0/>
- Pin runtime versions and all dependent weights, because stable-diffusion.cpp explicitly warns that CLI options and APIs change often.
  — <https://github.com/leejet/stable-diffusion.cpp>
- Check the original Ideogram 4.0 license before commercial use, because the GGUF card inherits it rather than setting its own.
  — <https://huggingface.co/leejet/ideogram-4-GGUF>

## Superseded by this

- 2026-06-03 — No local GGUF variant existed before Ideogram 4.0; the official base release provided open FP8 and NF4 weights, but not this third-party GGUF package.
- 2026-06-04 — The assumption that Ideogram 4 cannot run in stable-diffusion.cpp is obsolete; the runtime announced support for Ideogram4.

## Still unknown

- No independent dated primary source confirms the publication date of the GGUF conversion for the 2026-06-11 event: the public model card reflects repository state, while the Hugging Face profile shows an update on 2026-06-07.
- Exact hashes, current stable-diffusion.cpp compatibility with these files, and output quality relative to the original FP8 and NF4 weights remain unverified.
- The official 2026-06-03 release of Ideogram 4.0 and the third-party GGUF package are separate entities: the former released the base model, and the latter converted it for a specific runtime.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/leejet/ideogram-4-GGUF | leejet/ideogram-4-GGUF | 2026-09-05 |
| https://github.com/leejet/stable-diffusion.cpp | leejet/stable-diffusion.cpp | 2026-09-05 |
| https://ideogram.ai/blog/ideogram-4.0/ | Ideogram 4.0 Technical Details: Open model at the forefront of design | 2026-09-05 |
| https://ideogram.ai/news/ideogram-4.0/ | Ideogram releases 4.0, a frontier image model with open weights, and a new brand for the company | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:ideogram-4-gguf`, thread `ideogram-4`, 1 dated events 2026-06-11 → 2026-06-11.
- **Practical note:** As of 2026-06-11, practitioners can use the linked Hugging Face repository as a candidate source for Ideogram 4 GGUF artifacts, while independently verifying its files, license, provenance, and runtime compatibility before use.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
