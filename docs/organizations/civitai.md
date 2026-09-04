---
title: Civitai — Civitai platform, business, and access evolution
category: organizations
tags: [civitai, civitai-clubs, civitai_monetization, organization, platform-business-and-access-evolution, platform_policy]
aliases: ["Civitai"]
---

# Civitai — Civitai platform, business, and access evolution

**Development line:** `organization:civitai` · thread `platform-business-and-access-evolution`  
**Events:** 5 dated, 2023-10-17 → 2026-04-13 · **Researched:** 2026-09-03 · confidence: medium

## What it is

Civitai — платформа Civit AI, Inc. для авторов и пользователей image-AI, где ищут, публикуют и генерируют с пользовательскими моделями и медиа; по роли это каталог моделей рядом с Hugging Face, но с лентой, генератором и Creator Studio. - Каталог: модели, изображения, видео и 3D-ресурсы. - Работа: загрузка и поиск моделей, публикация медиа, генерация на площадке. - Монетизация: Buzz, paid/early access, licensing fees и Creator Program. Ограничение: доступ 18+; Великобритания заблокирована, а SFW и полный каталог разделены между .com и .red. Вердикт: годится как витрина и рабочая площадка для image-AI, если заранее выбрать домен, проверить политику и не строить автоматизацию на скрейпинге.

## Development line

- **2023-10-17 — Civitai records a monetization-related platform development.** On 2023-10-17, Civitai recorded a development associated with monetization. No source URL or source text was extracted for this member, so the specific mechanism and its effect cannot be stated from the sealed evidence alone.
- **2024-01-06 — Civitai seeks feedback on Clubs and community sustainability.** On 2024-01-06, Civitai published material about Clubs and requested feedback on sustainable community development. The linked Civitai education material indicates that Clubs were part of the platform's community structure, although the sealed links alone do not establish the final policy or rollout details.
- **2025-04-25 — Civitai enforcement changes are reported by its user community.** On 2025-04-25, a Stable Diffusion community post discussed Civitai tightening enforcement. The sealed evidence contains only that third-party link, so the underlying policy, its rationale, and whether the account was accurate require primary-source research before this can be treated as a fully verified public fact.
- **2025-07-21 — Civitai’s planned restriction of UK access is reported.** On 2025-07-21, a Stable Diffusion community post reported that Civitai intended to block UK users in the following week. The supplied link alone does not confirm that the restriction took effect, its scope, or its basis; those points need first-party confirmation.
- **2026-04-13 — Civitai outlines separate .com and .red entry points.** On 2026-04-13, Civitai published an article describing Civitai.com and Civitai.red as two access points and indicating a forthcoming direction for them. The link establishes the existence of that first-party announcement, but the sealed evidence does not provide enough detail to state the operational distinction or user impact.

## What changed

2023-10-17 — Buzz и Bounties ввели внутреннюю экономику: Buzz можно было получать или покупать и тратить на tips, Bounties и обучение LoRA. 2024-01-06 — Clubs предложили как creator memberships; 2024-01-10 их отключили, пообещав переработку в пользовательские разделы и возврат потраченного Buzz. 2025-04-25 — вслед за обновлением policy 2025-04-23 запретили новые категории контента; X/XXX-uploads обязали снабжать generation metadata, а real-person content ограничили в лентах и монетизации. 2025-07-21 — предупреждение стало фактической региональной блокировкой: с 2025-07-24 Civitai недоступен в Англии, Шотландии, Уэльсе и Северной Ирландии из-за Online Safety Act. 2026-04-13 — источник от 2026-04-09, обновлённый 2026-04-16, разделил входы: .com — SFW, карты, memberships и Creator Program; .red — полный каталог, NSFW и crypto. Аккаунт, загрузки и follows общие. Найдено сегодня, 2026-09-03: текущий Creator Program работает через Creator Studio; cash-out требует Creator Score выше 10k и Civitai Green membership.

## How to use this

From 2026-04-13, practitioners should verify which Civitai entry point and applicable platform rules govern their region and workflow before relying on hosted models, Clubs, or account access; the earlier 2024-01-06 and 2025 reports indicate that community and enforcement conditions may change.

1. Проверьте доступ: сервис только для 18+, а для большинства функций нужен зарегистрированный аккаунт.
  — <https://civitai.red/content/tos>
2. Выберите домен до поиска: .com для SFW и card/membership-функций, .red для полного каталога и mature content; одного аккаунта достаточно для обоих доменов.
  — <https://civitai.red/articles/28369/two-front-doors-civitaicom-civitaired-and-whats-next>
3. В каталоге моделей отфильтруйте ресурс по типу и базовому семейству, затем сверьте его с вашим workflow до скачивания или запуска генерации.
  — <https://civitai.red/models>
4. Для загрузки моделей и коммерческих настроек используйте Creator Studio: там задаются paid access, early access и licensing fees; в Creator Program вступайте только после проверки eligibility.
  — <https://civitai.red/creator-program>
5. Перед публикацией или on-site generation проверьте safety rules; для sexualized X/XXX-контента добавьте generation metadata, минимум prompt.
  — <https://civitai.red/articles/13632/policy-and-content-adjustments>
6. Для программного доступа используйте только официальный API или MCP со своими валидными credentials и в рамках rate limits.
  — <https://civitai.red/content/tos>

## Best practices

- Разделяйте ссылки по назначению: mature/NSFW-ресурсы сохраняйте на .red; .com теперь SFW-представление и такие объекты там не покажет.
  — <https://civitai.red/articles/28369/two-front-doors-civitaicom-civitaired-and-whats-next>
- Храните локальную копию своих важных загрузок до policy-review: нарушающие новые правила объекты сначала скрываются, затем могут быть удалены после grace period.
  — <https://civitai.red/articles/13632/policy-and-content-adjustments>
- При публикации точно маркируйте контент, не используйте likeness реальных людей или запрещённые категории и сообщайте о нарушениях через штатный report flow.
  — <https://civitai.red/safety>
- Не заменяйте официальный API/MCP скрейпером: условия разрешают автоматизированный доступ только через предоставленные интерфейсы, с credentials и rate limits.
  — <https://civitai.red/content/tos>
- Не считайте получение Buzz гарантией cash-out: заранее проверьте лимит своего membership tier и порог Creator Score/Green membership для программы выплат.
  — <https://civitai.red/creator-program>

## Superseded by this

- 2024-01-06: Clubs как действующий способ закрытых creator memberships — obsolete; функция была отключена 2024-01-10.
- До 2025-04-23: совет публиковать X/XXX без generation metadata — obsolete; такой контент теперь скрывается до добавления минимум prompt.
- До 2025-07-24: совет использовать Civitai из Великобритании без проверки доступности — obsolete; страна заблокирована из-за Online Safety Act.
- До 2026-04-16: совет вести полный каталог и NSFW-ссылки на civitai.com — obsolete; .com стал SFW-входом, полный каталог находится на .red.
- До 2026-04-16: совет считать все типы Buzz взаимозаменяемыми между доменами — obsolete; Green и Yellow Buzz разделены, тогда как Blue имеет отдельные условия использования.

## Still unknown

- Детали 2024 Clubs подтверждены доступной community-транскрипцией сообщения Civitai: исходные Civitai-страницы из события не открылись, поэтому этот отрезок не имеет доступного первичного текста в данной проверке.
- У найденных текущих материалов Civitai нет первичного китайскоязычного аналога; китайские зеркала и агрегаторы исключены, поэтому zh-CN coverage остаётся пробелом.
- Clubs и нынешний Creator Program относятся к монетизации, но найденные материалы не доказывают прямую продуктовую преемственность между ними.
- Совместимость конкретной модели с ComfyUI, A1111 или другим локальным workflow проверяется на странице её версии; универсального практического рецепта установки Civitai не публикует в использованных источниках.

## Sources

| source | title | read |
|---|---|---|
| https://medium.com/civitai/introducing-buzz-bounties-a-rewards-system-for-generative-ai-builders-dcdde9c2b044 | Introducing Buzz & Bounties, a Rewards System for Generative AI Builders | 2026-09-03 |
| https://www.reddit.com/r/StableDiffusion/comments/192ye95 | Civitai Clubs temporarily disabled | 2026-09-03 |
| https://civitai.red/articles/13632/policy-and-content-adjustments | Policy & Content Adjustments | 2026-09-03 |
| https://civitai.red/region-blocked | Access Restricted for UK Visitors | 2026-09-03 |
| https://civitai.red/articles/28369/two-front-doors-civitaicom-civitaired-and-whats-next | Two Front Doors: Civitai.com, Civitai.red, and What's Next | 2026-09-03 |
| https://civitai.red/content/tos | Terms of Service | 2026-09-03 |
| https://civitai.red/safety | Safety Center | Policies and Guidelines | 2026-09-03 |
| https://civitai.red/models | AI Models | Civitai | 2026-09-03 |
| https://civitai.red/creator-program | Earn on Civitai | 2026-09-03 |

## Agent brief {#agent-brief}

- **Subject:** `organization:civitai`, thread `platform-business-and-access-evolution`, 5 dated events 2023-10-17 → 2026-04-13.
- **Practical note:** From 2026-04-13, practitioners should verify which Civitai entry point and applicable platform rules govern their region and workflow before relying on hosted models, Clubs, or account access; the earlier 2024-01-06 and 2025 reports indicate that community and enforcement conditions may change.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
