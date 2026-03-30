---
title: Retention, LTV & ROI
category: Product Analytics
tags: [retention, LTV, lifetime-value, ROI, CAC, payback-period, profitability]
---

# Retention, LTV & ROI

Core profitability metrics that measure user loyalty, lifetime revenue, and return on acquisition investment.

## Key Facts

- **Retention**: share of users who returned and continued using the product in a given period
- **LTV** (Lifetime Value): total revenue from a customer over their entire relationship with the product
- **CAC** (Customer Acquisition Cost): total cost to convert a prospect into a paying customer
- **ROI** (Return on Investment): `ROI = LTV / CAC` (measured in percent)
- Business becomes profitable when `LTV > CAC`
- All three metrics are best measured per [[cohort-analysis]] cohort
- Connected to [[unit-economics]] as the long-term validation of unit profitability

## Patterns

**Retention calculation from cohort table:**

```
Cohort: January users (1000 people)
Month 0: 1000 (100%)
Month 1: 400  (40%)   <- Retention Month 1
Month 2: 200  (20%)   <- Retention Month 2
Month 3: 100  (10%)   <- Retention Month 3
```

**Cumulative LTV calculation:**

```
               Revenue/user   Cumulative LTV
Month 0        $10            $10
Month 1        $8             $18
Month 2        $5             $23
Month 3        $3             $26
Month 4        $2             $28

CAC = $20
Break-even at Month 2 (LTV $23 > CAC $20)
ROI at Month 4 = $28 / $20 = 140%
```

**Projection with stable retention:**

```
Given:
- Month 2 retention: 80%
- Month 3 retention: 50%
- Month 4 retention: 25%
- Month 5 retention: 20%

Total audience in June = sum of surviving cohorts from each month
Revenue = audience * ARPU per cohort
```

## Gotchas

- **Symptom**: LTV appears to exceed CAC but company is losing money -> **Cause**: LTV calculated on too few months of data, extrapolated optimistically -> **Fix**: Use actual cohort data for at least 3-6 months before projecting
- **Symptom**: ROI looks great on paper but cash flow is negative -> **Cause**: Long payback period - CAC is paid upfront, LTV accumulates over months -> **Fix**: Track payback period (months until cumulative LTV > CAC) separately from total ROI
- **Symptom**: Retention looks flat but revenue is declining -> **Cause**: Users return but spend less each visit -> **Fix**: Track both usage retention AND revenue retention (dollar retention) separately

## See Also

- [[cohort-analysis]] - computing retention per cohort
- [[unit-economics]] - CAC, CPA, and margin calculations
- [[product-metrics-nsm]] - where retention fits in the metrics hierarchy
- [[funnel-analysis]] - understanding which funnel steps drive churn
