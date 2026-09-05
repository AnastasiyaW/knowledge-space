---
title: SAMA
category: projects
date: 2026-03-20
tags: [project, sama]
aliases: ["SAMA"]
---

# SAMA

**Development line:** `project:sama` · thread `sama`  
**Last event:** 2026-03-20 · 1 dated since 2026-03-20 · **Researched:** 2026-09-05 · confidence: high

## What it is

SAMA: открытая модель instruction-guided video editing для пользователей Wan, которые меняют объекты, стиль или текст в ролике, сохраняя движение. — semantic anchoring планирует правку на опорных кадрах; — motion alignment удерживает временную динамику; — доступны SAMA-14B и официальный ComfyUI workflow. Лимит: Linux, NVIDIA GPU, Python 3.10, CUDA 12.1-совместимая среда и Wan2.1-T2V-14B. Вердикт: это локальный inference stack поверх Wan, не hosted-сервис.

## Development line

- **2026-03-20 — SAMA public project, source, and model resources were linked.** On 2026-03-20, a dated SAMA message linked the project's public website, source repository, and the Hugging Face page for SAMA-14B. These links establish that the three public resources were associated with SAMA on that date, without establishing further claims about the model or project.

## What changed

2026-03-20 — опубликована статья SAMA; препринт был подан 2026-03-19 и содержит 24 страницы, 12 фигур. 2026-03-21 — выпущен checkpoint SAMA-14B; SAMA-5B всё ещё отмечен как Coming soon. 2026-03-24 — открыт официальный SAMA-ComfyUI workflow. 2026-06-20 — SAMA принят на ECCV 2026. 2026-06-26 — опубликован metadata-набор SAMA-edit-filtered-1M.

## How to use this

As of 2026-03-20, practitioners can use the linked SAMA website, source repository, and SAMA-14B model page as the primary starting points for evaluation, while verifying capabilities, licensing, and usage requirements from those resources before adoption.

1. Клонируйте репозиторий, создайте окружение Python 3.10 и установите зависимости.
  — <https://github.com/Cynthiazxy123/SAMA>
2. Скачайте SAMA-14B и подготовьте полную локальную директорию Wan2.1-T2V-14B.
  — <https://huggingface.co/syxbb/SAMA-14B>
3. Задайте MODEL_ROOT, STATE_DICT, SRC_VIDEO, PROMPT и OUTPUT_DIR в infer_sh/run_sama.sh, затем запустите скрипт.
  — <https://github.com/Cynthiazxy123/SAMA>
4. Для node-based workflow используйте официальный ComfyUI integration с Wan base model и SAMA-14B.
  — <https://github.com/Cynthiazxy123/SAMA>

## Best practices

- Проверьте, что базовая директория Wan2.1-T2V-14B полна: скрипт намеренно останавливается при отсутствующих файлах.
  — <https://github.com/Cynthiazxy123/SAMA>
- Используйте исходный FPS; при его отсутствии явно задайте --fps.
  — <https://github.com/Cynthiazxy123/SAMA>
- Учитывайте автоматический padding входных кадров к требованию Wan 4k+1.
  — <https://github.com/Cynthiazxy123/SAMA>

## Superseded by this

- 2026-03-20 — состояние «только статья»: с 2026-03-21 доступен SAMA-14B, а с 2026-03-24 есть официальный ComfyUI workflow.

## Still unknown

- Официальные материалы не дают измеренного VRAM, скорости inference или поддерживаемых разрешений; для планирования железа нужна отдельная проверка конфигурации и workflow.

## Sources

| source | title | read |
|---|---|---|
| https://cynthiazxy123.github.io/SAMA/ | SAMA: Factorized Semantic Anchoring and Motion Alignment for Instruction-Guided Video Editing | 2026-09-05 |
| https://github.com/Cynthiazxy123/SAMA | Cynthiazxy123/SAMA — official inference code | 2026-09-05 |
| https://huggingface.co/syxbb/SAMA-14B | syxbb/SAMA-14B | 2026-09-05 |
| https://arxiv.org/abs/2603.19228 | SAMA: Factorized Semantic Anchoring and Motion Alignment for Instruction-Guided Video Editing | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:sama`, thread `sama`, 1 dated events 2026-03-20 → 2026-03-20.
- **Practical note:** As of 2026-03-20, practitioners can use the linked SAMA website, source repository, and SAMA-14B model page as the primary starting points for evaluation, while verifying capabilities, licensing, and usage requirements from those resources before adoption.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
