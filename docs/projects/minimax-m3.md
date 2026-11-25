---
title: MiniMax M3
category: projects
date: 2026-06-13
tags: [minimax-m3, project]
aliases: ["MiniMax M3"]
---

# MiniMax M3

**Development line:** `project:minimax-m3` · thread `minimax-m3`  
**Last event:** 2026-06-13 · 1 dated since 2026-06-13 · **Researched:** 2026-09-05 · confidence: medium

## What it is

MiniMax M3 is an open-weight native-multimodal MoE model for developers building coding agents, document/repository analysis, and image or video-input workflows.

- Text, image, and video input.
- Hosted Anthropic-compatible and OpenAI-compatible APIs.
- Local serving through SGLang, vLLM, Transformers, KTransformers, or Unsloth.

1M-token context; about 428B total parameters and 23B activated parameters; the official Hugging Face checkpoint is BF16 under the minimax-community licence.

Start with the hosted API; self-host only after sizing hardware and context capacity.

## Development line

- **2026-06-13 — MiniMax M3 public project, model, and API resources appeared.** On 2026-06-13, MiniMax M3 was linked through a public GitHub project repository, a Hugging Face model page, and MiniMax text-generation documentation. These links connect the project source, model distribution, and usage documentation surfaces.

## What changed

- 2026-06-01 — MiniMax M3 launched in MiniMax Code, Token Plan, and the API; MiniMax said the weights would follow within ten days.
- 2026-06-13 — the public GitHub repository, Hugging Face checkpoint, and API documentation were listed together; the upstream GitHub history shows no separately dated model or documentation change on this date.
- 2026-06-18 — KTransformers was added to the documented local-deployment choices.
- 2026-06-22 — an Unsloth tutorial was added to the documented local-deployment choices.

## How to use this

As of 2026-06-13, evaluate MiniMax M3 against its linked repository, Hugging Face model page, and text-generation documentation before deciding whether to adopt it.

1. Create a MiniMax API or subscription key and select `MiniMax-M3` as the model.
  — <https://platform.minimax.io/docs/guides/text-generation>
2. For the recommended API path, send an Anthropic Messages request to `https://api.minimax.io/anthropic/v1/messages`; use the OpenAI-compatible `/v1` endpoint only when your client requires it.
  — <https://platform.minimax.io/docs/guides/text-generation>
3. Set `thinking` to `adaptive` for mixed workloads, `enabled` for deliberate reasoning, or `disabled` when latency and throughput matter more.
  — <https://github.com/MiniMax-AI/MiniMax-M3>
4. For local inference, download `MiniMaxAI/MiniMax-M3` and serve it with a supported runtime such as SGLang or vLLM.
  — <https://huggingface.co/MiniMaxAI/MiniMax-M3>

## Best practices

- Begin with the official sampling defaults: `temperature=1.0` and `top_p=0.95`.
  — <https://github.com/MiniMax-AI/MiniMax-M3>
- Treat the 1M context window as a deployment target, not an automatic setting: choose accelerator, dtype, parallelism, cache, and maximum context for the actual traffic shape.
  — <https://github.com/vllm-project/vllm-project.github.io/blob/main/_posts/2026-06-12-minimax-m3-vllm.md>
- Probe provider-specific tool support in the exact client before depending on it; an open issue reports that Anthropic-style built-in web search was unsupported despite Messages API compatibility.
  — <https://github.com/MiniMax-AI/MiniMax-M3/issues/23>

## Superseded by this

- 2026-06-01 — guidance that an M2-series model is the latest M-series default is superseded for new M3-targeted long-context, multimodal, coding, and agentic work. Current documentation keeps M2 models available rather than declaring them retired.

## Still unknown

- No first-party release note or upstream commit identifies a distinct MiniMax M3 model, weights, or API change on 2026-06-13; we treat the date as an access-link step, not a launch date.
- The 2026-07-01 and 2026-07-11 README commits have generic messages, so their user-visible changes cannot be stated reliably.
- MiniMax has not published a single current first-party hardware-sizing table for the official M3 BF16 checkpoint across target context lengths.

## Sources

| source | title | read |
|---|---|---|
| https://www.minimax.io/blog/minimax-m3 | MiniMax M3: Frontier Coding, 1M Context, Native Multimodality — All in One Model | 2026-09-05 |
| https://github.com/MiniMax-AI/MiniMax-M3 | MiniMax-AI/MiniMax-M3 | 2026-09-05 |
| https://github.com/MiniMax-AI/MiniMax-M3/commits/main | MiniMax-M3 commit history | 2026-09-05 |
| https://huggingface.co/MiniMaxAI/MiniMax-M3 | MiniMaxAI/MiniMax-M3 model card | 2026-09-05 |
| https://platform.minimax.io/docs/guides/text-generation | Model Invocation — MiniMax API Docs | 2026-09-05 |
| https://github.com/vllm-project/vllm-project.github.io/blob/main/_posts/2026-06-12-minimax-m3-vllm.md | MiniMax M3 in vLLM: Day-0 Serving for 1M-Token Multimodal Reasoning | 2026-09-05 |
| https://github.com/MiniMax-AI/MiniMax-M3/issues/23 | M3 Bug: Anthropic-compatible endpoint does not support the web_search tool | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:minimax-m3`, thread `minimax-m3`, 1 dated events 2026-06-13 → 2026-06-13.
- **Practical note:** As of 2026-06-13, practitioners should evaluate MiniMax M3 against its linked repository, Hugging Face model page, and text-generation documentation before deciding whether to adopt it.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.