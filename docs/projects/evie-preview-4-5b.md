---
title: EVIE-Preview-4.5B
category: projects
date: 2026-08-18
tags: [evie-preview-4-5b, project, tencent/evie-preview-4.5b]
aliases: ["EVIE-Preview-4.5B"]
---

# EVIE-Preview-4.5B

**Development line:** `project:evie-preview-4-5b` · thread `evie-preview-4-5b`  
**Last event:** 2026-08-18 · 1 dated since 2026-08-18 · **Researched:** 2026-09-05 · confidence: medium

## What it is

EVIE-Preview-4.5B — открытая 4,54B-модель для мультиязычного поиска по сканам, таблицам, графикам и документам. Возможности: текстовый запрос к изображениям страниц; MaxSim late-interaction retrieval; запросы на английском, французском, немецком, итальянском, испанском, португальском и китайском. Лимит: BF16-чекпойнт занимает 8,5 GB, а индекс на 1 млн страниц требует 179,2 GiB при 768 визуальных токенах. Вердикт: подходит для self-hosted visual document retrieval, если команда готова хранить многовекторный индекс и запускать CUDA-инференс.

## Development line

- **2026-08-18 — Dated public references for EVIE-Preview-4.5B.** 4,54B visual-document-retrieval checkpoint на базе Qwen3.5-4B с 128-мерными токенными векторами и лицензией Apache-2.0.

## What changed

2026-08-18 — опубликован EVIE-Preview-4.5B: 4,54B visual-document-retrieval checkpoint на базе Qwen3.5-4B с 128-мерными токенными векторами и лицензией Apache-2.0.

## How to use this

As of 2026-08-18, practitioners can begin their evaluation from the linked GitHub and Hugging Face pages for EVIE-Preview-4.5B, while verifying capabilities, licensing, and usage requirements directly from those sources before adoption.

1. Установите `colpali-engine>=0.3.15` и `accelerate`; для воспроизводимого запуска используйте зависимости из репозитория.
  — <https://huggingface.co/tencent/EVIE-Preview-4.5B>
2. Загрузите `ColQwen3_5` с идентификатором `tencent/EVIE-Preview-4.5B` в BF16 на CUDA и обработчик `ColQwen3_5Processor`.
  — <https://huggingface.co/tencent/EVIE-Preview-4.5B>
3. Перед обработкой запросов включите двунаправленное внимание для full-attention слоёв, а перед каждым query forward сбрасывайте `model.rope_deltas = None`; затем считайте MaxSim-оценки через `processor.score`.
  — <https://github.com/Tencent/EVIE-Preview-4.5B>
4. Для пакетной проверки страниц используйте `infer.py` с повторяемыми аргументами `--query` и `--image`.
  — <https://github.com/Tencent/EVIE-Preview-4.5B>

## Best practices

- Начинайте с 768 визуальных токенов на страницу: это тренировочный бюджет модели и более экономичный вариант индекса.
  — <https://huggingface.co/tencent/EVIE-Preview-4.5B>
- Не используйте стандартные causal masks: опубликованный код явно переключает full-attention слои в bidirectional mode, иначе результаты не соответствуют заявленным оценкам.
  — <https://huggingface.co/tencent/EVIE-Preview-4.5B>
- Проверяйте качество на собственных документах и запросах: заявленные результаты относятся к ViDoRe, а не к произвольному корпоративному корпусу.
  — <https://huggingface.co/tencent/EVIE-Preview-4.5B>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- Точная дата и состав последующих изменений в Hugging Face-репозитории не подтверждены первичным источником с календарной меткой, поэтому они не включены в new_events.
- Заявления о лидерстве на ViDoRe приведены из model card; независимое воспроизведение в этой записи не проверялось.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/Tencent/EVIE-Preview-4.5B | Tencent/EVIE-Preview-4.5B — исходный код и инструкция запуска | 2026-09-05 |
| https://huggingface.co/tencent/EVIE-Preview-4.5B | tencent/EVIE-Preview-4.5B — model card, параметры, результаты и quick start | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:evie-preview-4-5b`, thread `evie-preview-4-5b`, 1 dated events 2026-08-18 → 2026-08-18.
- **Practical note:** As of 2026-08-18, practitioners can begin their evaluation from the linked GitHub and Hugging Face pages for EVIE-Preview-4.5B, while verifying capabilities, licensing, and usage requirements directly from those sources before adoption.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
