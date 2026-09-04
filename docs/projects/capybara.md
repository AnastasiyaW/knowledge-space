---
title: Capybara — Capybara development
category: projects
tags: [capybara, capybara-development, project]
aliases: ["CAPYBARA", "Capybara"]
---

# Capybara — Capybara development

**Development line:** `project:capybara` · thread `capybara-development`  
**Events:** 2 dated, 2026-02-17 → 2026-02-24 · **Researched:** 2026-09-04 · confidence: medium

## What it is

Capybara — open-source инференс-пайплайн для автора, которому нужны генерация и instruction-based редактирование в одном интерфейсе. — text-to-image (T2I) и text-to-video (T2V); — instruction-based image-to-image (TI2I) и video-to-video (TV2V); — одиночные запуски, CSV-пакеты, distributed inference через Accelerate и узлы ComfyUI. Ограничение: документация рекомендует Python 3.11 и CUDA 12.6; FP8 требует NVIDIA Ada/Hopper с compute capability не ниже 8.9 и torchao. Вердикт: это пригодная для локального инференса интеграция, но не документированная production- или training-платформа.

## Development line

- **2026-02-17 — Capybara source, model, and demo resources were linked.** On 2026-02-17, the dated resource set linked Capybara’s source repository and model page together with a Qwen3-VL model and a hosted endpoint. This is material as an early public-facing development step for Capybara, although the sealed links alone do not establish the exact capability, release status, or relationship of each linked resource.
- **2026-02-24 — Capybara documentation surfaced ComfyUI and FP8 workflows.** On 2026-02-24, the dated links pointed to Capybara documentation covering ComfyUI support, FP8 quantization, and a sample workflow. This is material because it marks a practical integration and deployment path, while the sealed evidence does not prove whether those capabilities were newly released on that date.

## What changed

Capybara — 2026-02-17: вышел v0.1 inference framework с T2I, T2V, TI2I и TV2V. 2026-02-24: в документации зафиксирован путь через custom nodes ComfyUI, FP8 и пример workflow; официальный README датирует появление этих возможностей 2026-02-20, поэтому это дата изменения кода, а 2026-02-24 — дата зафиксированного события. Найдено сегодня, 2026-09-04: текущий first-party README по-прежнему содержит только эти две датированные строки, отмечает ComfyUI как выполненное и оставляет release unified creation model и training code в TODO.

## How to use this

After 2026-02-24, practitioners evaluating Capybara should consult its ComfyUI documentation, sample workflow, and FP8 guidance rather than relying only on the base repository or model page.

1. Создайте изолированное окружение Python 3.11, установите PyTorch для CUDA 12.6 и зависимости проекта.
  — <https://github.com/xgen-universe/Capybara>
2. Скачайте все обязательные компоненты checkpoint в структуру ckpts/; Qwen3-VL-8B-Instruct нужен только при включённом переписывании инструкции.
  — <https://github.com/xgen-universe/Capybara>
3. Для первого прогона вызовите inference.py с task_type t2i или t2v; для ti2i и tv2v добавьте media_path и текстовую инструкцию.
  — <https://github.com/xgen-universe/Capybara>
4. Для серии задач подготовьте CSV с img_path либо video_path и instruction, затем передайте csv_path и data_root_path.
  — <https://github.com/xgen-universe/Capybara>
5. Для ComfyUI подключите корень Capybara в custom_nodes и запускайте ComfyUI в том же окружении capybara.
  — <https://github.com/xgen-universe/Capybara/blob/main/comfyui/README.md>
6. Загрузите sample_workflow.json в canvas ComfyUI, затем смените task_type и вход reference под T2I, T2V, TI2I или TV2V.
  — <https://github.com/xgen-universe/Capybara/blob/main/comfyui/examples/sample_workflow.json>

## Best practices

- Начинайте с официального базового режима: 480p и 50 шагов для видео, 720p и 50 шагов для изображений; повышайте разрешение только после рабочего baseline.
  — <https://github.com/xgen-universe/Capybara>
- В ComfyUI для TI2I и TV2V задавайте кадр или видео через reference: aspect ratio выводится из reference, а guidance_scale внутри узла фиксирован на 1.0.
  — <https://github.com/xgen-universe/Capybara/blob/main/comfyui/README.md>
- Включайте FP8 только на Ada/Hopper с torchao: это примерно вдвое сокращает память весов transformer, но не обещает ускорения и закрепляет transformer в GPU-памяти.
  — <https://github.com/xgen-universe/Capybara/blob/main/comfyui/README.md>
- Не смешивайте Python-окружения Capybara и ComfyUI: документация требует запускать ComfyUI из того же окружения, чтобы custom nodes видели зависимости.
  — <https://github.com/xgen-universe/Capybara/blob/main/comfyui/README.md>
- Перед скачиванием зафиксируйте разрешившийся model repository и revision: официальная ссылка xgen-universe сейчас перенаправляет на Glanty/Capybara.
  — <https://huggingface.co/xgen-universe/Capybara>

## Superseded by this

- 2026-02-20: прежний TODO «Add support for ComfyUI» устарел; Capybara имеет custom nodes и sample workflow. Нативный CLI при этом остаётся поддерживаемым путём, а не заменённым.

## Still unknown

- Официальные материалы не объясняют, означает ли перенаправление Hugging Face с xgen-universe/Capybara на Glanty/Capybara перенос владения, зеркало или ошибку; перед применением нужно проверить конкретные файлы и revision.
- First-party документация не даёт таблицы VRAM, независимых бенчмарков или доказательства production-готовности; также training code остаётся не выпущенным.
- Временный demo URL на ngrok из события 2026-02-17 не удалось безопасно открыть, поэтому его текущая доступность не подтверждена.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/xgen-universe/Capybara | xgen-universe/Capybara — repository README | 2026-09-04 |
| https://raw.githubusercontent.com/xgen-universe/Capybara/main/README.md | Capybara — main README, raw source | 2026-09-04 |
| https://huggingface.co/xgen-universe/Capybara | xgen-universe/Capybara — Hugging Face model page, redirected to Glanty/Capybara | 2026-09-04 |
| https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct | Qwen3-VL-8B-Instruct — Hugging Face model card | 2026-09-04 |
| https://github.com/xgen-universe/Capybara/blob/main/comfyui/README.md | Capybara ComfyUI Custom Nodes | 2026-09-04 |
| https://raw.githubusercontent.com/xgen-universe/Capybara/main/comfyui/README.md | Capybara ComfyUI Custom Nodes — raw source | 2026-09-04 |
| https://github.com/xgen-universe/Capybara/blob/main/comfyui/examples/sample_workflow.json | Capybara ComfyUI sample workflow | 2026-09-04 |
| https://raw.githubusercontent.com/xgen-universe/Capybara/main/comfyui/examples/sample_workflow.json | Capybara ComfyUI sample workflow — raw source | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:capybara`, thread `capybara-development`, 2 dated events 2026-02-17 → 2026-02-24.
- **Practical note:** After 2026-02-24, practitioners evaluating Capybara should consult its ComfyUI documentation, sample workflow, and FP8 guidance rather than relying only on the base repository or model page.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
