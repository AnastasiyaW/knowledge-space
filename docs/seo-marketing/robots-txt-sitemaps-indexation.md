---
title: robots.txt, Sitemaps, and Indexation
category: techniques
tags: [seo-marketing, robots-txt, sitemap-xml, indexation, crawl-budget, indexnow, google-indexing-api]
---

# robots.txt, Sitemaps, and Indexation

Detailed coverage of robots.txt configuration, sitemap.xml requirements, indexation analysis, crawl budget optimization, and forced indexation methods.

## robots.txt

### Requirements
- Three separate blocks: Yandex, Google, other search engines
- Don't block folders with CSS and JS files (search engines need to render them)
- Visually verify on adequacy
- Always include sitemap URL

### What to Disallow
```
Disallow: /admin/                    # Admin panel
Disallow: /search/                   # Internal search results
Disallow: /?sort=                    # Sorting parameters
Disallow: /?results_on_page=         # Items per page
Disallow: /print/                    # Print pages
Disallow: /rss/                      # RSS feeds
Disallow: /?utm_                     # UTM parameters
```

### robots.txt vs Other Directives
- **robots.txt** - controls crawling (NOT indexation); saves crawl budget; doesn't remove already-indexed pages
- **Meta robots tag** - controls indexation; use `noindex` to prevent
- **X-Robots-Tag** - HTTP header for non-HTML documents (PDF, etc.)

### Use `clean-param` for GET Parameters
Instead of blocking every parameter variant in robots.txt, Yandex supports `clean-param` directive to collapse URL variants.

## sitemap.xml

### Requirements
- Accessible at `https://site.ru/sitemap.xml`
- Contains only 200 OK pages
- Max 50,000 URLs per sitemap file
- Max 10MB per sitemap file
- Multiple sitemaps -> create index sitemap
- No URLs blocked in robots.txt
- All URLs use main host (no www), https://, trailing slash
- Each URL appears only once
- Generated dynamically (must be current on each request)
- Must have `lastmod` tags with accurate dates
- Submit to Yandex Webmaster and Google Search Console

## Indexation Analysis

### Process
1. Crawl site with Screaming Frog
2. Download excluded/indexed pages from Yandex Webmaster (max 50k)
3. Compare two lists: what's on site vs not in index
4. Analyze reason for every non-indexed page

### Nesting Level Check
1. Crawl with Screaming Frog
2. Sort by nesting level
3. Everything >5 levels deep -> analyze
4. If traffic pages buried deep -> create sitemap or restructure

### Indexation Accessibility Checks
- Check for meta `noindex`, `nofollow`
- Check for canonical tags (pointing elsewhere)
- X-Robots-Tag in HTTP headers
- Pages blocked in robots.txt

### Google Supplemental Index
Low-quality secondary index. Many pages there harms overall ranking.

**Main causes**:
1. Content duplication - most common
2. Incorrect internal linking causing low page weight
3. Too short/spammy text; auto-generated unreadable content

## Crawl Budget Optimization

### Last-Modified / If-Modified-Since Headers
- **Common mistake**: setting modification date to current time on every request
- **Correct**: only update when content actually changes
- **Benefits**: faster page load, reduced server load, modification date in SERP, faster indexation

### Server Log Analysis
Use Screaming Frog Log File Analyser:
- Find redirects encountered by search robots
- Find most/least crawled URLs
- Find uncrawled URLs and orphan pages
- Identify bots to block
- Correlate crawl frequency with page importance

## Forcing Indexation

### Google Indexing API
- Add large volumes of pages without developers
- Can index pages on sites without Search Console access
- Service accounts created once reusable for any site
- Best for large-scale page additions

### Yandex IndexNow
- Notify about new, changed, or deleted pages
- Use IndexNow plugins for common CMS
- In most cases, correct internal linking resolves all Yandex indexation issues

### Other Methods
- Submit URL in Google Search Console URL Inspection
- Submit in Yandex Webmaster
- Ensure pages linked from indexed pages (internal linking fixes most problems)

## Gotchas
- **robots.txt blocks crawling, not indexation** - a page blocked in robots.txt can still appear in search results if other pages link to it
- **Static sitemaps go stale** - always generate dynamically; an outdated sitemap is worse than none
- **lastmod must be accurate** - setting every page to today's date reduces crawl efficiency
- **Previous contractors often leave bad robots.txt rules** - always review manually on project start
- **Supplemental index in Google is a warning sign** - many pages there means site-wide quality issues
- **IndexNow doesn't guarantee indexation** - it only accelerates discovery; quality still determines whether a page gets indexed

## See Also
- [[technical-seo-audit]] - Full audit framework including robots.txt
- [[core-web-vitals-performance]] - Performance affecting crawl budget
- [[site-structure-urls]] - Structure affecting crawl depth
- [[seo-analytics-reporting]] - Monitoring indexation metrics
