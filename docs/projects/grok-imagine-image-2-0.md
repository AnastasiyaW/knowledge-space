---
title: Grok Imagine Image 2.0 — Grok Imagine image generation
category: projects
date: 2026-08-10
tags: [grok, grok-imagine-image, grok-imagine-image-2-0, project]
aliases: ["Grok Imagine Image 2.0"]
---

# Grok Imagine Image 2.0 — Grok Imagine image generation

**Development line:** `project:grok-imagine-image-2-0` · thread `grok-imagine-image`  
**Last event:** 2026-08-10 · 1 dated since 2026-08-10 · **Researched:** 2026-09-05 · confidence: high

## What it is

Grok Imagine Image 2.0 — модель xAI для генерации и редактирования изображений в Grok и API. Возможности: текст-в-изображение, редактирование по инструкции, до пяти референсов, 1K/2K и пакетная обработка. Цена API — от $0.04 за изображение; для повторяемого результата закрепляйте quality явно. Вердикт: подходит для итеративных макетов и композитинга, но дефолт качества теперь меняет стоимость и результат.

## Development line

- **2026-08-10 — Grok Imagine Image 2.0 was introduced through an xAI product-news entry.** Модель стала доступна как Quality Mode в Grok и как `grok-imagine-image-2.0` в API.

## What changed

2026-08-10 — событие соответствует общему релизу, но официальный анонс датирован 2026-08-07: модель стала доступна как Quality Mode в Grok и как `grok-imagine-image-2.0` в API. 2026-08-28 — `quality=auto` стал допустимым, а значение по умолчанию сменилось с `medium` на `auto`; сейчас auto выбирает Low для генерации и Medium для редактирования. Также лимит референсов вырос с трёх до пяти, добавлены пропорции 21:9 и 5:2. 2026-09-02 — объявлен retirement `grok-imagine-image-quality` на 2026-11-02: его запросы будут обслуживаться Image 2.0 с `quality=low`; Image 1.0 не затронут.

На дату события 2026-08-10 дополнительное официальное уточнение: исходный релиз был 2026-08-07, а не 2026-08-10; область релиза — grok.com/imagine, iOS, Android и API.

## How to use this

From 2026-08-10, practitioners evaluating Grok Imagine should treat Image 2.0 as a dated product-line milestone and consult the linked xAI and Grok pages; they must separately verify features, access, and availability before depending on it.

1. Откройте Grok Imagine и выберите Quality Mode для интерактивной генерации или редактирования.
  — <https://x.ai/news/grok-imagine-image-2>
2. Для API создайте ключ в xAI Console и вызывайте модель `grok-imagine-image-2.0`.
  — <https://docs.x.ai/developers/model-capabilities/imagine>
3. Для новой картинки отправьте prompt в `POST /v1/images/generations`; задайте число результатов, aspect ratio и resolution.
  — <https://docs.x.ai/developers/model-capabilities/imagine>
4. Для правки отправьте URL либо base64 data URI исходной картинки в `POST /v1/images/edits` и опишите требуемое изменение.
  — <https://docs.x.ai/developers/model-capabilities/imagine>
5. Для композитинга передайте до пяти исходных изображений в один edit-запрос.
  — <https://docs.x.ai/developers/model-capabilities/imagine>

## Best practices

- Явно передавайте `quality=low` или `quality=medium`: `auto` стал дефолтом 2026-08-28 и выбирает разное качество для generation и editing.
  — <https://docs.x.ai/developers/release-notes>
- Закрепите slug `grok-imagine-image-2.0` в новых интеграциях; не планируйте новую работу на `grok-imagine-image-quality`, который будет снят 2026-11-02.
  — <https://docs.x.ai/developers/release-notes>
- Считайте входные изображения отдельно: edit оплачивает и image input, и сгенерированный output.
  — <https://docs.x.ai/developers/model-capabilities/imagine>
- Для больших независимых наборов используйте Batch API, поддерживаемый моделью, а не превышайте лимит шесть запросов в секунду в real-time API.
  — <https://docs.x.ai/developers/models/grok-imagine-image-2.0>

## Superseded by this

- 2026-08-28: прежнее допущение, что пропущенный `quality` означает `medium`, устарело; теперь это `auto`.
- 2026-09-02: для новых интеграций устаревает guidance использовать `grok-imagine-image-quality`; его retirement назначен на 2026-11-02.

## Still unknown

- Официальная страница grok.com/imagine не отдала доступный текст в проверке, поэтому конкретные тарифы и географическая доступность потребительского интерфейса не подтверждены.

## Sources

| source | title | read |
|---|---|---|
| https://x.ai/news/grok-imagine-image-2 | Imagine Image 2.0 | SpaceXAI | 2026-09-05 |
| https://docs.x.ai/developers/model-capabilities/imagine | Imagine Overview | SpaceXAI Docs | 2026-09-05 |
| https://docs.x.ai/developers/models/grok-imagine-image-2.0 | Grok Imagine Image 2.0 | SpaceXAI Docs | 2026-09-05 |
| https://docs.x.ai/developers/release-notes | Release Notes | SpaceXAI Docs | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:grok-imagine-image-2-0`, thread `grok-imagine-image`, 1 dated events 2026-08-10 → 2026-08-10.
- **Practical note:** From 2026-08-10, practitioners evaluating Grok Imagine should treat Image 2.0 as a dated product-line milestone and consult the linked xAI and Grok pages; they must separately verify features, access, and availability before depending on it.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
