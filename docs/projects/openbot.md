---
title: OpenBot — Project development
category: projects

tags: [openbot, project, project-development]
aliases: ["OpenBot"]
---

# OpenBot — Project development

**Development line:** `project:openbot` · thread `project-development`  
**Last event:** - · 0 dated since - · **Researched:** 2026-09-05 · confidence: medium

## What it is

OpenBot is a template teams clone to run governed AG-UI coworkers on our own infrastructure instead of using a hosted agent.

- Bot isolation: gives each Bot its own browser profile, filesystem and granted tools.
- Policy gateway: routes browser, file and MCP actions through a fail-closed CEL check and audit trail.
- Agent support: accepts custom AG-UI agents as well as shipped proof-of-concept and LangGraph Bots.

It remains alpha software with no hosted version or installable package.

Use it when our team can own Docker, PostgreSQL, model credentials and access policy; do not treat it as a managed service.

## Development line

- The dated line is not written up yet; what is known stands below.

## What changed

- 2026-08-17 — v0.0.1 introduced the laptop-run alpha with isolated per-Bot computers, governed actions, AG-UI support and CopilotKit Intelligence threads.
- 2026-08-22 — v0.0.2–v0.0.4 made fresh-clone tool access usable while tightening the safety boundary: automatic local AGENT_TOOL_TOKEN generation, skill-based tool selection above 12 grants, audit visibility, fixed OpenAI-compatible routing, packaged skills and refusal of an unresolvable page reference.
- 2026-08-28 — v0.0.5 added administrator-granted Bot-to-Bot handoff and human escalation, repaired stuck tool-result conversations, and added Responses API streaming support for gpt-5.6-* models.

## How to use this

We record no practitioner workflow change as of 2026-08-22. Research the linked repository first and recover the source message to establish what changed.

1. Clone OpenBot and prepare Docker, Bun 1.3+, a CopilotKit Intelligence project, and a model credential.
  — <https://github.com/CopilotKit/openbot>
2. Copy .env.example to .env, use the CopilotKit CLI to obtain INTELLIGENCE_API_KEY, and set the model credential.
  — <https://github.com/CopilotKit/openbot>
3. Run bun install, then bash scripts/start.sh; open http://localhost:3010 after its health checks pass.
  — <https://github.com/CopilotKit/openbot>
4. Replace the example tenant package with brand.yaml, agents.yaml, channels.yaml, model.yaml and knowledge.yaml; add skills.yaml if needed.
  — <https://github.com/CopilotKit/openbot/blob/main/docs/configuration.md>
5. Create or connect coworkers from /agents, configure MCP servers and grants under /admin/plugins, and set browser/file/MCP rules under /admin/boundaries.
  — <https://github.com/CopilotKit/openbot>
6. Test a controlled browser action, add a deny rule, retry it, and inspect the permitted or refused action in /admin/audit.
  — <https://github.com/CopilotKit/openbot>

## Best practices

- Enable an identity provider before allowing other people in: default single-user mode treats every visitor as one administrator.
  — <https://github.com/CopilotKit/openbot>
- Keep tools least-privileged. Skills declare which tools to offer, but they do not grant access; Bot grants remain the effective boundary.
  — <https://github.com/CopilotKit/openbot/releases>
- Keep the default per-Bot computer isolation; use gVisor through COMPUTER_RUNTIME=runsc where the host supports it.
  — <https://github.com/CopilotKit/openbot>
- Treat policy and audit as an operating loop: test a denied action before granting it, then review the resulting audit trail.
  — <https://github.com/CopilotKit/openbot>
- For a released deployment, pin the container digest from container-images.json and verify its GitHub provenance attestation rather than deploying a mutable tag.
  — <https://github.com/CopilotKit/openbot/blob/main/docs/releasing.md>

## Superseded by this

- 2026-08-22 — Fresh laptop clones no longer need manual AGENT_TOOL_TOKEN provisioning when started with scripts/start.sh; deployments outside that script still fail closed without a token.
- 2026-08-22 — Offering every granted tool to Bots holding more than 12 tools is replaced by skill-matched offers plus unclaimed granted tools.
- 2026-08-22 — A browser action whose cited element cannot be resolved is no longer allowed through; the Bot must take a fresh snapshot.
- 2026-08-28 — gpt-5.6-* framework-Bot runs that silently dropped Responses API content blocks are replaced by handling for both streaming shapes.

## Still unknown

- The 2026-08-22 item carries only the repository URL, so its exact intended release cannot be identified; GitHub records v0.0.2, v0.0.3 and v0.0.4 on that date.
- OpenBot remains alpha and its README says the repository is a template rather than a hosted product, so production readiness for a particular deployment requires its own security and operations review.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/CopilotKit/openbot | OpenBot README | 2026-09-05 |
| https://github.com/CopilotKit/openbot/releases | Releases · CopilotKit/OpenBot | 2026-09-05 |
| https://github.com/CopilotKit/openbot/blob/main/docs/configuration.md | OpenBot configuration | 2026-09-05 |
| https://github.com/CopilotKit/openbot/blob/main/docs/releasing.md | OpenBot releasing guide | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:openbot`, thread `project-development`, 0 dated events - → -.
- **Practical note:** We advise no practitioner workflow change as of 2026-08-22; research the linked repository first and recover the source message to establish what changed.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.