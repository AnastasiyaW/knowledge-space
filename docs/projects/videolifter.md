---
title: VideoLifter
category: projects
date: 2025-01-22
tags: [project, videolifter]
aliases: ["VideoLifter"]
---

# VideoLifter

**Development line:** `project:videolifter` · thread `videolifter`  
**Last event:** 2025-01-22 · 2 dated since 2025-01-09 · **Researched:** 2026-09-05 · confidence: medium

## What it is

VideoLifter — SfM-free фреймворк для исследователей 3D-реконструкции: принимает некалиброванные изображения из видео, использует DUSt3R и MASt3R для начальной геометрии, затем оптимизирует 3D Gaussian representation и выравнивает фрагменты в общую сцену. Возможности: оценка поз и структуры, реконструкция длинных видео по локальным окнам, novel-view synthesis. Мера: авторы заявляют сокращение времени обучения более чем на 82%. Вердикт: применять стоит на CUDA-окружении и подготовленных Tanks and Temples либо CO3D, ожидая исследовательский pipeline с обучением и оценкой.

## Development line

- **2025-01-09 — VideoLifter project website referenced.** Иерархическое stereo-выравнивание заменяет предварительно рассчитанные камеры и традиционный SfM при переходе от видео к 3D.
- **2025-01-22 — VideoLifter GitHub repository referenced.** On 2025-01-22, a dated record linked the VITA-Group/VideoLifter GitHub repository and an earlier related The recorded link. This establishes a public source-repository reference in the project history, but does not establish repository version, release, commit, or feature status on that date.

## What changed

2025-01-09 — опубликовано описание метода: иерархическое stereo-выравнивание заменяет предварительно рассчитанные камеры и традиционный SfM при переходе от видео к 3D. 2025-01-22 — появился официальный репозиторий воспроизведения с зависимостями, предобученным MASt3R checkpoint и отдельными скриптами для Tanks and Temples и CO3D.

## How to use this

From 2025-01-22, practitioners locating VideoLifter implementation material should begin with the linked VITA-Group/VideoLifter repository, using the 2025-01-09 website as the public project entry point and separately verifying version, license, and usage details.

1. Клонируйте репозиторий с submodules и скачайте checkpoint MASt3R_ViTLarge_BaseDecoder_512_catmlpdpt_metric.pth в submodules/mast3r/checkpoints.
  — <https://github.com/VITA-Group/VideoLifter>
2. Создайте conda-окружение с Python 3.10, PyTorch 2.1.0 и CUDA 11.8; затем установите requirements и два локальных CUDA-пакета.
  — <https://github.com/VITA-Group/VideoLifter>
3. Подготовьте данные: Tanks and Temples в data/Tanks либо авторский CO3D preprocessing в data/co3d.
  — <https://github.com/VITA-Group/VideoLifter>
4. Запустите scripts/train_tt.sh для Tanks and Temples или scripts/train_co3d.sh для CO3D; результаты предназначены для обучения и оценки 3D-реконструкции.
  — <https://github.com/VITA-Group/VideoLifter>

## Best practices

- Клонируйте с --recursive: DUSt3R и MASt3R подключены как submodules, без них pipeline не воспроизводится.
  — <https://github.com/VITA-Group/VideoLifter>
- Используйте зафиксированные авторами версии Python, PyTorch и CUDA, а не произвольное современное окружение.
  — <https://github.com/VITA-Group/VideoLifter>
- Скомпилируйте CUDA kernels для RoPE из CroCo: авторы помечают это как необязательное, но настоятельно рекомендуемое ускорение.
  — <https://github.com/VITA-Group/VideoLifter>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- Не найдено датированного release-тега, пакета или модели VideoLifter после исходного репозитория; текущая документация описывает исследовательское воспроизведение, но не подтверждает поддержку произвольных пользовательских видео как готового продукта.
- Для события 2025-01-22 GitHub README доступен, но его страница не указывает собственную дату конкретного изменения; поэтому детали окружения следует читать как текущее состояние официального репозитория, а не как доказательство того, что каждая из них была добавлена именно 22 января.

## Sources

| source | title | read |
|---|---|---|
| https://videolifter.github.io/ | VideoLifter: Lifting Videos to 3D with Fast Hierarchical Stereo Alignment | 2026-09-05 |
| https://github.com/VITA-Group/VideoLifter | VITA-Group/VideoLifter — official implementation | 2026-09-05 |
| https://arxiv.org/abs/2501.01949 | VideoLifter: Lifting Videos to 3D with Fast Hierarchical Stereo Alignment | 2026-09-05 |
| https://ece.utexas.edu/news/wenyan-cong-receives-best-paper-award-cvpr-workshop | Wenyan Cong Receives Best Paper Award at CVPR Workshop | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:videolifter`, thread `videolifter`, 2 dated events 2025-01-09 → 2025-01-22.
- **Practical note:** From 2025-01-22, practitioners locating VideoLifter implementation material should begin with the linked VITA-Group/VideoLifter repository, using the 2025-01-09 website as the public project entry point and separately verifying version, license, and usage details.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
