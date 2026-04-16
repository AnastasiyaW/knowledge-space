---
title: Product Metrics Framework
category: concepts
tags: [bi-analytics, product-analytics, metrics, dau, mau, retention, stickiness]
---

# Product Metrics Framework

Core product metrics that measure user engagement, retention, and product health. These metrics form the foundation for product analytics across mobile apps, web products, and SaaS platforms.

## Key Facts

- **DAU** (Daily Active Users) - unique users active in a day
- **WAU** (Weekly Active Users) - unique users active in 7 days
- **MAU** (Monthly Active Users) - unique users active in 30 days
- **Stickiness** = DAU/MAU - measures how habit-forming the product is
- **Retention rate** - % of users who return after first use on day N
- **Churn rate** = 1 - Retention - % of users who stop using the product
- "Active" must be explicitly defined per product (a login? a transaction? a feature use?)

## Patterns

### Stickiness Benchmarks (DAU/MAU)

```toml
Stickiness = DAU / MAU
```

| Range | Interpretation | Examples |
|-------|---------------|----------|
| 50%+ | Daily use habit | Social media, email |
| 25-50% | Several times per week | Productivity apps |
| 10-25% | Weekly use | Fitness, finance apps |
| <10% | Infrequent use | Travel booking, real estate |

Stickiness is contextual - don't compare messenger stickiness to hotel booking app.

### Retention Types

**N-day retention**: % of users from install cohort who return on exactly day N.

**Bracket retention**: % who return in a day range (e.g., day 7-14).

**Return-on retention**: % who used app at least once since install, still active on day N.

How to read retention curves:
- Curve flattening = product has core value (users who stay, stay long-term)
- Curve dropping to 0 = no product-market fit, everyone churns
- Higher D1 vs D7 vs D30 = earlier engagement is key

### User Lifecycle Stages

1. **Impression** - user sees ad
2. **Click** - user clicks ad
3. **Install** - app downloaded and installed
4. **First open** (registration/onboarding)
5. **Key event** - target action (first purchase, activation)
6. **Retention** - returning usage
7. **Monetization** - purchase/subscription
8. **Churn** - stop using app

### DAU/MAU Stickiness SQL Pattern

```sql
SELECT
    event_date,
    COUNT(DISTINCT user_id) as dau,
    COUNT(DISTINCT user_id) OVER (
        ORDER BY event_date
        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) as mau_rolling,
    ROUND(100.0 * COUNT(DISTINCT user_id) /
        COUNT(DISTINCT user_id) OVER (
            ORDER BY event_date
            ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
        ), 1) as stickiness
FROM events
GROUP BY event_date;
```

### Alert Strategy

Set automated alerts for:
- Sharp drops in DAU (>15% vs rolling average)
- Funnel conversion below threshold
- Revenue per user below target

## Gotchas

- DAU/MAU can be misleading if "active" is defined too loosely (e.g., counting passive pageviews)
- Retention benchmarks differ dramatically by product category - always compare within your vertical
- Stickiness can be artificially inflated by push notifications that generate opens without real engagement
- Churn rate = 1 - Retention is only valid when both use the same time window and "active" definition

## See Also

- [[product-analytics-fundamentals]] - analyst role and metrics pyramid
- [[cohort-retention-analysis]] - cohort-based retention analysis
- [[unit-economics]] - LTV and customer profitability
- [[mobile-analytics-platforms]] - tools for measuring these metrics
