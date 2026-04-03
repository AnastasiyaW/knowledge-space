---
title: SEO Tools and Workflow
category: reference
tags: [seo-marketing, tools, screaming-frog, ahrefs, wordpress, tilda, browser-extensions, ai-workflow]
---

# SEO Tools and Workflow

Complete tool stack for SEO work, CMS integration (WordPress, Tilda), browser extensions, AI workflow integration, and standard operating procedures.

## Analytics Platforms

### Yandex Metrika
- Primary traffic analytics for RU-segment
- Key reports: traffic sources, bounce rate, time on site, goal conversions
- Webvisor: session recording for behavioral analysis
- Segment by channel (organic/paid/direct/referral)
- Set up goals for leads, calls, purchases
- Provides Yandex-specific data unavailable elsewhere

### Google Analytics (GA4)
- Essential for Google traffic analysis
- Key metrics: sessions, users, engagement rate, conversions
- Integration with GSC for query-level data
- Audience analysis for content strategy

### Yandex Webmaster
- Crawl and indexing status for Yandex
- Query statistics: impressions, clicks, CTR, average position
- Error reports: 404s, crawl blocks, redirect chains
- Submit sitemap.xml; regional binding
- Turbo pages for mobile

### Google Search Console
- Coverage report: indexed vs excluded pages
- Performance: queries, impressions, clicks, CTR, position
- Core Web Vitals monitoring
- Link reports, manual actions
- URL Inspection for individual page status

## Position Tracking

### Rush Analytics
- RU market position tracking (daily/weekly)
- Group queries by clusters; track visibility by category
- Competitor comparison; schedule auto-reports

### Serpstat
- Multi-functional: tracking + keyword research + competitor analysis
- Domain analytics; backlink analysis; site audit
- Batch analysis of multiple domains

### Alternatives
SE Ranking, TopVisor - position monitoring with frequency customization, white-label reports.

## Keyword Research Tools

### Yandex Wordstat
- Primary search volume source for RU segment
- Broad, phrase, exact match operators
- Region filter; seasonal history
- Browser extension for inline frequency display

### Google Keyword Planner
- Google search volume (often ranges, not precise)
- Keyword ideas; Google-specific demand patterns

### Key Collector (Desktop)
- Mass Wordstat parsing with automation
- Stop-word filtering, deduplication
- Multi-pass frequency collection
- Export to Excel/CSV for semantic core management

### Ahrefs / SEMrush
- International keyword databases
- Competitor traffic estimates
- Backlink analysis (Ahrefs strongest)
- Content gap analysis

## Technical Audit Tools

### Screaming Frog SEO Spider
- Desktop crawler mimicking Googlebot
- Finds: 404s, redirect chains, duplicate titles, missing H1, canonical issues, oversized images
- Export to Excel; free up to 500 URLs, paid unlimited
- PageSpeed API integration for batch CWV analysis
- Custom Search with regex for specific patterns
- **For large sites**: dedicated server install, crawl for days

### PageSpeed Insights / Lighthouse
- Core Web Vitals: LCP, FID/INP, CLS
- Mobile vs desktop scores
- Specific improvement recommendations

## Browser Extensions

| Extension | Purpose |
|-----------|---------|
| SEO Meta in 1 Click | Title, description, H1-H6, canonical, robots for any page |
| Yandex Metrika Helper / Google Tag Assistant | Verify analytics code installation |
| MozBar / Ahrefs Toolbar | Quick DA/PA estimates, backlink counts in SERP |
| Redirect Path | Redirect chains and status codes |
| Web Developer | Disable JS/CSS to see page as robots |
| User-Agent Switcher | Simulate bot crawling |
| WordStatter / WordStat Assistant | Wordstat collection in browser |

## CMS: Tilda

### SEO Setup
- Connect Google Tag Manager first -> deploy Metrika, GA, GSC verification
- Page-level: Settings -> SEO -> Title, Description, Canonical, Noindex toggle
- Site-wide: domain connection, HTTPS, www redirect
- sitemap.xml and robots.txt: auto-generated (use HTTPS checkbox)
- Lazy Load: keep enabled (affects CWV)
- Custom 404 page: create template, assign in settings

### Limitations
- Cannot add arbitrary HTML to `<head>` without workarounds
- JS rendering limitations vs full CMS
- Suitable for SMB, low-to-medium competition
- Works for regional promotion outside major metros

## CMS: WordPress

### Initial Setup
1. Install via hosting panel
2. Install plugins: Yoast SEO (or RankMath), Rus2Lat (transliterate URLs)
3. Permalinks: "Post name" or "Category/Post name"
4. Google Tag Manager in theme header

### Per-Page SEO
- Title: Yoast/RankMath "SEO title" field (distinct from H1)
- Description: "Meta description" field
- URL slug: keyword-based from pre-prepared list
- Canonical and Noindex toggles available

### Architecture
- Pages: evergreen (contacts, about, services)
- Posts: blog articles with categories
- Categories: can serve as landing pages with SEO metadata

## HTML Basics for SEO

### Essential Tags
- `<title>` - page title in search results
- `<meta name="description">` - snippet description
- `<h1>` through `<h6>` - heading hierarchy (one H1 per page)
- `<a href="">` - hyperlinks
- `<img src="" alt="">` - images with alt text
- `<p>`, `<ul>`, `<ol>`, `<li>` - paragraphs and lists

### What to Check in Code
- Title and description present and correct
- Single H1 matching target keyword
- Image alt attributes present
- No accidental `noindex` blocking pages
- Canonical pointing to correct URL
- HTTPS on all pages; www normalization

### CSS/JS Relevance
- CSS: layout shifts (CLS) affect Core Web Vitals
- JS: Yandex renders differently from Google; critical pages should not depend on JS
- Heavy JS delays indexation

## AI Tools in SEO

### ChatGPT / Claude Integration
**Effective prompt structure**: context + goal + constraints.
- Bad: "How to improve SEO"
- Good: "What strategies increase organic traffic for women's clothing e-commerce in competitive regional market?"

**Use cases**:
- Meta tag drafts (title/description variants)
- Content briefs for copywriters
- Competitor analysis summaries
- Technical audit explanations for clients
- FAQ section generation
- Schema.org markup generation
- Anchor list construction from competitor data

English prompts often yield better technical responses. Iterate: first output is draft, refine with follow-ups.

## Standard Workflow

### Project Onboarding Checklist
1. Access: Webmaster, GSC, Metrika, GA4
2. Position tracking: configure queries in Rush Analytics
3. Baseline crawl: Screaming Frog full audit -> document errors
4. Baseline metrics: current traffic, positions, indexation
5. GTM installed and functional

### Monthly Reporting
- Position dynamics: top-10, top-3 counts
- Organic traffic: sessions vs previous month/year
- Conversions from organic
- Technical health changes
- Work performed + next month plan

### Page Optimization Workflow
1. Identify target cluster from semantic core
2. Check competitors in top-10
3. Prepare: H1, URL, title, description, content brief
4. Implement on CMS
5. Submit URL for indexing in GSC/Webmaster
6. Track position

## Tool Selection Summary

| Task | Primary | Alternative |
|------|---------|-------------|
| Traffic analytics | Metrika + GA4 | - |
| Position tracking | Rush Analytics | Serpstat, SE Ranking |
| Keyword research | Wordstat | Key Collector (bulk) |
| Technical crawl | Screaming Frog | Netpeak Spider |
| Backlinks | Ahrefs | Serpstat |
| Page speed | PageSpeed Insights | GTmetrix |
| Quick page check | SEO Meta extension | MozBar |
| Competitor analysis | Serpstat | Keys.so |

## Gotchas
- **Screaming Frog free version limits to 500 URLs** - paid license essential for sites over 500 pages
- **Tilda has SEO ceiling** - suitable for SMB only, not competitive niches
- **WordPress permalinks must be set at launch** - changing later requires redirect management
- **GTM is the universal analytics deployment method** - never inject tracking codes directly into templates
- **AI-generated meta tags need human review** - always verify keyword inclusion and natural language
- **Daily morning check (5-10 min) catches problems early** - make it a non-negotiable habit

## See Also
- [[seo-analytics-reporting]] - KPIs and reporting methodology
- [[technical-seo-audit]] - Audit framework using these tools
- [[keyword-research-semantic-core]] - Tool usage for semantic work
- [[core-web-vitals-performance]] - PageSpeed and Lighthouse details
