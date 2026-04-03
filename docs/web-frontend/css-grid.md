---
title: CSS Grid
category: concepts
tags: [web-frontend, css, grid, layout]
---

# CSS Grid

Grid is a 2-dimensional layout system for rows AND columns simultaneously. Unlike Flexbox (1D), Grid defines a structure that items fill.

## Enabling Grid

```css
.container { display: grid; }
```

Direct children become grid items. Nothing visible changes until you define rows/columns.

## Defining Structure

```css
grid-template-columns: 200px 1fr 200px;        /* Fixed sidebar, flexible center */
grid-template-columns: repeat(3, 1fr);           /* 3 equal columns */
grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));  /* Responsive */
grid-template-rows: 80px 1fr auto;              /* Fixed header, flexible main, auto footer */
```

### The `fr` Unit
`fr` distributes remaining space after fixed sizes. `1fr 2fr` = 1/3 + 2/3 of remaining. `fr` accounts for `gap` automatically (unlike `%`).

### repeat(), minmax(), auto-fill/auto-fit
```css
repeat(3, 1fr)                              /* 1fr 1fr 1fr */
repeat(auto-fill, minmax(250px, 1fr))       /* Fill: keeps empty tracks */
repeat(auto-fit, minmax(250px, 1fr))        /* Fit: collapses empty tracks, items stretch */
minmax(200px, 1fr)                          /* Min 200px, max 1fr */
```

**The single most useful Grid pattern** - responsive grid with no media queries:
```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
}
```

## Gap

```css
gap: 20px;             /* Row and column */
gap: 20px 30px;        /* Row | Column */
```

## Placing Items

Grid lines are numbered starting at 1. Negative numbers count from end.

```css
.item {
  grid-column: 1 / 3;       /* Start line / End line (exclusive) */
  grid-row: 1 / 4;
  grid-column: 1 / span 2;  /* Start at 1, span 2 columns */
  grid-column: span 2;      /* Span 2 from auto position */
  grid-area: 1 / 1 / 4 / 3; /* row-start / col-start / row-end / col-end */
}
```

## grid-template-areas

```css
.grid {
  display: grid;
  grid-template-columns: 250px 1fr;
  grid-template-rows: 80px 1fr 60px;
  grid-template-areas:
    "header  header"
    "sidebar content"
    "footer  footer";
}
.header  { grid-area: header; }
.sidebar { grid-area: sidebar; }
.content { grid-area: content; }
.footer  { grid-area: footer; }
```

- Each row is a string, columns separated by spaces
- Areas must form rectangles
- `.` for empty cells: `"header ." ". content"`

### Responsive with Areas
```css
@media (max-width: 768px) {
  .grid {
    grid-template-columns: 1fr;
    grid-template-areas: "header" "content" "sidebar" "footer";
  }
}
```

## Auto Flow and Implicit Tracks

```css
grid-auto-flow: row;         /* Default: fill rows first */
grid-auto-flow: column;      /* Fill columns first */
grid-auto-flow: dense;       /* Backtrack to fill gaps */
grid-auto-rows: minmax(100px, auto);  /* Height of auto-generated rows */
```

## Alignment

### All Items (Container)
```css
justify-items: stretch | start | end | center;   /* Horizontal in cells */
align-items: stretch | start | end | center;      /* Vertical in cells */
place-items: center;                               /* Both axes shorthand */

justify-content: center;   /* Align entire grid within container */
align-content: center;
place-content: center;
```

### Individual Item
```css
.item {
  justify-self: center;
  align-self: end;
  place-self: center end;
}
```

## Subgrid

```css
.parent { display: grid; grid-template-columns: repeat(3, 1fr); }
.nested {
  display: grid;
  grid-template-columns: subgrid;  /* Inherit parent's column tracks */
  grid-column: span 3;
}
```

Subgrid aligns nested items to parent tracks - essential for card layouts where content aligns across cards.

## Common Patterns

### Holy Grail
```css
body {
  display: grid;
  grid-template-columns: 250px 1fr 200px;
  grid-template-rows: auto 1fr auto;
  grid-template-areas:
    "header header header"
    "nav    main   aside"
    "footer footer footer";
  min-height: 100vh;
}
```

### Masonry-like (Dense Packing)
```css
.gallery {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  grid-auto-rows: 200px;
  grid-auto-flow: dense;
  gap: 8px;
}
.tall { grid-row: span 2; }
.wide { grid-column: span 2; }
```

### Overlapping Elements
```css
.hero { display: grid; grid-template: 1fr / 1fr; }
.hero > * { grid-area: 1 / 1; }   /* All in same cell = overlap */
.hero-text { z-index: 2; }
```

## Grid vs Flexbox

| Use Grid | Use Flexbox |
|----------|-------------|
| 2D layout (rows AND columns) | 1D (row OR column) |
| Known structure | Content-driven sizes |
| Items align across rows | Items wrap naturally |
| Complex page layouts | Component internals |
| `grid-template-areas` | Simple centering |

They nest well: Grid for page layout, Flexbox for components within cells.

## Gotchas

- **`fr` is NOT `%`**: `fr` accounts for gaps, `%` doesn't (may cause overflow)
- **`auto-fill` vs `auto-fit`**: both responsive, but `auto-fit` collapses empty tracks
- **Grid line numbering starts at 1**: not 0
- **`minmax()` required for responsive**: `repeat(auto-fit, 1fr)` is invalid; need `minmax(min, 1fr)`
- **Subgrid requires spanning**: nested element must span parent tracks to use `subgrid`

## See Also

- [[css-flexbox]] - 1D layout companion
- [[css-responsive-design]] - Media queries, viewport units
- [[figma-layout-and-components]] - Grid design in Figma
