---
title: Windows-Copilot-API
category: projects
date: 2026-06-22
tags: [project, windows-copilot-api, windows-copilot-api-development]
aliases: ["Windows-Copilot-API"]
---

# Windows-Copilot-API

**Development line:** `project:windows-copilot-api` · thread `windows-copilot-api-development`  
**Last event:** 2026-06-22 · 1 dated since 2026-06-22 · **Researched:** 2026-09-06 · confidence: high

## What it is

Windows-Copilot-API is an unofficial cross-platform bridge. It turns a signed-in consumer Copilot session into Python calls or a local OpenAI-compatible chat endpoint.

- Python chat, streaming, and conversation IDs
- Local `/v1/chat/completions` and `/v1/models` endpoints
- Browser sign-in and a persisted local session

## Development line

- **2026-06-22 — Windows-Copilot-API repository and Microsoft Copilot site were linked.** On 2026-06-22, public links connected the Windows-Copilot-API GitHub repository alongside Microsoft's Copilot website. This establishes a dated public reference point for the project's development line, but does not establish a release, feature set, ownership, or deployment status. No original source text or independent corroborating evidence was provided.

## What changed

- 2026-06-22 — Windows-Copilot-API added Docker deployment, rate limiting, host/port handling fixes, troubleshooting material, and a CLI fix. The core local/OpenAI-compatible bridge had already landed on 2026-06-19.
- 2026-06-23 — A patch-and-diagnostic update landed.
- 2026-06-24 — Sign-in expanded to Google as well as Microsoft accounts, and automatic Cloudflare-clearance handling landed.

The repository lists no GitHub releases, so commits—not release versions—are the reliable historical anchors.

## How to use this

1. Do not route a live consumer-Copilot workload through this project: the consumer terms say not to use tools or computer programs, such as bots or scrapers, to access Copilot.
  — <https://www.microsoft.com/en-us/microsoft-copilot/for-individuals/termsofuse>
2. For a supported Microsoft 365 integration, use the separate Microsoft 365 Copilot APIs: obtain the required Microsoft 365 Copilot and E3/E5-equivalent licensing, register an Entra application, acquire a user token, and call the Graph `/copilot` API surface.
  — <https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/copilot-apis-overview>
3. For historical code analysis, pin the 2026-06-22 commit state; do not attribute the later Google-login or automatic-clearance behavior to that date.
  — <https://github.com/sums001/Windows-Copilot-API/commits/master/>

## Best practices

- Treat consumer access as disallowed rather than as a production fallback. Microsoft explicitly bars programmatic bot or scraper access to Copilot.
  — [Microsoft Copilot Terms of Use](https://www.microsoft.com/en-us/microsoft-copilot/for-individuals/termsofuse)
- Do not treat mutable `master` as a release artifact. Pin a commit SHA because the repository has no GitHub releases.
  — [Windows-Copilot-API releases](https://github.com/sums001/Windows-Copilot-API/releases)
- When reviewing historical mechanics, keep later OAuth and automatic-clearance changes separate from the 2026-06-22 state.
  — [Windows-Copilot-API commit history](https://github.com/sums001/Windows-Copilot-API/commits/master/)
- Choose the licensed Microsoft Graph Copilot APIs when we require supported enterprise integration with Microsoft 365 data and governance.
  — [Microsoft 365 Copilot APIs overview](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/copilot-apis-overview)

## Superseded by this

- 2026-06-12 — Guidance to use this bridge against consumer Copilot is superseded. Explicit consumer terms ban tools, computer programs, bots, and scrapers for Copilot access.
- 2026-06-24 — Microsoft-account-only setup guidance is superseded. The repository updated sign-in to support both Microsoft and Google accounts.
- 2026-06-24 — Pre-automation Cloudflare-clearance guidance is superseded for interactive clients by automatic clearance handling. Headless service use still depends on an out-of-band visible-browser re-login when clearance expires.

## Still unknown

- The repository’s About text claims GPT-4 and GPT-5 access, but its detailed README exposes one generic `copilot` model with no model picker; the exact upstream model cannot be verified.
- The current README is mutable and the repository has no GitHub releases, so current behavior cannot be backdated to 2026-06-22 without a commit-specific inspection.
- GitHub’s history view establishes calendar dates, not enough timestamp or timezone detail to order the several 2026-06-22 commits precisely.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/sums001/Windows-Copilot-API | Windows-Copilot-API repository | 2026-09-06 |
| https://copilot.microsoft.com/ | Microsoft Copilot | 2026-09-06 |
| https://github.com/sums001/Windows-Copilot-API/commits/master/ | Windows-Copilot-API commit history | 2026-09-06 |
| https://github.com/sums001/Windows-Copilot-API/blob/master/README.md | Windows-Copilot-API README | 2026-09-06 |
| https://github.com/sums001/Windows-Copilot-API/commit/dfbe3a91112640db7ff991511cf00d3176d80d53 | Google + msft account oauth commit | 2026-09-06 |
| https://github.com/sums001/Windows-Copilot-API/commit/878a2ff1ec5607b5c417a57a9ff0a7daa6e5b48e | Automatic CF clearance commit | 2026-09-06 |
| https://github.com/sums001/Windows-Copilot-API/releases | Windows-Copilot-API releases | 2026-09-06 |
| https://www.microsoft.com/en-us/microsoft-copilot/for-individuals/termsofuse | Microsoft Copilot Terms of Use | 2026-09-06 |
| https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/copilot-apis-overview | Microsoft 365 Copilot APIs overview | 2026-09-06 |

## Agent brief {#agent-brief}

- **Subject:** `project:windows-copilot-api`, thread `windows-copilot-api-development`, 1 dated events 2026-06-22 → 2026-06-22.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
