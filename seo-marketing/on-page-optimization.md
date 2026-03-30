---
title: On-Page Text Optimization
category: concepts
tags: [seo, meta-tags, title, description, h1, content-optimization, text-factors, lsi]
---

# On-Page Text Optimization

Optimization of individual page elements (meta tags, headings, body text) that search engines use to determine page relevance for specific queries. Text factors are especially critical for Yandex ranking.

## Key Facts

- **Text ranking factors** = how search engines evaluate content relevance based on keyword placement, density, and semantic completeness across page zones
- Text factors carry significantly more weight in Yandex than in Google; Google relies more heavily on link authority and behavioral signals
- Key text zones in priority order: **Title** > **H1** > **URL** > **Description** > **H2-H6 headings** > **body text** > **alt attributes** > **anchor text of internal links**
- **Title tag**: most important on-page factor; should contain the primary keyword near the beginning; optimal length 50-70 characters (Google truncates at ~60)
- **Meta description**: not a direct ranking factor but critically affects CTR; optimal length 150-160 characters; should contain a call-to-action
- **H1**: one per page, should contain the primary keyword, must differ from Title tag (can be longer, more natural)
- **LSI keywords** (Latent Semantic Indexing): semantically related terms that help search engines understand topic depth; include naturally throughout content
- See [[keyword-research-semantic-core]] for identifying target queries per page
- See [[technical-seo-audit]] for ensuring meta tags are properly implemented

## Patterns

### Meta tag optimization template

```html
<!-- Title: primary keyword + modifier + brand -->
<title>Buy iPhone 15 Pro Max - Price from $999 | StoreName</title>

<!-- Description: value prop + CTA + modifiers -->
<meta name="description" content="iPhone 15 Pro Max at the best price.
Free shipping, 2-year warranty. Compare models and order online today.">

<!-- H1: primary keyword in natural form -->
<h1>iPhone 15 Pro Max</h1>

<!-- H2s: secondary keywords / cluster subtopics -->
<h2>iPhone 15 Pro Max Specifications</h2>
<h2>Compare iPhone 15 Models</h2>
<h2>Customer Reviews</h2>
```

### Title tag formulas by page type

```
Category page:   [Primary KW] - [Modifier] | [Brand]
                 "Buy Running Shoes - Free Shipping | SportShop"

Product page:    [Product Name] - [Key Feature] | [Brand]
                 "Nike Air Max 90 - Black/White | SportShop"

Service page:    [Service KW] in [Location] - [USP] | [Brand]
                 "Plumbing Services in NYC - 24/7 Emergency | FixIt"

Blog post:       [Question/Topic] - [Year if relevant] | [Brand]
                 "How to Choose Running Shoes - 2025 Guide | SportShop"
```

### Content optimization checklist

```
1. Title:       Contains primary keyword, <70 chars
2. H1:          Contains primary keyword, differs from Title
3. URL:         Short, contains keyword, hyphen-separated
4. Description: 150-160 chars, contains keyword, has CTA
5. H2-H3:       Contain secondary/LSI keywords
6. Body text:   Primary keyword in first 100 words
7. Images:      Alt text contains keyword variations
8. Internal links: Anchor text with relevant keywords
9. Content depth: Covers all user intent aspects
10. Word count:  Match or exceed top-ranking competitors
```

### Text quality spectrum

```
BAD:    No text / copy-pasted / auto-generated spam
POOR:   Template text with keyword stuffing
OK:     Unique text but generic, no expertise signals
GOOD:   Expert text with original data/insights
BEST:   Comprehensive, answers all user intents,
        includes tables/images/video, E-E-A-T signals
```

## Gotchas

- **Keyword stuffing penalty** - repeating the keyword unnaturally triggers spam filters in both Google and Yandex; natural integration > forced repetition
- **Title != H1** - many CMS auto-duplicate Title into H1; they should be related but not identical (Title is for SERP, H1 is for on-page context)
- **Description is not a ranking factor** but directly impacts CTR, which IS a ranking factor; treat it as ad copy, not keyword dumping
- **Content length is not a ranking factor per se** - longer content correlates with better rankings because it tends to be more comprehensive, not because of word count; match competitor depth, don't pad
- **Duplicate meta tags across pages** tank SEO - each page must have unique Title and Description; audit with Screaming Frog or Sitebulb
- **Alt text is for accessibility first** - describe what the image shows; keyword inclusion should be natural, not forced

## See Also

- [[keyword-research-semantic-core]] - Building the keyword map for optimization
- [[site-structure-architecture]] - URL structure and internal linking
- [[seo-content-strategy]] - Content planning beyond individual page optimization
- [Google Title Link Documentation](https://developers.google.com/search/docs/appearance/title-link)
- [Google Meta Description Best Practices](https://developers.google.com/search/docs/appearance/snippet)
- [Ahrefs On-Page SEO Guide](https://ahrefs.com/blog/on-page-seo/)
