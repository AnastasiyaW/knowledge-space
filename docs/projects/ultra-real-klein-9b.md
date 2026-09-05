---
title: Ultra Real - Klein 9b — Klein 9b
category: projects
date: 2026-03-23
tags: [klein-9b, project, ultra-real-klein-9b]
aliases: ["Ultra Real - Klein 9b"]
---

# Ultra Real - Klein 9b — Klein 9b

**Development line:** `project:ultra-real-klein-9b` · thread `klein-9b`  
**Last event:** 2026-03-23 · 1 dated since 2026-03-23 · **Researched:** 2026-09-05 · confidence: medium

## What it is

Ultra Real - Klein 9b — LoRA для пользователей FLUX.2 Klein 9B в ComfyUI: генерация портретов, image-edit и апскейл старых изображений. Версии: V1–V4; V3 делает более деликатную текстуру, V4 предназначена для детализации. Ограничение: это не базовая модель и требует совместимого Klein 9B workflow. Вердикт: для натуральной кожи стоит начинать с V3, а V4 подключать только для detail-pass.

## Development line

- **2026-03-23 — Ultra Real - Klein 9b linked to a Civitai model page and ComfyUI workflows.** V2 заявлена как более естественная текстура кожи с лучшим сохранением тона и освещения.

## What changed

2026-03-23 — Ultra Real - Klein 9b был доступен как LoRA-линейка V1/V2 для FLUX.2 Klein 9B: V2 заявлена как более естественная текстура кожи с лучшим сохранением тона и освещения. 2026-04-10 — запись модели обновлена и показывает линейку V1–V4; V3 описана как более деликатная текстура без лишних веснушек, V4 — как отдельный режим детализации. 2026-04-13 — текущая карточка указывает FLUX.2 Klein 9B как базовую модель и V1–V4 как варианты одной LoRA-линейки.

## How to use this

From 2026-03-23, practitioners should use the linked Civitai model page and ComfyUI workflows repository as the dated reference points for evaluating Ultra Real - Klein 9b; the links alone do not verify a specific version, workflow compatibility, or performance claim.

1. Установите совместимые компоненты FLUX.2 Klein 9B: diffusion model, Qwen 3 8B text encoder и flux2 VAE в соответствующие каталоги ComfyUI.
  — <https://github.com/Comfy-Org/docs/blob/main/ja/tutorials/flux/flux-2-klein.mdx>
2. Загрузите Ultra Real - Klein 9b в LoRA-слот Klein 9B workflow; для V3 при image-edit начните с веса 0.6, для V4 — с 0.55.
  — <https://www.seaart.ai/indo/models/detail/0b4b3278ab4fd5b6471cd029ef88fc09>
3. Для редактирования используйте instruction, сохраняющую лицо, выражение, фигуру, позу и композицию; для V2 опубликован ориентир веса 0.5.
  — <https://tensor.art/models/981017447823890853>
4. Для text-to-image начните с веса 0.7–0.8 и описывайте кадр как фотографию; опубликованный V2 ориентир — 0.7.
  — <https://www.seaart.ai/indo/models/detail/0b4b3278ab4fd5b6471cd029ef88fc09>

## Best practices

- Не использовать V4 как универсальный style LoRA: в описании она предназначена для детализации; для обычной генерации применяйте текстовый prompt или другую LoRA.
  — <https://www.seaart.ai/indo/models/detail/0b4b3278ab4fd5b6471cd029ef88fc09>
- Не переносить настройки V1 без проверки: V1 может усиливать поры и веснушки и менять свет или тон кожи; V3 заявлена как более деликатный вариант.
  — <https://www.seaart.ai/indo/models/detail/0b4b3278ab4fd5b6471cd029ef88fc09>
- Для image-edit явно просите сохранить черты, выражение, позу и композицию, иначе LoRA может менять больше, чем только фактуру кожи.
  — <https://tensor.art/models/981017447823890853>

## Superseded by this

- 2026-04-10 — V1 не является предпочтительным режимом для естественной кожи: текущая карточка описывает V3 как более деликатную текстуру, а V4 как специализированный detail-pass.
- 2026-04-10 — совет применять одну и ту же LoRA для генерации и детализации устарел: V4 отдельно ограничена задачей детализации.

## Still unknown

- Прямая страница Civitai и репозиторий workflow были недоступны для содержательной загрузки при проверке; настройки подтверждены зеркалами и страницами публикации, а не исходными файлами workflow.
- Текущая карточка SeaArt показывает даты объявления 2026-03-13, обновления 2026-04-10 и публикации 2026-04-13, но не даёт отдельных дат релиза V3 и V4; поэтому их нельзя датировать точнее.
- Идентификатор Civitai 2462105 позднее отображается на некоторых зеркалах также для UltraReal - Krea2, Klein9b; не доказано, что это продолжение той же Klein 9B LoRA, а не переиспользование карточки.

## Sources

| source | title | read |
|---|---|---|
| https://civitai.com/models/2462105/ultra-real-klein-9b | Ultra Real - Klein 9b — Civitai model page | 2026-09-05 |
| https://github.com/vizsumit/comfyui-workflows | vizsumit/comfyui-workflows | 2026-09-05 |
| https://civarchive.com/seaart/models/0b4b3278ab4fd5b6471cd029ef88fc09/versions/4eaaed353d71f3ae09efa4411c954877 | Ultra Real - Klein 9b V2 — CivArchive | 2026-09-05 |
| https://www.seaart.ai/indo/models/detail/0b4b3278ab4fd5b6471cd029ef88fc09 | Ultra Real - Klein 9b — SeaArt model page | 2026-09-05 |
| https://tensor.art/models/981017447823890853 | Ultra Real - Klein 9b V1 — Tensor.Art | 2026-09-05 |
| https://github.com/Comfy-Org/docs/blob/main/ja/tutorials/flux/flux-2-klein.mdx | FLUX.2 Klein ComfyUI tutorial | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:ultra-real-klein-9b`, thread `klein-9b`, 1 dated events 2026-03-23 → 2026-03-23.
- **Practical note:** From 2026-03-23, practitioners should use the linked Civitai model page and ComfyUI workflows repository as the dated reference points for evaluating Ultra Real - Klein 9b; the links alone do not verify a specific version, workflow compatibility, or performance claim.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
