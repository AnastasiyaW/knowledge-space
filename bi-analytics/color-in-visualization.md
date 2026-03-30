---
title: Color in Data Visualization
category: BI Tools - Visualization
tags: [color, palette, colorbrewer, categorical, sequential, diverging, accessibility, color-blind]
---

# Color in Data Visualization

Color encoding strategies for data visualization: categorical, sequential (continuous), and diverging scales. Includes palette selection and accessibility considerations.

## Key Facts

- Three scale types: **categorical** (groups), **sequential/continuous** (magnitude), **diverging** (deviation from center)
- Maximum 5-7 colors in a categorical palette - human memory limit for distinguishing categories
- One color = one entity across all charts in a dashboard (consistency)
- Gray is the most important color - start with gray, add color only where it aids comprehension
- Default safe choice: blue, gray, and their shades
- Always check palettes for color-blind accessibility
- [[visualization-principles]] data-ink ratio applies to color usage
- Connected to [[dashboard-design-patterns]] for consistent color language across views

## Scale Types

| Scale | Purpose | Rules |
|-------|---------|-------|
| **Categorical** | Group by category | No implied order, equal visual weight, max 5-7 colors |
| **Sequential** | Encode magnitude | One hue, light=low, dark=high, careful interpolation |
| **Diverging** | Show deviation | Two polar colors through neutral (gray), red-green for good/bad, blue-orange for neutral deviation |

## Patterns

**Categorical palette rules:**

```
DO:
  - Same color = same category across ALL charts
  - Muted/desaturated colors for large areas
  - Equal saturation across categories (no hierarchy)
  - Verify readability against background

DON'T:
  - Use continuous scale for categorical data (creates false hierarchy)
  - Use more than 7 colors
  - Use the same color for different things in different charts
```

**Adding custom palette to Tableau:**

```xml
<!-- File: My Tableau Repository/Preferences.tps -->
<workbook>
  <preferences>
    <color-palette name="Corporate" type="regular">
      <color>#2B5F8A</color>
      <color>#7BA7CC</color>
      <color>#A8D8A8</color>
      <color>#E8B960</color>
      <color>#CC6666</color>
    </color-palette>
    <color-palette name="Heatmap" type="ordered-sequential">
      <color>#F7FCF5</color>
      <color>#74C476</color>
      <color>#006D2C</color>
    </color-palette>
    <color-palette name="Deviation" type="ordered-diverging">
      <color>#D73027</color>
      <color>#FFFFBF</color>
      <color>#1A9850</color>
    </color-palette>
  </preferences>
</workbook>
```

**Color palette tools:**

```
ColorBrewer 2.0  - https://colorbrewer2.org (designed for maps/data viz)
DataColorPicker  - interpolation-based palette generator
DataWrapper      - built-in palette checker
Coolors           - palette generator from photos
Paletton         - color wheel based
Adobe Color      - advanced color harmony tools
```

## Gotchas

- **Symptom**: Users with color vision deficiency cannot read the chart -> **Cause**: Red-green palette without alternative encoding -> **Fix**: Use color-blind safe palettes (ColorBrewer), add shape/pattern as secondary encoding
- **Symptom**: Sequential scale looks misleading on a map -> **Cause**: Bad interpolation - color steps don't match data distribution -> **Fix**: Adjust interpolation breakpoints in Tableau (Edit Colors > Advanced) to match data distribution
- **Symptom**: Double encoding (size + color for same metric) confuses users -> **Cause**: Redundant encoding without clear purpose -> **Fix**: Use double encoding only when it genuinely aids comparison; default to single encoding
- **Symptom**: Chart looks garish and unprofessional -> **Cause**: Using fully saturated primary colors -> **Fix**: Reduce saturation and brightness; use muted tones for large areas, bright accents only for highlights

## See Also

- [[visualization-principles]] - data-ink ratio and Tufte principles
- [[dashboard-design-patterns]] - applying consistent color to dashboard layouts
- ColorBrewer: https://colorbrewer2.org
- Tableau color docs: https://help.tableau.com/current/pro/desktop/en-us/viewparts_marks_markproperties_color.htm
