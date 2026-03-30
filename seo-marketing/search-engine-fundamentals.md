---
title: Search Engine Fundamentals
category: concepts
tags: [seo, search-engines, ranking-factors, crawling, indexing, serp]
---

# Search Engine Fundamentals

How search engines discover, index, and rank web pages. Core mental model for all SEO work - understanding this determines whether optimization efforts target the right factors.

## Key Facts

- Search engines operate in 3 phases: **crawling** (discovering pages via links and sitemaps), **indexing** (storing page content in the search engine database), **ranking** (ordering results by relevance and quality)
- Google uses 200+ ranking factors grouped into: technical (page speed, mobile-friendliness, HTTPS), content (relevance, E-E-A-T, freshness), authority (backlinks, brand signals), behavioral (CTR, bounce rate, dwell time)
- Yandex ranking differs from Google: text factors carry significantly more weight in Yandex, while Google emphasizes link authority more heavily
- SERP (Search Engine Results Page) contains organic results, paid ads, featured snippets, knowledge panels, People Also Ask, local pack, image/video carousels
- Core Web Vitals (LCP, INP, CLS) are confirmed Google ranking signals since 2021
- E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) is Google's quality framework - not a direct ranking factor but guides quality rater evaluations
- See [[keyword-research-semantic-core]] for how to identify what users search for
- See [[technical-seo-audit]] for ensuring search engines can properly crawl and index your site

## Patterns

### How a page gets ranked (simplified flow)

```
1. Googlebot discovers URL (via sitemap, internal link, or external link)
2. Crawler fetches page HTML, renders JS (if needed)
3. Content is parsed, tokenized, stored in inverted index
4. User enters query -> Google matches query terms against index
5. Ranking algorithm scores each candidate page:
   - Query-document relevance (BM25, BERT, MUM)
   - Page authority (PageRank, link graph)
   - User signals (historical CTR for this query)
   - Technical quality (page speed, mobile UX)
6. SERP assembled with top results + SERP features
```

### Google vs Yandex key differences

| Factor | Google | Yandex |
|--------|--------|--------|
| Link weight | High (PageRank still core) | Lower (Minusinsk filter) |
| Text optimization | Moderate | Very high (text factors dominant) |
| Regional ranking | Less emphasis | Strong regional component |
| Behavioral factors | Moderate | Very high weight |
| Commercial intent | Universal algorithm | Separate commercial ranking |
| AI in ranking | RankBrain, BERT, MUM | MatrixNet, Palekh, YATI |

### SERP features checklist

```
Featured Snippet:    Target with clear Q&A format, lists, tables
Knowledge Panel:     Requires structured data (Schema.org)
People Also Ask:     Mine for content ideas and FAQ sections
Local Pack:          Google Business Profile + local SEO signals
Image Pack:          Image alt text + filename optimization
Video Carousel:      YouTube optimization + video Schema markup
Site Links:          Clear site structure + internal linking
```

## Gotchas

- **Yandex AGS filter**: penalizes sites with low-quality content mass-generated for SEO; demotion is not visible in Webmaster - only through traffic analysis
- **Google Helpful Content Update**: system-wide signal that demotes sites with content written primarily for search engines rather than humans
- **Indexing is not instant** - new pages can take days to weeks to appear in search results; use URL Inspection tool in Google Search Console to request indexing
- **Rankings fluctuate daily** - don't react to single-day position changes; analyze trends over 2-4 week periods minimum
- **Mobile-first indexing** means Google primarily uses the mobile version of your page for indexing and ranking - desktop-only content may not be indexed

## See Also

- [[keyword-research-semantic-core]] - Finding and organizing search queries
- [[on-page-optimization]] - Optimizing individual pages for ranking factors
- [Google Search Central: How Search Works](https://developers.google.com/search/docs/fundamentals/how-search-works)
- [Google Search Quality Rater Guidelines](https://static.googleusercontent.com/media/guidelines.raterhub.com/en//searchqualityevaluatorguidelines.pdf)
- [Yandex Webmaster Help](https://yandex.com/support/webmaster/)
