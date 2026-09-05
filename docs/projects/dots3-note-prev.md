---
title: dots3-note preview
category: projects
date: 2026-08-17
tags: [dots-studio/dots3-note-prev, dots3-note-prev, dots3-note-preview-release, project]
aliases: ["dots3-note preview"]
---

# dots3-note preview

**Development line:** `project:dots3-note-prev` · thread `dots3-note-preview-release`  
**Last event:** 2026-08-17 · 1 dated since 2026-08-17 · **Researched:** 2026-09-05 · confidence: medium

## What it is

dots3-note preview — модель dots studio для команд, которым нужен локальный мультимодальный агент: текстовый вывод, понимание изображений, документов, графиков, аудио и видео, tool use и длинный контекст. 280B параметров всего, 16B активных, контекст до 512K токенов. Вердикт: практична только для крупного GPU-инференса; это не модель для одной обычной видеокарты.

## Development line

- **2026-08-17 — Dots Studio published public resources for dots3-note preview.** `dots3-note-prev` и FP8-вариант `dots3-note-prev-fp8`; опубликованы 280B/16B MoE, входы text/image/video/audio и текстовый вывод.

## What changed

2026-08-17 — вышла preview-версия первых открытых весов семейства dots3: `dots3-note-prev` и FP8-вариант `dots3-note-prev-fp8`; опубликованы 280B/16B MoE, входы text/image/video/audio и текстовый вывод. 2026-08-25 — официальная интеграция в Transformers оставалась открытым PR #47844: добавлены inference-only обработка всех четырёх модальностей, BF16/FP8 и тесты, но это ещё не поддержка в стабильном релизе библиотеки.

## How to use this

As of 2026-08-17, practitioners should treat dots3-note preview as a separately documented project line and consult its Studio Dots, GitHub, and Hugging Face resources before attempting use; its exact capabilities and setup remain unverified from this evidence.

1. Для серверного запуска возьмите FP8-чекпойнт `dots-studio/dots3-note-prev-fp8` и разверните его через vLLM или SGLang на одном 8-GPU узле; задайте меньший контекст, если память или требуемая параллельность не позволяют 512K.
  — <https://github.com/studio-dots-ai/dots3-note-prev>
2. Поднимите OpenAI-совместимый endpoint с именем модели `dots3-note-prev`, затем вызывайте `/v1/chat/completions`; для прямого ответа отключите thinking через `enable_thinking=False`.
  — <https://github.com/studio-dots-ai/dots3-note-prev>
3. Передавайте изображение, аудио или видео как multimodal content; видео с аудиодорожкой обрабатывается вместе со звуком.
  — <https://github.com/studio-dots-ai/dots3-note-prev>

## Best practices

- Для production-подобного serving предпочтителен FP8 на восьми GPU: BF16 требует больше памяти, а длину контекста нужно подбирать вместе с числом одновременных запросов и модальностями.
  — <https://github.com/studio-dots-ai/dots3-note-prev>
- Не рассчитывайте на стабильный Transformers для нативного запуска: официальный PR #47844 на момент проверки открыт; используйте указанную ревизию PR только осознанно либо выберите vLLM main/nightly.
  — <https://github.com/huggingface/transformers/pull/47844>

## Superseded by this

- 2026-08-25 — предположение, что модель уже имеет стабильную нативную поддержку Transformers, устарело: официальный PR #47844 остаётся открытым.

## Still unknown

- Дата 2026-08-17 подтверждает зафиксированный шаг, но доступный первичный initial commit на Hugging Face отображался как сделанный примерно 11 дней до 2026-09-05; точную причину расхождения дат без исторического timestamp релиза установить нельзя.
- Полный технический отчёт на странице проекта помечен как forthcoming, поэтому независимая проверка заявленных бенчмарков и качества не выполнена.
- Отдельные поля event_findings и new_events не представлены в обязательной схеме ответа; дополнения для шага 2026-08-17 и новый шаг 2026-08-25 отражены в what_changed.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/studio-dots-ai/dots3-note-prev | studio-dots-ai/dots3-note-prev README | 2026-09-05 |
| https://huggingface.co/dots-studio/dots3-note-prev | dots-studio/dots3-note-prev model card | 2026-09-05 |
| https://huggingface.co/dots-studio/dots3-note-prev/commit/09293f609e9df8ec1b165792420bc7be2cfb86a8 | Release dots3-note preview model commit | 2026-09-05 |
| https://github.com/huggingface/transformers/pull/47844 | Transformers PR #47844: Add dots3-note Preview model support | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:dots3-note-prev`, thread `dots3-note-preview-release`, 1 dated events 2026-08-17 → 2026-08-17.
- **Practical note:** As of 2026-08-17, practitioners should treat dots3-note preview as a separately documented project line and consult its Studio Dots, GitHub, and Hugging Face resources before attempting use; its exact capabilities and setup remain unverified from this evidence.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
