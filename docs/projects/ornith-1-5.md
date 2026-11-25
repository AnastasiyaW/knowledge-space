---
title: Ornith-1.5
category: projects
date: 2026-08-20
tags: [ornith, ornith-1-5, project]
aliases: ["Ornith-1.5"]
---

# Ornith-1.5

**Development line:** `project:ornith-1-5` · thread `ornith-1-5`  
**Last event:** 2026-08-20 · 1 dated since 2026-08-20 · **Researched:** 2026-09-05 · confidence: medium

## What it is

Ornith-1.5 — семейство MIT-лицензированных мультимодальных моделей для разработчиков, которым нужен локальный OpenAI-совместимый endpoint вместо закрытого API. — 9B Dense для одного GPU и квантованных сборок. — 35B-A3B MoE с примерно 3B активных параметров на токен. — 397B MoE для многогPU-сервинга. Базовый контекст — до 262 144 токенов; 397B требует примерно 800 GB в bf16. Вердикт: 35B-A3B — практический серверный вариант, 397B — вариант для инфраструктуры с несколькими ускорителями.

## Development line

- **2026-08-20 — Ornith-1.5 release page and model collection were linked.** Линейка из 9B Dense, 35B MoE и 397B MoE расширила Ornith-1.0 от генерации scaffold и rollout до совместной генерации задач, scaffold и rollout для RL.

## What changed

2026-08-20 — выпущена Ornith-1.5: линейка из 9B Dense, 35B MoE и 397B MoE расширила Ornith-1.0 от генерации scaffold и rollout до совместной генерации задач, scaffold и rollout для RL.

Дополнение к событию: 35B-модель названа Ornith-1.5-35B-A3B и активирует около 3B параметров на токен; флагман Ornith-1.5-397B заявлен как 397B MoE.

## How to use this

From 2026-08-20, practitioners should treat Ornith-1.5 as a distinct release line and consult its linked official page and model collection before choosing a checkpoint or workflow.

1. Выберите checkpoint: 9B для компактного запуска, 35B-A3B для серверного reasoning/coding, 397B — если доступен многогPU-узел.
  — <https://huggingface.co/collections/ornith-ai/ornith-15>
2. Для 35B-A3B установите актуальный vLLM или SGLang и поднимите OpenAI-совместимый сервер с parser для reasoning и tool calls.
  — <https://huggingface.co/ornith-ai/Ornith-1.5-35B-A3B?hardware=b200>
3. Подключите клиент к локальному /v1 endpoint и читайте финальный ответ из content, а reasoning trace — из reasoning_content.
  — <https://huggingface.co/ornith-ai/Ornith-1.5-35B-A3B?hardware=b200>
4. Для простого локального теста 9B загрузите checkpoint через Transformers pipeline или запустите его через vLLM.
  — <https://huggingface.co/ornith-ai/Ornith-1.5-9B/tree/main>

## Best practices

- Для обычных задач начните с temperature=0.6, top_p=0.95 и top_k=20; temperature=1.0 у автора предназначена для воспроизведения бенчмарков.
  — <https://huggingface.co/ornith-ai/Ornith-1.5-35B-A3B?hardware=b200>
- Используйте runtime не старее Transformers 5.8.1, vLLM 0.19.1 или SGLang 0.5.9 для 35B-A3B.
  — <https://huggingface.co/ornith-ai/Ornith-1.5-35B-A3B?hardware=b200>
- Не включайте YaRN/RoPE scaling для коротких запросов: статическое масштабирование может ухудшить качество; подбирайте factor под действительно нужное окно.
  — <https://huggingface.co/ornith-ai/Ornith-1.5-35B-A3B?hardware=b200>

## Superseded by this

- 2026-08-20 — Ornith-1.5 заменяет Ornith-1.0 как актуальную линейку для задач, где важна полная self-improvement loop; Ornith-1.0 остаётся предыдущим состоянием, а не удалённой моделью.
- 2026-08-20 — для 35B актуальное имя checkpoint — Ornith-1.5-35B-A3B, а не общее «Ornith-1.5-35B».

## Still unknown

- Первая страница Ornith датирована только «Aug. 2026», поэтому точный день 2026-08-20 подтверждён входным событием, но не отдельно на странице автора.
- Заявленные бенчмарки — результаты команды Ornith; независимого воспроизведения в использованных первичных источниках нет.
- Mobile-вариант Ornith-1.5-9B упомянут в анонсе, но его отдельная актуальная карточка и требования к запуску не проверялись.

## Sources

| source | title | read |
|---|---|---|
| https://ornith.ai/ornith_1_5.html | Ornith-1.5: From Self-Scaffolding to Self-Improvement | 2026-09-05 |
| https://huggingface.co/collections/ornith-ai/ornith-15 | Ornith-1.5 - a ornith-ai Collection | 2026-09-05 |
| https://huggingface.co/ornith-ai/Ornith-1.5-35B-A3B?hardware=b200 | ornith-ai/Ornith-1.5-35B-A3B | 2026-09-05 |
| https://huggingface.co/ornith-ai/Ornith-1.5-9B/tree/main | ornith-ai/Ornith-1.5-9B | 2026-09-05 |
| https://huggingface.co/ornith-ai/Ornith-1.5-397B/blame/main/README.md | README.md · ornith-ai/Ornith-1.5-397B | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:ornith-1-5`, thread `ornith-1-5`, 1 dated events 2026-08-20 → 2026-08-20.
- **Practical note:** From 2026-08-20, practitioners should treat Ornith-1.5 as a distinct release line and consult its linked official page and model collection before choosing a checkpoint or workflow.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
