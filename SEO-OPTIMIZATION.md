# Knowledge Vault - SEO & LLM Discoverability Optimization Plan

Date: 2026-04-03
Status: PLAN (not implemented yet)

Based on deep research across 3 areas: technical SEO for MkDocs Material, LLM discoverability (AI search engines), and content strategy (semantic core).

---

## Executive Summary

The site has 558+ articles across 22 domains. Current state: 10 sample articles deployed, MkDocs Material configured with basic features. To maximize discoverability by both traditional search engines and AI systems (Google AI Overviews, ChatGPT Search, Perplexity), we need optimizations at 4 levels:

1. **Technical SEO** - sitemap, robots.txt, schema markup, OG cards, page speed
2. **LLM Discoverability** - llms.txt, AI crawler policy, definition-first content, RAG-friendly structure
3. **Content Architecture** - hub-and-spoke model, internal linking, semantic core
4. **Content Quality** - E-E-A-T signals, freshness, titles/descriptions

---

## Phase 1: Technical Foundation (Week 1) - LOW EFFORT

### 1.1 mkdocs.yml Upgrade

Current config is minimal. Full SEO-optimized config:

```yaml
site_name: Knowledge Vault
site_url: https://happyin.space/
site_description: >-
  Comprehensive technical knowledge base with 558+ curated articles
  covering Kafka, Python, SQL, DevOps, Security, and 17 more domains.
  Built for LLM agents and engineers.
site_author: AnastasiyaW

theme:
  name: material
  custom_dir: overrides
  palette:
    - scheme: slate
      primary: deep purple
      accent: amber
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
    - scheme: default
      primary: deep purple
      accent: amber
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
  font:
    text: Inter
    code: JetBrains Mono
  features:
    - navigation.instant
    - navigation.instant.prefetch
    - navigation.tracking
    - navigation.path          # Breadcrumbs + auto BreadcrumbList JSON-LD
    - navigation.indexes       # Section index pages (pillar/hub pages)
    - navigation.sections
    - navigation.expand
    - navigation.top
    - search.suggest
    - search.highlight
    - content.code.copy
    - content.code.annotate
    - toc.follow
  icon:
    repo: fontawesome/brands/github

repo_url: https://github.com/AnastasiyaW/knowledge-vault
repo_name: knowledge-vault

plugins:
  - search
  - social:                    # Auto-generate OG card images per page
      cards: true
  - privacy:                   # Self-host Google Fonts, external assets
      assets: true
  - meta                       # Bulk frontmatter via .meta.yml per directory
  - minify:                    # HTML/CSS/JS minification
      minify_html: true
  - llmstxt:                   # Generate llms.txt + llms-full.txt for AI agents
      full_output: llms-full.txt
  - redirects:                 # 301 redirects for restructured URLs
      redirect_maps: {}

markdown_extensions:
  - pymdownx.highlight:
      anchor_linenums: true
      line_spans: __span
      pygments_lang_class: true
  - pymdownx.inlinehilite
  - pymdownx.snippets
  - pymdownx.superfences
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.details
  - admonition
  - tables
  - toc:
      permalink: true
      toc_depth: 3
  - attr_list
  - md_in_html
  - pymdownx.emoji:
      emoji_index: !!python/name:material.extensions.emoji.twemoji
      emoji_generator: !!python/name:material.extensions.emoji.to_svg

extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/AnastasiyaW/knowledge-vault
    - icon: fontawesome/brands/linkedin
      link: https://www.linkedin.com/in/happyinhappy/

extra_css:
  - stylesheets/graph.css

extra_javascript:
  - javascripts/graph.js
```

**New plugins to install:**
```bash
pip install mkdocs-minify-plugin mkdocs-llmstxt mkdocs-redirects
```

Social plugin and privacy plugin are built into Material for MkDocs (may need Insiders for social cards).

### 1.2 robots.txt

Create `docs/robots.txt`:

```
# Traditional search engines
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

# AI search crawlers - ALLOW
User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-User
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: Applebot
Allow: /

User-agent: Applebot-Extended
Allow: /

# AI training crawlers - BLOCK
User-agent: GPTBot
Disallow: /

User-agent: Google-Extended
Disallow: /

User-agent: CCBot
Disallow: /

User-agent: Bytespider
Disallow: /

User-agent: Meta-ExternalAgent
Disallow: /

User-agent: Diffbot
Disallow: /

User-agent: cohere-ai
Disallow: /

User-agent: ImagesiftBot
Disallow: /

User-agent: Timpibot
Disallow: /

User-agent: omgili
Disallow: /

# Default - allow all others
User-agent: *
Allow: /

Sitemap: https://happyin.space/sitemap.xml
```

**Rationale:** Allow AI search (for citations/visibility), block AI training (content protection). Review quarterly as new crawlers appear.

### 1.3 Google Search Console + Bing

1. Add property: `https://happyin.space/`
2. Verify via HTML file in `docs/`
3. Submit sitemap
4. Set up Bing Webmaster Tools (can import from GSC)

### 1.4 IndexNow via GitHub Actions

Create `.github/workflows/indexnow.yml` for automatic Bing/Yandex notification on deploy.

---

## Phase 2: LLM Discoverability (Weeks 1-2) - HIGHEST IMPACT

### 2.1 Article Opening Restructure

**THE single highest-impact optimization.** 44% of AI citations come from first 30% of article. First 200 words must work as standalone citation.

**Before (current pattern):**
```markdown
# FastAPI - Introduction & Core Concepts

## What is FastAPI

A modern, high-performance Python web framework for building APIs, built on:
```

**After (definition-first):**
```markdown
# FastAPI - Introduction & Core Concepts

FastAPI is a modern, high-performance Python web framework for building APIs. Built on Starlette (ASGI) and Pydantic (validation), it delivers auto-generated OpenAPI documentation, type-safe request handling, and async-first performance comparable to Go and Node.js. FastAPI is the fastest-growing Python web framework as of 2026, used in production by Microsoft, Netflix, and Uber.

## Key Advantages
```

**Rules for every article:**
- First 1-2 sentences: clean factual definition (what it IS, not what it does for you)
- Next 2-3 sentences: key differentiators, version context, who uses it
- NO "In this article...", "Let's explore...", "Welcome to..."
- First 200 words = complete mini-answer an AI can cite verbatim

### 2.2 Question-Based Headings

99.2% of question-based queries trigger AI Overviews. Structure articles as implicit FAQs:

```markdown
## What is Kafka Consumer Group?
## How Does Partition Assignment Work?
## How to Configure Consumer Group Settings
## What Happens During Rebalancing?
## Common Consumer Group Issues and Solutions
```

Mix question headings with action headings for variety. Not EVERY heading needs to be a question.

### 2.3 Self-Contained Sections (RAG Alignment)

AI search chunks content at 256-512 tokens (~200-400 words). Each H2/H3 section should:
- Start with a definition sentence ("X is Y that does Z")
- Be readable without context from previous sections
- NOT use "as mentioned above", "the example from section 2"
- Include relevant keywords naturally

### 2.4 Statistics and Specifics

AI systems prefer concrete, verifiable claims over vague statements.

**Before:** "Kafka supports many partitions per cluster"
**After:** "Kafka supports up to 200,000 partitions per cluster as of version 3.x (KIP-500)"

Add version numbers, performance benchmarks, concrete configuration values, RFC/KIP references.

### 2.5 llms.txt Configuration

The mkdocs-llmstxt plugin generates both files automatically. Configure sections for all 22 domains. Even though no AI company has confirmed using it, it's zero-cost and growing adoption (844K+ sites).

---

## Phase 3: Structured Data (Weeks 2-4) - HIGH IMPACT

### 3.1 Template Override for TechArticle JSON-LD

Create `overrides/main.html`:

```jinja2
{% extends "base.html" %}

{% block extrahead %}
  {{ super() }}

  {# Open Graph #}
  <meta property="og:type" content="article" />
  <meta property="og:title" content="{{ page.title }} - {{ config.site_name }}" />
  <meta property="og:description" content="{{ page.meta.description | default(config.site_description) }}" />
  <meta property="og:url" content="{{ page.canonical_url }}" />
  <meta property="og:site_name" content="{{ config.site_name }}" />

  {# Twitter Card #}
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{{ page.title }} - {{ config.site_name }}" />
  <meta name="twitter:description" content="{{ page.meta.description | default(config.site_description) }}" />

  {# TechArticle JSON-LD #}
  {% if page and page.meta and page.meta.description %}
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "TechArticle",
    "headline": "{{ page.title }}",
    "description": "{{ page.meta.description }}",
    "url": "{{ page.canonical_url }}",
    {% if page.meta.date %}"datePublished": "{{ page.meta.date }}",{% endif %}
    {% if page.meta.updated %}"dateModified": "{{ page.meta.updated }}",{% endif %}
    "author": {
      "@type": "Person",
      "name": "{{ config.site_author | default('AnastasiyaW') }}",
      "url": "https://github.com/AnastasiyaW"
    },
    "publisher": {
      "@type": "Organization",
      "name": "{{ config.site_name }}",
      "url": "{{ config.site_url }}"
    },
    "mainEntityOfPage": {
      "@type": "WebPage",
      "@id": "{{ page.canonical_url }}"
    },
    "proficiencyLevel": "{{ page.meta.level | default('Intermediate') }}"
  }
  </script>
  {% endif %}
{% endblock %}
```

**CRITICAL:** Only emit schema when `description` is present. Partially-filled schema causes 18% citation PENALTY (empirical finding from 2026 study of 730 AI citations).

### 3.2 Article Frontmatter Template

Every article should have:

```yaml
---
description: "Concise 140-160 char description with primary keyword."
date: 2026-04-03
updated: 2026-04-03
tags:
  - primary-domain
  - secondary-topic
level: Intermediate
---
```

For bulk defaults, create `.meta.yml` per domain directory:
```yaml
# docs/kafka/.meta.yml
tags:
  - kafka
  - messaging
level: Intermediate
```

### 3.3 Breadcrumbs

`navigation.path` feature auto-generates visual breadcrumbs AND BreadcrumbList JSON-LD. Already in our config.

---

## Phase 4: Content Architecture (Weeks 3-6) - MEDIUM EFFORT, HIGH IMPACT

### 4.1 Hub-and-Spoke Structure

Each of 22 domains gets an index page (hub/pillar) via `navigation.indexes`:

```
docs/
  kafka/
    index.md          # Hub page (3000-5000 words overview)
    event-sourcing-and-cqrs.md
    consumer-groups.md
    ...
```

**Hub page template:**
1. H1: Domain name + comprehensive overview (300-500 words)
2. Topic map / learning path
3. Links to ALL articles in domain
4. Cross-domain connections
5. FAQ section (People Also Ask sourced)

### 4.2 Internal Linking Strategy

Target: 5-10 internal links per 2,000 words.

Every article MUST have:
- Link back to domain hub page
- "Related Articles" section at bottom (3-5 links)
- "Prerequisites" links at top (if applicable)
- Contextual body links to related concepts

Anchor text: descriptive, keyword-rich, varied. Never "click here".

### 4.3 Title and Meta Description Templates

**Titles** (50-60 chars):
| Type | Template |
|------|----------|
| Concept | `[Concept] in [Tech]: [Clarifier]` |
| Tutorial | `How to [Action] in [Tech]` |
| Reference | `[Tech] [Resource]: [Scope]` |
| Troubleshooting | `Fix [Problem] in [Tech]` |
| Comparison | `[A] vs [B]: [Differentiator]` |

**Meta descriptions** (140-160 chars):
Formula: [Context/Problem] + [What covered] + [Value/CTA]

Each of 558 articles needs UNIQUE title and description. Prevent cannibalization via keyword-to-URL map.

---

## Phase 5: E-E-A-T & Authority (Ongoing) - HIGH IMPACT

### 5.1 Author/About Pages

Create `docs/about/index.md` and `docs/about/author.md`:
- Professional profile, expertise areas, GitHub link
- Person schema (JSON-LD) with knowsAbout, sameAs
- Linked from every article via template

### 5.2 Content Freshness

- Display "Last updated" on every article
- Use `git-revision-date-localized` plugin for auto dates
- Quarterly review cycle: ~140 articles/quarter
- Content < 3 months old = 3x more likely cited by AI
- Content > 3 months without update = 3x more likely to LOSE visibility

### 5.3 Backlink Strategy

- Submit to tech newsletters (Python Weekly, DevOps Weekly, etc.)
- Cross-post summaries on DEV.to, Hashnode (canonical to our site)
- Answer StackOverflow questions with links
- Community engagement on Reddit (Perplexity heavily uses Reddit - 24% of citations)

---

## Phase 6: Custom Domain (Optional but Recommended)

**Problem:** `*.github.io` shares domain with millions of sites. Google allocates crawl budget per domain. "Discovered - currently not indexed" can persist for months.

**Solution:** Custom domain (~$10-20/year) gives:
- Dedicated crawl budget
- Independent domain authority
- Professional perception
- Better indexing speed for 558 pages

Options: `knowledge-vault.dev`, `knowledge-vault.tech`, subdomain of existing domain.

---

## Phase 7: Bot-Only Multilingual Layer - IMPLEMENTED

**Concept:** Make the site discoverable in 5 non-English languages WITHOUT translating any content. Only search engine bots and AI agents see the multilingual layer - zero visual changes for human visitors.

### What was implemented:

**7.1 Multilingual llms.txt files** (5 languages):
- `docs/llms.txt` - English (primary)
- `docs/llms-zh.txt` - Chinese
- `docs/llms-ko.txt` - Korean
- `docs/llms-es.txt` - Spanish
- `docs/llms-de.txt` - German
- `docs/llms-fr.txt` - French

Each file contains the same article URLs but with translated domain names, article descriptions, and site summary. AI agents (ChatGPT, Claude, Perplexity) discovering these files can serve the content to users searching in their native language.

**7.2 Schema.org `availableLanguage`** on homepage:
WebSite JSON-LD in `overrides/main.html` declares:
```json
"availableLanguage": ["en", "zh", "ko", "es", "de", "fr"]
```
This tells Google/Bing: "this site has descriptions relevant for speakers of these languages." Used by AI Overviews when generating cross-language responses.

**7.3 robots.txt references** to all llms-*.txt files (as comments, for discoverability).

### Why NOT Russian:
Russian speakers find content through Russian-language sources. The target audience for multilingual discovery = developers who search in their language for English technical content.

### Maintenance:
When new articles are added (Stage 3 pipeline), update ALL 6 llms-*.txt files with translated descriptions. Can be automated via Stage 3 generation pipeline.

---

## Implementation Priority Summary

| # | Action | Impact | Effort | Phase |
|---|--------|--------|--------|-------|
| 1 | Update mkdocs.yml (plugins, features) | HIGH | Low | 1 |
| 2 | Create robots.txt | Medium | Low | 1 |
| 3 | Set up GSC + Bing | HIGH | Low | 1 |
| 4 | **Restructure article openings (definition-first)** | **VERY HIGH** | Medium | 2 |
| 5 | Question-based headings | HIGH | Medium | 2 |
| 6 | Self-contained sections | HIGH | Medium | 2 |
| 7 | Add statistics/specifics to content | HIGH | Medium | 2 |
| 8 | Template override for JSON-LD schema | HIGH | Medium | 3 |
| 9 | Add frontmatter to all articles | HIGH | Medium | 3 |
| 10 | Create 22 domain hub pages | HIGH | High | 4 |
| 11 | Internal linking (5-10 per article) | HIGH | High | 4 |
| 12 | Titles + meta descriptions for 558 articles | HIGH | High | 4 |
| 13 | Author/About pages | Medium | Low | 5 |
| 14 | Content freshness system | HIGH | Ongoing | 5 |
| 15 | Custom domain | HIGH | Low | 6 |
| 16 | Multilingual llms-*.txt (5 languages) | Medium | Low | 7 - DONE |
| 17 | Schema.org availableLanguage | Medium | Low | 7 - DONE |

---

## Key Research Sources

### Research Papers
- GEO: Generative Engine Optimization (Princeton, KDD 2024) - foundational paper on AI search optimization
- GEO-SFE (arXiv:2603.29979, March 2026) - structural features for AI citation

### Industry Reports
- Previsible 2025 State of AI Discovery (1.96M sessions)
- Kevin Indig - State of AI Search Optimization 2026
- Cloudflare - Who's Crawling Your Site 2025
- Tinuiti Q1 2026 AI Citation Trends

### Key Stats
- 44% of AI citations from first 30% of article (first-content bias)
- 8.5/10 semantic completeness -> 340% higher AI citation rate
- Partial schema -> 18% citation PENALTY (worse than no schema)
- Content < 3 months old -> 3x more likely cited
- Citation in AI Overview -> 80%+ CTR increase
- Question-based queries -> 99.2% trigger AI Overviews

### Raw Research Files
- `skill-generator/state/incoming-research/seo--mkdocs-material-technical-seo-raw.md`
- `skill-generator/state/incoming-research/seo--llm-discoverability-ai-search-raw.md`
- `skill-generator/state/incoming-research/seo--content-strategy-semantic-core-raw.md`
