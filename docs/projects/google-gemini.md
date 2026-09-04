---
title: Gemini — Gemini product development
category: projects
tags: [gemini, gemini-app, gemini-gems, gemini-product-development, google-gemini, project]
aliases: ["Gemini", "Google Gemini"]
---

# Gemini — Gemini product development

**Development line:** `project:google-gemini` · thread `gemini-product-development`  
**Events:** 1 dated, 2026-07-22 → 2026-07-22 · **Researched:** 2026-09-04 · confidence: medium

## What it is

Gemini — продукты Google для чата, файлов, кода и интеграции модели в приложение. — Gemini Apps: диалог, вложения и выбор модели. — Gems: сохранённые инструкции для повторяемых задач. — Gemini API и AI Studio: мультимодальные вызовы, структурированный вывод и инструменты. Мера: доступные model ID и статусы меняются; текущий справочник уже содержит `gemini-3.8-flash`, а `gemini-3.6-flash` остаётся в списке. Вывод: для личной рутины нужен Gem, для продукта — API с явным выбором модели и проверкой ответа.

## Development line

- **2026-07-22 — Gemini 3.6 Flash was linked with updated Flash model variants.** On 2026-07-22, the sealed record linked an official Google Blog Gemini-models page whose URL identifies Gemini 3.6 Flash, Gemini 3.5 Flash Lite, and Gemini 3.5 Flash Cyber. It also linked an AI Studio new-chat URL configured for Gemini 3.6 Flash, establishing a contemporaneous model-selection reference. The supplied evidence does not establish launch details, capabilities, regions, or terms, so none are stated here.

## What changed

2024-05-14 — Gemini Apps: Gemini Advanced получил Gemini 1.5 Pro с контекстом 1 млн токенов и загрузкой файлов; источник найден сегодня. 2024-05-14 — Gems: Google показал настраиваемые версии Gemini, но в тот день это была пометка «soon», а не подтверждённый общедоступный запуск; источник найден сегодня. 2024-05-14, найдено сегодня — Gemini API: Google представил Gemini 1.5 Flash для высокочастотных задач, а Gemini 1.5 Pro получил контекст до 2 млн токенов и обработку аудио в API и AI Studio. 2024-12-20 — AI Studio: указан URL нового чата; он не раскрывает модель, версию или релиз, поэтому более точное изменение не подтверждено. 2026-07-22 — Flash-линейка: связанная страница Google от 2026-07-21 представила Gemini 3.6 Flash, 3.5 Flash-Lite и ограниченный пилот 3.5 Flash Cyber; 3.6 и 3.5 Flash-Lite стали доступны через Gemini API и AI Studio. 2026-09-04, найдено сегодня — текущий каталог Gemini API перечисляет `gemini-3.8-flash`, `gemini-3.7-flash`, `gemini-3.6-flash` и `gemini-3.5-flash-lite`; 3.6 больше не единственный актуальный выбор. Ограничение: 3.5 Flash Cyber не стал общедоступной API-моделью — Google описывает пилот для правительств и доверенных партнёров через CodeMender. Вывод: для новой интеграции берите версию из текущего каталога, а не из старой ссылки AI Studio.

## How to use this

From 2026-07-22, practitioners should treat Gemini 3.6 Flash as a recorded AI Studio model-selection candidate and verify its capabilities, rollout, and pricing in the linked official model update before adopting it.

1. Для личной задачи откройте Gemini Apps, войдите в аккаунт, выберите модель, добавьте при необходимости файл или изображение и отправьте запрос.
  — <https://support.google.com/gemini/answer/13275745?hl=en>
2. Для повторяемой роли откройте Explore Gems → New Gem; задайте имя и инструкции с ролью, задачей, контекстом и форматом, проверьте в preview и сохраните.
  — <https://support.google.com/gemini/answer/15235603>
3. Для интеграции создайте проект и ключ в AI Studio, храните ключ в переменной окружения, установите SDK и выполните первый вызов Interactions API из Python, JavaScript или REST.
  — <https://ai.google.dev/gemini-api/docs/get-started>
4. Перед выпуском выберите точный model ID из живого каталога и закрепите его в конфигурации; текущая документация начинает с `gemini-3.8-flash`.
  — <https://ai.google.dev/gemini-api/docs/models?hl=en>
5. Когда ответ требует свежих данных, подключите Google Search; при обращении к собственной системе объявите функцию, выполните её в приложении и верните результат модели.
  — <https://ai.google.dev/gemini-api/docs/tools>

## Best practices

- Формулируйте цель, ограничения, формат и контекст явно; используйте несколько согласованных примеров, если важны стиль или классификация.
  — <https://ai.google.dev/gemini-api/docs/prompting-strategies>
- Для Gemini 3.x сначала оставляйте temperature, top-p и top-k по умолчанию; документируйте и проверяйте каждое изменение, потому что настройка может ухудшить сложное рассуждение или вызвать цикл.
  — <https://ai.google.dev/gemini-api/docs/prompting-strategies>
- Используйте Structured Outputs для фиксированного финального формата, а Function Calling — для действия; JSON по схеме всё равно проверяйте на семантику и бизнес-правила.
  — <https://ai.google.dev/gemini-api/docs/structured-output>
- Проверяйте ответ Gemini Apps перед профессиональным решением: справка прямо предупреждает, что приложение может ошибаться.
  — <https://support.google.com/gemini/answer/13275745?hl=en>
- Выбирайте тариф до передачи рабочих данных: для Free Google указывает использование контента для улучшения продуктов, для Paid — нет; сверяйте это с требованиями команды и договора.
  — <https://ai.google.dev/gemini-api/docs/pricing>

## Superseded by this

- 2024-05-14: состояние «Gems скоро появятся» устарело — текущая справка описывает создание, предварительную проверку и сохранение Gems.
- 2024-05-14: рекомендация начинать новую API-интеграцию с Gemini 1.5 Flash или 1.5 Pro устарела; текущий каталог Gemini API ведёт по 3.x и перечисляет Gemini 3.8 Flash.
- 2026-07-22: Gemini 3.6 Flash и 3.5 Flash-Lite остаются доступными, но считать 3.6 Flash автоматически самым новым Flash нельзя: текущий каталог также содержит 3.7 и 3.8 Flash.
- 2024-12-20: URL нового чата AI Studio — точка входа, а не устойчивая рекомендация по версии модели.

## Still unknown

- Точные формулировки двух записей от 2024-05-14 недоступны: официальные анонсы того дня подтверждают направление, но не текст каждой записи.
- Запись от 2024-12-20 даёт только URL нового чата AI Studio; из него нельзя достоверно вывести модель, версию или релиз.
- Gemini Apps, Gems и Gemini API — разные поверхности одного семейства, а не отдельные проекты; доступность зависит от аккаунта, тарифа, региона и модели.

## Sources

| source | title | read |
|---|---|---|
| https://blog.google/products-and-platforms/products/gemini/google-gemini-update-may-2024/ | Get more done with Gemini: Try 1.5 Pro and more intelligent features | 2026-09-04 |
| https://blog.google/innovation-and-ai/products/google-gemini-update-flash-ai-assistant-io-2024/ | Gemini breaks new ground with a faster model, longer context, AI agents and more | 2026-09-04 |
| https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/ | Introducing Gemini 3.6 Flash, 3.5 Flash-Lite, and 3.5 Flash Cyber | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/models?hl=en | Models | Gemini API | Google AI for Developers | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/get-started | Getting started | Gemini API | Google AI for Developers | 2026-09-04 |
| https://support.google.com/gemini/answer/13275745?hl=en | Use Gemini Apps | 2026-09-04 |
| https://support.google.com/gemini/answer/15235603 | Tips for creating custom Gems | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/prompting-strategies | Prompt design strategies | Gemini API | Google AI for Developers | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/tools | Using tools with Gemini API | Google AI for Developers | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/structured-output | Structured outputs | Gemini API | Google AI for Developers | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/pricing | Gemini Developer API pricing | Gemini API | Google AI for Developers | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:google-gemini`, thread `gemini-product-development`, 1 dated events 2026-07-22 → 2026-07-22.
- **Practical note:** From 2026-07-22, practitioners should treat Gemini 3.6 Flash as a recorded AI Studio model-selection candidate and verify its capabilities, rollout, and pricing in the linked official model update before adopting it.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
