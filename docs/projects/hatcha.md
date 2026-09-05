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

HATCHA is an open-source reverse CAPTCHA from monday.com for Next.js and Express. It issues a computational challenge, stores the answer only on the server, signs the hash and expiry with an HMAC token, and returns a verification token.

- Five built-in challenges: run computational tasks for agent verification.
- React components: provide client integration and provider wrappers.
- Server handlers: route verification requests in Next.js and Express.
- Custom generators: register non-standard challenges.

Built-in challenges are capped at 30 seconds.

This provides an extra gate for low-risk agent-only scenarios, not proof of identity, authority, or agent safety.

## Development line

- **2026-06-27 — HATCHA's GitHub repository was referenced.** The monorepo splits into core, React, and server packages, with adapters for Next.js and Express.

## What changed

2026-06-27 — monday.com released HATCHA as a public MIT project. The monorepo splits into core, React, and server packages, with adapters for Next.js and Express.

## How to use this

We can treat the HATCHA GitHub repository as the implementation source after the 2026-06-27 repository reference. Check its contents and release status before relying on a specific feature.

1. Install the React and server packages: `npm install @mondaycom/hatcha-react @mondaycom/hatcha-server`.
  — <https://github.com/mondaycom/HATCHA>
2. Create a Next.js route handler with `createHatchaHandler` and pass a unique server `HATCHA_SECRET`.
  — <https://github.com/mondaycom/HATCHA>
3. Wrap the application in `HatchaProvider`, import styles, and call `requestVerification` before the target agent-only action.
  — <https://usehatcha.dev/>
4. Verify the issued verification token on the server before allowing the protected action; do not expose the challenge or response as client secrets.
  — <https://github.com/mondaycom/HATCHA>

## Best practices

- Place HATCHA in front of low-risk agent-only workflows, demos, or sandboxes, but keep separate authentication, authorization, audit logs, anti-abuse controls, and spend limits for data or financial actions.
  — <https://news.lavx.hu/article/monday-com-releases-hatcha-a-reverse-captcha-for-ai-agents>
- Keep `HATCHA_SECRET` strictly on the server, use a strong value, and set rate limits alongside an explicit threat model.
  — <https://news.lavx.hu/article/monday-com-releases-hatcha-a-reverse-captcha-for-ai-agents>
- Register a custom challenge generator for non-standard use cases, but retain server-side verification and a bounded TTL.
  — <https://github.com/mondaycom/HATCHA>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The repository has no published GitHub Releases; primary sources do not identify the exact commit or version corresponding to 2026-06-27.
- No primary changelog post was dated 2026-06-27; details rely on a 2026-06-26 publication and current documentation, leaving subsequent changes unconfirmed.

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
- **Practical note:** We can treat the HATCHA GitHub repository as the implementation source after the 2026-06-27 repository reference, while verifying its contents and release status before relying on a specific feature.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
