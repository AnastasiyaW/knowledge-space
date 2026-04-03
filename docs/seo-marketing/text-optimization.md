---
title: Text Optimization and Content Zones
category: techniques
tags: [seo-marketing, text-optimization, title, meta-description, seo-text, tf-idf, bm25]
---

# Text Optimization and Content Zones

How search engines evaluate text relevance (TF-IDF, BM25) and the practical methodology for optimizing every document text zone: Title, H1, Description, anchor text, SEO body text. Covers two distinct optimization strategies - traffic vs positional - and Text Analyzer workflows.

## Text Relevance Calculation

### TF-IDF
`TF-IDF = TF x IDF`
- **TF (Term Frequency)** - ratio of word occurrences to total document words
- **IDF (Inverse Document Frequency)** - inverse of how often a word appears across all documents

Key principle: a word frequent in ONE document but rare across all documents has high significance for that document. Stop words (prepositions, conjunctions) appear everywhere and get very low weight.

### BM25
Improved ranking function actively used by Yandex:
- Better relevance calculation for multi-word queries than TF-IDF
- Does NOT account for word position relative to each other
- Key in Yandex ranking algorithms

### Quorum and Word Order
- Documents must contain enough passage coverage (quorum) to enter ranking
- Pair word occurrences (AB) and full sets (ABC) counted separately
- Rarer words in query carry higher weight
- Word order in document should match query structure

## Two Optimization Strategies

### Traffic Optimization
**For**: E-commerce, aggregators, portals with wide semantic space.

- Targets maximum coverage of MF/LF queries, not specific HF positions
- Growth driver: creation + optimization of new landing pages
- Template-based optimization at scale
- Iteration: build structure for main sections, apply templates, then deepen category by category

### Positional Optimization
**For**: Service sites, B2B, construction, legal - small keyword sets.

- Targets maximum positions on ALL queries (HF especially critical)
- Growth driver: iterative improvement of a fixed page set
- Manual, precise optimization
- Iteration: full semantics -> full structure -> create pages -> optimize (iteration 1) -> monitor -> correct (iteration 2) -> repeat

## Document Text Zones

| Zone | Tag | Ranking Impact | Notes |
|------|-----|----------------|-------|
| Title | `<title>` | Highest | Most important SEO zone |
| H1 | `<h1>` | Very high | One per page, main query |
| H2-H6 | `<h2>`-`<h6>` | High | Structural headings |
| Description | `<meta description>` | CTR only (not text ranking) | Click-through optimization |
| Anchor text | `<a>` | High for donor; counts for acceptor | Internal + external links |
| Text fragments | Various | Medium | Tables, characteristics, navigation, banners |
| SEO text | Body main text | Medium | Main copywritten content |
| Keywords meta | `<meta keywords>` | None | Ignored by all engines; delete if spammy |
| noindex | `<!--noindex-->` | Removal | Yandex only; hides content from indexation |

## Title Tag

### General Rules
- Most important SEO zone
- Exact inclusion of most important queries
- Most important query at beginning
- One sentence, NOT split by period
- Yandex: up to 20 words; Google: up to 12 words
- Use synsets (synonym groups)
- Add primary region toponym when relevant

### Traffic Title (Wide Coverage)
```
Buy [Category.Singular] in [City], prices on [Category.Plural], store [Brand]
```
Template variables with all inflection forms. 2 occurrences of main word in different morphological forms.

### Positional Title (Max Rank)
- Exact keyword occurrences entered "as is"
- Almost no tail queries; pattern from TOP competitors
- Usually shorter, 1 occurrence of main word

### Article Title
- Keywords + clickbait for informational intent
- Attention-grabbing phrasing

## H1 Tag
- ONE per page, placed above content
- Only main query (preferably exact form)
- Short, grammatically correct
- Not polluted with other tags (no `<p>` inside H1)

## Meta Description
- Not visible in browser; does NOT participate in text ranking
- Purpose: increase SERP snippet CTR
- Length: 120-170 chars (Yandex), up to 300 chars (Google)
- 2-3 sentences, 1 keyword per sentence
- Commercially attractive, use special symbols: `http://unicode-table.com/`

## SEO Text Rules

### Commercial Sites (Yandex)
- Strictly follow Text Analyzer (TA) requirements
- Match exact keyword occurrence counts
- Even keyword density throughout text
- Do NOT abuse commercial tails (buy, price, order)
- NO nonsensical keyword insertions
- Include thematic LSI words, minimize filler
- **Without Text Analyzer analysis - do not write at all**

### Writing for Both Engines
Tension: Google rewards large optimized texts; Yandex may penalize ANY text on commercial pages.

If Yandex TOP competitors have no text, you cannot use optimized text without risk.

Workarounds for Google-only text:
- Output via JavaScript `document.write`
- Add via Google Tag Manager
- Via GTM: canonical from page without text (closed from Yandex) to copy with text

### Informational Articles
- Table of contents, clear H1/H2/H3 structure
- Cover ALL useful points from all competitors
- Add extra paragraphs from semantics and unique insights
- Size: longer than any single competitor
- Rich media (images, video, for how-to: image per step)
- Alternate between text, images, quotes, lists ("user sticks")

### Product Listings (Baden-Baden Era)
Only generated text survives on listings:
- 1 occurrence of main query
- 1-2 occurrences of individual query words (spread apart)
- Do NOT write commercial words near the query
- 2-3 sentences, up to 100 words, carrying useful information

## Text Analyzer (TA) Workflow

**Purpose**: Reference tool before writing ANY SEO text.

### TA Configuration
- Clustering: HARD mode with threshold 3
- Exclude sites of different type from analysis
- Use synonyms; do NOT analyze single query
- Up to 6 queries optimal (more dilutes results)
- Do NOT include LF queries (they distort results)
- Use SERP of target region

### What TA Determines
- Whether text is needed at all on this page type
- Safe number of keyword occurrences by type
- Content brief generation almost automatically
- Keyword spam detection across all document zones

## Copywriter Brief Structure
1. Heading structure (H2-H3 with target keywords)
2. Instructions for each section
3. LSI keywords per paragraph
4. Word count and paragraph count per section
5. Links to best competitor examples
6. Text Analyzer output with highlighted required occurrences

## Optimization Checklist

| Zone | Traffic Site | Positional Site | Info Site |
|------|-------------|-----------------|-----------|
| Title | Template, wide coverage | Exact match, short | Clickbait + query |
| H1 | Template or manual, exact | Exact, short | Natural, question/phrase |
| Description | Template | Manual, CTR-focused | Manual, CTR-focused |
| SEO text | By TA; generated if short | By TA; written manually | Full article, competitive |
| Headings | Template H2/H3 | Manual semantic hierarchy | Rich H2-H4 with queries |
| LSI | Auto-generated | By TA | Rich, ~50 relevant terms |

## Gotchas
- Keywords in `<b>`, `<strong>`, `<em>` signal keyword manipulation to search engines
- Baden-Baden filter penalizes keyword density spam on commercial pages
- Text on product listings should be generated, not hand-written (generation survives Yandex filters)
- Copywriters must be trained on TA rules; those who cannot follow them must be replaced
- Token count approximation: 1 word ~ 1.3 tokens; 1,000 words ~ 1,300 tokens

## See Also
- [[keyword-research-semantic-core]] - Building the semantic core that drives text optimization
- [[on-page-optimization]] - Content audit and page-type content blocks
- [[search-engine-filters]] - Baden-Baden and text-related penalties
- [[seo-tools-and-workflow]] - Rush Analytics Text Analyzer, content checking tools
