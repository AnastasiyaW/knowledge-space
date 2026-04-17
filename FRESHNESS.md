---
title: Knowledge Freshness Map
type: meta
updated: 2026-03-30
---

# Knowledge Freshness Map

How fast each domain's content goes stale. Determines re-generation priority.

## Stability Tiers

### Tier 1: Foundational (5-10+ years stable)

Core CS and math - changes rarely, if ever.

| Domain | Why stable |
|--------|-----------|
| `algorithms/` | Dijkstra doesn't get patches. Sorting is sorting. |
| `data-science/` (math parts) | Linear algebra, probability, statistics, gradient descent - textbook material |
| `architecture/` | CAP theorem, CQRS, event sourcing - patterns, not tools |
| `linux-cli/` | Bash, permissions, pipes - unchanged since the 90s |

### Tier 2: Slow-moving (2-5 years stable)

Established tools with backward compatibility. New versions add features, don't break old ones.

| Domain | Why slow | Watch for |
|--------|----------|-----------|
| `sql-databases/` | SQL standard barely moves. PostgreSQL/MySQL add features gradually | Major version releases (PG 18, MySQL 9) |
| `kafka/` | Kafka protocol stable, KRaft migration is the big shift | KRaft becoming default, new KIPs |
| `rust/` | Edition-based evolution, strong backward compat | New edition (2024), async trait stabilization |
| `java-spring/` | Spring Boot 3.x cycle, Java LTS releases | Spring Boot 4, Java 25 LTS |
| `php/` | Laravel major versions annually, PHP slow evolution | Laravel 12, PHP 9 |
| `nodejs/` | Design patterns don't expire. Node LTS cycle | Node 24 LTS, new permissions API |
| `testing-qa/` | pytest/Playwright stable APIs | Playwright major versions |
| `bi-analytics/` | Tableau updates, but core viz principles stay | Tableau Cloud changes |
| `data-engineering/` | Spark/Airflow mature. Iceberg/Delta evolving | Table format wars, Spark 4 |

### Tier 3: Fast-moving (6-18 months before stale)

Active development, frequent breaking changes, new tools replacing old ones.

| Domain | Why fast | Watch for |
|--------|----------|-----------|
| `web-frontend/` | React 19+, new CSS features, build tool churn | React Server Components, CSS nesting adoption |
| `devops/` | K8s releases quarterly, Terraform licensing shifts | OpenTofu, K8s Gateway API replacing Ingress |
| `llm-agents/` (RAG, embeddings, prompting) | Techniques evolve but core ideas hold | New retrieval patterns, embedding models |
| `ios-mobile/` | SwiftUI changes every WWDC, yearly iOS updates | WWDC 2026, Swift 6 concurrency |
| `security/` | New CVEs daily, anti-fraud arms race | New attack vectors, browser privacy changes |
| `seo-marketing/` | Google algorithm updates, AI Overviews disruption | Core updates, SGE/AI Overviews expansion |

### Tier 4: Ephemeral (monthly updates)

Built from cutting-edge material. Already partially outdated by the time it's generated.

| Domain | Status | Action needed |
|--------|--------|---------------|
| `image-generation/` | Models release weekly. FLUX Kontext, Step1X-Edit - some already superseded | Monthly from latest papers/repos |
| `llm-agents/` (agents, frameworks) | LangChain/LangGraph/CrewAI rewrite constantly. Agent patterns from 3 months ago are already legacy | Monthly - track framework releases |

## Re-generation Schedule

| Frequency | Domains |
|-----------|---------|
| **Never** (until fundamentals change) | algorithms, data-science (math), architecture, linux-cli |
| **Yearly** | sql-databases, kafka, rust, java-spring, php, nodejs, testing-qa, bi-analytics, data-engineering |
| **Every 6 months** | web-frontend, devops, llm-agents (RAG, embeddings, prompting), ios-mobile, security, seo-marketing |
| **Monthly** | image-generation, llm-agents (agent frameworks, function calling, multi-agent) |
## How to Update a Domain

1. Submit a PR with new or updated articles in `docs/{domain}/`
2. Follow the format rules in `AGENTS.md` and `CONTRIBUTING.md`
3. CI validates format, wiki-links, freshness, and deploys on merge to master
