---
title: Huihui-Qwen3.8-27B-abliterated — Public model availability
category: projects
date: 2026-08-17
tags: [huihui-ai/huihui-qwen3.8-27b-abliterated, huihui-qwen3-8-27b-abliterated, project, public-model-availability]
aliases: ["Huihui-Qwen3.8-27B-abliterated"]
---

# Huihui-Qwen3.8-27B-abliterated — Public model availability

**Development line:** `project:huihui-qwen3-8-27b-abliterated` · thread `public-model-availability`  
**Last event:** 2026-08-17 · 1 dated since 2026-08-17 · **Researched:** 2026-09-05 · confidence: medium

## What it is

Huihui-Qwen3.8-27B-abliterated is an abliterated variant of base Qwen3.8-27B for developers who need an open checkpoint with text and image input compatible with Transformers, vLLM, or SGLang.

- Chat: handles text dialogue.
- Image processing: accepts visual input.
- Server calls: exposes an OpenAI-compatible endpoint.

Safety filtering is substantially reduced, and the model card recommends research and controlled environments. It is not a replacement for a safe production model.

## Development line

- **2026-08-17 — Huihui-Qwen3.8-27B-abliterated became publicly available through Hugging Face.** The artifact contains 18 safetensors files and takes 55,6 GB. The README clarifies that MTP and the vision component are unmodified.

## What changed

2026-08-17 — verified revision d42ca89 was recorded. The artifact contains 18 safetensors files and takes 55,6 GB. Its README clarifies that MTP and the vision component are unmodified.

The model card reports that ablation applies only to layers 18–51 to preserve most of the original performance. We can pin the earlier version with revision d42ca89.

## How to use this

As of 2026-08-17, we can treat Huihui-Qwen3.8-27B-abliterated as a publicly discoverable model line. We can evaluate the linked model artifact, related quantized variants, and the ZeroGPU Space. The dated links alone do not support choosing a specific variant or relying on performance claims.

1. Load AutoProcessor and AutoModelForMultimodalLM for local multimodal execution. Format text and image messages with the chat template and call generate.
  — <https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated>
2. Install vLLM for an OpenAI-compatible endpoint. Run `vllm serve "huihui-ai/Huihui-Qwen3.8-27B-abliterated"` and send requests to `/v1/chat/completions`.
  — <https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated>
3. Run `python3 -m sglang.launch_server --model-path "huihui-ai/Huihui-Qwen3.8-27B-abliterated"` for SGLang and use the endpoint on the chosen port.
  — <https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated>

## Best practices

- Pin the revision for reproducible runs: the card explicitly points to d42ca89 for the earlier version.
  — <https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated>
- Keep manual output review and do not use the checkpoint directly in public or high-risk products: the author warns of reduced safety filtering.
  — <https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated>
- Pick separate downstream quantizations for llama.cpp, Ollama, or LM Studio. Do not treat the BF16 repository as ready for these runtimes.
  — <https://huggingface.co/models?other=base_model%3Aquantized%3Ahuihui-ai%2FHuihui-Qwen3.8-27B-abliterated>

## Superseded by this

- After 2026-08-17, the description of pinned revision d42ca89 as having only MTP unchanged is obsolete. Its README was updated to clarify that the vision component is also unmodified.

## Still unknown

- In the available primary history, the exact calendar time for commit d42ca89 appears as relative ("19 days ago"). It matches 2026-08-17 on the verification date, but the primary source gave no ISO timestamp.
- Nothing confirms whether the ZeroGPU Space from the event is an official launch route or represents the same model revision.
- The date for changing the ablation range to layers 18–51 is not visible in the available primary output, so we do not record it as a separate dated event.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated | huihui-ai/Huihui-Qwen3.8-27B-abliterated — Hugging Face model card | 2026-09-05 |
| https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated/commit/d42ca8978c5a66e92c3446d46e8adfe03ef692ff | Update README.md · huihui-ai/Huihui-Qwen3.8-27B-abliterated at d42ca89 | 2026-09-05 |
| https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated/tree/d42ca8978c5a66e92c3446d46e8adfe03ef692ff | huihui-ai/Huihui-Qwen3.8-27B-abliterated at d42ca89 | 2026-09-05 |
| https://huggingface.co/models?other=base_model%3Aquantized%3Ahuihui-ai%2FHuihui-Qwen3.8-27B-abliterated | Quantized Models for huihui-ai/Huihui-Qwen3.8-27B-abliterated | 2026-09-05 |
| https://huggingface.co/Qwen/Qwen3.8-27B | Qwen/Qwen3.8-27B — Hugging Face model card | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:huihui-qwen3-8-27b-abliterated`, thread `public-model-availability`, 1 dated events 2026-08-17 → 2026-08-17.
- **Practical note:** As of 2026-08-17, practitioners can treat Huihui-Qwen3.8-27B-abliterated as a publicly discoverable model line and evaluate the linked model artifact, related quantized variants, and ZeroGPU Space; the dated links alone do not support choosing a specific variant or relying on performance claims.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
