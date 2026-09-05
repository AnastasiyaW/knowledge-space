---
title: OmniRoute
category: projects
date: 2026-07-25
tags: [omniroute, project]
aliases: ["OmniRoute"]
---

# OmniRoute

**Development line:** `project:omniroute` · thread `omniroute`  
**Last event:** 2026-07-25 · 1 dated since 2026-07-25 · **Researched:** 2026-09-05 · confidence: high

## What it is

OmniRoute — MIT-шлюз для подключения Claude Code, Codex, Cursor, Cline и других клиентов к провайдерам моделей через один endpoint. Возможности: провайдеры и модели, fallback и combo-маршрутизация, квоты, MCP/A2A, desktop/PWA. Мера: в текущем README заявлены 352 провайдера и 1 312 chat-model IDs для линии v3.8.50. Вердикт: подходит для самостоятельного развёртывания и управления несколькими API-источниками; сведения о доступных бесплатных квотах нужно перепроверять перед расчётом нагрузки.

## Development line

- **2026-07-25 — OmniRoute GitHub repository reference.** Поддержка Gemini 3.6 flash-high, flash-medium и flash-low уже была добавлена через провайдер Antigravity CLI, но ожидала выпуска v3.8.49; это подтверждено сопровождающим 2026-07-26.

## What changed

2026-07-25 — опубликованная v3.8.48 отставала от ветки разработки: поддержка Gemini 3.6 flash-high, flash-medium и flash-low уже была добавлена через провайдер Antigravity CLI, но ожидала выпуска v3.8.49; это подтверждено сопровождающим 2026-07-26. 2026-08-06 — дорожная карта закрепила переход от линии v3.8.x к v3.9.0 LTS и модульному v4: v3 остаётся стабильной веткой, а новые возможности переносятся в v4.

## How to use this

From 2026-07-25, practitioners should use the linked OmniRoute GitHub repository as the starting point for source inspection, without inferring a supported feature set or release status until the repository is researched.

1. Для разработки из исходников клонируйте репозиторий, выполните npm install, npm run build и npm start; сервер разработки запускается через npm run dev на порту 20128.
  — <https://github.com/diegosouzapw/OmniRoute/discussions/8556>
2. Подключите совместимый клиент к endpoint OmniRoute и настройте провайдеры, модели и правила fallback в панели или конфигурации проекта.
  — <https://github.com/diegosouzapw/OmniRoute>

## Best practices

- Не принимайте наличие модели в ветке разработки за наличие в опубликованном релизе: для Gemini 3.6 на 25 июля требовалась ветка release/v3.8.49 либо сборка из исходников.
  — <https://github.com/diegosouzapw/OmniRoute/discussions/8556>
- Для рабочего окружения выбирайте стабильную v3/LTS-линию, а nightly и release-ветки используйте только для проверки новых возможностей.
  — <https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.51/ROADMAP.md>

## Superseded by this

- 2026-07-25: предположение, что опубликованная v3.8.48 содержит Gemini 3.6, устарело; поддержка была только в готовящейся ветке v3.8.49.
- 2026-08-06: стратегия, при которой все новые возможности добавляются в v3, заменяется разделением на стабильную v3/LTS и модульную v4.

## Still unknown

- В заданной схеме нет полей event_findings и new_events. Деталь события 2026-07-25 и последующее событие 2026-08-06 сохранены в what_changed; первоисточник для первого дополнения датирован 2026-07-26.
- Текущая стабильная опубликованная версия не подтверждена этим набором источников: репозиторий отображает ветку release/v3.8.51, но не является доказательством опубликованного релиза.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/diegosouzapw/OmniRoute | OmniRoute repository and README | 2026-09-05 |
| https://github.com/diegosouzapw/OmniRoute/discussions/8556 | New Release? — maintainer answer on Gemini 3.6 and release/v3.8.49 | 2026-09-05 |
| https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.51/ROADMAP.md | OmniRoute Roadmap | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:omniroute`, thread `omniroute`, 1 dated events 2026-07-25 → 2026-07-25.
- **Practical note:** From 2026-07-25, practitioners should use the linked OmniRoute GitHub repository as the starting point for source inspection, without inferring a supported feature set or release status until the repository is researched.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
