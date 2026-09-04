---
title: SeedVR2
category: projects
date: 2026-07-30
tags: [project, seedvr, seedvr2, seedvr2-development-and-distribution]
aliases: ["SeedVR2"]
---

# SeedVR2

**Development line:** `project:seedvr2` · thread `seedvr2-development-and-distribution`  
**Last event:** 2026-07-30 · 3 dated since 2025-06-09 · **Researched:** 2026-09-04 · confidence: high

## What it is

SeedVR2 — наследник SeedVR для prompt-free восстановления видео и изображений: одноступенчатый апскейл, адаптивное оконное внимание, модели 3B и 7B, а также сторонняя 1.44B-дистилляция для менее ёмкого оборудования. Ограничение: официальный запуск ориентирован на многопроцессорную GPU-инференс-схему; 1.4B-вариант поддерживает только изображения и требует отдельной поддержки загрузчика ComfyUI. Вердикт: для максимальной точности берите официальные 3B/7B, а 1.4B — осознанный компромисс скорости и детализации.

## Development line

- **2025-06-09 — SeedVR2 project page was linked.** On 2025-06-09, a link to the SeedVR2 project page was recorded. The dated link establishes a public reference point for the project, but does not itself establish a release, model availability, or implementation details.
- **2025-06-11 — SeedVR code and model repositories were linked.** On 2025-06-11, links to the ByteDance-Seed/SeedVR source repository and the SeedVR model repository on Hugging Face were recorded. This is an upstream distribution and reference event for the SeedVR2 line, although the supplied links alone do not prove the exact relationship between SeedVR and SeedVR2 or a release state on that date.
- **2026-07-30 — SeedVR2-1.4B ComfyUI package was linked.** On 2026-07-30, a Hugging Face repository named SeedVR2-1.4B and its ComfyUI directory were linked. This records a practical ComfyUI-oriented distribution path for the named model, although the dated links alone do not verify its provenance, completeness, or compatibility.

## What changed

2025-06-09 — SeedVR2 представлен как одноступенчатое adversarial diffusion-восстановление видео; входные размеры должны быть кратны 32. 2025-06-11 — создан официальный репозиторий с кодом запуска и checkpoint-моделями SeedVR2-3B/7B. 2026-07-30 — опубликована сторонняя 1.44B шестислойная дистилляция SeedVR2-7B с готовой интеграцией в ComfyUI для апскейла статичных изображений.

## How to use this

As of 2026-07-30, practitioners should treat SeedVR2 as a versioned deployment path: consult the official project and repository references first, then independently assess the linked 1.4B ComfyUI package before using it in a workflow.

1. Для официального запуска клонируйте репозиторий, создайте окружение Python 3.10, установите requirements, FlashAttention и совместимый Apex.
  — <https://github.com/ByteDance-Seed/SeedVR>
2. Скачайте официальный checkpoint, например ByteDance-Seed/SeedVR2-3B, в локальную папку ckpts/ через snapshot_download.
  — <https://github.com/ByteDance-Seed/SeedVR>
3. Запустите projects/inference_seedvr2_3b.py через torchrun, указав входную папку, выходное разрешение, seed и sequence-parallel degree; размеры входа должны быть кратны 32.
  — <https://github.com/ByteDance-Seed/SeedVR>
4. Для 1.4B-варианта в ComfyUI положите ComfyUI checkpoint в models/diffusion_models, VAE в models/vae, скопируйте support folder в custom_nodes и перезапустите ComfyUI.
  — <https://huggingface.co/lvladikov/SeedVR2-1.4B>
5. Загрузите готовый workflow, начните с 4×; используйте один шаг, CFG 1, Euler/simple и denoise 1.
  — <https://huggingface.co/lvladikov/SeedVR2-1.4B/blob/main/comfyui/seedvr2_1.4b_upscale_image.json>

## Best practices

- Не используйте 1.4B checkpoint в стандартном SeedVR2 loader: шесть блоков требуют добавленной ветки определения архитектуры.
  — <https://huggingface.co/lvladikov/SeedVR2-1.4B>
- Для ComfyUI берите checkpoint из подкаталога comfyui/, а не корневой: у него есть conditioning tensors, которые требует загрузчик.
  — <https://huggingface.co/lvladikov/SeedVR2-1.4B>
- Начинайте с 4×; 8× снижает качество. Не увеличивайте VAE tile_size выше 512; при нехватке памяти уменьшите его до 256.
  — <https://huggingface.co/lvladikov/SeedVR2-1.4B/blob/main/comfyui/seedvr2_1.4b_upscale_image.json>
- Проверяйте результат на лёгких деградациях и малых разрешениях: официальный проект предупреждает о переусилении деталей, а также о слабой устойчивости к тяжёлым деградациям и большим движениям.
  — <https://github.com/ByteDance-Seed/SeedVR>

## Superseded by this

- Не подтверждено: SeedVR (CVPR 2025) не объявлен устаревшим; официальный репозиторий продолжает хранить SeedVR и SeedVR2 как отдельные модели.
- 2026-07-30: 1.4B-дистилляция не заменяет официальные 3B/7B по fidelity; она предназначена для ограничений памяти и задержки.

## Still unknown

- SeedVR2-1.4B — сторонняя дистилляция lvladikov, а не официальный checkpoint ByteDance Seed; её численные замеры и сравнения не являются независимой валидацией.
- В исторической ссылке на ByteDance-Seed/SeedVR-Models текущий URL перенаправляется на SeedVR2-3B, поэтому точное состояние исходного model-tree на 2025-06-11 не восстановлено из этой страницы.
- Официальная документация описывает multi-GPU запуск; практическая поддержка single-GPU, offload и ComfyUI развивается в отдельных community implementations и не подтверждена этой официальной инструкцией.

## Sources

| source | title | read |
|---|---|---|
| https://iceclear.github.io/projects/seedvr2/ | SeedVR2: One-Step Video Restoration via Diffusion Adversarial Post-Training | 2026-09-05 |
| https://arxiv.org/abs/2506.05301 | SeedVR2: One-Step Video Restoration via Diffusion Adversarial Post-Training | 2026-09-05 |
| https://github.com/ByteDance-Seed/SeedVR | ByteDance-Seed/SeedVR — Repo for SeedVR2 and SeedVR | 2026-09-05 |
| https://huggingface.co/ByteDance-Seed/SeedVR-Models/tree/main | ByteDance-Seed/SeedVR2-3B model tree | 2026-09-05 |
| https://huggingface.co/lvladikov/SeedVR2-1.4B | lvladikov/SeedVR2-1.4B | 2026-09-05 |
| https://huggingface.co/lvladikov/SeedVR2-1.4B/tree/main/comfyui | SeedVR2-1.4B ComfyUI files | 2026-09-05 |
| https://huggingface.co/lvladikov/SeedVR2-1.4B/blob/main/comfyui/seedvr2_1.4b_upscale_image.json | SeedVR2-1.4B ComfyUI upscale workflow | 2026-09-05 |
| https://www.reddit.com/r/StableDiffusion/comments/1va0dxy/seedvr214b_a_6layer_distillation_of_seedvr27b/ | SeedVR2-1.4B — a 6-layer distillation of SeedVR2-7B | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:seedvr2`, thread `seedvr2-development-and-distribution`, 3 dated events 2025-06-09 → 2026-07-30.
- **Practical note:** As of 2026-07-30, practitioners should treat SeedVR2 as a versioned deployment path: consult the official project and repository references first, then independently assess the linked 1.4B ComfyUI package before using it in a workflow.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
