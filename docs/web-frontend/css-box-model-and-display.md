---
title: CSS Box Model and Display
category: css
tags: [css, box-model, display, margin, padding, border-box]
---

# CSS Box Model and Display

## Key Facts

- Every element is a rectangular box: **content** -> **padding** -> **border** -> **margin**
- `box-sizing: content-box` (default): width/height = content only; padding and border add to total size
- `box-sizing: border-box`: width/height includes content + padding + border; the standard modern reset
- `display: block` - full-width, stacks vertically, respects width/height/margin
- `display: inline` - flows in text, ignores width/height, only horizontal margin/padding affect layout
- `display: inline-block` - inline flow but respects width/height and all margins
- `display: none` - removed from layout and accessibility tree; `visibility: hidden` hides but keeps space
- **Margin collapsing**: adjacent vertical margins of block elements collapse to the larger value
- `outline` does not affect layout (sits outside box model); `border` does
- Related: [[css-flexbox]], [[css-grid-layout]], [[css-positioning-and-z-index]]

## Patterns

### Universal Box-Sizing Reset

```css
*, *::before, *::after {
  box-sizing: border-box;
}
```

### Centering a Block Element

```css
/* Horizontal center with auto margins */
.container {
  max-width: 1200px;
  margin-inline: auto; /* shorthand for margin-left + margin-right */
  padding-inline: 1rem;
}
```

### Logical Properties (Modern)

```css
/* Physical (old) */
margin-left: 1rem;
padding-top: 0.5rem;

/* Logical (modern, respects writing direction) */
margin-inline-start: 1rem;
padding-block-start: 0.5rem;

/* Shorthand: block = top/bottom, inline = left/right (for LTR) */
margin-block: 1rem 2rem; /* top, bottom */
margin-inline: auto;     /* left, right */
```

### Display Flow Comparison

```css
/* Block: div, p, section */
.block { display: block; width: 300px; } /* takes 300px, stacks */

/* Inline: span, a, em */
.inline { display: inline; } /* width/height ignored */

/* Inline-block: best of both */
.badge {
  display: inline-block;
  padding: 4px 8px;
  width: 100px; /* respected unlike inline */
}
```

## Gotchas

- Forgetting `border-box` causes layout bugs: a `width: 100%` element with padding overflows its parent
- Vertical margins collapse between siblings and between parent-child (no border/padding separating them); horizontal margins never collapse
- `margin: auto` only works for horizontal centering on block elements with explicit width; for vertical centering use flexbox/grid
- `padding` on `inline` elements expands visually but doesn't push surrounding lines away vertically
- `%` values for padding/margin are relative to the **parent's width** (even for vertical padding)

## See Also

- [MDN: The box model](https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/The_box_model)
- [MDN: display](https://developer.mozilla.org/en-US/docs/Web/CSS/display)
