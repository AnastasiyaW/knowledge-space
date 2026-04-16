---
title: Cohort & Retention Analysis
category: concepts
tags: [bi-analytics, cohort-analysis, retention, ltv, product-analytics]
---

# Cohort & Retention Analysis

Cohort analysis groups users by a shared characteristic at a fixed point in time and tracks their behavior over subsequent periods. It is the primary method for measuring retention, LTV, and the impact of product changes on different user groups.

## Key Facts

- **Cohort** = group of users who performed an action in a defined time window
- **Acquisition cohort**: grouped by install/signup week/month
- **Behavioral cohort**: users who completed a specific action
- Cohort analysis compares target metrics across cohorts over time, accounting for seasonality
- Typical pattern: group by first event date, track metric (retention, revenue) for D1, D7, D14, D30
- Cohort analysis by acquisition source reveals which channels produce highest-LTV users

## Patterns

### Retention Measurement Types

**N-day retention**: % of users from install cohort who return on exactly day N.

**Bracket retention**: % who return in a day range (e.g., day 7-14).

**Return-on retention**: % who used app at least once since install, still active on day N.

### SQL Cohort Retention Query

```sql
WITH cohorts AS (
    SELECT
        user_id,
        DATE_TRUNC('month', first_order_date) as cohort_month
    FROM users
),
activities AS (
    SELECT
        c.user_id,
        c.cohort_month,
        DATE_TRUNC('month', o.order_date) as activity_month,
        DATEDIFF('month', c.cohort_month,
            DATE_TRUNC('month', o.order_date)) as period
    FROM cohorts c
    JOIN orders o ON c.user_id = o.user_id
)
SELECT
    cohort_month,
    period,
    COUNT(DISTINCT user_id) as users
FROM activities
GROUP BY 1, 2
ORDER BY 1, 2;
```

### Cohort Analysis in Tableau

Use `DATEDIFF` to calculate days since first event, `DATETRUNC` to normalize to week/month cohort groups, then pivot with table calculations for the cohort grid.

```sql
-- First event date per user (LOD)
{FIXED [User ID] : MIN([Event Date])}

-- Cohort month
DATETRUNC('month', {FIXED [User ID] : MIN([Event Date])})

-- Period number
DATEDIFF('month',
    {FIXED [User ID] : MIN([Event Date])},
    [Event Date])
```

### Cohort Analysis in AppsFlyer

- Group installs by date
- Track N-day retention, revenue per cohort
- Compare performance across cohorts/sources
- D1/D7/D30 retention shows engagement quality
- D30 ROAS (revenue / ad spend) shows financial return

### User Segmentation Patterns

Create segments based on event history and properties:
- "Users who completed onboarding but not made first purchase in 7 days"
- "Users who used feature X in last 30 days"
- Export segments for push notifications or ad targeting

### Behavioral Analysis (Amplitude Pathfinder)

- Shows actual user navigation paths through the product
- What do users do AFTER event X?
- What did users do BEFORE event Y (drop-off)?
- Discover unexpected usage patterns

## Gotchas

- In AppMetrica, current incomplete month is excluded from retention % calculation - filter by date range and sum installations from completed months only
- Avoid optimizing for installs only - cheap install volume often correlates with low LTV
- Cohort sizes vary naturally; small cohorts produce noisy retention curves that shouldn't be over-interpreted
- When comparing cohorts across time, account for seasonality (holiday cohorts behave differently from regular ones)
- Retention metrics are only valid at day scale in some systems - check data granularity before calculating

## See Also

- [[product-metrics-framework]] - DAU/MAU, stickiness, churn definitions
- [[unit-economics]] - LTV and payback period calculations
- [[funnel-analysis]] - pre-retention funnel optimization
- [[mobile-attribution-fraud]] - cohort quality by acquisition source
- [[sql-for-analytics]] - window functions for cohort queries
