---
title: Lucida
category: projects
date: 2026-07-21
tags: [lucida, lucida-development, project]
aliases: ["Lucida"]
---

# Lucida

**Development line:** `project:lucida` · thread `lucida-development`  
**Last event:** 2026-07-21 · 1 dated since 2026-07-21 · **Researched:** 2026-09-05 · confidence: high

## What it is

Lucida — MIT-модель сегментации и альфа-маттинга для пользователей, которым RMBG-2.0 или обычный background remover теряет полупрозрачные и тонкие детали.

Возможности: RGBA-вывод, локальный Python/CLI/HTTP-запуск, Transformers и ComfyUI.

Мера: опубликованный тест на 203 изображениях даёт средний MAE 0,0257 для текущих v7-весов.

Вердикт: выбирайте её для текста, принтов, камуфляжа и иллюстраций; для тонких структур, сложных сцен и волос измеренные конкуренты остаются сильнее.

## Development line

- **2026-07-21 — Lucida development resources were linked.** Добавлена категория print-design/sticker, средний MAE стал 0,0257 на 203 изображениях, а модель появилась в официальной коллекции моделей ComfyUI.

## What changed

2026-07-13 — выпущена Lucida v1.0: первая публичная версия с MIT-весами, поддержкой Transformers и тестом на 191 изображении в восьми категориях. 2026-07-18 — v1.1 добавила обучение на 9 426 парах для сохранения непрозрачных частей прозрачных объектов и обрезанных краем кадра объектов; прозрачностный MAE ухудшился с 0,0376 до 0,0403. 2026-07-21 — на момент этого шага актуальным релизом была Lucida v1.2 от 2026-07-20: добавлена категория print-design/sticker, средний MAE стал 0,0257 на 203 изображениях, а модель появилась в официальной коллекции моделей ComfyUI. 2026-07-23 — v1.3 опубликовала v13 с loss для чистоты фона и «супом» чекпойнтов; заявленный средний MAE был 0,0250. 2026-07-24 — веса v13 отозваны из-за регрессии на многослойных реальных иллюстрациях; в модели снова обслуживаются v7-веса, а v14 обозначена как работа в процессе.

## How to use this

From 2026-07-21, practitioners should treat Lucida's GitHub repository, Hugging Face model page, and linked showcase/demo Spaces as the dated starting points for evaluating or reproducing the project, while independently verifying versions and capabilities.

1. Установите проект с Python 3.12+ через uv и выполните `uv run bgr remove input.jpg -o output.png --model lucida`; сохраняйте результат в PNG, чтобы не потерять альфа-канал.
  — <https://github.com/egeorcun/lucida>
2. Для Python загрузите `egeorcun/lucida` через `AutoModelForImageSegmentation` или pipeline с `trust_remote_code=True`; вход приводите к RGB.
  — <https://huggingface.co/egeorcun/lucida>
3. Для ComfyUI скачайте `lucida.safetensors` в `ComfyUI/models/background_removal/` и откройте приложенный workflow Remove Background (BiRefNet).
  — <https://github.com/egeorcun/lucida>
4. Для быстрой проверки без локальной установки загрузите изображение в демонстрацию Gradio, работающую на ZeroGPU.
  — <https://huggingface.co/spaces/egeorcun/lucida-demo>

## Best practices

- Используйте 1024×1024 для инференса: это рекомендуемое и обучающее разрешение; затем масштабируйте alpha обратно к исходному размеру.
  — <https://github.com/egeorcun/lucida>
- Для сложных многообъектных кадров, тонких конструкций и волос сравнивайте результат с InSPyReNet или RMBG-2.0, а не предполагаете универсальное преимущество Lucida.
  — <https://github.com/egeorcun/lucida>
- Не переходите на v13: опубликованные веса были возвращены к v7 после обнаруженной регрессии на реальных layered-design изображениях.
  — <https://github.com/egeorcun/lucida/releases>
- Перед коммерческим применением самостоятельно оцените лицензионный риск: часть обучающих наборов указана как research-only, хотя код и веса выпущены под MIT.
  — <https://github.com/egeorcun/lucida>

## Superseded by this

- 2026-07-18: v1.0 заменена v1.1 для прозрачных объектов с непрозрачными частями и объектов у края кадра.
- 2026-07-20: v1.1 заменена v1.2/v7 для print-design и sticker-art задач.
- 2026-07-24: руководство использовать v13 устарело; опубликованные веса возвращены к v7 из-за регрессии на многослойных иллюстрациях.

## Still unknown

- Полная публикация от 2026-07-21 не содержит текста, поэтому её точный авторский тезис не восстановлен; связь шага с v1.2 установлена по ближайшему первичному релизу от 2026-07-20 и ссылкам на те же репозиторий, веса и демо.
- Схема ответа не содержит отдельных полей event_findings и new_events; их сведения включены в хронологию what_changed.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/egeorcun/lucida | egeorcun/lucida — README | 2026-09-05 |
| https://huggingface.co/egeorcun/lucida | egeorcun/lucida — Hugging Face model card | 2026-09-05 |
| https://huggingface.co/spaces/egeorcun/lucida-demo | Lucida — Background Removal demo | 2026-09-05 |
| https://github.com/egeorcun/lucida/releases | egeorcun/lucida — GitHub releases | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:lucida`, thread `lucida-development`, 1 dated events 2026-07-21 → 2026-07-21.
- **Practical note:** From 2026-07-21, practitioners should treat Lucida's GitHub repository, Hugging Face model page, and linked showcase/demo Spaces as the dated starting points for evaluating or reproducing the project, while independently verifying versions and capabilities.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
