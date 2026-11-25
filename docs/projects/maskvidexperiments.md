---
title: MaskVidExperiments
category: projects
date: 2026-08-23
tags: [maskvid-experiments, maskvidexperiments, project]
aliases: ["MaskVidExperiments"]
---

# MaskVidExperiments

**Development line:** `project:maskvidexperiments` · thread `maskvid-experiments`  
**Last event:** 2026-08-23 · 1 dated since 2026-08-23 · **Researched:** 2026-09-05 · confidence: medium

## What it is

MaskVidExperiments — набор узлов ComfyUI для тех, у кого уже есть покадровая маска объекта и нужно инпейнтить или стилизовать его в видео без дрожащего crop. — Subject Crop/Uncrop строит стабильный crop для всего клипа и вклеивает обработанный объект обратно с растушёвкой. — Mask Cleanup чистит краткие шумные области маски; Mask To Latent Space переводит видеомаску в геометрию VAE; есть отдельные узлы для аудиолатента и мягкого Differential Diffusion. Лимит: заявлены ComfyUI >=0.15.0 и GPLv3; это не сегментатор и не видеомодель. Вердикт: берите для локального масочного редактирования уже размеченного видео, а не как замену маскам, модели или проверенному production workflow.

## Development line

- **2026-08-23 — MaskVidExperiments GitHub repository was publicly referenced.** Датированная ссылка указывает на уже существовавший проект v0.2.0; в просмотренной истории main нет commit на эту дату.

## What changed

2026-07-28: initial commit помечен как Initial release. 2026-07-29: добавлен MVEx Differential Diffusion (Soft) для мягких краёв маски по шагам денойза. 2026-08-04: маски начали группироваться по точным границам VAE-латентов; добавлен узел, который переносит латентную маску обратно на пиксельные кадры. 2026-08-08: сопоставление с циклом VAE-чанков и GPU-редукция с CPU fallback сделали перевод маски ближе к геометрии видеомодели. 2026-08-10: добавлены Frame Range Mask и узлы Audio Mask To Latent/Debug. 2026-08-13: crop_scale=0 стал режимом full-frame passthrough для сравнения с crop-пайплайном. 2026-08-14: закреплён минимум ComfyUI 0.15.0 и добавлена автоматическая публикация в Registry при version bump. 2026-08-15: латентные маски выровнены по сетке токенов 2x2 MiniMax H3. 2026-08-17: метаданные проекта повышены с 0.1.0 до 0.2.0; отрицательное upscale_megapixels разрешило downscale. 2026-08-23: датированная ссылка указывает на уже существовавший проект v0.2.0; в просмотренной истории main нет commit на эту дату.

## How to use this

As of 2026-08-23, practitioners can use the linked MaskVidExperiments GitHub repository as a dated project source, while treating its contents and version state as unreviewed until separately verified.

1. Склонируйте репозиторий в ComfyUI/custom_nodes и перезапустите ComfyUI; документация заявляет минимум v0.15.0 и отсутствие отдельных зависимостей сверх ComfyUI.
  — <https://github.com/drozbay/MaskVidExperiments/blob/d98cc899c1fac718acf81cde1735bf57281097cf/README.md>
2. Подайте кадры и готовую маску в Mask Cleanup при кратком шуме, затем в Subject Crop; пропустите crop через свой sampler или inpaint workflow и верните его через Subject Uncrop вместе с исходными кадрами, bboxes и crop-масками.
  — <https://github.com/drozbay/MaskVidExperiments/blob/d98cc899c1fac718acf81cde1735bf57281097cf/README.md>
3. Для видеомаски подключите Mask To Latent Space к VAE, оставьте compression=auto, если VAE подключён, и передайте результат в Set Latent Noise Mask; manual используйте только когда геометрия VAE известна.
  — <https://github.com/drozbay/MaskVidExperiments/blob/d98cc899c1fac718acf81cde1735bf57281097cf/README.md>

## Best practices

- Для минимального движения crop выбирайте tracked; combined подходит для одного неподвижного окна, zoomed — когда важна постоянная доля объекта. Смотрите debug, а pixel-exact вставка сохраняется только без изменения размера crop.
  — <https://github.com/drozbay/MaskVidExperiments/blob/d98cc899c1fac718acf81cde1735bf57281097cf/README.md>
- Не подавайте пиксельную видеомаску напрямую в Set Latent Noise Mask: используйте Mask To Latent Space, чтобы не размывать маску trilinear-resize между кадрами.
  — <https://github.com/drozbay/MaskVidExperiments/blob/d98cc899c1fac718acf81cde1735bf57281097cf/README.md>
- Ставьте crop_scale=0, чтобы за два bypass сравнить crop-пайплайн с полным кадром до принятия решения по конкретному клипу.
  — <https://github.com/drozbay/MaskVidExperiments/blob/d98cc899c1fac718acf81cde1735bf57281097cf/README.md>

## Superseded by this

- 2026-08-17: метаданные проекта 0.1.0 сменены на 0.2.0 (commit d98cc89).

## Still unknown

- Отдельный поиск по Simplified Chinese не дал доступного первичного или implementation-источника; китайская доказательная линия остаётся непокрытой.
- У upstream нет опубликованного benchmark по VRAM, скорости, длинным клипам или качеству временной стабильности; граф не запускался в собственной среде.
- Подтверждены минимум ComfyUI 0.15.0 и поддержка геометрии названных VAE в документации, но нет полной матрицы протестированных версий ComfyUI, видеомоделей и железа.
- Перед production-применением нужен закреплённый commit и отдельная проверка лицензионной совместимости GPLv3.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/drozbay/MaskVidExperiments | MaskVidExperiments — GitHub repository | 2026-09-06 |
| https://github.com/drozbay/MaskVidExperiments/blob/d98cc899c1fac718acf81cde1735bf57281097cf/README.md | MaskVidExperiments README at commit d98cc89 | 2026-09-06 |
| https://github.com/drozbay/MaskVidExperiments/commits/main | MaskVidExperiments main commit history | 2026-09-06 |
| https://github.com/drozbay/MaskVidExperiments/commit/d98cc899c1fac718acf81cde1735bf57281097cf | Bump version to 0.2.0 — commit d98cc89 | 2026-09-06 |
| https://github.com/drozbay/MaskVidExperiments/blob/d98cc899c1fac718acf81cde1735bf57281097cf/pyproject.toml | Project metadata at commit d98cc89 | 2026-09-06 |

## Agent brief {#agent-brief}

- **Subject:** `project:maskvidexperiments`, thread `maskvid-experiments`, 1 dated events 2026-08-23 → 2026-08-23.
- **Practical note:** As of 2026-08-23, practitioners can use the linked MaskVidExperiments GitHub repository as a dated project source, while treating its contents and version state as unreviewed until separately verified.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
