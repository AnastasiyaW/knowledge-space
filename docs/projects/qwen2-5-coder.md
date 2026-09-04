---
title: Qwen2.5-Coder
category: projects
date: 2024-11-12
tags: [project, qwen, qwen2-5-coder, qwen2-5-coder-launch]
aliases: ["Qwen2.5-Coder"]
---

# Qwen2.5-Coder

**Development line:** `project:qwen2-5-coder` · thread `qwen2-5-coder-launch`  
**Last event:** 2024-11-12 · 2 dated since 2024-11-12 · **Researched:** 2026-09-04 · confidence: high

## What it is

Qwen2.5-Coder is a family of six base and instruction-tuned code LLMs from 0.5B to 32B for completion, chat, code repair, and fine-tuning.

- Generation: generates code.
- Reasoning: reasons through programming tasks.
- Repair: fixes bugs in code.
- Fill-in-the-middle: completes code between prefix and suffix.

Context reaches up to 128K, but the standard configuration sets 32K.
The family fits local and self-hosted tasks, but Qwen directs new agentic development to Qwen3-Coder.

## Development line

- **2024-11-12 — Qwen released the Qwen2.5-Coder model family.** To the previously available 1.5B and 7B, Qwen added 0.5B, 3B, 14B, and 32B in base and instruct variants.
- **2024-11-12 — Qwen made a Qwen2.5-Coder Artifacts experience available.** To the previously available 1.5B and 7B, Qwen added 0.5B, 3B, 14B, and 32B in base and instruct variants.

## What changed

2024-11-12 — Qwen opened the full Qwen2.5-Coder lineup: to the previously available 1.5B and 7B, Qwen added 0.5B, 3B, 14B, and 32B in base and instruct variants. 2025-07-22 — Qwen released Qwen3-Coder as the next generation for agentic coding; the original Qwen2.5-Coder repository now redirects to it.

## How to use this

From 2024-11-12, practitioners could evaluate Qwen2.5-Coder through its released model collection, demo, repository, and Artifacts experience rather than relying only on a general chat interface.

1. For interactive tasks, choose an instruction variant of suitable size, load the tokenizer and model through Transformers, and build the request with apply_chat_template.
  — <https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct>
2. For a self-hosted API, serve the chosen checkpoint through vLLM; the server exposes an OpenAI-compatible /v1/chat/completions endpoint.
  — <https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct>
3. For completion or FIM, run the base model; for normal dialogue, use Instruct rather than base.
  — <https://huggingface.co/Qwen/Qwen2.5-Coder-7B>

## Best practices

- Do not use base models for conversation without custom post-training; choose Instruct for an assistant.
  — <https://huggingface.co/Qwen/Qwen2.5-Coder-7B>
- Enable YaRN only when context above 32K is truly needed: static scaling can hurt short requests.
  — <https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct>
- Update Transformers to at least version 4.37, or loading the Qwen2 architecture fails with KeyError.
  — <https://huggingface.co/Qwen/Qwen2.5-Coder-7B>

## Superseded by this

- 2025-07-22 — Qwen3-Coder became Qwen's current line for agentic coding; Qwen2.5-Coder remains an available set of checkpoints, but its original GitHub repository redirects to Qwen3-Coder.

## Still unknown

- The current status of the public Qwen2.5-Coder-Artifacts Space is paused; its availability history and fitness as a working product remain unconfirmed.
- The 3B license differs: it uses the Qwen Research License, whereas 0.5B, 1.5B, 7B, 14B, and 32B use Apache 2.0.

## Sources

| source | title | read |
|---|---|---|
| https://qwenlm.github.io/blog/qwen2.5-coder-family/ | Qwen2.5-Coder Series: Powerful, Diverse, Practical. | 2026-09-05 |
| https://arxiv.org/abs/2409.12186 | Qwen2.5-Coder Technical Report | 2026-09-05 |
| https://huggingface.co/Qwen/Qwen2.5-Coder-7B | Qwen/Qwen2.5-Coder-7B model card | 2026-09-05 |
| https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct | Qwen/Qwen2.5-Coder-32B-Instruct model card | 2026-09-05 |
| https://github.com/QwenLM/Qwen2.5-Coder | QwenLM/Qwen2.5-Coder repository redirect | 2026-09-05 |
| https://qwenlm.github.io/blog/qwen3-coder/ | Qwen3-Coder: Agentic Coding in the World | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:qwen2-5-coder`, thread `qwen2-5-coder-launch`, 2 dated events 2024-11-12 → 2024-11-12.
- **Practical note:** From 2024-11-12, practitioners could evaluate Qwen2.5-Coder through its released model collection, demo, repository, and Artifacts experience rather than relying only on a general chat interface.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.