---
title: OpenMAIC
category: projects
date: 2026-03-16
tags: [openmaic, openmaic-development, project]
aliases: ["OpenMAIC"]
---

# OpenMAIC

**Development line:** `project:openmaic` · thread `openmaic-development`  
**Last event:** 2026-03-16 · 1 dated since 2026-03-16 · **Researched:** 2026-09-05 · confidence: medium

## What it is

OpenMAIC is an open-source classroom generator for educators and learners: slides, quizzes, interactive HTML scenes, project-based learning, AI teacher/peer discussion, whiteboard, TTS, and exports. Self-hosting currently requires Node.js 22.19+ and pnpm 10+. Verdict: use it when a generated lesson needs a playable classroom rather than a chatbot answer.

## Development line

- **2026-03-16 — OpenMAIC project resources referenced.** On 2026-03-16, a dated OpenMAIC message referenced the project's GitHub repository and public website. The supplied evidence does not establish a release, feature, launch, or other technical milestone, so this event records the availability of those project resources only.

## What changed

2026-03-16 — OpenMAIC was founded and open-sourced as a multi-agent interactive-classroom project; the first tagged release followed on 2026-03-26.

## How to use this

As of 2026-03-16, practitioners can use the referenced GitHub repository and project website as the identified OpenMAIC resources; no specific capability, release, or usage guidance is established by the supplied evidence.

1. Clone the repository and install dependencies with pnpm.
  — <https://github.com/THU-MAIC/OpenMAIC>
2. Copy .env.example to .env.local and configure at least one LLM provider.
  — <https://github.com/THU-MAIC/OpenMAIC>
3. Run pnpm dev, then open http://localhost:3000; use pnpm build && pnpm start for a production build.
  — <https://github.com/THU-MAIC/OpenMAIC>
4. For a shared deployment, set ACCESS_CODE so the UI and API routes require the site password.
  — <https://github.com/THU-MAIC/OpenMAIC>

## Best practices

- Treat pre-0.3 interactive widgets as compatibility candidates: v0.3.0 removed same-origin access from the iframe sandbox.
  — <https://raw.githubusercontent.com/THU-MAIC/OpenMAIC/main/CHANGELOG.md>
- Do not put credentials in Docker build arguments; image metadata or build provenance can retain them.
  — <https://github.com/THU-MAIC/OpenMAIC>
- Use ACCESS_CODE for a shared instance rather than leaving its generated classrooms and API routes open.
  — <https://github.com/THU-MAIC/OpenMAIC>

## Superseded by this

- 2026-06-28 — AGPL-3.0 commercial-licensing guidance is obsolete: v0.3.0 relicensed OpenMAIC under MIT.
- 2026-06-28 — guidance assuming interactive widgets may use same-origin iframe access is obsolete; that sandbox permission was removed.

## Still unknown

- The exact capability set and commit at the 2026-03-16 launch cannot be reconstructed from a launch-tagged source: the first tagged release is v0.1.0 on 2026-03-26.
- The hosted service was not used as evidence because its page did not expose readable content during review.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/THU-MAIC/OpenMAIC | THU-MAIC/OpenMAIC repository and current setup guide | 2026-09-05 |
| https://raw.githubusercontent.com/THU-MAIC/OpenMAIC/main/CHANGELOG.md | OpenMAIC changelog | 2026-09-05 |
| https://shangqingtu.github.io/ | Shangqing Tu — News | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:openmaic`, thread `openmaic-development`, 1 dated events 2026-03-16 → 2026-03-16.
- **Practical note:** As of 2026-03-16, practitioners can use the referenced GitHub repository and project website as the identified OpenMAIC resources; no specific capability, release, or usage guidance is established by the supplied evidence.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
