# <img src="docs/assets/favicon-animated.gif" width="32" height="32" alt="logo" style="vertical-align: middle;"> <span><img src="https://readme-typing-svg.demolab.com?font=Inter&weight=800&size=28&pause=99999&color=BB86FC&vCenter=true&width=120&height=32&lines=Happyin" alt="Happyin" height="28"></span> <span><img src="https://readme-typing-svg.demolab.com?font=Inter&weight=800&size=28&pause=99999&color=03DAC6&vCenter=true&width=180&height=32&lines=Knowledge" alt="Knowledge" height="28"></span> <span><img src="https://readme-typing-svg.demolab.com?font=Inter&weight=800&size=28&pause=99999&color=FF7597&vCenter=true&width=90&height=32&lines=Space" alt="Space" height="28"></span>

Curated technical knowledge base across 22 domains. Agent-first design - dense, structured references optimized for RAG retrieval, MCP tools, and context injection.

**560 articles | 22 domains | 2100+ cross-references**

**Live site:** [<img src="https://readme-typing-svg.demolab.com?font=Inter&weight=700&size=16&pause=99999&color=FFD740&vCenter=true&width=160&height=22&lines=happyin.space+%E2%86%97" alt="happyin.space" height="18">](https://happyin.space/)

## What's inside

| Domain | Articles | Coverage |
|--------|:--------:|----------|
| `data-science/` | 85 | ML, statistics, neural networks, CV, NLP, math foundations |
| `python/` | 43 | Core language, FastAPI, Django, async, testing, packaging |
| `web-frontend/` | 40 | React, TypeScript, CSS, Figma, bundlers, accessibility |
| `devops/` | 39 | Docker, Kubernetes, Terraform, CI/CD, monitoring, SRE |
| `architecture/` | 39 | Microservices, DDD, system design, API patterns, CQRS |
| `data-engineering/` | 38 | ETL/ELT, Spark, Airflow, data warehouses, streaming, CDC |
| `kafka/` | 33 | Broker internals, consumers, producers, Streams, KSQL, Connect |
| `sql-databases/` | 27 | PostgreSQL, MySQL, query optimization, migrations, indexing |
| `linux-cli/` | 25 | Shell scripting, filesystem, systemd, permissions, networking |
| `llm-agents/` | 24 | RAG, fine-tuning, agent frameworks, prompt engineering, embeddings |
| `java-spring/` | 21 | Spring Boot, JPA, microservices, Kotlin, Android |
| `bi-analytics/` | 21 | Tableau, Power BI, SQL analytics, dashboards, product analytics |
| `algorithms/` | 19 | Sorting, graphs, DP, data structures, complexity analysis |
| `security/` | 18 | Web security, penetration testing, Active Directory, anti-fraud |
| `seo-marketing/` | 16 | Technical SEO, keyword research, link building, AI-driven SEO |
| `testing-qa/` | 15 | Selenium, Playwright, API testing, CI integration, test design |
| `rust/` | 14 | Ownership, lifetimes, async, error handling, unsafe |
| `php/` | 12 | Laravel, MVC, ORM, testing, PHP 8 features |
| `nodejs/` | 10 | Event loop, streams, clusters, performance, design patterns |
| `ios-mobile/` | 10 | SwiftUI, Swift, Android/Kotlin fundamentals |
| `image-generation/` | 27 | Diffusion models, flow matching, LoRA training, inpainting |
| `misc/` | 9 | JavaScript, Go, competitive programming, interview prep |

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

### What NOT to modify

These files are infrastructure - do not modify without explicit maintainer request:

- `mkdocs.yml` - site configuration
- `overrides/` - Jinja2 templates, SEO, 404 page
- `docs/javascripts/` - knowledge graph visualization
- `docs/stylesheets/` - site styling
- `docs/CNAME` - domain configuration
- `.github/workflows/` - CI/CD pipelines
- `.claude/rules/` - agent guardrails

## Site

The knowledge base is published as a searchable MkDocs Material site at [happyin.space](https://happyin.space/).

- Auto-deploys to Cloudflare Pages on push to `master`
- Interactive knowledge graph on the homepage
- Full-text search across all 560 articles
- Dark/light mode, SEO optimized

## Stats

```
Total articles:     560
Total domains:       22
Wiki links:       2,100+
Topic communities:   68
```

## License

MIT
