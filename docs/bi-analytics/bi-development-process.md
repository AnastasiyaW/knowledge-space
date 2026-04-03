---
title: BI Development Process
category: concepts
tags: [bi-analytics, requirements, dashboard-map, metrics-registry, workflow, stakeholders]
---

# BI Development Process

The BI development process covers the full lifecycle from requirements gathering through stakeholder interviews, dashboard planning with wireframes, data exploration, building, iteration, and publishing. Following a structured process prevents the most common anti-pattern: building the wrong thing.

## Key Facts

- Real-world anti-pattern: "Just build something, we'll figure out details later" -> rework loops and unused dashboards
- Invest 2 days in requirements to save 2 weeks of rework
- Dashboard Map = wireframe + question-answer mapping, done before opening Tableau
- Metrics registry = single source of truth for all metric definitions
- BI analyst competency matrix: 4 levels (theoretical -> can teach others)
- Visualization = information design + graphic design + UX + storytelling + tool proficiency

## Patterns

### BI Development Workflow

1. **Requirements gathering** - interview stakeholders, document questions and KPIs
2. **Dashboard Map** - wireframe the structure before touching Tableau
3. **Data exploration** - understand actual data structure, granularity, quirks
4. **Data preparation** - model joins, create calculated fields (on paper first)
5. **Build MVP** - minimum version, test with stakeholders
6. **Iterate** - refine based on feedback
7. **Publish and document** - publish to server, document data sources and metrics

### Requirements Gathering Interview

**Business questions:**
- What decisions does this dashboard help make?
- How often is it used? (daily, weekly, monthly)
- What actions follow from seeing the data? (investigate, escalate, do nothing)

**Users:**
- Who are the users? (PMs, analysts, executives)
- What is their Tableau/BI skill level?
- Who is in the test group?

**Data questions:**
- What data is available? (DWH tables, CSV files, CRM exports)
- Is data clean or raw? Who prepared it?
- Are there non-additive metrics? (require separate scale field, cannot just SUM)
- Are there special data quirks? (e.g., "All Regions" row in region field needs filtering)

**Timeline:**
- Deadline? MVP or full version?

### Dashboard Map (Structure)

Plan before building. For each element, define:
- **Question** the user is asking ("Which region is underperforming?")
- **Chart type** that answers it best
- **Data fields** needed
- **Filters** that apply

Dashboard structure pattern:
```
Level 1: KPI summary (total state, one number per metric)
Level 2: Trend over time (improving or declining?)
Level 3: Breakdown by dimension (which segment drives the trend?)
Level 4: Detail/drill-down (individual records, anomalies)
```

### Metrics Registry

A single source of truth for all business metric definitions:

| Field | Example |
|-------|---------|
| **Name** | active_sellers |
| **Business definition** | Sellers with at least one listing in the period |
| **SQL/formula** | `COUNT(DISTINCT seller_id) WHERE adverts > 0` |
| **Owner** | Listings team |
| **Data source** | DWH table `listings.sellers` |
| **Granularity** | Daily, with scale field for weekly/monthly |
| **Special notes** | "All Regions" row must be excluded for totals |

Without a registry: different dashboards show different numbers for the same metric because each analyst defined it differently.

### Data Field Dictionary Example

For a listings dashboard:
- `execution_date` - Date
- `region` - Geographic region; note: "All Regions" row exists, filter when showing totals
- `scale` - Data granularity (day/week/month); non-additive, must filter by scale, not sum
- `listers` - Active sellers (those with at least one listing)
- `retention_7_days` - % still active 7 days after first listing (only valid at day scale)
- `retention_28_days` - % still active 28 days (only valid at day scale)

### Stakeholder Communication

**Anti-pattern**: building in isolation, surprising stakeholders with "finished" work.

**Better approach:**
- Show wireframe before building
- Show draft at 50% completion
- Weekly check-ins on large projects

**Handling "just build something" requests:**
"If I build without understanding requirements, we'll likely rebuild it. 2 days in requirements = saves 2 weeks of rework."

**Handling urgent timeline pressure:**
Agree on MVP scope: minimum viable dashboard that delivers value in available time.

### BI Analyst Competency Assessment

5 visualization components: information design, graphic design, UX, storytelling, tool proficiency.

4-level competency scale:
1. Theoretical knowledge only
2. Can do with documentation/lookup
3. Knows nuances, has own examples
4. Can teach others

Self-assess against desired level to identify gaps.

## Gotchas

- Non-additive metrics (e.g., metrics stored with a "scale" field for day/week/month) cannot be summed - must filter by scale
- Retention metrics may only be valid at day scale - check granularity before calculating
- "All Regions" or similar aggregate rows in source data must be filtered out when showing totals, or you get double-counting
- Peak load on BI servers is non-linear and unpredictable - one heavy report can consume 75% of server CPU
- Current incomplete periods should be excluded or marked clearly to avoid misleading comparisons

## See Also

- [[dashboard-design-patterns]] - visual design after requirements are set
- [[product-analytics-fundamentals]] - metrics pyramid and KPI selection
- [[tableau-fundamentals]] - building in Tableau
- [[powerbi-fundamentals]] - building in Power BI
- [[bi-tools-comparison]] - choosing the right BI tool
