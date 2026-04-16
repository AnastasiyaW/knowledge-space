---
title: Keyword Research and Semantic Core
category: techniques
tags: [seo-marketing, keywords, semantic-core, wordstat, clustering, search-demand]
---

# Keyword Research and Semantic Core

Complete process of collecting, cleaning, clustering, and assigning keyword groups to pages. Covers Yandex Wordstat operators, collection methods, SERP-based clustering, and tools.

## Core Terminology

- **Semantic core** - complete set of keyword groups covering all user search demand for a site
- **Marker** - anchor query most precisely describing a page's content; the base for expansion
- **Cluster** - group of queries served by a single page
- **Frequency** - number of times a query was searched per month (Wordstat data)
- **Cloud of queries** - full expanded set of queries collected around markers

## Sources for Query Collection

### Reliable Sources
1. **Yandex Wordstat** - direct search demand data (most accurate for RU segment)
2. **Search suggestion parsing** - tools collecting autocomplete suggestions
3. **Parsing programs** - Key Collector, Rush Analytics (automate Wordstat/suggestion collection)

### Less Reliable (Supplementary)
1. **Keyword databases** - pre-collected query lists; unclear origin/completeness; may contain garbage
2. **Competitor site parsing** - reflects competitor's structural decisions, not full demand

### Supporting Data
- Yandex Metrika - queries that previously drove traffic
- Yandex Webmaster - search appearance statistics
- Google Keyword Planner - Google equivalent of Wordstat

## Yandex Wordstat Deep Dive

### Left vs Right Column
- **Left column** - N-gram frequency dictionary: sum of all queries containing the phrase in any form, any order, any length
- **Right column** - "Similar queries" - unreliable; shows queries same users searched, not synonyms

### Wordstat Operators

| Operator | Effect | Example |
|---------|--------|---------|
| None | All queries containing the N-gram | `phone samsung` -> 1,250,000 |
| `"phrase"` | Fixes word count (exact number only) | `"phone samsung"` -> 12,000 |
| `!word` | Fixes exact word form (no inflections) | `!mobile !phones` -> 61,000 |
| `[phrase]` | Fixes word order | `[mobile phones]` -> 938,000 vs `[phones mobile]` -> 60 |
| `+word` | Forces inclusion of stop words | `fridge +how` |
| `-word` | Excludes queries containing word | `fridge -reviews` |
| `(a\|b)` | OR operator for variants | `smartphone (samsung\|galaxy)` |

### Combining Operators
**For collecting queries:**
```text
fridge (samsung|lg) (buy|price|order) -reviews
```

**For precise frequency:**
```text
"[!fridge !samsung]"
```
Quotes + brackets + exclamation = most precise frequency (all three constraints).

### 7-Word Trick
Write the same word 7 times in quotes to find all queries of that exact length:
```text
"keyword keyword keyword keyword keyword keyword keyword"
```
Does NOT work for queries longer than 7 words.

## Frequency Types

| Type | Operator | When to Use |
|------|----------|-------------|
| General | `query` | Abbreviated core, HF markers |
| Phrase | `"query"` | Expanded core, frequency validation |
| Exact | `"[!exact !query]"` | Most precise count, confirming demand |

## Standard Collection Process

### Step 1: Collect Markers
**Manual** - for "dirty" niches or small semantics (<30 Wordstat pages). Tools: WordStatter, WordStat Assistant extensions.

**Automated** - for large catalogs and clean niches. Tools: Rush Analytics, Key Collector.

**Expand markers before collecting**: add Cyrillic/Latin variants, commercial prefixes, price indicators - each generates different suggestion sets.

### Step 2: Parse Wordstat Left Column
For each expanded marker, collect all queries from left column.

### Step 3: Parse Search Suggestions
Suggestions can 5-7x the query list. Each of 100 markers can generate 600-700 unique queries.

### Step 4: Parse Competitor Structure (Optional)
Crawl competitor category pages with Screaming Frog, extract H1 values = competitor's structured semantic decisions.

**Example**: For a phone store, crawl a competitor's `/tag/` pages only (exclude pagination) to extract all filter/attribute pages as H1 values.

### Step 5: Combine and Clean
Remove stop words: non-commercial stops ("reviews", "forum", "DIY"), competitor brand names, geographic stops if not needed.

### Step 6: Check Frequency
Pull frequency for all collected queries. Remove zero-frequency queries before creating pages.

### Step 7: Cluster
**SERP-based clustering** (standard):
- Service collects TOP-10 results for each query
- If 2 queries share >=8 TOP-10 pages -> same group (same intent)
- Principle: same documents in SERP = identical user intent

**Manual refinement always required**: merge incorrectly separated clusters, split incorrectly merged ones, fix cluster names.

### Step 8: Cross-Multiplication (Large Catalogs)
Products x Brands x Attributes = generated query list. Pull frequency, remove zero-frequency results.

## Cluster to Page Assignment

| Page Type | Assignment Rule |
|-----------|----------------|
| Homepage | Highest-frequency "parent" cluster |
| Category pages | Category-level clusters |
| Subcategory pages | Subcategory clusters |
| Product/service pages | Specific product clusters |
| Blog/informational | Informational query clusters |

Some queries can ONLY rank on the homepage - check SERP: if all top results are homepages, assign to homepage.

## AI-Assisted Workflows

### Marker Generation with AI
**Iteration 1**: Provide site type, topic, base keywords, known characteristics -> get ALL characteristic types.

**Iteration 2**: For each characteristic type, list all values including synonyms, jargon, misspellings. Format as table.

**Result**: [characteristic] x [value] combinations -> each row becomes a parse marker.

### Meta Tag Generation
**Title rules**: most frequent query at beginning; each word once; up to 80 chars / 12 words; natural sentence, not keyword list; no discounting words.

**Description rules**: 150-159 chars, max 18 words; call to action + USP; synonyms to keywords; 1-2 neutral emoji allowed.

### Content Brief Generation via AI
1. Run text analysis via Rush Analytics on target keywords
2. Parse competitor pages - extract text with heading hierarchy and token counts
3. Generate outline via AI: title, summary, target audience, H2-H3 structure
4. Distribute keywords and LSI across outline sections with exact occurrence counts

## Tools for Semantic Work

### SEOXL Excel Add-in
- **Color by cluster** - alternating colors for cluster boundaries
- **Sort within cluster** - sorts by frequency inside each cluster
- **Sort clusters by total frequency** - highest-traffic clusters first
- **Lemma dictionary** - most frequent word roots across queries; find stop-word categories
- **Cluster review** - separate sheet with first row per cluster; merge by dragging adjacent
- **Squeeze** - strips specified word roots; exposes distinguishing modifiers for deduplication

### Key Collector (Desktop)
- Mass Wordstat parsing, frequency collection, internal clustering
- 4-pass frequency collection (base, phrase, exact phrase, [exact exact])
- SERP-based clustering: hard (intersection) or soft (union), configurable
- Task scheduler for overnight unattended runs
- Multi-group mode: apply operations to all groups simultaneously

### Rush Analytics (Cloud)
Cloud-based parsing, frequency checking, SERP-based clustering.

### Google Sheets Scripts
All SEOXL functions replicable via Google Apps Script generated by AI. Prompt format: describe scope ("work with selected range") -> describe action per cell -> specify output location -> iterate with corrections.

## Gotchas
- **Right column of Wordstat is unreliable** - use only as supplementary; shows "queries same users searched" not synonyms
- **Zero-frequency queries should not get pages** - creates thin content harming overall site quality
- **SERP-based clustering requires manual review** - automatic clustering fails in 10-20% of cases
- **Marker expansion is critical** - bare markers miss 5-7x queries that expanded variants capture
- **Cross-multiplication generates garbage** - always validate with frequency data before creating pages
- **Do not include LF queries in text analyzer** - they distort results; use up to 6 queries optimal

## See Also
- [[text-optimization]] - Using semantic core for content briefs and text analyzer
- [[site-structure-urls]] - How clusters map to site structure
- [[seo-tools-workflow]] - Tool setup and configuration details
- [[seo-strategy-by-site-type]] - Strategy differences in semantic approach
