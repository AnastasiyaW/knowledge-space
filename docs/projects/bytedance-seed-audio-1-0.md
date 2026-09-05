---
title: Seed Audio 1.0 — Seed Audio
category: projects
date: 2026-07-22
tags: [bytedance-seed-audio-1-0, project, seed-audio]
aliases: ["Seed Audio 1.0"]
---

# Seed Audio 1.0 — Seed Audio

**Development line:** `project:bytedance-seed-audio-1-0` · thread `seed-audio`  
**Last event:** 2026-07-22 · 1 dated since 2026-07-22 · **Researched:** 2026-09-05 · confidence: high

## What it is

Seed Audio 1.0 — аудиомодель ByteDance для создателей видео, игр, рекламы и подкастов: генерирует речь, диалоги, эффекты и атмосферу из промпта, с референсом голоса или изображения. Лимит подтверждённого внешнего API — до трёх аудиореференсов по 30 секунд; официальный материал заявляет до двух минут аудио за один проход. Вердикт: это альтернатива связке TTS и ручного саунд-дизайна для черновой звуковой сцены, но права на голосовой референс остаются обязанностью пользователя.

## Development line

- **2026-07-22 — Seed Audio 1.0 product page and BytePlus activation path.** On 2026-07-22, the development record linked Seed Audio 1.0’s official product page and a BytePlus Voice console activation path. Together, those dated official links mark a public-facing product and onboarding step for the project, although they do not establish the exact announcement wording, feature set, availability, or release scope.

## What changed

2026-07-22 — Seed Audio 1.0 стал доступен через BytePlus как единая модель для речи, звуковых эффектов и атмосферы; официальный анонс датирован 2026-07-20, поэтому дата 22 июля описывает появление в выбранной ленте, а не первичную дату анонса.

2026-07-20 — ByteDance описала модель как генератор полной звуковой сцены: тайминг реплик задаётся с точностью 100 мс, один проход может дать до двух минут аудио с продолжением.

## How to use this

As of 2026-07-22, practitioners can treat Seed Audio 1.0 as an official product path to evaluate through Seed and BytePlus Voice, while confirming activation eligibility, availability, and capabilities before relying on it.

1. Активируйте Seed Audio в BytePlus через предоставленную консоль и создайте проект.
  — <https://console.byteplus.com/voice/new/setting/activate?projectName=default>
2. Опишите сцену одним промптом: персонажей, реплики, эмоцию, среду и ключевые звуки; при необходимости укажите моменты входа реплик.
  — <https://seed.bytedance.com/en/blog/from-speech-to-audio-creation-introducing-the-seed-audio-1-0-audio-creation-model>
3. Для программного вызова передайте обязательный prompt; референсы аудио обозначайте как @Audio1–@Audio3 и сохраните URL результата.
  — <https://fal.ai/models/bytedance/seed-audio-1.0/api>

## Best practices

- Используйте только разрешённые голосовые референсы; официальный материал прямо ограничивает такой сценарий авторизованным образцом.
  — <https://seed.bytedance.com/en/blog/from-speech-to-audio-creation-introducing-the-seed-audio-1-0-audio-creation-model>
- Для асинхронной генерации не блокируйте приложение: отслеживайте очередь или используйте webhook.
  — <https://fal.ai/models/bytedance/seed-audio-1.0/api>
- Держите API-ключ на сервере, а не в браузере или клиентском приложении.
  — <https://fal.ai/models/bytedance/seed-audio-1.0/api>

## Superseded by this

- 2026-07-20: для аудиосцены больше не обязательно собирать речь, эффекты и атмосферу как изолированные клипы; Seed Audio 1.0 предлагает единый сценовый запрос, но не отменяет проверку результата и прав на исходные голоса.

## Still unknown

- Официальная страница проекта не отдала технические спецификации при проверке, а консоль BytePlus требует интерактивного доступа; текущие тарифы, регионы и точный API-контракт BytePlus не подтверждены.
- Список содержит событие 2026-07-22, но первичный материал ByteDance датирован 2026-07-20; причина двухдневного расхождения не раскрыта.

## Sources

| source | title | read |
|---|---|---|
| https://seed.bytedance.com/en/seedaudio1_0 | ByteDance Seed — Seed Audio 1.0 project page | 2026-09-05 |
| https://console.byteplus.com/voice/new/setting/activate?projectName=default | BytePlus Voice — Seed Audio activation | 2026-09-05 |
| https://seed.bytedance.com/en/blog/from-speech-to-audio-creation-introducing-the-seed-audio-1-0-audio-creation-model | From Speech to Audio Creation | Introducing the Seed Audio 1.0 Audio Creation Model | 2026-09-05 |
| https://fal.ai/models/bytedance/seed-audio-1.0/api | Seed Audio 1.0 Text to Audio API Docs | fal | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:bytedance-seed-audio-1-0`, thread `seed-audio`, 1 dated events 2026-07-22 → 2026-07-22.
- **Practical note:** As of 2026-07-22, practitioners can treat Seed Audio 1.0 as an official product path to evaluate through Seed and BytePlus Voice, while confirming activation eligibility, availability, and capabilities before relying on it.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
