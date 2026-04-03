---
title: Core Web Vitals and Performance
category: techniques
tags: [seo-marketing, core-web-vitals, lcp, cls, fid, mobile-first, spa, ssr, page-speed]
---

# Core Web Vitals and Performance

Page experience signals including Core Web Vitals metrics, mobile-first indexation, SPA/AJAX rendering solutions, and performance analysis workflow.

## Core Web Vitals Metrics

| Metric | What It Measures | Bad Threshold |
|--------|-----------------|---------------|
| LCP (Largest Contentful Paint) | Render time of largest visible element | >= 4000ms |
| TBT (Total Blocking Time) | JS blocking time | >= 300ms |
| CLS (Cumulative Layout Shift) | Visual stability (ad blocks shifting content) | >= 0.25 |
| FID (First Input Delay) | Interactivity after first interaction | Deprecated in favor of INP |
| INP (Interaction to Next Paint) | Response time after any interaction | Replaced FID |

**Google's stance**: Content quality takes precedence over page experience. Page experience cannot replace relevant and useful content.

## Page Experience Signals
- Core Web Vitals (LCP, FID/INP, CLS)
- Mobile optimization
- HTTPS
- No intrusive interstitials

## Analysis Workflow

### 1. Setup Screaming Frog with PageSpeed API
- Configuration -> API Access -> PageSpeed Insights
- Create service account, get API key, enable PageSpeed Insights API
- Connect in Screaming Frog; choose Mobile or Desktop

### Available Data Categories
- **Overview**: page size, HTML size, CSS size
- **CrUX Metrics**: real user data from Chrome (28-day average)
- **Lighthouse Metrics**: lab data (LCP, TBT, CLS scores)
- **Opportunities**: improvement suggestions per page
- **Diagnostics**: DOM element count, performance details

### 2. Filter Pages Exceeding Thresholds
- LCP >= 4000ms
- TBT >= 300ms
- CLS >= 0.25

### 3. Investigate Specific Issues
Click page -> PageSpeed Details -> Opportunities -> e.g., "Eliminate Rendering-Blocking Resources" -> shows blocking resource URLs.

### 4. Competitive Comparison
- Screaming Frog -> Mode -> List
- Compare: homepage, category page, product card for your site + main competitors
- Export -> comparative analysis
- **Goal: reach niche average, not perfect scores**

## Mobile-First Indexation

- Google indexes mobile version for ranking
- Audit mobile vs desktop content for parity
- All page types must pass mobile optimization tests
- Adaptive markup required for PC, tablets, smartphones
- Desktop-only content not visible on mobile may not be indexed

## SPA/AJAX Sites

### Problem
- SPA (Single Page Application) - rendering happens client-side via JS
- Well-indexed by Google (with issues); poorly indexed by Yandex
- Technologies: Angular, React, Vue, Elm

### Solution: Server-Side Rendering (SSR/Prerendering)
Bot gets static HTML; users get JS version. Yandex confirmed: serving different HTML to bots is NOT a violation if not aimed at deceiving users.

### What Must Be in Rendered HTML
- Standard meta tags
- Graphic content with all meta tags
- Internal and external links with all attributes
- Text content with formatting
- Navigation menus and elements
- Micromarkup (OpenGraph, Schema.org)

### Checking Bot's View
1. Enable User-Agent Switcher with YandexBot/Googlebot
2. Disable JS (Web Developer extension)
3. Open pages, check CTRL+U source for content
4. Check in Yandex Webmaster
5. Check in Google Search Console
6. Check in saved copy (cache)

### Prerender Services
- prerender.io
- getseojs.com
- phantomjs.org
- SEO.js
- HtmlUnit

## Image Optimization

### Naming Requirements
- Standard formats: .jpg, .png
- All images in `/images/` folder
- Filename: transliterated H1 heading (lowercase, hyphen-separated)
- `alt` attribute: same template as filename (in original language)
- `title` attribute: same as alt
- Pre-optimize all images for speed (most common cause of low scores)

## Performance Tools

| Tool | Purpose |
|------|---------|
| PageSpeed Insights | Core Web Vitals metrics per page |
| Google Lighthouse | Lab data + improvement recommendations |
| Screaming Frog + PageSpeed API | Batch CWV analysis for entire site |
| GTmetrix | Alternative speed testing tool |

## Key Principle

**Do not chase perfect PageSpeed scores** - it wastes time and budget. Goal = be at niche average. If competitors score 40-50, you don't need 95.

## Gotchas
- **CWV is a tiebreaker, not a primary ranking signal** - content quality and relevance always win over speed
- **CrUX data requires traffic** - new/low-traffic pages have no real user metrics, only lab data
- **Images are the #1 cause of slow pages** - optimize images before touching CSS/JS
- **Mobile-first means mobile IS the primary index** - features/content only on desktop may be completely ignored
- **SPA sites poorly indexed by Yandex** - SSR/prerendering is mandatory, not optional
- **Content hidden under spoilers/collapsibles gets full weight** - Google confirmed no reduction for mobile-friendly expandable content

## See Also
- [[technical-seo-audit]] - Full audit framework
- [[robots-txt-sitemaps-indexation]] - Indexation and crawl budget
- [[seo-tools-workflow]] - Tool stack for performance analysis
- [[search-engine-mechanics]] - How technical factors fit in ranking
