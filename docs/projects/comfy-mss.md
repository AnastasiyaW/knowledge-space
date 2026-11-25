---
title: Comfy-MSS
category: projects

tags: [comfy-mss, comfy-mss-development, project]
aliases: ["Comfy-MSS"]
---

# Comfy-MSS

**Development line:** `project:comfy-mss` · thread `comfy-mss-development`  
**Last event:** - · 0 dated since - · **Researched:** 2026-09-05 · confidence: high

## What it is

Comfy-MSS — набор custom nodes ComfyUI поверх pymss для разделения AUDIO на вокал и инструментальные стемы.

Возможности: MSS и VR/UVR-разделение, пользовательские MSST-модели, пакетная загрузка, ensemble, инверсия фазы, нормализация и сохранение WAV/FLAC/MP3.

Ограничение: пользовательский маршрут поддерживает только MSST, а графы v1.0.x несовместимы с v1.1.0+ из-за переименования типов узлов.

Вердикт: это более полный маршрут для stem separation в ComfyUI, но обновление до 1.1 требует пересобрать старые графы.

## Development line

- The dated line is not written up yet; what is known stands in the sections below.

## What changed

2026-07-06 — Comfy-MSS был задокументирован как пакет для разделения ComfyUI AUDIO на вокальные и инструментальные стемы через модели MSS и VR/UVR, с ensemble, нормализацией и phase-invert.

2026-05-31 — опубликован тег 1.0.0. 2026-06-03 — тег 1.0.1 закрепил версию пакета. 2026-06-13 — 1.0.2 обновил зависимость pymss до 2.0.6. 2026-06-28 — 1.0.3 переработал узлы и нормализовал обработку ширины интерфейса. 2026-08-03 — 1.0.4 привёл пользовательские модели в соответствие с pymss: нужен отдельный каталог с weight-файлом и YAML; VR/UVR исключены из Custom MSS Separate. 2026-08-11 — 1.1.0 переименовал типы узлов и сделал графы 1.0.x несовместимыми.

## How to use this

As of 2026-07-06, make no practitioner workflow change from these links alone; wait for sourced release or post-content evidence before adopting or documenting Comfy-MSS usage.

1. Установить репозиторий в `ComfyUI/custom_nodes` и установить `pymss` в то же Python-окружение, что использует ComfyUI; затем перезапустить ComfyUI.
  — <https://github.com/pymss-project/comfy-mss>
2. Подать AUDIO в `MSS Separate` либо `VR Separate`, выбрать каталоговую модель, устройство и источник загрузки; отсутствующая модель по умолчанию загружается автоматически.
  — <https://github.com/pymss-project/comfy-mss>
3. Для серии файлов использовать `Load Audio Batch` и list-вариант separator; последующие узлы выполняются по каждому элементу списка.
  — <https://github.com/pymss-project/comfy-mss>
4. Для своей MSST-модели положить weight-файл и `.yaml` в отдельную дочернюю папку `<pymss_model_dir>/custom`, затем нажать `Refresh Models`.
  — <https://github.com/pymss-project/comfy-mss>
5. Сохранить полученные стемы через `Save Audio`; доступны WAV, FLAC и MP3 с частотой 32/44,1/48 кГц.
  — <https://github.com/pymss-project/comfy-mss>

## Best practices

- Перед обновлением до 1.1.0 сохранить и пересобрать графы v1.0.x: переименование типов узлов делает их несовместимыми.
  — <https://github.com/pymss-project/comfy-mss/blob/main/README.md>
- Оставлять `chunk_size` и `overlap_size` в значении Default, пока не нужна проверенная настройка: тогда применяются значения YAML выбранной модели.
  — <https://github.com/pymss-project/comfy-mss>
- Для переносимых workflow не вшивать машинные пути: использовать стандартный каталог `ComfyUI/models/pymss`, переменные `COMFY_MSS_MODEL_DIR`/`PYMSS_MODEL_DIR` или extra model paths.
  — <https://github.com/pymss-project/comfy-mss>

## Superseded by this

- 2026-08-03 — прежняя практика произвольного custom-layout заменена требованием отдельной папки с поддерживаемым weight-файлом и YAML; VR/UVR больше не относятся к Custom MSS Separate.
- 2026-08-11 — workflow v1.0.x устарели для 1.1.0+ и требуют пересборки из-за переименования node types.

## Still unknown

- Пакет не публикует GitHub Releases; даты и scope его версий подтверждены тегами, а не отдельными release notes.
- Точка 2026-07-06 является датой независимого документирования Comfy-MSS, а не подтверждённым релизом самого пакета.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/pymss-project/comfy-mss | pymss-project/comfy-mss — ComfyUI custom nodes for music source separation | 2026-09-05 |
| https://github.com/pymss-project/comfy-mss/blob/main/README.md | Comfy-MSS README | 2026-09-05 |
| https://github.com/pymss-project/comfy-mss/tags | Comfy-MSS tags and dated changes | 2026-09-05 |
| https://pypi.org/project/pymss/ | pymss on PyPI | 2026-09-05 |
| https://github.com/SlavaSexton/ComfyUI-Agent-Kit/blob/master/CHANGELOG.md | ComfyUI-Agent-Kit changelog 2.3.0 | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:comfy-mss`, thread `comfy-mss-development`, 0 dated events - → -.
- **Practical note:** As of 2026-07-06, make no practitioner workflow change from these links alone; wait for sourced release or post-content evidence before adopting or documenting Comfy-MSS usage.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
