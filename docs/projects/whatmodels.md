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

WhatModels is a model selector for users of Ollama, llama.cpp and other local runtimes to pick models by GPU or manual VRAM, estimating maximum context and generation speed.

- GPU catalog to choose hardware presets.
- Manual VRAM input to specify custom memory limits.
- Minimum context filters to screen out configurations that fall short.
- Quantization comparison to evaluate size against memory.
- Fit categories to group models into "runs well", "tight fit" and "doesn't fit".

Generation speed appears only for catalog GPUs and remains an estimate rather than a runtime benchmark.

The tool suits initial model and hardware selection, but production inference requires verification on local hardware.

## Development line

- **2026-05-15 — WhatModels public website documented.** On 2026-05-15, a message in the WhatModels thread linked to the project's public website. This establishes a dated public reference point for WhatModels, but the available evidence does not identify a launch, release, or feature change.

## What changed

2026-05-15 — WhatModels operated as a web compatibility calculator for local LLMs. The published example configured two RTX 5060 Ti 16 GB cards, 16K context, a minimum of 10 tokens/s and 64 GB RAM.

After 2026-05-15 — We found no confirmed dated releases beyond the initial event. Current repository documentation describes a static browser calculation with no backend or API: VRAM combines model weights and KV-cache, and generation speed derives from memory bandwidth and weight size.

## How to use this

As of 2026-05-15, practitioners can use the documented WhatModels public website as a project discovery point; its specific capabilities and release status still require separate verification.

1. Open the calculator and choose a GPU from the list or enter available VRAM manually.
  — <https://whatmodelscanirun.com/>
2. Set the minimum acceptable context; when selecting a GPU from the list, compare estimated tokens per second.
  — <https://github.com/BenD10/whatmodels>
3. Start with "Runs well" results; verify "Tight fit" options locally with the required context and quantization.
  — <https://github.com/BenD10/whatmodels>

## Best practices

- Include KV-cache alongside weights: a model fitting by GGUF file size can run out of memory at the target context.
  — <https://github.com/BenD10/whatmodels>
- Treat speed estimates as preliminary: generation speed depends on memory bandwidth, quantization, context and runtime engine overhead.
  — <https://github.com/BenD10/whatmodels>
- Compare configurations on the same model and quantization at the same required context, then confirm the result in the target runtime.
  — <https://habr.com/ru/articles/1035862/>

## Superseded by this

- 2026-05-16 — Choosing a local LLM solely by parameter count or file size is obsolete for long-context tasks: calculation must include KV-cache and quantization.

## Still unknown

- No primary dated changelog for WhatModels exists for 2026-05-15 or later changes; the GitHub repository shows current code but provides no dated release milestones in the available material.
- The initial schema recorded the 2026-05-15 event without dedicated finding fields; outside this event, no subsequent dated development steps are confirmed.

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