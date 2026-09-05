---
title: Stable Diffusion 3
category: projects
date: 2024-02-22
tags: [project, stable-diffusion-3]
aliases: ["Stable Diffusion 3", "Stable Diffusion 3 Medium"]
---

# Stable Diffusion 3

**Development line:** `project:stable-diffusion-3` · thread `stable-diffusion-3`  
**Last event:** 2024-02-22 · 1 dated since 2024-02-22 · **Researched:** 2026-09-04 · confidence: high

## What it is

Stable Diffusion 3 — семейство MMDiT text-to-image моделей Stability AI для ComfyUI, Diffusers и API. Возможности: генерация по тексту, сложные композиции, типографика, image-to-image через поддерживающие пайплайны. SD3 Medium — 2B-параметровая, gated-модель; для организаций с коммерческим применением и годовой выручкой выше $1M нужна Enterprise-лицензия. Вердикт: SD3 Medium доступна, но сама Stability AI признала, что первый открытый релиз серии не оправдал ожиданий, и выпустила SD 3.5 как заменяющую линию.

## Development line

- **2024-02-22 — Stability AI announced Stable Diffusion 3.** Заявлена линейка 0.8B–8B с diffusion transformer и flow matching.

## What changed

2024-02-22 — Stability AI открыла early-preview waitlist для Stable Diffusion 3: заявлена линейка 0.8B–8B с diffusion transformer и flow matching. 2024-06-03 — Сохранённая ссылка ведёт на недоступную short-ссылку Reddit; проверяемого изменения модели по ней установить нельзя. 2024-06-12 — вышли открытые веса Stable Diffusion 3 Medium, 2B-параметровой модели. 2024-10-22 — вышли Stable Diffusion 3.5 Large и 3.5 Large Turbo; компания прямо указала, что июньский SD3 Medium не соответствовал её ожиданиям. 2024-10-29 — в линейку добавилась Stable Diffusion 3.5 Medium.

## How to use this

From 2024-02-22, practitioners should treat Stable Diffusion 3 as an officially announced project and follow its official news and project pages for verified updates.

1. Создайте аккаунт Hugging Face, примите условия доступа к gated-репозиторию и скачайте веса SD3 Medium либо совместимую Diffusers-версию.
  — <https://huggingface.co/stabilityai/stable-diffusion-3-medium>
2. Для локального запуска в ComfyUI используйте приложенные официальные workflow; если выбрана раздельная поставка весов, положите все три текстовых энкодера вместе с моделью.
  — <https://huggingface.co/stabilityai/stable-diffusion-3-medium>
3. Для Python обновите Diffusers, загрузите StableDiffusion3Pipeline с репозитория stable-diffusion-3-medium-diffusers и перенесите пайплайн на CUDA.
  — <https://huggingface.co/stabilityai/stable-diffusion-3-medium>
4. Перед коммерческим внедрением проверьте выручку организации: при коммерческом применении выше $1M в год требуется Enterprise License.
  — <https://stability.ai/license>

## Best practices

- Для повторяемых результатов передавайте torch.Generator с фиксированным seed; Diffusers использует его для детерминированной выборки латентов.
  — <https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/stable_diffusion_3>
- Не смешивайте пакеты весов: вариант без T5XXL требует отдельных энкодеров, а FP8-вариант T5XXL — компромисс между качеством и потреблением ресурсов.
  — <https://huggingface.co/stabilityai/stable-diffusion-3-medium>
- Для нового проекта сравните SD3 Medium с SD 3.5: SD 3.5 выпущена после признания недостатков первого открытого релиза SD3.
  — <https://stability.ai/news-updates/introducing-stable-diffusion-3-5>

## Superseded by this

- 2024-10-22: рекомендация начинать новый проект с SD3 Medium устарела для большинства задач; Stability AI представила SD 3.5 после того, как признала, что июньский открытый релиз не соответствовал ожиданиям.
- 2024-06-12: статус SD3 как preview/waitlist устарел после открытого выпуска весов SD3 Medium.

## Still unknown

- Short-ссылка Reddit из события 2024-06-03 вернула Internal Error, поэтому её исходный пост, автор и конкретное утверждение не верифицированы.
- В истории объединены Stable Diffusion 3 и Stable Diffusion 3 Medium; это одна продуктовая линия, но Medium является конкретным 2B-релизом, а не полным набором вариантов, анонсированных в феврале 2024 года.

## Sources

| source | title | read |
|---|---|---|
| https://stability.ai/news/stable-diffusion-3 | Stable Diffusion 3 — Stability AI | 2026-09-05 |
| https://www.reddit.com/r/StableDiffusion/s/xBOocPBskt | Reddit short link for the 2024-06-03 item | 2026-09-05 |
| https://stability.ai/news-updates/stable-diffusion-3-medium | Announcing the Open Release of Stable Diffusion 3 Medium | 2026-09-05 |
| https://huggingface.co/stabilityai/stable-diffusion-3-medium | stabilityai/stable-diffusion-3-medium — Hugging Face | 2026-09-05 |
| https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/stable_diffusion_3 | Stable Diffusion 3 pipeline — Diffusers documentation | 2026-09-05 |
| https://stability.ai/news-updates/introducing-stable-diffusion-3-5 | Introducing Stable Diffusion 3.5 — Stability AI | 2026-09-05 |
| https://stability.ai/license | Stability AI License | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:stable-diffusion-3`, thread `stable-diffusion-3`, 1 dated events 2024-02-22 → 2024-02-22.
- **Practical note:** From 2024-02-22, practitioners should treat Stable Diffusion 3 as an officially announced project and follow its official news and project pages for verified updates.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
