---
title: Claude Code
category: projects
tags: [claude-code, claude-code-billing, project]
aliases: ["Claude Code"]
---

# Claude Code

**Development line:** `project:claude-code` · thread `claude-code`  
**Events:** 2 dated, 2026-02-22 → 2026-05-13 · **Researched:** 2026-09-04 · confidence: medium

## What it is

Claude Code — агент для разработчика, который читает и изменяет кодовую базу, выполняет команды и помогает довести изменение до проверяемого результата. — исследует код, исправляет ошибки, пишет тесты и запускает проверки; — работает с Git: commits, ветки и pull requests; — подключает внешние данные и инструменты через MCP; — доступен в CLI, Desktop, VS Code, JetBrains и Web. Ограничение: нужен Pro, Max, Team, Enterprise, Console или поддерживаемый облачный провайдер; бесплатный Claude.ai доступа не даёт. Вердикт: используйте его как агента в репозитории с явными проверками, а не как замену ревью и CI.

## Development line

- **2026-02-22 — Claude Code gains desktop-oriented automation capabilities.** On 2026-02-22, a linked report indicated that Claude Code gained desktop-oriented functionality intended to automate a greater portion of development work. The dated link identifies this as a product-development event, but does not establish the exact feature set or release conditions.
- **2026-05-13 — Reports describe a Claude Code-related unexpected-charge incident.** On 2026-05-13, linked reports described an alleged Claude Code-related incident involving unexpected charges and an Anthropic API key in a project context. The available links do not establish the cause, scope, or remediation, so this is retained as a reported user-impact event pending research.

## What changed

Claude Code — линия развития расширила терминальный агент до нескольких рабочих поверхностей и сделала выбор способа аутентификации частью контроля расходов. — 2026-02-22: desktop-линия была заявлена с preview локального приложения, комментариями к diff, наблюдением за GitHub PR, исправлением CI и автоматическим merge после зелёных тестов. — 2026-05-13: важно разделять два механизма расходов: закрытый дефект v2.1.119 на macOS, где строка `HERMES.md` в недавнем commit message уводила Max-использование в extra usage, и документированный приоритет `ANTHROPIC_API_KEY` над OAuth-подпиской. — Найдено сегодня, первичный источник: 2026-08-17–21 в v2.1.234–v2.1.239 появились research-preview `/design`, карточки устройств для Remote Control и `ANTHROPIC_DEFAULT_MODEL`; текущая документация подтверждает CLI, Desktop, Web и IDE-поверхности. Ограничение: для `HERMES.md` не опубликован точный номер исправляющего релиза, а февральская desktop-хронология не подтверждена первичной заметкой. Вердикт: для текущего процесса опирайтесь на документацию по поверхностям, аутентификации и обновлениям, а исторические инциденты используйте как проверку рисков.

## How to use this

After the 2026-02-22 report, practitioners should evaluate desktop automation controls before relying on them in development workflows. The 2026-05-13 reports are not sufficient to prescribe a verified billing or API-key mitigation; research must establish the cause before operational guidance changes.

1. Установите Claude Code штатным способом для своей платформы и проверьте установку через `claude --version` или `claude doctor`.
  — <https://code.claude.com/docs/en/getting-started>
2. Откройте каталог репозитория, запустите `claude`, пройдите вход и дайте ограниченную задачу с ожидаемым результатом.
  — <https://code.claude.com/docs/en/overview>
3. В незнакомом проекте начните с обзора, затем запросите связи компонентов и трассировку нужного потока выполнения.
  — <https://code.claude.com/docs/en/common-workflows>
4. Для многозадачного или неясного изменения сначала используйте plan mode, проверьте план, затем поручите реализацию и запуск проверок.
  — <https://code.claude.com/docs/en/best-practices>
5. Перед unattended- или `-p`-запуском проверьте `/status`; если должна использоваться подписка, убедитесь, что в окружении нет `ANTHROPIC_API_KEY`.
  — <https://code.claude.com/docs/en/authentication>

## Best practices

- Дайте агенту выполняемую проверку: тест, build, lint или screenshot; требуйте фактический результат, а не заявление об успехе.
  — <https://code.claude.com/docs/en/best-practices>
- Для крупных изменений разделяйте explore, plan, implement и commit; для однострочного очевидного изменения план не нужен.
  — <https://code.claude.com/docs/en/best-practices>
- Держите `CLAUDE.md` коротким: команды, нестандартные правила, тесты и архитектурные решения; ситуативные инструкции переносите в skills.
  — <https://code.claude.com/docs/en/best-practices>
- Ограничивайте разрешения allowlist-правилами и sandbox, а чувствительные действия оставляйте в Manual mode.
  — <https://code.claude.com/docs/en/best-practices>
- Сверяйте активный способ входа: `ANTHROPIC_API_KEY` выше OAuth-подписки, а в неинтерактивном `-p` он применяется всегда, если задан.
  — <https://code.claude.com/docs/en/authentication>
- Для API-расходов используйте `/usage` как оценку, а Console Usage — как источник итогового биллинга.
  — <https://code.claude.com/docs/en/costs>

## Superseded by this

- До 2026-02-22: модель «Claude Code только в терминале» устарела; сегодня официально поддерживаются Desktop, IDE и Web наряду с CLI.
- 2026-04-25: описание `HERMES.md` как текущего обязательного workaround устарело — issue закрыт и затронутым пользователям была обещана компенсация; точную версию исправления всё равно нельзя утверждать.
- Найдено сегодня, 2026-09-04: предположение, что подписка всегда побеждает при наличии OAuth-входа, устарело — `ANTHROPIC_API_KEY` имеет более высокий приоритет, а `-p` использует его автоматически.

## Still unknown

- Материалы от 2026-05-13 описывают два разных механизма: `HERMES.md` в commit message и приоритет `ANTHROPIC_API_KEY`; источники не доказывают, что это один дефект.
- Точный релиз, в котором исправлен `HERMES.md`-дефект, не указан на странице закрытого issue.
- Не найдена первичная февральская release note, подтверждающая весь набор заявленных desktop-функций и их точную дату запуска.

## Sources

| source | title | read |
|---|---|---|
| https://code.claude.com/docs/en/overview | Overview — Claude Code Docs | 2026-09-04 |
| https://code.claude.com/docs/en/getting-started | Advanced setup — Claude Code Docs | 2026-09-04 |
| https://code.claude.com/docs/en/common-workflows | Common workflows — Claude Code Docs | 2026-09-04 |
| https://code.claude.com/docs/en/best-practices | Best practices for Claude Code — Claude Code Docs | 2026-09-04 |
| https://code.claude.com/docs/en/authentication | Authentication — Claude Code Docs | 2026-09-04 |
| https://code.claude.com/docs/en/costs | Manage costs effectively — Claude Code Docs | 2026-09-04 |
| https://code.claude.com/docs/en/whats-new | What's new — Claude Code Docs | 2026-09-04 |
| https://github.com/anthropics/claude-code/issues/53262 | HERMES.md in git commit messages causes requests to route to extra usage billing instead of plan quota — Issue #53262 | 2026-09-04 |
| https://the-decoder.com/anthropic-updates-claude-code-with-desktop-features-that-automate-more-of-the-dev-workflow/ | Anthropic updates Claude Code with desktop features that automate more of the dev workflow | 2026-09-04 |
| https://vc.ru/ai/2897200-bag-v-claude-code-privel-k-spisaniyu-sredstv-iz-za-hermes-md | Anthropic списала $200 сверх тарифа Max 20x из-за HERMES.md в коммите | 2026-09-04 |
| https://www.reddit.com/r/ClaudeAI/comments/1tbaq2d/psa_if_your_project_has_an_anthropic_api_key_in/ | PSA: If your project has an ANTHROPIC_API_KEY in any .env file, Claude Code will silently bill your API account instead of your Max plan | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:claude-code`, thread `claude-code`, 2 dated events 2026-02-22 → 2026-05-13.
- **Practical note:** After the 2026-02-22 report, practitioners should evaluate desktop automation controls before relying on them in development workflows. The 2026-05-13 reports are not sufficient to prescribe a verified billing or API-key mitigation; research must establish the cause before operational guidance changes.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
