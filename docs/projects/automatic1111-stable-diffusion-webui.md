---
title: Stable Diffusion — Stable Diffusion development
category: projects
tags: [automatic1111-stable-diffusion-webui, dataset, project, stable-diffusion-development, stable_diffusion, stable_diffusion_v2_2_2_xl_beta]
aliases: ["Stable Diffusion", "Stable Diffusion 3"]
---

# Stable Diffusion — Stable Diffusion development

**Development line:** `project:automatic1111-stable-diffusion-webui` · thread `stable-diffusion-development`  
**Events:** 1 dated, 2022-07-26 → 2022-07-26 · **Researched:** 2026-09-04 · confidence: medium

## What it is

Stable Diffusion — семейство генеративных моделей изображений для художников и разработчиков, которым нужен выбор между self-hosting и API, а не только закрытый сервис вроде Midjourney. — text-to-image и image-to-image; — ControlNet для управления по Canny, depth или blur; — варианты Large, Turbo, Medium и Flash. Лимит: API SD 3.5 выдаёт 1 Мп изображения, по умолчанию 1024×1024; вход image-to-image — до 10 МиБ. Вердикт: для новых интеграций выбирайте SD 3.5, а не ранние SD3 или SDXL beta-идентификаторы.

## Development line

- **2022-07-26 — Stable Diffusion beta-access signup milestone.** On 2022-07-26, the sealed Stable Diffusion record linked to Stability AI's beta-signup form. This supports retaining a beta-access milestone, but it does not establish a released model version, eligibility, or feature set.

## What changed

2022-07-26 — регистрация в beta означала ограниченное тестирование, а не публичный выпуск весов; исследовательский доступ был объявлен 2022-08-10, публичный выпуск — 2022-08-22. 2023-03-09 — ссылка NeuralPic не указывает конкретный датасет, модель или релиз Stable Diffusion; изменение продукта не подтверждено. 2023-03-25 — запись `stable_diffusion_v2_2_2_xl_beta` не содержит URL, поэтому дату и характер изменения нельзя подтвердить. Найдено сегодня: 2023-04-13 официальный API добавил движок `stable-diffusion-xl-beta-v2-2-2` для SDXL beta и DreamStudio. 2024-03-07 — ссылка ведёт только на профиль X, поэтому конкретный пост не проверяем. Официальный статус SD3 в этот период: ранний preview/waitlist с вариантами от 800M до 8B параметров. 2024-03-13 — конкретный пост X недоступен для проверки; подтверждённого изменения модели или API из него нет. Найдено сегодня: 2024-06-12 вышел SD3 Medium для REST API и скачивания весов; 2024-10-22 появились SD 3.5 Large и Large Turbo, а 2024-10-29 — SD 3.5 Medium. Найдено сегодня: с 2025-04-17 API-идентификаторы SD3 автоматически перенаправляются на эквиваленты SD 3.5. В актуальном списке Core Models от 2026-05-20 остаются SD 3.5 Medium, Large и Large Turbo.

## How to use this

For the 2022-07-26 historical record, treat beta signup—not a confirmed public release—as the operational access route; confirm current availability and terms separately.

1. Выберите путь: API для управляемой интеграции или локальный запуск для контроля инфраструктуры; для качества на 1 Мп берите Large, для скорости — Large Turbo или Flash, для более экономного запуска — Medium.
  — <https://platform.stability.ai/docs/api-reference>
2. Для API создайте аккаунт и ключ, затем передавайте ключ только в заголовке Authorization.
  — <https://platform.stability.ai/docs>
3. Отправьте multipart POST на `/v2beta/stable-image/generate/sd3` с `prompt`, `model` и `output_format`; для image-to-image добавьте исходное изображение, `strength` и `mode=image-to-image`.
  — <https://platform.stability.ai/docs/api-reference>
4. Для локального запуска примите условия доступа к весам, установите `diffusers`, `transformers` и `accelerate`, загрузите `StableDiffusion3Pipeline` и сохраните результат генерации.
  — <https://huggingface.co/stabilityai/stable-diffusion-3.5-medium>
5. Если композицию нужно привязать к референсу, подключите SD3.5 Large ControlNet с Canny, depth или blur condition image.
  — <https://github.com/Stability-AI/sd3.5>

## Best practices

- Не храните и не коммитьте API-ключ: передавайте его в Authorization header и заменяйте при утечке.
  — <https://platform.stability.ai/docs>
- Для повторяемых сравнений задавайте явный seed: он управляет случайностью генерации.
  — <https://platform.stability.ai/docs/api-reference>
- Для SD 3.5 Medium не раздувайте prompt дальше 256 токенов T5: длинные запросы могут давать артефакты по краям; для структуры и анатомии используйте Skip Layer Guidance.
  — <https://huggingface.co/stabilityai/stable-diffusion-3.5-medium>
- При дефиците VRAM применяйте официально описанные 4-bit quantization и CPU offload вместо произвольной замены весов.
  — <https://huggingface.co/stabilityai/stable-diffusion-3.5-medium>
- До коммерческого self-hosting проверьте лицензию: Community License покрывает организации и людей с годовой выручкой ниже $1M, выше нужен Enterprise License.
  — <https://huggingface.co/stabilityai/stable-diffusion-3.5-medium>
- В продукте добавляйте собственные content-safety guardrails: фильтрация обучения не гарантирует отсутствие вредного результата.
  — <https://huggingface.co/stabilityai/stable-diffusion-3.5-medium>

## Superseded by this

- 2022-07-26: совет записываться в beta устарел после публичного выпуска Stable Diffusion 2022-08-22.
- 2023-04-13: ограничения и имя движка `stable-diffusion-xl-beta-v2-2-2` относятся к историческому SDXL beta, а не к рекомендуемому новому API-пути.
- 2024-02—03: рекомендации ждать SD3 early preview устарели после выпуска SD3 и SD 3.5.
- 2025-04-17: для официального API инструкции с `sd3-large`, `sd3-large-turbo` и `sd3-medium` устарели — вызовы автоматически перенаправляются на SD 3.5.

## Still unknown

- Содержимое регистрации beta 2022-07-26 недоступно; её значение как предварительного доступа выведено из последующих официальных объявлений.
- Ссылка NeuralPic от 2023-03-09 не связывает событие с конкретным датасетом, чекпойнтом или релизом Stable Diffusion.
- У записи 2023-03-25 нет URL: название похоже на последующий API engine SDXL beta, но не доказывает, что именно он был показан в эту дату.
- Ссылки X от 2024-03-07 и 2024-03-13 не отдали содержание, поэтому из них нельзя вывести изменение модели, лицензии или руководства компании.
- Линии `dataset`, `stable_diffusion` и `stable_diffusion_v2_2_2_xl_beta` могут объединять разные предметы: неподтверждённую ссылку на датасет, неофициальную beta-наводку и официальные релизы моделей.

## Sources

| source | title | read |
|---|---|---|
| https://stability.ai/beta-signup-form | Stability AI beta signup form — недоступна при чтении | 2026-09-04 |
| https://twitter.com/EMostaque | Emad Mostaque on X — недоступен при чтении | 2026-09-04 |
| https://twitter.com/EMostaque/status/1767662732797411433 | Emad Mostaque, post 1767662732797411433 — недоступен при чтении | 2026-09-04 |
| https://stability.ai/news-updates/stable-diffusion-launch-announcement | Stable Diffusion launch announcement | 2026-09-04 |
| https://stability.ai/news-updates/stable-diffusion-public-release | Stable Diffusion Public Release | 2026-09-04 |
| https://stability.ai/news-updates/stable-diffusion-xl-beta-available-for-api-customers-and-dreamstudio-users | Stable Diffusion XL Beta Available for API Customers and DreamStudio Users | 2026-09-04 |
| https://stability.ai/news-updates/stable-diffusion-3 | Stable Diffusion 3 | 2026-09-04 |
| https://platform.stability.ai/docs/release-notes | Stability AI Developer Platform release notes | 2026-09-04 |
| https://stability.ai/core-models | Stability AI Core Models | 2026-09-04 |
| https://platform.stability.ai/docs | Stability AI API: Getting Started | 2026-09-04 |
| https://platform.stability.ai/docs/api-reference | StabilityAI REST API (v2beta) | 2026-09-04 |
| https://huggingface.co/stabilityai/stable-diffusion-3.5-medium | stabilityai/stable-diffusion-3.5-medium model card | 2026-09-04 |
| https://github.com/Stability-AI/sd3.5 | Stability-AI/sd3.5 | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:automatic1111-stable-diffusion-webui`, thread `stable-diffusion-development`, 1 dated events 2022-07-26 → 2022-07-26.
- **Practical note:** For the 2022-07-26 historical record, treat beta signup—not a confirmed public release—as the operational access route; confirm current availability and terms separately.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
