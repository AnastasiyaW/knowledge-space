---
title: GPT-5.6 Sol Ultra
category: projects

tags: [gpt-5-6-sol-ultra, gpt_5_6_sol_ultra, project]
aliases: ["GPT-5.6 Sol Ultra"]
---

# GPT-5.6 Sol Ultra

**Development line:** `project:gpt-5-6-sol-ultra` · thread `gpt-5-6-sol-ultra`  
**Last event:** - · 0 dated since - · **Researched:** 2026-09-05 · confidence: high

## What it is

GPT-5.6 Sol Ultra is a mode of GPT-5.6 Sol for engineers who need parallel agents.

- Four agents by default
- Tools
- Long context

The API documents model ID `gpt-5.6-sol` with no separate Ultra ID.
Use it for heavy verifiable tasks, not for regular requests.

## Development line

- The dated line is not written up yet. What is known stands in the sections below.

## What changed

- 2026-07-09 — OpenAI released GPT-5.6 to general availability. Sol became the flagship tier. Ultra became a mode with multiple parallel agents.
- 2026-07-12 — A published note on the cycle double cover conjecture proof credited the proof to GPT-5.6 Sol Ultra. It credited the write-up to Codex with GPT-5.6 Sol.
- 2026-07-30 — OpenAI lowered API prices by 20% for Terra and 80% for Luna. Sol Ultra was unaffected by this change.
- 2026-08-21 — OpenAI lowered the Sol API price by more than 20% for the next three months.

## How to use this

No verified practical-use change can be proposed from the dated links alone.

1. Specify model `gpt-5.6-sol` for API use. There is no separate Ultra identifier in the model catalog.
  — <https://developers.openai.com/api/docs/models/gpt-5.6-sol>
2. Select high reasoning effort for a difficult single task. The available levels are none, low, medium, high, xhigh, and max.
  — <https://developers.openai.com/api/docs/models/gpt-5.6-sol>
3. Build an ultra-like run with beta multi-agent in the Responses API for parallel work.
  — <https://openai.com/index/gpt-5-6/>
4. Choose ultra in Codex when the task justifies higher token use. The mode is available on Plus and higher tiers.
  — <https://openai.com/index/gpt-5-6/>

## Best practices

- Do not pass `gpt-5.6-sol-ultra` as an API model ID. Use `gpt-5.6-sol` with a reasoning configuration or a multi-agent workflow.
  — <https://developers.openai.com/api/docs/models/gpt-5.6-sol>
- Evaluate ultra by final result verification. The mode increases token usage because it sums work across parallel agents.
  — <https://openai.com/index/gpt-5-6/>
- Pin a snapshot instead of relying on a model alias so behavior stays stable.
  — <https://developers.openai.com/api/docs/models/gpt-5.6-sol>

## Superseded by this

- 2026-07-09 — Treating Ultra as a separate model is obsolete. OpenAI describes it as a mode of GPT-5.6 Sol, and the API catalog documents `gpt-5.6-sol`.

## Still unknown

- The PDF document lacks a creation date, so it confirms attribution without dating it independently.
- The text of the X post was unavailable during review, so its wording and date were not used as evidence.

## Sources

| source | title | read |
|---|---|---|
| https://openai.com/index/gpt-5-6/ | GPT-5.6: Frontier intelligence that scales with your ambition | 2026-09-05 |
| https://developers.openai.com/api/docs/models/gpt-5.6-sol | GPT-5.6 Sol Model | OpenAI API | 2026-09-05 |
| https://cdn.openai.com/pdf/04d1d1e4-bc75-476a-97cf-49055cd98d31/cdc_proof.pdf | A Proof of the Cycle Double Cover Conjecture | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:gpt-5-6-sol-ultra`, thread `gpt-5-6-sol-ultra`, 0 dated events - → -.
- **Practical note:** No verified practical-use change can be proposed from the dated links alone.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.