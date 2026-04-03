---
title: CSS Custom Properties and Animations
category: css
tags: [css, custom-properties, css-variables, animations, transitions, keyframes]
---

# CSS Custom Properties and Animations

## Key Facts

- **CSS Custom Properties** (variables): declared with `--name`, used with `var(--name, fallback)`
- Defined on any selector; `:root` for global scope, component selector for local scope
- Custom properties cascade and inherit; can be overridden per-element or via media queries
- **Transitions**: animate between two states on property change; `transition: property duration timing-function delay`
- **Animations**: multi-step, auto-playing; defined with `@keyframes` and applied with `animation` shorthand
- `transition` only animates properties that have a numeric interpolation path (color, opacity, transform - yes; display - no)
- `will-change: transform` hints browser to GPU-accelerate; use sparingly (memory cost)
- `prefers-reduced-motion` media query must be respected: disable/reduce animations for accessibility
- `transform` and `opacity` are the only properties that can be animated without triggering layout reflow
- Related: [[css-selectors-and-specificity]], [[css-box-model-and-display]]

## Patterns

### Design Tokens as Custom Properties

```css
:root {
  /* Colors */
  --color-primary: #2563eb;
  --color-primary-hover: #1d4ed8;
  --color-text: #1f2937;
  --color-bg: #ffffff;

  /* Spacing */
  --space-xs: 0.25rem;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 2rem;

  /* Typography */
  --font-sans: system-ui, -apple-system, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}

/* Dark mode override */
@media (prefers-color-scheme: dark) {
  :root {
    --color-text: #f3f4f6;
    --color-bg: #111827;
  }
}
```

### Transition on Hover

```css
.button {
  background: var(--color-primary);
  color: white;
  transition: background 200ms ease, transform 150ms ease;
}
.button:hover {
  background: var(--color-primary-hover);
  transform: translateY(-1px);
}
.button:active {
  transform: translateY(0);
}
```

### Keyframe Animation

```css
@keyframes fade-in {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}

.card {
  animation: fade-in 300ms ease-out forwards;
}

/* Staggered animation with custom property */
.card:nth-child(1) { --delay: 0ms; }
.card:nth-child(2) { --delay: 100ms; }
.card:nth-child(3) { --delay: 200ms; }
.card { animation-delay: var(--delay, 0ms); }
```

### Accessible Motion

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Gotchas

- Custom properties are NOT static preprocessor variables; they're live, cascade-aware, and can change at runtime (e.g., via JS or hover)
- `var(--undefined)` without fallback resolves to `initial` keyword, not blank; always provide fallback for optional props
- `transition: all` triggers transitions on every changed property, including ones you don't intend; list properties explicitly
- `height: auto` cannot be transitioned directly; use `max-height` with a generous value, or `grid-template-rows: 0fr/1fr` trick
- Animating `width`/`height`/`top`/`left` causes layout recalculation (reflow) every frame; use `transform: translate()/scale()` instead

## See Also

- [MDN: Custom properties](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties)
- [MDN: CSS Animations](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_animations)
