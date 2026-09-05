---
title: Seoul World Model — Public project release
category: projects
date: 2026-03-17
tags: [project, public-project-release, seoul-world-model]
aliases: ["Seoul World Model"]
---

# Seoul World Model — Public project release

**Development line:** `project:seoul-world-model` · thread `public-project-release`  
**Last event:** 2026-03-17 · 1 dated since 2026-03-17 · **Researched:** 2026-09-05 · confidence: high

## What it is

Seoul World Model (SWM) — исследовательская модель мира, которая генерирует видео маршрута по координатам, траектории камеры и текстовому сценарию, извлекая уличные изображения Сеула из геоиндекса. — удерживает геометрию и внешний вид места через retrieval-augmented conditioning; — поддерживает произвольное движение камеры и текстовые изменения сцены; — повторно привязывает генерацию к будущей точке маршрута через Virtual Lookahead Sink. Ограничение: на 2026-09-05 официально не опубликованы веса, inference-код, синтетические данные и код интерполяции, поэтому это пока не доступный для развёртывания инструмент.

## Development line

- **2026-03-17 — Seoul World Model public project and code references recorded.** On 2026-03-17, the Seoul World Model development line recorded links to a public project website and a GitHub repository. This is a material public reference point for the project's history because it connects the project to both an official presentation surface and source-code location.

## What changed

2026-03-17 — Seoul World Model появился как официальный проект к работе Grounding World Simulation Models in a Real-World Metropolis; репозиторий объявил будущую публикацию весов, inference-кода, синтетических данных и компонентов подготовки обучающих видео.

Дополнение к событию 2026-03-17: препринт от 2026-03-16 называет систему Seoul World Model (SWM), описывает её как дообучение предобученной video-world model и уточняет состав обучения: 440 тыс. уличных изображений Сеула, реальные driving-видео и синтетические городские данные. Источник: https://arxiv.org/abs/2603.15583.

Новое событие 2026-03-16: опубликован препринт Grounding World Simulation Models in a Real-World Metropolis, задавший метод: геопривязанный retrieval, cross-temporal pairing, синтетические траектории и Virtual Lookahead Sink. Источник: https://arxiv.org/abs/2603.15583.

## How to use this

From 2026-03-17, practitioners should use the Seoul World Model project website together with its linked GitHub repository as the starting point for evaluating and obtaining the project, rather than relying on an unverified repost.

1. Проверьте официальный репозиторий перед планированием эксперимента: на текущий момент он не даёт загрузки модели или inference-инструкций.
  — <https://github.com/naver-ai/seoul-world-model>
2. Используйте проектную страницу и статью как спецификацию исследовательского воспроизведения: входы системы — стартовая геопозиция, траектория камеры, текстовый промпт и локальная база street-view-референсов.
  — <https://seoul-world-model.github.io/>
3. Не заявляйте воспроизводимость или производственное применение до публикации весов, inference-кода и данных авторами.
  — <https://github.com/naver-ai/seoul-world-model>

## Best practices

- Оценивайте привязку к месту отдельно от визуальной правдоподобности: в абляции меньшее число референсов снижало mPSNR, хотя FID/FVD не показывали однозначного ухудшения.
  — <https://arxiv.org/abs/2603.15583>
- Для длинных маршрутов повторно извлекайте референс впереди по траектории, а не полагайтесь только на начальный кадр: это принцип Virtual Lookahead Sink из работы.
  — <https://arxiv.org/abs/2603.15583>
- Не подменяйте ожидаемую публикацию доступным релизом: в официальном репозитории всё ещё указано, что веса и код будут выпущены позднее.
  — <https://github.com/naver-ai/seoul-world-model>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- Официальный репозиторий содержит только README и не имеет GitHub Releases; дата публикации весов, inference-кода, синтетических данных и кода интерполяции не названа.
- Цифры данных требуют осторожности: проектная страница говорит о 1,2 млн панорам и 10 тыс. синтетических видео, а статья уточняет 440 тыс. street-view изображений в составе fine-tuning; это разные уровни пайплайна, но авторы не публикуют готовый набор и точную конфигурацию обучения.

## Sources

| source | title | read |
|---|---|---|
| https://seoul-world-model.github.io/ | Seoul World Model: Grounding World Simulation Models in a Real-World Metropolis | 2026-09-05 |
| https://github.com/naver-ai/seoul-world-model | naver-ai/seoul-world-model | 2026-09-05 |
| https://github.com/naver-ai/seoul-world-model/releases | Releases · naver-ai/seoul-world-model | 2026-09-05 |
| https://arxiv.org/abs/2603.15583 | Grounding World Simulation Models in a Real-World Metropolis | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:seoul-world-model`, thread `public-project-release`, 1 dated events 2026-03-17 → 2026-03-17.
- **Practical note:** From 2026-03-17, practitioners should use the Seoul World Model project website together with its linked GitHub repository as the starting point for evaluating and obtaining the project, rather than relying on an unverified repost.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
