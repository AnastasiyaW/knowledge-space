---
title: BI Systems and Dashboards
category: practices
tags: [data-science, bi, dashboards, analytics, tableau, superset]
---

# BI Systems and Dashboards

Business Intelligence transforms data into actionable decisions. A BI system is a product - not a one-time project. Covers dashboard design, tool selection, and the analytics infrastructure pipeline.

## Dashboard Types

| Type | Purpose | Design Pattern |
|------|---------|----------------|
| Alerts/Mailings | Early warning | Simple good/bad indicators |
| Overview/Hub | Current state at a glance | KPI + sparkline + top lists |
| Entity Page | Deep dive into one entity | Sections matching lifecycle |
| Analytical | Complex hypothesis testing | Large main chart + supporting context |
| Self-Service | User-driven exploration | Filters on left, results on right |

## Key Metrics and KPIs

### Product Metrics
- **DAU/MAU**: daily/monthly active users
- **Retention rate**: % returning after N days (D1, D7, D30)
- **Churn rate**: 1 - retention
- **ARPU**: revenue / active users
- **LTV**: predicted total revenue from a user
- **CAC**: marketing spend / new customers
- **LTV/CAC > 3** for healthy business

### Conversion Funnel
```sql
SELECT
    COUNT(DISTINCT CASE WHEN event = 'page_view' THEN user_id END) as views,
    COUNT(DISTINCT CASE WHEN event = 'add_to_cart' THEN user_id END) as carts,
    COUNT(DISTINCT CASE WHEN event = 'purchase' THEN user_id END) as purchases
FROM events WHERE date BETWEEN '2024-01-01' AND '2024-01-31';
```

### Cohort Analysis
Group users by signup date, track metric over time per cohort.

```sql
WITH cohorts AS (
    SELECT user_id,
        DATE_TRUNC('month', first_visit) as cohort_month,
        DATE_TRUNC('month', visit_date) as activity_month
    FROM user_visits
)
SELECT cohort_month, activity_month,
    COUNT(DISTINCT user_id) as active_users
FROM cohorts GROUP BY 1, 2;
```

## SQL for Analytics

```sql
-- Running total
SELECT date, revenue,
    SUM(revenue) OVER (ORDER BY date) as running_total
FROM daily_revenue;

-- Rolling 7-day average
SELECT date, revenue,
    AVG(revenue) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
    as rolling_7d_avg
FROM daily_revenue;

-- Month-over-month growth
SELECT month,
    revenue,
    LAG(revenue) OVER (ORDER BY month) as prev_month,
    (revenue - LAG(revenue) OVER (ORDER BY month))
    / LAG(revenue) OVER (ORDER BY month) * 100 as growth_pct
FROM monthly_revenue;
```

## Dashboard Design Process

### Canvas Framework
1. **Users & Context**: who, when, how they use it
2. **Task Understanding**: what decisions they make
3. **Questions**: what specific questions the dashboard answers
4. **Visualization**: which chart types match which questions

### Wireframe Principles
- Block size reflects information importance
- Attract attention via: position (top-left), contrast (size, color), unusual shape
- Alerts: evenly distributed elements with deviation highlighting
- Analytical tools: large analysis chart + small trend charts

## BI Tools

| Tool | Type | Strength |
|------|------|----------|
| **Tableau** | Commercial | Industry standard, drag-and-drop |
| **Apache Superset** | Open source | SQL-based, rich charts |
| **Metabase** | Open source | Simple "question" paradigm |
| **Redash** | Open source | SQL-first, for data teams |
| **DataLens** | Free (Yandex) | ClickHouse native |
| **Looker Studio** | Free (Google) | BigQuery/GA integration |

**Key difference** from matplotlib/seaborn: BI tools are for presenting to non-technical stakeholders. Python plotting is for analysis.

## Data Pipeline for Dashboards

Source (OLTP) -> ETL/ELT -> Data Warehouse (OLAP) -> Semantic Layer -> BI Tool -> Users

### DWH Architecture
1. **Staging** (raw): load from sources in original quality
2. **Core**: consolidation, normalization, business rules
3. **Presentation** (data marts): star schemas, business-ready aggregates

## Gotchas
- Dashboard without defined KPIs has no purpose - start with business goals
- Chaotic report creation leads to unmanageable sprawl - systematize content
- BI is NOT a one-time project - treat it as a product with iterations
- Small user count in a segment makes statistics unreliable - always show N

## See Also
- [[data-visualization]] - Python plotting for analysis
- [[hypothesis-testing]] - A/B testing on dashboard metrics
- [[ds-workflow]] - dashboards in project lifecycle
- [[sql-fundamentals]] - SQL for analytics queries
