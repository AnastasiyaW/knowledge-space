---
title: SEO Analytics Tools
category: reference
tags: [seo, analytics, google-analytics, google-search-console, yandex-metrica, yandex-webmaster, rank-tracking]
---

# SEO Analytics Tools

Core analytics platforms for measuring SEO performance. Every SEO specialist needs proficiency in at least Google Search Console + Google Analytics (for Google traffic) and Yandex Webmaster + Yandex Metrica (for Yandex traffic).

## Key Facts

- **Yandex Metrica** = free web analytics tool from Yandex; tracks site visits, user behavior, goals/conversions, heat maps (click maps, scroll maps), and session recordings (Webvisor)
- **Yandex Webmaster** = site monitoring tool; tracks indexation status, search queries, technical errors, incoming links, and site health; equivalent to Google Search Console
- **Google Analytics 4 (GA4)** = Google's web analytics platform; event-based model (replaced Universal Analytics); tracks real-time traffic, user journeys, conversions, audiences
- **Google Search Console (GSC)** = free tool for monitoring site presence in Google Search; shows search queries, impressions, clicks, CTR, average position, indexation status, Core Web Vitals
- **Position tracking tools** = external services (Rush Analytics, SE Ranking, Ahrefs, SEMrush) that monitor keyword rankings daily across search engines and regions
- Key SEO metrics hierarchy: **Positions** (leading indicator) -> **Traffic** (lagging indicator) -> **Leads** (business metric) -> **Sales** (revenue metric)
- See [[search-engine-fundamentals]] for understanding what the metrics mean
- See [[technical-seo-audit]] for using GSC/Webmaster data to diagnose issues

## Patterns

### Google Search Console key reports

```
Performance Report:
- Queries:    What search terms drive impressions and clicks
- Pages:      Which pages get the most organic traffic
- Countries:  Geographic distribution of search traffic
- Devices:    Desktop vs mobile vs tablet split
- Dates:      Trend analysis (compare periods)
- Filters:    Combine dimensions (query + page + country)

Indexing Report:
- Pages indexed vs not indexed
- Reasons for exclusion (noindex, redirected, 404, etc.)
- URL Inspection: check individual URL's index status

Core Web Vitals Report:
- Groups URLs by CWV status (Good / Needs Improvement / Poor)
- Based on CrUX (Chrome User Experience Report) real user data
- 75th percentile threshold (not average)

Links Report:
- Top linked pages (external)
- Top linking sites
- Top linking anchor text
- Internal links distribution
```

### Yandex Metrica key capabilities

```
Standard reports:
- Traffic sources (organic, direct, referral, social, ads)
- Search queries (what Yandex queries brought users)
- Pages (which pages are visited most)
- Geography, devices, demographics

Unique to Yandex Metrica:
- Webvisor:       Session recordings of actual user visits
- Click maps:     Heatmap of where users click on pages
- Scroll maps:    How far users scroll on each page
- Form analytics: Where users abandon forms
- Goals:          Custom conversion tracking (URL, event, JS)

SEO-specific usage:
- Filter by traffic source = "organic" -> Yandex
- Compare organic traffic week-over-week, month-over-month
- Set goals for lead forms to connect SEO to business metrics
```

### GA4 for SEO workflow

```
1. Acquisition > Traffic Acquisition:
   - Filter: Session default channel = "Organic Search"
   - Track organic sessions, engaged sessions, conversions

2. Engagement > Landing Pages:
   - Which pages users land on from organic search
   - Engagement rate, average engagement time per page

3. Explore > Free Form:
   - Create custom exploration: Landing page x Source
   - Filter source = google / yandex
   - Metrics: sessions, conversions, engagement rate

4. Search Console Integration:
   - Link GSC to GA4 for combined query + behavior data
   - Reports > Library > Search Console collection
```

### Position tracking setup

```
1. Select target keywords from semantic core
2. Group by clusters/pages
3. Set tracking parameters:
   - Search engines: Google, Yandex
   - Regions: target city/region
   - Device: desktop + mobile (separate)
   - Frequency: daily for active projects, weekly for monitoring
4. Track competitor domains alongside yours
5. Monitor:
   - Top-3, Top-10, Top-30 visibility percentages
   - Position changes (gains/losses)
   - Competitors entering/leaving top positions
```

## Gotchas

- **GSC data is delayed 2-3 days** - don't expect real-time position data; for same-day checks use incognito search (but that's personalized and imprecise too)
- **GSC shows impressions even without clicks** - a page can have 10,000 impressions at position 50; this doesn't mean it gets traffic, it means it appeared in SERPs
- **Yandex Metrica Webvisor is GDPR-sensitive** - session recordings capture user interactions; ensure your privacy policy covers this if serving EU users
- **GA4 data sampling** kicks in for large datasets in free tier; use BigQuery export for accurate analysis of high-traffic sites
- **Position tracking tools show snapshot positions** - actual user-facing rankings vary by location, device, search history, and time; treat tracked positions as directional indicators
- **Don't confuse average position (GSC) with actual rank** - if you rank #3 for one query variant and #50 for another, average might show #25

## See Also

- [[technical-seo-audit]] - Using analytics data for technical diagnostics
- [[seo-promotion-strategy]] - Using metrics to guide strategy decisions
- [Google Search Console](https://search.google.com/search-console)
- [Google Analytics 4](https://analytics.google.com/)
- [Yandex Metrica](https://metrica.yandex.com/)
- [Yandex Webmaster](https://webmaster.yandex.com/)
- [Ahrefs Rank Tracker](https://ahrefs.com/rank-tracker)
- [SEMrush Position Tracking](https://www.semrush.com/position-tracking/)
