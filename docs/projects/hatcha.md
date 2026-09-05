---
title: HATCHA — Public repository reference
category: projects
date: 2026-06-27
tags: [hatcha, project, public-repository-reference]
aliases: ["HATCHA"]
---

# HATCHA — Public repository reference

**Development line:** `project:hatcha` · thread `public-repository-reference`  
**Last event:** 2026-06-27 · 1 dated since 2026-06-27 · **Researched:** 2026-09-05 · confidence: medium

## What it is

HATCHA is an open-source reverse CAPTCHA from monday.com for Next.js and Express. It issues a computational challenge and stores the answer only on the server. It signs the hash and expiry with an HMAC token, then returns a verification token.

- Five built-in challenges that issue verification tasks.
- React components that handle client interactions.
- Server handlers that verify solutions.
- Custom generators that create user-defined challenges.

Built-in challenges are capped at 30 seconds. It provides an extra gate for low-risk agent-only scenarios, not proof of identity, authority, or agent security.

## Development line

- **2026-06-27 — HATCHA's GitHub repository was referenced.** The monorepo splits into core, React, and server packages, with Next.js and Express adapters.

## What changed

2026-06-27 — HATCHA became available as a public MIT project from monday.com. The monorepo splits into core, React, and server packages, with Next.js and Express adapters.

## How to use this

After the 2026-06-27 repository reference, we can treat the HATCHA GitHub repository as the implementation source. Check its contents and release status before relying on any feature.

1. Install the React and server packages: `npm install @mondaycom/hatcha-react @mondaycom/hatcha-server`.
  — <https://github.com/mondaycom/HATCHA>
2. In Next.js, create a route handler with `createHatchaHandler` and pass a unique server `HATCHA_SECRET`.
  — <https://github.com/mondaycom/HATCHA>
3. Wrap the application in `HatchaProvider`, import styles, and call `requestVerification` before the target agent-only action.
  — <https://usehatcha.dev/>
4. Verify the issued verification token on the server before granting the restricted action; never expose the challenge and answer as client secrets.
  — <https://github.com/mondaycom/HATCHA>

## Best practices

- Place HATCHA before low-risk agent-only flows, demos, or sandboxes. Keep separate authentication, authorization, audit logs, abuse controls, and spend limits for actions with data or money.
  — <https://news.lavx.hu/article/monday-com-releases-hatcha-a-reverse-captcha-for-ai-agents>
- Keep `HATCHA_SECRET` only on the server, set a strong value, and configure rate limits alongside an explicit threat model.
  — <https://news.lavx.hu/article/monday-com-releases-hatcha-a-reverse-captcha-for-ai-agents>
- Register a custom challenge generator for non-standard scenarios, but keep server validation and a bounded TTL.
  — <https://github.com/mondaycom/HATCHA>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The repository has no published GitHub Releases; primary sources do not identify the exact commit and version for 2026-06-27.
- We found no dated primary changelog post for 2026-06-27. A publication on 2026-06-26 and current documentation confirm event details, but they do not prove later changes did not occur.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/mondaycom/HATCHA | GitHub — mondaycom/HATCHA | 2026-09-05 |
| https://usehatcha.dev/ | HATCHA — Reverse CAPTCHA for AI Agents | 2026-09-05 |
| https://news.lavx.hu/article/monday-com-releases-hatcha-a-reverse-captcha-for-ai-agents | Monday.com releases HATCHA, a reverse CAPTCHA for AI agents | 2026-09-05 |
| https://developer-community.monday.com/ai-category-25/welcoming-agents-to-the-ecosystem-5206 | Welcoming Agents to the Ecosystem | 2026-09-05 |
| https://developer.monday.com/api-reference/docs/build-on-monday-with-ai | Build on monday.com with AI | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:hatcha`, thread `public-repository-reference`, 1 dated events 2026-06-27 → 2026-06-27.
- **Practical note:** After the 2026-06-27 repository reference, we can treat the HATCHA GitHub repository as the implementation source. Check its contents and release status before relying on any feature.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
