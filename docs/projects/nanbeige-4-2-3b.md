---
title: Nanbeige4.2-3B
category: projects
date: 2026-07-26
tags: [nanbeige, nanbeige-4-2-3b, nanbeige4-2-3b, project]
aliases: ["Nanbeige4.2-3B"]
---

# Nanbeige4.2-3B

**Development line:** `project:nanbeige-4-2-3b` · thread `nanbeige4-2-3b`  
**Last event:** 2026-07-26 · 1 dated since 2026-07-26 · **Researched:** 2026-09-06 · confidence: medium

## What it is

Nanbeige4.2-3B is a BF16 model for teams ready to run their own runtime and verify target tasks.

- Reasoning mode for multi-step reasoning.
- Chat template for structured chat turns.
- Tool calling for function execution.
- Local runtimes across Transformers, SGLang, vLLM, and llama.cpp.

3B non-embedding parameters against 4B on the Hub card; claimed context reaches 262144 tokens.

The model fits controlled local deployments, but custom code and long context require a pinned version and target environment tests.

## Development line

- **2026-07-26 — Nanbeige4.2-3B public model and inference resources were linked.** On 2026-07-26, a development update linked the Nanbeige4.2-3B Hugging Face model page, a filtered listing of related quantized base-model entries, and an inference space. This establishes a dated public access point for the model and its related deployment options.

## What changed

- 2026-07-21 — Hub history records the initial commit and a separate upload of modeling_nanbeige.py, confirming early repository and code access without establishing the exact timestamp for all weights.
- 2026-07-24 — Nanbeige Lab submitted v1 of the technical report to arXiv.
- 2026-07-26 — configuration_nanbeige.py was added to the repository.
- 2026-07-27 — Nanbeige4.2 support merged into llama.cpp master, but the associated CI run failed.
- 2026-07-28 — The README replaced the local technical report PDF link with an arXiv link.
- 2026-08-14 — An independent paper described fixes for running through Transformers on Apple Silicon/MPS.
- 2026-09-04 — The stable release of llama.cpp v0.4.0 listed support for nanbeige4.2-3B.

## How to use this

As of 2026-07-26, practitioners should consult the Nanbeige4.2-3B Hugging Face model page and related quantized variants before choosing an artifact, and use the linked inference space to assess accessible inference availability.

1. Create a local environment with transformers==4.45.1 and load AutoTokenizer with use_fast=false, then AutoModelForCausalLM with torch_dtype="auto", device_map="auto", and trust_remote_code=true.
  — <https://huggingface.co/Nanbeige/Nanbeige4.2-3B>
2. Pass messages through tokenizer.apply_chat_template with add_generation_prompt=true, tokenize without special tokens, and start with a short generation request.
  — <https://huggingface.co/Nanbeige/Nanbeige4.2-3B>
3. For an OpenAI-compatible server, use developer-specified SGLang nbg42 or vLLM nanbeige42 forks with nanbeige reasoning and tool-call parsers.
  — <https://huggingface.co/Nanbeige/Nanbeige4.2-3B>
4. For GGUF deployment, take llama.cpp v0.4.0 as the documented baseline with built-in Nanbeige4.2-3B support and verify the chosen quantization with a short smoke test.
  — <https://github.com/ggml-org/llama.cpp/releases>

## Best practices

- Check the author and code before enabling trust_remote_code, then pin the full commit hash via revision: the Hub recommends this to protect against upstream code changes.
  — <https://huggingface.co/docs/transformers/models>
- Set preserve_thinking=false for standard chat; set it to true for multi-step tool, office, and code tasks. Use the template with tools and prefer tool_call_format="xml" for tool calls.
  — <https://huggingface.co/Nanbeige/Nanbeige4.2-3B>
- Do not treat 262144 tokens as a guaranteed working context; begin with a short target run. An independent paper reported issues with the original checkpoint under Transformers on Apple Silicon/MPS.
  — <https://arxiv.org/abs/2608.13987>
- Do not rely on the outdated assumption that stock llama.cpp lacks support: pin v0.4.0 or verify a newer version separately.
  — <https://github.com/ggml-org/llama.cpp/releases>

## Superseded by this

- {"claim":"Датировать исходную публикацию Nanbeige4.2-3B 2026-07-26.","obsolete_since":"2026-09-06 (историческая проверка)","source_url":"https://huggingface.co/Nanbeige/Nanbeige4.2-3B/commits/main"}
- {"claim":"У stock llama.cpp нет поддержки Nanbeige4.2-3B.","obsolete_since":"2026-09-04","source_url":"https://github.com/ggml-org/llama.cpp/releases"}
- {"claim":"Локальный PDF в Hub README является канонической ссылкой на технический отчёт.","obsolete_since":"2026-07-28","source_url":"https://huggingface.co/Nanbeige/Nanbeige4.2-3B/commit/f56ec5a9650268aa098496734743c25ea778bd2d"}

## Still unknown

- Exact initial public release time of the weights lacks an absolute timestamp: Hub history shows only the calendar day.
- The inference-labs Space lacks official confirmation, and we could not verify its API, hardware configuration, or live output.
- The checked model card lists no provider endpoint; this reflects current status rather than proof against external hosting.
- Official Nanbeige4.2-3B-DSpark is described as a 0.8B draft model to accelerate the 3B model, but Hub shows only relative commit times; an absolute first release date is not in the timeline.
- Minimum VRAM, latency, and production quality for specific runtimes remain unverified by direct testing.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/Nanbeige/Nanbeige4.2-3B | Nanbeige/Nanbeige4.2-3B · Hugging Face | 2026-09-06 |
| https://huggingface.co/Nanbeige/Nanbeige4.2-3B/commits/main | Commits · Nanbeige/Nanbeige4.2-3B | 2026-09-06 |
| https://arxiv.org/abs/2607.22083 | Nanbeige4.2-3B: Unlocking Agentic Capabilities in a Compact Model | 2026-09-06 |
| https://github.com/ggml-org/llama.cpp/actions/runs/30278196993 | model: Add support for Nanbeige4.2 (#25994) · ggml-org/llama.cpp@b77d646 · GitHub | 2026-09-06 |
| https://huggingface.co/Nanbeige/Nanbeige4.2-3B/commit/f56ec5a9650268aa098496734743c25ea778bd2d | Update README.md · Nanbeige/Nanbeige4.2-3B at f56ec5a | 2026-09-06 |
| https://arxiv.org/abs/2608.13987 | Nanbeige4.2-3B on Apple Silicon: Fixing Deployment Bugs and Decreasing Looped Transformer Memory Overhead | 2026-09-06 |
| https://github.com/ggml-org/llama.cpp/releases | Releases · ggml-org/llama.cpp | 2026-09-06 |
| https://huggingface.co/docs/transformers/models | Loading models · Hugging Face | 2026-09-06 |
| https://huggingface.co/Nanbeige/Nanbeige4.2-3B-DSpark | Nanbeige4.2-3B-DSpark · Hugging Face | 2026-09-06 |

## Agent brief {#agent-brief}

- **Subject:** `project:nanbeige-4-2-3b`, thread `nanbeige4-2-3b`, 1 dated events 2026-07-26 → 2026-07-26.
- **Practical note:** As of 2026-07-26, practitioners should consult the Nanbeige4.2-3B Hugging Face model page and related quantized variants before choosing an artifact, and use the linked inference space to assess accessible inference availability.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.