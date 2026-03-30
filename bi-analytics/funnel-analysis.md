---
title: Funnel Analysis
category: Product Analytics
tags: [funnel, conversion, sales-funnel, user-journey, drop-off, optimization]
---

# Funnel Analysis

Sequential analysis of user steps toward a goal action, measuring conversion between each step to identify drop-off points.

## Key Facts

- A funnel defines a sequence of steps and a time window
- Users are tracked from step 1; only users who completed step 1 enter the funnel
- Between steps, users may perform other actions (non-linear path is normal)
- Different analytics systems compute funnels differently - verify methodology
- The funnel does not need to go all the way to the final transaction if downstream events are costly to measure
- Segment funnels by [[cohort-analysis]] dimensions to find where optimization helps most
- Connected to [[product-metrics-nsm]] via the metrics hierarchy

## Patterns

**E-commerce funnel example:**

```
Site visitors        100,000  (100%)
  -> Product views    50,000  (50%)
  -> Add to cart      10,000  (10%)
  -> Checkout start    5,000  (5%)
  -> Order placed      3,000  (3%)
  -> Payment received  2,500  (2.5%)
  -> Not returned      2,300  (2.3%)
```

**Funnel traversal logic:**

```
Given funnel: A -> B -> C

User sequences:
(1) A -> B -> C        PASSES (sequential match)
(2) A -> A -> C        FAILS  (skipped B)
(3) B -> C             FAILS  (no A at start)
(4) A -> C -> B -> D   PASSES (B after A, C after B - order matters, gaps OK)
(5) A -> C -> A -> C   FAILS  (B never occurs after A)
(6) D -> A -> D -> B -> C -> A  PASSES (subsequence A...B...C exists)
```

**Segmentation for funnel analysis:**

```
Useful cross-sections:
- By traffic source (organic, paid, social, direct)
- By geography / region
- By device type (desktop, mobile, tablet)
- By user type (new vs returning)
- By time period (day, week, month cohorts)
- By landing page

Analysis approach:
1. Build funnel, examine in various segments
2. Find segments with high/low performance
3. Study users who convert: what actions do they take?
4. Study users who drop off: at which step and why?
5. Form hypotheses, run A/B tests
```

## Gotchas

- **Symptom**: Funnel shows 0% conversion at a step -> **Cause**: Step event name changed after a deploy -> **Fix**: Verify event tracking is firing correctly before analyzing
- **Symptom**: Conversion improved after redesign, but revenue did not change -> **Cause**: Users who previously dropped off were low-intent; new flow just adds noise -> **Fix**: Measure downstream metrics (revenue, LTV), not just funnel step conversion
- **Symptom**: Different tools show different funnel numbers -> **Cause**: Different attribution windows, session definitions, or step ordering logic -> **Fix**: Document funnel calculation methodology (strict sequence vs any-order, time window, deduplication)

## See Also

- [[cohort-analysis]] - segmenting funnels by cohort
- [[product-metrics-nsm]] - placing funnel steps in the metrics hierarchy
- [[unit-economics]] - connecting funnel conversion to profitability
- [[dashboard-design-patterns]] - funnel visualization in dashboards
