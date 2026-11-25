---
title: Awesome Harness Engineering
category: projects
date: 2026-07-06
tags: [awesome-harness-engineering, project]
aliases: ["Awesome Harness Engineering"]
---

# Awesome Harness Engineering

**Development line:** `project:awesome-harness-engineering` · thread `awesome-harness-engineering`  
**Last event:** 2026-07-06 · 1 dated since 2026-07-06 · **Researched:** 2026-09-05 · confidence: medium

## What it is

Awesome Harness Engineering — curated GitHub-список для инженеров агентных систем, а не runtime или модель. Возможности: навигация по loop, планированию, контексту, инструментам, MCP, правам, памяти, оркестрации, проверке, наблюдаемости и sandboxing; готовые AGENTS.md, PLAN.md, IMPLEMENT.md и checklist-шаблоны. Ограничение: репозиторий не выпускает версий и не заменяет проверку первичных источников. Вердикт: использовать как карту решений и стартовых артефактов, затем валидировать выбранный подход в собственном runtime.

## Development line

- **2026-07-06 — Awesome Harness Engineering GitHub repository was referenced.** On 2026-07-06, a dated message associated with Awesome Harness Engineering linked to its GitHub repository. This establishes a public repository reference for the project on that date, but does not establish a release, feature change, or other milestone.

## What changed

2026-07-06 — список был зафиксирован как отдельный каталог ресурсов по harness engineering; он уже агрегировал материалы о контексте, инструментах, планировании, правах, памяти, верификации и sandboxing.

## How to use this

As of 2026-07-06, practitioners should use the linked GitHub repository as the discoverable entry point for Awesome Harness Engineering, while verifying its contents before relying on any specific capability or revision.

1. Откройте README и выберите раздел по наблюдаемой проблеме: loop, context, tools, permissions, memory, orchestration, verification или observability.
  — <https://github.com/ai-boost/awesome-harness-engineering>
2. Для нового или длинного агентного задания возьмите подходящий шаблон: AGENTS.md для правил среды, PLAN.md для milestones и проверок, IMPLEMENT.md для решений и отклонений.
  — <https://github.com/ai-boost/awesome-harness-engineering>
3. Перед добавлением ресурса или принятием рекомендации проверьте, что она решает конкретную проблему harness, а не является общим материалом о модели.
  — <https://github.com/ai-boost/awesome-harness-engineering/blob/main/CONTRIBUTING.md>

## Best practices

- Строить список компонентов вокруг конкретного ограничения агента и убирать scaffolding, когда его предпосылка перестаёт быть верной.
  — <https://github.com/ai-boost/awesome-harness-engineering>
- Принимать только технически содержательные, переносимые по принципу ресурсы; не включать общие ML-работы, нерелевантные model benchmarks и маркетинговые анонсы.
  — <https://github.com/ai-boost/awesome-harness-engineering/blob/main/CONTRIBUTING.md>
- Проверять ссылки регулярно: репозиторий содержит скрипт с ограничением одновременных запросов, таймаутом и повторными попытками.
  — <https://github.com/ai-boost/awesome-harness-engineering/blob/main/verify_urls.py>

## Superseded by this

- 2026-08-12 и ранее — статичная трактовка каталога как неизменного списка устарела: история коммитов показывает регулярные точечные добавления ресурсов в Skills & MCP, Evals & Verification, Context и другие разделы.
- 2026-09-01 — представление каталога как только набора ссылок неполно: в нём поддерживаются также шаблоны рабочих артефактов и критерии их внесения.

## Still unknown

- Точная причина появления ссылки 2026-07-06 не подтверждена автором репозитория: первичный GitHub-интерфейс в доступной выдаче не показал commit, связанный именно с этим днём.
- Сторонние снимки расходятся по дате создания: один указывает 2026-07-05/06 как раннее появление в каталоге, другой называет создание 2026-03-29. Поэтому создание репозитория не приписано событию 2026-07-06.
- Числа stars, forks и commits быстро меняются и не являются стабильной характеристикой для выбора инструмента.
- Репозиторий не публикует GitHub Releases; изменения следует отслеживать по истории коммитов, а не по версиям.
- Тема едина: все найденные материалы описывают один curated list, а не отдельный агентный runtime.
- Нельзя утверждать, что каждая внешняя ссылка в каталоге остаётся доступной: наличие verify_urls.py показывает механизм проверки, но не предоставляет свежий полный результат.
- event_findings: [{"event_date":"2026-07-06","finding":"Сторонний каталог зафиксировал первое появление проекта 2026-07-06 08:01:15 и последний commit 2026-07-05 13:48:11; это уточняет, что событие относится к раннему распространению уже существующего списка, а не к подтверждённому релизу.","source_date":"2026-07-06","source_url":"https://devlive.org/project/ai-boost/awesome-harness-engineering"},{"event_date":"2026-07-06","finding":"Снимок аудита, созданный 2026-07-07, записал 2,861 stars, 294 forks и 88 открытых pull requests; это исторический snapshot, а не текущие показатели.","source_date":"2026-07-07","source_url":"https://huggingface.co/datasets/cy0307/awesome-loop-engineering/blob/refs%2Fpr%2F3/data/resource_source_audit.csv"}]
- new_events: [{"date":"2026-08-07","summary":"Добавлены ruvnet/metaharness в Generators & Meta-Harnesses и addyosmani/agent-skills в Skills & MCP; каталог расширился в направлении оптимизации harness и переносимых skills.","source_url":"https://github.com/ai-boost/awesome-harness-engineering/commits/main"},{"date":"2026-08-16","summary":"В раздел Evals & Verification добавлен Accio-org/RealReplicaBench; проверка агентного поведения стала отдельным поддерживаемым направлением обновления списка.","source_url":"https://github.com/ai-boost/awesome-harness-engineering/commits/main"},{"date":"2026-08-22","summary":"Добавлен zero-trust guide Google для ADK в раздел безопасности и прав; безопасность обновляется вместе с ресурсами по runtime и orchestration.","source_url":"https://github.com/ai-boost/awesome-harness-engineering/commits/main"},{"date":"2026-09-01","summary":"Добавлен HarnessRouter в Task Runners & Orchestration; каталог продолжал получать новые практические runtime-ресурсы после исходного события.","source_url":"https://github.com/ai-boost/awesome-harness-engineering/commits/main"}]

## Sources

| source | title | read |
|---|---|---|
| https://github.com/ai-boost/awesome-harness-engineering | Awesome Harness Engineering — repository README | 2026-09-05 |
| https://github.com/ai-boost/awesome-harness-engineering/commits/main | Commit history — ai-boost/awesome-harness-engineering | 2026-09-05 |
| https://github.com/ai-boost/awesome-harness-engineering/blob/main/CONTRIBUTING.md | Contributing — ai-boost/awesome-harness-engineering | 2026-09-05 |
| https://github.com/ai-boost/awesome-harness-engineering/blob/main/verify_urls.py | verify_urls.py — ai-boost/awesome-harness-engineering | 2026-09-05 |
| https://devlive.org/project/ai-boost/awesome-harness-engineering | ai-boost/awesome-harness-engineering — TrendForge project record | 2026-09-05 |
| https://huggingface.co/datasets/cy0307/awesome-loop-engineering/blob/refs%2Fpr%2F3/data/resource_source_audit.csv | resource_source_audit.csv — awesome-loop-engineering dataset | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:awesome-harness-engineering`, thread `awesome-harness-engineering`, 1 dated events 2026-07-06 → 2026-07-06.
- **Practical note:** As of 2026-07-06, practitioners should use the linked GitHub repository as the discoverable entry point for Awesome Harness Engineering, while verifying its contents before relying on any specific capability or revision.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
