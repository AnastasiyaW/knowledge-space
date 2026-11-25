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

Huihui-Qwen3.8-27B-abliterated is an abliterated variant of base Qwen3.8-27B for developers who need an open multimodal checkpoint compatible with Transformers, vLLM, or SGLang.

- Chat for conversational text generation.
- Image processing for visual inputs.
- OpenAI-compatible serving for remote API calls.

Safety filtering is substantially reduced, and the model card recommends research and controlled environments. It is not a replacement for a safe production model.

## Development line

- **2026-08-17 — Huihui-Qwen3.8-27B-abliterated became publicly available through Hugging Face.** The artifact contains 18 safetensors files and takes 55,6 GB; the README specifies that MTP and the vision component remain unmodified.

## What changed

2026-08-17 — verified revision d42ca89 is pinned: the artifact contains 18 safetensors files and takes 55,6 GB; the README clarifies that MTP and the vision component remain unmodified.

The model card reports that ablation applies only to layers 18–51 to preserve most original performance. We can pin the previous version to revision d42ca89.

## How to use this

As of 2026-08-17, we can treat Huihui-Qwen3.8-27B-abliterated as a publicly discoverable model line and evaluate the linked model artifact, related quantized variants, and ZeroGPU Space; the dated links alone do not support choosing a specific variant or relying on performance claims.

1. For multimodal local runs, load AutoProcessor and AutoModelForMultimodalLM, format messages with text and images through the chat template, and call generate.
  — <https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated>
2. For an OpenAI-compatible endpoint, install vLLM, run `vllm serve "huihui-ai/Huihui-Qwen3.8-27B-abliterated"`, and send requests to `/v1/chat/completions`.
  — <https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated>
3. For SGLang, run `python3 -m sglang.launch_server --model-path "huihui-ai/Huihui-Qwen3.8-27B-abliterated"`, and use the endpoint on the chosen port.
  — <https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated>

## Best practices

- Pin the revision for reproducible runs: the model card points directly to d42ca89 for the earlier version.
  — <https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated>
- Keep manual output review and avoid using the checkpoint directly in public or high-risk products: the author warns of reduced safety filtering.
  — <https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated>
- For llama.cpp, Ollama, or LM Studio, pick separate derivative quantizations rather than treating the BF16 repository as ready for these runtimes.
  — <https://huggingface.co/models?other=base_model%3Aquantized%3Ahuihui-ai%2FHuihui-Qwen3.8-27B-abliterated>

## Superseded by this

- After 2026-08-17, describing pinned revision d42ca89 as having only MTP unmodified became obsolete: its README clarified that the vision component is also unmodified.

## Still unknown

- In the available primary history, the exact calendar timestamp for commit d42ca89 is relative ("19 days ago"); it matches 2026-08-17 on the check date, but the primary source gave no ISO timestamp.
- Whether the ZeroGPU Space from the event is an official launch path or represents the same model revision remains unconfirmed.
- The date of the subsequent ablation change to layers 18–51 does not appear in the available primary output, so we do not list it as a separate dated event.

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
