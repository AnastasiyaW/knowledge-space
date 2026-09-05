---
title: Holo3
category: projects
date: 2026-04-02
tags: [h-company-holo3, holo3-model-release, holo3_model_release, project]
aliases: ["Holo3"]
---

# Holo3

**Development line:** `project:h-company-holo3` · thread `holo3-model-release`  
**Last event:** 2026-04-02 · 1 dated since 2026-04-02 · **Researched:** 2026-09-05 · confidence: high

## What it is

Holo3 — мультимодальная MoE-модель для computer use: принимает текст и до пяти изображений, возвращает текстовое действие или решение для агентного контура. Доступны API-модели 35B-A3B и 122B-A10B с контекстом 65 536 токенов; открытые веса исходной 35B-A3B опубликованы по Apache-2.0. Практический вывод: для новой интеграции следует начинать с текущей Holo3.1-линейки, а исходную Holo3 рассматривать как предшественника и совместимый открытый чекпойнт.

## Development line

- **2026-04-02 — H Company released the Holo3 model.** On 2026-04-02, H Company published Holo3 as a new model release. The linked project, API, and model-repository pages indicate that the release was intended for both direct use and model access. The record contains no source text or independent research, so the exact capabilities and release terms remain unconfirmed.

## What changed

2026-04-02 — опубликованы открытые веса Holo3-35B-A3B; релизная страница относит Holo3 к computer-use моделям и заявляет 122B-A10B как API-флагман. 2026-04-15 — HoloTab сделал модель доступной через браузерное агентное приложение. 2026-04-28 — выпущен Holotron 3 Nano (30B-A3B), отдельная более быстрая модель для автоматизации компьютерных задач. 2026-06-01 — Holo3.1 расширила линию вариантами 0.8B, 4B, 9B и 35B-A3B, function calling, мобильной поддержкой и локальными квантованными весами.

## How to use this

From 2026-04-02, practitioners should evaluate Holo3 through H Company’s model and API documentation before selecting it for a workflow; the exact supported capabilities and access terms require verification from the linked pages.

1. Создайте аккаунт Portal-H и API-ключ; бесплатный уровень даёт ограниченный доступ к API 35B-A3B.
  — <https://hcompany.ai/holo-models-api>
2. Для ограниченных по времени и хорошо заданных задач используйте `holo3-1-35b-a3b`; для сложных многошаговых сценариев — `holo3-122b-a10b`, если условия коммерческого использования и тарифа подходят.
  — <https://hcompany.ai/holo-models-api>
3. Для локального запуска исходного открытого Holo3 загрузите `Hcompany/Holo3-35B-A3B` через Transformers, vLLM или SGLang и передавайте сообщения в мультимодальном chat template.
  — <https://huggingface.co/Hcompany/Holo3-35B-A3B>
4. Если нужны мобильные сценарии, function calling или локальные квантизованные веса, переходите на Holo3.1 и выбирайте размер и формат весов под целевое железо.
  — <https://hcompany.ai/holo3.1>

## Best practices

- Выбирайте 35B-A3B для latency-sensitive, экономичных и хорошо определённых автоматизаций; 122B-A10B — для новых или сложных многошаговых сред.
  — <https://hcompany.ai/holo-models-api>
- Перед локальным развёртыванием проверяйте формат весов и рантайм: исходный Holo3 документирован для Transformers, vLLM и SGLang; Holo3.1 добавляет FP8, Q4 GGUF и NVFP4.
  — <https://huggingface.co/Hcompany/Holo3-35B-A3B>
- Не считать заявление о zero data retention заменой собственной оценки данных: API указывает, что по умолчанию не сохраняет prompts и responses, но учётные метаданные и токены логируются.
  — <https://hcompany.ai/holo-models-api>

## Superseded by this

- 2026-06-01 — Holo3.1 заменяет исходную Holo3 как рекомендуемую линия для мобильных сред, function calling и локального запуска в квантованном виде.
- 2026-06-01 — совет ограничиваться единственным 35B-A3B вариантом устарел: доступны 0.8B, 4B, 9B и 35B-A3B варианты Holo3.1.

## Still unknown

- Для 122B-A10B текущая API-страница указывает лицензию Research only (non-commercial); условия доступа и лицензирования на дату релиза 2 апреля отдельно не подтверждены.
- Публичные источники подтверждают выпуск Holo3-35B-A3B 2 апреля, тогда как основная анонсная страница датирована 31 марта; различие похоже на дату анонса и дату публикации весов, но точное время публикации не указано.

## Sources

| source | title | read |
|---|---|---|
| https://hcompany.ai/holo3 | Holo3: Breaking the Computer Use Frontier — H Company, 31 March 2026 | 2026-09-05 |
| https://hcompany.ai/holo-models-api | Holo Models API — H Company | 2026-09-05 |
| https://huggingface.co/Hcompany/Holo3-35B-A3B | Hcompany/Holo3-35B-A3B — Hugging Face | 2026-09-05 |
| https://hcompany.ai/holo3.1 | Holo3.1: Fast & Local Computer Use Agents — H Company, 1 June 2026 | 2026-09-05 |
| https://hcompany.ai/meet-holotab | HoloTab — H Company, 15 April 2026 | 2026-09-05 |
| https://hcompany.ai/holotron3 | Holotron 3 Nano — H Company, 28 April 2026 | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:h-company-holo3`, thread `holo3-model-release`, 1 dated events 2026-04-02 → 2026-04-02.
- **Practical note:** From 2026-04-02, practitioners should evaluate Holo3 through H Company’s model and API documentation before selecting it for a workflow; the exact supported capabilities and access terms require verification from the linked pages.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
