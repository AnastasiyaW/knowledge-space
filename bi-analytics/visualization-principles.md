---
title: Data Visualization Principles
category: BI Tools - Visualization
tags: [visualization, tufte, data-ink-ratio, design, information-design, chart-selection, lie-factor]
---

# Data Visualization Principles

Edward Tufte's principles of good data visualization applied to BI dashboards. Core framework for creating effective, honest, information-dense visualizations.

## Key Facts

- Nine principles from Tufte's "The Visual Display of Quantitative Information"
- **Data-ink ratio** = pixels used for data / total pixels. Higher is better. KPI for any dashboard
- **Lie factor** = size of effect shown / size of actual effect. Must equal 1.0
- Good visualization shows data at the lowest granularity level, then aggregates at different levels
- Four visualization goals: description, exploration, storage, decoration
- [[dashboard-design-patterns]] apply these principles to specific dashboard types
- [[color-in-visualization]] is a dedicated sub-topic of visual encoding

## The Nine Principles

1. **Show the data** - display all data at lowest granularity when possible (jitter plots, beeswarm)
2. **Provoke thinking about data** - not about design, technology, or decoration
3. **Do not distort data** - avoid lie factor, 3D charts, truncated axes
4. **High information density** - data points per square cm should be high (sparklines, small multiples)
5. **Show large datasets concisely** - encode many variables with few visual elements (Minard's Napoleon map)
6. **Enable comparison** - provide context (goals, previous year, averages, events, trend lines)
7. **Reveal data at multiple levels** - drill from overview to detail
8. **Serve a clear purpose** - description, exploration, storage, or decoration
9. **Reflect data nature logically** - use real-world visual metaphors when appropriate

## Patterns

**Data-ink ratio improvement checklist:**

```
Remove non-data-ink:
  [ ] Background colors/images
  [ ] Grid lines (keep only if essential)
  [ ] Borders and outlines
  [ ] Decorative icons and shadows

Reduce redundant data-ink:
  [ ] Round numbers appropriately
  [ ] Embed legend into chart (direct labels)
  [ ] Use inline labels instead of axis labels
  [ ] Remove repeated axis values
```

**Context additions for actionable dashboards:**

```
Without context: bare line chart with values -> hard to judge good/bad

With context:
  + Goal lines (target values)
  + Year-over-year comparison
  + Color highlighting for problem areas
  + Event annotations on timeline
  + Growth percentages vs previous period
```

**Chart anti-patterns (lie factor violations):**

```
AVOID:
  - 3D pie charts (perspective distorts proportions)
  - Truncated Y-axis (makes small changes look dramatic)
  - Area/icon scaling by height when data maps to area
  - Cumulative charts that hide declining trends
  - Missing context (showing 2 years when 10 years tells different story)
```

## Gotchas

- **Symptom**: Users say dashboard is "pretty but useless" -> **Cause**: Low data-ink ratio - too many decorative elements -> **Fix**: Apply data-ink reduction checklist, remove icons/shadows/borders
- **Symptom**: Stakeholders draw wrong conclusions from chart -> **Cause**: Lie factor > 1 due to icon/area scaling or truncated axis -> **Fix**: Audit charts for proportional accuracy, always start Y-axis at 0 for bar charts
- **Symptom**: Dashboard has only aggregated numbers, no insight -> **Cause**: Missing granular data and context -> **Fix**: Show individual data points (jitter/beeswarm), add comparison context (goals, YoY)

## See Also

- [[color-in-visualization]] - color scales and palette selection
- [[dashboard-design-patterns]] - layout patterns for different dashboard types
- [[tableau-performance-optimization]] - balancing information density with load time
- Tufte, "The Visual Display of Quantitative Information": https://www.edwardtufte.com/tufte/books_vdqi
