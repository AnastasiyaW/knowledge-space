---
title: Kimi K2
category: projects
date: 2025-07-13
tags: [kimi, kimi-k2, kimi-k2-development, project]
aliases: ["Kimi", "Kimi K2"]
---

# Kimi K2

**Development line:** `project:kimi-k2` · thread `kimi-k2-development`  
**Last event:** 2025-07-13 · 1 dated since 2025-07-13 · **Researched:** 2026-09-04 · confidence: medium

## What it is

Kimi K2 — an open-weight MoE language-model family for builders who need a self-hosted text-and-tool-use model rather than the current Kimi hosted API.

- Kimi-K2-Base for research and fine-tuning.
- Kimi-K2-Instruct for chat and agent loops.
- Local OpenAI-compatible chat and tool calling; the former hosted API also offered Anthropic compatibility.

## Development line

- **2025-07-13 — Kimi K2 public availability references.** On 2025-07-13, official project, source-code, model-publisher, web-chat, and mobile-access links recorded Kimi K2. These dated references mark a public-availability milestone for the project. The exact release wording and version details remain to be verified from source research.

## What changed

- 2025-07-13 — Kimi K2 Base and Instruct were already public. Official records date the initial model and kimi-k2-0711-preview API release to 2025-07-11, so 13 July is not a distinct K2 version.
- 2025-08-01 — kimi-k2-turbo-preview added a high-speed hosted option, with a time-limited 50% launch promotion.

## How to use this

From 2025-07-13, evaluate Kimi K2 from official project and source references instead of third-party summaries. Confirm developer-platform model availability separately before integrating an API.

1. Choose the route first: retain K2 only for an existing self-hosted or reproducible deployment. For a new hosted integration, choose a currently listed Kimi model, because all kimi-k2 API IDs are discontinued.
  — <https://platform.kimi.ai/docs/models>
2. For local chat or agents, start from the official Kimi-K2-Instruct checkpoint rather than Base. Base is the foundation checkpoint for research and custom post-training.
  — <https://github.com/MoonshotAI/Kimi-K2>
3. Serve the K2 weights with one of the officially recommended engines: vLLM, SGLang, KTransformers, or TensorRT-LLM.
  — <https://huggingface.co/moonshotai/Kimi-K2-Instruct>
4. Use the local chat-completions interface and start Kimi-K2-Instruct at temperature 0.6. Keep a system prompt when no special instruction is needed.
  — <https://huggingface.co/moonshotai/Kimi-K2-Instruct>
5. For a tool loop, send the available tool schemas, execute the returned call in your application, append its result, and continue until the completion no longer requests tools.
  — <https://github.com/MoonshotAI/Kimi-K2>
6. For a new Kimi API call, create an API key, use the current model ID from the model list, and call POST /v1/chat/completions at https://api.moonshot.ai/v1.
  — <https://platform.kimi.ai/docs/api/chat>

## Best practices

- State the task, relevant context, output format, and target length explicitly. The prompt guide warns that the model cannot infer unstated requirements.
  — <https://platform.kimi.ai/docs/guide/prompt-best-practice>
- Separate supplied material with delimiters and spell out ordered steps for multi-stage work.
  — <https://platform.kimi.ai/docs/guide/prompt-best-practice>
- Use representative examples when output style or schema matters. Require answers to stay within supplied reference material when grounding is required.
  — <https://platform.kimi.ai/docs/guide/prompt-best-practice>
- Do not treat tool calling as one request: retain the returned assistant tool-call message and append each tool result before asking the model to continue.
  — <https://huggingface.co/moonshotai/Kimi-K2-Instruct>
- Do not hard-code historical K2 preview names for hosted use. They are discontinued and unsupported, so migrate and recheck the current model list.
  — <https://platform.kimi.ai/docs/models>
- Budget API traffic at the user level, not the key level: concurrency, RPM, TPM, and TPD limits are shared across models.
  — <https://platform.moonshot.ai/docs/introduction#text-generation-model>

## Superseded by this

- 2025-09-05 — kimi-k2-0711-preview as the current hosted K2 model for new integrations; superseded by kimi-k2-0905-preview.
- 2026-05-25 — any kimi-k2 preview, Turbo, or Thinking identifier as a supported hosted API target; the K2 series was discontinued.
- 2026-08-31 — kimi-k2.5 as a supported API fallback for K2-era integrations; it was retired.

## Still unknown

- The source links establish K2's public artifacts and releases, but not the exact claims made in the 2025-07-13 and 2025-08-01 messages whose text is unavailable.
- First-party dates conflict. The platform changelog, the 0905 announcement, and the research catalog place the original K2 release on 2025-07-11, while the current Kimi Agent overview says 2025-09-05. The latter may mean the 0905 update, but it is not explicitly corrected there.
- The July 2025 Kimi app links and the K2 model release are related product surfaces, but they do not prove which model version powered each app client on that day.
- Official sources retire K2 from the hosted API, but do not state a post-retirement maintenance or security-support policy for self-hosted K2 weights.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/MoonshotAI/Kimi-K2 | Kimi K2 is the large language model series developed by Moonshot AI team | 2026-09-04 |
| https://moonshotai.github.io/Kimi-K2/ | Kimi K2: Open Agentic Intelligence | 2026-09-04 |
| https://huggingface.co/moonshotai/Kimi-K2-Instruct | moonshotai/Kimi-K2-Instruct | 2026-09-04 |
| https://platform.moonshot.ai/docs/introduction#text-generation-model | Main Concepts - Kimi API Platform | 2026-09-04 |
| https://platform.kimi.ai/docs/models | Model List - Kimi API Platform | 2026-09-04 |
| https://platform.kimi.ai/docs/api/chat | Chat Completions API - Kimi API Platform | 2026-09-04 |
| https://platform.kimi.ai/docs/guide/prompt-best-practice | Best Practices for Prompts - Kimi API Platform | 2026-09-04 |
| https://platform.kimi.ai/blog/posts/changelog | Kimi Open Platform: New Feature Release Log | 2026-09-04 |
| https://www.kimi.com/en/blog/kimi-k2 | Kimi K2: Open Agentic Intelligence | 2026-09-04 |
| https://arxiv.org/abs/2507.20534 | Kimi K2: Open Agentic Intelligence | 2026-09-04 |
| https://platform.kimi.com/blog/posts/kimi-k2-0905 | Kimi K2 模型更新，带来更强的代码能力、更快的 API | 2026-09-04 |
| https://www.kimi.com/en/blog/kimi-k2-thinking | Introducing Kimi K2 Thinking | 2026-09-04 |
| https://www.kimi.com/en/blog/kimi-k2-5 | Kimi K2.5: Visual Agentic Intelligence | 2026-09-04 |
| https://www.kimi.com/en/blog/kimi-k2-6 | Kimi K2.6: Advancing Open-Source Coding | 2026-09-04 |
| https://www.kimi.com/en/blog/kimi-k3 | Kimi K3: Open Frontier Intelligence | 2026-09-04 |
| https://www.kimi.com/en/blog/ | Kimi Research Blog | Moonshot AI | 2026-09-04 |
| https://github.com/MoonshotAI/kimi-help-center/blob/master/en-US/agent/overview.md | Kimi Agent overview | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:kimi-k2`, thread `kimi-k2-development`, 1 dated events 2025-07-13 → 2025-07-13.
- **Practical note:** From 2025-07-13, evaluate Kimi K2 from official project and source references instead of third-party summaries. Confirm developer-platform model availability separately before integrating an API.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
