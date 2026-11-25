---
title: "DIRECT"
category: "projects"
date: 2026-09-09
tags: ["direct", "direct-development", "project", "yandex-direct-skill"]
aliases: ["DIRECT"]
---

# DIRECT

**Development line:** project:yandex-direct-skill · thread direct-development  
**Last event:** 2026-09-09 · 2 dated since 2026-06-09 · **Researched:** 2026-11-25 · confidence: medium

## What it is

yandex-direct is a Claude Code skill for Yandex Direct statistics and campaign management in the open-source (MIT) polyakov-claude-skills repository.

The skill folder holds `SKILL.md` alongside `assets/previews`, `config`, `references` and `scripts`. The repository also includes sibling skills for Yandex Metrika, Webmaster, Wordstat and Search API.

## Development line

- **2026-06-09 — DIRECT project resources were linked.** A DIRECT development-line message on 2026-06-09 linked the project website, source repository and Hugging Face page. We treat these links as a public project milestone for the development history. We did not review the announcement text or the exact status of each linked resource.
- **2026-09-09 — Yandex.Direct skill release after 6-month delay.** The author announced the release of the Yandex.Direct skill after a 6-month delay caused by API limitations and a transition to composite ads. The announcement details the skill's capabilities (traffic analysis, campaign creation, UTM tags) and the process for obtaining an API key.
  - The repository README lists yandex-direct under available skills ('statistics and management of Yandex Direct'). It shows the install command `/plugin install yandex-direct` after adding the marketplace, or manual installation by copying the skill folder into `.claude/skills/` globally or per project. The same README lists related Yandex skills: yandex-metrika, yandex-webmaster, yandex-wordstat and yandex-search-api. It also lists a separate zoomkit skill for Direct balances, invoices and reports. The repository is MIT-licensed and showed 238 stars and 61 forks when observed. (undated page; observed 2026-09-09) — <https://github.com/artwist-polyakov/polyakov-claude-skills>
  - The skill directory contains `SKILL.md` and the folders `assets/previews`, `config`, `references` and `scripts`, shipping with preview assets and helper scripts. (undated page; observed 2026-09-09) — <https://github.com/artwist-polyakov/polyakov-claude-skills/tree/main/plugins/yandex-direct/skills/yandex-direct>
  - The config README notes commands read `config/.env` directly. Settings are `YANDEX_DIRECT_TOKEN` (a user OAuth token with Direct API access), `YANDEX_DIRECT_ACCOUNT` (the default advertising account login), `YANDEX_DIRECT_LOCALE` (ru, en or tr) and `YANDEX_DIRECT_USE_OPERATOR_UNITS` (auto, never or always). Run `uv run scripts/whoami.py` and `uv run scripts/accounts.py` to check the connection. Tokens, selected accounts, cache and logs stay local and are not committed to Git. (undated page; observed 2026-09-09) — <https://github.com/artwist-polyakov/polyakov-claude-skills/tree/main/plugins/yandex-direct/skills/yandex-direct/config>
  - `API_ACCESS.md` requires three things: an OAuth app with `direct:api` permission, an approved application for Direct API access, and a user token for someone with access to the ad account. Registering the app and filing the application are separate steps; a token alone is not enough. Opening API settings requires at least one campaign in the account, though connecting the skill does not require running ads. The application form should request full access to work with real campaigns. The skill uses Python 3.11+ and the Direct API v5 JSON endpoint, with Live v4 for a few methods that have no v5 equivalent. (undated page; observed 2026-09-09) — <https://github.com/artwist-polyakov/polyakov-claude-skills/blob/main/plugins/yandex-direct/skills/yandex-direct/config/API_ACCESS.md>

## What changed

The repository added the Yandex.Direct skill as the installable `yandex-direct` plugin. It works through the Direct API, requiring a registered OAuth app, an approved API access application and a user token.

## How to use this

1. Add the marketplace with `/plugin marketplace add artwist-polyakov/polyakov-claude-skills`, then install the skill with `/plugin install yandex-direct`. Alternatively, copy the skill folder into `~/.claude/skills/` (global) or `.claude/skills/` (per project).
  — <https://github.com/artwist-polyakov/polyakov-claude-skills>
2. Get access to the Direct API. Create an OAuth app with the `direct:api` permission and save its ClientID. Under the same account, file an application in the Direct API settings, choosing full access. Then obtain a user token.
  — <https://github.com/artwist-polyakov/polyakov-claude-skills/blob/main/plugins/yandex-direct/skills/yandex-direct/config/API_ACCESS.md>
3. Copy `config/.env.example` to `config/.env` and fill in `YANDEX_DIRECT_TOKEN` and, if needed, `YANDEX_DIRECT_ACCOUNT`. The account value is the client login, for example the `ulogin` parameter in the cabinet URL. Then verify with `uv run scripts/whoami.py` and `uv run scripts/accounts.py`.
  — <https://github.com/artwist-polyakov/polyakov-claude-skills/tree/main/plugins/yandex-direct/skills/yandex-direct/config>

## Best practices

- Never print the `.env` file, the token or the `Authorization` header into the conversation, debug logs or the command line.
  — <https://github.com/artwist-polyakov/polyakov-claude-skills/tree/main/plugins/yandex-direct/skills/yandex-direct/config>
- When working with several ad accounts or running commands in parallel, pass `--account` explicitly. This keeps commands independent of the saved choice set with `accounts.py --use`.
  — <https://github.com/artwist-polyakov/polyakov-claude-skills/tree/main/plugins/yandex-direct/skills/yandex-direct/config>
- In the API application, describe the tool honestly. The suggested pattern is that it shows 'was → will be' before any write, performs the user-approved task, re-reads the data and reports the actual result. It runs no financial operations and keeps the token local.
  — <https://github.com/artwist-polyakov/polyakov-claude-skills/blob/main/plugins/yandex-direct/skills/yandex-direct/config/API_ACCESS.md>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The exact release date of the skill in the repository is not shown on the pages.
- The linked pages do not confirm the reasons given for the delay (limited API coverage, the move to combinatorial ads).
- The full list of skill capabilities (traffic analysis, ad creation, UTM tags, preview templates) is not visible in the captured pages, because `SKILL.md` was not captured.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/artwist-polyakov/polyakov-claude-skills | GitHub - artwist-polyakov/polyakov-claude-skills: a set of skills for AI agents | 2026-09-09 |
| https://github.com/artwist-polyakov/polyakov-claude-skills/tree/main/plugins/yandex-direct/skills/yandex-direct | polyakov-claude-skills/plugins/yandex-direct/skills/yandex-direct (directory listing) | 2026-09-09 |
| https://github.com/artwist-polyakov/polyakov-claude-skills/tree/main/plugins/yandex-direct/skills/yandex-direct/config | yandex-direct skill config: connecting to Yandex Direct (README) | 2026-09-09 |
| https://github.com/artwist-polyakov/polyakov-claude-skills/blob/main/plugins/yandex-direct/skills/yandex-direct/config/API_ACCESS.md | yandex-direct skill: API_ACCESS.md, connecting to the Direct API | 2026-09-09 |

## Agent brief {#agent-brief}

- **Subject:** project:yandex-direct-skill, thread direct-development, 2 dated events 2026-06-09 → 2026-09-09.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.