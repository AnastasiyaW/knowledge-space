---
title: Responsive Design and Media Queries
category: css
tags: [responsive, media-queries, mobile-first, viewport, breakpoints, clamp]
---

# Responsive Design and Media Queries

## Key Facts

- **Mobile-first**: write base styles for small screens, add `@media (min-width: ...)` for larger screens
- `<meta name="viewport" content="width=device-width, initial-scale=1.0">` is mandatory for responsive sites
- Common breakpoints: 480px (mobile), 768px (tablet), 1024px (desktop), 1440px (large desktop)
- `@media (min-width: 768px)` = tablet and up (mobile-first); `@media (max-width: 767px)` = mobile only (desktop-first)
- **Container queries** (`@container`) size elements based on parent container, not viewport
- `clamp(min, preferred, max)` creates fluid typography/spacing without media queries
- `rem` for font sizes (relative to root), `em` for component-internal spacing, `%`/`vw` for widths
- `srcset` and `sizes` on `<img>` serve different image resolutions based on viewport
- `aspect-ratio` CSS property maintains proportions without padding hacks
- Related: [[css-flexbox]], [[css-grid-layout]], [[html-semantics-and-document-structure]]

## Patterns

### Mobile-First Breakpoints

```css
/* Base: mobile */
.container { padding: 1rem; }
.grid { display: flex; flex-direction: column; gap: 1rem; }

/* Tablet */
@media (min-width: 768px) {
  .container { padding: 2rem; }
  .grid { flex-direction: row; flex-wrap: wrap; }
  .grid > * { flex: 1 1 calc(50% - 0.5rem); }
}

/* Desktop */
@media (min-width: 1024px) {
  .container { max-width: 1200px; margin-inline: auto; }
  .grid > * { flex: 1 1 calc(33.333% - 0.667rem); }
}
```

### Fluid Typography with clamp()

```css
h1 { font-size: clamp(1.5rem, 4vw, 3rem); }
/* min 1.5rem, scales with viewport, max 3rem */

p { font-size: clamp(1rem, 2vw + 0.5rem, 1.25rem); }
```

### Responsive Images

```html
<img
  src="photo-800.jpg"
  srcset="photo-400.jpg 400w, photo-800.jpg 800w, photo-1200.jpg 1200w"
  sizes="(max-width: 600px) 100vw, (max-width: 1000px) 50vw, 33vw"
  alt="Product photo"
>

<!-- Art direction with <picture> -->
<picture>
  <source media="(min-width: 800px)" srcset="landscape.jpg">
  <source media="(min-width: 400px)" srcset="square.jpg">
  <img src="portrait.jpg" alt="Responsive image">
</picture>
```

### Container Queries

```css
.card-container {
  container-type: inline-size;
  container-name: card;
}

@container card (min-width: 400px) {
  .card { flex-direction: row; }
  .card-image { width: 40%; }
}
```

## Gotchas

- `@media (hover: hover)` detects devices with actual hover capability; use for hover-only effects to avoid "stuck hover" on touch devices
- `100vh` on mobile includes the browser address bar; use `100dvh` (dynamic viewport height) for true visible area
- `vw` includes scrollbar width, causing horizontal overflow; use `100%` of body or `calc(100vw - scrollbar)` alternatively
- `clamp()` fallback not needed for modern browsers but requires a static fallback for IE11 if supporting
- `prefers-reduced-motion: reduce` media query should disable animations for accessibility

## See Also

- [MDN: Responsive design](https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Responsive_Design)
- [MDN: Container queries](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries)
