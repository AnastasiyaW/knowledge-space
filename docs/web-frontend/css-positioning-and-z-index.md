---
title: CSS Positioning and Z-Index
category: css
tags: [css, position, z-index, stacking-context, fixed, sticky, absolute, relative]
---

# CSS Positioning and Z-Index

## Key Facts

- `position: static` (default) - normal document flow, top/left/z-index have no effect
- `position: relative` - offset from normal position; creates containing block for absolute children
- `position: absolute` - removed from flow; positioned relative to nearest non-static ancestor
- `position: fixed` - removed from flow; positioned relative to viewport; stays on scroll
- `position: sticky` - relative until scroll threshold, then fixed within its container
- **Stacking context** is created by: positioned elements with z-index, opacity < 1, transform, filter, etc.
- `z-index` only works on positioned elements (`relative`, `absolute`, `fixed`, `sticky`)
- Elements within the same stacking context are compared; z-index cannot break out of parent's context
- `inset: 0` is shorthand for `top: 0; right: 0; bottom: 0; left: 0`
- Related: [[css-box-model-and-display]], [[css-flexbox]], [[responsive-design-and-media-queries]]

## Patterns

### Modal Overlay

```css
.overlay {
  position: fixed;
  inset: 0;          /* covers entire viewport */
  background: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  display: flex;
  justify-content: center;
  align-items: center;
}
.modal {
  position: relative; /* z-index relative to overlay */
  background: white;
  padding: 2rem;
  max-width: 500px;
}
```

### Sticky Header

```css
.header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: white; /* must be opaque to cover scrolling content */
}
```

### Absolute Positioning Within Parent

```css
.card {
  position: relative; /* creates containing block */
}
.badge {
  position: absolute;
  top: -8px;
  right: -8px;
}
```

### Tooltip Pattern

```css
.tooltip-wrapper {
  position: relative;
  display: inline-block;
}
.tooltip {
  position: absolute;
  bottom: 100%;       /* above the element */
  left: 50%;
  transform: translateX(-50%); /* center horizontally */
  white-space: nowrap;
  pointer-events: none;
}
```

## Gotchas

- `z-index` on a flex/grid child works without explicit `position` (flex/grid items create stacking contexts)
- `position: sticky` requires the parent to have scrollable overflow and enough height; won't work if parent has `overflow: hidden`
- `transform` on a parent creates a new containing block, breaking `position: fixed` children (they become relative to the transform container, not the viewport)
- Stacking context isolation: `isolation: isolate` creates a stacking context without side effects - useful for component encapsulation
- `position: absolute` with `inset: 0` + `margin: auto` + explicit `width`/`height` = centered element (works alongside the flexbox centering approach)

## See Also

- [MDN: position](https://developer.mozilla.org/en-US/docs/Web/CSS/position)
- [MDN: Stacking context](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_positioned_layout/Understanding_z-index/Stacking_context)
