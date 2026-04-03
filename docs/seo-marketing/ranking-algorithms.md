---
title: Ranking Algorithms - Yandex and Google
category: concepts
tags: [seo-marketing, algorithms, yandex, google, neural-networks, bert, yati]
---

# Ranking Algorithms - Yandex and Google

Evolution of search engine algorithms from heuristic rules to transformer-based neural ranking. Covers the major algorithm updates, their impact on SEO strategy, and the key technical signals (Core Web Vitals, E-E-A-T) that shape modern ranking.

## Yandex Algorithm Evolution

### Pre-Neural Era
| Algorithm | Year | Impact |
|-----------|------|--------|
| Nepot filter | 2005 | Nullified link weight when link deemed paid/commercial |
| Magadan | 2008 | Named algorithm era begins; geo-dependence; text uniqueness |
| ACS filter | 2009 | Auto-generated content sanctioned |
| Snozhinks | 2009 | Matrixnet ML introduced; keyword-stuffed texts penalized |
| Krasnodor | 2010 | "Spectrum" technology: classifies queries by multiple intents |
| Baden-Baden | 2017 | Penalty for over-optimized content with excess keyword density |

### Neural Era

**Palekh (2016)** - Deep Structured Semantic Model (DSSM). Compares query against document title using neural embeddings.

**Korolev (2016-2018)** - Extends DSSM to full page content. Integrates assessor-based quality ratings.

**Expert-assessment networks (2019)** - Training targets based on expert quality ratings instead of click signals.

**YATI (2020)** - Yet Another Transformer with Improvements:
- Transformer architecture processing multiple streams: anchor list, click-based URL index
- Processes texts up to 10 sentences in full (previous models truncated)
- Word vector space for semantic understanding
- Part of the Y1 update (2021): +2000 improvements, YaTI + YaLM

**Yandex Proxima** - quality metric combining:
- Commercial quality components
- Domain-specific quality signals (medicine, legal, financial)
- User value: Expertise, Authority, Trustworthiness

## Google Algorithm Evolution

| Algorithm | Year | Impact |
|-----------|------|--------|
| Panda | 2011 | Penalizes thin/duplicate/low-quality content; affected 12% of results |
| Penguin | 2012 | Penalizes spam links, link farms, purchased link schemes |
| Hummingbird | 2012 | Semantic query understanding; context over individual keywords |
| RankBrain | 2015 | ML component; finds relevant pages by meaning without exact match |
| Mobile-Friendly | 2015 | Mobile-optimized pages get priority in mobile search |
| Mobile-First Index | 2018 | Mobile version of site used as primary version for indexing |
| BERT | 2019 | Bidirectional context analysis; prepositions and full sentence meaning |
| Core Web Vitals | 2020 | LCP, FID/INP, CLS as ranking signals |

### Google E-E-A-T Framework
Originally E-A-T, expanded to E-E-A-T:
- **Experience** - direct first-hand experience with topic
- **Expertise** - expert-level knowledge of subject
- **Authoritativeness** - authority of author and site in the niche
- **Trustworthiness** - site reliability: quality content, full contacts, payment/delivery info

YMYL sites (Your Money or Your Life - health, finance, legal, safety) face strictest E-E-A-T requirements since Google Medic Update (2018).

## Core Web Vitals

Three technical quality signals (2020+):

| Metric | What It Measures | Bad Threshold |
|--------|-----------------|---------------|
| LCP (Largest Contentful Paint) | Load time of main visible content | >= 4000ms |
| FID/INP (First Input Delay / Interaction to Next Paint) | Interactivity after first input | varies |
| CLS (Cumulative Layout Shift) | Visual stability during page load | >= 0.25 |

**Google's stance**: Content quality takes precedence over page experience. Page experience cannot replace relevant and useful content.

## Key Patterns

### Algorithm Impact Pattern
Most algorithm updates target one of three manipulation vectors:
1. **Content quality** (Panda, Baden-Baden, Fred) - thin, duplicate, or spammy content
2. **Link manipulation** (Penguin, Minusinsk) - purchased or spam link schemes
3. **User deception** (YMYL, behavioral penalties) - misleading content or click manipulation

### Neural Ranking Implications
- Exact keyword matching is less critical; semantic relevance matters more
- Longer, higher-quality content benefits from transformer models that process full text
- YATI (Yandex) and BERT (Google) understand context, prepositions, and sentence meaning
- Anchor text remains important but is processed semantically, not just as string match

## Gotchas
- Google's Mobile-First Index means the mobile version is what gets ranked - desktop-only content may not be indexed
- Core Web Vitals are a tiebreaker, not a primary ranking signal - do not over-invest in perfect scores at the expense of content
- YMYL niches require demonstrated expertise (credentials, citations) - generic content will not rank regardless of optimization
- Yandex and Google have fundamentally different factor priorities (behavioral vs links) - single-engine strategies underperform

## See Also
- [[search-engine-fundamentals]] - Ranking factor groups and priorities
- [[search-engine-filters]] - Specific penalty algorithms and recovery
- [[commercial-ranking-factors]] - E-A-T implementation details
- [[text-optimization]] - How text zones interact with neural ranking
