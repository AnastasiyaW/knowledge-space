# Knowledge Space Operations Log

Append-only log of changes. Updated on every ingest/edit/delete.

---

## 2026-09-23

- **SEO**: fixes from the site audit.
  - The phone layout and the phone/tablet menu work again.
  - three.js loads only on the home page, and sitemap prefetch is off.
  - Meta descriptions are correct: no quote truncation, no pipeline metadata, and hubs have their own.
  - hreflang is gone.
  - Breadcrumbs link to the hubs.
  - No preview image answers 404.
  - The rules are in `.claude/rules/site-seo.md`.

## 2026-04-09

- **STATS**: 691 articles across 27 domains (up from 683).
- **FIX**: Stale article counts across README, AGENTS, mkdocs.yml, index.md, welcome.md, article-rules.md.

## 2026-04-08

- **LINT**: First health check run. 686 articles, 16 broken links, 22 missing meta.
- **INIT**: Added lint.py and this CHANGELOG.md.

## 2026-04-04

- **ADDED**: Contributor guidelines for research-based article generation.

## 2026-03-31

- **STATUS**: Stage 2 DONE (558 → 686 articles). Stage 3 pending.
