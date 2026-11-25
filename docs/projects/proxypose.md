---
title: ProxyPose
category: projects
date: 2026-07-11
tags: [project, proxypose, proxypose-development]
aliases: ["ProxyPose"]
---

# ProxyPose

**Development line:** `project:proxypose` · thread `proxypose-development`  
**Last event:** 2026-07-11 · 1 dated since 2026-07-11 · **Researched:** 2026-09-05 · confidence: high

## What it is

ProxyPose — метод и открытая реализация для исследователей компьютерного зрения, которым нужна 6-DoF-траектория локальной поверхности или объекта из монокулярного видео. Возможности: RGB-видео и одна точка в первом кадре; генерация proxy-видео с цветным многогранником; восстановление позы геометрическим PnP; применение к объектам, камере и лицам. Ограничение: быстрые движения, отражающие и текстурно-бедные поверхности могут вызвать drift или размыть proxy-кадры. Вердикт: практичен для воспроизводимой исследовательской оценки на GPU, если допускается генеративный этап и проверка результатов.

## Development line

- **2026-07-11 — ProxyPose public project resources linked.** On 2026-07-11, ProxyPose was presented through linked project, source-code, and Hugging Face resources. This is a material public development-line event because it establishes a discoverable project presence, although the linked resources' technical claims and release status were not independently researched.

## What changed

2026-07-11 — опубликованы проектная страница, исходный код и веса ProxyPose для 6-DoF pose tracking через video-to-video translation.

## How to use this

As of 2026-07-11, practitioners should use the linked project page, repository, and Hugging Face resource as the starting points for evaluating ProxyPose, while treating this link-only event as unverified for technical capabilities and release details.

1. Клонировать репозиторий, создать окружение Python 3.10, установить PyTorch CUDA 12.1, PyTorch3D и пакет ProxyPose.
  — <https://github.com/ruihangzhang97/proxypose>
2. Открыть локальный annotator командой `proxypose-annotate --input-video ...`, выбрать точку в первом кадре и сохранить JSON с координатами.
  — <https://github.com/ruihangzhang97/proxypose>
3. При необходимости оценить фокусное расстояние через Depth Anything 3; иначе используется фиксированный горизонтальный FOV 45°.
  — <https://github.com/ruihangzhang97/proxypose>
4. Запустить `proxypose-infer` с видео, JSON-точки и выходным путём; для меньшей модели передать конфигурацию Wan2.1-T2V-1.3B.
  — <https://github.com/ruihangzhang97/proxypose>

## Best practices

- Начинать с 14B для качества, а 1.3B выбирать для быстрых экспериментов или ограниченной VRAM; LoRA и базовая модель должны соответствовать выбранному размеру.
  — <https://github.com/ruihangzhang97/proxypose>
- Использовать оценённую Depth Anything 3 фокусную длину, когда точность геометрии важнее быстрого запуска.
  — <https://github.com/ruihangzhang97/proxypose>
- Проверять траектории вручную на быстрых, отражающих и текстурно-бедных сценах: эти случаи заявлены как источники drift и деградации contour detection.
  — <https://ruihangzhang97.github.io/proxypose/>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- Дата добавления в репозиторий текущей поддержки Wan2.1-T2V-1.3B не подтверждена доступной историей коммитов, поэтому она не внесена как отдельное датированное событие.

## Sources

| source | title | read |
|---|---|---|
| https://ruihangzhang97.github.io/proxypose/ | ProxyPose — 6-DoF Pose Tracking via Video-to-Video Translation | 2026-09-05 |
| https://github.com/ruihangzhang97/proxypose | Official ProxyPose repository and installation guide | 2026-09-05 |
| https://arxiv.org/abs/2607.06555 | ProxyPose: 6-DoF Pose Tracking via Video-to-Video Translation | 2026-09-05 |
| https://github.com/ruihangzhang97/proxypose/issues/2 | Issue #2: Request for Wan2.1-T2V-1.3B ProxyPose variant | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:proxypose`, thread `proxypose-development`, 1 dated events 2026-07-11 → 2026-07-11.
- **Practical note:** As of 2026-07-11, practitioners should use the linked project page, repository, and Hugging Face resource as the starting points for evaluating ProxyPose, while treating this link-only event as unverified for technical capabilities and release details.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
