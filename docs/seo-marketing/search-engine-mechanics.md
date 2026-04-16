---
title: Search Engine Mechanics
category: concepts
tags: [seo-marketing, search-engines, crawling, indexing, ranking, relevance]
---

# Search Engine Mechanics

How search engines discover, process, and rank web documents. Covers crawling, indexing pipeline, linguistic processing, and the core ranking factor groups that determine SERP positions.

## Key Terminology

- **Document** - a web page (not a site); the fundamental unit of search
- **Collection** - total set of indexed documents (~13.5 billion in Yandex)
- **Term** - a single word
- **Query** - text entered in search field
- **Intent** - what the user actually wants (not just what they typed)
- **Relevance** - how well a document matches user intent expressed through query

## Crawling Architecture

**Crawler (search bot/robot/spider)** - program that finds and scans sites by following links, storing content in the search engine database.

### Crawler Control Mechanisms
1. `robots.txt` - allow/disallow rules for bot access
2. `sitemap.xml` - map of pages to crawl
3. Yandex Webmaster / Google Search Console - direct management
4. Meta robots, canonical, x-robot-tag, noindex/nofollow tags
5. RSS feed
6. YML file (Yandex product catalog format)
7. IndexNow / Google Indexing API - instant push notifications

## Linguistic Processing

### Lemmatization
All word forms reduced to base form (lemma). Enables matching queries to documents regardless of inflection.

### Inverted Index
For each term across all documents, stores which documents contain that term.

```yaml
Direct:   Document 1 → [word_a, word_b, word_c]
Inverted: word_a → [Document 1, Document 3]
          word_b → [Document 1, Document 2]
```

**Boolean search**: `Cat AND Hare AND NOT Fox` - find all documents matching the expression.

### Query Rewriting
- **Query rewrite** - modifying query weights on individual words for better results
- **Query reformulation** - adding synonyms to the query automatically
- Example: "what is seo" rewritten to include "means", "abbreviation", "stands for"

## Ranking Factor Groups

Over 2000+ factors exist. Grouped into categories:

### Text Factors (Internal)
- Term frequency in document zones (TF-IDF, BM25)
- Text uniqueness
- LSI (latent semantic indexing - related terms)
- Text length, grammar quality
- Direct keyword inclusion and word permutation presence

### Link Factors (External)
- Anchor list composition
- Link growth rate and total backlink count
- Authority and count of linking domains
- Topical similarity between donor and acceptor
- Donor's commercial "sellability" indicator

### Commercial Factors (Internal)
- Product/service assortment size
- Payment and delivery options
- Guarantee and return policy, price visibility
- Structured catalog, multiple contact methods
- Conversion elements (CTAs, forms, callback)

### Host Factors (Internal)
- Domain age, number of indexed pages
- Domain ownership change history
- Domain zone (.ru, .com, etc.)

### Technical Factors (Internal)
- Server response codes, code validity
- Page load speed, HTTPS
- Duplicate content and redirects

### Behavioral Factors
- **Internal (on-site)**: time on site, depth of browsing, bounce rate
- **External (in SERP)**: last click, single click, type-in return visits, snippet CTR

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
- **Yandex vs Google priorities are inverted** - links dominate Google, behavioral factors dominate Yandex. Strategy must account for this
- **2000+ factors** does not mean all are equal - a handful of factors per query type drive 80%+ of ranking variance
- **Relevance != keyword count** - modern engines use semantic understanding, not just term matching
- **Sandbox applies universally** - even legitimate new sites face 2-12 months of suppressed rankings

## See Also
- [[ranking-algorithms-history]] - Algorithm timelines and neural network evolution
- [[text-optimization]] - Document zones and relevance scoring
- [[behavioral-factors-ctr]] - Behavioral factors deep dive
- [[commercial-ranking-factors]] - Commercial factors and E-E-A-T
