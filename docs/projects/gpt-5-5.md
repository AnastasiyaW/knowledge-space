---
title: GPT-5.5
category: projects
date: 2026-04-23
tags: [gpt-5-5, gpt-5-5-announcement, project]
aliases: ["GPT-5.5"]
---

# GPT-5.5

**Development line:** `project:gpt-5-5` · thread `gpt-5-5-announcement`  
**Last event:** 2026-04-23 · 1 dated since 2026-04-23 · **Researched:** 2026-09-06 · confidence: high

## What it is

GPT-5.5 — an OpenAI API model for teams building coding, tool-using, and professional-work agents.

- Supports Responses and Chat Completions, function calling, structured outputs, hosted tools, computer use, and MCP.
- Offers the pinned `gpt-5.5-2026-04-23` snapshot.

1,050,000-token context; 128,000-token maximum output; API Free is unsupported. Retain it for a pinned or evaluated workload, but use GPT-6 Astra as the new-workload baseline.

## Development line

- **2026-04-23 — GPT-5.5 announcement.** On 2026-04-23, an OpenAI announcement marked a public milestone for GPT-5.5. The announcement confirms a dated public step for the project, but does not establish capabilities, availability, pricing, or migration details.

## What changed

- **2026-04-23:** GPT-5.5 began rolling out in ChatGPT and Codex for eligible plans, aimed at coding, computer use, knowledge work, and research.
- **2026-04-24:** GPT-5.5 and GPT-5.5 Pro became available in the API; API-deployment safeguards were added.
- **2026-05-05:** GPT-5.5 Instant replaced GPT-5.3 Instant as ChatGPT’s default and appeared in the API as `chat-latest`.
- **2026-05-07:** GPT-5.5-Cyber entered limited preview for defenders securing critical infrastructure.
- **2026-05-28:** GPT-5.5 Instant received a ChatGPT/API style update; Canvas was removed for Instant and Thinking.
- **2026-06-09:** Instant personalization expanded to ChatGPT Go and Free, with Free using a reduced past-chat set.
- **2026-06-24:** ChatGPT updated Instant for multi-turn context, complex constraints, and decision-oriented conversations.
- **2026-07-06:** GPT-5.5 Instant Mini replaced GPT-5.3 Instant Mini as the ChatGPT fallback after Instant or Auto rate limits.

## How to use this

1. Choose `gpt-5.5` for the maintained alias, or `gpt-5.5-2026-04-23` when behavior must stay pinned; confirm the API usage tier first.
  — <https://developers.openai.com/api/docs/models/gpt-5.5>
2. Use the Responses API for reasoning, tool-calling, or multi-turn work.
  — <https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.5>
3. Start with `reasoning.effort: medium`. Evaluate `low` for latency-sensitive work and raise effort only after representative evaluation.
  — <https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.5>
4. Use Structured Outputs, `previous_response_id` for response state, and a stable prompt prefix for cached repeated traffic.
  — <https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.5>
5. For a new system, establish the accuracy target with GPT-6 Astra, then compare cost and latency before retaining GPT-5.5.
  — <https://developers.openai.com/api/docs/guides/model-selection>

## Best practices

- Treat GPT-5.5 as a new model family. Begin with a fresh, minimal prompt baseline instead of carrying forward an older prompt stack.
  — <https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.5>
- State outcome, success criteria, constraints, evidence rules, output shape, and stop conditions. Avoid procedural instructions unless the path itself is required.
  — <https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.5>
- Use Structured Outputs rather than placing a JSON schema in prompt prose.
  — <https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.5>
- Put stable prompt content first and dynamic context last. Use `prompt_cache_key` consistently and inspect cached-token usage.
  — <https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.5>
- Put tool inputs, side effects, retry safety, and failure modes in tool descriptions. Preserve `phase` exactly if assistant items are replayed manually.
  — <https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.5>

## Superseded by this

- :{

## Still unknown

- Availability, rate limits, and the ChatGPT model picker depend on the account, plan, region, and API tier. We checked no target account.
- GPT-5.5, GPT-5.5 Pro, Thinking, Instant, Cyber, and Instant Mini are distinct variants or access modes. Do not transfer access, safety, or capability claims between them.
- The reviewed Simplified-Chinese launch page established no separate China-specific rollout or regional API entitlement.
- Checked sources contain no official retirement date for the `gpt-5.5` API alias.

## Sources

| source | title | read |
|---|---|---|
| https://openai.com/index/introducing-gpt-5-5/ | Introducing GPT-5.5 | 2026-09-06 |
| https://openai.com/index/gpt-5-5-system-card/ | GPT-5.5 System Card | 2026-09-06 |
| https://openai.com/zh-Hans-CN/index/introducing-gpt-5-5/ | 重磅发布 GPT-5.5 | 2026-09-06 |
| https://developers.openai.com/api/docs/models/gpt-5.5 | GPT-5.5 Model | OpenAI API | 2026-09-06 |
| https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.5 | Model guidance | OpenAI API | 2026-09-06 |
| https://developers.openai.com/api/docs/guides/model-selection | Model selection | OpenAI API | 2026-09-06 |
| https://openai.com/index/gpt-5-5-instant/ | GPT-5.5 Instant: smarter, clearer, and more personalized | 2026-09-06 |
| https://openai.com/index/gpt-5-5-with-trusted-access-for-cyber/ | Scaling Trusted Access for Cyber with GPT-5.5 and GPT-5.5-Cyber | 2026-09-06 |
| https://help.openai.com/en/articles/6825453 | ChatGPT — Release Notes | 2026-09-06 |

## Agent brief {#agent-brief}

- **Subject:** `project:gpt-5-5`, thread `gpt-5-5-announcement`, 1 dated events 2026-04-23 → 2026-04-23.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.