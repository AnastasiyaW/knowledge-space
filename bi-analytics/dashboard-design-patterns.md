---
title: Dashboard Design Patterns
category: BI Tools - Design
tags: [dashboard, design-pattern, wireframe, layout, UX, attention, BI-analyst, actionable]
---

# Dashboard Design Patterns

Layout patterns, attention principles, and design workflows for different types of BI dashboards.

## Key Facts

- Users start reading from top-left corner, but contrast (size, color, unusual shape) can redirect attention
- Group visualizations into blocks by: aggregation level, data dimension, business area
- Order blocks by importance, then arrange internal elements by importance
- [[visualization-principles]] Tufte principles apply within each block
- [[color-in-visualization]] should be consistent across blocks
- Wireframe Builder available in PowerPoint, Tableau Public, and Miro - includes chart chooser and layout area
- Five BI analyst skills: technical tool knowledge, information design, graphic design, UX design, storytelling

## Dashboard Types

| Type | Pattern | Key Feature |
|------|---------|-------------|
| **Alerts / Reports** | Monotone tables, even layout | Highlight deviations from tracked metrics |
| **Overview / Hub** | Mirrors org structure | Central KPI block with hierarchical branches per business unit |
| **Entity Pages** | Long-scroll or multi-tab | Header overview + deep-dive sections below |
| **Analytical Tools** | Complex, filter-heavy | Large analytical charts + supporting trend charts for context |
| **Experiments** | Text + metrics charts | Experiment description + results with red/green significance coding |
| **Self-service / Ad-hoc** | Filters left, results right | Many filters, user-driven exploration |
| **Directional / Project** | No fixed pattern | Each chart answers a specific question |

## Patterns

**Dashboard construction workflow:**

```
1. Strategic session -> business questions
2. Dashboard Canvas -> map questions to visualizations
3. Group visualizations into logical blocks
   - By aggregation level
   - By dimension/slice
   - By business area
4. Prioritize blocks (importance ranking)
5. Prioritize elements within blocks
6. Create wireframe (PowerPoint/Miro/Tableau)
7. Build in Tableau
8. Iterate with users
```

**Attention hierarchy:**

```
Primary attention (top-left):
  -> KPI cards, NSM, traffic lights

Secondary attention (top-right, center):
  -> Trend charts, comparisons

Tertiary (bottom):
  -> Detail tables, drill-down views

Override with contrast:
  -> Red alert on gray background attracts
     attention regardless of position
```

**Wireframe Builder components:**

```
Chart Chooser:
  - Select chart type based on task
  - Comparison -> bar chart
  - Trend -> line chart
  - Composition -> stacked bar / pie
  - Distribution -> histogram / box plot
  - Relationship -> scatter plot

Layout Area:
  - Divide into blocks
  - Set block sizes by importance
  - Add titles, descriptions, comments
  - Define filter placement
```

## Gotchas

- **Symptom**: Users open dashboard once then never return -> **Cause**: Dashboard answers no specific question or is too generic -> **Fix**: Start from business questions (Dashboard Canvas), not from available data
- **Symptom**: Dashboard loads slowly, users leave -> **Cause**: Too many visualizations rendering simultaneously -> **Fix**: Use hidden containers, drill-down actions, limit to 6 sheets max per view. See [[tableau-performance-optimization]]
- **Symptom**: Dashboard is "pretty" but not actionable -> **Cause**: Missing context - no goals, no comparisons, no annotations -> **Fix**: Add target lines, YoY deltas, event annotations, color-coded performance indicators
- **Symptom**: Different teams interpret the same dashboard differently -> **Cause**: No shared metric definitions or visual language -> **Fix**: Document metric definitions, use consistent color encoding, add tooltips

## See Also

- [[visualization-principles]] - Tufte's nine principles
- [[color-in-visualization]] - consistent color language
- [[tableau-performance-optimization]] - making dashboards fast
- Tableau dashboard best practices: https://help.tableau.com/current/pro/desktop/en-us/dashboards_best_practices.htm
