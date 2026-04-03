---
title: Keyword Research and Semantic Core
category: techniques
tags: [seo-marketing, keywords, semantic-core, wordstat, clustering]
---

# Keyword Research and Semantic Core

The complete process of building a semantic core: collecting marker queries, parsing search demand, cleaning and clustering, then mapping clusters to site pages. Covers Yandex Wordstat operators, SERP-based clustering, and AI-assisted workflows.

## Core Terminology

- **Semantic core** - complete set of keyword groups covering all user search demand for a site
- **Marker** - anchor query that most precisely describes a page's content; the base for expansion
- **Cluster** - group of queries that should be served by a single page
- **Frequency** - number of times a query was searched per month (Wordstat data)
- **Cloud of queries** - full expanded set of queries collected around markers

## Sources for Query Collection

### Primary (Reliable)
1. **Yandex Wordstat** - direct search demand data (most accurate for RU)
2. **Search suggestion parsing** - autocomplete suggestions from Yandex/Google
3. **Parsing tools** - Key Collector, Rush Analytics (automate collection)

### Secondary (Supplements)
- **Keyword databases** - pre-collected query lists; quality unknown
- **Competitor site parsing** - reflects competitor's structural decisions, not full demand
- **Yandex Metrika** - queries that previously drove traffic
- **Google Keyword Planner** - Google search volume estimates

## Yandex Wordstat Operators

| Operator | Effect | Example |
|---------|--------|---------|
| None | All queries containing the N-gram | `smartphone samsung` -> 1,250,000 |
| `"phrase"` | Fixes word count (exact number of words) | `"smartphone samsung"` -> 12,000 |
| `!word` | Fixes exact word form (no inflections) | `!mobile !phones` -> 61,000 |
| `[phrase]` | Fixes word order | `[mobile phones]` -> 938,000 vs `[phones mobile]` -> 60 |
| `+word` | Forces inclusion of stop words | `fridge +how` |
| `-word` | Excludes queries containing word | `fridge -reviews` |
| `(a\|b)` | OR operator for variants | `phone (samsung\|galaxy)` |

### Operator Combinations
Combine for precision:
- **Collection**: `fridge (samsung\|lg) (buy\|price) -reviews`
- **Exact measurement**: `"[!exact !query]"` - quotes + brackets + exclamation = most precise frequency

### 7-Word Trick
Repeat a word 7 times in quotes to find all 7-word queries containing it:
```
"keyword keyword keyword keyword keyword keyword keyword"
```
Does NOT work for queries longer than 7 words.

## Frequency Types

| Type | Operator | Use Case |
|------|----------|----------|
| General | `query` | Abbreviated core, HF markers |
| Phrase | `"query"` | Expanded core, frequency validation |
| Exact | `"[!exact !query]"` | Most precise count, confirming demand |

## Standard Collection Process

### Step 1: Collect Markers
**Manual** (dirty niches, small semantics <30 Wordstat pages): browser extensions like WordStatter.
**Automated** (large catalogs, clean niches): Rush Analytics, Key Collector.

Expand markers before parsing: add Cyrillic/Latin variants, commercial prefixes (`buy`, `price`), different spellings.

### Step 2: Parse Wordstat Left Column
For each expanded marker, collect all queries from the left column.

### Step 3: Parse Search Suggestions
Suggestions can 5-7x the query list. Each marker generates 600-700 unique queries.

### Step 4: Parse Competitor Structure (Optional)
Crawl competitor category pages with Screaming Frog, extract H1 values as structured semantic decisions.

### Step 5: Clean
Remove stop words: non-commercial terms (reviews, forum, DIY), competitor brands, geographic terms if irrelevant.

### Step 6: Check Frequency
Remove zero-frequency queries before creating pages.

### Step 7: Cluster (SERP-Based)
- Service collects TOP-10 results for each query
- If 2 queries share >= 8 TOP-10 pages -> same group (same intent)
- Tools: Rush Analytics clustering module, Key Collector
- **Manual refinement always required**: merge incorrectly split clusters, split incorrectly merged ones

### Step 8: Cross-Multiplication (Large E-commerce)
Products x Brands x Attributes = generated query list. Pull frequency, remove zeros.

## Cluster-to-Page Assignment

| Page Type | Assignment Rule |
|-----------|----------------|
| Homepage | Highest-frequency "parent" cluster |
| Category pages | Category-level clusters |
| Subcategory pages | Subcategory clusters |
| Product/service pages | Specific product clusters |
| Blog/informational | Informational query clusters |

Some queries can ONLY rank on the homepage - check SERP: if all top results are homepages, that query belongs there.

## AI-Assisted Marker Generation

**Iteration 1**: Describe site type, topic, base keywords, known characteristics. Ask AI to list ALL characteristic types for the niche.

**Iteration 2**: For each characteristic type, list all possible values including synonyms, colloquial variants, common misspellings. Format as table with topic keyword appended.

Result: characteristic x value matrix where each row becomes a parse marker.

## AI-Assisted Meta Tag Generation

### Title Rules (via AI prompt)
- Most frequent query at beginning in original word order
- Each word used only once (including different inflections)
- Use only words from cluster queries
- Length: up to 80 characters / 12 words
- Must read naturally (not keyword list)

### Description Rules (via AI prompt)
- 150-159 characters, max 18 words
- Include call to action and USP
- Use synonyms to keywords, read naturally
- 1-2 neutral emoji in middle/end

## Spreadsheet Tools for Semantic Work

### SEOXL Excel Add-in
- **Cluster coloring** - highlights rows when cluster group changes
- **H1 propagation** - copies H1 to all rows in same cluster
- **Sort within cluster** - by frequency inside each cluster
- **Sort clusters** - by aggregate frequency
- **Lemma dictionary** - most frequent word roots across all queries
- **Cluster review (Razbor)** - separate sheet with first row per cluster, hover shows all queries
- **Squeeze (Vyzhimka)** - strips specified word roots, exposes distinguishing modifiers for deduplication

### Duplicate Cluster Workflow
1. Apply squeeze to cluster-label column (strip product word + synonyms)
2. Sort by squeezed column
3. Conditional formatting to highlight duplicates
4. In cluster review: drag duplicates adjacent, delete separator
5. Complete review -> groups merged on main sheet

## Gotchas
- Wordstat left column shows N-gram sums, not exact query frequency - always use quotes for real numbers
- SERP-based clustering is the standard method because it directly reflects search engine intent interpretation
- Never create pages for zero-frequency queries
- Competitor parsing reflects their structural decisions, not full demand - use as supplement only
- AI-generated markers need frequency validation; many generated combinations will have zero search volume

## See Also
- [[text-optimization]] - Using semantic core for text briefs
- [[site-structure-architecture]] - Mapping clusters to URL structure
- [[seo-tools-and-workflow]] - Key Collector, Rush Analytics, Screaming Frog
- [[seo-strategy-by-site-type]] - Different semantic strategies per site type
