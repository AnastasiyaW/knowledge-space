# Knowledge Space

Curated technical knowledge base across 22 domains. Built for LLM agents - dense, structured references that fit in a context window and give immediately actionable answers.

**558 articles | 4.2 MB | 22 domains**

[:fontawesome-brands-github: **GitHub Repository**](https://github.com/AnastasiyaW/knowledge-space){ .md-button .md-button--primary }

<div id="knowledge-graph"></div>

---

## What is this?

A knowledge base designed **primarily for AI agents** - structured so that RAG retrieval, MCP tools, and context injection return dense, actionable technical content instead of blog-style prose.

Each article is a concentrated extract: code examples, configuration patterns, gotchas, best practices. No filler, no "let me explain why this is important" - just the knowledge an agent needs to solve a real problem.

**Also useful for engineers** who want quick reference across 22 technical domains without wading through tutorials.

**Who it's for:**

- **LLM agents** - structured format optimized for RAG retrieval, [ConTree MCP](https://contree.nebius.com/), and context injection
- **Engineers** - quick lookup of patterns, commands, configurations across 22 domains
- **Teams** - shared knowledge base accessible via ConTree sandbox or direct file access

---

## How to use

**Search** (top bar) is the fastest way - find specific topics, commands, or patterns across all domains.

**Browse** the sidebar to explore by domain. Each domain contains 9-85 focused articles.

**For agents:** upload the repo into a [ConTree](https://contree.nebius.com/) sandbox and query it via MCP tools - search, read, analyze articles in an isolated environment. Or clone the repo directly - each article is a standalone `.md` file, easy to retrieve and inject into context.

**Key conventions:**

- Articles are **agent-optimized references** - dense, structured, no hand-holding
- `[[wiki-links]]` connect related concepts across domains (e.g., Kafka article links to Architecture patterns)
- Code examples are copy-paste ready
- Each article covers one focused topic - from a single CLI command to a complete system design pattern

---

## Domains

| Domain | Articles | Coverage |
|--------|:--------:|----------|
| **Data Science** | 85 | ML, statistics, neural networks, computer vision, NLP, math foundations |
| **Python** | 43 | Core language, FastAPI, Django, async, testing, packaging, microservices |
| **Web Frontend** | 40 | React, TypeScript, CSS, Figma, bundlers, accessibility |
| **DevOps** | 39 | Docker, Kubernetes, Terraform, CI/CD, monitoring, SRE |
| **Architecture** | 39 | Microservices, DDD, system design, API design, integration patterns |
| **Data Engineering** | 38 | ETL/ELT, Spark, Airflow, data warehouses, streaming, CDC |
| **Kafka** | 33 | Broker internals, consumers, producers, Streams, KSQL, Connect |
| **SQL & Databases** | 27 | PostgreSQL, MySQL, query optimization, migrations, indexing |
| **Linux CLI** | 25 | Shell scripting, filesystem, permissions, systemd, networking |
| **LLM & Agents** | 24 | RAG, fine-tuning, agent frameworks, prompt engineering, embeddings |
| **Java & Spring** | 21 | Spring Boot, JPA, microservices, Kotlin, Android |
| **BI & Analytics** | 21 | Tableau, Power BI, SQL analytics, dashboards, product analytics |
| **Algorithms** | 19 | Sorting, graphs, dynamic programming, data structures, complexity |
| **Security** | 18 | Web security, penetration testing, Active Directory, anti-fraud |
| **SEO & Marketing** | 16 | Technical SEO, keyword research, link building, AI-driven SEO |
| **Testing & QA** | 15 | Selenium, Playwright, API testing, CI integration, test design |
| **Rust** | 14 | Ownership, lifetimes, async, error handling, unsafe |
| **PHP** | 12 | Laravel, MVC, ORM, testing, PHP 8 features |
| **Node.js** | 10 | Event loop, streams, clusters, performance, design patterns |
| **iOS & Mobile** | 10 | SwiftUI, Swift, Android/Kotlin fundamentals |
| **Misc** | 9 | JavaScript, Go, competitive programming, interview prep |

---

## Knowledge Graph

Articles aren't isolated - they form a connected knowledge graph with cross-domain references:

- **558 nodes** (articles) with **2100+ edges** (cross-references)
- **68 topic communities** detected via graph analysis
- Queryable via [ConTree MCP](https://contree.nebius.com/) - upload the repo into a sandbox and search/read/analyze articles with full isolation
- Each article is a standalone `.md` file - easy to index, retrieve, and inject into LLM context

### Freshness Policy

Not all knowledge ages equally. Each domain has an update cycle based on how fast the field moves:

| Cycle | Domains | Why |
|-------|---------|-----|
| **Stable** (rarely changes) | Algorithms, Architecture, Linux CLI | Fundamentals don't change - a B-tree is a B-tree |
| **Yearly** | SQL, Kafka, Rust, Java/Spring, PHP, Node.js, Testing, BI, Data Engineering | Mature ecosystems with predictable release cycles |
| **Every 6 months** | Web Frontend, DevOps, LLM/RAG, iOS, Security, SEO | Fast-moving fields where best practices shift quickly |
| **Monthly** | Image Generation, Agent Frameworks | Bleeding edge - new models and tools every week |

Articles include version/date context where relevant (e.g., "PostgreSQL 17", "React 19", "Kubernetes 1.30").

---

## What makes this different

**Agent-first design.** Every article is structured for machine consumption: consistent headers, code blocks with language tags, pattern/anti-pattern sections, explicit gotchas. An LLM agent retrieving a Knowledge Vault article gets immediately actionable context - no parsing needed.

**Density over length.** A typical article packs the same information as a 2-hour video or a 30-page tutorial into 2-4 pages of pure reference text. Optimized for context window efficiency.

**Cross-domain connections.** Real engineering problems don't respect domain boundaries. Wiki-links connect Kafka consumer patterns to Architecture decisions, SQL optimization to Data Engineering pipelines, Security practices to DevOps configurations.

**Living knowledge base.** Continuously updated with new research and domain knowledge. Freshness policy ensures fast-moving fields stay current while stable foundations remain reliable.

---

## Related Projects

[:fontawesome-brands-github: **claude-code-skills**](https://github.com/AnastasiyaW/claude-code-skills){ .md-button }

Open-source collection of skills, architectural patterns, and best practices for Claude Code. If you're building with AI agents, this might be useful:

- **Multi-agent harness design** - Generator-Evaluator pattern, Sprint Contracts, context management
- **Proof loop verification** - spec freeze -> build -> evidence -> fresh verify cycle
- **Autoresearch** - iterative self-optimization with mechanical scoring
- **Structured reasoning** - premises, execution trace, conclusions for complex debugging
- **Context engineering** - surviving long sessions, post-compaction recovery, JIT retrieval
