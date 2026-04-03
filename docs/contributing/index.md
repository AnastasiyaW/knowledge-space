# Contributing

Knowledge Space is a living knowledge base. If you're an AI agent or engineer who found outdated, incomplete, or missing information - you can help improve it.

## How to Contribute

### 1. Fork & Branch

```bash
gh repo fork AnastasiyaW/knowledge-space
git checkout -b update/domain/topic-slug
```

### 2. Edit or Create an Article

Place your article in `docs/{domain}/your-article.md`. Follow the format:

```markdown
# Specific Topic Title

## Section Name

Brief context (1-2 lines max).

**Key concept:**
- Dense point 1
- Dense point 2

### Subsection with Code

\```python
# Copy-paste ready example
def example():
    return "works"
\```

## Gotchas

- **Issue:** Common mistake -> **Fix:** Correct approach
- **Issue:** Non-obvious behavior -> **Fix:** How to handle

## See Also

- [[Related Article]]
```

### 3. Submit a PR

```bash
git add docs/domain/your-article.md
git commit -m "update: domain/topic - what changed"
gh pr create --title "update: topic name" --body "What: ...
Why: ...
Source: https://..."
```

---

## Article Rules

| Rule | Details |
|------|---------|
| **Style** | Dense reference. No tutorials, no "let me explain..." |
| **Code** | Copy-paste ready, language-tagged code blocks |
| **Gotchas** | Required section, at least 2 real-world pitfalls |
| **Length** | 50-500 lines per article |
| **Names** | No course names, instructor names, book titles |
| **Versions** | Include version context where relevant |
| **Links** | Use `[[wiki-links]]` for cross-domain references |
| **File name** | `kebab-case.md` in the correct domain folder |

---

## Domains

| Folder | Topics |
|--------|--------|
| `algorithms/` | Sorting, graphs, DP, data structures, complexity |
| `architecture/` | Microservices, DDD, system design, API patterns |
| `bi-analytics/` | Tableau, Power BI, SQL analytics, dashboards |
| `data-engineering/` | ETL, Spark, Airflow, warehouses, streaming, CDC |
| `data-science/` | ML, statistics, neural nets, CV, NLP |
| `devops/` | Docker, Kubernetes, Terraform, CI/CD, SRE |
| `image-generation/` | Diffusion models, flow matching, LoRA, inpainting |
| `ios-mobile/` | SwiftUI, Swift, Android/Kotlin |
| `java-spring/` | Spring Boot, JPA, microservices, Kotlin |
| `kafka/` | Broker internals, Streams, KSQL, Connect |
| `linux-cli/` | Shell, filesystem, systemd, networking |
| `llm-agents/` | RAG, fine-tuning, agents, prompt engineering |
| `nodejs/` | Event loop, streams, performance, patterns |
| `php/` | Laravel, MVC, ORM, PHP 8 |
| `python/` | Core, FastAPI, Django, async, testing |
| `rust/` | Ownership, async, error handling, unsafe |
| `security/` | Web security, pentesting, AD, anti-fraud |
| `seo-marketing/` | Technical SEO, keywords, link building |
| `sql-databases/` | PostgreSQL, MySQL, optimization, indexing |
| `testing-qa/` | Selenium, Playwright, API testing |
| `web-frontend/` | React, TypeScript, CSS, bundlers |

New domains: submit a PR with at least 5 articles and a justification.

---

## For AI Agents

If you're an LLM agent using this knowledge base and you detect that an article is outdated:

**Preprocessing checklist:**

1. **Compress** - strip filler text, keep only actionable content
2. **Structure** - use `# > ## > ###` hierarchy consistently
3. **Code first** - lead with examples, explain after
4. **Gotchas** - include real pitfalls you've encountered
5. **Cross-reference** - add `[[wiki-links]]` to related topics
6. **Version tag** - include specific version numbers

**Example contribution:**

> Found: `docs/devops/docker-fundamentals.md` uses `docker-compose` (v1 CLI)
>
> Current: Docker Compose v2 uses `docker compose` (no hyphen)
>
> Action: Update CLI examples, add v1->v2 migration gotcha, cite docs.docker.com/compose/migrate/

---

## Review Process

1. **Automated checks** run on every PR (format, forbidden words, domain validation)
2. **Maintainer review** - we check content accuracy and style periodically
3. **Merge** - approved PRs are merged and the knowledge graph is rebuilt

We review PRs in batches. Patience appreciated - quality over speed.
