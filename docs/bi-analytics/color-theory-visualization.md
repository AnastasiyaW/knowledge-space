---
title: Color Theory for Data Visualization
category: concepts
tags: [bi-analytics, color, visualization, accessibility, palette, colorbrewer]
---

# Color Theory for Data Visualization

Color is one of the most powerful and most frequently misused encoding attributes in data visualization. Proper use of color scales, accessibility considerations, and consistent color semantics across dashboards significantly impact readability and trustworthiness.

## Key Facts

- Three color scale types: categorical, sequential, diverging
- Max 5-7 colors per dashboard - more colors = impossible to remember associations
- One color = one entity across all charts in a dashboard
- Gray is the default base color; add color only where it helps the user
- Default safe choice when unsure: blue, gray, and their shades
- Muted shades over bright: reduce saturation and brightness
- Common associations: green = good, red = bad

## Patterns

### Color Scale Types

| Type | Use Case | Rules |
|------|----------|-------|
| **Categorical** | Group/separate categories | No sense of order; max 5-7 colors; all equal visual weight |
| **Sequential** | Encode numeric values | One base color + gradient; light = less, dark = more |
| **Diverging** | Show deviations from 0/mean | Two polar colors; gradient through neutral gray; red-green for good-bad, blue-orange for deviations |

### Color Interpolation

Interpolation = mapping color shades to specific numeric values. Incorrect interpolation makes charts misleading. Always verify heatmaps and maps for proper interpolation in Tableau.

### Custom Palette in Tableau

Add to: `My Tableau Repository/Preferences.tps`

Palette types:
- `regular` = categorical palette
- `sequential` = continuous gradient
- `diverging` = two-pole gradient

### Color-Blind Safe Resources

- **ColorBrewer** (colorbrewer2.org) - the gold standard for cartographic/data palettes
- **DataColorPicker** - generates palettes with perceptual uniformity
- **Coolors** - palette generator with accessibility testing
- **Paletton** - color wheel based palette design

### Color Checklist

1. Prepare a color palette before starting
2. One color = one entity consistently across charts
3. Double coding (color + size) is OK but often unnecessary
4. Large area charts -> use pastel colors (lower saturation)
5. Gray as primary base color
6. Test for color-blind accessibility
7. Dark text on light background (verify contrast)

### Color in Power BI

Custom themes allow full color control via JSON:
```json
{
  "name": "MyTheme",
  "dataColors": ["#118DFF", "#12239E", "..."],
  "background": "#FFFFFF",
  "foreground": "#252423",
  "tableAccent": "#118DFF"
}
```

Apply via: View -> Themes -> Browse for themes.

### Conditional Color in DAX

```dax
KPI Color =
IF([Actual] >= [Target], "#28A745", "#DC3545")
```

Apply in: Visualizations -> Value field -> Conditional formatting -> Field value.

## Gotchas

- Red-green combination is the worst for color-blind users (8% of males) - use blue-orange or blue-red instead
- Sequential scales with too-similar shades become unreadable in print
- Bright saturated colors create visual fatigue on data-heavy dashboards
- Color that "pops" on a monitor may wash out when projected - test in presentation environment
- Using the same color for different entities across charts breaks the dashboard's visual language

## See Also

- [[dashboard-design-patterns]] - layout and visual hierarchy
- [[tableau-chart-types]] - encoding attributes and chart selection
- [[powerbi-advanced-features]] - Power BI themes and conditional formatting
