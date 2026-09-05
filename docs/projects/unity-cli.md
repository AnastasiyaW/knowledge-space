---
title: Unity CLI
category: projects
date: 2026-07-23
tags: [project, unity-cli, unity-cli-introduction, unity_cli]
aliases: ["Unity CLI"]
---

# Unity CLI

**Development line:** `project:unity-cli` · thread `unity-cli-introduction`  
**Last event:** 2026-07-23 · 1 dated since 2026-07-23 · **Researched:** 2026-09-05 · confidence: medium

## What it is

Unity CLI — автономный бинарник `unity` для Unity 6.0 LTS+ и CI. — устанавливает Editor и модули; — открывает и обслуживает проекты, лицензии и авторизацию; — с `com.unity.pipeline` управляет локальным запущенным Editor или dev Player, запускает команды и C# eval. Ограничение: CLI и Pipeline остаются экспериментальными; Pipeline — отдельный пакет и по умолчанию работает локально. Вердикт: для новых скриптов и CI это замена Hub CLI, но версию beta нужно фиксировать и проверять по release notes.

## Development line

- **2026-07-23 — Unity published an announcement about Unity CLI.** On 2026-07-23, Unity published a dated official blog entry concerning Unity CLI. The project-specific official link makes this a material introduction milestone in the Unity CLI history. The sealed evidence does not establish its capabilities, availability, or technical behavior.

## What changed

2026-04-04 — первая публичная beta дала единый бинарник для Windows, macOS и Linux, управления Editor, проектами, auth и machine-readable output. 2026-04-23 — появились создание проектов, просмотр changelog и обновление до выбранной версии. 2026-05-06 — Unity Hub 3.18 начал поставлять отдельный CLI, независимый от desktop Hub. 2026-05-07 — beta.4 добавила диагностику, completion и основные команды управления Editor и проектами. 2026-05-21 — service-account auth и `unity pipeline install` сделали unattended CI и подключение Pipeline штатными сценариями. 2026-06-04 — `unity eval` и `unity status` добавили C# eval и наблюдение за подключённым Editor. 2026-06-16 — добавлены лицензирование и клонирование проектов из GitHub, GitLab и Unity Version Control. 2026-06-25 — появился `unity mcp` для агентских интеграций. 2026-06-30 — ветка перешла на 1.0 beta; исправлены утечки OAuth/session ID в логах и JSON/NDJSON output. 2026-07-16 — появился тёплый интерактивный `unity shell`. 2026-07-23 — 1.0.0-beta.3 добавила history, completion, session context и framed NDJSON в shell. 2026-08-12 — beta.4 добавила winget/Homebrew и подняла Linux minimum до glibc 2.34. 2026-08-13 — beta.5 прекратила передачу имени и email из `unity bug`. 2026-08-21 — beta.6 изменила CI-значимые exit codes `unity bug` и `unity test`. 2026-09-02 — beta.8 заменила отозванную beta.7, добавила Unity-aware VCS workflow и исправила несовместимость с неопубликованной версией Pipeline.

## How to use this

As of 2026-07-23, practitioners should track Unity CLI as an official Unity development line and evaluate it for command-line automation only after confirming its documented capabilities.

1. Установите CLI по актуальной инструкции Unity и проверьте доступность командой `unity --version`.
  — <https://docs.unity.com/en-us/unity-cli/use-unity-cli>
2. Посмотрите команды через `unity --help`, установите конкретную версию Editor с нужными модулями и проверьте доступные module IDs.
  — <https://unity.com/ru/blog/meet-the-unity-cli>
3. Выполните `unity auth login`, затем `unity auth status`; для unattended CI используйте поддерживаемую service-account authentication.
  — <https://docs.unity.com/ko-kr/unity-cli/unity-cli-reference>
4. Откройте проект через `unity open <path>`; для terminal-first CI укажите конкретную версию Editor, а не интерактивный выбор.
  — <https://docs.unity.com/en-us/unity-cli/use-unity-cli>
5. Если нужно управлять работающим Editor, установите `com.unity.pipeline` командой `unity pipeline install`, затем вызовите `unity command`, чтобы получить доступный набор команд проекта.
  — <https://learn.unity.com/tutorial/6a7e194752fbca26e9ebccbe>
6. Для CI запрашивайте JSON или NDJSON, обрабатывайте stdout отдельно от stderr и проверяйте exit code.
  — <https://unity.com/ru/blog/meet-the-unity-cli>

## Best practices

- Считайте `unity --help` у установленной версии источником истины по флагам: документация может не содержать недавно добавленную команду.
  — <https://docs.unity.com/ko-kr/unity-cli/unity-cli-reference>
- В CI явно задавайте версию Editor: без неё неинтерактивный `unity install` завершается ошибкой.
  — <https://docs.unity.com/ko-kr/unity-cli/unity-cli-reference>
- Не обновляйте Linux runner до beta.4+ без glibc 2.34; для Ubuntu 20.04 и старее, Debian 11, RHEL/CentOS 8 и Amazon Linux 2 оставьте beta.3.
  — <https://docs.unity.com/ja-jp/unity-cli/release-notes>
- Оставляйте Pipeline на localhost, пока не спроектированы аутентификация и сеть для удалённого доступа.
  — <https://learn.unity.com/tutorial/6a7e194752fbca26e9ebccbe>
- Обновите кратковременно установленную beta.7 до beta.8: beta.7 была отозвана из-за несовместимости с ещё не опубликованным Pipeline package.
  — <https://discussions.unity.com/t/unity-cli-1-0-0-beta-8-is-rolling-out/1735542>
- Перед `unity close` сохраните изменения: ни обычный вызов, ни `--force` не сохраняют работу.
  — <https://discussions.unity.com/t/unity-cli-1-0-0-beta-8-is-rolling-out/1735542>

## Superseded by this

- 2026-05-06 — для новых скриптов не следует выбирать Hub CLI с `-- --headless` как основной путь: отдельный Unity CLI предназначен для новых automation и CI сценариев; Hub CLI deprecated и поддерживается минимально. https://docs.unity.com/hub/cli-overview
- 2026-09-02 — 1.0.0-beta.7 не является допустимой версией для обновления: релиз был отозван и заменён beta.8 из-за несовместимости с требуемым Pipeline package. https://discussions.unity.com/t/unity-cli-1-0-0-beta-8-is-rolling-out/1735542

## Still unknown

- Официальная документация всё ещё помечает Unity CLI как experimental; дата GA и долгосрочная поддержка не объявлены.
- CLI и `com.unity.pipeline` — разные компоненты: без Pipeline CLI не получает поверхность управления работающим Editor или Player.
- Официальный материал по ссылке события датирован 2026-07-20, хотя событие датировано 2026-07-23; beta.3 в release notes действительно вышла 2026-07-23.
- Проверена официальная китайская документация, но независимый китайский отчёт об эксплуатации для рекомендаций не найден и не использован.

## Sources

| source | title | read |
|---|---|---|
| https://unity.com/ru/blog/meet-the-unity-cli | Meet the Unity CLI: управлять Unity с терминала | 2026-09-05 |
| https://unity.com/blog/meet-the-unity-cli | Meet the Unity CLI: manage Unity from your terminal | 2026-09-05 |
| https://docs.unity.com/en-us/unity-cli | Unity command-line interface (CLI) | 2026-09-05 |
| https://docs.unity.com/en-us/unity-cli/use-unity-cli | Use the Unity command-line interface (CLI) | 2026-09-05 |
| https://docs.unity.com/zh-cn/unity-cli/use-unity-cli | Use the Unity command-line interface (CLI) | 2026-09-05 |
| https://docs.unity.com/ko-kr/unity-cli/unity-cli-reference | Unity command-line interface (CLI) reference | 2026-09-05 |
| https://docs.unity.com/ja-jp/unity-cli/release-notes | Unity command-line interface (CLI) release notes | 2026-09-05 |
| https://unity.com/unity-hub/release-notes | Unity Hub Release Notes | 2026-09-05 |
| https://docs.unity.com/hub/cli-overview | Command line interface overview | 2026-09-05 |
| https://learn.unity.com/tutorial/6a7e194752fbca26e9ebccbe | Introduction to Unity CLI | 2026-09-05 |
| https://discussions.unity.com/t/unity-cli-1-0-0-beta-6-is-rolling-out/1734486 | Unity CLI 1.0.0-beta.6 is rolling out | 2026-09-05 |
| https://discussions.unity.com/t/unity-cli-1-0-0-beta-8-is-rolling-out/1735542 | Unity CLI 1.0.0-beta.8 is rolling out | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:unity-cli`, thread `unity-cli-introduction`, 1 dated events 2026-07-23 → 2026-07-23.
- **Practical note:** As of 2026-07-23, practitioners should track Unity CLI as an official Unity development line and evaluate it for command-line automation only after confirming its documented capabilities.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
