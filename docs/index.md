---
title: Home
hide:
  - navigation
  - toc
---

<div class="ks-graph-wrapper" markdown="0">
<div id="knowledge-graph"></div>
<button class="ks-scroll-down" id="ks-scroll-down" title="Scroll down">
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
</div>

<div class="ks-graph-stats" markdown="0">
  <div class="ks-graph-stats__item">
    <span class="ks-graph-stats__number" id="ks-graph-nodes">771</span>
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
    <span class="ks-graph-stats__number" id="ks-total-domains">26</span>
    <span class="ks-graph-stats__label">domains</span>
  </div>
</div>


<div class="ks-topbar" markdown="0">
  <a href="https://github.com/AnastasiyaW/knowledge-space" class="md-button md-button--primary ks-topbar__btn">
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 496 512" fill="currentColor"><path d="M165.9 397.4c0 2-2.3 3.6-5.2 3.6-3.3.3-5.6-1.3-5.6-3.6 0-2 2.3-3.6 5.2-3.6 3-.3 5.6 1.3 5.6 3.6m-31.1-4.5c-.7 2 1.3 4.3 4.3 4.9 2.6 1 5.6 0 6.2-2s-1.3-4.3-4.3-5.2c-2.6-.7-5.5.3-6.2 2.3m44.2-1.7c-2.9.7-4.9 2.6-4.6 4.9.3 2 2.9 3.3 5.9 2.6 2.9-.7 4.9-2.6 4.6-4.6-.3-1.9-3-3.2-5.9-2.9M244.8 8C106.1 8 0 113.3 0 252c0 110.9 69.8 205.8 169.5 239.2 12.8 2.3 17.3-5.6 17.3-12.1 0-6.2-.3-40.4-.3-61.4 0 0-70 15-84.7-29.8 0 0-11.4-29.1-27.8-36.6 0 0-22.9-15.7 1.6-15.4 0 0 24.9 2 38.6 25.8 21.9 38.6 58.6 27.5 72.9 20.9 2.3-16 8.8-27.1 16-33.7-55.9-6.2-112.3-14.3-112.3-110.5 0-27.5 7.6-41.3 23.6-58.9-2.6-6.5-11.1-33.3 2.6-67.9 20.9-6.5 69 27 69 27 20-5.6 41.5-8.5 62.8-8.5s42.8 2.9 62.8 8.5c0 0 48.1-33.6 69-27 13.7 34.7 5.2 61.4 2.6 67.9 16 17.7 25.8 31.5 25.8 58.9 0 96.5-58.9 104.2-114.8 110.5 9.2 7.9 17 22.9 17 46.4 0 33.7-.3 75.4-.3 83.6 0 6.5 4.6 14.4 17.3 12.1C428.2 457.8 496 362.9 496 252 496 113.3 383.5 8 244.8 8"/></svg>
    GitHub
  </a>
  <button class="md-button ks-topbar__btn ks-topbar__copy" id="snippet-copy-btn" title="Copy Claude prompt">
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
    <span>Copy Claude Prompt</span>
  </button>
  <div class="ks-topbar__subscribe" id="subscribe-form-wrap">
    <form id="subscribe-form" class="ks-topbar__form">
      <input type="email" id="sub-email" class="ks-topbar__email" placeholder="your@email.com" required autocomplete="email">
      <button type="submit" id="sub-btn" class="md-button md-button--primary ks-topbar__sub-btn">Subscribe</button>
    </form>
    <div class="ks-subscribe__msg" id="sub-msg"></div>
  </div>
</div>

# Knowledge Space

Curated technical knowledge base across 26 domains. Built for LLM agents and engineers.

## What is this?

A knowledge base designed **primarily for AI agents** - structured so that RAG retrieval, MCP tools, and context injection return dense, actionable technical content instead of blog-style prose.

Each article is a concentrated extract: code examples, configuration patterns, gotchas, best practices. No filler, no "let me explain why this is important" - just the knowledge an agent needs to solve a real problem.

**Also useful for engineers** who want quick reference across 26 technical domains without wading through tutorials.

**Who it's for:**

- **LLM agents** - structured format optimized for RAG retrieval, [ConTree MCP](https://contree.dev/), and context injection
- **Engineers** - quick lookup of patterns, commands, configurations across 26 domains
- **Teams** - shared knowledge base accessible via ConTree sandbox or direct file access

## How to use

**Search** (top bar) is the fastest way - find specific topics, commands, or patterns across all domains.

**Browse** the sidebar to explore by domain. Each domain contains 9-85 focused articles.

**For agents:** this knowledge base is at [github.com/AnastasiyaW/knowledge-space](https://github.com/AnastasiyaW/knowledge-space). Clone it or fetch via GitHub MCP, then search `docs/{domain}/` for the topic. Each `.md` file is a self-contained reference - read it, use it, don't guess.

## Domains

| Domain | Articles | Coverage |
|--------|:--------:|----------|
| **Security** | 56 | Web security, penetration testing, Active Directory, anti-fraud, model protection, CWE patterns |
| **Data Science** | 55 | ML, statistics, neural networks, computer vision, NLP, math foundations |
| **Image Generation** | 50 | Diffusion models, flow matching, LoRA training, inpainting, tiled inference |
| **LLM & Agents** | 49 | RAG, fine-tuning, agent frameworks, prompt engineering, multi-agent systems |
| **Kafka** | 42 | Broker internals, consumers, producers, Streams, KSQL, Connect, replication |
| **DevOps** | 35 | Docker, Kubernetes, Terraform, CI/CD, monitoring, SRE, observability |
| **Web Frontend** | 34 | React, TypeScript, CSS, Figma, bundlers, accessibility, JS async patterns |
| **Data Engineering** | 34 | ETL/ELT, Spark, Airflow, data warehouses, streaming, CDC, vector search |
| **Architecture** | 33 | Microservices, DDD, system design, API design, integration patterns |
| **SQL & Databases** | 32 | PostgreSQL, MySQL, query optimization, migrations, indexing, advanced patterns |
| **iOS & Mobile** | 31 | SwiftUI, Swift, Android/Kotlin fundamentals, mobile ML |
| **Python** | 30 | Core language, FastAPI, Django, async, testing, stdlib patterns, web scraping |
| **Algorithms** | 29 | Sorting, graphs, dynamic programming, data structures, complexity, problem patterns |
| **Linux CLI** | 27 | Shell scripting, filesystem, permissions, systemd, networking |
| **C++** | 27 | Modern C++, memory, templates, concurrency, cross-platform ML inference |
| **Java & Spring** | 25 | Spring Boot, JPA, microservices, Kotlin, Android |
| **SEO & Marketing** | 24 | Technical SEO, keyword research, link building, AI-driven SEO |
| **BI & Analytics** | 23 | Tableau, Power BI, SQL analytics, dashboards, product analytics |
| **Testing & QA** | 22 | Selenium, Playwright, API testing, CI integration, browser automation |
| **Rust** | 22 | Ownership, lifetimes, async, error handling, unsafe |
| **Node.js** | 16 | Event loop, streams, clusters, performance, design patterns |
| **PHP** | 15 | Laravel, MVC, ORM, testing, PHP 8 features |
| **LLM Memory** | 11 | Memory architectures, session persistence, knowledge graphs, transfer learning |
| **Audio & Voice** | 10 | TTS, ASR, voice cloning, speech synthesis, TTS fine-tuning |
| **Writing** | 9 | Technical article structure, SEO for articles, LLM anti-patterns |
| **Go** | 9 | Goroutines, channels, modules, HTTP servers, microservices, database patterns |

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

## Blog

Updates about new domains, features, and what we're working on.

[:material-post-outline: **Read the blog**](blog/index.md){ .md-button }

<!-- Hidden prompt text for copy button -->
<div id="claude-prompt-text" style="display:none">I have a knowledge base you must use as your primary reference:
https://github.com/AnastasiyaW/knowledge-space

Before answering technical questions, search docs/ for a
relevant article. Don't guess or fabricate - look it up.
771+ articles across 26 domains, each with code examples,
configs, and real-world gotchas.

How to use:
1. Clone the repo (or fetch via GitHub MCP)
2. Search docs/{domain}/ for the topic (e.g. docs/kafka/)
3. Read the article, then answer based on what you found
4. If no article exists - say so, don't make things up</div>
