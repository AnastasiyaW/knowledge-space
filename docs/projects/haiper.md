---
title: Haiper — Public launch and iOS availability
category: projects
tags: [haiper, project, public-launch-and-ios-availability]
aliases: ["Haiper"]
---

# Haiper — Public launch and iOS availability

**Development line:** `project:haiper` · thread `public-launch-and-ios-availability`  
**Events:** 2 dated, 2024-03-13 → 2024-03-16 · **Researched:** 2026-09-04 · confidence: medium

## What it is

Haiper — бывшая облачная платформа для авторов и интеграторов, конкурировавшая с Runway в text-to-video и image-to-video. — text-to-video, image-to-video, keyframe conditioning, video-to-video и text-to-image; — раньше: веб, iOS и HTTP API. В опубликованной документации 2.x указаны 540p/720p и 5–8 кредитов за секунду, но продажа доступа и успешный новый job не подтверждены. Вывод: не выбирать Haiper для нового production workflow; API считать legacy до авторизованного пробного job.

## Development line

- **2024-03-13 — Haiper’s official website was publicly referenced.** On 2024-03-13, a dated record linked to Haiper’s official website. This documents a public web presence for the project at that time. The available evidence does not establish the specific product claim or launch wording accompanying the link.
- **2024-03-16 — Haiper’s iOS app was publicly linked.** On 2024-03-16, a dated record linked to Haiper’s Apple App Store listing and to the earlier Haiper record. This documents public iOS app availability or promotion at that time. The available evidence does not establish the app’s capabilities, release status, or accompanying announcement text.

## What changed

Haiper: 2024-03-13 — веб-адрес Haiper стал точкой входа. Современное тому времени описание фиксирует публичный beta-сервис: бесплатные короткие text-to-video, анимацию изображений и repaint; 2 секунды HD либо до 4 секунд с меньшим качеством. 2024-03-16 — к веб-маршруту добавлен исходный App Store URL. Это подтверждает появление iOS-маршрута в продуктовых ссылках, но не дату релиза приложения. 2024-10-21 (найдено сегодня) — Haiper 2.0 и Templates расширили продукт от базовой генерации к версии модели и шаблонному созданию роликов. 2024-12-18 (найдено сегодня) — Haiper 2.5 вышел в API-интеграцию с VEED: развитие сместилось к партнёрским и API-сценариям. 2025-03-20 (найдено сегодня) — Sifted сообщил о найме Microsoft двух сооснователей Haiper. 2025-06-23 (найдено сегодня) — Sifted сообщил, что NetMind купила AI-модель Haiper; это сменило владельца технологии. 2026-09-04 (найдено сегодня) — домен и API-документация открываются, но подтверждённого нового пользовательского входа, оплаты или завершённой генерации нет.

## How to use this

From 2024-03-16, practitioners should treat Haiper as having a publicly referenced web presence and an iOS distribution path, while verifying current availability and capabilities directly before relying on either.

1. Проверьте, может ли поставщик реально выдать API key после пополнения; если ключ не выдаётся, остановитесь: публичный путь запуска не подтверждён.
  — <https://docs.haiper.ai/api-reference/authentication>
2. Только с действующим ключом отправьте один одноразовый text-to-video job на documented endpoint и сохраните generation_id.
  — <https://docs.haiper.ai/api-reference/endpoint/2-0-text-to-video>
3. Опросите status по generation_id; обрабатывайте pending, processing, post_processing и failed как разные состояния.
  — <https://docs.haiper.ai/api-reference/endpoint/get-creation-status>
4. Запрашивайте результат только после succeed; detail endpoint возвращает URL видео и outputs.
  — <https://docs.haiper.ai/api-reference/endpoint/get-creation-detail>

## Best practices

- Не храните единственную копию ролика или проекта в облаке Haiper: сообщения пользователей начала февраля 2025 фиксируют недоступность сайта и работ после закрытия.
  — <https://uk.trustpilot.com/review/haiper.ai>
- Для клиентских материалов явно передавайте is_public=false: в опубликованном API значение по умолчанию — true.
  — <https://docs.haiper.ai/api-reference/endpoint/2-0-text-to-video>
- Закладывайте лимиты в клиент: по документации это 500 HTTP-запросов в минуту и 40 параллельных генераций; на 429 не повторяйте запрос бесконтрольно.
  — <https://docs.haiper.ai/api-reference/rate-limits>
- Не запрашивайте детали до succeed: сначала status, затем detail; это предотвращает ложный успех и пустые ссылки.
  — <https://docs.haiper.ai/api-reference/endpoint/get-creation-detail>

## Superseded by this

- 2024-03-05—2024-03-13: рекомендация зарегистрироваться в бесплатной consumer beta и генерировать ролики в веб-приложении устарела для нового пользователя; потребительский доступ не подтверждён после событий 2025 года.
- 2024-03-16: рекомендация устанавливать приложение по исходному App Store URL устарела как актуальный onboarding-маршрут: при проверке он не отдал текущую карточку продукта.
- 2024-12-18: анонс Haiper 2.5 API и VEED — историческое описание интеграции, а не подтверждение, что исходный API или партнёрский маршрут принимает новую работу сегодня.
- Исторические цены из опубликованной документации не являются текущей офертой, пока не подтверждены выдача ключа и успешный job.

## Still unknown

- Официального датированного заявления Haiper о закрытии consumer-продукта не найдено; февраль 2025 подтверждается пользовательскими сообщениями и поздними вторичными источниками, а не уведомлением компании.
- Не выполнен авторизованный API job и не проверена выдача нового ключа, поэтому опубликованная документация может быть сохранённым legacy-артефактом.
- Исходный App Store URL не отдал текущую карточку при проверке; неизвестны его региональный статус, делистинг и доступность старым пользователям.
- Покупка модели NetMind подтверждена, но не подтверждено, предлагает ли NetMind эту модель новым пользователям сегодня.

## Sources

| source | title | read |
|---|---|---|
| https://haiper.ai/ | Haiper - AI Video Generator | 2026-09-04 |
| https://apps.apple.com/app/id6468952574 | Apple App Store URL, app id 6468952574 | 2026-09-04 |
| https://techcrunch.com/2024/03/05/competition-in-ai-video-generation-heats-up-as-deepmind-alums-unveil-haiper/ | Competition in AI video generation heats up as DeepMind alums unveil Haiper | 2026-09-04 |
| https://testapp.haiper.ai/home | Unlock Creativity with AI Content Generator Tools | Haiper | 2026-09-04 |
| https://testapp2.haiper.ai/blog/haiper-partners-with-veed | Haiper Launches Its 2.5 Model-Powered API with VEED | 2026-09-04 |
| https://sifted.eu/articles/microsoft-haiper-ai-hires-video-sora-inflection/ | Exclusive: Microsoft scoops up talent from AI video startup Haiper | 2026-09-04 |
| https://sifted.eu/articles/haiper-ai-sold-for-parts | Exclusive: Haiper AI sold for parts after Microsoft poaches cofounders | 2026-09-04 |
| https://uk.trustpilot.com/review/haiper.ai | Haiper Reviews | Read Customer Service Reviews of haiper.ai | 2026-09-04 |
| https://docs.haiper.ai/llms.txt | Haiper documentation index | 2026-09-04 |
| https://docs.haiper.ai/pricing | Pricing for Haiper Web App & iOS App - Haiper | 2026-09-04 |
| https://docs.haiper.ai/api-reference/authentication | Authentication - Haiper | 2026-09-04 |
| https://docs.haiper.ai/api-reference/endpoint/2-0-text-to-video | Text to Video - Haiper | 2026-09-04 |
| https://docs.haiper.ai/api-reference/endpoint/get-creation-status | Get Creation Status - Haiper | 2026-09-04 |
| https://docs.haiper.ai/api-reference/endpoint/get-creation-detail | Get Creation Detail - Haiper | 2026-09-04 |
| https://docs.haiper.ai/api-reference/rate-limits | Rate Limits - Haiper | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:haiper`, thread `public-launch-and-ios-availability`, 2 dated events 2024-03-13 → 2024-03-16.
- **Practical note:** From 2024-03-16, practitioners should treat Haiper as having a publicly referenced web presence and an iOS distribution path, while verifying current availability and capabilities directly before relying on either.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
