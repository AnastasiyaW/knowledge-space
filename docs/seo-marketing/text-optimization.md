---
title: Text Optimization
category: techniques
tags: [seo-marketing, text-optimization, meta-tags, title, h1, description, tf-idf, bm25, content-brief]
---

# Text Optimization

Document text zones, meta tag rules, text relevance scoring (TF-IDF, BM25), text analyzer workflow, and content brief creation. Covers both traffic-oriented and positional optimization strategies.

## Text Relevance Calculation

### TF-IDF
- **TF (Term Frequency)** - ratio of word occurrences to total document words
- **IDF (Inverse Document Frequency)** - inverse of how often word appears across all documents
- High TF-IDF = word frequent in ONE document but rare across collection
- Stop words (prepositions, conjunctions) appear everywhere -> very low TF-IDF

### BM25
Improved ranking function actively used by Yandex:
- Better relevance calculation for multi-word queries than TF-IDF
- Does NOT account for word position relative to each other
- Actively used in Yandex ranking algorithms

### Quorum Filtering and Word Order
- Documents must contain enough passage coverage (quorum) to enter main ranking
- Pair word occurrences (AB) and full set (ABC) counted separately
- Rarer words in query carry higher weight
- Word order in document should match query structure

## Two Optimization Strategies

### Traffic Optimization
**For**: E-commerce, aggregators, portals

- Maximum coverage of wide semantic core
- Many MF/LF queries, not positions on specific HF queries
- Growth driver: creation + optimization of new landing pages
- Mass-production character of SEO

**Iteration**: First-approximation semantics -> structure for main sections -> create all possible pages -> template optimization -> detailed semantics per category -> manual optimization per category -> repeat.

### Positional Optimization
**For**: Service sites, B2B, construction, transport, legal

- Maximum position growth on small keyword set
- HF queries especially critical
- Growth driver: iterative improvement of fixed set of pages
- Precise, targeted character of SEO

**Iteration**: Full semantics -> full structure -> create all pages -> manual optimization iteration 1 -> deploy, wait, monitor -> corrections iteration 2 -> repeat.

## Document Text Zones

| Zone | Tag | Ranking Impact | Notes |
|------|-----|----------------|-------|
| Title | `<title>` | Highest | Most important SEO zone |
| H1 | `<h1>` | Very high | One per page, main query |
| H2-H6 | `<h2>`, `<h3>` | High | Structural headings |
| Description | `<meta description>` | CTR only (not ranking) | Click-through optimization |
| Anchor text | `<a>` | High for donor + acceptor | Internal + external links |
| Text fragments | Body small text | Medium | Tables, characteristics, navigation |
| SEO text | Body main text | Medium | Main copywritten text |
| Keywords meta | `<meta keywords>` | None | Ignored; delete if spammy |
| noindex blocks | `<!--noindex-->` | Removal | Yandex only |

## Title Tag Rules

### General Rules
- Most important SEO zone
- Exact inclusion of most important queries
- Most important query at beginning
- One sentence, NOT split by period
- Yandex: up to 20 words; Google: up to 12 words
- Use synsets (synonym groups)
- Add primary region toponym
- Only zone where grammatical agreement not critical

### Traffic Title
Cover maximum queries:
```text
Buy fridge in Moscow, prices for fridges, online store Brand
```

**Template formula:**
```text
Buy %Category.Nom.Sg% in %City.Prep% online, prices for %Category.Nom.Pl%.
Sale of %Category.Gen.Pl%.
```

Rules: synonyms, transliterations, permutations; sacrifice exact keyword form for breadth; word order > word form; 2 occurrences of main word in different forms.

### Positional Title
Maximum position on specific queries:
```sql
PVC windows from manufacturer - Moscow
```

Rules: exact keyword occurrences entered "as is"; almost no tail queries; pattern from strong competitors; shorter than traffic title; 1 occurrence of main word.

### Article Title
Clicks and information intent:
```text
Simple recipe for cottage cheese pancakes with step-by-step photos
```

Rules: keyword inclusions + clickbait; attention-grabbing phrasing; look at competitor solutions.

## H1 Tag
- Must be ONE per page, placed above content
- Only main query (preferably in exact form)
- Short, grammatically correct
- Not polluted with other tags (`<p>` inside H1 = bad)

## Meta Description
- NOT visible in browser (code only)
- Does NOT participate in text ranking
- Purpose: increase SERP snippet CTR
- Length: 120-170 chars (Yandex), up to 300 chars (Google)
- Both key occurrences should fit in 170 chars
- 2-3 sentences; 1 keyword per sentence
- Special symbols: unicode-table.com

## noindex Tag (Yandex Only)
```html
<!--noindex-->content to hide<!--/noindex-->
```
Prohibits indexation of any page section. Does NOT work in Google.

## Text Analyzer (TA)

**Purpose**: Reference tool before writing ANY SEO text.

**What it does**:
- Analyzes competitor texts in TOP
- Determines safe number of keyword occurrences by type
- Shows whether text is needed at all
- Creates content brief almost automatically
- Checks all document zones for keyword spam

**Tool**: Rush Analytics text analyzer

### TA Requirements
- Clustering: HARD mode with threshold 3
- Exclude sites of different type from analysis
- Use synonyms; do NOT analyze single query
- Up to 6 queries optimal (more dilutes results)
- Do NOT include LF queries - they distort results
- Use SERP of target region

## SEO Text on Commercial Sites

- Strictly follow Text Analyzer requirements
- Follow exact keyword occurrence count and text volume
- Sometimes text is genuinely not needed
- Even keyword density throughout text
- Do not abuse commercial words (buy, price, order)
- Include thematic LSI words, no filler
- **WITHOUT TEXT ANALYZER ANALYSIS - DO NOT WRITE AT ALL**

### Yandex vs Google Text Tension
Google rewards large optimized texts; Yandex may penalize ANY text on commercial pages.

**If competitors in Yandex TOP have no text -> you cannot use optimized text without risk.**

Workarounds to show text only to Google:
- Output text via JavaScript `document.write`
- Add text via Google Tag Manager
- Via GTM: set canonical from page without text to copy with text

## Content Types by Page

### Product Listings
- Only write text if Text Analyzer recommends it
- TA recommends <100 words -> text NOT needed
- TA recommends ~100-150 words -> generation only
- TA recommends >150 words -> can write full text
- Track anchor zone `<a>` occurrences separately

### Listing Generation Rules (Baden-Baden Era)
- 1 occurrence of main query
- 1-2 occurrences of individual words (spread apart)
- Do NOT write commercial words near the query
- 2-3 sentences, up to 100 words total
- Connected, useful text

### Product Cards
- Text uniqueness NOT critical
- Page uniqueness via: generated text, customer reviews, accessories section
- Same generation rules as category pages

### Service Pages
- Only meaningful text by copywriter
- Do NOT generate; mandatory: use Text Analyzer
- Only write based on Content Audit

### Informational Articles
- Table of contents, clear H1/H2/H3 structure
- Include LSI terms (no more than 50)
- Cover ALL useful points from all competitors + extras
- Size: longer than any single competitor
- More images, video; alternate text/images/lists/quotes

## Copywriter Brief Structure

Complete brief must contain:
1. Heading structure (H2-H3 with target keywords)
2. Instructions for each section
3. LSI keywords for each paragraph
4. Word/paragraph count per section
5. Links to best competitor examples
6. Text analyzer output with highlighted required occurrences

**Token count**: 1 word = 1.3 tokens; 1,000 words = 1,300 tokens.

## Optimization Checklist by Site Type

| Zone | Traffic Site | Positional Site | Informational |
|------|-------------|-----------------|---------------|
| Title | Template, wide coverage | Exact match, short | Clickbait + query |
| H1 | Template or manual, exact | Exact, short | Natural phrase |
| Description | Template | Manual, CTR-focused | Manual, CTR-focused |
| SEO text | By TA; generated if short | By TA; copywriter | Full article |
| Heading structure | Template h2/h3 | Manual semantic | Rich h2/h3/h4 |
| LSI words | Auto-generated | By TA | Rich, 50 LSI |
| Content audit | Required | Required | Required |

## Gotchas
- **Keywords meta tag does nothing** - delete if spammy, otherwise ignore
- **Baden-Baden penalizes keyword density** - always check via text analyzer before writing
- **Keywords in bold/strong tags signal manipulation** - do not use `<b>`, `<strong>`, `<em>` on keywords
- **Description does not affect ranking** - only CTR; don't stuff keywords for ranking purposes
- **Yandex vs Google text conflict is real** - the GTM/JS workaround is a standard practice, not a hack
- **Commercial tail words hurt** - "buy", "price", "order" near keywords trigger spam detection

## See Also
- [[keyword-research-semantic-core]] - Semantic core collection and clustering
- [[behavioral-factors-ctr]] - CTR optimization via snippets
- [[niche-content-audit]] - Content audit methodology
- [[filters-and-penalties]] - Baden-Baden filter details
