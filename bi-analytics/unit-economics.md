---
title: Unit Economics
category: Product Analytics
tags: [unit-economics, CPA, ARPU, LTV, CAC, gross-profit, metrics, business-model]
---

# Unit Economics

Method for evaluating business model profitability by analyzing revenue and costs per single unit (product or customer).

## Key Facts

- Core formula: `User Acquisition * (ARPU - CPA) = Gross Profit`
- Expanded: `UA * (C1 * APC * AvP * Margin - CPA) = Gross Profit`
- A business is viable only when individual unit is profitable
- Uses [[product-metrics-nsm]] to decompose and find growth levers
- Goldratts Theory of Constraints: find the parameter with the highest marginal impact on Gross Profit, then focus all effort on expanding it
- Connected to [[cohort-analysis]] for tracking per-cohort profitability over time

## Core Metrics

| Metric | Full Name | Description |
|--------|-----------|-------------|
| CPA | Cost Per Acquisition | Cost to acquire one user |
| CAC | Customer Acquisition Cost | Total cost to convert a prospect into a buyer |
| ARPU | Average Revenue Per User | Average revenue from an acquired user |
| C1 | Conversion to first purchase | Share of users who make first purchase |
| APC | Average Payment Count | Number of repeat purchases |
| AvP | Average Price | Average order value |
| COGS | Cost of Goods Sold | Direct costs per unit |
| GMV | Gross Merchandise Value | Total sales volume before deductions |
| ROMI | Return on Marketing Investment | Revenue returned per marketing dollar |

## Patterns

**Decision framework based on unit economics:**

```
Growth levers (pick one to focus on):
1. Attract more users (increase UA)
2. Reduce acquisition cost (lower CPA/CAC)
3. Increase conversion to purchase (raise C1)
4. Increase average order value (raise AvP)
5. Increase repeat purchases (raise APC)
6. Increase GMV
```

**Business model identification by revenue type:**

| Business Type | Primary "Unit" | Key Metrics |
|---------------|---------------|-------------|
| Media / Social | Audience | MAU, CAC, depth of view, stickiness, ad revenue per user |
| E-commerce | Purchase | Revenue, ARPU, ARPPU, Margin, LTV, Retention |
| Marketplace | Lead / Transaction | Commission, lead cost, conversion lead-to-deal |
| Subscription | Subscriber | MRR, churn rate, LTV, CAC payback period |

## Gotchas

- **Symptom**: High conversion rate but low profitability -> **Cause**: Looking at vanity metrics (conversion) without cost context -> **Fix**: Always pair conversion with CPA and margin per conversion
- **Symptom**: Marketplace seems unprofitable by lead volume -> **Cause**: Comparing sites by lead count ignoring lead quality (conversion to deal) -> **Fix**: Compare end-to-end: cost per deal, not cost per lead
- **Symptom**: Funnel stops at "phone view" step -> **Cause**: Downstream events (calls, deals) are expensive to measure -> **Fix**: Accept partial funnel, estimate with sampling or CRM data

## See Also

- [[funnel-analysis]] - breaking down conversion steps
- [[retention-ltv-roi]] - long-term profitability per cohort
- [[product-metrics-nsm]] - choosing the right North Star Metric
- https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields.htm
