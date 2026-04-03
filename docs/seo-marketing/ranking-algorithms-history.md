---
title: Ranking Algorithms History
category: concepts
tags: [seo-marketing, algorithms, yandex, google, neural-networks, bert, yati]
---

# Ranking Algorithms History

Timeline of major search engine algorithm updates for both Yandex and Google, including the evolution from heuristic ranking to neural network-based systems.

## Yandex Algorithm Timeline

| Algorithm | Year | Significance |
|-----------|------|-------------|
| Nepot filter | 2005 | Nullified link weight when link deemed commercial/paid |
| Magadan | 2008 | Named algorithm era begins; geo-dependence; text uniqueness recognition |
| ACS filter | 2009 | Sanctions for low-quality auto-generated content |
| Snozhinks | 2009 | Matrixnet ML introduced; keyword-stuffed texts penalized |
| Krasnodor | 2010 | "Spectrum" technology: classifies queries by different intents |
| Baden-Baden | 2017 | Penalty for over-optimized content with excess keyword density |
| YATI | 2020 | Transformer-based text analysis; major NLP improvement |
| Y1 | 2021 | Major update (+2000 improvements); transformer-based YaTI + YaLM |

## Yandex Neural Network Evolution

### Pre-2016: Heuristic Era
Heuristic algorithms, table-based factors, content-only signals.

### 2016-2018: Palekh and Korolev
- Based on Deep Structured Semantic Model (DSSM)
- **Palekh**: compares query against document title
- **Korolev**: extends to full page content comparison; assessor opinions integrated

### 2019: Expert-Assessment Neural Networks
Training targets based on expert quality ratings.

### 2020+: YATI (Yandex Attention to Intent)
- Transformer architecture
- Multiple streams: anchor list, click-based URL index
- Larger text consideration: texts up to 10 sentences processed in full
- Word vector space for semantic understanding

### Yandex Proxima (Quality Metric)
Combines commercial, conversion, expert signals:
- Commercial quality components
- Domain-specific quality (medicine, legal, financial)
- User value signals: Expertise, Authority, Trustworthiness

## Google Algorithm Timeline

| Algorithm | Year | Significance |
|-----------|------|-------------|
| Panda | 2011 | Penalizes thin/duplicate/low-quality content; affected 12% of results |
| Penguin | 2012 | Penalizes spam links, link farms, purchased link schemes |
| Hummingbird | 2012 | Semantic query understanding; context > individual keywords |
| RankBrain | 2015 | ML component; relevant pages by meaning without exact match |
| Mobile-Friendly | 2015 | Mobile-optimized pages get priority in mobile search |
| Mobile-First Index | 2018 | Mobile version used as primary for indexing |
| BERT | 2019 | Bidirectional context analysis; prepositions and full sentence meaning |
| Core Web Vitals | 2020 | LCP, FID/INP, CLS as ranking signals |

## Google E-E-A-T Framework

Originally E-A-T, expanded to E-E-A-T:
- **E (Experience)** - direct first-hand experience with topic
- **E (Expertise)** - expert-level knowledge of subject
- **A (Authoritativeness)** - authority of author and site in the niche
- **T (Trustworthiness)** - site reliability: quality content, full contacts, payment/delivery info

YMYL sites (health, finance, legal, safety) subject to strictest E-E-A-T requirements since 2018.

## Google BERT (2019)

Bidirectional Encoder Representations from Transformers: processes query context including prepositions and full sentence, not just individual keywords. Marks shift from keyword matching to semantic understanding.

## Key Facts
- Yandex uses 2000+ ranking factors
- Google's algorithm updates have increasingly targeted content quality and user intent
- Both engines have converged on transformer-based architectures for semantic understanding
- YMYL niches face strictest quality requirements on both platforms

## Gotchas
- **Algorithm names matter for diagnostics** - when traffic drops, correlating timing with known algorithm rollouts is the fastest way to identify cause
- **YATI changed everything for Yandex** - pre-2020 Yandex text optimization advice is largely outdated
- **E-E-A-T is not a direct ranking factor** - it is a quality framework used by human assessors whose ratings train the algorithms
- **Mobile-First means mobile IS the index** - desktop-only content not visible on mobile version may not be indexed at all

## See Also
- [[search-engine-mechanics]] - Core ranking factor groups
- [[filters-and-penalties]] - Specific penalty algorithms
- [[commercial-ranking-factors]] - E-A-T and commercial factors detail
- [[text-optimization]] - How text relevance scoring works
