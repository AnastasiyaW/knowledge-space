---
title: LMX-Omni-52B-Halo
category: projects
date: 2026-06-12
tags: [lmx-omni-52b-halo, project]
aliases: ["LMX-Omni-52B-Halo"]
---

# LMX-Omni-52B-Halo

**Development line:** `project:lmx-omni-52b-halo` · thread `lmx-omni-52b-halo`  
**Last event:** 2026-06-12 · 1 dated since 2026-06-12 · **Researched:** 2026-09-05 · confidence: high

## What it is

LMX-Omni-52B-Halo — набор из Qwen3.6-35B-A3B-MTP, Flux-2-Klein-9B, Whisper-Large-v3-Turbo и kokoro-v1 для локальных мультимодальных приложений. Возможности: чат и анализ изображений; генерация и редактирование изображений; транскрибация; синтез речи. Ограничение: загрузка компонентов занимает около 44,8 ГБ, а класс Halo ориентирован на устройства уровня Strix Halo. Вердикт: выбирать для локального any-to-any прототипа или приложения, если оправданы объём загрузки и задержка внутреннего tool-calling цикла.

## Development line

- **2026-06-12 — LMX-Omni-52B-Halo was linked to its Hugging Face model repository.** On 2026-06-12, the record recorded a link to the Hugging Face repository for LMX-Omni-52B-Halo. This establishes the repository as a project artifact by that date, but does not establish its release status, capabilities, licensing, or intended use.

## What changed

2026-06-12 — модельная карточка описывала LMX-Omni-52B-Halo как единый OpenAI-совместимый omni-набор; первичный репозиторий был создан 2026-06-03, а 2026-06-04 его манифест перевели на unified format и удалили старый collection.json. 2026-06-23 — в опубликованный манифест добавлен настраиваемый для коллекции system prompt. 2026-08-08 — открыт нерешённый отчёт: коллекция не передаёт planner reasoning_content в поток Open WebUI; для интерфейса, которому нужен видимый ход рассуждений, это остаётся ограничением.

## How to use this

As of 2026-06-12, practitioners should use the linked Hugging Face repository as the starting point for verifying LMX-Omni-52B-Halo artifacts and documentation before relying on the project.

1. Установите Lemonade, затем скачайте все компоненты командой `lemonade pull LMX-Omni-52B-Halo` и запустите модель командой `lemonade run LMX-Omni-52B-Halo`.
  — <https://huggingface.co/lemonade-sdk/LMX-Omni-52B-Halo>
2. В OpenAI-совместимом клиенте выбирайте имя модели для запросов к `/chat/completions`; сервер сам вызывает компоненты и возвращает изображения и аудио в сообщении ответа.
  — <https://huggingface.co/lemonade-sdk/LMX-Omni-52B-Halo>
3. В MCP-клиенте передайте `model: "LMX-Omni-52B-Halo"` в `lemonade_omni`, если нужен один мультимодальный turn с изображениями и аудио.
  — <https://github.com/lemonade-sdk/lemonade/blob/main/docs/api/mcp.md>

## Best practices

- Явно указывайте Halo только на подходящем оборудовании; MCP по умолчанию использует меньшую и более быструю LMX-Omni-5.5B-Lite.
  — <https://github.com/lemonade-sdk/lemonade/blob/main/docs/api/mcp.md>
- Для артефактов MCP задавайте `output_dir`: это даёт уникальные имена файлов и подходит клиентам, которые не отображают audio content blocks.
  — <https://github.com/lemonade-sdk/lemonade/blob/main/docs/api/mcp.md>
- Не рассчитывайте на потоковое отображение reasoning в Open WebUI: зарегистрированная проблема для Omni-коллекций остаётся открытой.
  — <https://github.com/lemonade-sdk/lemonade/issues/2990>

## Superseded by this

- 2026-05-21 — прежнее руководство по старым «collections» устарело: релиз Lemonade v10.6.0 заменил их моделями LMX-Omni-52B-Halo и LMX-Omni-5.5B-Lite.
- 2026-06-04 — старый формат manifest `collection.json` для этой модели заменён unified-файлом `LMX-Omni-52B-Halo.json`.

## Still unknown

- Первичный источник не датирует именно 2026-06-12 выпуском или изменением; он подтверждает состояние страницы, но не даёт отдельной записи о событии в этот день.
- Схема ответа не содержит запрошенные поля event_findings и new_events; их фактические дополнения отражены в what_changed и unknowns.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/lemonade-sdk/LMX-Omni-52B-Halo | LMX-Omni-52B-Halo model card | 2026-09-05 |
| https://huggingface.co/lemonade-sdk/LMX-Omni-52B-Halo/commits/main | LMX-Omni-52B-Halo commit history | 2026-09-05 |
| https://github.com/lemonade-sdk/lemonade/blob/main/docs/dev/lemonade-omni.md | Lemonade Omni Models documentation | 2026-09-05 |
| https://github.com/lemonade-sdk/lemonade/blob/main/docs/api/mcp.md | Lemonade MCP API documentation | 2026-09-05 |
| https://github.com/lemonade-sdk/lemonade/releases/tag/v10.6.0 | Lemonade v10.6.0 release | 2026-09-05 |
| https://github.com/lemonade-sdk/lemonade/issues/2990 | Omni collections do not stream planner reasoning_content | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:lmx-omni-52b-halo`, thread `lmx-omni-52b-halo`, 1 dated events 2026-06-12 → 2026-06-12.
- **Practical note:** As of 2026-06-12, practitioners should use the linked Hugging Face repository as the starting point for verifying LMX-Omni-52B-Halo artifacts and documentation before relying on the project.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
