---
title: MosaicMem
category: projects

tags: [mosaicmem, mosaicmem-development, project]
aliases: ["MosaicMem"]
---

# MosaicMem

**Development line:** `project:mosaicmem` · thread `mosaicmem-development`  
**Last event:** - · 0 dated since - · **Researched:** 2026-09-05 · confidence: high

## What it is

MosaicMem: исследовательская архитектура для video world models, которая хранит видеопатчи в 3D и возвращает их в нужной точке обзора; заявлены навигация, редактирование памяти, динамические события и авторегрессионный rollout. Показанная длина навигации — до двух минут; к 5 сентября 2026 года код на странице проекта всё ещё помечен «Coming», поэтому это не готовый инструмент для внедрения.

## Development line

- The dated line is not written up yet; what is known stands in the sections below.

## What changed

2026-03-19 — опубликована страница MosaicMem и представлен препринт arXiv:2603.17117 от 17 марта 2026 года: метод объединяет 3D-патчи с latent-conditioning, PRoPE и выравниванием памяти; авторы сравнивают его с GEN3C и Context-as-Memory.

Дополнение к событию 2026-03-19: препринт был размещён на arXiv 17 марта 2026 года, а авторская запись на Hugging Face Papers датирована 19 марта 2026 года. Практический лимит, заявленный на странице проекта, — исследовательская навигация до двух минут, а не выпуск SDK или весов.

## How to use this

As of 2026-03-19, no supported workflow change follows from this record alone; practitioners should treat the linked MosaicMem webpage as a lead for future research, not as evidence of a capability, release, or adoption recommendation.

1. Используйте страницу проекта и препринт как спецификацию метода: подготовьте видеогенератор с доступом к camera pose, представлению патчей и conditioning; готового официального кода, весов или API страница не предоставляет.
  — <https://mosaicmem.github.io/mosaicmem/>
2. Реализуйте или оцените схему как исследовательский pipeline: lift патчей в 3D, retrieval для целевого вида, patch-and-compose, затем генерация с PRoPE и alignment.
  — <https://arxiv.org/abs/2603.17117>

## Best practices

- Не объявляйте MosaicMem готовой production-библиотекой: официальный проект указывает, что код появится позже; воспроизводимость требует собственной реализации либо будущего официального релиза.
  — <https://mosaicmem.github.io/mosaicmem/>
- Оценивайте отдельно сохранение геометрии при возврате камеры и способность генерировать динамику: именно этот компромисс метод пытается улучшить относительно explicit- и implicit-memory baselines.
  — <https://arxiv.org/abs/2603.17117>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- Официальные код, веса, лицензия, требования к вычислениям и воспроизводимый практический workflow не опубликованы на использованной странице проекта.
- Не найдено последующего датированного официального события, которое меняло бы статус метода после 19 марта 2026 года.

## Sources

| source | title | read |
|---|---|---|
| https://mosaicmem.github.io/mosaicmem/ | MosaicMem | 2026-09-05 |
| https://arxiv.org/abs/2603.17117 | MosaicMem: Hybrid Spatial Memory for Controllable Video World Models | 2026-09-05 |
| https://huggingface.co/papers/2603.17117 | Paper page - MosaicMem: Hybrid Spatial Memory for Controllable Video World Models | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:mosaicmem`, thread `mosaicmem-development`, 0 dated events - → -.
- **Practical note:** As of 2026-03-19, no supported workflow change follows from this record alone; practitioners should treat the linked MosaicMem webpage as a lead for future research, not as evidence of a capability, release, or adoption recommendation.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
