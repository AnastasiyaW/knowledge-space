---
title: Technical SEO Audit
category: techniques
tags: [seo-marketing, technical-audit, hosting, duplicates, response-codes, crawl-budget, screaming-frog]
---

# Technical SEO Audit

Comprehensive technical audit framework covering prioritization, duplicate pages, server response codes, hosting requirements, content validation, and CMS development requirements.

## Audit Prioritization Framework

### Priority Levels
1. **Errors blocking page indexation** - hosting issues, JS rendering, mirrors/canonicals, page duplicates
2. **Errors blocking correct content indexation** - JS not rendering, markup issues
3. **Errors blocking page ranking** - duplicate tags, broken links, duplicate content, deep nesting, over-optimized content
4. **Other** - lower priority fixes

### Priority Rules
- Focus on tasks affecting maximum number of pages
- Fix incorrect paginated redirects (high priority) over 5 broken links to 404s (low priority)
- Deploy new title template (high priority) over updating HTML sitemap (low priority)
- Understand client budget required for implementation; implement result-producing tasks first

### Priority by Site Size
- **Small sites (<50 pages)**: low priority - errors have minimal impact
- **Medium sites**: medium priority
- **Large sites (50k+ pages)**: critical - one structural error can exclude thousands from index

## Setup and Monitoring

### Proactive Monitoring
1. Top 1000 queries from Metrika -> position tracking
2. Same queries -> Yandex Webmaster Favorites
3. Top 100 traffic pages -> "Important Pages" in Webmaster
4. Configure Webmaster notifications
5. Connect meta-scanner (Rush Analytics) for daily page change detection
6. Don't clog robots.txt; use `clean-param` for GET parameters

### Meta-Scanner
Tracks baseline page changes before they affect traffic:
- Monitors: Title, Description, H1, URL, Meta robots, Canonical, robots.txt, Text content
- Push notification on discrepancy
- Prevents traffic loss from unnoticed developer changes

### Hosting Requirements
- **HTTP/2**: Check at `http2.pro/`; contact hosting to enable
- **SSL/TLS**: Check at `ssllabs.com/ssltest/`; recommend TLS 1.2; configure DNS CAA Policy
- **Load testing**: `loadimpact.com`
- **Stability**: Connect Metrika alerts

## Duplicate Pages

### Types and Solutions

| Duplicate Type | Solution |
|----------------|----------|
| www vs non-www | Choose main mirror, 301 redirect |
| http vs https | 301 redirect to https |
| Trailing slash | Check what ranks, 301 redirect |
| Homepage variants (`/index.html`) | 301 redirect to homepage |
| Case sensitivity (`/Page` vs `/page`) | 301 redirect to lowercase |
| Product sorting params (`?sort=price`) | Close in robots.txt or implement via JS |
| Pagination duplicates | Separate meta templates for page 2+ |
| Product in multiple categories | Canonical tags or redirect |
| Technical subdomains (old., dev.) | Close from indexation or HTTP auth |
| Print pages (`/print/`) | Close in robots.txt |
| UTM parameters | Close in robots.txt with Disallow |

### Finding Duplicates
- Yandex Webmaster (Duplicate pages section)
- Screaming Frog SEO Spider
- Search operators: `site:domain.ru`

## Server Response Codes

### Required Behavior
- **200 OK** - all valid pages
- **301** - permanent redirect (always use for SEO, never 302)
- **404** - broken pages must return actual 404 (not 200)
- **503** - during maintenance (not 403 or 502)
- **500** - not acceptable, fix immediately

### Link Quality
- Zero links to 3xx/4xx pages in full site crawl
- Zero broken links in Screaming Frog crawl

## Basic Merges (Required on Every Project)

All redirect with 301 to canonical URL:
1. `http://` -> `https://` (SSL required)
2. `www.domain.ru` -> `domain.ru` (pick one, 301 the other)
3. `domain.ru/page/` -> `domain.ru/page` (trailing slash normalization)
4. `domain.ru/Page` -> `domain.ru/page` (uppercase normalization)

Check each with Redirect Path browser extension.

## Content Audit Checks

### Hidden Text
1. Disable styles and scripts
2. Check 5-10 pages of each type
3. Hidden relevant text CAN be used but NEVER via `display:none`
4. Mobile-First: content under spoilers/collapsibles does NOT receive weight reduction (Google confirmed)

### Content Quality
- Check 5-10 pages per type for uniqueness (content-watch.ru for batch)
- Spam/auto-generation: look for inconsistent text, keyword stuffing, semantic tag spam
- Generated text must be static

### Markup/Layout Audit
- Disable JS and CSS, verify: content, prices, photos visible
- Styles in .css files (no inline); JS in external files
- Max 20 external CSS/JS files per page
- Default charset: UTF-8

## Anti-Parsing Defense

### Ineffective Methods
- User-Agent restrictions (easily bypassed)
- Country/provider restrictions (loses real traffic)
- CAPTCHA (bypassed, annoys users)

### Effective Methods
1. **Fingerprinting** - multi-parameter client evaluation
2. **Traffic classification** - good bots, bad bots, browsers, suspicious
3. **Rate limiting** - per minute, per session, by duration
4. **ML/Statistical classification** - pattern identification
5. **Behavioral biometrics** - mouse movements, device orientation

### Blocking Fake Bot Scraping
**Reverse DNS validation**:
1. Bot claims GoogleBot/YandexBot -> extract IP
2. Reverse DNS -> get hostname
3. Verify: Google = `googlebot.com`/`google.com`; Yandex = `yandex.ru`/`.net`/`.com`
4. Forward DNS: hostname -> IP
5. IPs don't match -> fake bot -> block

## CMS/Development Requirements

- Title, Description, H1, SEO text: independently editable per page AND via templates
- Alt and Title for images: individually and via fillable templates
- Users and robots see identical content; no hidden text in source
- When JS disabled: links to all pages accessible from homepage
- favicon.ico in site root
- Static resources: gzip compression; caching headers >= 3 days; cache bust via timestamp
- All dev/staging closed from robots via HTTP auth

## Tools

| Tool | Use |
|------|-----|
| Screaming Frog SEO Spider | Full site crawl: 404s, redirect chains, duplicate titles, missing H1, canonical issues |
| Screaming Frog Log File Analyser | Server log analysis: crawled/uncrawled URLs, orphan pages, bot identification |
| Redirect Path (extension) | Check redirect chains for any URL |
| SEO in 1 Click (extension) | View meta tags, H1-H6, canonical for current page |
| Web Developer (extension) | Disable JS/CSS to see page as robots do |
| User-Agent Switcher | Simulate bot to check rendering |
| Link Redirect Trace | Follow redirect chains |

**Infrastructure note**: For crawling large sites (hundreds of thousands of pages), buy a dedicated server, install Screaming Frog, crawl for days.

## Repeat Audit Schedule

| Project Size | Technical Audit | Competitor Visibility Audit |
|--------------|-----------------|---------------------------|
| Small | No repeat needed | Every 3-6 months |
| Medium | Every 3-6 months | Every 3-6 months |
| Large | Monthly | Every 3-6 months |

## Gotchas
- **robots.txt controls crawling, not indexation** - pages blocked in robots.txt can still appear in index if linked from elsewhere
- **302 redirects do NOT transfer ranking signals** - always use 301 for permanent moves
- **Previous contractors often leave bad robots.txt rules** - always review manually before any other work
- **CloudFlare can cause false 403 responses** in audit tools like bertal.ru
- **"Page quality insufficient" in Webmaster** usually means thin content on auto-generated pages, not technical error
- **Developer changes can silently break SEO** - meta-scanner catches problems before traffic drops

## See Also
- [[robots-txt-sitemaps-indexation]] - robots.txt, sitemap.xml, and indexation deep dive
- [[core-web-vitals-performance]] - Page speed and Core Web Vitals
- [[site-structure-urls]] - URL rules and structure validation
- [[seo-analytics-reporting]] - Monitoring and diagnostics workflow
