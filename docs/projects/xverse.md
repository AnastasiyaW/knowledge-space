---
title: XVerse — Public resources and demo
category: projects
date: 2025-11-12
tags: [project, public-resources-and-demo, xverse]
aliases: ["XVerse"]
---

# XVerse — Public resources and demo

**Development line:** `project:xverse` · thread `public-resources-and-demo`  
**Last event:** 2025-11-12 · 2 dated since 2025-06-30 · **Researched:** 2026-09-05 · confidence: high

## What it is

XVerse — открытая реализация на базе FLUX.1-dev для художников и разработчиков, которым нужен управляемый text-to-image с одним или несколькими референсами. Возможности: раздельная идентичность субъектов; управление позой, стилем и освещением; локальный Gradio и CLI; XVerseBench. Предел: базовый режим требует 24 ГБ VRAM для двух условий, а режим с CPU offload — 16 ГБ для трёх, с заметной потерей скорости. Вердикт: применим локально для multi-subject personalization, но опубликованное веб-демо сейчас показывает runtime error.

## Development line

- **2025-06-30 — XVerse public resources were linked.** Статья была опубликована 2025-06-26, а код — выпущен 2025-06-26; модель применяет token-specific text-stream modulation в DiT. Дополнение к событию: статья называет точный preprint arXiv:2506.21416 и авторов ByteDance; XVerseBench включает 20 человеческих идентичностей, 74 объекта, 45 животных и 300 тестовых промптов (страница проекта, без собственной даты публикации).
- **2025-11-12 — XVerse Hugging Face Space was highlighted.** Репозиторий датирует выпуск демо 2025-07-10. При проверке 2026-09-05 Space отдаёт runtime error, поэтому его нельзя считать доступным рабочим путём.

## What changed

2025-06-30 — публичный старт XVerse: статья была опубликована 2025-06-26, а код — выпущен 2025-06-26; модель применяет token-specific text-stream modulation в DiT. Дополнение к событию: статья называет точный preprint arXiv:2506.21416 и авторов ByteDance; XVerseBench включает 20 человеческих идентичностей, 74 объекта, 45 животных и 300 тестовых промптов (страница проекта, без собственной даты публикации). 2025-11-12 — ссылка вела на официальный Hugging Face Space, но это не обозначает новый релиз модели: репозиторий датирует выпуск демо 2025-07-10. При проверке 2026-09-05 Space отдаёт runtime error, поэтому его нельзя считать доступным рабочим путём.

Новые самостоятельные события: 2025-07-08 — добавлен low-VRAM inference, заявлен запуск с 24 ГБ VRAM; 2025-07-10 — выпущен Hugging Face Space; 2025-07-18 — добавлены квантизованные diffusion-модели и group offload с заявленным запуском от 16 ГБ VRAM; 2025-09-19 — работа принята на NeurIPS 2025. Все четыре даты опубликованы в журнале изменений официального репозитория.

## How to use this

From 2025-06-30, practitioners could locate XVerse's official project, code, and model resources together; by 2025-11-12, they should also check the official Hugging Face Space as its public interactive entry point, while treating the Space's launch or change date as unverified.

1. Клонировать репозиторий, создать окружение Python 3.10.16, установить зафиксированные PyTorch 2.6.0/CUDA 12.4, requirements, FlashAttention и httpx, затем скачать checkpoints и отдельно добавить model_ir_se50.pth.
  — <https://github.com/bytedance/XVerse>
2. Задать пути к Florence-2, SAM2, InsightFace, CLIP, FLUX.1-dev, DPG-VQA и DINO; запустить локальный интерфейс командой python run_gradio.py.
  — <https://github.com/bytedance/XVerse>
3. Для воспроизводимого запуска передать prompt, изображения, подписи и флаги idips в inference_single_sample.py; для нескольких референсов количества images, captions и idips должны совпадать.
  — <https://github.com/bytedance/XVerse>
4. При дефиците памяти включить use_low_vram либо use_lower_vram; для квантизованных FLUX использовать документированный bnb-nf4 или GGUF-путь и повторно подобрать веса.
  — <https://github.com/bytedance/XVerse>

## Best practices

- Включайте в основной prompt точное описание каждого активного референса либо используйте ENT1/ENT2: без него генерация завершается ошибкой.
  — <https://github.com/bytedance/XVerse>
- Не включайте CPU offload без необходимости: документация прямо предупреждает о существенном снижении скорости.
  — <https://github.com/bytedance/XVerse>
- После перехода на квантизованный FLUX заново подберите weight_id, weight_ip и LoRA scales: квантизация может ухудшить результат.
  — <https://github.com/bytedance/XVerse>
- Для оценки изменений запускайте supplied XVerseBench script; он сохраняет результаты в results.
  — <https://github.com/bytedance/XVerse>

## Superseded by this

- 2025-07-08: прежнее требование полноценного режима с большей памятью частично заменено режимом low-VRAM на 24 ГБ для до двух условий.
- 2025-07-18: low-VRAM guidance от 2025-07-08 расширена квантизацией и group offload; заявленный минимум стал 16 ГБ VRAM для до трёх условий.
- 2026-09-05: рекомендация использовать официальный Space как рабочий путь устарела до восстановления сервиса: страница показывает runtime error; локальный запуск остаётся документированным путём.

## Still unknown

- Официальный README отмечает ComfyUI implementation и Benchmark Leaderboard как невыпущенные; отдельного поддерживаемого ComfyUI-пути подтверждать нельзя.
- Hugging Face Space в предоставленном событии 2025-11-12 не содержит собственного датированного changelog, поэтому нельзя надёжно установить, что именно изменилось в этот день, помимо наличия ссылки на демо.
- Название XVerse также используется несвязанной организацией xverse для языковых моделей; в этой истории речь идёт только о ByteDance XVerse для генерации изображений.

## Sources

| source | title | read |
|---|---|---|
| https://bytedance.github.io/XVerse/ | XVerse: Consistent Multi-Subject Control of Identity and Semantic Attributes via DiT Modulation | 2026-09-05 |
| https://github.com/bytedance/XVerse | ByteDance/XVerse official implementation | 2026-09-05 |
| https://huggingface.co/ByteDance/XVerse/tree/main | ByteDance/XVerse model repository | 2026-09-05 |
| https://huggingface.co/spaces/ByteDance/XVerse | ByteDance XVerse Hugging Face Space | 2026-09-05 |
| https://arxiv.org/abs/2506.21416 | XVerse: Consistent Multi-Subject Control of Identity and Semantic Attributes via DiT Modulation | 2026-09-05 |
| https://raw.githubusercontent.com/bytedance/XVerse/main/README.md | XVerse README | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:xverse`, thread `public-resources-and-demo`, 2 dated events 2025-06-30 → 2025-11-12.
- **Practical note:** From 2025-06-30, practitioners could locate XVerse's official project, code, and model resources together; by 2025-11-12, they should also check the official Hugging Face Space as its public interactive entry point, while treating the Space's launch or change date as unverified.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
