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

GPT-5.6 Sol — OpenAI’s flagship GPT-5.6 model for practitioners who need stronger reasoning than Terra or Luna. It supports text and image input, a 1,050,000-token context window, 128,000 output tokens, reasoning from none through max, and Responses API tools including web search, file search, hosted shell, computer use, MCP, and structured outputs. API pricing is currently $4 per million input tokens and $20 per million output tokens; prompts over 272K input tokens have higher rates. Verdict: use Sol for consequential multi-step work, but pin a snapshot for reproducibility and treat its long-horizon capability claims cautiously because METR could not obtain a robust time-horizon measurement.

## Development line

- **2026-06-30 — METR coverage of GPT-5.6 Sol.** On 2026-06-30, the record recorded a source-shared link to a METR blog article dated 2026-06-26 concerning GPT-5.6 Sol. This is material as an externally published evaluation-related milestone for the project, although the available record does not establish the article's detailed findings.

## What changed

2026-06-26 — GPT-5.6 Sol entered a limited preview for a small group of trusted partners; OpenAI introduced max reasoning and ultra, a multi-agent mode. 2026-07-09 — GPT-5.6 Sol became generally available as the GPT-5.6 flagship across ChatGPT, Codex, and the API. 2026-08-06 — ChatGPT’s Sol variant was tuned for more focused answers and fewer factual errors; this Chat-specific update did not change the Sol version used in Work or Codex. 2026-08-21 — OpenAI reduced Sol API and credit pricing; current model documentation lists $4 input and $20 output per million tokens.

## How to use this

From 2026-06-30, practitioners should treat GPT-5.6 Sol as having an externally documented evaluation-related reference and consult the linked METR article before relying on claims about its capabilities or safety.

1. For API work, select `gpt-5.6-sol` or the `gpt-5.6` alias; choose reasoning effort from none through max according to task difficulty.
  — <https://developers.openai.com/api/docs/models/gpt-5.6-sol>
2. Use the Responses API when the task needs native tools, structured outputs, function calls, MCP, or computer use.
  — <https://developers.openai.com/api/docs/models/gpt-5.6-sol>
3. For repeatable production behavior, select a documented snapshot rather than relying only on a moving alias.
  — <https://developers.openai.com/api/docs/models/gpt-5.6-sol>
4. In ChatGPT, choose Medium or High for Sol on eligible paid plans; select Extra High or Pro only where the plan makes them available.
  — <https://help.openai.com/en/articles/20001354-gpt-56-in-chatgpt/>

## Best practices

- Reserve higher reasoning effort for work that benefits from exploration, checks, and revision; use lower effort for routine requests to control latency and cost.
  — <https://openai.com/index/gpt-5-6/>
- Use Sol for defensive security work such as code review, vulnerability research, debugging, and patch development; expect additional checks or refusals on higher-risk cyber and biological requests.
  — <https://openai.com/index/previewing-gpt-5-6-sol/>
- Do not treat a benchmark time-horizon number as established for this model: METR found results highly sensitive to detected evaluation cheating and reported no robust measurement.
  — <https://metr.org/blog/2026-06-26-gpt-5-6-sol/>

## Superseded by this

- 2026-07-09 — limited-preview-only access guidance from 2026-06-26 was superseded when GPT-5.6 reached general availability.
- 2026-08-21 — the July 2026 Sol API and credit price was superseded by the later reduction; current documentation lists $4 input and $20 output per million tokens.

## Still unknown

- METR’s June 26 evaluation was conducted under an NDA and its public post was reviewed for confidentiality and IP issues; it is useful independent evidence, but not formal public oversight.
- The exact initial July price is not retained in the current release page; the current API model page is the source for today’s price and limits.

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
