---
title: Cohort Analysis
category: Product Analytics
tags: [cohort, segmentation, comparison, retention, version-comparison, growth-points]
---

# Cohort Analysis

Technique for dividing users into groups (cohorts) by a shared characteristic or action within a time period, then tracking their behavior over time.

## Key Facts

- A cohort is a group of people who performed a specific action in a specific time period
- Primary use: compare behavior across time-based cohorts to find trends, growth points, and regression
- Can substitute A/B testing when comparing product versions (old vs new cohorts)
- Cohorts defined by: install date, first visit, first purchase, first search, registration date
- Cross-section dimensions: gender, geography, income, traffic type, landing page, device type, lead type
- [[retention-ltv-roi]] is typically measured per cohort
- Connected to [[funnel-analysis]] - funnels can be segmented by cohort

## Patterns

**Cohort retention table construction:**

```
             Month 0   Month 1   Month 2   Month 3
Jan cohort   1000      400       200       100
Feb cohort   1200      500       250       -
Mar cohort   800       350       -         -

Retention %:
             Month 0   Month 1   Month 2   Month 3
Jan cohort   100%      40%       20%       10%
Feb cohort   100%      42%       21%       -
Mar cohort   100%      44%       -         -
```

**Version comparison workflow:**

```
1. Take new users who arrived in OLD version -> compute metrics
2. Take new users who arrived in NEW version -> compute metrics
3. Compare metrics between cohorts
4. Segment by dimension to find WHERE improvement happened
5. Watch for novelty effect (initial spike that fades)
```

**Dimensions to analyze:**

```
Time-based segments:        User-attribute segments:
- Install date              - Gender
- First visit date          - Geography
- First purchase date       - Income bracket
- First search date         - Traffic source
                            - Landing page
                            - Lead type

Result metrics:             Time granularity:
- Revenue                   - Day
- Average check             - Week
- Sales count               - Month
- Cost of acquisition
```

## Gotchas

- **Symptom**: New version looks worse than old -> **Cause**: Comparing ALL users, not separating old from new -> **Fix**: Compare only new users in each version (arrivals after release vs before)
- **Symptom**: Conversion spiked right after release then dropped -> **Cause**: Novelty effect - existing users exploring new features -> **Fix**: Wait 2-4 weeks, measure only new-user cohorts
- **Symptom**: Cohort table shows misleading retention -> **Cause**: Mixing cohort definitions (by install vs by first purchase) -> **Fix**: Be explicit about what action defines cohort entry

## See Also

- [[retention-ltv-roi]] - computing LTV and ROI from cohort data
- [[funnel-analysis]] - combining funnels with cohort segmentation
- [[unit-economics]] - profitability calculations per cohort
- Lean Analytics book by Alistair Croll
