---
title: Base44 — Superagent
category: projects
date: 2026-03-31
tags: [base44, project, superagent]
aliases: ["Base44"]
---

# Base44 — Superagent

**Development line:** `project:base44` · thread `superagent`  
**Last event:** 2026-03-31 · 1 dated since 2026-03-31 · **Researched:** 2026-09-05 · confidence: medium

## What it is

Base44 is a managed backend and AI app builder for internal tools and automated workflows.

- Applications, databases, authentication, server functions, integrations, and hosting.
- Superagents for scheduled actions and event-driven tasks.

Agent access is bounded by connected tools and their permissions. We can use it for quick internal apps and scoped automations, but integration permissions must be planned separately.

## Development line

- **2026-03-31 — Base44’s Superagent page and documentation were referenced.** Persistent agents connect to Gmail, Calendar, Stripe, Slack, CRM, and over 100 services. Base44 tested the feature with roughly 20% of users before release. Current documentation outlines the model. We build the agent in chat, attach connectors, knowledge, and memory, and run scheduled tasks or connector triggers.

## What changed

2026-03-31 — Base44 moved Superagents from test to general availability. Persistent agents connect to Gmail, Calendar, Stripe, Slack, CRM, and over 100 services. Base44 tested the feature with roughly 20% of users before release. Documentation outlines the workflow: we build the agent in chat, add connectors, knowledge, and memory, then set up scheduled tasks or connector triggers.

## How to use this

From 2026-03-31 onward, treat Base44’s Superagent-labelled page as a discovery lead and consult the official documentation before choosing a workflow; do not assume a launch or capability change without follow-up evidence.

1. Create a Superagent in the Superagents section and describe the first task in chat.
  — <https://docs.base44.com/superagents/creating-a-superagent>
2. Connect the tool through Brain → Integrations and grant the minimum permissions needed: read-only or manage.
  — <https://docs.base44.com/superagents/creating-a-superagent>
3. Add knowledge and skills, then set up a scheduled task or a connector trigger.
  — <https://docs.base44.com/Getting-Started/superagent>
4. Install the CLI, create a backend, and connect the SDK client when building an app with a custom frontend.
  — <https://docs.base44.com/developers/home>

## Best practices

- Start with one recurring task, then refine agent behavior in chat based on observed results.
  — <https://docs.base44.com/Getting-Started/superagent>
- Connect tools first, then grant permissions separately; use read-only instead of manage to inspect data.
  — <https://docs.base44.com/superagents/creating-a-superagent>
- Keep reference documents in Knowledge and working files in Files, so context boundaries stay clean.
  — <https://docs.base44.com/Getting-Started/superagent>

## Superseded by this

- 2026-03-31 — Base44 added Superagents alongside the app builder. A Superagent operates across the workspace, while an app agent stays inside its own app.

## Still unknown

- Base44 has no official dated changelog entry for the 2026-03-31 event. A founder's public post confirms the launch date and test group size, not a release note.
- The response schema lacks fields for event_findings and new_events; the 2026-03-31 finding is included in what_changed. We added no new dated events without a primary source.

## Sources

| source | title | read |
|---|---|---|
| https://www.linkedin.com/posts/maorshlomo_were-launching-base44-superagents-today-activity-7437524930801369088-xFcd | Introducing Base44 Superagents: AI Agents for Everyone | 2026-09-05 |
| https://docs.base44.com/Getting-Started/superagent | Building a Superagent | 2026-09-05 |
| https://docs.base44.com/superagents/creating-a-superagent | Creating a Superagent | 2026-09-05 |
| https://docs.base44.com/developers/home | Base44 Developer Platform | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:base44`, thread `superagent`, 1 dated events 2026-03-31 → 2026-03-31.
- **Practical note:** From 2026-03-31 onward, treat Base44’s Superagent-labelled page as a discovery lead and consult the official documentation before choosing a workflow; do not assume a launch or capability change without follow-up evidence.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
