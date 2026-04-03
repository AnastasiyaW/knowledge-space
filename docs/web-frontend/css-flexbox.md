---
title: CSS Flexbox
category: concepts
tags: [web-frontend, css, flexbox, layout]
---

# CSS Flexbox

Flexbox is a 1-dimensional layout system for distributing space and aligning items along a single axis (row or column). It replaced float-based layouts for component-level design.

## Enabling Flexbox

```css
.container { display: flex; }         /* Block-level flex container */
.container { display: inline-flex; }  /* Inline-level */
```

All direct children become **flex items** automatically.

## Container Properties

### Direction and Wrapping
```css
flex-direction: row;             /* Default: left-to-right */
flex-direction: row-reverse;     /* Right-to-left */
flex-direction: column;          /* Top-to-bottom */
flex-direction: column-reverse;

flex-wrap: nowrap;       /* Default: single line, items shrink */
flex-wrap: wrap;         /* Wrap to next line */

flex-flow: row wrap;     /* Shorthand: direction + wrap */
```

### Main Axis Alignment (justify-content)
```css
justify-content: flex-start;      /* Packed to start (default) */
justify-content: flex-end;        /* Packed to end */
justify-content: center;          /* Centered */
justify-content: space-between;   /* First/last at edges, equal gaps */
justify-content: space-around;    /* Equal space around each (edges half) */
justify-content: space-evenly;    /* Equal space everywhere */
```

### Cross Axis Alignment (align-items)
```css
align-items: stretch;     /* Default: fill container height */
align-items: flex-start;  /* Top (for row) */
align-items: flex-end;    /* Bottom */
align-items: center;      /* Centered */
align-items: baseline;    /* Text baseline alignment */
```

### Multi-line Cross Axis (align-content)
Only applies with `flex-wrap: wrap` creating multiple lines:
```css
align-content: flex-start | flex-end | center | space-between | space-around | stretch;
```

### Gap
```css
gap: 16px;           /* Row and column gap */
gap: 16px 24px;      /* Row | Column */
```

Modern replacement for margin hacks. No gap on outer edges.

## Item Properties

### flex-grow / flex-shrink / flex-basis
```css
flex-grow: 0;      /* Default: don't grow */
flex-grow: 1;      /* Grow to fill available space (proportional) */

flex-shrink: 1;    /* Default: shrink when needed */
flex-shrink: 0;    /* Don't shrink (may overflow) */

flex-basis: auto;  /* Default: use content/width */
flex-basis: 200px; /* Starting size before grow/shrink */
flex-basis: 0;     /* Ignore content, distribute ALL space via grow */
```

### Shorthand
```css
flex: 0 1 auto;     /* Default: no grow, shrink, auto basis */
flex: 1;            /* flex: 1 1 0 - grow equally, ignore content */
flex: auto;         /* flex: 1 1 auto - grow, respect content */
flex: none;         /* flex: 0 0 auto - fixed size */
flex: 0 0 200px;   /* Fixed 200px */
```

### Individual Item Overrides
```css
.item { align-self: center; }     /* Override align-items for this item */
.item { order: -1; }              /* Move before items with order 0 */
```

`order` is visual only - screen readers follow DOM order.

## auto Margin Trick

```css
.nav-last  { margin-left: auto; }   /* Push to right in row */
.centered  { margin: auto; }        /* Center both axes in flex */
```

`margin: auto` in flex absorbs remaining space in that direction.

## Common Patterns

### Centering (Holy Grail)
```css
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}
```

### Horizontal Navigation
```css
nav { display: flex; justify-content: space-between; align-items: center; }
.nav-links { display: flex; gap: 24px; list-style: none; }
```

### Card Row (Equal Height)
```css
.cards { display: flex; gap: 24px; }
.card { flex: 1; }  /* Equal width */
```

### Footer Sticks to Bottom
```css
body { display: flex; flex-direction: column; min-height: 100vh; }
main { flex: 1; }       /* Takes remaining space */
footer { flex-shrink: 0; }
```

### Responsive Wrapping
```css
.grid { display: flex; flex-wrap: wrap; gap: 16px; }
.grid-item { flex: 1 1 300px; }  /* Min 300px, wraps when needed */
```

## Flexbox vs Grid

| Feature | Flexbox | Grid |
|---------|---------|------|
| Dimension | 1D (row OR column) | 2D (rows AND columns) |
| Best for | Components (nav, cards) | Page layout, complex grids |
| Content-driven | Yes | No (grid defines cells) |

**Rule**: Flexbox for component-level, Grid for page-level. They compose well together.

## Gotchas

- **`flex-basis` overrides `width`**: in a row direction, `flex-basis` takes priority over `width`
- **`flex: 1` means `flex: 1 1 0`**: basis is 0, distributing ALL space, not just remaining
- **Default `min-width: auto`**: flex items won't shrink below their content; override with `min-width: 0` or `overflow: hidden`
- **`order` accessibility**: visual order changes don't affect tab/screen reader order
- **`margin: auto` absorbs space**: can break `justify-content` if you don't expect it

## See Also

- [[css-grid]] - 2D layout system
- [[css-box-model-and-layout]] - Display, position, box model
- [[css-responsive-design]] - Media queries and fluid layouts
