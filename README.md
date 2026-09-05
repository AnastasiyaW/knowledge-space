# <img src="docs/assets/favicon-animated.gif" width="28" height="28" alt="logo"> Happyin Knowledge Space

A curated technical reference across 28 domains — Kafka, Python, SQL, ML, security, image generation, and more — written so AI agents and engineers get dense, runnable answers instead of tutorial prose.

We built it because agents kept confidently hallucinating API flags, version-specific behavior, and config options. Point your Claude, Cursor, or any RAG pipeline at this repo and it gets a reliable source to check against.

**975+ articles | 28 domains | 3134+ cross-references**

[![Live site](https://img.shields.io/badge/Live_site-happyin.space-FFD740?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA2NCA2NCI+PGNpcmNsZSBjeD0iMjgiIGN5PSIyMiIgcj0iOSIgZmlsbD0iI2JiODZmYyIvPjxjaXJjbGUgY3g9IjQyIiBjeT0iMzAiIHI9IjciIGZpbGw9IiMwM2RhYzYiLz48Y2lyY2xlIGN4PSIxOCIgY3k9IjQwIiByPSI2IiBmaWxsPSIjZmY3NTk3Ii8+PC9zdmc+)](https://happyin.space/)

## What's inside

| Domain | Articles | Coverage |
|--------|:--------:|----------|
| `projects/` | 85 | One page per tool, model or product the news conveyor follows: dated development line, current use, obsolete guidance, sources |
| `image-generation/` | 77 | Diffusion models, flow matching, LoRA training, inpainting, tiled inference |
| `llm-agents/` | 71 | RAG, fine-tuning, agent frameworks, prompt engineering, multi-agent |
| `security/` | 61 | Web security, pentesting, Active Directory, anti-fraud, model protection, CWE |
| `data-science/` | 57 | ML, statistics, neural networks, CV, NLP, math foundations |
| `devops/` | 47 | Docker, Kubernetes, Terraform, CI/CD, monitoring, SRE, observability |
| `kafka/` | 43 | Broker internals, consumers, producers, Streams, KSQL, Connect, replication |
| `organizations/` | 38 | One page per company or lab: leadership and structure changes, product lines, what each change made obsolete |
| `architecture/` | 37 | Microservices, DDD, system design, API patterns, CQRS |
| `web-frontend/` | 36 | React, TypeScript, CSS, Figma, bundlers, accessibility, JS async |
| `data-engineering/` | 34 | ETL/ELT, Spark, Airflow, data warehouses, streaming, CDC, vector search |
| `algorithms/` | 33 | Sorting, graphs, DP, data structures, complexity analysis |
| `python/` | 33 | Core language, FastAPI, Django, async, testing, stdlib, web scraping |
| `sql-databases/` | 33 | PostgreSQL, MySQL, query optimization, migrations, indexing, advanced |
| `ios-mobile/` | 31 | SwiftUI, Swift, Android/Kotlin fundamentals, mobile ML |
| `cpp/` | 29 | Modern C++, memory, templates, concurrency, cross-platform ML |
| `linux-cli/` | 29 | Shell scripting, filesystem, systemd, permissions, networking |
| `java-spring/` | 25 | Spring Boot, JPA, microservices, Kotlin, Android |
| `seo-marketing/` | 25 | Technical SEO, keyword research, link building, AI-driven SEO |
| `testing-qa/` | 25 | Selenium, Playwright, API testing, CI integration, browser automation |
| `bi-analytics/` | 23 | Tableau, Power BI, SQL analytics, dashboards, product analytics |
| `rust/` | 22 | Ownership, lifetimes, async, error handling, unsafe |
| `nodejs/` | 16 | Event loop, streams, clusters, performance, design patterns |
| `php/` | 15 | Laravel, MVC, ORM, testing, PHP 8 features |
| `audio-voice/` | 14 | TTS, ASR, voice cloning, speech synthesis, TTS fine-tuning |
| `writing/` | 14 | Technical article structure, SEO for articles, LLM anti-patterns |
| `llm-memory/` | 13 | Memory architectures, session persistence, knowledge graphs |
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
