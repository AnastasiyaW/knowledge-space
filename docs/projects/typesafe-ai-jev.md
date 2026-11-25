---
title: "TypeSafe AI: type-safe-ai-jev — Type Safe Ai Jev"
category: "projects"
date: 2026-10-07
tags: ["project", "type-safe-ai-jev", "typesafe-ai-jev"]
aliases: ["TypeSafe AI: type-safe-ai-jev"]
---

# TypeSafe AI: type-safe-ai-jev — Type Safe Ai Jev

TypeSafe AI: Jev is a hosted typed-decision model for developers building routing, scoring, and binary gates instead of chat responses.

**Development line:** project:typesafe-ai-jev · thread type-safe-ai-jev  
**Last event:** 2026-10-07 · 7 dated since 2026-09-15 · **Researched:** 2026-11-25 · confidence: medium

## What it is

Jev accepts state plus Choice, Score, or Noul questions, then returns structured values with probabilities. A type-valid answer can still be wrong or prompt-influenced. Use it behind bounded code paths with measured escalation, not as an autonomous judge.

## Development line

- **2026-09-15 — Early access announced.** TypeSafe AI announced Jev as its first public System One model in early access, defining the contract as unstructured state in and typed probabilistic decisions out.
- **2026-09-17 — LangChain integration guide.** LangChain published a Jev integration guide covering Choice, Score, and Noul questions and its TypeSafeClassifier interface.
- **2026-09-18 — TypeSafe AI releases Jev model and open-source replicas.** TypeSafe AI publicly released the Jev model, a classifier-style AI that selects from predefined options rather than generating text. Reviewed reports described performance against other rerankers and LLMs, open-source replicas, benchmark results on phishing detection, and community discussion on Hacker News; however, the vendor announcement does not substantiate the replica, phishing-benchmark, or community-performance claims.
  - The vendor announcement is dated 15 September and describes Jev as TypeSafe AI’s first public System One model in early access; it does not substantiate the listed replica, phishing-benchmark, or community-performance claims. (2026-09-15) — <https://typesafe.ai/blog/introducing-system-one-models-and-jev>
- **2026-09-21 — LangSmith evaluator integration.** LangSmith added Jev as an available evaluator provider for LLM-as-a-judge workflows.
- **2026-09-22 — TypeSafe AI launches Jev, a System One model new-class AI model.** Reviewed launch coverage described TypeSafe AI launching Jev as the first model of the System One class, introducing an inference paradigm focused on typed probabilistic decisions rather than token generation; the retained research supports the typed-decision contract and early access, but not the founder, stealth-exit, or comparative speed-and-cost claims.
- **2026-09-22 — TypeSafe launches Jev AI model with task-specific capabilities.** Reviewed reporting described Jev as an AI model optimized for fast decision-making tasks such as ticket search, email sorting, and ad analysis, citing console availability, pricing of $0.042 per million tokens, response times of 70-500ms, and a free tier; however, these task-specific capabilities, pricing, latency, and availability details were not independently established.
- **2026-09-22 — other reporting on this date.**
  - TypeSafe AI’s own announcement places initial public early access on 15 September, so this reviewed launch record should not be treated as evidence that Jev first became public on 22 September. (2026-09-15) — <https://typesafe.ai/blog/introducing-system-one-models-and-jev>
- **2026-10-07 — Survey on calibration and decision correctness.** A non-peer-reviewed evidence survey reported that type validity does not ensure decision correctness and recommended confidence-gated escalation tested on new workloads.

## What changed

Jev moved from early access into documented LangChain and LangSmith integrations. Independent analysis showed that typed output and confidence scores do not prove correctness. The reviewed September records describe launch coverage, but the vendor announcement dated first public access earlier on 15 September.

## How to use this

1. Define a bounded decision over supplied state, rather than ask for open-ended generation.
  — <https://www.langchain.com/blog/building-a-harness-with-jev>
2. Choose Choice for a declared label set, Score for an ordered rubric, or Noul for a true-or-false proposition.
  — <https://www.langchain.com/blog/building-a-harness-with-jev>
3. Pass the state and questions through TypeSafeClassifier.invoke after configuring TYPESAFE\_API\_KEY.
  — <https://www.langchain.com/blog/building-a-harness-with-jev>
4. Use the structured result in application code for routing or prioritization; retain an LLM for open-ended reasoning and generation.
  — <https://www.langchain.com/blog/building-a-harness-with-jev>

## Best practices

- Use Jev for narrow, declared decisions inside a code-owned workflow; do not treat it as a drop-in replacement for a generative model.
  — <https://www.langchain.com/blog/building-a-harness-with-jev>
- Set and test confidence thresholds on held-out workloads, then escalate uncertain cases instead of assuming a threshold transfers across tasks.
  — <https://eurekaleo.github.io/awesome-jev-survey/paper/main.pdf>
- Treat input state as untrusted: typed output prevents parsing failures but does not prevent incorrect or input-influenced decisions.
  — <https://eurekaleo.github.io/awesome-jev-survey/paper/main.pdf>

## Superseded by this

- Treating a type-valid Jev response or a reported confidence value as proof that the selected decision is correct.
  — <https://eurekaleo.github.io/awesome-jev-survey/paper/main.pdf>

## Still unknown

- The current official API reference was linked but not directly retrievable in this session; practical SDK and HTTP details were cross-checked through LangChain and an explicitly unofficial Chinese translation.
- The reviewed records mention open-source replicas, a specific pricing figure, latency, and task-specific capabilities, but these exact claims were not independently established by the sources retained here.
- No dated, directly attributable community-use report met the requirement for a page-own-date citation.

## Sources

| source | title | read |
|---|---|---|
| https://typesafe.ai/blog/introducing-system-one-models-and-jev | Introducing System One Models & Jev | 2026-11-25 |
| https://www.langchain.com/blog/building-a-harness-with-jev | Building a Harness with Jev | 2026-11-25 |
| https://www.langchain.com/blog/jev-is-now-available-in-langsmith-evals | Jev is now available in LangSmith Evals | 2026-11-25 |
| https://eurekaleo.github.io/awesome-jev-survey/paper/main.pdf | Jev and Typed Decision Models: An Empirical Survey of Calibration, Selective Control, and Open Implementations | 2026-11-25 |
| https://jevland.com/docs/quickstart/ | 快速开始 · Jev 中文文档 | 2026-11-25 |

## Agent brief {#agent-brief}

- **Subject:** project:typesafe-ai-jev, thread type-safe-ai-jev, 7 dated events 2026-09-15 → 2026-10-07.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
