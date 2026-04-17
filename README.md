# <img src="docs/assets/favicon-animated.gif" width="28" height="28" alt="logo"> Happyin Knowledge Space

Curated technical knowledge base across 26 domains. Agent-first design - dense, structured references optimized for RAG retrieval, MCP tools, and context injection.

**771+ articles | 26 domains | 2100+ cross-references**

[![Live site](https://img.shields.io/badge/Live_site-happyin.space-FFD740?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA2NCA2NCI+PGNpcmNsZSBjeD0iMjgiIGN5PSIyMiIgcj0iOSIgZmlsbD0iI2JiODZmYyIvPjxjaXJjbGUgY3g9IjQyIiBjeT0iMzAiIHI9IjciIGZpbGw9IiMwM2RhYzYiLz48Y2lyY2xlIGN4PSIxOCIgY3k9IjQwIiByPSI2IiBmaWxsPSIjZmY3NTk3Ii8+PC9zdmc+)](https://happyin.space/)

## What's inside

| Domain | Articles | Coverage |
|--------|:--------:|----------|
| `security/` | 56 | Web security, pentesting, Active Directory, anti-fraud, model protection, CWE |
| `data-science/` | 55 | ML, statistics, neural networks, CV, NLP, math foundations |
| `image-generation/` | 50 | Diffusion models, flow matching, LoRA training, inpainting, tiled inference |
| `llm-agents/` | 49 | RAG, fine-tuning, agent frameworks, prompt engineering, multi-agent |
| `kafka/` | 42 | Broker internals, consumers, producers, Streams, KSQL, Connect, replication |
| `devops/` | 35 | Docker, Kubernetes, Terraform, CI/CD, monitoring, SRE, observability |
| `web-frontend/` | 34 | React, TypeScript, CSS, Figma, bundlers, accessibility, JS async |
| `data-engineering/` | 34 | ETL/ELT, Spark, Airflow, data warehouses, streaming, CDC, vector search |
| `architecture/` | 33 | Microservices, DDD, system design, API patterns, CQRS |
| `sql-databases/` | 32 | PostgreSQL, MySQL, query optimization, migrations, indexing, advanced |
| `ios-mobile/` | 31 | SwiftUI, Swift, Android/Kotlin fundamentals, mobile ML |
| `python/` | 30 | Core language, FastAPI, Django, async, testing, stdlib, web scraping |
| `algorithms/` | 29 | Sorting, graphs, DP, data structures, complexity analysis |
| `linux-cli/` | 27 | Shell scripting, filesystem, systemd, permissions, networking |
| `cpp/` | 27 | Modern C++, memory, templates, concurrency, cross-platform ML |
| `java-spring/` | 25 | Spring Boot, JPA, microservices, Kotlin, Android |
| `seo-marketing/` | 24 | Technical SEO, keyword research, link building, AI-driven SEO |
| `bi-analytics/` | 23 | Tableau, Power BI, SQL analytics, dashboards, product analytics |
| `testing-qa/` | 22 | Selenium, Playwright, API testing, CI integration, browser automation |
| `rust/` | 22 | Ownership, lifetimes, async, error handling, unsafe |
| `nodejs/` | 16 | Event loop, streams, clusters, performance, design patterns |
| `php/` | 15 | Laravel, MVC, ORM, testing, PHP 8 features |
| `llm-memory/` | 11 | Memory architectures, session persistence, knowledge graphs |
| `audio-voice/` | 10 | TTS, ASR, voice cloning, speech synthesis, TTS fine-tuning |
| `writing/` | 9 | Technical article structure, SEO for articles, LLM anti-patterns |
| `go/` | 9 | Goroutines, channels, modules, HTTP servers, microservices |

## For AI agents

### Quick access via sandbox

Upload the repo into a [ConTree](https://contree.dev/) sandbox (or any other isolated environment you prefer) and query it via MCP tools - search, read, and analyze articles:

```bash
# Upload to ConTree sandbox
contree upload --path ./docs

# Search across all domains
contree search "kafka consumer rebalancing"

# Read specific article
contree read docs/kafka/consumer-groups.md
```

### Direct file access

Clone and point your agent at it:

```bash
git clone https://github.com/AnastasiyaW/knowledge-space.git
```

Each article is a standalone `.md` file - easy to index, retrieve, and inject into LLM context. Articles cross-reference each other with `[[wiki-links]]` forming a navigable knowledge graph.

### Article format

Every article follows a consistent structure optimized for machine consumption:

```markdown
# Consumer Groups

## Key Facts
- Bullets with [[wiki links]]

## Patterns
[Code. Configs. Commands. Runnable.]

## Gotchas
[symptom -> cause -> fix]

## See Also
[Cross-references + official docs]
```

## Freshness policy

Not all knowledge ages equally. Each domain has an update cycle:

| Cycle | Domains |
|-------|---------|
| **Stable** (fundamentals) | Algorithms, Architecture, Linux CLI |
| **Yearly** | SQL, Kafka, Rust, Java/Spring, PHP, Node.js, Testing, BI, Data Engineering |
| **Every 6 months** | Web Frontend, DevOps, LLM/RAG, iOS, Security, SEO |
| **Monthly** | Image Generation, Agent Frameworks |

Articles include version context where relevant (e.g., "PostgreSQL 17", "React 19").

## Contributing

We accept contributions from both AI agents and humans. See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide.

**Quick version:**

1. Fork the repo
2. Create/update an article in `docs/{domain}/`
3. Follow the article format (dense reference, not tutorial)
4. Submit a PR

### For agents submitting findings

If you're an agent that discovered outdated or missing information:

1. **Branch**: `update/{domain}/{topic-slug}`
2. **Format**: follow the article structure above - compress, no filler
3. **PR**: include what changed, why, and source links
4. **Forbidden**: course names, instructor names, tutorial prose, marketing language

Automated validation checks run on every PR.

## License

MIT
