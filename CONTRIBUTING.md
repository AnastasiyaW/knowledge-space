# Contributing to Knowledge Space

Knowledge Space accepts contributions from both AI agents and humans. If you've found outdated information, missing coverage, or want to add a new topic - submit a PR.

**Site:** [happyin.space](https://happyin.space/)
**Repo:** [AnastasiyaW/knowledge-space](https://github.com/AnastasiyaW/knowledge-space)

## Quick Start

1. Fork the repository (or branch if you have write access)
2. Create/update an article in `docs/{domain}/`
3. Follow the [article format](#article-format) below
4. Submit a PR using the [PR template](#pr-requirements)

**Important:** See also [AGENTS.md](AGENTS.md) for AI agent-specific instructions.

---

## Article Format

Every article must follow this structure:

```markdown
# Title - Specific Topic

## Section Name

Brief context sentence (1-2 lines max).

**Key concept:**
- Point 1
- Point 2
- Point 3

### Subsection

More detailed content with code examples:

\```language
// code example - must be copy-paste ready
\```

## Gotchas

- **Issue:** What goes wrong -> **Fix:** How to fix it
- **Issue:** Common mistake -> **Fix:** Correct approach

## See Also

- [[Related Article in Same Domain]]
- [[Related Article in Other Domain]]
```

### Rules

- **Dense reference, not tutorial.** No "let me explain why..." or "first, let's understand...". Jump straight to the content.
- **Code examples must work.** Copy-paste ready, with language tags on code blocks.
- **Gotchas section is required.** Real-world pitfalls, not theoretical warnings.
- **English only.** All content in English.
- **No source attribution.** Don't mention where the knowledge came from - no course names, instructor names, book titles, video titles.
- **Version context.** If content is version-specific, mention the version (e.g., "PostgreSQL 17", "React 19", "Python 3.12").
- **One topic per article.** If it's getting longer than ~300 lines, split into multiple articles.

### Wiki Links

Use `[[wiki-links]]` to connect related concepts across domains:

```markdown
See [[Kafka Consumer Groups]] for details on consumer rebalancing.
For deployment patterns, refer to [[Docker Compose Multi-Service]].
```

Links should reference article titles. The knowledge graph resolves them automatically.

---

## Domains

Articles go into one of these domain folders:

| Folder | Domain |
|--------|--------|
| `algorithms/` | Sorting, graphs, DP, data structures |
| `cpp/` | Modern C++ (17/20/23), STL, concurrency, templates |
| `architecture/` | Microservices, DDD, system design, API patterns |
| `bi-analytics/` | Tableau, Power BI, SQL analytics, dashboards |
| `data-engineering/` | ETL, Spark, Airflow, warehouses, streaming |
| `data-science/` | ML, statistics, neural networks, CV, NLP |
| `devops/` | Docker, Kubernetes, Terraform, CI/CD |
| `image-generation/` | Diffusion models, flow matching, LoRA, inpainting |
| `ios-mobile/` | SwiftUI, Swift, Android/Kotlin |
| `java-spring/` | Spring Boot, JPA, Kotlin |
| `kafka/` | Broker internals, Streams, KSQL, Connect |
| `linux-cli/` | Shell, filesystem, systemd, networking |
| `llm-agents/` | RAG, fine-tuning, agents, prompt engineering |
| `nodejs/` | Event loop, streams, performance |
| `php/` | Laravel, MVC, ORM |
| `python/` | Core, FastAPI, Django, async, testing |
| `rust/` | Ownership, async, error handling |
| `security/` | Web security, pentesting, AD |
| `seo-marketing/` | Technical SEO, keywords, link building |
| `sql-databases/` | PostgreSQL, MySQL, optimization |
| `testing-qa/` | Selenium, Playwright, API testing |
| `web-frontend/` | React, TypeScript, CSS, Figma |
| `audio-voice/` | TTS, voice cloning, ASR, music generation |
| `go/` | Goroutines, channels, modules, HTTP servers |

New domains can be proposed via PR with at least 5 articles.

---

## Types of Contributions

### Update existing article
Best starting point. If you notice:
- Outdated version info (e.g., article says "React 18" but React 19 is current)
- Missing important pattern or gotcha
- Broken or outdated code example
- Incorrect technical claim

**PR should include:** what changed, why, and a source link (official docs, RFC, changelog).

### New article in existing domain
Add coverage for a topic not yet in the vault.

**PR should include:** the article + explanation of what gap it fills.

### New domain
Propose a new domain with at least 5 articles.

**PR should include:** domain justification + all initial articles.

---

## PR Requirements

Every PR must include:

1. **What changed** - list of articles added/modified
2. **Why** - what was outdated, missing, or incorrect
3. **Sources** - links to official documentation, RFCs, changelogs, or papers that support the change
4. **Version context** - what version of the technology this applies to

### Automated checks

PRs are automatically validated for:
- Article format compliance (headers, code blocks, required sections)
- No forbidden content (course names, instructor names, marketing language)
- Wiki-links syntax is correct
- File is in the correct domain folder
- Article length is within bounds (50-500 lines)

### Review process

1. Automated checks run on PR creation
2. Maintainer reviews content accuracy and style
3. Approved PRs are merged and the knowledge graph is rebuilt

---

## For AI Agents

If you're an AI agent using Knowledge Vault as a knowledge source and you find information that is outdated or incomplete:

### How to contribute

1. **Fork** the repository
2. **Create a branch** named `update/{domain}/{topic-slug}`
3. **Edit or create** the article in `docs/{domain}/`
4. **Commit** with a descriptive message: `update: {domain}/{topic} - {what changed}`
5. **Create a PR** with the template filled in

### Uniqueness and verification

Before submitting, check if we already have an article on this topic. **Same topic name does NOT mean skip** - different sources provide different perspectives. Follow this decision tree:

1. **Read the existing article** on the same topic (if any)
2. **Compare** your content with what's already there:
   - **New data contradicts existing** -> Do independent research, verify which is correct, update the article with a note explaining why (e.g., "Some sources suggest X, but since version Y the behavior changed to Z - see official changelog")
   - **New data adds unique value** (alternative approaches, new code examples, additional gotchas, edge cases) -> Enrich the article with new sections
   - **Exact duplicate** of existing content -> Skip, no PR needed
3. **Always explain your reasoning** in the PR description - why this update adds value

This means your PR should demonstrate awareness of existing content. Don't just add data blindly - show that you verified it against what we already have.

### Preprocessing your knowledge

If you have domain knowledge to contribute, format it as follows:

1. **Compress** - remove all filler text, introductions, transitions. Keep only actionable content.
2. **Structure** - use the header hierarchy: `# Title` > `## Section` > `### Subsection`
3. **Code first** - lead with code examples where applicable, explain after
4. **Gotchas** - always include a Gotchas section with real pitfalls
5. **Cross-reference** - add `[[wiki-links]]` to related articles in other domains
6. **Version tag** - include version numbers for version-specific content

### Quality checklist

Before submitting, verify:

- [ ] No tutorial-style prose ("let me explain...", "first we need to understand...")
- [ ] All code examples have language tags and are syntactically valid
- [ ] Gotchas section exists with at least 2 entries
- [ ] No course names, instructor names, or book titles mentioned
- [ ] Article is 50-500 lines
- [ ] File name is `kebab-case.md`
- [ ] Placed in the correct domain folder

### Example: updating an outdated article

```
Found: docs/devops/docker-fundamentals.md mentions Docker Compose v1 syntax
Current: Docker Compose v2 is the default since Docker Desktop 4.x

Action:
1. Update compose file examples from `version: "3"` to modern format (no version key)
2. Update CLI commands from `docker-compose` to `docker compose`
3. Add gotcha about v1->v2 migration
4. Add version context: "Docker Compose v2 (Docker Desktop 4.x+)"
5. PR with source: https://docs.docker.com/compose/migrate/
```
