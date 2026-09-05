---
title: Marionette — Public project release
category: projects
date: 2026-08-18
tags: [alayalab/marionette, marionette, project, public-project-release]
aliases: ["Marionette"]
---

# Marionette — Public project release

**Development line:** `project:marionette` · thread `public-project-release`  
**Last event:** 2026-08-18 · 1 dated since 2026-08-18 · **Researched:** 2026-09-05 · confidence: high

## What it is

Marionette: пайплайн Alaya Lab для исследователей world models: ActionGPT и PoseGPT предсказывают 276-мерное артикулированное состояние, детерминированный bridge рендерит геометрию, а дообученный Wan2.2-Fun-5B-Control создаёт RGB-видео.

- управление: подмена action token или trajectory root на уровне состояния;
- запуск: два Python-окружения для stage 1 и stage 2;
- границы: один вид монстра, сканы конкретных локаций и non-commercial research license.

Мера: опубликованный checkpoint observation весит 10.0 GB, а необходимая сторонняя базовая модель — около 23 GB.

Вердикт: это воспроизводимый исследовательский pipeline, а не универсальный игровой движок или готовый сервис генерации видео.

## Development line

- **2026-08-18 — Marionette public project resources were linked.** On 2026-08-18, the Marionette development line was represented by links to its project page, source repository, Hugging Face model page, and hosted world-model space. This is a material public-project milestone because it connects the project’s documentation, code, model distribution, and runnable demonstration.

## What changed

2026-08-13 — опубликованы project page, inference code, runtime assets и controllability demos; полный трёхступенчатый pipeline стал доступен для локального запуска. 2026-08-14 — на arXiv опубликована работа «Marionette: Predicting World States, Rendering Geometry, Painting Appearance»; она зафиксировала архитектуру и заявленные результаты контроля состояния. 2026-08-18 — материалы проекта, репозиторий, веса Hugging Face и демонстрация были собраны в одном выпуске; карточка весов уточняет точное имя базовой модели, размеры checkpoints, настройки inference и ограничения.

## How to use this

From 2026-08-18, practitioners should use the linked project page, repository, Hugging Face model page, and hosted space as the starting set for evaluating Marionette; capabilities, licensing, and reproduction steps still require source research before adoption.

1. Клонировать репозиторий, загрузить веса Marionette и стороннюю базовую модель, затем запустить `bash run_demo.sh`.
  — <https://huggingface.co/AlayaLab/Marionette>
2. Для раздельного запуска создать render-окружение для stage 1 и Wan-окружение для stage 2; запустить `run_stage1_render.sh`, затем `run_stage2_wan.sh`.
  — <https://github.com/AlayaLab/Marionette>
3. Держать checkpoint observation и его prompt одной парой; опубликованные настройки — 704×1280, 40 steps, guidance 6.0, 81-frame chunks, 30 fps.
  — <https://huggingface.co/AlayaLab/Marionette>

## Best practices

- Не объединять stage 1 и stage 2 в одно окружение: рендеру нужен Python 3.12 и EGL, а diffusion stage требует torch, diffusers и decord.
  — <https://github.com/AlayaLab/Marionette>
- Фиксировать `TORCH_SEED` для воспроизводимости dynamics stage; сравнивать результаты на одной машине по равенству воспроизводимых артефактов, а не с переносимым хешем видео.
  — <https://github.com/AlayaLab/Marionette>
- Не переносить action IDs между checkpoints: их смысл определяется словарём конкретной обучающей выборки.
  — <https://huggingface.co/AlayaLab/Marionette>
- Не применять модель к новой геометрии без нового terrain scan и не интерпретировать её как general character-motion model.
  — <https://huggingface.co/AlayaLab/Marionette>

## Superseded by this

- 2026-08-13 — статус roadmap «pretrained weights uploading» устарел: модельная карточка AlayaLab/Marionette теперь перечисляет опубликованные checkpoints и инструкции загрузки.

## Still unknown

- Hugging Face Space `hugging-apps/marionette-world-model` returned an internal error during verification, so its live behaviour and maintenance status are unverified.
- The supplied response schema has no `event_findings` or `new_events` fields. The event-specific addition for 2026-08-18 is therefore recorded in `what_changed`; separately dated 2026-08-13 and 2026-08-14 developments are also recorded there.

## Sources

| source | title | read |
|---|---|---|
| https://alayalab.github.io/Marionette/ | Marionette — Predicting World States, Rendering Geometry, Painting Appearance | 2026-09-05 |
| https://github.com/AlayaLab/Marionette | AlayaLab/Marionette repository | 2026-09-05 |
| https://huggingface.co/AlayaLab/Marionette | AlayaLab/Marionette — weights model card | 2026-09-05 |
| https://arxiv.org/abs/2608.14530 | Marionette: Predicting World States, Rendering Geometry, Painting Appearance | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:marionette`, thread `public-project-release`, 1 dated events 2026-08-18 → 2026-08-18.
- **Practical note:** From 2026-08-18, practitioners should use the linked project page, repository, Hugging Face model page, and hosted space as the starting set for evaluating Marionette; capabilities, licensing, and reproduction steps still require source research before adoption.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
