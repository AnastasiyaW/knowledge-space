---
title: Gemini — Gemini development
category: projects
tags: [gemini, gemini-development, project]
aliases: ["Gemini", "Gemini 1.5", "Gemini 3.7 Flash"]
---

# Gemini — Gemini development

**Development line:** `project:gemini` · thread `gemini-development`  
**Events:** 6 dated, 2024-02-16 → 2026-08-14 · **Researched:** 2026-09-04 · confidence: high

## What it is

Gemini — семейство Google для чата, работы с текстом, кодом, изображениями, аудио и видео, а также для API-интеграций. Возможности: Gemini app для ручной работы; AI Studio для проверки промптов и генерации кода; Gemini API для приложений; Live API для потоковых голосовых и vision-интерфейсов. Ограничение: доступ к приложению, API-ключам, тарифам, Live API и функциям macOS независим; Live API всё ещё Preview. Вердикт: прототипируйте в AI Studio, а в production закрепляйте конкретный stable model ID и проверяйте его тариф и lifecycle.

## Development line

- **2024-02-16 — Google publishes a Gemini model-development announcement.** On 2024-02-16, Google linked an official Technology & AI blog item about Gemini as a next-generation model. This is a first-party model-development announcement for Gemini. The supplied link alone does not establish its exact feature or availability scope.
- **2024-12-12 — Gemini-related Live interface appears in Google AI Studio.** On 2024-12-12, a Google AI Studio Live page was linked for the Gemini line. This indicates a Gemini-related live-interaction surface in the developer environment. The supplied URL does not establish the precise model, API, or launch status.
- **2026-03-03 — Gemini 3.1 Flash-Lite Preview appears with pricing documentation.** On 2026-03-03, Google AI Studio linked Gemini 3.1 Flash-Lite Preview alongside official pricing documentation for that named preview. This is a material availability-and-pricing step for the Gemini developer model line. The supplied links do not establish quotas, regions, or final-release status.
- **2026-04-10 — Gemini app announces 3D-model and chart capabilities.** On 2026-04-10, Google linked an official Gemini app announcement concerning 3D models and charts, together with the Gemini app. This records a product-capability step in the Gemini application surface. The URLs alone do not establish how the capability was implemented or which accounts received it.
- **2026-04-16 — Gemini gains a Mac-specific product surface.** On 2026-04-16, Google linked a Gemini page specifically for Mac. This records an expansion of the Gemini product's desktop-platform surface. The supplied URL does not establish the exact supported macOS versions, rollout scope, or feature set.
- **2026-08-14 — Google introduces Gemini 3.7 Flash for AI Studio.** On 2026-08-14, Google linked an official announcement introducing Gemini 3.7 Flash and an AI Studio prompt URL selecting that model. This is a material model-release and developer-availability step. The supplied links do not establish the model's final status, limits, or regional availability.

## What changed

Gemini — линия изменений: — 2024-02-16: Gemini 1.5 Pro принесла MoE-архитектуру, стандартный контекст 128K и ограниченный preview до 1M токенов через AI Studio и Vertex AI. — 2024-12-12: с Gemini 2.0 появилась Multimodal Live API-линия для real-time аудио и видеопотоков; исторический AI Studio Live URL сейчас требует входа, а нынешний Live API работает через stateful WebSocket и остаётся Preview. — 2026-03-03: Gemini 3.1 Flash-Lite вышел в preview для высокочастотных задач, перевода, модерации и обработки данных; preview endpoint позже был снят. — 2026-04-10: Gemini app получила генерацию интерактивных симуляций и моделей прямо в чате, включая управляемые параметры визуализаций. — 2026-04-16: Gemini for macOS добавил desktop-вход с горячими клавишами и контекстом экрана; нужна Apple Silicon машина с macOS 15+ в поддерживаемой стране. — 2026-08-14: Gemini 3.7 Flash, объявленный Google 13 августа, стал Flash-моделью для coding и agent workflows. — Найдено 2026-09-04: Gemini 3.8 Flash вышел 2 сентября и указан как текущий stable Flash; Gemini 3.7 Flash остаётся fully supported, но в списке моделей уже помечен previous-generation.

## How to use this

As of 2026-08-14, practitioners should track Gemini by product surface: use AI Studio's Live interface for live workflows (2024-12-12), evaluate and price Gemini 3.1 Flash-Lite Preview before adoption (2026-03-03), and select Gemini 3.7 Flash in AI Studio where available (2026-08-14), while treating Gemini app and Mac features as separate product surfaces.

1. Для разовой работы откройте Gemini app, войдите в Google Account и начните чат с текстом или приложенными материалами.
  — <https://gemini.google.com/app>
2. На Mac установите Gemini for macOS только если устройство Apple Silicon, macOS Sequoia 15.0+ и страна поддерживает Gemini app.
  — <https://gemini.google/mac/>
3. Для прототипа откройте Google AI Studio, выберите подходящий prompt-интерфейс, протестируйте модель, параметры, safety settings и нужные инструменты.
  — <https://ai.google.dev/gemini-api/docs/ai-studio-quickstart>
4. После удачного прототипа используйте Get code, создайте или импортируйте Cloud project и выпустите API auth key для серверной интеграции.
  — <https://ai.google.dev/gemini-api/docs/api-key>
5. Перед внедрением выберите конкретный stable endpoint из текущего списка моделей; для новых сложных agent/coding задач оцените gemini-3.8-flash, а не автоматически старый 3.7 endpoint.
  — <https://ai.google.dev/gemini-api/docs/models>
6. Для голосового или vision-диалога в реальном времени используйте отдельный Live API путь с WebSocket; для client-to-server сценария применяйте ephemeral tokens.
  — <https://ai.google.dev/gemini-api/docs/live-api>

## Best practices

- Закрепляйте production на конкретном stable model ID, а не на latest или experimental alias: latest меняется автоматически, а experimental endpoint может иметь более строгие лимиты и измениться без стабильного контракта.
  — <https://ai.google.dev/gemini-api/docs/models>
- Для Gemini 3 формулируйте короткие прямые инструкции; не переносите без необходимости многословные техники prompt engineering от старых моделей.
  — <https://ai.google.dev/gemini-api/docs/gemini-3>
- Для сложного JSON Schema включайте Structured Output, а не полагайтесь только на инструкцию «ответь JSON»; для повторяемого формата добавляйте несколько согласованных примеров.
  — <https://ai.google.dev/gemini-api/docs/prompting-strategies>
- В long-context запросах размещайте вопрос после материала, не отправляйте ненужный контекст и кэшируйте повторно используемые файлы или данные.
  — <https://ai.google.dev/gemini-api/docs/long-context>
- Держите API-ключ вне Git и вне клиентского кода; для веб- и мобильного production вызывайте Gemini через backend, а ключ ограничивайте.
  — <https://ai.google.dev/gemini-api/docs/api-key>
- Перед расчётом стоимости сверяйте текущую таблицу: free и paid tiers различаются лимитами, функциями и обработкой контента, поэтому цена из старого анонса не является сметой.
  — <https://ai.google.dev/gemini-api/docs/pricing?hl=ru#gemini-3.1-flash-lite-preview>

## Superseded by this

- 2024-02-16 — режим раннего доступа Gemini 1.5 Pro с 128K стандартного контекста и ограниченным 1M preview является исторической доступностью, а не правилом выбора модели сегодня.
- 2026-03-03 — endpoint `gemini-3.1-flash-lite-preview` снят 2026-05-25; его прямой заменой был `gemini-3.1-flash-lite`. В текущем lifecycle для последнего уже указан shutdown 2027-05-07 и следующая рекомендуемая замена `gemini-3.5-flash-lite`.
- Найдено 2026-09-04 — формулировка «Gemini 3.7 Flash — новейший Flash» устарела: `gemini-3.8-flash` выпущен 2026-09-02. `gemini-3.7-flash` не выключен, но является previous-generation stable вариантом.

## Still unknown

- Gemini объединяет разные рабочие поверхности — consumer app, macOS app, AI Studio, Gemini API и Live API. Доступ к одной из них не доказывает доступ к тарифам, квотам или функциям другой.
- Исторический URL AI Studio Live теперь ведёт на форму входа. Точный интерфейс и настройки страницы от декабря 2024 нельзя проверить без авторизованного сеанса; запуск Live-направления подтверждён отдельным официальным анонсом от 11 декабря 2024 и текущей документацией.
- Страница Gemini for macOS подтверждает текущие требования и ограничения, но не содержит собственной даты запуска; дата 2026-04-16 не подтверждена этой страницей независимо.

## Sources

| source | title | read |
|---|---|---|
| https://blog.google/technology/ai/google-gemini-next-generation-model-february-2024/#sundar-note | Our next-generation model: Gemini 1.5 | 2026-09-04 |
| https://blog.google/innovation-and-ai/models-and-research/google-deepmind/google-gemini-ai-update-december-2024/ | Google introduces Gemini 2.0: A new AI model for the agentic era | 2026-09-04 |
| https://aistudio.google.com/live | Sign in - Google Accounts | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/pricing?hl=ru#gemini-3.1-flash-lite-preview | Цены на API Gemini Developer | 2026-09-04 |
| https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-flash-lite/ | Gemini 3.1 Flash-Lite: Built for intelligence at scale | 2026-09-04 |
| https://blog.google/innovation-and-ai/products/gemini-app/3d-models-charts/ | The Gemini app can now generate interactive simulations and models. | 2026-09-04 |
| https://gemini.google.com/app | Google Gemini | 2026-09-04 |
| https://gemini.google/mac/ | Gemini for macOS – native AI assistant and Mac automation | 2026-09-04 |
| https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-3-7-flash/ | Introducing Gemini 3.7 Flash | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/models | Models | Gemini API | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/deprecations?hl=en | Gemini deprecations | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/latest-model | What's new in Gemini 3.8 Flash | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/ai-studio-quickstart | Google AI Studio quickstart | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/api-key | Using Gemini API keys | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/prompting-strategies | Prompt design strategies | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/long-context | Long context | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/gemini-3 | Gemini 3 developer guide | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/live-api | Gemini Live API overview | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:gemini`, thread `gemini-development`, 6 dated events 2024-02-16 → 2026-08-14.
- **Practical note:** As of 2026-08-14, practitioners should track Gemini by product surface: use AI Studio's Live interface for live workflows (2024-12-12), evaluate and price Gemini 3.1 Flash-Lite Preview before adoption (2026-03-03), and select Gemini 3.7 Flash in AI Studio where available (2026-08-14), while treating Gemini app and Mac features as separate product surfaces.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
