---
title: IGGT4D
category: projects
date: 2026-07-22
tags: [iggt4d, project]
aliases: ["IGGT4D"]
---

# IGGT4D

**Development line:** `project:iggt4d` · thread `iggt4d`  
**Last event:** 2026-07-22 · 1 dated since 2026-07-22 · **Researched:** 2026-09-05 · confidence: medium

## What it is

IGGT4D — модель, которая последовательно обрабатывает видеокадры и совместно предсказывает камеру, геометрию, устойчивые идентичности объектов и instance masks. Возможности: потоковая 4D-реконструкция; оценка позы; трекинг объектов; open-vocabulary сегментация. Ограничение: checkpoint на 1B параметров требует принять условия доступа на Hugging Face; датасет, benchmark, обучение и оценочный код ещё не выпущены. Вердикт: пригоден для inference-исследований с собственными последовательностями изображений, но не для полного воспроизводимого обучения или бенчмаркинга.

## Development line

- **2026-07-22 — IGGT4D GitHub Pages site was linked.** Причинная потоковая модель для объединения геометрии сцены и постоянных идентичностей объектов.

## What changed

2026-07-22 — IGGT4D был представлен как Streaming 4D Instance-Grounded Geometry Transformer: причинная потоковая модель для объединения геометрии сцены и постоянных идентичностей объектов.

## How to use this

From 2026-07-22, practitioners should treat the linked IGGT4D GitHub Pages site as a project reference point, while verifying its specific guidance or release status before relying on it.

1. Клонируйте официальный репозиторий и создайте окружение Conda с Python 3.10.
  — <https://github.com/HorizonRobotics/IGGT4D>
2. Установите PyTorch; README приводит пример PyTorch 2.8.0 с CUDA 12.8, затем установите пакет через `pip install -e .`.
  — <https://github.com/HorizonRobotics/IGGT4D>
3. Примите условия доступа к checkpoint на Hugging Face, скачайте его и сохраните как `checkpoints/model.safetensors`.
  — <https://huggingface.co/HorizonRobotics/IGGT4D>
4. Запустите `python streaming_infer.py` для demo либо передайте `--image-dir` и `--output-dir` для собственной последовательности RGB-кадров.
  — <https://github.com/HorizonRobotics/IGGT4D>
5. При необходимости включите `--camera` для внешних параметров камеры и сохранение результатов через `--save-npy` или `--save-ply`.
  — <https://github.com/HorizonRobotics/IGGT4D>

## Best practices

- Оставляйте streaming-режимом режим по умолчанию для длинных последовательностей; `--mode full` — offline full-attention вариант.
  — <https://github.com/HorizonRobotics/IGGT4D>
- Не планируйте обучение, оценку или сравнение на официальном benchmark до их релиза: в репозитории они остаются в списке ожидаемых артефактов.
  — <https://github.com/HorizonRobotics/IGGT4D>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- Для события 2026-07-22 первичный arXiv-источник уточняет дату подачи статьи: 2026-07-21 16:00:01 UTC; это подтверждает название, десять авторов и масштаб InsScene4D-147K, но не даёт отдельной датированной публикации именно на 2026-07-22.
- Точная дата, когда inference-код и checkpoint стали доступны, не указана на прочитанных первичных страницах; поэтому это не добавлено как отдельное датированное событие.
- Публичная страница проекта говорит, что датасет и benchmark выйдут позднее, а репозиторий также ожидает training и evaluation code.

## Sources

| source | title | read |
|---|---|---|
| https://iggt4d.github.io/ | IGGT4D: Streaming 4D Instance-Grounded Geometry Transformer | 2026-09-05 |
| https://arxiv.org/abs/2607.19228 | IGGT4D: Streaming 4D Instance-Grounded Geometry Transformer | 2026-09-05 |
| https://github.com/HorizonRobotics/IGGT4D | HorizonRobotics/IGGT4D | 2026-09-05 |
| https://huggingface.co/HorizonRobotics/IGGT4D | HorizonRobotics/IGGT4D model card | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:iggt4d`, thread `iggt4d`, 1 dated events 2026-07-22 → 2026-07-22.
- **Practical note:** From 2026-07-22, practitioners should treat the linked IGGT4D GitHub Pages site as a project reference point, while verifying its specific guidance or release status before relying on it.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
