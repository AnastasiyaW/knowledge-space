---
title: Dashboard Design Patterns
category: concepts
tags: [bi-analytics, dashboard, design, ux, layout, gestalt, f-pattern, storytelling]
---

# Dashboard Design Patterns

Dashboard design combines information design, graphic design, UX, and storytelling. Good design follows established patterns for reading direction, visual hierarchy, and cognitive principles to ensure users can quickly find and act on insights.

## Key Facts

- Users read left-to-right, top-to-bottom (F-pattern for European audiences)
- High-attention zone: upper-left corner; low-attention zone: lower-right
- Contrast overrides F-pattern: large colorful objects attract attention regardless of position
- KPI factoids and sparklines go in upper-left for maximum impact
- Dashboard structure: Summary -> Trend -> Breakdown -> Detail (general to specific)
- Max 5-7 colors per dashboard; consistent color coding across charts
- Each chart should answer exactly one user question

## Patterns

### Dashboard Structure (General to Specific)

```text
Level 1: KPI summary (total state, one number per metric)
Level 2: Trend over time (is it improving or declining?)
Level 3: Breakdown by dimension (which segment drives the trend?)
Level 4: Detail/drill-down (individual records, anomalies)
```

Visual layout:
```text
Header (title)
+-- KPI factoids + sparklines (upper area, high attention)
+-- Trend charts (middle area)
+-- Detail table (lower area)
```

### Modular Layout

Divide dashboard into invisible rectangular blocks (like newspaper columns):
- Use Tiled containers (only one outer Tiled, then vertical/horizontal inside)
- No floating elements (breaks adaptive sizing)

Dashboard sizing modes:
- **Fixed**: preserves exact specified size
- **Range**: min/max width/height range (recommended)
- **Automatic**: adjusts to screen, but elements may shift

Rule: plan structure first, then create containers. Vertical outer, horizontals inside, then verticals within horizontals.

### UX Principles

**Fitts's Law**: elements that need frequent interaction should be larger and closer to center.

**Hick's Law**: more choices = longer decision time. Minimize filter options where possible.

Filter placement: near the charts they control. UX = user habits + common sense.

### Gestalt Principles

- **Proximity**: nearby objects are perceived as related - use padding to group related charts
- **Enclosed area**: objects inside a visible container are perceived as one group
- **Similarity/Contrast**: similar-looking items are grouped; different-looking items are separated

### Storytelling vs Operational Dashboards

**Storytelling** = data + visual + narrative. Used in presentations, not in operational dashboards. Add annotations, titles, context lines to guide the user through the insight.

**Operational dashboards** = designed for repeated use, self-service exploration, minimal narrative.

### Visualization Checklist

Before finalizing a dashboard:
- [ ] KPI factoids in upper-left (high attention zone)
- [ ] Chart hierarchy: summary -> trend -> breakdown -> detail
- [ ] Max 5-7 colors; consistent color coding across charts
- [ ] Each chart answers exactly one user question
- [ ] Filter labels are clear; filter positions near affected charts
- [ ] Context lines and annotations where meaningful
- [ ] Performance: initial load < 10 seconds
- [ ] Mobile layout considered if needed
- [ ] Tested with actual stakeholders in test group

### Report Storytelling Principles

- One clear question answered per page
- Title states the insight, not just the topic ("Sales grew 23% vs LY" not "Sales Analysis")
- Consistent color coding (red=bad, green=good)
- Annotations on key events in time series
- Context: add comparison periods, targets, benchmarks

## Gotchas

- Building in isolation without stakeholder check-ins is the #1 anti-pattern - show wireframe before building, show draft at 50%
- A large map in the lower-right will draw attention away from KPIs in the upper-left due to contrast override
- More than 6 sheets per workbook degrades performance - consider splitting into multiple dashboards
- Mobile layout is a separate design in Tableau, not automatic - plan for it explicitly if needed
- "Just build something" requests lead to rework - invest 2 days in requirements to save 2 weeks of rebuilding

## See Also

- [[color-theory-visualization]] - color scales and accessibility
- [[tableau-chart-types]] - chart selection and encoding
- [[bi-development-process]] - requirements gathering before design
- [[powerbi-advanced-features]] - bookmarks and drill-through for navigation
