---
title: SEO Analytics and Reporting
category: techniques
tags: [seo-marketing, analytics, kpis, reporting, position-tracking, traffic-analysis, monitoring]
---

# SEO Analytics and Reporting

Project control system: KPI metrics, monthly reporting structure, meta-scanner monitoring, hypothesis building for traffic drops, and task management.

## Project Setup

### With Existing History
1. Get access to: Yandex Metrika, Yandex Webmaster, Google Analytics, Google Search Console
2. Extract queries with traffic from Webmaster and Metrika
3. Add to position tracking (Rush Analytics or similar)

### New Project
1. Add to: Metrika, Webmaster, GA, GSC
2. Collect or generate initial query list manually
3. Add to position tracking

## Daily Monitoring Routine

Every morning (5-10 minutes):
1. Open Yandex Metrika
2. Open Yandex Webmaster
3. Open Google Search Console
4. Check that all is OK

## Core KPI Metrics

### 1. Traffic + Segments
- Total organic traffic
- By search engine (Yandex, Google)
- By type (brand vs non-brand)
- By region (city-level)
- By conversion rates per segment

### 2. Indexation + Segments
**Process**: Crawl site -> segment by page type -> check indexation in Rush Analytics -> identify anomalies.

Track by page type: categories, tags, brands, pagination, product cards.

**Note**: Google index is usually ~30% larger than Yandex.

### 3. Links + Segments
Track: total donor domains and pages, priority page metrics, competitor metrics, dynamics of changes.

### 4. Visibility
**Definition**: estimated % of traffic achievable given semantic core frequencies and current positions.

**Setup**: segment queries into projects, group segments, load into tracker, track competitor dynamics.

**Schedule**: all competitors every 3-6 months; deep audit of growing competitors every 6 months.

### 5. Positions + Segments
% of queries in TOP-3, TOP-5, TOP-10 per search engine. Less useful than visibility but helps spot patterns.

## Meta-Scanner (Page Change Monitoring)

**Purpose**: catch page changes before they affect traffic.

**Workflow**:
1. Load current data as reference baseline
2. Service checks at intervals
3. Discrepancy -> push notification
4. Fix before traffic impact

**What to monitor**: Title, Description, H1, URL, Meta robots, Canonical, robots.txt, Text content.

**Value**: developer uploads broken robots.txt -> next day push notification -> fixed immediately -> traffic never dropped.

## Monthly Report Structure

Build one master report per month:

1. **Position dynamics**: top-10, top-3 counts, visibility trend
2. **Organic traffic**: sessions vs previous month and YoY
3. **Goal conversions**: leads, purchases from organic
4. **Technical health**: new crawl errors, indexation changes
5. **Work performed**: list all implemented changes
6. **Next month plan**

Keep reports concise: 1-2 page summary with charts more effective than 10-page document.

## Hypothesis Building for Traffic Drops

### Segmented Analysis Approach

**Sharp drop example**:
1. Traffic dropped
2. Segment by page type
3. Brand pages dropped specifically
4. Investigate brand pages
5. Title template broke on brand pages
6. Fix with development team

**Gradual decline example**:
1. Traffic gradually declining
2. Check main metrics
3. Indexation declining
4. Segment indexation
5. Tag pages losing indexation
6. Developer accidentally closed them via meta robots
7. Fix

### Position Drop Diagnosis
1. **Do not panic** (first rule)
2. Identify nature:
   - **Mass drop** (all pages) -> technical problem (robots.txt, sitemap, server)
   - **Segmented drop** (specific type) -> text or technical issue for that template
   - **Point drop** (single page) -> text or link issue for that page

## Task Management

**First months** (many briefs/tasks):
- Identify 3-5 priority tasks
- Constantly check status
- Plan monthly, check plan vs actual at month end
- Track stalled tasks

## Repeat Audit Schedule

| Project Size | Technical Audit | Competitor Visibility |
|--------------|-----------------|----------------------|
| Small | No repeat | Every 3-6 months |
| Medium | Every 3-6 months | Every 3-6 months |
| Large | Monthly | Every 3-6 months |

## Analytics Tools

| Metric | Primary Tool | Alternative |
|--------|-------------|-------------|
| Traffic | Yandex Metrika + GA4 | - |
| Positions | Rush Analytics | Serpstat, SE Ranking |
| Indexation | Yandex Webmaster + GSC | - |
| Leads/sales | CRM (AmoCRM, TildaCRM) | Google Sheets |
| Multi-channel | Roistat, Utmstat | - |

### Rush Analytics Position Tracking Setup
1. Create project: name + full domain URL
2. Add target engine + region (e.g., Yandex/Russia/Moscow)
3. Add Google with same region
4. Add both desktop and mobile (separate SERP)
5. Set daily tracking (recommended)
6. Import keyword list (minimum 20-50 queries)
7. Run first check; configure recurring checks

## Summary: Control System

**Setup at start**: connect all tools, configure meta-scanner, add queries to tracking, segment queries.

**Monthly**: traffic + indexation + links + visibility + positions (all segmented).

**Operational**: 3-5 priority tasks, track stalled tasks, daily morning check.

**Periodic**: technical audit per schedule, competitor visibility every 3-6 months.

## Gotchas
- **Don't panic on traffic drops** - segment first, diagnose second, act third
- **Google index is ~30% larger than Yandex** - this is normal, not an error
- **Positions are less useful than visibility** - positions fluctuate daily, visibility shows trends
- **Meta-scanner pays for itself on first catch** - developer errors caught in 1 day vs 2-3 weeks
- **Brand vs non-brand traffic distinction is critical** - brand traffic growth may mask non-brand decline
- **Monthly reports should be concise** - clients read 2-page summaries, not 10-page documents

## See Also
- [[seo-tools-workflow]] - Tool configuration and setup
- [[technical-seo-audit]] - Audit methodology
- [[seo-strategy-by-site-type]] - Strategy drives KPI selection
- [[behavioral-factors-ctr]] - Behavioral metrics in analytics
