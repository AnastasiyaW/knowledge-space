---
title: Site Structure and URL Architecture
category: concepts
tags: [seo, site-structure, url, internal-linking, breadcrumbs, crawl-depth, silo]
---

# Site Structure and URL Architecture

How pages are organized and interconnected on a website. Correct structure enables efficient crawling, distributes link equity, and maps directly to the semantic core. Two dimensions: click structure (navigation depth) and slash structure (URL hierarchy).

## Key Facts

- **Site structure** = the system of mutual page arrangement and their interconnections through internal links
- Proper structure allows search engine bots to quickly crawl and index all pages, distributes PageRank/link juice efficiently, and helps users navigate
- **Click structure** (click depth) = how many clicks from the homepage to reach any page; ideal is 3 clicks max for important pages
- **Slash structure** (URL depth) = directory depth in the URL path; `site.com/category/subcategory/product/` = 3 levels
- Click depth and slash depth should align - a page 5 URL levels deep but 2 clicks from home sends mixed signals
- Structure should mirror the semantic core: each cluster = one page, cluster hierarchy = URL hierarchy
- **Flat structure** (all pages 1-2 clicks from home) works for small sites (<100 pages); **hierarchical structure** (category/subcategory) for larger sites
- **Internal linking** distributes authority from high-authority pages (homepage, popular pages) to deeper pages
- See [[keyword-research-semantic-core]] for deriving structure from keyword clusters
- See [[technical-seo-audit]] for identifying structural issues

## Patterns

### Optimal URL structure by site type

```
E-commerce:
  site.com/                              (homepage)
  site.com/category/                     (category)
  site.com/category/subcategory/         (subcategory)
  site.com/category/subcategory/product/ (product)

Service site:
  site.com/                              (homepage)
  site.com/services/                     (services hub)
  site.com/services/service-name/        (service page)
  site.com/blog/                         (blog index)
  site.com/blog/article-slug/            (blog post)

Info site:
  site.com/                              (homepage)
  site.com/topic/                        (topic hub)
  site.com/topic/subtopic/               (article)
```

### Internal linking patterns

```
Hub-and-spoke (silo model):
  Hub page links to all spoke pages in the cluster
  Spoke pages link back to hub
  Spokes can cross-link within the same silo
  Minimal cross-silo links (preserves topical authority)

Breadcrumb navigation:
  Home > Category > Subcategory > Page
  - Implemented as structured data (Schema.org BreadcrumbList)
  - Shows in SERP as rich result
  - Critical for both UX and crawling

Contextual links:
  Links within body text to related pages
  Use descriptive anchor text (NOT "click here")
  Most powerful internal link type for SEO
```

### URL best practices

```
GOOD:  site.com/running-shoes/nike-air-max/
BAD:   site.com/catalog.php?cat=12&id=456
BAD:   site.com/running_shoes/Nike-Air-Max-2024-Black-White-Size-42/

Rules:
- Use hyphens (-) not underscores (_) as word separators
- Lowercase only
- Short and descriptive (3-5 words max per segment)
- Remove stop words (a, the, and, of)
- Include target keyword naturally
- No dynamic parameters if possible (URL rewrite)
- Trailing slash consistency (pick one, redirect the other)
```

### Screaming Frog site structure audit

```
1. Crawl site with Screaming Frog
2. Check "Crawl Depth" tab - flag pages > 3 clicks deep
3. Check "URL" tab - flag URLs > 115 characters
4. Export internal link data -> build link equity flow map
5. Identify orphan pages (no internal links pointing to them)
6. Identify pages with only 1 internal link (vulnerable)
```

## Gotchas

- **Orphan pages** (no internal links) are invisible to crawlers that follow links; they may still be indexed via sitemap but rank poorly due to zero internal link equity
- **URL changes break SEO** - changing URL structure without 301 redirects loses all accumulated authority and causes 404 errors; always implement redirect maps
- **Pagination creates crawl traps** - infinite scroll or deep pagination (page 500+) wastes crawl budget; use `rel="next/prev"` (still useful for Yandex) or load-more buttons
- **Filter pages in e-commerce** - every filter combination can create thousands of unique URLs; block non-essential filter pages via robots.txt or noindex to prevent crawl budget waste
- **Subdomain vs subfolder** - `blog.site.com` is treated as a separate site by search engines; `site.com/blog/` inherits domain authority; prefer subfolder unless there's a technical reason for subdomain

## See Also

- [[keyword-research-semantic-core]] - Deriving structure from keyword clusters
- [[technical-seo-audit]] - Finding and fixing structural issues
- [Google URL Structure Guidelines](https://developers.google.com/search/docs/crawling-indexing/url-structure)
- [Screaming Frog SEO Spider](https://www.screamingfrog.co.uk/seo-spider/)
- [Ahrefs Site Structure Guide](https://ahrefs.com/blog/website-structure/)
