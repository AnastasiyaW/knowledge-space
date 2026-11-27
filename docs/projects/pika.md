---
title: Pika
category: projects
date: 2025-02-07
tags: [pika, pika-product-development, pika_camera_control, pikadditions, project]
aliases: ["Pika", "Pika AI Selves"]
---

# Pika

**Development line:** `project:pika` · thread `pika-product-development`  
**Last event:** 2025-02-07 · 2 dated since 2023-09-12 · **Researched:** 2026-09-04 · confidence: medium

## What it is

Pika: облачная платформа для авторов коротких роликов, конкурирующая с Runway в text-to-video, image-to-video и video-to-video. Возможности: Pika 2.5, Pikaframes, Pikascenes, Pikadditions, Pikaswaps, Pikatwists и Pikaffects. Лимит в текущей тарифной сетке: основные ролики — 5 или 10 секунд, Pikaframes — до 25 секунд. Вердикт: подходит для быстрых генераций и эффектных преобразований, но не заменяет покадровый композитинг или длинный монтаж.

## Development line

- **2023-09-12 — Pika camera-control development was recorded.** Zoom, pan и rotate; направления панорамирования можно сочетать, а типы движения — нет.
- **2025-02-07 — Pika Additions entered Pika's product line.** On 2025-02-07, an official Pika URL identified a named capability, Pika Additions. The dated link does not establish its mechanics, availability, or rollout scope, so this event records the appearance of that named capability only.

## What changed

2023-09-12 — в Discord-версии появился параметр -camera: zoom, pan и rotate; направления панорамирования можно сочетать, а типы движения — нет. 2023-11-29 — Pika 1.0 перевела продукт от Discord-бота к новому веб-интерфейсу и новому модели для генерации и редактирования видео в 3D-анимации, аниме, мульт- и кинематографическом стилях. 2025-02-07 — Pikadditions добавил video-to-video вставку человека или объекта в существующий ролик; независимый датированный источник фиксирует запуск 6 февраля 2025 года. 2026-02-28 — содержание привязанной публикации X не удалось проверить: страница не отдала текст. Нельзя надёжно связать с этой датой конкретную модель или выпуск. 2025-04-10 — Pikaframes получил переходы и трансформации между максимум пятью кадрами, с общей длиной до 25 секунд. 2025-04-24 — появился Pikatwists для текстового описания преобразования ролика. 2025-05-01 — появились новые Pikaffects; поддержка видео-входа отмечена в истории приложения 9 мая 2025 года. 2026-01-26 — история приложения зафиксировала Pika 2.5; текущая тарифная страница указывает его как доступную модель для text-to-video и image-to-video.

## How to use this

From 2023-09-12 and 2025-02-07, practitioners should track camera control and Pika Additions as separate Pika capability areas, and verify current behavior and access before relying on either in a production workflow.

1. Войдите в Pika и выберите режим: text-to-video, image-to-video, Pikaframes, Pikadditions, Pikaswaps, Pikatwists или Pikaffects.
  — <https://pika.art/pricing>
2. Для Pikadditions загрузите исходное видео, при необходимости референс-изображение объекта, и опишите добавление текстом; API принимает 720p или 1080p и длительность 5 либо 10 секунд.
  — <https://mcp.pika.art/models/pika/pikadditions/video-to-video>
3. Для API сначала загрузите локальный медиафайл через presigned upload, затем передайте возвращённый URL в запрос генерации.
  — <https://mcp.pika.art/models/pika/pikadditions/video-to-video>
4. Сохраните идентификатор асинхронной задачи, опрашивайте её до completed или failed и только затем запрашивайте URL результата.
  — <https://mcp.pika.art/models/pika/pikadditions/video-to-video>

## Best practices

- Для управляемого движения в историческом Discord-режиме ставьте -camera без пробела перед дефисом; используйте zoom, pan или rotate и не объединяйте несовместимые типы движения.
  — <https://mmmnote.com/article/7e7/11/article-41241b98282aa08c.shtml>
- Для API задавайте Idempotency-Key для повторяемого запроса и не меняйте тело запроса при повторном использовании ключа.
  — <https://mcp.pika.art/models/pika/pikadditions/video-to-video>
- Не считайте queued или running готовым роликом: обрабатывайте completed и failed как терминальные состояния, а 429 — с Retry-After.
  — <https://mcp.pika.art/models/pika/pikadditions/video-to-video>
- Не выбирайте Pikadditions для покадровой ротоскопии, пиксельно-точного композитинга или полнометражного видео; документация прямо относит эти задачи к неподходящим.
  — <https://mcp.pika.art/models/pika/pikadditions/video-to-video>

## Superseded by this

- 2023-09-12 — прежний Discord-синтаксис -camera является историческим, а не описанием текущего веб-продукта.
- 2023-11-29 — Pika 1.0 и его прежний веб-опыт заменены последующими линейками, включая Pika 2.5 в текущей тарифной сетке.
- 2025-02-07 — раннее описание Pikadditions как единственной новинки устарело: текущая линейка также включает Pikascenes, Pikaswaps, Pikatwists, Pikaffects и Pikaframes.

## Still unknown

- Публикация X от 2026-02-28 не отдала текст при проверке; её содержание, точная модель и масштаб изменения неизвестны.
- Ссылки 2023 года на Discord и The source не были доступны для независимого прочтения; камера-контроль и Pika 1.0 подтверждены датированными вторичными источниками.
- Тема Pika AI Selves не подтверждена доступными источниками как отдельный продукт или функция Pika; возможно, это отдельное наименование в исходных сообщениях.
- Запрошенные отдельные поля event_findings и new_events не предусмотрены заданной схемой ответа; их факты сохранены в хронологии what_changed.

## Sources

| source | title | read |
|---|---|---|
| https://mmmnote.com/article/7e7/11/article-41241b98282aa08c.shtml | Pika Labs推出影像控制新功能,-camera提升视觉丰富度 | 2026-09-05 |
| https://petapixel.com/2023/11/28/generative-video-startup-pika-labs-launches-version-1-0-raises-55-million-in-funding/ | Generative Video Startup Pika Labs Launches Version 1.0, Raises $55 Million in Funding | 2026-09-05 |
| https://pika.art/blog | Blog | Pika | 2026-09-05 |
| https://pika.art/pikadditions | Pika | 2026-09-05 |
| https://www.tomsguide.com/ai/ai-image-video/pika-labs-launches-pikadditions-to-add-anything-and-anyone-to-any-video-heres-how | Pika Labs launches 'Pikadditions' to add anything and anyone to any video — here's how | 2026-09-05 |
| https://mcp.pika.art/models/pika/pikadditions/video-to-video | Pikadditions | Pika API | 2026-09-05 |
| https://pika.art/pricing | Subscription Pricing | Pika | 2026-09-05 |
| https://apps.apple.com/us/app/pika-ai-video/id6680155400?platform=vision | Pika - AI Video App - App Store | 2026-09-05 |
| https://x.com/pika_labs/status/2027549433261658534 | x.com | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:pika`, thread `pika-product-development`, 2 dated events 2023-09-12 → 2025-02-07.
- **Practical note:** From 2023-09-12 and 2025-02-07, practitioners should track camera control and Pika Additions as separate Pika capability areas, and verify current behavior and access before relying on either in a production workflow.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.

<!-- live-update:06c7c10844b7ed72ed62dccaa822bdae7f792ba53f257a054730ad1d38182839 -->
## 2026-09-17 — Pika introduces a new multi-model creative platform

Pika launched a creative platform. The pricing covers Pika and partner models through pooled credits.

## 2026-09-19 — Pika’s relaunch adds third-party video models

Archived pricing shows third-party video models in Pika’s September relaunch, including Wan 3.0 and Seedance 2.5. Nobody verified the intake label’s full model list independently.

## 2026-09-19 — Pika’s relaunch updates Fancy-plan credits

Archived pricing puts the Fancy plan at 8,550 monthly credits after the September relaunch, under a wider multi-model system.

### Usage and practices

- Check the plan table and credit burn per run for your chosen model, resolution, and duration. [Source](https://pika.art/pricing?interval=month&plan=standard)
- Pick a model and generate or edit in Pika Create. Use a paid plan if you need commercial rights. [Source](https://pika.art/pricing?interval=month&plan=standard)
- Attach the source image and describe the exact change for image edits. Keep only essential references and name each reference’s role. [Source](https://create.pika.art/apps/nano-banana?tab=all-apps)
- Pick the output format after generation in Nano Banana. PNG is default, while JPEG and WEBP are available. [Source](https://create.pika.art/apps/nano-banana?tab=all-apps)
- Budget by finished clips, not credits. Per-model burn rates mean more credits can yield fewer finished outputs. [Source](https://www.strategyoffinance.com/essays/pika-repriced-without-changing-its-prices/)
- Limit reference images and state the role of each one so composition stays consistent. [Source](https://create.pika.art/apps/nano-banana?tab=all-apps)
- Pass exact target text for translated image copy, then check the spelling yourself. [Source](https://create.pika.art/apps/nano-banana?tab=all-apps)

### What practitioners say

- One independent pricing analyst noted on 2026-10-13 that September’s credit boost did not lower final video costs, because partner models burned more credits than earlier baselines. [Source](https://www.strategyoffinance.com/essays/pika-repriced-without-changing-its-prices/)

### Additional evidence

- 2026-09-17: Pika’s official launch video introduces a new creative platform. Current pricing confirms all plans include every model, covering Google, OpenAI, Kling, Pika, Grok, and Seedance. [Source](https://www.youtube.com/watch?v=zIyjTj2dk10)
- 2026-09-19: An analysis of archived pricing dates the relaunch between September 13 and 21. It documents third-party video models like Wan 3.0 and Seedance 2.5 in the credit table, but does not verify MiniMax H3 or GPT Image 2.5 for that September record. [Source](https://www.strategyoffinance.com/essays/pika-repriced-without-changing-its-prices/)
- 2026-09-19: Archived pricing records Fancy at 8,550 monthly credits after relaunch, not 8,500. It notes a slider up to $880 monthly; official pricing now lists Fancy from 8,550 credits at $95 per month. [Source](https://www.strategyoffinance.com/essays/pika-repriced-without-changing-its-prices/)

### Subsequent developments

- 2026-10-16: Pika announced an official ChatGPT extension to bring its tools and library into ChatGPT, offering a 250-credit trial. [Source](https://www.youtube.com/watch?v=HU_AfpToV_E)

### Superseded guidance (retained for history)

- 2026-09-21: The September 2026 pricing structure replaced previous plans: Standard had 700 credits, Pro had 2,300, and Fancy had 6,000. [Source](https://www.strategyoffinance.com/essays/pika-repriced-without-changing-its-prices/)
- 2026-09-21: A free tier requiring credit packs replaced the older free tier with monthly video credits. [Source](https://www.strategyoffinance.com/essays/pika-repriced-without-changing-its-prices/)

### Limits and open questions

- No dated first-party source confirms the claimed 8,500-credit giveaway; archived pricing records Fancy at 8,550 monthly credits instead.
- No public dated source verifies MiniMax H3 in the September 2026 launch roster.
- The two September 19 records overlap heavily, and public research did not clarify whether they cover separate announcements.
- Live product changes can alter current model availability and credit pricing.

<!-- Retained base: 13a85a61e6ba4f53f96a9c36f253b66b2e90e6d8; article blob: 5f5f05a66640753fe54645cae30dd235bbafc836 -->
