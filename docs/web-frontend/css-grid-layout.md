---
title: CSS Grid Layout
category: css
tags: [css, grid, layout, two-dimensional, grid-template, grid-area]
---

# CSS Grid Layout

## Key Facts

- CSS Grid is a **two-dimensional** layout system (rows AND columns simultaneously)
- `display: grid` on parent creates grid container; children become grid items
- `grid-template-columns` / `grid-template-rows` define track sizes
- `fr` unit distributes remaining space proportionally: `1fr 2fr` = 1/3 + 2/3
- `repeat(3, 1fr)` shorthand for `1fr 1fr 1fr`
- `minmax(min, max)` constrains track size: `minmax(200px, 1fr)` = at least 200px, grows with space
- `auto-fit` / `auto-fill` with `repeat()` create responsive grids without media queries
- `gap` (or `row-gap` / `column-gap`) adds gutters between tracks
- `grid-column` / `grid-row` on items specify placement: `grid-column: 1 / 3` spans 2 columns
- Named grid areas via `grid-template-areas` for readable layout definitions
- Related: [[css-flexbox]], [[responsive-design-and-media-queries]], [[css-box-model-and-display]]

## Patterns

### Responsive Auto-Fit Grid

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}
/* Items auto-wrap and fill available space - no media queries needed */
```

### Named Areas Layout

```css
.layout {
  display: grid;
  grid-template-areas:
    "header header"
    "sidebar main"
    "footer footer";
  grid-template-columns: 250px 1fr;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
}

.header  { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main    { grid-area: main; }
.footer  { grid-area: footer; }
```

### Spanning Items

```css
.featured {
  grid-column: 1 / -1; /* span all columns (-1 = last line) */
}
.wide {
  grid-column: span 2; /* span 2 columns from auto-placed position */
}
```

### Implicit vs Explicit Grid

```css
.grid {
  grid-template-columns: repeat(3, 1fr); /* explicit: 3 columns */
  grid-auto-rows: minmax(100px, auto);   /* implicit: auto-created rows */
  grid-auto-flow: dense;                 /* fill gaps when items span */
}
```

### Alignment Within Grid

```css
.grid {
  justify-items: center;  /* horizontal alignment of all items in their cells */
  align-items: center;    /* vertical alignment */
  justify-content: center; /* align the grid itself in the container */
  align-content: center;
}
.item {
  justify-self: start; /* override for single item */
  align-self: end;
}
```

## Gotchas

- `auto-fit` collapses empty tracks to 0; `auto-fill` keeps empty tracks at their size - `auto-fit` is usually what you want for responsive layouts
- Grid items default to `min-width: auto` / `min-height: auto`; content can overflow cells - use `minmax(0, 1fr)` instead of `1fr` to allow shrinking
- `grid-template-areas` requires every row to have the same number of cells; use `.` for empty cells
- Subgrid (`grid-template-columns: subgrid`) lets nested grids align to parent grid tracks; limited browser support until 2023
- Grid does not have a `flex-grow` equivalent; track sizes are fixed or proportional, items don't compete for space within a track

## See Also

- [MDN: CSS Grid Layout](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout)
- [CSS Tricks: Complete Guide to Grid](https://css-tricks.com/snippets/css/complete-guide-grid/)
