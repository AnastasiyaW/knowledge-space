---
title: "DataLens Platform: datalens-platform-ai-agents — Datalens Platform Ai Agents"
category: "projects"
date: 2026-11-26
tags: ["datalens-platform", "datalens-platform-ai-agents", "project"]
aliases: ["DataLens Platform: datalens-platform-ai-agents"]
---

# DataLens Platform: datalens-platform-ai-agents — Datalens Platform Ai Agents

**Development line:** project:datalens-platform · thread datalens-platform-ai-agents  
**Last event:** 2026-11-26 · 2 dated since 2026-11-26 · **Researched:** 2026-11-27 · confidence: medium

## What it is

DataLens Platform is Yandex B2B Tech's BI and analytics service, a competitor to Apache Superset and Microsoft Power BI.

It now has autonomous AI agents and built-in Neuroanalyst assistants across data engineering and visualization. Abilities:

- Natural-language control: connects data sources and loads records into Lakehouse storage
- Generation and debugging: calculated fields, charts and complete multi-widget dashboards
- External agent access: a Model Context Protocol server (@datalens-tech/mcp) that calls the public API
- Domain context: modular skills (datalens-skills) that encode corporate metrics
- Pipelines as code: a type-safe Python SDK (datalens-sdk)

The service runs inside cloud security boundaries. Analytical prompts and schema metadata do not train public foundational models. Natural-language generation is still limited by database dialect compatibility and schema complexity. Agent harnesses and production BI infrastructure are linked end to end.

## Development line

- **2026-11-26 — DataLens Platform adds AI agents for end-to-end data work.** Yandex B2B Tech updated the DataLens Platform analytics service. Its built-in Neuro-analyst and external AI agents can now do data tasks at every stage from natural-language requests. That covers connecting data sources, loading data into a Lakehouse storage, and building dashboards.
- **2026-11-26 — DataLens Platform adds AI agents for end-to-end data work.** Yandex B2B Tech updated DataLens Platform so AI agents can handle data tasks from connecting sources to building dashboards. Skills carry company-specific rules. More than 50 companies got early access, and a public SaaS release was planned for December.
- **2026-11-26 — other reporting on this date.**
  - The update has three integration tiers. The protocol layer is the @datalens-tech/mcp Model Context Protocol server exposing api.datalens.tech. The domain knowledge layer is datalens-skills packages that encode corporate business logic. The code layer is datalens-sdk for Python. Agent interactions run inside enterprise cloud security boundaries, with no model training on client queries. (2026-11-26) — <https://habr.com/ru/companies/yandex_cloud_and_infra/articles/1112340/>
  - The closed enterprise preview enrolled over 50 client organizations. They test automated Lakehouse data ingestion and dashboard generation before a broad commercial SaaS rollout across Yandex Cloud in December 2026. (2026-11-26) — <https://kod.ru/datalens-platform-ii-agenty>

## What changed

DataLens Platform moved from manual visualization authoring to an agent-driven data platform. It added the built-in Neuroanalyst and layers for external AI agents. Three pieces came with it: a Model Context Protocol server for direct tool-based API calls, modular skill packages for enterprise metrics, and a Python SDK for automation. A natural-language instruction can now run the whole path, from Lakehouse data ingestion to a published dashboard.

## How to use this

1. Connect agent environments or coding assistants to DataLens through the @datalens-tech/mcp Model Context Protocol server, configured for api.datalens.tech.
  — <https://habr.com/ru/companies/yandex_cloud_and_infra/articles/1112340/>
2. Load business definitions and calculation rules with datalens-skills packages, so the agent reasons by internal reporting standards.
  — <https://habr.com/ru/companies/yandex_cloud_and_infra/articles/1112340/>
3. Ask the agent or the built-in Neuroanalyst in natural language to connect database sources, load tables into Lakehouse storage and create dataset models.
  — <https://habr.com/ru/companies/yandex_cloud_and_infra/articles/1112340/>
4. Ask the agent to generate calculated fields, configure visualization widgets and deploy complete dashboards across target workbooks.
  — <https://habr.com/ru/companies/yandex_cloud_and_infra/articles/1112340/>

## Best practices

- Write metric calculations and KPI business rules into datalens-skills packages, so the agent does not hallucinate when it generates calculated fields.
  — <https://habr.com/ru/companies/yandex_cloud_and_infra/articles/1112340/>
- Set workspace-level and report-level AI permissions, so automated schema inspection stays away from sensitive data sources.
  — <https://habr.com/ru/companies/yandex_cloud_and_infra/articles/1112340/>
- Export agent-generated dashboard definitions and dataset schemas with datalens-sdk into version-controlled repositories, so a rollback is deterministic.
  — <https://habr.com/ru/companies/yandex_cloud_and_infra/articles/1112340/>

## Superseded by this

- Dataset preparation, calculated field authoring and dashboard construction in DataLens needed manual UI work or custom scripts. There was no protocol-level agent orchestration.
  — <https://habr.com/ru/companies/yandex_cloud_and_infra/articles/1112340/>

## Still unknown

- Canonical documentation paths on yandex.cloud, mozgi.io and kt.team were hidden behind search-engine grounding redirects. They could not be independently verified without web fetching.
- The model checkpoints and inference pricing behind the Yandex Cloud AI Studio agent runtime were not disclosed in the initial release materials.
- Independent community benchmarks and external developer postmortems are not available during the closed enterprise preview.

## Sources

| source | title | read |
|---|---|---|
| https://habr.com/ru/companies/yandex_cloud_and_infra/articles/1112340/ | DataLens Platform: AI-агенты для сквозной работы с данными | 2026-11-27 |
| https://kod.ru/datalens-platform-ii-agenty | В DataLens Platform появились ИИ-агенты для сквозной работы с данными | 2026-11-27 |

## Agent brief {#agent-brief}

- **Subject:** project:datalens-platform, thread datalens-platform-ai-agents, 2 dated events 2026-11-26 → 2026-11-26.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
