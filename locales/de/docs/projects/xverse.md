---
title: "XVerse — Публичные ресурсы и демо"
category: projects
date: 2025-11-12
tags: [project, public-resources-and-demo, xverse]
aliases: ["XVerse"]
level: 2
source_sha256: 25a6e07a1c4e062cc5ea0f1089979a1cc165f0c32957dc1a63182aa7585660a9
translation: machine
translated_at: '2026-10-24'
---
# XVerse — Публичные ресурсы и демо {#xverse-public-resources-and-demo}

**Линия разработки:** `project:xverse` · тред `public-resources-and-demo`  
**Последнее событие:** 2025-11-12 · 2 датированных с 2025-06-30 · **Проверено:** 2026-09-05 · достоверность: высокая

## Что это {#what-it-is}

XVerse — открытая реализация на базе FLUX.1-dev для художников и разработчиков, которым нужен управляемый text-to-image с одним или несколькими референсами. Возможности: раздельная идентичность субъектов; управление позой, стилем и освещением; локальный Gradio и CLI; XVerseBench. Ограничение: базовый режим требует 24 ГБ VRAM для двух условий, а режим с CPU offload — 16 ГБ для трёх, с заметной потерей скорости. Вердикт: применим локально для multi-subject personalization, но опубликованное веб-демо сейчас показывает runtime error.

## Линия разработки {#development-line}

- **2025-06-30 — публичные ресурсы XVerse были связаны.** Статья была опубликована 2025-06-26, а код — выпущен 2025-06-26; модель применяет token-specific text-stream modulation в DiT. Дополнение к событию: статья называет точный preprint arXiv:2506.21416 и авторов ByteDance; XVerseBench включает 20 человеческих идентичностей, 74 объекта, 45 животных и 300 тестовых промптов (страница проекта, без собственной даты публикации).
- **2025-11-12 — выделен Hugging Face Space XVerse.** Репозиторий датирует выпуск демо 2025-07-10. При проверке 2026-09-05 Space отдаёт runtime error, поэтому его нельзя считать доступным рабочим путём.

## Что изменилось {#what-changed}

2025-06-30 — публичный старт XVerse: статья была опубликована 2025-06-26, а код — выпущен 2025-06-26; модель применяет token-specific text-stream modulation в DiT. Дополнение к событию: статья называет точный preprint arXiv:2506.21416 и авторов ByteDance; XVerseBench включает 20 человеческих идентичностей, 74 объекта, 45 животных и 300 тестовых промптов (страница проекта, без собственной даты публикации). 2025-11-12 — ссылка вела на официальный Hugging Face Space, но это не обозначает новый релиз модели: репозиторий датирует выпуск демо 2025-07-10. При проверке 2026-09-05 Space отдаёт runtime error, поэтому его нельзя считать доступным рабочим путём.

Новые самостоятельные события: 2025-07-08 — добавлен low-VRAM inference, заявлен запуск с 24 ГБ VRAM; 2025-07-10 — выпущен Hugging Face Space; 2025-07-18 — добавлены квантизованные diffusion-модели и group offload с заявленным запуском от 16 ГБ VRAM; 2025-09-19 — работа принята на NeurIPS 2025. Все четыре даты опубликованы в журнале изменений официального репозитория.

## Как использовать {#how-to-use-this}

С 2025-06-30 практики могли найти официальный проект, код и ресурсы модели XVerse вместе; к 2025-11-12 им также следует проверять официальный Hugging Face Space как публичную интерактивную точку входа, при этом дату запуска или изменения Space считать неподтверждённой.

1. Клонировать репозиторий, создать окружение Python 3.10.16, установить зафиксированные PyTorch 2.6.0/CUDA 12.4, requirements, FlashAttention и httpx, затем скачать checkpoints и отдельно добавить model_ir_se50.pth.
  — <https://github.com/bytedance/XVerse>
2. Задать пути к Florence-2, SAM2, InsightFace, CLIP, FLUX.1-dev, DPG-VQA и DINO; запустить локальный интерфейс командой python run_gradio.py.
  — <https://github.com/bytedance/XVerse>
3. Для воспроизводимого запуска передать prompt, изображения, подписи и флаги idips в inference_single_sample.py; для нескольких референсов количества images, captions и idips должны совпадать.
  — <https://github.com/bytedance/XVerse>
4. При дефиците памяти включить use_low_vram либо use_lower_vram; для квантизованных FLUX использовать документированный bnb-nf4 или GGUF-путь и повторно подобрать веса.
  — <https://github.com/bytedance/XVerse>

## Лучшие практики {#best-practices}

- Включайте в основной prompt точное описание каждого активного референса либо используйте ENT1/ENT2: без него генерация завершается ошибкой.
  — <https://github.com/bytedance/XVerse>
- Не включайте CPU offload без необходимости: документация прямо предупреждает о существенном снижении скорости.
  — <https://github.com/bytedance/XVerse>
- После перехода на квантизованный FLUX заново подберите weight_id, weight_ip и LoRA scales: квантизация может ухудшить результат.
  — <https://github.com/bytedance/XVerse>
- Для оценки изменений запускайте прилагаемый скрипт XVerseBench; он сохраняет результаты в results.
  — <https://github.com/bytedance/XVerse>

## Что заменено этим {#superseded-by-this}

- 2025-07-08: прежнее требование полноценного режима с большим объёмом памяти частично заменено режимом low-VRAM на 24 ГБ для до двух условий.
- 2025-07-18: low-VRAM guidance от 2025-07-08 расширена квантизацией и group offload; заявленный минимум стал 16 ГБ VRAM для до трёх условий.
- 2026-09-05: рекомендация использовать официальный Space как рабочий путь устарела до восстановления сервиса: страница показывает runtime error; локальный запуск остаётся документированным путём.

## Что остаётся неизвестным {#still-unknown}

- Официальный README отмечает ComfyUI implementation и Benchmark Leaderboard как невыпущенные; отдельного поддерживаемого ComfyUI-пути подтверждать нельзя.
- Hugging Face Space в предоставленном событии 2025-11-12 не содержит собственного датированного changelog, поэтому нельзя надёжно установить, что именно изменилось в этот день, помимо наличия ссылки на демо.
- Название XVerse также используется несвязанной организацией xverse для языковых моделей; в этой истории речь идёт только о ByteDance XVerse для генерации изображений.

## Источники {#sources}

| source | title | read |
|---|---|---|
| https://bytedance.github.io/XVerse/ | XVerse: Consistent Multi-Subject Control of Identity and Semantic Attributes via DiT Modulation | 2026-09-05 |
| https://github.com/bytedance/XVerse | ByteDance/XVerse official implementation | 2026-09-05 |
| https://huggingface.co/ByteDance/XVerse/tree/main | ByteDance/XVerse model repository | 2026-09-05 |
| https://huggingface.co/spaces/ByteDance/XVerse | ByteDance XVerse Hugging Face Space | 2026-09-05 |
| https://arxiv.org/abs/2506.21416 | XVerse: Consistent Multi-Subject Control of Identity and Semantic Attributes via DiT Modulation | 2026-09-05 |
| https://raw.githubusercontent.com/bytedance/XVerse/main/README.md | XVerse README | 2026-09-05 |

## Краткая сводка для агента {#agent-brief}

- **Субъект:** `project:xverse`, тред `public-resources-and-demo`, 2 датированных события 2025-06-30 → 2025-11-12.
- **Практическая заметка:** С 2025-06-30 практики могли найти официальный проект, код и ресурсы модели XVerse вместе; к 2025-11-12 им также следует проверять официальный Hugging Face Space как публичную интерактивную точку входа, при этом дату запуска или изменения Space считать неподтверждённой.
- **Достоверность:** высокая. Датированные замены выше являются источником истины о том, что устарело.
