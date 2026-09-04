---
title: FLUX.2 — FLUX.2 development
category: models
tags: [flux, flux-2, flux-2-development, project]
aliases: ["1.58-bit FLUX", "FLUX", "FLUX.1", "FLUX.2", "FLUX.2 [dev] Turbo"]
---

# FLUX.2 — FLUX.2 development

**Development line:** `project:flux-2` · thread `flux-2-development`  
**Events:** 5 dated, 2024-11-07 → 2025-12-30 · **Researched:** 2026-09-04 · confidence: medium

## What it is

FLUX.2 — семейство BFL для API-команд, локальных разработчиков и ComfyUI-пайплайнов, где один базовый контур должен и генерировать, и редактировать изображение. — text-to-image, редактирование по тексту и композиции с несколькими референсами; — [max]/[pro]/[flex] для API, [dev] и [klein] для локального запуска; — типографика, структурированные промпты и контроль цвета для производственных макетов. Лимит: [pro] делит 9 МП между входами и выходом; локальные веса [dev] и [klein] 9B имеют некоммерческое ограничение, тогда как [klein] 4B — Apache 2.0. Вердикт: выбирайте FLUX.2, когда нужны референсы и редактирование в одном процессе; не подменяйте им автоматически отдельные FLUX.1.1 API-возможности.

## Development line

- **2024-11-07 — FLUX 1.1 Ultra was publicly documented.** On 2024-11-07, this development line linked the Black Forest Labs page for FLUX 1.1 Ultra and the corresponding fal.ai model route. Together, the dated links mark a public FLUX 1.1 Ultra documentation and availability milestone in the lineage preceding FLUX.2.
- **2024-12-30 — A FLUX research-paper record entered the development line.** On 2024-12-30, the line linked Hugging Face paper record 2412.18653. This preserves a dated research reference in the FLUX lineage; the supplied evidence does not establish the paper's precise contribution to a particular release.
- **2025-11-25 — A FLUX.2 development model repository was linked.** On 2025-11-25, a Comfy-Org repository named flux2-dev was linked from Hugging Face. This marks a public distribution or integration point for a FLUX.2 development model, without asserting capabilities not shown in the sealed evidence.
- **2025-11-27 — FLUX.2 prompting guidance was documented.** On 2025-11-27, the line linked Black Forest Labs' FLUX.2 prompting guide alongside a The source reference. This makes prompting guidance a dated part of the FLUX.2 public development record; the linked source text was not supplied.
- **2025-12-30 — FLUX.2-dev-Turbo was linked with a hosted demo.** On 2025-12-30, the line linked the Hugging Face model page for FLUX.2-dev-Turbo and a hosted demo space. This marks a Turbo-labelled FLUX.2 development variant and a public demonstration route in the chronology, without inferring performance characteristics.

## What changed

FLUX.2 — линия отделяет наследие FLUX.1, собственно FLUX.2 и сторонние адаптеры. 2024-11-07 — FLUX1.1 [pro] Ultra добавил до 4 МП и RAW-режим; это отдельная ветка FLUX.1, не релиз FLUX.2. 2024-12-30 — 1.58-bit FLUX показал 1,58-битную квантизацию FLUX.1-dev; это исследовательский метод для FLUX.1, не формат весов FLUX.2. 2025-11-25 — найдено сегодня: BFL выпустила FLUX.2 [pro] и [flex], добавив единый контур генерации/редактирования, до 4 МП, несколько референсов, структурированные промпты и улучшенную типографику. 2025-11-25 — Comfy-Org упаковал квантизированные компоненты FLUX.2-dev для ComfyUI; это дистрибутив под ComfyUI, а не отдельный базовый релиз BFL. 2025-11-27 — руководство BFL закрепило для [pro]/[max] работу без negative prompts, структурные JSON-промпты и multi-reference editing. 2025-12-30 — fal/FLUX.2-dev-Turbo добавил сторонний LoRA-адаптер для FLUX.2-dev: заявлены 8 шагов вместо типичных 50 и поддержка text-to-image/editing. 2026-01-15 — найдено сегодня: BFL выпустила [klein] 4B/9B и Base-варианты для локальных интерактивных запусков; 4B Apache 2.0, 9B FLUX NCL. 2026-02-17 — найдено сегодня: API/webhook-успех сменил статус с SUCCESS на Ready. 2026-03-03 — найдено сегодня: улучшения [pro] идут через flux-2-pro-preview, а flux-2-pro остаётся фиксированным снимком для воспроизводимости. 2026-04-23 — найдено сегодня: началась публичная beta managed LoRA inference для [klein] через -finetuned endpoints. 2026-07-31 — подтверждённого изменения не зафиксировано: связанная публикация недоступна для чтения.

## How to use this

By 2025-12-30, practitioners should consult the linked FLUX.2 model repositories, prompting guide, and Turbo demo before selecting a FLUX workflow, rather than treating the original FLUX release as the only documented path.

1. Выберите вариант по задаче: [max] для максимального качества и grounding search, [pro] для коммерческого потока, [flex] для текста в кадре, [klein] для скорости, [dev] для некоммерческой разработки и кастомизации; перед локальным запуском проверьте лицензию конкретных весов.
  — <https://help.bfl.ai/articles/6122710168-which-flux-2-model-should-i-choose>
2. Для BFL API отправьте запрос в выбранный endpoint, сохраните возвращённый polling_url и забирайте результат по нему; успех — Ready, Error и Failed — терминальные ошибки.
  — <https://docs.bfl.ai/quick_start/generating_images>
3. Для нового качества начните с preview endpoint; для повторяемого продакшена выберите непредпросмотровый фиксированный endpoint и не смешивайте их в одной серии.
  — <https://docs.bfl.ai/quick_start/generating_images>
4. Для локального FLUX.2-dev примите условия доступа к официальному репозиторию, загрузите модель через Diffusers в bfloat16/CUDA и передайте image вместе с prompt, если нужна правка исходника.
  — <https://huggingface.co/black-forest-labs/FLUX.2-dev/tree/main>
5. Для локального ComfyUI-старта с [klein] 4B обновите ComfyUI, выберите готовый text-to-image или image-editing workflow и разложите text encoder, diffusion model и VAE по указанным каталогам models.
  — <https://docs.comfy.org/zh/tutorials/flux/flux-2-klein>
6. Если узкое место — задержка FLUX.2-dev, подключите сторонний fal Turbo LoRA к базовой модели только с его 8-шаговыми sigmas; в опубликованном примере используются 8 шагов и guidance_scale 2.5.
  — <https://huggingface.co/fal/FLUX.2-dev-Turbo>

## Best practices

- Для [pro]/[max] стройте промпт как Subject + Action + Style + Context; критичное ставьте первым, а для большинства задач держитесь 30–80 слов.
  — <https://docs.bfl.ai/guides/prompting_guide_flux2>
- Не используйте negative prompts: опишите желаемое состояние, например sharp focus throughout вместо no blur.
  — <https://docs.bfl.ai/guides/prompting_guide_flux2>
- Для сложной автоматизации используйте JSON-промпт, но начинайте с простой структуры; HEX-код привязывайте к конкретному объекту, а не к изображению целиком.
  — <https://docs.bfl.ai/guides/prompting_guide_flux2>
- В multi-reference editing явно назначайте роль каждому входному изображению; для [pro] соблюдайте общий лимит 9 МП, поэтому при 1 МП выхода — не более восьми референсов.
  — <https://docs.bfl.ai/guides/prompting_guide_flux2>
- Не меняйте endpoint незаметно: preview берите для последних улучшений, фиксированный endpoint — когда результат должен воспроизводиться.
  — <https://docs.bfl.ai/quick_start/generating_images>
- Для обучения и LoRA берите undistilled Klein Base, для интерактивной генерации — distilled Klein; отдельно проверьте, что 4B Apache 2.0, а 9B остаётся FLUX NCL.
  — <https://bfl.ai/blog/flux2-klein-towards-interactive-visual-intelligence>

## Superseded by this

- 2026-02-17: обработка webhook-успеха через status=SUCCESS устарела; проверяйте status=Ready.
- 2026-03-03: ожидание, что flux-2-pro автоматически получает последние улучшения, устарело; для них нужен flux-2-pro-preview, а фиксированный flux-2-pro сохраняют ради воспроизводимости.
- 2026-04-23: FLUX.1-era Finetuning API уже был deprecated в октябре 2025; для self-serve LoRA BFL направляет к FLUX.2 [klein] -finetuned endpoints с finetune_id и finetune_strength.
- 2024-12-30: 1.58-bit FLUX нельзя использовать как инструкцию по установке FLUX.2 — работа квантизирует FLUX.1-dev.

## Still unknown

- Содержимое публикации от 2026-07-31 не удалось прочитать ни через предоставленное зеркало, ни через canonical X URL; изменение не заявлено.
- События 2024-11-07 и 2024-12-30 относятся к FLUX.1.1/FLUX.1-dev, а не к FLUX.2: это родственная, но не единая линия релизов.
- Качество и совместимость FLUX.2 [dev] Turbo подтверждены только карточкой fal; независимый воспроизводимый бенчмарк не проверялся.
- Китайская официальная документация ComfyUI найдена, но самостоятельный запуск на конкретном железе в этот раз не проводился.

## Sources

| source | title | read |
|---|---|---|
| https://blackforestlabs.ai/flux-1-1-ultra/ | Introducing FLUX1.1 [pro] Ultra and Raw Modes | Black Forest Labs | 2026-09-04 |
| https://huggingface.co/papers/2412.18653 | 1.58-bit FLUX | Hugging Face Papers | 2026-09-04 |
| https://huggingface.co/Comfy-Org/flux2-dev | Comfy-Org/flux2-dev | Hugging Face | 2026-09-04 |
| https://bfl.ai/blog/flux-2 | FLUX.2: Frontier Visual Intelligence | Black Forest Labs | 2026-09-04 |
| https://docs.bfl.ai/guides/prompting_guide_flux2 | Prompting Guide - FLUX.2 [pro] & [max] | Black Forest Labs | 2026-09-04 |
| https://huggingface.co/fal/FLUX.2-dev-Turbo | FLUX.2 [dev] Turbo LoRA | fal | 2026-09-04 |
| https://bfl.ai/blog/flux2-klein-towards-interactive-visual-intelligence | FLUX.2 [klein]: Towards Interactive Visual Intelligence | Black Forest Labs | 2026-09-04 |
| https://docs.bfl.ai/release-notes | Release Notes | Black Forest Labs | 2026-09-04 |
| https://docs.bfl.ai/quick_start/generating_images | Image Generation with Text Prompts | Black Forest Labs | 2026-09-04 |
| https://help.bfl.ai/articles/6122710168-which-flux-2-model-should-i-choose | Which FLUX.2 model should I choose? | Black Forest Labs Knowledge Base | 2026-09-04 |
| https://huggingface.co/black-forest-labs/FLUX.2-dev/tree/main | black-forest-labs/FLUX.2-dev at main | Hugging Face | 2026-09-04 |
| https://docs.comfy.org/zh/tutorials/flux/flux-2-klein | ComfyUI Flux.2 Klein 4B 指南 | ComfyUI | 2026-09-04 |
| https://bfl.ai/models/flux-2 | FLUX.2 - Next Generation Image Generation | Black Forest Labs | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:flux-2`, thread `flux-2-development`, 5 dated events 2024-11-07 → 2025-12-30.
- **Practical note:** By 2025-12-30, practitioners should consult the linked FLUX.2 model repositories, prompting guide, and Turbo demo before selecting a FLUX workflow, rather than treating the original FLUX release as the only documented path.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
