---
title: LocateAnything — Model release
category: projects
date: 2026-05-29
tags: [locateanything, model-release, project]
aliases: ["LocateAnything"]
---

# LocateAnything — Model release

**Development line:** `project:locateanything` · thread `model-release`  
**Last event:** 2026-05-29 · 1 dated since 2026-05-29 · **Researched:** 2026-09-05 · confidence: high

## What it is

LocateAnything — исследовательская 3B-модель NVIDIA из семейства Eagle для visual grounding: object detection, referring-expression grounding, GUI grounding, OCR/text localization, layout grounding и pointing. Она предсказывает целый bounding box параллельно, а не координаты по одному токену; заявлено 12.7 boxes/s на одном H100 в Hybrid Mode. Вердикт: подходит для R&D и локальной интеграции задач локализации, но опубликованные веса имеют некоммерческую лицензию.

## Development line

- **2026-05-29 — NVIDIA published LocateAnything resources and a LocateAnything-3B model page.** On 2026-05-29, NVIDIA's LocateAnything research page and the linked NVIDIA LocateAnything-3B Hugging Face model page were shared. This marks a public project-and-model availability step in LocateAnything's development history.

## What changed

2026-05-29 — LocateAnything стала доступна как LocateAnything-3B; первичные материалы уточняют, что публикация кода, весов, демо, веб-страницы и отчёта датирована 2026-05-26, а не 29 мая. Модель объединяет MoonViT-SO-400M, Qwen2.5-3B-Instruct и MLP-проектор; Parallel Box Decoding предсказывает x1,y1,x2,y2 одним блоком. Данные обучения: 12M изображений, 138M+ запросов и 785M боксов. 2026-06 — в Eagle добавлены batch inference на FlashAttention для A100/RTX 4090 и LoRA-скрипт для visual-prompt fine-tuning; при этом базовый публичный checkpoint по-прежнему не поддерживает visual-prompt inference без дообучения.

## How to use this

From 2026-05-29, practitioners can assess LocateAnything through NVIDIA's public research resource and the linked LocateAnything-3B model page before choosing it for object-location workflows.

1. Клонируйте NVlabs/Eagle, перейдите в Embodied и установите пакет командой pip install -e .
  — <https://github.com/NVlabs/EAGLE/blob/main/Embodied/README.md>
2. Загрузите nvidia/LocateAnything-3B через LocateAnythingWorker, передайте RGB-изображение и вызовите detect, ground_multi, detect_text, ground_gui либо point.
  — <https://github.com/NVlabs/EAGLE/blob/main/Embodied/README.md>
3. Разберите ответ: box-координаты лежат в диапазоне 0–1000, поэтому масштабируйте их на ширину и высоту исходного изображения.
  — <https://github.com/NVlabs/EAGLE/blob/main/Embodied/README.md>
4. Для пакетной обработки скачайте модельный репозиторий и запустите batch_infer.py с --attn la_flash и подходящим batch size.
  — <https://github.com/NVlabs/EAGLE/blob/main/Embodied/README.md>

## Best practices

- Для обычного запуска используйте Hybrid Mode: Fast Mode применяется по умолчанию, а проблемные блоки переобрабатываются Slow Mode.
  — <https://research.nvidia.com/labs/lpr/locate-anything/>
- Для полного ответа задавайте max_new_tokens=8192; модельная карточка рекомендует Hybrid Mode как компромисс между скоростью и точностью.
  — <https://huggingface.co/nvidia/LocateAnything-3B>
- На A100 и других не-Hopper/Blackwell GPU используйте la_flash batch runtime вместо dense SDPA; опубликованный пример на A100 уменьшает peak reserved memory с 35.12 GB до 11.71 GB.
  — <https://github.com/NVlabs/EAGLE/blob/main/Embodied/README.md>
- Не рассчитывайте на visual-prompt inference у исходного nvidia/LocateAnything-3B: для этой задачи нужен собственный fine-tuning по опубликованному коду.
  — <https://github.com/NVlabs/EAGLE/blob/main/Embodied/README.md>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- Первичные источники датируют первоначальную публикацию 2026-05-26, тогда как событие зафиксировано 2026-05-29; доступные материалы не объясняют трёхдневный разрыв.
- Для июньских обновлений Eagle публикует только месяц, а не точные дни, поэтому их нельзя надёжно привязать к отдельным дневным событиям.
- Не найдено первичного подтверждения, что публичные веса получили коммерческое разрешение; модельная карточка по-прежнему ограничивает их академическими и некоммерческими исследованиями.

## Sources

| source | title | read |
|---|---|---|
| https://research.nvidia.com/labs/lpr/locate-anything/ | LocateAnything: Fast and High-Quality Vision-Language Grounding with Parallel Box Decoding | 2026-09-05 |
| https://huggingface.co/nvidia/LocateAnything-3B | nvidia/LocateAnything-3B model card | 2026-09-05 |
| https://github.com/NVlabs/EAGLE | NVlabs/Eagle repository | 2026-09-05 |
| https://github.com/NVlabs/EAGLE/blob/main/Embodied/README.md | LocateAnything implementation and usage guide | 2026-09-05 |
| https://arxiv.org/abs/2605.27365 | LocateAnything: Fast and High-Quality Vision-Language Grounding with Parallel Box Decoding | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:locateanything`, thread `model-release`, 1 dated events 2026-05-29 → 2026-05-29.
- **Practical note:** From 2026-05-29, practitioners can assess LocateAnything through NVIDIA's public research resource and the linked LocateAnything-3B model page before choosing it for object-location workflows.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
