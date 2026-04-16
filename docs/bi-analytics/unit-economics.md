---
title: Unit Economics
category: concepts
tags: [bi-analytics, unit-economics, ltv, cpa, arpu, business-metrics]
---

# Unit Economics

Unit economics is an economic modeling method for determining business profitability by evaluating profitability per unit of goods or per single customer. It applies when launching startups, planning to scale, pitching to investors, or when user acquisition and advertising are the main cost drivers.

## Key Facts

- Core formula: `Profit = Revenue - Variable Costs - Fixed Costs`
- Business is viable when Gross Profit > Fixed Costs
- **Gross Profit is King** - the primary metric for unit economics
- Higher cost-per-lead doesn't mean worse economics - lead quality (conversion to deal) matters more than quantity
- Contribution margin (Revenue minus variable costs per unit) must be positive before scaling

## Core Formulas

```yaml
Profit (Margin) = Gross Profit - Fixed Costs
Gross Profit = Revenue - Variable Costs

Main Unit Economics Formula:
User Acquisition x (ARPU - CPA) = Gross Profit

Where:
ARPU = C1 x APC x AvP x Margin

Expanded:
User Acquisition x (C1 x APC x AvP x Margin - CPA) = Gross Profit

Payback Period = CPA / (Monthly ARPU x Margin)
```

## Patterns

### Key Metrics

| Metric | Definition |
|--------|-----------|
| **CPA/CAC** | Cost Per Acquisition / Customer Acquisition Cost |
| **ARPU** | Average Revenue Per User |
| **GMV** | Gross Merchandise Value - total volume before expenses |
| **LTV** | Lifetime Value - total revenue from customer over lifetime |
| **ROMI** | Return on Marketing Investment |
| **C1** | Conversion to first purchase (% of users) |
| **APC** | Average Payment Count (repeat purchases) |
| **AvP** | Average Price per transaction |
| **COGS** | Cost of Goods Sold - direct cost per transaction |
| **ROAS** | Return On Ad Spend = Revenue / Ad Spend |
| **ROI** | Return on Investment = (Revenue - Cost) / Cost |

### Marketing Cost Metrics

| Metric | Formula |
|--------|---------|
| **CPI** | Cost Per Install = Ad Spend / Installs |
| **CPC** | Cost Per Click = Ad Spend / Clicks |
| **CPM** | Cost Per Mille = Cost per 1,000 impressions |
| **CTR** | Click-Through Rate = Clicks / Impressions |
| **CVR** | Conversion Rate = Actions / Clicks |

### Growth Levers (Goldratt Theory of Constraints)

1. Find the parameter whose change gives the greatest contribution to Gross Profit
2. Subordinate the product to this parameter (focus on it)
3. Expand/scale it

Possible decisions based on metrics:
- Attract more users (increase User Acquisition)
- Reduce acquisition cost (reduce CPA)
- Increase conversion to purchase (increase C1)
- Increase average order value (increase AvP)
- Increase repeat purchase count (increase APC)
- Increase GMV

### RFM Segmentation (DAX Example)

RFM = Recency, Frequency, Monetary - customer segmentation model:

```dax
Recency = DATEDIFF(MAX(Orders[OrderDate]), TODAY(), DAY)
Frequency = COUNT(Orders[OrderID])
Monetary = SUM(Orders[Revenue])
```

Rank customers 1-5 on each dimension, combine into RFM score for targeting.

## Gotchas

- A cheap acquisition channel with low-quality users is worse than an expensive channel with high-LTV users - always analyze cohort behavior by acquisition source
- ARPU averaged across all users can mask bimodal distributions (whales vs free users)
- Payback period is critical for subscription models - if payback > average user lifetime, the model doesn't work
- Unit economics calculated at launch may not hold at scale due to market saturation and rising acquisition costs

## See Also

- [[product-metrics-framework]] - DAU/MAU and engagement metrics
- [[cohort-retention-analysis]] - cohort-based LTV analysis
- [[mobile-attribution-fraud]] - attribution and ROAS measurement
- [[web-marketing-analytics]] - traffic source analysis and ROI
