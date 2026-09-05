---
title: WhatModels — Public website
category: projects
date: 2026-05-15
tags: [project, public-website, whatmodels]
aliases: ["WhatModels"]
---

# WhatModels — Public website

**Development line:** `project:whatmodels` · thread `public-website`  
**Last event:** 2026-05-15 · 1 dated since 2026-05-15 · **Researched:** 2026-09-05 · confidence: medium

## What it is

WhatModels selects local LLMs for Ollama, llama.cpp and similar runtimes by GPU model or manual VRAM limits, estimating maximum context and generation speed.

- GPU catalog to select existing video cards.
- Manual VRAM input for custom memory configurations.
- Minimum context filters to narrow down model choices.
- Quantization comparison across formats.
- Fit categories grouping models into "runs well", "tight fit" and "doesn't fit".

Speed estimates apply only to catalog GPUs and remain theoretical rather than runtime benchmarks.

We use it for initial model and hardware screening, but production deployment requires a local run.

## Development line

- **2026-05-15 — WhatModels public website documented.** On 2026-05-15, the project documented its public website. This gives a dated reference point for WhatModels, without a confirmed launch, release, or feature change.

## What changed

2026-05-15 — WhatModels served as a web compatibility calculator for local LLMs; the published example specified two RTX 5060 Ti 16 GB cards, 16K context, minimum 10 tokens/s and 64 GB RAM.

After 2026-05-15 — no dated releases appeared beyond the initial event. Current repository documentation describes static in-browser calculation without a backend or API: VRAM sums weights and KV-cache, while speed derives from memory bandwidth and weight size.

## How to use this

As of 2026-05-15, we use the WhatModels public website as a project discovery point; specific capabilities and release status still require separate verification.

1. Open the calculator and select a GPU from the list or enter available VRAM manually.
  — <https://whatmodelscanirun.com/>
2. Set minimum acceptable context, and compare estimated tokens per second when choosing a GPU from the list.
  — <https://github.com/BenD10/whatmodels>
3. Start with "Runs well" results, and verify "Tight fit" options with a local run using the required context and quantization.
  — <https://github.com/BenD10/whatmodels>

## Best practices

- Count KV-cache with model weights: a model fitting by GGUF file size can still run out of memory at the required context.
  — <https://github.com/BenD10/whatmodels>
- Treat speed estimates as preliminary: generation speed depends on memory bandwidth, quantization, context length and engine overhead.
  — <https://github.com/BenD10/whatmodels>
- Compare the same model and quantization at the target context length, then verify the result in your runtime.
  — <https://habr.com/ru/articles/1035862/>

## Superseded by this

- 2026-05-16 — Sizing a local LLM solely by parameter count or file size is obsolete for long-context tasks: calculation must include KV-cache and quantization.

## Still unknown

- No dated changelog exists for WhatModels on 2026-05-15 or later; the GitHub repository shows current state without dated release milestones.
- Outside the 2026-05-15 event, no new dated development steps are confirmed.

## Sources

| source | title | read |
|---|---|---|
| https://whatmodelscanirun.com/ | What Models? — Pick the right model for your GPU in seconds | 2026-09-05 |
| https://github.com/BenD10/whatmodels | BenD10/whatmodels — Figure out what models you can run locally | 2026-09-05 |
| https://www.forum.mista.ru/topic/901896 | Confaster — ИИ-агент для 1С Конфигуратора с MCP сервером | 2026-09-05 |
| https://habr.com/ru/articles/1035862/ | Калькулятор VRAM для локальных LLM: Какие модели ИИ запустятся у вас на компьютере? | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:whatmodels`, thread `public-website`, 1 dated events 2026-05-15 → 2026-05-15.
- **Practical note:** As of 2026-05-15, practitioners can use the documented WhatModels public website as a project discovery point; its specific capabilities and release status still require separate verification.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
