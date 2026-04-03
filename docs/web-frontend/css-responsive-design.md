---
title: CSS Responsive Design
category: concepts
tags: [web-frontend, css, responsive, media-queries, mobile-first]
---

# CSS Responsive Design

One codebase adapts to all screen sizes. ~60% of web traffic is mobile; Google ranks mobile-first.

## Viewport Meta Tag

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

**Must be in every responsive page.** Without it, mobile browsers render at ~980px width and zoom out.

## Media Queries

```css
/* Mobile-first (recommended) */
.container { padding: 16px; }

@media (min-width: 768px) {
  .container { padding: 32px; }
}
@media (min-width: 1024px) {
  .container { padding: 64px; max-width: 1200px; margin: 0 auto; }
}
```

### Syntax
```css
@media screen and (min-width: 768px) { }
@media (max-width: 767px) { }
@media (min-width: 768px) and (max-width: 1023px) { }
@media (orientation: landscape) { }
@media (prefers-color-scheme: dark) { }
@media (prefers-reduced-motion: reduce) { }
@media (hover: hover) { }        /* Has hover capability */
@media (pointer: coarse) { }     /* Touch screen */

/* Modern range syntax (Level 4) */
@media (768px <= width <= 1024px) { }
```

### Common Breakpoints
| Breakpoint | Target |
|-----------|--------|
| 375px | iPhone SE/12 mini |
| 768px | Tablets |
| 1024px | Small laptops |
| 1200px | Desktop |
| 1440px | Large desktop |

### Mobile-First vs Desktop-First
**Mobile-first** (`min-width`): progressive enhancement, smaller CSS for mobile, forces content prioritization. Recommended.

**Desktop-first** (`max-width`): override down. Older approach.

## Viewport Units

```css
width: 100vw;        /* 100% viewport width */
height: 100dvh;      /* Dynamic viewport height (mobile-friendly) */
height: 100svh;      /* Small viewport (bar visible) */
height: 100lvh;      /* Large viewport (bar hidden) */
```

**Problem with `100vh` on mobile**: mobile browser address bar appears/disappears, causing overflow. Use `100dvh` for full-screen mobile sections.

## Fluid Typography with clamp()

```css
h1 { font-size: clamp(1.5rem, 4vw, 3rem); }
p  { font-size: clamp(1rem, 1rem + 0.5vw, 1.25rem); }
```

- **min**: accessibility floor (never below)
- **preferred**: scales with viewport
- **max**: readability cap (never above)
- Eliminates media queries for font sizes in most cases

## calc(), min(), max()

```css
width: calc(100% - 40px);        /* Mixed unit arithmetic */
width: min(100%, 800px);          /* Full width, max 800px */
width: max(300px, 50%);           /* At least 300px */
padding: clamp(16px, 4vw, 64px);
```

**calc() requires spaces** around operators: `calc(100% - 20px)` not `calc(100%-20px)`.

## Responsive Images

```html
<img src="photo.jpg" alt="..." style="max-width: 100%; height: auto;">

<!-- Art direction -->
<picture>
  <source media="(min-width: 1024px)" srcset="photo-desktop.jpg">
  <source media="(min-width: 768px)" srcset="photo-tablet.jpg">
  <img src="photo-mobile.jpg" alt="Description">
</picture>

<!-- Resolution switching -->
<img src="photo-400.jpg"
     srcset="photo-400.jpg 400w, photo-800.jpg 800w, photo-1200.jpg 1200w"
     sizes="(max-width: 600px) 100vw, (max-width: 1200px) 50vw, 600px"
     alt="Description">
```

### object-fit
```css
.card-image {
  width: 100%; height: 200px;
  object-fit: cover;          /* Fill + crop (like background-size: cover) */
  object-position: center;
}
```

| Value | Behavior |
|-------|----------|
| `fill` | Stretches (distorts) |
| `contain` | Fits, preserves ratio (may letterbox) |
| `cover` | Fills + crops, preserves ratio |
| `none` | Original size |

## Layout Patterns

### Container with Max-Width
```css
.container {
  width: 100%; max-width: 1200px;
  margin: 0 auto; padding: 0 16px;
}
```

### Responsive Grid (No Media Queries)
```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
}
```

### Hamburger Menu
```css
.nav-links { display: flex; gap: 24px; }
.hamburger { display: none; }

@media (max-width: 768px) {
  .nav-links { display: none; }
  .nav-links.active {
    display: flex; position: fixed;
    inset: 0; flex-direction: column;
    justify-content: center; align-items: center;
  }
  .hamburger { display: block; }
}
```

## Gotchas

- **Missing viewport meta**: everything renders tiny on mobile
- **`100vh` on mobile**: address bar causes overflow, use `100dvh`
- **`:hover` on touch**: hover effects don't work; use `@media (hover: hover)` for hover-only styles
- **Testing only at standard breakpoints**: resize slowly to find where layout actually breaks
- **`vw` causing horizontal scroll**: `100vw` includes scrollbar width; use `100%` for container width

## See Also

- [[css-grid]] - Auto-responsive grid patterns
- [[css-flexbox]] - Responsive wrapping with flex
- [[css-box-model-and-layout]] - Viewport units, sizing
- [[figma-design-workflow]] - Designing for multiple breakpoints
