---
title: Hyper-SD
category: projects
date: 2024-08-28
tags: [hyper-sd, hyper_sd, project]
aliases: ["Hyper-SD"]
---

# Hyper-SD

**Development line:** `project:hyper-sd` · thread `hyper-sd`  
**Last event:** 2024-08-28 · 2 dated since 2024-04-22 · **Researched:** 2026-09-04 · confidence: medium

## What it is

Hyper-SD — дистиллированные LoRA и один SDXL UNet для генерации за меньшее число шагов вместо обычного многосшагового сэмплинга. — N-step LoRA для SDXL, SD1.5, SD3 и FLUX.1-dev. — Unified LoRA на 1–8 шагов для SDXL и SD1.5. — Примеры ControlNet и готовые ComfyUI workflow для SDXL/SD1.5. Лимит: это не универсальная базовая модель; FLUX.1-dev и SD3 требуют доступа к закрытым базовым весам. Вывод: использовать стоит только с точно названной поддерживаемой базой, не перенося настройки на новые семейства моделей без проверки.

## Development line

- **2024-04-22 — Hyper-SD launched public models and interactive demos.** On 2024-04-22, Hyper-SD launched a public project site and model repository, alongside interactive demonstrations for one-step XL text-to-image and scribble-guided workflows. This was a public availability milestone for the project. The linked resources alone do not establish training details, benchmark results, or exact release versions.
- **2024-08-28 — Hyper-SD added FLUX.1-dev LoRA checkpoint variants.** On 2024-08-28, Hyper-SD added two LoRA checkpoint variants for FLUX.1-dev, corresponding to 8-step and 16-step generation. This extended the project's public artifact line to a FLUX.1-dev workflow. The dated links do not establish the checkpoints' quality, licensing, or whether they replaced earlier Hyper-SD artifacts.

## What changed

Hyper-SD — линия развития от ускорения SDXL/SD1.5 к четырём конкретным семействам базовых моделей. — 2024-04-22: появились практические точки входа — репозиторий весов, Hyper-SDXL one-step text-to-image и Hyper-SD15 Scribble. — 2024-04-30 и 2024-05-13 [найдено сегодня]: добавлены CFG-preserved LoRA на 8 и 12 шагов для SDXL и SD1.5, рассчитанные на CFG 5–8. — 2024-08-19 [найдено сегодня]: добавлены CFG LoRA для SD3 на 4, 8 и 16 шагов. — 2024-08-28: добавлены Hyper-FLUX.1-dev LoRA на 8 и 16 шагов; официальная карточка датирует их доступность 2024-08-26. — 2024-11-04 [найдено сегодня]: статья обновлена до v3 и принята на NeurIPS 2024; новый checkpoint в этой записи не заявлен. — 2026-09-04 [найдено сегодня]: текущая официальная карточка всё ещё документирует FLUX.1-dev, SD3-Medium, SDXL Base 1.0 и SD v1.5, но не заявляет поддержку более новых семейств. Мера: каждый из проверенных FLUX LoRA на 8 и 16 шагов занимает 1,39 GB. Вывод: актуальная практическая область — ускорение этих зафиксированных баз, а не общий адаптер для новых diffusion-моделей.

## How to use this

From 2024-04-22, practitioners could evaluate Hyper-SD through its public model and demo resources. From 2024-08-28, practitioners working with FLUX.1-dev should select and test the 8-step or 16-step Hyper-SD LoRA variant rather than assuming the earlier Hyper-SD assets apply unchanged.

1. Hyper-SD: выберите ровно одну поддерживаемую базу и LoRA того же семейства с нужным числом шагов; не используйте один файл как универсальный для SDXL, SD1.5, SD3 и FLUX.
  — <https://huggingface.co/ByteDance/Hyper-SD>
2. Hyper-SD: для FLUX.1-dev или SD3 сначала получите доступ к базовой модели, затем загрузите LoRA через совместимый Diffusers pipeline, fuse-ните её и перенесите pipeline на CUDA.
  — <https://huggingface.co/ByteDance/Hyper-SD>
3. Hyper-SD: начните с официальных настроек семейства — для FLUX.1-dev используйте LoRA scale около 0.125, 8 или 16 шагов и guidance 3.5; для SD3 используйте scale 0.125 и guidance 3/5/7 на 4/8/16 шагах.
  — <https://huggingface.co/ByteDance/Hyper-SD>
4. Hyper-SD: для SDXL/SD1.5 N-step LoRA задайте DDIM с timestep spacing trailing; для unified LoRA используйте TCDScheduler и подберите число шагов с eta.
  — <https://huggingface.co/ByteDance/Hyper-SD>
5. Hyper-SD: в ComfyUI импортируйте workflow, соответствующий семейству весов; для one-step SDXL UNet установите приложенный custom scheduler в custom_nodes.
  — <https://huggingface.co/ByteDance/Hyper-SD/tree/main/comfyui>

## Best practices

- Hyper-SD: сначала воспроизведите официальный baseline на одном prompt и целевом числе шагов, а уже затем меняйте LoRA scale, CFG или eta.
  — <https://huggingface.co/ByteDance/Hyper-SD>
- Hyper-SD: не смешивайте scheduler-подходы — N-step варианты используют DDIM trailing, unified варианты используют TCDScheduler.
  — <https://huggingface.co/ByteDance/Hyper-SD>
- Hyper-SD: при работе с ControlNet сохраняйте тот же базовый model family и sampler-рецепт, что в официальном примере, вместо переноса настроек между SDXL и SD1.5.
  — <https://huggingface.co/ByteDance/Hyper-SD>
- Hyper-SD: для ComfyUI берите опубликованный workflow как стартовую конфигурацию; one-step SDXL UNet без требуемого scheduler custom node не воспроизводит заявленный режим timestep 800.
  — <https://huggingface.co/ByteDance/Hyper-SD/tree/main/comfyui>

## Superseded by this

- 2024-04-22 — представление Hyper-SD только как ускорителя SDXL/SD1.5 стало неполным после официальных LoRA для SD3 от 2024-08-19 и FLUX.1-dev от 2024-08-26.
- 2024-04-22 — перенос настроек one-step demo на все базы больше не годится: поздние официальные инструкции разделяют FLUX, SD3, SDXL и SD1.5 по LoRA, scheduler, CFG и числу шагов. Ни один ранний checkpoint официально не помечен deprecated.

## Still unknown

- Официальная поддержка Flux.1 Kontext, Flux.2, SD3.5, SDXL-derived checkpoints и текущих версий ComfyUI/Diffusers не подтверждена.
- Текущая карточка заканчивает список анонсов checkpoint на 2024-08-26; это не доказывает прекращение проекта, но более новый roadmap не найден.
- Пространства Hugging Face существуют, но их успешная генерация под текущей нагрузкой не проверялась.

## Sources

| source | title | read |
|---|---|---|
| https://hyper-sd.github.io/ | Hyper-SD: Trajectory Segmented Consistency Model for Efficient Image Synthesis | 2026-09-04 |
| https://huggingface.co/ByteDance/Hyper-SD | ByteDance/Hyper-SD | 2026-09-04 |
| https://huggingface.co/spaces/ByteDance/Hyper-SDXL-1Step-T2I | Hyper SDXL 1Step T2I | 2026-09-04 |
| https://huggingface.co/spaces/ByteDance/Hyper-SD15-Scribble | Hyper SD15 Scribble | 2026-09-04 |
| https://huggingface.co/ByteDance/Hyper-SD/blob/main/Hyper-FLUX.1-dev-8steps-lora.safetensors | Hyper-FLUX.1-dev-8steps-lora.safetensors | 2026-09-04 |
| https://huggingface.co/ByteDance/Hyper-SD/blob/main/Hyper-FLUX.1-dev-16steps-lora.safetensors | Hyper-FLUX.1-dev-16steps-lora.safetensors | 2026-09-04 |
| https://huggingface.co/ByteDance/Hyper-SD/tree/main/comfyui | ByteDance/Hyper-SD ComfyUI workflows | 2026-09-04 |
| https://arxiv.org/abs/2404.13686 | Hyper-SD: Trajectory Segmented Consistency Model for Efficient Image Synthesis | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:hyper-sd`, thread `hyper-sd`, 2 dated events 2024-04-22 → 2024-08-28.
- **Practical note:** From 2024-04-22, practitioners could evaluate Hyper-SD through its public model and demo resources. From 2024-08-28, practitioners working with FLUX.1-dev should select and test the 8-step or 16-step Hyper-SD LoRA variant rather than assuming the earlier Hyper-SD assets apply unchanged.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
