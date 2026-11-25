---
title: SketchVideo
category: projects
date: 2025-04-07
tags: [project, sketchvideo, sketchvideo-development]
aliases: ["SketchVideo"]
---

# SketchVideo

**Development line:** `project:sketchvideo` · thread `sketchvideo-development`  
**Last event:** 2025-04-07 · 2 dated since 2023-11-28 · **Researched:** 2026-09-04 · confidence: high

## What it is

SketchVideo — не единый инструмент для работы сегодня, а коллизия имён. — Sketch Video Synthesis (2023): оптимизирует Bézier-кривые поверх входного видео и экспортирует векторные SVG для стилизации, дорисовки и композитинга. — Sketch-based Video Generation and Editing (2025): генерирует или редактирует ролик по тексту и одному либо двум эскизам ключевых кадров. Ограничение актуального 2025 кода: до 49 кадров при 720×480; для A100 авторы указывают около 21 GB/95 s для SketchGen и 23 GB/230 s для SketchEdit. Вывод: выбирать нужно по авторскому репозиторию, а не по названию.

## Development line

- **2023-11-28 — SketchVideo project resources were made available.** Опубликованный код оптимизирует покадровые Bézier-кривые с CLIP-семантикой и межкадровой согласованностью, превращая исходное видео в SVG-эскиз.
- **2025-04-07 — A later SketchVideo resource set was linked.** Другой проект предоставил код и веса для генерации и локального редактирования видео по одному или двум эскизам ключевых кадров на базе CogVideo-2b.

## What changed

2023-11-28 — Sketch Video Synthesis: опубликованный код оптимизирует покадровые Bézier-кривые с CLIP-семантикой и межкадровой согласованностью, превращая исходное видео в SVG-эскиз. 2025-04-07 — SketchVideo: другой проект предоставил код и веса для генерации и локального редактирования видео по одному или двум эскизам ключевых кадров на базе CogVideo-2b.

Ни один из этих шагов не является обновлением другого: это два разных проекта с одинаковым именем.

## How to use this

As of 2025-04-07, practitioners should compare the later geometrylearning.com and IGLICT-linked resources with the 2023 project resources before selecting a SketchVideo implementation.

1. Для генеративного проекта создайте окружение Python 3.10 и установите зависимости; репозиторий требует diffusers==0.30.1.
  — <https://github.com/IGLICT/SketchVideo>
2. Скачайте веса SketchGen или SketchEdit и базовую модель CogVideo-2b, затем пропишите пути к ним в скриптах или config.py.
  — <https://github.com/IGLICT/SketchVideo>
3. Для генерации подготовьте эскиз 720×480 на одном или двух кадрах и запустите test_sketch_gen_single.sh либо test_sketch_gen_two.sh.
  — <https://github.com/IGLICT/SketchVideo>
4. Для редактирования подготовьте 49-кадровое видео 720×480, эскиз ключевого кадра и маски редактируемых областей, затем запустите test_sketch_edit.sh.
  — <https://github.com/IGLICT/SketchVideo>
5. Для векторизации видео используйте отдельный репозиторий 2023 года: установите зависимости, подготовьте клип короче 70 кадров с масками, постройте atlas и выполните operate_clipavideo.sh.
  — <https://github.com/yudianzheng/SketchVideo>

## Best practices

- Не смешивайте веса, инструкции и результаты двух репозиториев: их авторы, задачи и пайплайны различны.
  — <https://github.com/yudianzheng/SketchVideo>
- Для SketchVideo 2025 начинайте с одного или двух ключевых эскизов строго в 720×480; для редактирования входной клип должен содержать 49 кадров.
  — <https://github.com/IGLICT/SketchVideo>
- При нестабильном результате генеративного проекта пробуйте другие seed; авторы прямо не гарантируют успех на каждом запуске. Меньшее число DDIM-шагов сокращает время инференса.
  — <https://github.com/IGLICT/SketchVideo>
- Для проекта 2023 ограничивайте входной клип менее чем 70 кадрами и готовьте маски foreground-объекта до построения atlas.
  — <https://github.com/yudianzheng/SketchVideo>

## Superseded by this

- 2025-04-07: предположение, что IGLICT/SketchVideo является новой версией yudianzheng/SketchVideo, неверно; это независимый CVPR 2025 проект.
- 2025-04-01: для задачи генерации или редактирования по эскизу применим IGLICT/SketchVideo с весами; это не замена векторизации SVG из проекта 2023 года.

## Still unknown

- Страница http://geometrylearning.com/SketchVideo/ была недоступна при проверке, поэтому её содержимое не использовано.
- Не найдено доказательств общей кодовой базы, команды или преемственности между репозиториями 2023 и 2025; их следует вести как два отдельных subject_key.
- event_findings: 2023-11-28 — arXiv-первичник от 2023-11-26 уточняет авторов (Yudian Zheng, Xiaodong Cun, Menghan Xia, Chi-Man Pun) и то, что метод оптимизирует Bézier-кривые с CLIP-семантической потерей и atlas-based consistency loss; источник https://arxiv.org/abs/2311.15306.
- event_findings: 2025-04-07 — репозиторий уточняет названия весов SketchGen и SketchEdit, базу CogVideo-2b и лимит 49 кадров 720×480; README датирует релиз кода и весов 2025-04-01; источник https://github.com/IGLICT/SketchVideo.
- new_events: 2023-11-26 — опубликован arXiv-препринт Sketch Video Synthesis; источник https://arxiv.org/abs/2311.15306.
- new_events: 2025-03-30 — для независимого SketchVideo запущена project page и обновлён arXiv-препринт; источник https://github.com/IGLICT/SketchVideo.
- new_events: 2025-04-01 — для независимого SketchVideo опубликованы код и веса; источник https://github.com/IGLICT/SketchVideo.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/yudianzheng/SketchVideo | yudianzheng/SketchVideo — Sketch Video Synthesis | 2026-09-05 |
| https://sketchvideo.github.io/ | Sketch Video Synthesis project page | 2026-09-05 |
| https://arxiv.org/abs/2311.15306 | Sketch Video Synthesis | 2026-09-05 |
| https://github.com/IGLICT/SketchVideo | IGLICT/SketchVideo — Sketch-based Video Generation and Editing | 2026-09-05 |
| https://arxiv.org/abs/2503.23284 | SketchVideo: Sketch-based Video Generation and Editing | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:sketchvideo`, thread `sketchvideo-development`, 2 dated events 2023-11-28 → 2025-04-07.
- **Practical note:** As of 2025-04-07, practitioners should compare the later geometrylearning.com and IGLICT-linked resources with the 2023 project resources before selecting a SketchVideo implementation.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
