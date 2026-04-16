---
title: Tableau Chart Types & Visualization Selection
category: tools
tags: [bi-analytics, tableau, chart-types, visualization, encoding, anscombes-quartet]
---

# Tableau Chart Types & Visualization Selection

Choosing the right chart type is a core BI skill. Each visualization encodes data attributes differently, and the choice should be driven by the specific question being answered. Anscombe's Quartet demonstrates why: four datasets with identical statistics produce completely different visual shapes.

## Key Facts

- Visualization = set of encoding methods mapped to data
- For precision (exact values): use **length** and **position on axes**
- For separation (grouping): use **color**, **volume**, **size**
- Rule: understand what question the user is asking, then choose the chart that answers it
- Selfmade visualizations = internal analysis (Jupyter, matplotlib); Premade = communication to users (dashboards, presentations)

## Patterns

### Data Encoding Attributes

Main encoding attributes ranked by precision:
1. **Position on common scale** (most precise)
2. **Length**
3. **Angle/slope**
4. **Area**
5. **Color intensity**
6. **Color hue** (least precise for quantitative data)

### Chart Type Selection Guide

| Chart | Best For | Notes |
|-------|----------|-------|
| **Bar/Column** | Comparisons between categories | Horizontal bars for long labels |
| **Line** | Trends over time | Connect only continuous data |
| **Pie/Donut** | Part-to-whole | Use sparingly, max 5 slices |
| **Matrix/Pivot** | Cross-tabulation | When precise numbers matter |
| **Card** | Single KPI number | Dashboard header factoids |
| **Table** | Raw tabular data | Detail drill-down |
| **Treemap** | Hierarchical part-to-whole with size | Better than pie for many categories |
| **Map/Filled Map** | Geographic data | Check color interpolation |
| **Gauge** | Progress to goal | Single-metric target tracking |
| **Scatter** | Correlation between two measures | Add trend line for clarity |
| **Heatmap** | Pattern density across two dimensions | Sequential color scale |

### Visualization Categories

**Selfmade (for internal analysis):**
- Business analytics: quick data exploration (Jupyter + matplotlib/seaborn)
- Scientific visualization: physical processes, 3D
- Search/concept visualization: relationships and principles

**Premade (to communicate to users):**
- Dashboards and presentations: interactive business performance panels
- Entity cards / personal accounts: banking-style views (KPI factoids + sparklines)
- Data analysis tools: user explores data themselves via interactivity
- Infographics and journalism: attention-grabbing, design-heavy

### Sparklines and KPI Factoids

- **KPI factoid**: single number with label, shows current state (e.g., "Sales $5.7M")
- **Sparkline**: tiny inline chart showing trend without axes, placed next to factoid
- Both placed in upper-left area for maximum attention and quick state assessment

### Dashboard Actions (Interactivity)

| Action | Description |
|--------|-------------|
| **Filter** | Click element -> filter other charts (most common) |
| **Highlight** | Click -> highlight related data without filtering |
| **Parameter** | User action -> change parameter value |
| **Set** | User action -> add/remove from set |
| **GoToSheet** | Navigate to another worksheet/dashboard |
| **URL** | Open URL with dynamic parameters |

URL action example:
```text
https://crm.example.com/deal?object=<object_number>
```

## Gotchas

- Anscombe's Quartet: always visualize data before trusting summary statistics - four datasets with identical mean, variance, correlation, and regression line look completely different
- Pie charts with more than 5 slices become unreadable - use bar chart or treemap instead
- Large colorful objects attract attention regardless of position (contrast overrides F-pattern reading)
- Incorrect color interpolation in heatmaps and maps makes charts misleading - always verify
- Each worksheet generates one query to the source - more charts = more queries = slower dashboard

## See Also

- [[dashboard-design-patterns]] - layout, F-pattern, Gestalt principles
- [[color-theory-visualization]] - color scales and accessibility
- [[tableau-calculations]] - calculated fields for chart data
- [[powerbi-fundamentals]] - Power BI visualization types
