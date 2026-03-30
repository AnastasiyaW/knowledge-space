---
title: CSS Flexbox
category: css
tags: [css, flexbox, layout, alignment, flex-container, flex-item]
---

# CSS Flexbox

## Key Facts

- Flexbox is a **one-dimensional** layout system (row OR column, not both simultaneously)
- `display: flex` on parent makes children flex items; `display: inline-flex` for inline container
- **Main axis** direction set by `flex-direction`: `row` (default), `row-reverse`, `column`, `column-reverse`
- **Cross axis** is perpendicular to main axis
- `justify-content` aligns items along main axis: `flex-start`, `center`, `flex-end`, `space-between`, `space-around`, `space-evenly`
- `align-items` aligns items along cross axis: `stretch` (default), `center`, `flex-start`, `flex-end`, `baseline`
- `flex-wrap: wrap` allows items to wrap to next line; default `nowrap` squeezes all items in one line
- `gap` property adds spacing between flex items without margin hacks
- `flex` shorthand: `flex: <grow> <shrink> <basis>` - default is `0 1 auto`
- Related: [[css-grid-layout]], [[css-box-model-and-display]], [[responsive-design-and-media-queries]]

## Patterns

### Holy Grail Layout (Header/Main/Footer)

```css
body {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

main { flex: 1; } /* grows to fill remaining space */
header, footer { flex-shrink: 0; }
```

### Centering (The Classic)

```css
.center-both {
  display: flex;
  justify-content: center; /* main axis */
  align-items: center;     /* cross axis */
  min-height: 100vh;
}
```

### Responsive Card Row

```css
.cards {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}
.card {
  flex: 1 1 300px; /* grow, shrink, min-width basis */
  /* Cards grow equally, wrap when < 300px each */
}
```

### Navbar with Spacer

```css
.nav {
  display: flex;
  align-items: center;
  gap: 1rem;
}
.nav-spacer { margin-left: auto; } /* pushes subsequent items to the right */
```

### Flex Item Properties

```css
.item {
  flex-grow: 1;     /* proportion of remaining space to absorb */
  flex-shrink: 0;   /* don't shrink below basis */
  flex-basis: 200px; /* initial size before grow/shrink */
  align-self: center; /* override parent's align-items */
  order: -1;         /* move to front visually (default order: 0) */
}
```

## Gotchas

- `flex: 1` expands to `flex: 1 1 0%` (basis = 0), not `1 1 auto`; items ignore their content width and split space equally
- `flex-basis` vs `width`: flex-basis takes priority in flex context; use `min-width: 0` to allow text truncation inside flex items
- Flex items default to `min-width: auto` which prevents shrinking below content size; set `min-width: 0` or `overflow: hidden` to fix
- `margin: auto` on a flex item absorbs all extra space in that direction (useful for alignment hacks)
- `gap` in flexbox is well-supported (all modern browsers since 2021); no IE11 support

## See Also

- [MDN: Flexbox](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_flexible_box_layout)
- [CSS Tricks: Complete Guide to Flexbox](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)
