---
title: PrunaVAED — LTX Video
category: projects
date: 2026-08-03
tags: [ltx-video, ltx_video, project, prunavaed]
aliases: ["PrunaVAED"]
---

# PrunaVAED — LTX Video

**Development line:** `project:prunavaed` · thread `ltx-video`  
**Last event:** 2026-08-03 · 1 dated since 2026-08-03 · **Researched:** 2026-09-05 · confidence: high

## What it is

PrunaVAED — прuned decoder video VAE для LTX-2.3, заменяющий только декодирование существующих LTX-2.3 латентов. — сохраняет encoder и latent format LTX-2.3; — работает с distilled и two-stage LTX-2.3 pipelines; — не является T2V-моделью, денойзером или универсальным VAE. На H100 80 GB при bf16 и batch size 1 авторы заявляют 1.67–2.08× ускорение; на другом железе результат нужно замерять. Практический вердикт: это узкая оптимизация LTX-2.3 decode stage, а не способ ускорить всю генерацию.

## Development line

- **2026-08-03 — PrunaVAED entered the LTX Video integration thread.** Drop-in decoder для `diffusers/LTX-2.3-Diffusers`, а не новый генератор видео.

## What changed

2026-07-28 — поддержка PrunaVAED была влита в ComfyUI: нужен конвертированный `pruna_ltx2.3_vae_comfy_bf16.safetensors`, а PR описывает около 2× ускорение LTX-2.3 decoding. 2026-08-03 — PrunaVAED был зафиксирован как LTX-video development step; первичные материалы уточняют его область: drop-in decoder для `diffusers/LTX-2.3-Diffusers`, а не новый генератор видео.

Дополнение к событию 2026-08-03: ComfyUI PR датирован 2026-07-28 и уже был merged; поэтому это не новая интеграция августа, а более ранний факт, поясняющий состояние интеграции на дату события.

## How to use this

As of 2026-08-03, practitioners should evaluate PrunaVAED from the linked Hugging Face resource and check the linked ComfyUI pull request for integration status before relying on it in an LTX Video workflow.

1. Скачайте репозиторий весов, установите зависимости demo и запустите `demo/demo_distilled_decode.py`; он создаёт ролики stock LTX-2.3 VAE и PrunaVAED из одного latent и печатает decode time.
  — <https://huggingface.co/PrunaAI/PrunaVAED>
2. Для LTX-2 скачайте веса PrunaVAED и Gemma encoder, затем запустите distilled pipeline либо `ti2vid_two_stages_hq`; для image-to-video добавьте `--image path/to/image.jpg 0 0.8`.
  — <https://huggingface.co/PrunaAI/PrunaVAED>
3. В ComfyUI используйте поддержку из merged PR и конвертированный bf16-файл, указанный автором PR; заменяйте video VAE, не audio VAE и не transformer.
  — <https://github.com/Comfy-Org/ComfyUI/pull/15129>

## Best practices

- Сначала сравните оба декодера на одинаковом latent и своей целевой длине и разрешении: опубликованные цифры получены на одном H100 80 GB, bf16, batch size 1.
  — <https://huggingface.co/PrunaAI/PrunaVAED>
- Не применяйте модель к произвольным VAE latents и не рассчитывайте на bit-exact output; она проверялась только на двух LTX-2.3 pipelines.
  — <https://huggingface.co/PrunaAI/PrunaVAED>
- Перед коммерческим использованием или распространением проверьте ограничения LTX-2 Community License Agreement.
  — <https://huggingface.co/PrunaAI/PrunaVAED>

## Superseded by this

- 2026-07-28 — для ComfyUI устарело предположение, что PrunaVAED требует только внешнего custom-node решения: поддержка была merged в ComfyUI PR #15129.
- 2026-08-03 — устарело описание PrunaVAED как полноценной video-generation модели: текущая модельная карточка прямо ограничивает её роль decoder для LTX-2.3.

## Still unknown

- Модельная карточка не указывает дату первоначальной публикации репозитория, поэтому дату открытия весов нельзя надёжно сопоставить с событием 2026-08-03.
- Нет независимого benchmark на consumer GPU; заявленные скорость и VRAM подтверждены только авторским тестом на H100 80 GB.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/PrunaAI/PrunaVAED | PrunaAI/PrunaVAED model card | 2026-09-05 |
| https://github.com/Comfy-Org/ComfyUI/pull/15129 | Support PrunaVAED (faster LTX2.3 decoder) — ComfyUI pull request #15129 | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:prunavaed`, thread `ltx-video`, 1 dated events 2026-08-03 → 2026-08-03.
- **Practical note:** As of 2026-08-03, practitioners should evaluate PrunaVAED from the linked Hugging Face resource and check the linked ComfyUI pull request for integration status before relying on it in an LTX Video workflow.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
