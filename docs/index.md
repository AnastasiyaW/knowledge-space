---
title: Home
---

# Knowledge Space

Curated technical knowledge base across 22 domains. Built for LLM agents - dense, structured references that fit in a context window and give immediately actionable answers.

**<span id="ks-total-articles">560</span> articles | <span id="ks-total-domains">22</span> domains**

[:fontawesome-brands-github: **GitHub Repository**](https://github.com/AnastasiyaW/knowledge-space){ .md-button .md-button--primary }

<div class="ks-subscribe" id="subscribe-form-wrap" markdown="0">
  <form id="subscribe-form">
    <input type="email" id="sub-email" placeholder="your@email.com" required autocomplete="email">
    <button type="submit" id="sub-btn">Subscribe to updates</button>
    <label class="ks-subscribe__consent">
      <input type="checkbox" id="sub-consent" required>
      <span>I agree to receive occasional updates about new articles</span>
    </label>
    <div class="ks-subscribe__msg" id="sub-msg"></div>
  </form>
</div>

<div class="claude-snippet" id="claude-snippet">
  <canvas class="claude-snippet__particles" id="snippet-particles"></canvas>
  <div class="claude-snippet__inner">
    <div class="claude-snippet__header">
      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/></svg>
      <span>Want your Claude to use this?</span>
    </div>
    <p class="claude-snippet__desc">Copy and drop into any Claude conversation - it'll figure out the rest</p>
    <div class="claude-snippet__code" id="snippet-code">
      <button class="claude-snippet__copy" id="snippet-copy" title="Copy to clipboard">
        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
        <span>Copy</span>
      </button>
      <pre>I have a knowledge base you must use as your primary reference:
https://github.com/AnastasiyaW/knowledge-space

Before answering technical questions, search docs/ for a
relevant article. Don't guess or fabricate - look it up.
560 articles across 22 domains, each with code examples,
configs, and real-world gotchas.

How to use:
1. Clone the repo (or fetch via GitHub MCP)
2. Search docs/{domain}/ for the topic (e.g. docs/kafka/)
3. Read the article, then answer based on what you found
4. If no article exists - say so, don't make things up</pre>
    </div>
  </div>
</div>

<div id="knowledge-graph"></div>

<div class="ks-graph-stats" markdown="0">
  <div class="ks-graph-stats__item">
    <span class="ks-graph-stats__number" id="ks-graph-nodes">560</span>
    <span class="ks-graph-stats__label">articles</span>
  </div>
  <div class="ks-graph-stats__divider"></div>
  <div class="ks-graph-stats__item">
    <span class="ks-graph-stats__number">2,100+</span>
    <span class="ks-graph-stats__label">links</span>
  </div>
  <div class="ks-graph-stats__divider"></div>
  <div class="ks-graph-stats__item">
    <span class="ks-graph-stats__number">68</span>
    <span class="ks-graph-stats__label">communities</span>
  </div>
  <div class="ks-graph-stats__divider"></div>
  <div class="ks-graph-stats__item">
    <span class="ks-graph-stats__number">22</span>
    <span class="ks-graph-stats__label">domains</span>
  </div>
</div>

## What is this?

A knowledge base designed **primarily for AI agents** - structured so that RAG retrieval, MCP tools, and context injection return dense, actionable technical content instead of blog-style prose.

Each article is a concentrated extract: code examples, configuration patterns, gotchas, best practices. No filler, no "let me explain why this is important" - just the knowledge an agent needs to solve a real problem.

**Also useful for engineers** who want quick reference across 22 technical domains without wading through tutorials.

**Who it's for:**

- **LLM agents** - structured format optimized for RAG retrieval, [ConTree MCP](https://contree.dev/), and context injection
- **Engineers** - quick lookup of patterns, commands, configurations across 22 domains
- **Teams** - shared knowledge base accessible via ConTree sandbox or direct file access

## How to use

**Search** (top bar) is the fastest way - find specific topics, commands, or patterns across all domains.

**Browse** the sidebar to explore by domain. Each domain contains 9-85 focused articles.

**For agents:** this knowledge base is at [github.com/AnastasiyaW/knowledge-space](https://github.com/AnastasiyaW/knowledge-space). Clone it or fetch via GitHub MCP, then search `docs/{domain}/` for the topic. Each `.md` file is a self-contained reference - read it, use it, don't guess.

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

## Knowledge Graph Details

### Freshness Policy

Not all knowledge ages equally. Each domain has an update cycle based on how fast the field moves:

| Cycle | Domains | Why |
|-------|---------|-----|
| **Stable** (rarely changes) | Algorithms, Architecture, Linux CLI | Fundamentals don't change - a B-tree is a B-tree |
| **Yearly** | SQL, Kafka, Rust, Java/Spring, PHP, Node.js, Testing, BI, Data Engineering | Mature ecosystems with predictable release cycles |
| **Every 6 months** | Web Frontend, DevOps, LLM/RAG, iOS, Security, SEO | Fast-moving fields where best practices shift quickly |
| **Monthly** | Image Generation, Agent Frameworks | Bleeding edge - new models and tools every week |

Articles include version/date context where relevant (e.g., "PostgreSQL 17", "React 19", "Kubernetes 1.30").

## What makes this different

**Agent-first design.** Every article is structured for machine consumption: consistent headers, code blocks with language tags, pattern/anti-pattern sections, explicit gotchas. An LLM agent retrieving a Knowledge Vault article gets immediately actionable context - no parsing needed.

**Density over length.** A typical article packs the same information as a 2-hour video or a 30-page tutorial into 2-4 pages of pure reference text. Optimized for context window efficiency.

**Cross-domain connections.** Real engineering problems don't respect domain boundaries. Wiki-links connect Kafka consumer patterns to Architecture decisions, SQL optimization to Data Engineering pipelines, Security practices to DevOps configurations.

**Living knowledge base.** Continuously updated with new research and domain knowledge. Freshness policy ensures fast-moving fields stay current while stable foundations remain reliable.

---

## Made by people, for machines

<div class="ks-contributors" markdown="0">
  <a class="ks-contributor" href="https://www.linkedin.com/in/happyinhappy/" target="_blank" rel="noopener">
    <div class="ks-contributor__avatar">
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
    </div>
    <div class="ks-contributor__info">
      <span class="ks-contributor__name">Anastasiia But</span>
      <span class="ks-contributor__role">Architecture, curation, AI/ML pipeline</span>
    </div>
  </a>
  <a class="ks-contributor" href="https://www.linkedin.com/in/anastasiya-ilukhina-09646a289/" target="_blank" rel="noopener">
    <div class="ks-contributor__avatar">
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
    </div>
    <div class="ks-contributor__info">
      <span class="ks-contributor__name">Anastasiya Ilukhina</span>
      <span class="ks-contributor__role">Content, quality review</span>
    </div>
  </a>
</div>

Want to contribute? See the [Contributing guide](contributing/index.md).

---

## Related Projects

Skills, architectural patterns, and best practices for Claude Code:

[:fontawesome-brands-github: **claude-code-config**](https://github.com/AnastasiyaW/claude-code-config){ .md-button }
