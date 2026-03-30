---
title: Product Metrics & North Star Metric
category: Product Analytics
tags: [metrics, NSM, north-star, vanity-metrics, clarity-metrics, KPI, metrics-hierarchy, HEART]
---

# Product Metrics & North Star Metric

Framework for selecting, organizing, and prioritizing product metrics. Distinguishes vanity from clarity metrics and introduces hierarchical metric decomposition.

## Key Facts

- **Vanity metrics** (metrics of fame): absolute volume numbers - MAU, DAU, installs, registrations. Easy to measure, hard to act on, easy to game
- **Clarity metrics** (efficiency metrics): relative/ratio metrics - CTR, CR, ARPU. Help make decisions, hard to game
- NSM (North Star Metric): single metric reflecting the core value the product delivers to customers
- [[product-metrics-nsm]] localizes causes of changes and prevents shipping changes that harm top-level metrics
- Rule: upper-level metrics must not degrade even if the target metric for a release improved
- HEART framework (Google): Happiness, Engagement, Adoption, Retention, Task success - systematic approach to UX metrics

## NSM Examples

| Product Type | NSM | Rationale |
|-------------|-----|-----------|
| Photo sharing / Media | Daily active users | Content consumption drives ad revenue |
| E-commerce | Orders placed | Direct revenue proxy |
| Facebook | Daily user activity | Engagement drives network value |
| Airbnb | Nights booked | Core value for hosts and guests |

## Patterns

**Metrics hierarchy construction:**

```
NSM (e.g., Revenue)
  |-- Average Check
  |     |-- Items per check
  |     |-- Average item price
  |     |-- Discount volume
  |
  |-- Conversion to first purchase
  |     |-- Landing page -> Click "Buy"
  |     |-- Enter phone -> Enter auth code
  |     |-- Fill order fields -> Click "Pay"
  |     |-- Enter card details -> Payment received
  |
  |-- Repeat purchases
        |-- Push notification funnel
        |-- Feature engagement (search, filters, favorites)
        |-- Behavioral cohort analysis
```

**Metric selection by business model:**

```
Media/Social:
  - Audience: MAU, CAC, session depth, stickiness (time on site)
  - Monetization: ad load (impressions), revenue per user

E-commerce:
  - Money: Revenue, ARPU, ARPPU, Average Margin
  - Loyalty: LTV, Retention, Repeat purchases
  - Funnel: page view -> product view -> add to cart -> checkout -> order -> purchase -> returns

Marketplace:
  - Revenue: commission per op, subscription, lead fees, premium services
```

## Gotchas

- **Symptom**: Feature ships, target metric improves, but revenue drops -> **Cause**: No metrics hierarchy guardrails -> **Fix**: Always check parent metrics before celebrating child metric wins
- **Symptom**: Teams argue over which metric matters -> **Cause**: No agreed NSM -> **Fix**: Pick one NSM that reflects core user value, derive sub-metrics from it
- **Symptom**: MAU is growing but revenue is flat -> **Cause**: Tracking vanity metrics only -> **Fix**: Pair volume metrics with efficiency metrics (ARPU, conversion rates)

## See Also

- [[unit-economics]] - profitability per customer
- [[funnel-analysis]] - step-by-step conversion decomposition
- [[retention-ltv-roi]] - measuring long-term value
- HEART framework: https://library.gv.com/how-to-choose-the-right-ux-metrics-for-your-product-5f46359ab5be
