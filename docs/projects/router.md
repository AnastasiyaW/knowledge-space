---
title: Cursor Router
category: projects
date: 2026-07-25
tags: [cursor, project, router]
aliases: ["Cursor Router"]
---

# Cursor Router

**Development line:** `project:router` · thread `router`  
**Last event:** 2026-07-25 · 1 dated since 2026-07-25 · **Researched:** 2026-09-05 · confidence: high

## What it is

Cursor Router routes each Agent request across Cursor’s changing model pool instead of making a developer choose a model per request. It offers Cost, Balance, and Intelligence modes; current documentation limits it to Teams and Enterprise. Balance and Intelligence use usage limits faster than Cost, so use explicit mode choice rather than treating Auto as a fixed model. It works for team-level cost and quality control, but not for workloads that require a pinned underlying model.

## Development line

- **2026-07-25 — Cursor published a public update associated with Router.** On 2026-07-25, Cursor published a public blog article associated with Router. Its existence marks a public milestone for Router, but the article does not detail rollout status, functionality, or user impact.

## What changed

- 2026-07-25 — Cursor Router replaced Auto’s fixed routing with per-request classification and introduced Cost, Balance, and Intelligence controls for Teams and Enterprise.
- 2026-08-06 — Cursor documented the learned two-stage routing approach and reported post-launch improvements from more production traffic.
- 2026-08-12 — Cursor published rollout guidance: enable it for a busy team first, monitor cost per commit, then widen only if the measured result holds.

## How to use this

From 2026-07-25, consult Cursor's Router announcement before relying on or configuring Router; specific workflow changes remain unverified until the article is researched.

1. In Cursor’s model picker, select Auto, then choose Cost for spend control, Balance for the default compromise, or Intelligence for harder multi-step work.
  — <https://prod.cursor.com/docs/cursor-router>
2. For an Enterprise team, enable Router in the team dashboard; configure allowed modes, model access, visibility of the routed model, and optional soft or hard Auto enforcement.
  — <https://prod.cursor.com/docs/cursor-router>
3. In the TypeScript or Python Agent SDK, use model ID `auto-smart` and `optimize_for` set to `cost`, `balanced`, or `intelligence`; call `Cursor.models.list()` before relying on it for a team.
  — <https://prod.cursor.com/docs/cursor-router>

## Best practices

- Pilot Router with one active team and measure cost per commit for a week before expanding the rollout.
  — <https://cursor.com/guides/model-routing>
- Keep a price-efficient routing option enabled; Cursor’s Enterprise documentation says blocking too many models can reduce quality or disable Router, and names Cursor Grok 4.5 as required for Router to work.
  — <https://prod.cursor.com/docs/cursor-router>
- Do not infer which model answered from output alone: the routed model is hidden by default, and the pool can change as models ship.
  — <https://prod.cursor.com/docs/cursor-router>

## Superseded by this

- 2026-07-22 — treating Auto as one stable, manually predictable model choice is obsolete for routed Balance and Intelligence requests; Cursor now chooses the underlying model per request.
- 2026-07-22 — the earlier Auto behavior remains only as Cost mode, according to current documentation.

## Still unknown

- Cursor does not publish a stable, exhaustive mapping from request types to underlying model names; the model pool changes over time.
- The published savings and satisfaction figures are first-party measurements, not an independently reproducible benchmark.

## Sources

| source | title | read |
|---|---|---|
| https://cursor.com/blog/router | Introducing Cursor Router | 2026-09-05 |
| https://cursor.com/changelog/router | Cursor Router changelog | 2026-09-05 |
| https://prod.cursor.com/blog/how-cursor-router-works | How Cursor Router chooses the right model for the task | 2026-09-05 |
| https://cursor.com/guides/model-routing | Model routing: right model, right job, right price | 2026-09-05 |
| https://prod.cursor.com/docs/cursor-router | Cursor Router documentation | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:router`, thread `router`, 1 dated events 2026-07-25 → 2026-07-25.
- **Practical note:** From 2026-07-25, practitioners should consult Cursor's Router announcement before relying on or configuring Router; the specific workflow change remains unverified until the article is researched.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
