---
title: Ouroboros — Public project updates
category: projects
date: 2026-08-02
tags: [ouroboros, project, public-project-updates]
aliases: ["Ouroboros"]
---

# Ouroboros — Public project updates

**Development line:** `project:ouroboros` · thread `public-project-updates`  
**Last event:** 2026-08-02 · 1 dated since 2026-08-02 · **Researched:** 2026-09-07 · confidence: medium

## What it is

Ouroboros is a desktop and headless AI-agent runtime, not a model.

- Local memory: keeps project history and durable memory on disk.
- Model runner: runs configured remote models or a local GGUF model.
- Coordinator: manages specialist agents across tasks.
- Self-modification: alters its own implementation through review gates.

It requires a configured model provider or local model, and self-modification makes it a high-trust local environment.

Use it for isolated, reviewable coding and research work; do not treat it as an unattended network service.

## Development line

- **2026-08-02 — Ouroboros public source and release reference.** On 2026-08-02, an Ouroboros entry linked the GitHub repository and its releases/latest page alongside external technical and community references. The link bundle marks a public reference point, while leaving the exact release, change set, and authorship unverified.

## What changed

- 2026-07-31 — A public architecture-and-benchmark report appeared; v6.87.5 shipped platform packages with a historically limited artifact-proof boundary.
- 2026-08-02 — Source links mention Ouroboros, but the missing message body makes no release, model, or benchmark claim.
- 2026-08-07 — v6.90.0 tightened provider routes, quotas, delegation, and panic stops.
- 2026-08-08 — A technical report formalized reviewed core evolution and separated frozen benchmark snapshots from the live Hope lineage.
- 2026-08-21 — v6.109.0 added live task-cost status and ready-on-open agent accounts.
- 2026-09-01 — v6.114.0 became the stable release, adding capability-preservation checks and shape-based OpenRouter failover.
- 2026-09-05 — v7.0.0-rc.15 shipped as a prerelease with a concurrent-boot ledger-race fix without replacing the stable channel.

## How to use this

1. Download the current stable package for the target platform rather than cloning source for ordinary use.
  — <https://github.com/razzant/ouroboros/releases/latest>
2. On first launch, configure a supported remote provider or local GGUF model, then set the review policy and budget.
  — <https://github.com/razzant/ouroboros>
3. Run a bounded task through the desktop app or `ouroboros run --start`; keep external work in a separate Git worktree and export a patch when appropriate.
  — <https://github.com/razzant/ouroboros>
4. Use source mode only for development, modification, or lock-verified testing: sync the locked environment, start the server, then use the local UI or CLI.
  — <https://github.com/razzant/ouroboros>

## Best practices

- Stay on the latest stable release by default; treat v7 release candidates as test builds until one is marked stable.
  — <https://github.com/razzant/ouroboros/releases>
- Keep the server on loopback. A non-local bind needs `OUROBOROS_NETWORK_PASSWORD` or already-authenticated private ingress; never expose the password bypass on an open LAN or public port.
  — <https://github.com/razzant/ouroboros/blob/main/docs/DEPLOYMENT.md>
- Use the configured budget and review controls before allowing core changes, because the runtime can alter its own code, prompts, tools, and dependencies.
  — <https://github.com/razzant/ouroboros>
- For core contributions, keep one focused change, test a committed diff, and obtain a separate-context review with recorded evidence.
  — <https://github.com/razzant/ouroboros/blob/main/CONTRIBUTING.md>

## Superseded by this

- 2026-08-02 — Treating the mutable `/releases/latest` link as evidence of an August release is obsolete; use a date-pinned tag for historical release claims.
- 2026-08-02 — “Beats Codex and Claude Code” is too broad as operating guidance: the reported comparisons depend on model and harness, and the July report described parity on GAIA and SWE-bench Pro.
- 2026-09-01 — Installation advice based on v6.87.5 or v6.90.0 is superseded by stable v6.114.0; v7.0.0-rc.15 remains a prerelease.

## Still unknown

- The original 2026-08-02 message text is unavailable, so no release, model, or benchmark claim can safely be attached to that date beyond a source-linked project mention.
- The linked public report is dated 2026-07-31, and the mutable latest-release URL now resolves to a 2026-09-01 release; neither can be backdated to the event.
- Benchmark results remain author-reported and were not independently reproduced here. The July report gives 86.97% for the named Terminal-Bench configuration, while the August paper reports 86.74%.
- No verified Simplified-Chinese first-party guidance for this specific repository was located. The name Ouroboros is also used by unrelated projects, so future identity resolution should retain the `razzant/ouroboros` repository anchor.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/razzant/ouroboros | GitHub - razzant/ouroboros: Ouroboros — self-creating AI agent. Born Feb 16, 2026. | 2026-09-07 |
| https://habr.com/ru/companies/airi/articles/1065428/ | Мой агент Ouroboros побил Codex с Claude Code на Terminal-Bench, OSWorld и CL-Bench. Он написал себя сам / Хабр | 2026-09-07 |
| https://github.com/razzant/ouroboros/releases/latest | Release v6.114.0 · razzant/ouroboros · GitHub | 2026-09-07 |
| https://github.com/razzant/ouroboros/releases/tag/v6.87.5 | Release v6.87.5 · razzant/ouroboros · GitHub | 2026-09-07 |
| https://github.com/ANative-Lab/Awesome-Self-Evolving-Agents/issues/74 | Scope check: Ouroboros, reviewed self-modifying agent runtime · Issue #74 | 2026-09-07 |
| https://github.com/razzant/ouroboros/releases/tag/v6.90.0 | Release v6.90.0 · razzant/ouroboros · GitHub | 2026-09-07 |
| https://arxiv.org/abs/2608.08311 | Ouroboros: A Self-Developing Frontier Coding Agent with Reviewed Core Evolution | 2026-09-07 |
| https://github.com/razzant/ouroboros/releases | Releases · razzant/ouroboros · GitHub | 2026-09-07 |
| https://github.com/razzant/ouroboros/releases/tag/v6.114.0 | Release v6.114.0 · razzant/ouroboros · GitHub | 2026-09-07 |
| https://github.com/razzant/ouroboros/blob/main/docs/DEPLOYMENT.md | ouroboros/docs/DEPLOYMENT.md at main · razzant/ouroboros · GitHub | 2026-09-07 |
| https://github.com/razzant/ouroboros/blob/main/CONTRIBUTING.md | ouroboros/CONTRIBUTING.md at main · razzant/ouroboros · GitHub | 2026-09-07 |

## Agent brief {#agent-brief}

- **Subject:** `project:ouroboros`, thread `public-project-updates`, 1 dated events 2026-08-02 → 2026-08-02.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
