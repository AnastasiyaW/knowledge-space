---
title: Z-Image-Turbo-Fun-Controlnet-Union
category: projects
date: 2025-12-12
tags: [project, z-image-turbo-fun-controlnet-union, z-image-turbo-fun-controlnet-union-development, z_image]
aliases: ["Z-Image-Turbo-Fun-Controlnet-Union", "Z-Image-Turbo-Fun-Controlnet-Union-2.0"]
---

# Z-Image-Turbo-Fun-Controlnet-Union

**Development line:** `project:z-image-turbo-fun-controlnet-union` · thread `z-image-turbo-fun-controlnet-union-development`  
**Last event:** 2025-12-12 · 2 dated since 2025-12-02 · **Researched:** 2026-09-05 · confidence: high

## What it is

Z-Image-Turbo-Fun-Controlnet-Union — семейство весов ControlNet для Z-Image-Turbo в VideoX-Fun. Возможности: направлять генерацию по контурам, глубине, позе, линиям, Scribble и Gray; использовать inpaint; применять отдельный Tile-чекпойнт для сверхразрешения. Текущая Union 2.1-2602-8steps поддерживает семь типов контроля и рассчитана на 8 шагов. Вердикт: это локальный workflow, не hosted inference provider; актуальная ветка 2.1 заменила 1.0 и 2.0 для практического применения.

## Development line

- **2025-12-02 — Initial Z-Image-Turbo-Fun-Controlnet-Union repository milestone.** ControlNet на шести блоках с Canny, HED, Depth, Pose и MLSD.
- **2025-12-12 — Z-Image-Turbo-Fun-Controlnet-Union 2.0 repository milestone.** Больше управляемых блоков, более длительное обучение и режим inpaint.

## What changed

2025-12-02 — опубликован исходный Z-Image-Turbo-Fun-Controlnet-Union: ControlNet на шести блоках с Canny, HED, Depth, Pose и MLSD. 2025-12-12 — опубликован Z-Image-Turbo-Fun-Controlnet-Union-2.0: больше управляемых блоков, более длительное обучение и режим inpaint. 2025-12-17 — 2.1 исправил ошибку 2.0, из-за которой блоки выполняли два forward pass и замедляли inference. 2025-12-22 — вышли 8-step дистилляция 2.1 и Tile-модель для сверхразрешения. 2026-01-12 — 2601 добавил Scribble, lite-варианты и переобучение против mask leakage и артефактов. 2026-02-26 — 2602 добавил Gray Control.

## How to use this

From 2025-12-02, practitioners should use the linked Z-Image-Turbo-Fun-Controlnet-Union repository as the dated starting point for this line; from 2025-12-12, they should separately evaluate the linked 2.0 repository rather than assume it is identical to the initial repository.

1. Склонировать VideoX-Fun и создать каталоги моделей `models/Diffusion_Transformer` и `models/Personalized_Model`.
  — <https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union-2.0>
2. Скачать базовые веса Z-Image-Turbo и актуальный `Z-Image-Turbo-Fun-Controlnet-Union-2.1-2602-8steps.safetensors`; положить ControlNet в `models/Personalized_Model`.
  — <https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union-2.0>
3. Подать подготовленное control-изображение нужного типа и запускать 2.1 workflow из VideoX-Fun; для inpaint использовать соответствующий пример `predict_i2i_inpaint_2.1.py`.
  — <https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union-2.0>
4. Для 2602 Union использовать 8 diffusion steps и выбрать один из Canny, Depth, Pose, MLSD, HED, Scribble или Gray control.
  — <https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union-2.0>

## Best practices

- Для новой установки выбирать 2.1-2602-8steps: она включает исправления 2.0, 8-step дистилляцию и Gray Control.
  — <https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union-2.0>
- Держать подробный текстовый prompt; для 2.1 и 2.0 подбирать `control_context_scale` в диапазоне 0.65–1.00, а при inpaint увеличивать его для непрерывности изображения.
  — <https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union-2.0>
- Для слабого оборудования или более естественного результата при высоком control scale использовать lite 2601/2602; это ослабляет управление, поскольку контроль применяется к меньшему числу слоёв.
  — <https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union-2.0>

## Superseded by this

- 2025-12-17 — Z-Image-Turbo-Fun-Controlnet-Union-2.0 устарел для новых запусков: 2.1 исправляет его ошибку двойного forward pass и возвращает скорость single-step inference.
- 2025-12-22 — недистиллированный 2.1 уступает 2.1-8steps для обычной генерации: модельная карта рекомендует 8 шагов.
- 2026-02-26 — 2.1-2601-8steps не покрывает Gray Control; для него нужен 2.1-2602-8steps.

## Still unknown

- Путь `Z-Image-Turbo-Fun-Controlnet-Union-2.0` сейчас перенаправляет на 2.1; отдельная неизменяемая модельная карточка 2.0 по этому URL не доступна. Исторические свойства 2.0 подтверждены сохранённым разделом «Models Before 2601» в текущей первичной карточке.
- Нельзя установить из доступных первичных страниц, какой именно текст сопровождал The source-сообщения; выводы привязаны к датам публикации и обновления весов в первичном репозитории.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union | alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union — Hugging Face model card | 2026-09-05 |
| https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union/commits/main | Commit history — Z-Image-Turbo-Fun-Controlnet-Union | 2026-09-05 |
| https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union-2.0 | Z-Image-Turbo-Fun-Controlnet-Union-2.0 URL, redirected to the maintained 2.1 model card | 2026-09-05 |
| https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union-2.1/commits/main | Commit history — Z-Image-Turbo-Fun-Controlnet-Union-2.1 | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:z-image-turbo-fun-controlnet-union`, thread `z-image-turbo-fun-controlnet-union-development`, 2 dated events 2025-12-02 → 2025-12-12.
- **Practical note:** From 2025-12-02, practitioners should use the linked Z-Image-Turbo-Fun-Controlnet-Union repository as the dated starting point for this line; from 2025-12-12, they should separately evaluate the linked 2.0 repository rather than assume it is identical to the initial repository.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
