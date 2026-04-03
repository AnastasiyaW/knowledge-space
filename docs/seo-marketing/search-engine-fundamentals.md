---
title: Search Engine Fundamentals
category: concepts
tags: [seo-marketing, search-engines, crawling, indexing, ranking]
---

# Search Engine Fundamentals

How search engines discover, process, and rank web content. Covers crawling architecture, inverted indexes, linguistic processing, and the high-level ranking pipeline that every subsequent SEO technique builds upon.

## Key Terminology

- **Document** - a web page (not a site); the atomic unit of indexing
- **Collection** - total set of indexed documents (Yandex: ~13.5 billion)
- **Term** - a single word after linguistic processing
- **Query** - text entered in the search field
- **Intent** - what the user actually wants (may differ from literal query)

## Crawling Architecture

**Crawler (spider/bot)** - program that discovers and scans pages by following links, storing content in the search engine database.

### Crawler Control Mechanisms
| Method | Purpose |
|--------|---------|
| `robots.txt` | Allow/disallow rules for bot access |
| `sitemap.xml` | Map of pages to crawl |
| Yandex Webmaster / Google Search Console | Direct indexation management |
| `meta robots`, `canonical`, `x-robots-tag` | Per-page indexation directives |
| RSS / YML feeds | Structured content feeds |
| IndexNow / Google Indexing API | Push notifications for instant discovery |

### Crawl Budget
Search engines allocate finite crawl resources per site. Wasting crawl budget on duplicate, parameterized, or low-value pages reduces coverage of important pages. Large sites (100k+ pages) must actively manage what robots crawl.

## Linguistic Processing

### Lemmatization
All word forms reduced to base form (lemma): "buying", "bought", "buys" -> "buy". Enables matching queries to documents regardless of inflection.

### Inverted Index
Core data structure for search. For each term across all documents, stores which documents contain that term.

```
Direct index:   Document 1 -> [word_a, word_b, word_c]
Inverted index: word_a -> [Document 1, Document 3]
                word_b -> [Document 1, Document 2]
```

Boolean search: `Cat AND Hare AND NOT Fox` -> all documents matching the expression.

### Query Rewriting
Search engines modify queries before matching:
- **Query rewrite** - adjusting word weights for better relevance
- **Query reformulation** - adding synonyms automatically
- Example: "what is SEO" is expanded to include "means", "abbreviation", "stands for"

## Ranking Factor Groups

2000+ factors exist. Grouped into six categories:

### Text Factors (Internal)
- Term frequency in document zones (TF-IDF, BM25)
- Text uniqueness
- LSI (latent semantic indexing - related terms)
- Direct keyword inclusion and word permutation
- Grammar and spelling quality

### Link Factors (External)
- Anchor list composition
- Link growth dynamics
- Authority of linking domains
- Topical similarity between donor and acceptor
- Donor's "sellability" indicator (signals purchased links)

### Commercial Factors (Internal)
- Product/service assortment breadth
- Payment and delivery options, guarantee/return policy
- Price visibility and structured catalog
- Multiple contact methods, conversion elements

### Behavioral Factors
- **Internal (on-site)**: time on site, browsing depth, bounce rate
- **External (SERP)**: last click, single click, snippet CTR, type-in visits

### Host Factors
- Domain age, indexed page count, ownership change history
- Domain zone (.com, .ru, etc.), domain-level sanctions

### Technical Factors
- Server response codes, code validity
- Page load speed (Core Web Vitals)
- HTTPS, duplicate content handling, redirects

## Ranking Priority by Search Engine

| Factor Group | Yandex Priority | Google Priority |
|-------------|----------------|----------------|
| Behavioral | #1 (highest) | #3 |
| Text | #2 | #2 |
| Links | #3 | #1 (highest) |
| Commercial | #4 | #4 |
| Technical | foundational | foundational |

## Sandbox Filter

Temporary filter applied to new sites to prevent manipulation:
- Duration: 2-12 months depending on site
- Affects nearly all newly created sites
- Purpose: filters out sites created via black-hat methods

## Gotchas
- Yandex and Google weight factor groups differently - strategies must account for both
- Crawl budget is finite; poorly structured sites waste it on duplicate/parameterized pages
- Query rewriting means exact-match keyword targeting is less critical than intent matching
- Sandbox filter means new sites should not expect ranking results for 2-12 months

## See Also
- [[ranking-algorithms]] - Neural network evolution in Yandex and Google
- [[technical-seo-audit]] - Managing crawl budget and indexation
- [[behavioral-factors]] - Behavioral signals deep dive
- [[commercial-ranking-factors]] - Commercial factors and E-A-T
