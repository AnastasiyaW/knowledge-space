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

Base44 is a managed backend and application builder with autonomous background agents.

- Applications and hosting: creates web applications with managed hosting and custom frontends.
- Backend infrastructure: provides databases, user authentication, and server functions.
- Superagents: runs persistent background workers on schedules or incoming events.
- Integrations: connects external services to workspace logic.

Agent access depends strictly on connected tools and their assigned permissions. The platform fits internal applications and bounded automations, but integration permissions require explicit design.

## Development line

- **2026-03-31 — Base44’s Superagent page and documentation were referenced.** Base44 added persistent agents with connections to Gmail, Calendar, Stripe, Slack, CRM, and more than 100 services. The company tested the feature with roughly 20% of users before launch. Current documentation defines the operating model. We configure the agent in chat with connectors, knowledge, and memory, then run scheduled tasks or connector triggers.

## What changed

2026-03-31 — Base44 moved Superagents from test to general availability. These persistent agents connect to Gmail, Calendar, Stripe, Slack, CRM, and more than 100 services. Base44 tested the feature with roughly 20% of users before general release. The documentation outlines the workflow. We build the agent in chat, assign connectors, knowledge, and memory, then run scheduled tasks or connector triggers.

## How to use this

From 2026-03-31 onward, treat Base44’s Superagent-labelled page as a discovery lead and consult the official documentation before choosing a workflow; do not assume a launch or capability change without follow-up evidence.

1. Create a Superagent in the Superagents section and describe the specific task in chat.
  — <https://docs.base44.com/superagents/creating-a-superagent>
2. Connect the required tool through Brain → Integrations and set the minimum required mode: read-only or manage.
  — <https://docs.base44.com/superagents/creating-a-superagent>
3. Add knowledge and skills, then configure a scheduled task or a connector trigger.
  — <https://docs.base44.com/Getting-Started/superagent>
4. For applications with custom frontends, install the CLI, create the backend, and connect the SDK client.
  — <https://docs.base44.com/developers/home>

## Best practices

- Start with a single recurring task and refine agent behavior in chat based on observed output.
  — <https://docs.base44.com/Getting-Started/superagent>
- Connect tools first and grant permissions separately; use read-only instead of manage for viewing data.
  — <https://docs.base44.com/superagents/creating-a-superagent>
- Store reference documents in Knowledge and working files in Files; they form separate agent context boundaries.
  — <https://docs.base44.com/Getting-Started/superagent>

## Superseded by this

- 2026-03-31 — Base44 expanded beyond application building by adding Superagents. A Superagent operates across the whole workspace, while an app agent stays bounded to a single application.

## Still unknown

- No official dated changelog entry from Base44 exists for 2026-03-31; a public post by the founder confirms the launch date and test participation, not a release note.
- The response format lacks fields for event findings and new events; the fact for 2026-03-31 stays under what changed. We added no new dated events without a reliable primary source.

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