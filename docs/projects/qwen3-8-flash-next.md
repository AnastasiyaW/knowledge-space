---
title: Qwen3.8-Flash-Next — Qwen
category: projects
date: 2026-08-26
tags: [project, qwen, qwen3-8-flash-next]
aliases: ["Qwen3.8-Flash-Next"]
---

# Qwen3.8-Flash-Next — Qwen

**Development line:** `project:qwen3-8-flash-next` · thread `qwen`  
**Last event:** 2026-08-26 · 1 dated since 2026-08-26 · **Researched:** 2026-09-05 · confidence: high

## What it is

Qwen3.8-Flash-Next: открытая мультимодальная MoE-модель для разработчиков, которым нужны vision+text, кодинг и агентные сценарии. — запускается через Transformers, vLLM, SGLang, TokenSpeed и llama.cpp; — использует Gated DeltaNet, Qwen Sparse Attention, Gated Residual и n-gram embeddings. 125B параметров основной модели, 51B параметров таблиц n-gram embeddings и 6B активных параметров на токен; официальный пример сервинга задаёт контекст 262 144 токена. Практический выбор для экспериментов с открытыми весами; для managed production API официальный Qwen3.8-Flash позиционируется отдельно.

## Development line

- **2026-08-26 — Qwen3.8-Flash-Next project resources were documented.** Мультимодальной MoE-модели и раннего preview архитектуры Qwen4.

## What changed

2026-08-26 — опубликованы открытые веса Qwen3.8-Flash-Next: мультимодальной MoE-модели и раннего preview архитектуры Qwen4. 2026-08-31 — вышел технический отчёт с абляциями архитектуры, оценкой эффективности и стабильности обучения.

## How to use this

As of 2026-08-26, practitioners should verify Qwen3.8-Flash-Next through its linked source repository, model-hosting resources, and demo before selecting a checkpoint or deployment route.

1. Для прототипа с изображением и текстом загрузите `Qwen/Qwen3.8-Flash-Next` через Transformers pipeline `image-text-to-text` или через `AutoProcessor` и `AutoModelForMultimodalLM`.
  — <https://huggingface.co/Qwen/Qwen3.8-Flash-Next>
2. Для self-hosted OpenAI-compatible API запустите vLLM; официальный пример использует tensor parallelism 4, `--max-model-len 262144`, reasoning parser `qwen3` и tool-call parser `qwen3_coder`.
  — <https://github.com/QwenLM/Qwen3.8-Flash-Next>
3. Если инфраструктуру для open weights поддерживать не нужно, используйте Qwen Cloud: текущий managed Qwen3.8-Flash совместим с API OpenAI и Anthropic.
  — <https://www.qwencloud.com/>

## Best practices

- Для запуска с tool calls включайте одновременно reasoning parser `qwen3` и tool-call parser `qwen3_coder`; без них официальный serving-рецепт для этого режима не приведён.
  — <https://github.com/QwenLM/Qwen3.8-Flash-Next>
- На Apple Silicon используйте mlx-vlm либо готовую MLX-квантизацию; для llama.cpp выбирайте совместимые GGUF-веса, а не исходный checkpoint.
  — <https://github.com/QwenLM/Qwen3.8-Flash-Next>
- Не переносите лимит 262K из self-hosted примера на managed модель: Qwen Cloud отдельно заявляет для Qwen3.8-Flash контекст 1M.
  — <https://www.qwencloud.com/>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- Для события 2026-08-26: официальный репозиторий датирует выпуск 2026-08-26 и уточняет, что открыты веса Qwen3.8-Flash-Next — 125B-параметровой мультимодальной MoE-модели с 6B активных параметров на токен; source_date=2026-08-26; source_url=https://github.com/QwenLM/Qwen3.8-Flash-Next.
- Новое событие: 2026-08-31 — технический отчёт описал 14 pre-training бенчмарков: модель опережает 397B-A17B predecessor на восьми и отстаёт на остальных не более чем на 2,6 пункта, при примерно трети активных параметров, трети токенов обучения и около одной девятой FLOPs; source_date=2026-08-31; source_url=https://arxiv.org/abs/2608.30320.
- Текущая модельная карточка называет Qwen3.8-Flash production-версией на базе Flash-Next с 1M context и встроенными tools, но не указывает дату этого перехода; его нельзя привязать к событию 2026-08-26 или оформить как датированное supersedes.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/QwenLM/Qwen3.8-Flash-Next | QwenLM/Qwen3.8-Flash-Next | 2026-09-05 |
| https://huggingface.co/Qwen/Qwen3.8-Flash-Next | Qwen/Qwen3.8-Flash-Next model card | 2026-09-05 |
| https://arxiv.org/abs/2608.30320 | On the Design of Qwen3.8-Next Architecture: Evaluation, Efficiency, and Training Stability | 2026-09-05 |
| https://www.qwencloud.com/ | QwenCloud — AI-Native Models, Tools & Apps Platform | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:qwen3-8-flash-next`, thread `qwen`, 1 dated events 2026-08-26 → 2026-08-26.
- **Practical note:** As of 2026-08-26, practitioners should verify Qwen3.8-Flash-Next through its linked source repository, model-hosting resources, and demo before selecting a checkpoint or deployment route.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
