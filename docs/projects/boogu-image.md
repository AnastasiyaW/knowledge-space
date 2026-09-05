---
title: Boogu-Image
category: projects
date: 2026-06-18
tags: [boogu-image, boogu-image-development, boogu_image, project]
aliases: ["Boogu-Image"]
---

# Boogu-Image

**Development line:** `project:boogu-image` · thread `boogu-image-development`  
**Last event:** 2026-06-18 · 1 dated since 2026-06-18 · **Researched:** 2026-09-05 · confidence: medium

## What it is

Boogu-Image — исследовательское семейство открытых checkpoint’ов для команд, которым нужен локальный аналог связки Qwen-Image и ComfyUI. — Base: text-to-image, плотная китайская и английская типографика, дообучение. — Turbo: text-to-image за 3–4 шага, в первую очередь фотореализм. — Edit и Edit-Turbo: редактирование по текстовой инструкции. Мера: основные варианты имеют 10B параметров; Base/Edit заявлены для 1K, 1.5K и 2K, Turbo — для 1K. Вердикт: подходит для исследовательской и локальной интеграции, но не как готовый платный API или production-сервис без собственных защит и валидации.

## Development line

- **2026-06-18 — Boogu-Image public project resources were linked.** Отдельного официального релиза на эту дату не найдено; публичные точки входа уже вели к семейству 0.1, коду, весам и демо.

## What changed

2026-06-16: вышли Boogu-Image-0.1-Base, -Edit и четырёхшаговый -Turbo. 2026-06-17: появился ComfyUI-Boogu; позднее этот путь стал legacy после нативной поддержки в ComfyUI. 2026-06-18: отдельного официального релиза на эту дату не найдено; публичные точки входа уже вели к семейству 0.1, коду, весам и демо. 2026-06-25: Turbo получил hotfix-20260625 для артефактов разных соотношений сторон и фоновых артефактов без новых функций. 2026-06-30: вышел четырёхшаговый image-to-image вариант Edit-Turbo. 2026-07-08: Edit-Turbo получил hotfix для деградации качества и слабого удаления объектов; рекомендован revision 1K. 2026-07-16: опубликован технический отчёт Boogu-Image-0.1. 2026-07-22: добавлен путь online serving через vLLM-Omni. 2026-07-23: в ветке npu появился начальный backend для NPU.

## How to use this

As of 2026-06-18, practitioners should use the linked project site, repository, Hugging Face organization, demos, and gallery as the initial entry points for evaluating Boogu-Image.

1. Выбрать Base для плотного текста, controllability и 2K; Turbo — для быстрых фотореалистичных T2I; Edit или Edit-Turbo — для редактирования изображения по инструкции.
  — <https://raw.githubusercontent.com/Boogu-Project/Boogu-Image/main/README.md>
2. Создать чистое окружение Python 3.10 с совместимыми PyTorch/CUDA, установить зависимости проекта и скачать нужный checkpoint в локальный каталог models/ через Hugging Face CLI.
  — <https://raw.githubusercontent.com/Boogu-Project/Boogu-Image/main/README.md>
3. Для локального T2I задать одинаковый device в переменной окружения и аргументе CLI, затем запустить inference.py с путём к Base или Turbo, инструкцией и output_image_path.
  — <https://raw.githubusercontent.com/Boogu-Project/Boogu-Image/main/INFERENCE_GUIDE.md>
4. Для редактирования использовать Edit-совместимый checkpoint и передать входное изображение вместе с текстовой инструкцией; для переносимого workflow считать один референс текущим безопасным пределом.
  — <https://raw.githubusercontent.com/vllm-project/vllm-omni/main/recipes/Boogu/Boogu-Image.md>
5. В ComfyUI обновить основную установку, скачать repackaged-файлы Comfy-Org и собрать workflow из стандартных Load Diffusion Model, Load CLIP с type boogu, Load VAE и TextEncodeBooguEdit для editing.
  — <https://raw.githubusercontent.com/boogu-project/ComfyUI-Boogu/main/README.md>
6. Для API-сервинга запустить vLLM-Omni с --omni на Base или Edit и проверить ответ фиксированным seed; документированный старт для Base — одна A100/H100 с 40GB+ VRAM.
  — <https://raw.githubusercontent.com/vllm-project/vllm-omni/main/recipes/Boogu/Boogu-Image.md>

## Best practices

- Не ставить legacy ComfyUI-Boogu без специальной причины: текущая инструкция рекомендует нативные узлы ComfyUI и repackaged-модели.
  — <https://raw.githubusercontent.com/boogu-project/ComfyUI-Boogu/main/README.md>
- Для плотной двуязычной типографики начинать с Base на 2K; для фотореалистичного T2I по умолчанию выбирать Turbo.
  — <https://raw.githubusercontent.com/Boogu-Project/Boogu-Image/main/README.md>
- Для Edit-Turbo использовать hotfix-1k-20260708, а не исходный checkpoint: авторы называют 1K более стабильным.
  — <https://raw.githubusercontent.com/Boogu-Project/Boogu-Image/main/README.md>
- Начинать с default pipeline: prompt-tuning помечен как необязательный исследовательский путь и менее устойчивый, чем обычный запуск.
  — <https://raw.githubusercontent.com/Boogu-Project/Boogu-Image/main/INFERENCE_GUIDE.md>
- Не включать несколько offload-режимов одновременно; сначала добиться стабильного запуска без cache-ускорения, а torch.compile отключить при чёрных кадрах.
  — <https://raw.githubusercontent.com/Boogu-Project/Boogu-Image/main/INFERENCE_GUIDE.md>
- Не использовать без собственных moderation, validation и compliance-проверок в production: проект прямо ограничивает релиз исследовательским назначением.
  — <https://raw.githubusercontent.com/Boogu-Project/Boogu-Image/main/README.md>

## Superseded by this

- 2026-06-18: трактовка этой даты как даты запуска устарела — официальный журнал датирует Base, Edit и Turbo 2026-06-16.
- 2026-06-25: исходный Turbo следует заменить на revision hotfix-20260625 при проблемах с артефактами соотношений сторон и фона.
- 2026-07-08: исходный Edit-Turbo следует заменить на hotfix-1k-20260708; 1.5K hotfix существует, но 1K рекомендован как более стабильный.
- 2026-06-17: установка legacy custom node ComfyUI-Boogu больше не является рекомендуемым путём; актуален native ComfyUI workflow.

## Still unknown

- Официальный README одновременно публикует код и веса Apache-2.0 и называет Boogu-Image-0.1 research project rather than an official model release; практический смысл формулировки для коммерческого использования не разъяснён.
- Официальная посадочная страница описывает Boogu-Image-0.1-Pro как пятый вариант, но в проверенном списке моделей Hugging Face не найден отдельный checkpoint или датированное объявление Pro.
- Документация расходится по числу reference images: ранняя release note и vLLM recipe фиксируют один, тогда как общий inference guide описывает несколько путей; до отдельного воспроизводимого теста один референс — безопасный переносимый лимит.
- Проверены первичные документы, но независимая репликация заявленных arena и benchmark-результатов не проводилась.
- Данные не указывают на два разных проекта под именем Boogu-Image: ссылки и текущие официальные поверхности ведут к одному семейству 0.1.

## Sources

| source | title | read |
|---|---|---|
| https://boogu.org/ | Boogu-Image-0.1 — official project page | 2026-09-05 |
| https://github.com/boogu-project/Boogu-Image | boogu-project/Boogu-Image | 2026-09-05 |
| https://raw.githubusercontent.com/Boogu-Project/Boogu-Image/main/README.md | Boogu-Image README | 2026-09-05 |
| https://huggingface.co/Boogu | Boogu on Hugging Face | 2026-09-05 |
| https://huggingface.co/Boogu/Boogu-Image-0.1-Edit-Turbo/tree/hotfix-1k-20260708 | Boogu-Image-0.1-Edit-Turbo hotfix-1k-20260708 | 2026-09-05 |
| https://raw.githubusercontent.com/Boogu-Project/Boogu-Image/main/INFERENCE_GUIDE.md | Boogu Inference Guide | 2026-09-05 |
| https://raw.githubusercontent.com/boogu-project/ComfyUI-Boogu/main/README.md | ComfyUI-Boogu README | 2026-09-05 |
| https://raw.githubusercontent.com/vllm-project/vllm-omni/main/recipes/Boogu/Boogu-Image.md | vLLM-Omni Boogu-Image recipe | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:boogu-image`, thread `boogu-image-development`, 1 dated events 2026-06-18 → 2026-06-18.
- **Practical note:** As of 2026-06-18, practitioners should use the linked project site, repository, Hugging Face organization, demos, and gallery as the initial entry points for evaluating Boogu-Image.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
