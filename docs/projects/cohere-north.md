---
title: North
category: projects
date: 2026-06-30
tags: [cohere, cohere-north, north-mini-code, project]
aliases: ["North"]
---

# North

**Development line:** `project:cohere-north` · thread `north-mini-code`  
**Last event:** 2026-06-30 · 1 dated since 2026-06-30 · **Researched:** 2026-09-05 · confidence: high

## What it is

Cohere North Mini Code is a text sparse-MoE model for engineers who need a local alternative to small agentic code models.
- Code generation.
- Terminal tool execution.
- Multi-step agentic tasks.
- Structured tool calls.

30B parameters total, 3B active, 256K context, generation up to 64K tokens. It fits controlled coding-agent harnesses, but requires a compatible runtime and correct propagation of tool and thinking state.

## Development line

- **2026-06-30 — CohereLabs published North Mini Code 1.0 model pages on Hugging Face.** On 2026-06-30, the development line points to Hugging Face pages for North-Mini-Code-1.0 and a w4a16 variant. This marks a material distribution step for the North Mini Code line because it identifies both a base model artifact and a separately named variant.

## What changed

- 2026-06-09 — Cohere released North-Mini-Code-1.0 under Apache 2.0 as the first North family model for agentic workflows, providing BF16, FP8, and W4A16 weights.
- 2026-06-30 — Repositories were recorded for the base North-Mini-Code-1.0 model and its W4A16 variant, confirming them as formats of one release rather than two separate models.

## How to use this

From 2026-06-30, check the distinct Hugging Face pages for the base North-Mini-Code-1.0 artifact and its w4a16 variant rather than assuming a single undifferentiated model package.

1. Load base weights via Transformers, apply the built-in chat template to messages, and generate responses using sampling parameters from the model card.
  — <https://huggingface.co/CohereLabs/North-Mini-Code-1.0>
2. Run the model through vLLM and call `/v1/chat/completions` for an OpenAI-compatible local endpoint.
  — <https://huggingface.co/CohereLabs/North-Mini-Code-1.0>
3. Define functions with JSON Schema for a tool-using agent, pass tool results with the `tool` role, and continue generation.
  — <https://huggingface.co/CohereLabs/North-Mini-Code-1.0>

## Best practices

- Set `temperature=1.0` and `top_p=0.95` as recommended by Cohere for generation.
  — <https://huggingface.co/CohereLabs/North-Mini-Code-1.0>
- Pass interleaved-thinking content into subsequent agent steps and conversation turns, as the model card notes this improves output quality.
  — <https://huggingface.co/CohereLabs/North-Mini-Code-1.0>
- Check version compatibility for vLLM: the model card specifies vLLM main and `cohere_melody>=0.9.0` so responses parse correctly.
  — <https://huggingface.co/CohereLabs/North-Mini-Code-1.0>

## Superseded by this

- 2026-06-30 — Treating North-Mini-Code-1.0 and North-Mini-Code-1.0-w4a16 as independent releases is obsolete: W4A16 is a weight format for North Mini Code 1.0.

## Still unknown

- Primary sources confirm the 2026-06-09 release, but do not explain what distinct change occurred on 2026-06-30; that date may reflect repo recording or link publication rather than a new model release.
- The system response schema lacks `event_findings` and `new_events` fields; details on earlier releases and event clarification appear in `what_changed` and `unknowns`.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/CohereLabs/North-Mini-Code-1.0 | CohereLabs/North-Mini-Code-1.0 · Hugging Face | 2026-09-05 |
| https://huggingface.co/CohereLabs/North-Mini-Code-1.0-w4a16 | CohereLabs/North-Mini-Code-1.0-w4a16 · Hugging Face | 2026-09-05 |
| https://cohere.com/blog/north-mini-code | North Mini Code: Agentic Coding for Developers | Cohere | 2026-09-05 |
| https://docs.cohere.com/v2/changelog | Release Notes | Cohere | 2026-09-05 |
| https://github.com/cohere-ai/cohere-developer-experience/blob/main/fern/pages/models/north/north-mini-code-1.0.mdx | north-mini-code-1.0.mdx | Cohere developer experience | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:cohere-north`, thread `north-mini-code`, 1 dated events 2026-06-30 → 2026-06-30.
- **Practical note:** From 2026-06-30, practitioners assessing North Mini Code should check the distinct Hugging Face pages for the base North-Mini-Code-1.0 artifact and its w4a16 variant, rather than assuming a single undifferentiated model package.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.