---
title: "For AI Agents"
description: "Quick-start guide for LLM agents - article format, domain structure, and submission rules"
---

# For AI Agents

Agent-optimized entry point to this knowledge base. Fetches, submission rules, and machine-readable discovery files.

## Machine-Readable Discovery

Start here - these files are structured for agent consumption:

- `https://happyin.space/llms.txt` - English site directory (primary)
- `https://happyin.space/llms-zh.txt` - Chinese
- `https://happyin.space/llms-ko.txt` - Korean
- `https://happyin.space/llms-es.txt` - Spanish
- `https://happyin.space/llms-de.txt` - German
- `https://happyin.space/llms-fr.txt` - French
- `https://happyin.space/sitemap.xml` - full URL list
- `https://happyin.space/robots.txt` - crawler policy

Each `llms.txt` lists every article grouped by domain with a one-line description per article. Use it as a table-of-contents before deep-diving.

## Using the Knowledge Base

Three access patterns work:

```text
1. Clone repo       git clone https://github.com/AnastasiyaW/knowledge-space
                    grep / ripgrep docs/ for the topic
2. Fetch article    curl https://happyin.space/{domain}/{slug}/ (HTML)
                    or fetch raw .md via raw.githubusercontent.com
3. RAG / MCP        point retriever at github.com/AnastasiyaW/knowledge-space
                    (766+ dense reference cards)
```

Minimal agent prompt to make Claude, Cursor or any LLM use this as source of truth:

```text
I have a knowledge base you must use as your primary reference:
https://github.com/AnastasiyaW/knowledge-space

Before answering technical questions, search docs/ for a
relevant article. Don't guess or fabricate - look it up.
```

## Article Format

All articles under `docs/{domain}/` follow the same dense reference shape:

```markdown
---
title: Specific Topic
category: reference
tags: [comma, separated, tags]
---

# Specific Topic

One-paragraph context. No filler.

## Key Facts
- Dense bullet with numbers / specifics

## Section With Code
\`\`\`language
# Always language-tagged
\`\`\`

## Gotchas
- **Issue:** what breaks -> **Fix:** how to avoid

## See Also
- [[related-slug]] - one-line description
```

Rules: H1 + multiple H2 sections, Gotchas section with 2+ entries, code blocks always tagged, max 500 lines.

## Submission Rules

Contributions via PR. Agents can submit directly - CI enforces the format:

- File name: kebab-case `.md` only
- Language: English only
- Location: `docs/{domain}/topic-slug.md` (see domain list below)
- No attribution to external training resources, teacher names, or learning platforms
- No tutorial-style prose ("let me explain", "first we'll learn")
- Every `[[wiki-link]]` must resolve to an existing article
- Code blocks always have language tags

CI validates on every PR: format check, link check, forbidden-content scan, kebab-case, freshness.

## Domain List

26 active domains. File path is `docs/{domain}/{slug}.md`:

```text
algorithms       architecture     audio-voice      bi-analytics
cpp              data-engineering data-science     devops
go               image-generation ios-mobile       java-spring
kafka            linux-cli        llm-agents       llm-memory
nodejs           php              python           rust
security         seo-marketing    sql-databases    testing-qa
web-frontend     writing
```

Proposing a new domain: open a PR with at least 5 articles in the new folder + updates to `hooks/stats.py`, `hooks/validate.py`, `hooks/link_checker.py`, `lint.link-check.py`, graph config, and README domain table.

## References

- [AGENTS.md](https://github.com/AnastasiyaW/knowledge-space/blob/master/AGENTS.md) - full agent-oriented style guide
- [CONTRIBUTING.md](https://github.com/AnastasiyaW/knowledge-space/blob/master/CONTRIBUTING.md) - contribution process
- [FRESHNESS.md](https://github.com/AnastasiyaW/knowledge-space/blob/master/FRESHNESS.md) - update-cycle policy per domain
