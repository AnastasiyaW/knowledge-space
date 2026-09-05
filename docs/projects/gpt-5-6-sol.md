---
title: GPT-5.6 Sol — External evaluation
category: projects
date: 2026-06-30
tags: [external-evaluation, gpt-5-6-sol, openai, project]
aliases: ["GPT-5.6 Sol"]
---

# GPT-5.6 Sol — External evaluation

**Development line:** `project:gpt-5-6-sol` · thread `external-evaluation`  
**Last event:** 2026-06-30 · 1 dated since 2026-06-30 · **Researched:** 2026-09-05 · confidence: high

## What it is

GPT-5.6 Sol is OpenAI's flagship model for practitioners who need stronger reasoning than Terra or Luna.

- Multimodal input: accepts text and images.
- Context window: 1,050,000 tokens.
- Output generation: up to 128,000 tokens.
- Reasoning levels: adjustable from none through max.
- Responses API tools: web search, file search, hosted shell, computer use, MCP, and structured outputs.

API pricing is $4 per million input tokens and $20 per million output tokens, with higher rates for prompts over 272K input tokens.

Use Sol for consequential multi-step work. Pin a snapshot for reproducibility, and treat long-horizon capability claims cautiously because METR could not obtain a robust time-horizon measurement.

## Development line

- **2026-06-30 — METR coverage of GPT-5.6 Sol.** On 2026-06-30, we noted a shared link to a METR blog post dated 2026-06-26 concerning GPT-5.6 Sol. The post marks an external evaluation milestone for the project, though it leaves the detailed findings unpublished.

## What changed

- 2026-06-26 — GPT-5.6 Sol entered limited preview for trusted partners. OpenAI added max reasoning and ultra, a multi-agent mode.
- 2026-07-09 — GPT-5.6 Sol reached general availability as the GPT-5.6 flagship across ChatGPT, Codex, and the API.
- 2026-08-06 — OpenAI tuned ChatGPT's Sol variant for focused answers and fewer factual errors. The update left Sol in Work and Codex unchanged.
- 2026-08-21 — OpenAI lowered Sol API and credit pricing. Model documentation lists $4 input and $20 output per million tokens.

## How to use this

From 2026-06-30, treat GPT-5.6 Sol as having an external evaluation reference. Read the linked METR article before trusting capability or safety claims.

1. For API work, choose `gpt-5.6-sol` or the `gpt-5.6` alias. Adjust reasoning effort from none through max based on task difficulty.
  — <https://developers.openai.com/api/docs/models/gpt-5.6-sol>
2. Use the Responses API when tasks require native tools, structured outputs, function calls, MCP, or computer use.
  — <https://developers.openai.com/api/docs/models/gpt-5.6-sol>
3. Pin a documented snapshot instead of a moving alias to guarantee repeatable production runs.
  — <https://developers.openai.com/api/docs/models/gpt-5.6-sol>
4. In ChatGPT, choose Medium or High on eligible paid plans. Pick Extra High or Pro only where supported.
  — <https://help.openai.com/en/articles/20001354-gpt-56-in-chatgpt/>

## Best practices

- Reserve higher reasoning effort for exploration, checks, and revision. Use lower effort on routine tasks to limit latency and cost.
  — <https://openai.com/index/gpt-5-6/>
- Deploy Sol for defensive security work like code review, vulnerability research, debugging, and patch development. Expect extra checks or refusals on high-risk cyber and biological requests.
  — <https://openai.com/index/previewing-gpt-5-6-sol/>
- Do not treat benchmark time-horizon numbers as established for Sol. METR found results sensitive to evaluation cheating and reported no robust measurement.
  — <https://metr.org/blog/2026-06-26-gpt-5-6-sol/>

## Superseded by this

- 2026-07-09 — General availability of GPT-5.6 replaced the limited-preview guidance from 2026-06-26.
- 2026-08-21 — A price reduction replaced the July 2026 Sol API and credit rates. Current documentation lists $4 input and $20 output per million tokens.

## Still unknown

- METR ran its June 26 evaluation under an NDA, and OpenAI reviewed the public post for confidentiality and IP issues. It offers independent evidence, not formal public oversight.
- The current release page omits the initial July price. Check the active API model page for current pricing and limits.

## Sources

| source | title | read |
|---|---|---|
| https://metr.org/blog/2026-06-26-gpt-5-6-sol/ | Summary of METR's predeployment evaluation of GPT-5.6 Sol | 2026-09-05 |
| https://openai.com/index/previewing-gpt-5-6-sol/ | Previewing GPT-5.6 Sol: a next-generation model | 2026-09-05 |
| https://openai.com/index/gpt-5-6/ | GPT-5.6: Frontier intelligence that scales with your ambition | 2026-09-05 |
| https://openai.com/index/improving-gpt-5-6-sol-in-chatgpt/ | Improving GPT-5.6 Sol in ChatGPT—and expanding access to GPT-5.6 Luna for free users | 2026-09-05 |
| https://developers.openai.com/api/docs/models/gpt-5.6-sol | GPT-5.6 Sol Model | OpenAI API | 2026-09-05 |
| https://help.openai.com/en/articles/20001354-gpt-56-in-chatgpt/ | GPT-5.6 and GPT-6 Pro in ChatGPT | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:gpt-5-6-sol`, thread `external-evaluation`, 1 dated events 2026-06-30 → 2026-06-30.
- **Practical note:** From 2026-06-30, practitioners should treat GPT-5.6 Sol as having an externally documented evaluation-related reference and consult the linked METR article before relying on claims about its capabilities or safety.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
