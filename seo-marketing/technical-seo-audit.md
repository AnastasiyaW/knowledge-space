---
title: Technical SEO Audit
category: concepts
tags: [seo, technical-audit, indexing, robots-txt, sitemap, canonical, redirect, page-speed]
---

# Technical SEO Audit

Comprehensive technical inspection of a website for errors that prevent or hinder search engine crawling, indexing, and ranking. Should be performed iteratively - at project launch, when indexing problems arise, after major site changes, and as a regular monthly/quarterly check.

## Key Facts

- **Technical SEO audit** = thorough check of the site for technical errors and its compliance with search engine requirements
- Main audit areas: indexation, crawlability, page speed, mobile-friendliness, duplicate content, HTTP status codes, security (HTTPS), structured data
- Triggers for audit: new project launch, indexation problems, traffic drops, site migration, search engine algorithm updates
- **robots.txt** controls which pages crawlers can access; located at `site.com/robots.txt`; blocking important pages here is a common critical mistake
- **XML sitemap** lists all pages that should be indexed; located at `site.com/sitemap.xml`; must be submitted to Google Search Console and Yandex Webmaster
- **Canonical tag** (`rel="canonical"`) tells search engines which version of a duplicate page is the primary one
- **301 redirect** = permanent redirect (passes ~90-99% link equity); **302 redirect** = temporary (does not pass equity reliably)
- Core Web Vitals: **LCP** (Largest Contentful Paint, <2.5s), **INP** (Interaction to Next Paint, <200ms), **CLS** (Cumulative Layout Shift, <0.1)
- See [[site-structure-architecture]] for URL and internal linking issues
- See [[search-engine-fundamentals]] for how crawling and indexing work

## Patterns

### Technical audit checklist

```
INDEXATION:
[ ] robots.txt - not blocking important pages
[ ] XML sitemap - exists, valid, submitted to search consoles
[ ] Meta robots - no accidental noindex on important pages
[ ] Canonical tags - correct self-referencing canonicals
[ ] Index coverage report (GSC) - review errors/excluded pages

CRAWLABILITY:
[ ] Crawl depth - important pages within 3 clicks
[ ] Internal linking - no orphan pages
[ ] Redirect chains - max 1 redirect hop (no chains A->B->C)
[ ] Broken links (404) - fix or redirect
[ ] Crawl budget - block non-essential pages from crawling

PAGE SPEED:
[ ] Core Web Vitals - LCP <2.5s, INP <200ms, CLS <0.1
[ ] Image optimization - WebP/AVIF, lazy loading, proper sizing
[ ] CSS/JS minification and compression (Gzip/Brotli)
[ ] Server response time (TTFB) <200ms

DUPLICATES:
[ ] WWW vs non-WWW redirect (pick one)
[ ] HTTP vs HTTPS redirect (force HTTPS)
[ ] Trailing slash consistency
[ ] Parameter-based duplicates (filters, sort, pagination)
[ ] Thin/duplicate content pages

MOBILE:
[ ] Mobile-friendly test passes
[ ] Viewport meta tag present
[ ] Touch targets adequately sized (48px min)
[ ] No horizontal scrolling

SECURITY:
[ ] HTTPS with valid SSL certificate
[ ] Mixed content warnings resolved
[ ] HSTS header configured
```

### robots.txt template

```
User-agent: *
Disallow: /admin/
Disallow: /cart/
Disallow: /checkout/
Disallow: /search/
Disallow: /*?sort=
Disallow: /*?filter=
Allow: /

Sitemap: https://example.com/sitemap.xml

# Specific directives for Yandex
User-agent: Yandex
Disallow: /tmp/
Host: https://example.com
```

### Common HTTP status codes in SEO

```
200 OK           - Page loads normally (expected)
301 Moved        - Permanent redirect (passes link equity)
302 Found        - Temporary redirect (avoid for SEO)
304 Not Modified - Cached version valid (saves crawl budget)
404 Not Found    - Page doesn't exist (fix or redirect)
410 Gone         - Page permanently removed (faster deindexing)
500 Server Error - Server failure (critical - fix immediately)
503 Unavailable  - Temporary downtime (use during maintenance)
```

### Screaming Frog quick audit

```
1. Crawl full site (set crawler to follow robots.txt rules)
2. Review "Response Codes" tab:
   - Filter 3xx: check redirect chains, 302s that should be 301s
   - Filter 4xx: fix broken internal links
   - Filter 5xx: investigate server errors
3. Review "Page Titles" tab: find missing, duplicate, or too-long titles
4. Review "Meta Description" tab: find missing or duplicate descriptions
5. Review "H1" tab: find missing or multiple H1s
6. Review "Canonicals" tab: find missing or conflicting canonicals
7. Export "Crawl Depth" data: flag pages > 3 levels deep
```

## Gotchas

- **robots.txt Disallow does not remove pages from index** - it only prevents crawling; pages can still be indexed if they have external links; use `noindex` meta tag to remove from index
- **Redirect chains kill link equity** - each hop loses some PageRank; A->B->C->D can lose 30%+ equity; audit and flatten to single-hop redirects
- **Canonical is a hint, not a directive** - Google may ignore your canonical if it disagrees; monitor in GSC under "Page indexing" > "Duplicate, Google chose different canonical"
- **Blocking CSS/JS in robots.txt breaks rendering** - Google needs to render pages to evaluate them; blocking resources prevents proper indexing
- **HTTPS migration without redirects** is catastrophic - every HTTP URL needs a 301 to its HTTPS equivalent; missing redirects = losing all accumulated authority
- **Sitemap ≠ index guarantee** - being in the sitemap does not force indexing; it's a suggestion to crawlers; low-quality pages in sitemap waste crawl budget

## See Also

- [[site-structure-architecture]] - URL structure and internal linking
- [[seo-analytics-tools]] - Tools for monitoring technical health
- [Google Search Console Help](https://support.google.com/webmasters/answer/9012289)
- [Google PageSpeed Insights](https://pagespeed.web.dev/)
- [Screaming Frog SEO Spider](https://www.screamingfrog.co.uk/seo-spider/)
- [Yandex Webmaster](https://webmaster.yandex.com/)
