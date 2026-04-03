---
title: Power BI Advanced Features
category: tools
tags: [bi-analytics, power-bi, dax, bookmarks, drill-through, what-if, custom-visuals]
---

# Power BI Advanced Features

Advanced Power BI capabilities including custom themes, visuals from AppSource, What-If parameters for scenario analysis, drill-through navigation, bookmarks for storytelling, and advanced DAX patterns.

## Key Facts

- Custom themes via JSON files for brand compliance and accessibility
- Custom visuals from AppSource marketplace (`.pbiviz` format)
- What-If parameters create slicer-driven scenario analysis
- Drill-through enables summary-to-detail navigation via right-click
- Bookmarks capture report state (filters, page, visibility) for navigation and storytelling
- Performance Analyzer identifies slow visuals

## Patterns

### Custom Themes

```json
{
  "name": "MyTheme",
  "dataColors": ["#118DFF", "#12239E", "..."],
  "background": "#FFFFFF",
  "foreground": "#252423",
  "tableAccent": "#118DFF"
}
```

Apply: View -> Themes -> Browse for themes (JSON file) or select from gallery. Theme generators available as web tools.

### What-If Parameters

Create: Modeling -> New Parameter -> set name, data type, min, max, increment, default.

Creates automatically: a new table with single-column range + a slicer + a measure for selected value.

```dax
-- Auto-created
Discount Rate = SELECTEDVALUE('Discount'[Discount], 0)

-- User-created measure using the parameter
Revenue After Discount = [Total Revenue] * (1 - [Discount Rate])
```

**Metric switcher pattern** (select which metric to display via slicer):
```dax
Selected Metric =
SWITCH(
    SELECTEDVALUE('Metric Selector'[Metric]),
    "Revenue", [Total Revenue],
    "Profit", [Total Profit],
    "Orders", [Order Count]
)
```

### Drill-Through

Setup:
1. Create detail page
2. Drag dimension field to "Drill-through" section of Filters pane
3. On summary pages: right-click data point -> Drill through -> [page name]

Filter is passed automatically. A "Back" button appears on detail page.

Use case: region totals -> click region -> see all transactions in that region.

### Bookmarks

Captures: current page, filters, slicer values, visual visibility.

Create: View -> Bookmarks pane -> Add bookmark.

Common patterns:
- **Storytelling**: sequence of bookmarks as guided narrative
- **Custom navigation**: buttons with "Bookmark" action replace default page tabs
- **Conditional navigation**: button shows different page based on slicer
- **Visual type toggle**: show chart OR table of same data via bookmark + selection visibility
- **Rich tooltips**: create hover tooltips using SVG images

Button actions: Bookmark, Page navigation, Q&A, Drill-through, Web URL.

### Advanced DAX

**FORMAT function**:
```dax
Sales Label = FORMAT([Total Sales], "$#,##0.00")
Month Name = FORMAT(Date[Date], "MMMM YYYY")
```

**Conditional formatting via DAX**:
```dax
KPI Color = IF([Actual] >= [Target], "#28A745", "#DC3545")
```

Apply: Visualizations -> Value field -> Conditional formatting -> Field value.

**Calculated tables**:
```dax
Date Table = CALENDAR(DATE(2020,1,1), DATE(2025,12,31))
Top 10 Customers = TOPN(10, Customers, [Total Revenue], DESC)
```

### Performance Optimization

Use Performance Analyzer: View -> Performance Analyzer.

Optimization techniques:
- Prefer Import mode over DirectQuery for large aggregations
- Reduce column cardinality (remove unused columns)
- Pre-aggregate in Power Query before loading
- Use integer surrogate keys in relationships instead of text keys
- Avoid bidirectional relationships unless required
- Move complex calculations to Power Query (M) instead of DAX measures

## Gotchas

- Custom visuals from AppSource may not support all formatting options or may behave differently in Power BI Service vs Desktop
- What-If parameters create actual tables in the model - many parameters = model bloat
- Bookmarks capture visual visibility state, which can break if you add/remove visuals after creating bookmarks
- Drill-through only works on data points that match the drill-through filter dimension
- Performance Analyzer measures may vary between Desktop and Service due to different query engines

## See Also

- [[powerbi-fundamentals]] - DAX basics, data model, Power Query
- [[bi-tools-comparison]] - Power BI vs Tableau feature comparison
- [[dashboard-design-patterns]] - design principles for navigation
- [[color-theory-visualization]] - themes and color best practices
