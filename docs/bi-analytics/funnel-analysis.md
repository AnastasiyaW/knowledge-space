---
title: Funnel Analysis
category: concepts
tags: [bi-analytics, product-analytics, funnel, conversion, optimization]
---

# Funnel Analysis

Funnel analysis visualizes and measures user progression through a multi-step flow toward a conversion goal. Each step represents a user action, and the analysis focuses on drop-off rates between steps to identify optimization opportunities.

## Key Facts

- Funnel = sequence of user steps toward conversion goal
- Key metrics: step conversion (N to N+1), overall conversion, drop-off points, time between steps
- Typical e-commerce funnel: Visitor -> Product Page -> Add to Cart -> Checkout Start -> Payment -> Order Complete
- Typical mobile app funnel: app_open -> registration_start -> registration_complete -> onboarding_complete -> first_purchase
- Funnel optimization targets the biggest drop-off step first
- Time window matters: only count funnel completion if done within N days/hours

## Patterns

### Funnel Optimization Process

1. Identify biggest drop-off step
2. Hypothesize cause (confusing UX, too many steps, unclear value)
3. Test improvement (A/B or sequential)
4. Measure change in conversion

### Critical User Path (Event Map)

The minimum sequence of events defining the core user journey:
1. `app_open` - app launched
2. `registration_start` - registration flow opened
3. `registration_complete` - account created
4. `onboarding_complete` - tutorial finished
5. `first_purchase` - first payment

### Event Prioritization

1. Business KPI events (purchase, subscription, activation)
2. Funnel step events (key screens, key actions)
3. Error/crash events (identify issues)
4. Engagement events (feature usage depth)

### Funnel Analysis in Amplitude

- Define sequence of events: `sign_up` -> `onboarding_complete` -> `first_purchase`
- Shows drop-off at each step
- Segment by property: compare conversion for iOS vs Android
- Time window: only count funnel if completed within N days/hours

### SQL Funnel Pattern

```sql
SELECT
    COUNT(CASE WHEN event = 'page_view' THEN user_id END) as step1_views,
    COUNT(CASE WHEN event = 'add_to_cart' THEN user_id END) as step2_cart,
    COUNT(CASE WHEN event = 'checkout_start' THEN user_id END) as step3_checkout,
    COUNT(CASE WHEN event = 'purchase' THEN user_id END) as step4_purchase
FROM events
WHERE event_date = CURRENT_DATE;
```

### Install Conversion Rate (App Stores)

**Conversion rate** = installs / product page views. Benchmark: 25-35% for well-optimized apps.

Elements affecting conversion:
- **Icon** - first visual impression, recognizable at small size
- **Screenshots** - first 2-3 visible without scrolling (most important)
- **Preview video** - auto-plays on iOS, show core value in first 3 seconds
- **App name + subtitle** - conveys value proposition instantly
- **Ratings** - apps below 4.0 have significantly lower conversion
- **Reviews** - recent positive reviews matter more than old ones

## Gotchas

- Funnel analysis without time windowing can be misleading - a user who starts today and purchases 90 days later is different from one who completes in 10 minutes
- Counting events vs counting unique users gives very different funnel shapes
- Non-linear funnels (users skip steps, go back) require session-based analysis, not simple step counting
- Segmenting funnels by acquisition source often reveals that aggregate numbers hide dramatically different behavior patterns

## See Also

- [[product-analytics-fundamentals]] - metrics pyramid and analyst role
- [[cohort-retention-analysis]] - post-funnel retention tracking
- [[web-marketing-analytics]] - web funnel setup with GA/GTM
- [[mobile-analytics-platforms]] - funnel tools in Firebase, Amplitude
- [[app-store-optimization]] - app store conversion funnels
