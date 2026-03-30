---
title: Keyword Research and Semantic Core
category: concepts
tags: [seo, keywords, semantic-core, wordstat, search-volume, clustering, intent]
---

# Keyword Research and Semantic Core

The semantic core is a structured list of all search queries you want your site to rank for. It is the foundation of every SEO campaign - site structure, content plan, and optimization all derive from it.

## Key Facts

- **Semantic core** = complete set of search queries grouped into clusters, each cluster mapped to a specific page on the site
- Query types by intent: **informational** (how to, what is), **commercial** (best, review, comparison), **transactional** (buy, order, price), **navigational** (brand name, specific site)
- Query types by volume: **high-frequency** (HF, 10k+ monthly), **mid-frequency** (MF, 1k-10k), **low-frequency** (LF, <1k) - LF queries collectively drive 70%+ of organic traffic
- **Wordstat** (wordstat.yandex.ru) is the primary tool for Russian-market keyword research; shows raw frequency, refined frequency (with "!" operator), and exact match (with "!" + quotes)
- Wordstat operators: `!keyword` fixes word form, `"keyword"` limits to exact phrase length, `+keyword` forces inclusion of stop words
- The difference between raw and exact-match frequency can be 10-100x - always check `"!keyword"` for true demand
- **Clustering** = grouping queries that should rank on a single page (based on SERP overlap analysis or semantic similarity)
- See [[on-page-optimization]] for how to use the semantic core in content optimization
- See [[site-structure-architecture]] for mapping clusters to URL structure

## Patterns

### Keyword research workflow

```
1. Seed keywords: brainstorm base terms for the business
2. Expand via Wordstat: collect all related queries
   - Use "!" operator for exact forms
   - Check left column (suggestions) AND right column (related)
3. Competitor analysis: extract keywords competitors rank for
   - Tools: Ahrefs, SEMrush, Keys.so, SpyWords
4. Filter: remove irrelevant, duplicate, zero-volume queries
5. Cluster: group queries by landing page intent
6. Map: assign each cluster to existing or planned page
7. Prioritize: HF commercial queries first, then expand
```

### Wordstat frequency operators

```
Raw query:        купить iphone     -> 500,000 (includes all forms)
Word-form fixed:  !купить !iphone   ->  85,000 (exact word forms)
Exact match:      "!купить !iphone" ->  12,000 (only this 2-word phrase)

Always use "!query" for real demand estimation.
Raw numbers are inflated by long-tail variations.
```

### Clustering methods

```
SERP-based clustering (most accurate):
- For each query, collect top-10 Google/Yandex results
- If two queries share 3+ URLs in top-10 -> same cluster
- Tools: KeyAssort, SE Ranking, Rush Analytics

Semantic clustering (faster, less accurate):
- Group by lemmatized word overlap
- Useful for initial segmentation of large cores (50k+ queries)
```

### Search intent classification

```
Informational:  "how to install wordpress"     -> blog/guide page
Commercial:     "best wordpress hosting 2024"  -> comparison page
Transactional:  "buy hosting for wordpress"    -> product/service page
Navigational:   "bluehost login"               -> not targetable (brand query)

Mixed intent:   "wordpress hosting"            -> check SERP to determine
                If SERP shows mostly product pages -> transactional
                If SERP shows mostly reviews     -> commercial
```

## Gotchas

- **Raw Wordstat frequency is misleading** - "buy apartment" shows 2M+ but exact match "!buy !apartment" is 50x less; never estimate traffic from raw numbers
- **Seasonality** - some queries spike seasonally (e.g., "buy air conditioner" peaks in summer); use Wordstat history to identify seasonal patterns
- **Cannibalization** - if two pages target the same cluster, they compete against each other in search results, weakening both; one cluster = one page
- **Don't ignore zero-frequency queries** - Wordstat only shows queries with 10+ searches/month; real long-tail queries exist below this threshold and convert well
- **Clustering tools differ** - KeyAssort clusters aggressively (fewer groups), manual review clusters conservatively; always verify top clusters manually

## See Also

- [[on-page-optimization]] - Using semantic core for meta tags and content
- [[site-structure-architecture]] - Building site structure from semantic core
- [Yandex Wordstat](https://wordstat.yandex.ru/)
- [Google Keyword Planner](https://ads.google.com/home/tools/keyword-planner/)
- [Ahrefs Keywords Explorer](https://ahrefs.com/keywords-explorer)
- [SEMrush Keyword Magic Tool](https://www.semrush.com/analytics/keywordmagic/)
