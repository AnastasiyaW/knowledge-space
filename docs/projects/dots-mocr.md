---
title: dots.mocr
category: projects
date: 2026-03-22
tags: [dots-mocr, project]
aliases: ["dots.mocr"]
---

# dots.mocr

**Development line:** `project:dots-mocr` · thread `dots-mocr`  
**Last event:** 2026-03-22 · 1 dated since 2026-03-22 · **Researched:** 2026-09-05 · confidence: high

## What it is

dots.mocr — 3B VLM для команд, которым нужно извлекать из PDF и изображений не только текст, но и layout, таблицы, формулы и графику; конкурент PaddleOCR-VL и DeepSeek-OCR. Возможности: OCR и bbox, Markdown/HTML/LaTex-вывод, web/scene parsing, image-to-SVG через отдельную dots.mocr-svg. Ограничение: сложные таблицы, формулы и SVG ещё могут давать нестабильный результат. Вывод: для self-hosted document parsing разумно начинать с vLLM и валидировать сложные страницы на своих данных.

## Development line

- **2026-03-22 — dots.mocr project resources were linked.** On 2026-03-22, a dated message linked the dots.mocr GitHub repository, two Hugging Face resources, and a project website. This establishes a public reference point in the project's development line, including a separately linked SVG-related resource. The underlying post content and the nature of any release or update were not provided, so this record does not assert capabilities, versions, or performance.

## What changed

2026-03-22 — стали доступны основная 3B dots.mocr и отдельная 3B dots.mocr-svg; первичный анонс проекта датирован 2026-03-19, а не 22 марта. Для этого шага: GitHub называет основной релиз от 2026-03-19, указывает 3B-параметровую модель и вариант dots.mocr-svg для image-to-SVG; Hugging Face указывает BF16 и размер 3B для обеих моделей. Новые события: 2026-03-13 — статья MOCR впервые подана на arXiv; 2026-03-19 — статья обновлена до v2, опубликованы код и обе модели; 2026-03-20 — в репозитории были два последующих коммита с сообщениями «fix ignore» и «update».

## How to use this

As of 2026-03-22, practitioners should evaluate dots.mocr through the linked GitHub repository, project site, and the distinct Hugging Face resources—including the SVG-related resource—before choosing it for an OCR workflow; the dated links alone do not support capability or benchmark claims.

1. Разверните основной документный парсер через vLLM: `vllm serve rednote-hilab/dots.mocr --trust-remote-code`; для SVG выберите `rednote-hilab/dots.mocr-svg`.
  — <https://github.com/rednote-hilab/dots.mocr>
2. Передайте изображение или PDF в `dots_mocr/parser.py`; результат включает JSON с элементами layout, Markdown и изображение с bbox.
  — <https://github.com/rednote-hilab/dots.mocr>
3. Если нужен OpenAI-совместимый endpoint, запустите модель через vLLM и отправляйте image-plus-text сообщения в `/v1/chat/completions`.
  — <https://huggingface.co/rednote-hilab/dots.mocr>

## Best practices

- Для production-инференса используйте vLLM: авторы рекомендуют его, а Transformers отмечен как более медленный путь.
  — <https://github.com/rednote-hilab/dots.mocr>
- Выбирайте `dots.mocr-svg` для image-to-SVG; основная модель ограничена ёмкостью 3B и не одинаково сильна во всех SVG-задачах.
  — <https://github.com/rednote-hilab/dots.mocr>
- Не используйте точки в имени локальной папки весов: документация приводит `DotsMOCR` как временный обходной путь.
  — <https://github.com/rednote-hilab/dots.mocr>
- Проверяйте сложные таблицы, формулы и графику на целевом наборе: это прямо названные ограничения модели.
  — <https://github.com/rednote-hilab/dots.mocr>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- Поле event_findings отсутствует в предоставленной выходной схеме; его содержимое включено в what_changed. На GitHub нет versioned releases, поэтому текущую сборку нельзя привязать к формальному тегу или release asset.
- Репозиторий и model cards перенаправляют с rednote-hilab на studio-dots; источники не объясняют, является ли это только переименованием/переносом организации или сменой владельца.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/rednote-hilab/dots.mocr | studio-dots-ai/dots.mocr — Multimodal OCR: Parse Anything from Documents | 2026-09-05 |
| https://huggingface.co/rednote-hilab/dots.mocr | dots-studio/dots.mocr — Hugging Face model card | 2026-09-05 |
| https://huggingface.co/rednote-hilab/dots.mocr-svg | dots-studio/dots.mocr-svg — Hugging Face model card | 2026-09-05 |
| https://arxiv.org/abs/2603.13032 | Multimodal OCR: Parse Anything from Documents | 2026-09-05 |
| https://github.com/studio-dots-ai/dots.mocr/commits/main | studio-dots-ai/dots.mocr commit history | 2026-09-05 |
| https://github.com/studio-dots-ai/dots.mocr/releases | studio-dots-ai/dots.mocr releases | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:dots-mocr`, thread `dots-mocr`, 1 dated events 2026-03-22 → 2026-03-22.
- **Practical note:** As of 2026-03-22, practitioners should evaluate dots.mocr through the linked GitHub repository, project site, and the distinct Hugging Face resources—including the SVG-related resource—before choosing it for an OCR workflow; the dated links alone do not support capability or benchmark claims.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
