---
title: SHELLS
category: projects

tags: [google-shells, project, shells]
aliases: ["SHELLS"]
---

# SHELLS

**Development line:** `project:google-shells` · thread `shells`  
**Last event:** - · 0 dated since - · **Researched:** 2026-09-05 · confidence: high

## What it is

SHELLS — исследовательский метод для команд 3D-захвата: по калиброванным кадрам с нескольких камер он строит голову с фиксированной топологией и плотным семантическим соответствием. — DINOv2 с LoRA извлекает признаки; — грубая сетка направляет слои выборки вдоль нормалей; — общий трансформер предсказывает финальную сетку. Мера: 18k вершин за 0,08 с и около 2,4 GB заявленной inference-памяти в сравнении с 20 GB у объёмных базовых методов. Вывод: это спецификация для воспроизведения и оценки захвата, а не готовый публичный SDK.

## Development line

- The dated line is not written up yet; what is known stands in the sections below.

## What changed

2026-07-21 — SHELLS оформил переход от объёмной локальной доработки вершин к двухэтапной coarse-guided выборке поверхности: сначала грубая сетка, затем слои точек вокруг неё для одной согласованной 18k-вершинной реконструкции.

## How to use this

As of 2026-07-21, make no practice change from this line alone: retain the SHELLS and Google GNM links as leads for later verification before relying on either project or its relationship to the other.

1. Начинайте только с калиброванного многокамерного захвата: методу нужны изображения и параметры камер для проективной выборки признаков.
  — <https://arxiv.org/html/2605.31283v1>
2. Для самостоятельного воспроизведения реализуйте описанный порядок: DINOv2 с LoRA, разреженный глобальный граф, грубая сетка, затем слои точек на ±4 мм вдоль нормалей и общий трансформер.
  — <https://arxiv.org/html/2605.31283v1>
3. Оценивайте семантическое соответствие V2V и геометрическую близость к скану P2S отдельно: эти метрики могут расходиться.
  — <https://arxiv.org/html/2605.31283v1>
4. Не планируйте запуск из официального GitHub-репозитория SHELLS: он содержит код сайта проекта, а не реализацию модели или чекпойнты.
  — <https://github.com/syntec-research/SHELLS>

## Best practices

- Проверяйте калибровку, включая intrinsics, extrinsics и искажения объектива; метод использует известные параметры камер, а не решает геометрию из одиночного кадра.
  — <https://arxiv.org/html/2605.31283v1>
- Не используйте одиночный кадр как штатный вход: авторы называют single-view реконструкцию плохо определённой задачей; устойчивость показана от двух видов.
  — <https://arxiv.org/html/2605.31283v1>
- Не выдавайте сетку за фотореалистичный финальный актив: мелкие морщины и поры отсутствуют, для них нужен отдельный слой displacement maps и текстур.
  — <https://arxiv.org/html/2605.31283v1>
- Тестируйте крайние артикуляции языка и внешнюю геометрию волос или бороды отдельно: в опубликованных ограничениях эти случаи не покрыты надёжно.
  — <https://arxiv.org/html/2605.31283v1>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- Публичные код, веса, лицензия модели и воспроизводимый скрипт инференса SHELLS не найдены: официальный репозиторий SHELLS прямо описан как репозиторий сайта.
- Два исходных URL ведут к разным активам: SHELLS — к статье и сайту реконструкции, GNM — к параметрической модели головы. В тексте статьи SHELLS GNM не упомянут, поэтому их инженерная связь, помимо общих авторов и Google, не подтверждена.
- Не опубликован контракт подготовки реальных входных данных вне описанного авторами 13-камерного захвата, поэтому перенос на произвольную телефонную или некалиброванную съёмку не подтверждён.

## Sources

| source | title | read |
|---|---|---|
| https://arxiv.org/html/2605.31283v1 | Topologically Consistent Multi-view 3D Head Reconstruction via Coarse-Guided Layered Surface Sampling | 2026-09-05 |
| https://syntec-research.github.io/SHELLS/ | Topologically Consistent Multi-view 3D Head Reconstruction via Coarse-Guided Layered Surface Sampling | 2026-09-05 |
| https://github.com/syntec-research/SHELLS | GitHub - syntec-research/SHELLS: Website repository for the project SHELLS | 2026-09-05 |
| https://arxiv.org/abs/2605.31283v1 | arXiv:2605.31283v1 — Topologically Consistent Multi-view 3D Head Reconstruction via Coarse-Guided Layered Surface Sampling | 2026-09-05 |
| https://github.com/google/GNM/tree/main | GitHub - google/GNM: An open ecosystem of parametric human models and perception stacks, starting with GNM Head | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:google-shells`, thread `shells`, 0 dated events - → -.
- **Practical note:** As of 2026-07-21, make no practice change from this line alone: retain the SHELLS and Google GNM links as leads for later verification before relying on either project or its relationship to the other.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
