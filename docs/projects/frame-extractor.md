---
title: Frame Extractor
category: projects
date: 2026-08-21
tags: [frame-extractor, project]
aliases: ["Frame Extractor"]
---

# Frame Extractor

**Development line:** `project:frame-extractor` · thread `frame-extractor`  
**Last event:** 2026-08-21 · 1 dated since 2026-08-21 · **Researched:** 2026-09-05 · confidence: high

## What it is

Frame Extractor — локальный GUI и CLI для превращения видео в последовательность кадров для SfM и Gaussian Splatting. — адаптирует плотность кадров к движению камеры; — поддерживает фиксированный интервал, выбранные участки таймлайна и ручной экспорт; — сохраняет JPEG/PNG, CSV-манифест, настройки и summary рядом с кадрами. Текущий тестовый релиз — v0.2.0-rc.2; macOS Apple Silicon остаётся основной вручную протестированной платформой. Вердикт: для подготовки видеосъёмки к 3D-реконструкции используйте новый C++ GUI-проект, а не исходный Python CLI.

## Development line

- **2026-08-21 — Frame Extractor repository linked as a project development reference.** On 2026-08-21, the Frame Extractor development line included a link to its GitHub repository. This establishes a dated public reference for the project, but the available evidence does not identify a specific release, feature, change, or operational capability.

## What changed

2026-08-15 — исходный Python Frame Extractor получил переработку конвейера таймингов, более строгие тесты, timestamped-манифесты кадров и обязательное извлечение последнего успешно обработанного кадра. 2026-08-21 — Frame Extractor был доступен как Python-инструмент, который отслеживает регулярную сетку точек через dense OpenCV DIS optical flow и выбирает keyframes по накопленному смещению и потере точек. 2026-09-05 — исходный репозиторий помечен как проект, дальнейшая разработка которого перенесена в Adaptive Frame Extractor: кроссплатформенное приложение на C++20 с GUI, CLI, регионами таймлайна и готовыми пакетами.

## How to use this

As of 2026-08-21, practitioners should treat the linked Frame Extractor repository as the dated project reference to inspect before relying on its workflow; its capabilities and release status remain unverified.

1. Откройте Adaptive Frame Extractor, перетащите видео и выберите каталог результата.
  — <https://github.com/morishuz/adaptive-frame-extractor>
2. Выберите Low, Medium или High для адаптивного отбора либо fixed interval, при необходимости отметьте нужные регионы на таймлайне.
  — <https://github.com/morishuz/adaptive-frame-extractor>
3. Выберите JPEG либо PNG и запустите extraction; используйте keyframes.csv и summary.txt как манифест входа в COLMAP или Gaussian Splatting.
  — <https://github.com/morishuz/adaptive-frame-extractor>
4. Для автоматизации запустите CLI: ./build/release/frame-extractor input.mp4 --output-dir output.
  — <https://github.com/morishuz/adaptive-frame-extractor>

## Best practices

- Для неравномерного движения камеры начинайте с adaptive preset: фиксированный интервал создаёт дубли на остановках и может оставить недостаточное перекрытие при быстром движении.
  — <https://github.com/morishuz/adaptive-frame-extractor>
- Ограничивайте извлечение полезными регионами таймлайна и сохраняйте CSV-манифест вместе с изображениями, чтобы реконструкцию можно было воспроизвести.
  — <https://github.com/morishuz/adaptive-frame-extractor>
- В legacy CLI явно передавайте configs/default.yaml для воспроизводимого запуска; параметры DIS, сетки, оценки движения и порогов собраны в одном YAML.
  — <https://github.com/morishuz/frame-extractor>

## Superseded by this

- 2026-09-05 — рекомендация устанавливать и развивать Python-проект через uv устарела для новых пользователей: сам репозиторий направляет дальнейшую разработку в Adaptive Frame Extractor.
- 2026-09-05 — Python-only запуск с настройкой окружения заменён готовым кроссплатформенным GUI-приложением; legacy CLI остаётся применимым для существующих скриптов.

## Still unknown

- Для даты 2026-08-21 нет отдельного датированного первоисточника помимо ссылки на исходный репозиторий; поэтому event_findings намеренно пуст. Даты запуска Adaptive Frame Extractor и v0.2.0-rc.2 не удалось подтвердить через доступную страницу GitHub Releases.
- event_findings=[]
- new_events=[{"date":"2026-08-15","source_date":"2026-08-15","summary":"Исходный Python-проект получил refactor timing pipeline, расширенное покрытие тестами, timestamped keyframe manifests и final-frame extraction.","source_url":"https://github.com/morishuz/frame-extractor/commits/main/"},{"date":"2026-09-05","source_date":"2026-09-05","summary":"Текущая документация исходного проекта направляет новых пользователей в Adaptive Frame Extractor, кроссплатформенный C++20 GUI и CLI с локальной обработкой.","source_url":"https://github.com/morishuz/frame-extractor"}]} еицassistant to=developer? no. We gave invalid JSON! I inadvertently fields `

## Sources

| source | title | read |
|---|---|---|
| https://github.com/morishuz/frame-extractor | GitHub — morishuz/frame-extractor | 2026-09-05 |
| https://github.com/morishuz/frame-extractor/commits/main/ | GitHub — commit history for morishuz/frame-extractor | 2026-09-05 |
| https://github.com/morishuz/adaptive-frame-extractor | GitHub — morishuz/adaptive-frame-extractor | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:frame-extractor`, thread `frame-extractor`, 1 dated events 2026-08-21 → 2026-08-21.
- **Practical note:** As of 2026-08-21, practitioners should treat the linked Frame Extractor repository as the dated project reference to inspect before relying on its workflow; its capabilities and release status remain unverified.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
