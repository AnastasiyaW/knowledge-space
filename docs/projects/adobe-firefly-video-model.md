---
title: Adobe Firefly Video Model — Firefly Video Model rollout
category: projects
tags: [adobe-firefly-video-model, adobe_firefly, firefly-video-model-rollout, project]
aliases: ["Adobe Firefly Video", "Adobe Firefly Video Model"]
---

# Adobe Firefly Video Model — Firefly Video Model rollout

**Development line:** `project:adobe-firefly-video-model` · thread `firefly-video-model-rollout`  
**Events:** 2 dated, 2024-09-11 → 2024-10-14 · **Researched:** 2026-09-04 · confidence: high

## What it is

Adobe Firefly Video Model — модель Adobe для коротких клипов из текста и изображений; в Generate video она соседствует с партнёрскими моделями, поэтому Firefly Video нужно выбрать явно. — Text-to-Video и Image-to-Video с первым и последним ключевым кадром. — Управление форматом, разрешением, размером и углом кадра, движением камеры и стилем. — Экспорт или передача клипа в Firefly video editor и Premiere. Мера: текущая документация для Firefly Video указывает 5 секунд, 24 fps, 540p/720p/1080p и 16:9, 9:16 или 1:1; более высокое разрешение тратит больше generative credits. Вывод: это инструмент для отдельных планируемых шотов, переходов и b-roll, а длинную сцену нужно собирать монтажом из клипов.

## Development line

- **2024-09-11 — Adobe previews a forthcoming video model for Firefly.** On 2024-09-11, Adobe publicly signaled that a video model was planned for its Firefly product line. This was a material development milestone because it established the product direction before users could access a video-generation experience.
- **2024-10-14 — Adobe introduces a beta video-generation experience in Firefly.** On 2024-10-14, Adobe introduced a beta video-generation experience in the Firefly web application. This advanced the line from a forthcoming-model announcement to a user-facing beta stage.

## What changed

Adobe Firefly Video Model — путь от анонса к доступной модели внутри многомодельного Generate video. — 2024-09-11: Adobe анонсировала модель и waitlist; обещаны Text-to-Video, Image-to-Video, референс-изображения и управление камерой для b-roll и заполнения монтажных разрывов. — 2024-10-14: ранний доступ в Firefly web app получили отдельные участники сообщества; появились практические сценарии Text-to-Video и Image-to-Video для вставок и новых элементов в существующем материале. — 2025-02-12, найдено сегодня: публичная бета вошла в обновлённое Firefly web app, с генерацией из текста и изображения и 1080p на старте. — 2025-04-24, найдено сегодня: Adobe объявила Firefly Video Model общедоступной, а не бета-функцией. — 2025-07-17, найдено сегодня: Adobe заявила об улучшении точности движения, расширенных video controls, генерации звуковых эффектов и большем выборе партнёрских моделей в том же интерфейсе. — 2026-08-18–19, найдено сегодня: актуальная документация описывает Firefly Video как явный выбор модели в Generate video; новый unified generation and editing workspace остаётся beta-функцией.

## How to use this

As of 2024-10-14, practitioners could treat Firefly video generation as a beta workflow available through the Firefly web application; on 2024-09-11 it was only a forthcoming capability.

1. Откройте Firefly, выберите Video → Generate video и в Model выберите Firefly Video: при первом запуске интерфейс может поставить Veo 3.1.
  — <https://helpx.adobe.com/sg/firefly/web/work-with-audio-and-video/work-with-video/generate-videos-using-text-prompts.html>
2. Задайте разрешение, формат, Shot size, Camera angle и Motion; для Firefly Video доступны 540p, 720p или 1080p, 16:9, 9:16 либо 1:1.
  — <https://helpx.adobe.com/firefly/web/work-with-audio-and-video/work-with-video/use-style-presets-for-video-generation.html>
3. Напишите промпт по схеме кадр + персонаж/объект + действие + локация + эстетика, затем укажите стиль и движение камеры.
  — <https://helpx.adobe.com/uk/firefly/web/work-with-audio-and-video/work-with-video/writing-effective-text-prompts-for-video-generation.html>
4. Для управляемого перехода загрузите первый кадр, последний кадр или оба; при двух кадрах добавьте текстовое описание перехода.
  — <https://helpx.adobe.com/in/firefly/web/work-with-audio-and-video/work-with-video/generate-videos-using-images.html>
5. Сгенерируйте клип, затем скачайте его либо добавьте в Project media, Timeline или clip editor для дальнейшей сборки.
  — <https://helpx.adobe.com/firefly/web/unified-generation-and-editing-experience/generate-and-edit-content.html>
6. Перед запуском проверьте расход credits кнопкой рядом с Generate: он зависит от выбранного разрешения.
  — <https://helpx.adobe.com/firefly/web/work-with-audio-and-video/work-with-video/use-style-presets-for-video-generation.html>

## Best practices

- Держите промпт конкретным: кадр, субъект, действие, место, свет, цвет и стиль; больше четырёх субъектов часто сбивают модель.
  — <https://helpx.adobe.com/uk/firefly/web/work-with-audio-and-video/work-with-video/writing-effective-text-prompts-for-video-generation.html>
- Опишите действие глаголом и темпом, а движение камеры задайте либо в промпте, либо контролом Camera.
  — <https://helpx.adobe.com/uk/firefly/web/work-with-audio-and-video/work-with-video/writing-effective-text-prompts-for-video-generation.html>
- Итерируйте: начните с базового промпта и добавляйте детали по одному направлению, а для похожих результатов сохраняйте seed, промпт и настройки.
  — <https://helpx.adobe.com/sg/firefly/web/work-with-audio-and-video/work-with-video/generate-videos-using-text-prompts.html>
- Для Image-to-Video берите визуально совместимые ключевые кадры и описывайте переход; первый кадр отключает часть ручных controls, а последний отключает Motion.
  — <https://helpx.adobe.com/in/firefly/web/work-with-audio-and-video/work-with-video/generate-videos-using-images.html>
- Загружайте только изображения, на которые у вас есть права; держите вкладку открытой и не запускайте генерации одновременно в нескольких вкладках.
  — <https://helpx.adobe.com/cn/firefly/web/work-with-audio-and-video/work-with-video/about-generate-video.html>

## Superseded by this

- 2024-09-11: состояние coming soon и waitlist-only устарело после публичной беты 2025-02-12 и общей доступности 2025-04-24.
- 2024-10-14: ранний доступ для выбранных участников сообщества больше не является актуальным описанием доступа; ориентироваться нужно на текущие account-level условия и общую доступность 2025-04-24.
- 2025-02-12: обозначение модели как public beta устарело после объявления general availability 2025-04-24.
- 2025-02-12: обещание 4K coming soon не следует использовать как текущую настройку Firefly Video: в документации от 2026-08-18 для этого workflow перечислены 540p, 720p и 1080p.

## Still unknown

- Конкретные доступные модели, Image-to-Video, кредитная стоимость и право доступа не проверялись на аккаунте: Adobe указывает зависимость от плана, региона, типа пользователя и регуляторных ограничений.

## Sources

| source | title | read |
|---|---|---|
| https://blog.adobe.com/en/publish/2024/09/11/bringing-gen-ai-to-video-adobe-firefly-video-model-coming-soon | Bringing generative AI to video with Adobe Firefly Video Model | Adobe Blog | 2026-09-04 |
| https://blog.adobe.com/en/publish/2024/10/14/generate-video-beta-on-firefly-web-app | Generate Video (beta) on Firefly Web App | Adobe Blog | 2026-09-04 |
| https://blog.adobe.com/en/publish/2025/02/12/meet-firefly-video-model-ai-powered-creation-with-unparalleled-creative-control | Meet Firefly Video Model: AI-Powered creation with unparalleled creative control | Adobe Blog | 2026-09-04 |
| https://news.adobe.com/news/2025/04/adobe-revolutionizes-ai-assisted-creativity-firefly | Adobe Revolutionizes AI-Assisted Creativity with Firefly, the All-In-One Home for AI Content Creation, with New Partner and Firefly Models | 2026-09-04 |
| https://blog.adobe.com/en/publish/2025/07/17/firefly-adds-new-video-capabilities-industry-leading-ai-models-generate-sound-effects-feature | Firefly adds new video capabilities, industry leading AI models, and Generate Sound Effects feature | Adobe Blog | 2026-09-04 |
| https://helpx.adobe.com/sg/firefly/web/work-with-audio-and-video/work-with-video/generate-videos-using-text-prompts.html | Generate videos using text prompts | Firefly | 2026-09-04 |
| https://helpx.adobe.com/in/firefly/web/work-with-audio-and-video/work-with-video/generate-videos-using-images.html | Generate videos using images | Firefly | 2026-09-04 |
| https://helpx.adobe.com/uk/firefly/web/work-with-audio-and-video/work-with-video/writing-effective-text-prompts-for-video-generation.html | Writing effective text prompts for video generation | Firefly | 2026-09-04 |
| https://helpx.adobe.com/firefly/web/work-with-audio-and-video/work-with-video/use-style-presets-for-video-generation.html | Use style presets for video generation | Firefly | 2026-09-04 |
| https://helpx.adobe.com/firefly/web/unified-generation-and-editing-experience/generate-and-edit-content.html | Generate and edit images and videos in Firefly | Firefly | 2026-09-04 |
| https://helpx.adobe.com/cn/firefly/web/work-with-audio-and-video/work-with-video/about-generate-video.html | 生成视频常见问题 | Firefly | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:adobe-firefly-video-model`, thread `firefly-video-model-rollout`, 2 dated events 2024-09-11 → 2024-10-14.
- **Practical note:** As of 2024-10-14, practitioners could treat Firefly video generation as a beta workflow available through the Firefly web application; on 2024-09-11 it was only a forthcoming capability.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
