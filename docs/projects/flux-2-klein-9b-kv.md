---
title: FLUX.2 [Klein] KV - 9B — Model release and local inference
category: projects
date: 2026-03-13
tags: [flux-2-klein-9b-kv, image_generation, model-release-and-local-inference, project]
aliases: ["FLUX.2 [Klein] KV - 9B"]
---

# FLUX.2 [Klein] KV - 9B — Model release and local inference

**Development line:** `project:flux-2-klein-9b-kv` · thread `model-release-and-local-inference`  
**Last event:** 2026-03-13 · 1 dated since 2026-03-13 · **Researched:** 2026-09-05 · confidence: medium

## What it is

FLUX.2 [klein] 9B-KV — 9B flow-модель для локального или API-редактирования, когда обычный FLUX.2 [klein] 9B тратит время на повторную обработку тех же референсов. — text-to-image; — редактирование одного изображения; — multi-reference editing с KV-кешем; — BF16 и официальный FP8-вариант, а также сторонние GGUF-квантизации. Мера: 9B flow model, 8B Qwen3 text embedder, 4 шага; официальный BF16-вариант требует около 29 GB VRAM и рассчитан на RTX 5090 или выше. Вывод: выбирайте его для итеративного multi-reference editing, а не ради ускорения чистого text-to-image.

## Development line

- **2026-03-13 — FLUX.2 Klein 9B KV model availability and local-use resources.** Нулевой шаг вычисляет K/V референсов, шаги 1–3 повторно используют кеш. Официальная карточка заявляет до 2.5× для multi-reference editing; более подробная таблица показывает зависимость от числа референсов и разрешения — от 1.21× до 2.66×.

## What changed

2026-01-15 — Black Forest Labs выпустила семейство FLUX.2 [klein]: 9B уже объединял text-to-image, single-reference и multi-reference editing в 4-шаговой distilled-модели. 2026-03-12 — официальный inference-репозиторий получил коммит «FLUX.2 [klein] KV»: отдельный путь кеширования референсов, выбор `flux.2-klein-9b-kv` в CLI и таблицу ускорений. 2026-03-13 — FLUX.2 [klein] 9B-KV вышел как точный 9B-вариант с кешированием K/V: нулевой шаг вычисляет K/V референсов, шаги 1–3 повторно используют кеш. Официальная карточка заявляет до 2.5× для multi-reference editing; более подробная таблица показывает зависимость от числа референсов и разрешения — от 1.21× до 2.66×.

## How to use this

From 2026-03-13, practitioners should evaluate this line through the linked Hugging Face checkpoint or demo, and use the linked GGUF and ComfyUI workflow resources when selecting a local inference path.

1. Примите условия gated-модели и FLUX Non-Commercial License, затем скачайте официальный BF16-чекпойнт либо FP8-вариант.
  — <https://huggingface.co/black-forest-labs/FLUX.2-klein-9b-kv>
2. Для локального Python-пути обновите Diffusers из GitHub, загрузите `Flux2KleinKVPipeline`, перенесите его на CUDA в bfloat16 и начните с 1024×1024 и 4 inference steps.
  — <https://huggingface.co/black-forest-labs/FLUX.2-klein-9b-kv>
3. Для официального CLI задайте `KLEIN_9B_KV_MODEL_PATH`, запустите `scripts/cli.py --model_name flux.2-klein-9b-kv`, укажите один или несколько `input_images`, затем текстовую инструкцию.
  — <https://github.com/black-forest-labs/flux2/blob/main/docs/flux2_klein_kv_cache.md>
4. Для ComfyUI с меньшим дисковым и VRAM-бюджетом можно взять сторонний GGUF, положить его в `ComfyUI/models/unet`, установить ComfyUI-GGUF и импортировать совместимый workflow; это community-путь, не официальный runtime BFL.
  — <https://huggingface.co/QuantStack/FLUX.2-Klein-9B-KV-GGUF>
5. Для облачного запуска используйте текущий `flux-2-klein-9b-preview` для последних KV-улучшений либо фиксированный `flux-2-klein-9b`, когда важна воспроизводимость; опрашивайте возвращённый `polling_url`.
  — <https://docs.bfl.ai/quick_start/generating_images>

## Best practices

- Рассчитывайте на ускорение только в image-conditioned задачах: кеш сохраняет K/V именно референсных изображений.
  — <https://github.com/black-forest-labs/flux2/blob/main/docs/flux2_klein_kv_cache.md>
- Проверяйте выигрыш на своём числе референсов и разрешении: официальная таблица даёт для четырёх референсов 2.66× при 512×512, но 1.85× при 1440×1440.
  — <https://github.com/black-forest-labs/flux2/blob/main/docs/flux2_klein_kv_cache.md>
- Пишите подробную описательную инструкцию: у FLUX.2 [klein] нет prompt upsampling, поэтому важные объекты, изменения и сохраняемые свойства надо назвать явно.
  — <https://docs.bfl.ai/flux_2/flux2_overview>
- Не переносите требование 13 GB VRAM от Klein 4B на 9B-KV: для официального 9B-KV указан ориентир около 29 GB VRAM.
  — <https://huggingface.co/black-forest-labs/FLUX.2-klein-9b-kv>
- Для стабильных production-результатов выбирайте непредпросмотровый API endpoint; preview предназначен для последних изменений весов.
  — <https://docs.bfl.ai/flux_2/flux2_overview>

## Superseded by this

- 2026-03-12 — ручная активация KV-кеша в официальном CLI не нужна: выбор `flux.2-klein-9b-kv` включает KV-путь автоматически.
- 2026-03-13 — для multi-reference editing обычный FLUX.2 [klein] 9B перестал быть предпочтительным low-latency выбором; 9B-KV сохраняет его возможности и устраняет повторную обработку референсов.
- 2026-09-05 — считать preview API-вариант воспроизводимым нельзя: текущая документация разделяет изменяемый `flux-2-klein-9b-preview` и фиксированный `flux-2-klein-9b`.

## Still unknown

- Независимый запуск не выполнялся: заявленные ускорения — официальные измерения, но карта не раскрывает полный benchmark-стенд и не заменяет замер на целевых референсах и разрешении.
- BF16, FP8 и GGUF — не взаимозаменяемые runtime-пути: GGUF-конверсия, ComfyUI-GGUF и YarvixPA workflow являются сторонней интеграцией и не имеют здесь независимого E2E-подтверждения.
- Китайский поиск дал вторичный ComfyUI-гайд, но не первичный источник; его рекомендации не повышены до официальной совместимости.
- Нет признака, что ссылки относятся к разным моделям: BF16 и FP8 — официальные варианты одного 9B-KV, а GGUF — прямое стороннее квантование этой же базы.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/black-forest-labs/FLUX.2-klein-9b-kv | black-forest-labs/FLUX.2-klein-9b-kv · Hugging Face | 2026-09-05 |
| https://huggingface.co/black-forest-labs/FLUX.2-klein-9b-kv-fp8 | black-forest-labs/FLUX.2-klein-9b-kv-fp8 · Hugging Face | 2026-09-05 |
| https://github.com/black-forest-labs/flux2/blob/main/docs/flux2_klein_kv_cache.md | FLUX.2 [klein] 9B KV Cache — official inference documentation | 2026-09-05 |
| https://github.com/black-forest-labs/flux2/commits/main/docs/flux2_klein_kv_cache.md | History for flux2_klein_kv_cache.md — commit “FLUX.2 [klein] KV”, 2026-03-12 | 2026-09-05 |
| https://bfl.ai/blog/flux2-klein-towards-interactive-visual-intelligence | FLUX.2 [klein]: Towards Interactive Visual Intelligence — Black Forest Labs, 2026-01-15 | 2026-09-05 |
| https://docs.bfl.ai/flux_2/flux2_overview | FLUX.2 Overview — Black Forest Labs documentation | 2026-09-05 |
| https://docs.bfl.ai/quick_start/generating_images | Image Generation with Text Prompts — Black Forest Labs documentation | 2026-09-05 |
| https://huggingface.co/QuantStack/FLUX.2-Klein-9B-KV-GGUF | QuantStack/FLUX.2-Klein-9B-KV-GGUF · Hugging Face | 2026-09-05 |
| https://github.com/YarvixPA/ComfyUI-YarvixPA/blob/main/example_workflows/YarvixPA%20-%20Flux2%209B%20KV%20-%20GGUF.json | YarvixPA — Flux2 9B KV GGUF workflow | 2026-09-05 |
| https://www.stablediffusiontutorials.com/2026/03/flux2-klein-9b-kv.html | Flux2 Klein 9B KV (BF16/FP8/GGUF): Improved Multi-Editing, 2026-03-13 | 2026-09-05 |
| https://www.runcomfy.com/zh-CN/comfyui-workflows/flux-2-klein-9b-kv-image-edit-in-comfyui-precision-prompt-editing | FLUX.2 Klein 9B KV ComfyUI image-edit guide, Simplified Chinese | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:flux-2-klein-9b-kv`, thread `model-release-and-local-inference`, 1 dated events 2026-03-13 → 2026-03-13.
- **Practical note:** From 2026-03-13, practitioners should evaluate this line through the linked Hugging Face checkpoint or demo, and use the linked GGUF and ComfyUI workflow resources when selecting a local inference path.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
