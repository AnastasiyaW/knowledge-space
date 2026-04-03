---
title: CSS Methodology and SASS
category: concepts
tags: [web-frontend, css, bem, sass, scss, architecture]
---

# CSS Methodology and SASS

Without methodology, CSS becomes unmaintainable: fragile specificity chains, inconsistent naming, unpredictable cascading. BEM + SASS solve this at scale.

## BEM (Block Element Modifier)

### Structure
```
.block            - standalone component
.block__element   - part of block (child)
.block--modifier  - variant of block or element
```

### Examples
```css
.card { }
.card__title { }
.card__image { }
.card--featured { }
.card--dark { }
.button { }
.button--large { }
.button--disabled { }
```

```html
<div class="card card--featured">
  <img class="card__image" src="...">
  <h3 class="card__title">Title</h3>
  <button class="button button--large">Read more</button>
</div>
```

### BEM Rules
1. **Flat selectors**: `.card__title` not `.card .title` - consistent specificity
2. **No element of element**: `.card__footer__button` is wrong - make new block or `.card__action`
3. **Modifiers need base**: `class="button button--large"` not `class="button--large"` alone
4. **Blocks are location-independent**: styles don't depend on where block is placed

### Benefits
- All classes = `0,0,1,0` specificity (flat, predictable)
- Self-documenting: class name tells component and role
- Safe to move/copy blocks between pages

## SMACSS Categories

| Category | Prefix | Example |
|----------|--------|---------|
| Base | none | `html, body { margin: 0; }` |
| Layout | `l-` | `.l-header`, `.l-sidebar` |
| Module | none | `.card`, `.nav` |
| State | `is-` | `.is-hidden`, `.is-active` |
| Theme | `theme-` | `.theme-dark` |

## File Organization

```
css/
  global.css         - Reset, variables, base element styles
  layout.css         - Page-level layout
  components/
    card.css
    button.css
    form.css
  utils.css          - .hidden, .sr-only, .text-center
```

### Modern Reset
```css
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { font-size: 16px; -webkit-font-smoothing: antialiased; }
img, picture, video, canvas, svg { display: block; max-width: 100%; }
input, button, textarea, select { font: inherit; }
```

## SASS/SCSS

CSS preprocessor that compiles to regular CSS. SCSS syntax (`.scss`) is CSS-compatible.

### Variables
```scss
$color-primary: #3b82f6;
$font-body: 'Inter', sans-serif;
$breakpoint-tablet: 768px;

.button {
  background: $color-primary;
  font-family: $font-body;
}
```

SASS variables are compile-time. For runtime, use CSS custom properties.

### Nesting (BEM Pattern)
```scss
.nav {
  display: flex;

  &__item {                /* .nav__item */
    padding: 8px 16px;

    &--active {            /* .nav__item--active */
      color: $color-primary;
    }
    &:hover {              /* .nav__item:hover */
      background: #f5f5f5;
    }
  }
}
```

**Rule**: Don't nest deeper than 3 levels.

### Mixins
```scss
@mixin flex-center {
  display: flex; justify-content: center; align-items: center;
}

@mixin responsive($breakpoint) {
  @media (min-width: $breakpoint) { @content; }
}

@mixin button-variant($bg, $color: white) {
  background: $bg; color: $color;
  &:hover { background: darken($bg, 10%); }
}

.hero { @include flex-center; min-height: 100vh; }
.sidebar {
  display: none;
  @include responsive(768px) { display: block; width: 250px; }
}
.btn-primary { @include button-variant(#3b82f6); }
.btn-danger  { @include button-variant(#ef4444); }
```

### Extend / Placeholder
```scss
%card-base {
  border-radius: 8px; padding: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.card  { @extend %card-base; }
.modal { @extend %card-base; }
```

Prefer `@mixin` in most cases - `@extend` can produce unexpected CSS.

### Functions
```scss
@function rem($px) {
  @return ($px / 16) * 1rem;
}
.title { font-size: rem(24); }    /* 1.5rem */
```

Built-in: `darken()`, `lighten()`, `saturate()`, `mix()`, `rgba()`.

### Partials and @use
```scss
// _variables.scss
$color-primary: #3b82f6;

// main.scss
@use 'variables' as vars;
.button { background: vars.$color-primary; }
```

`@use` (namespaced, compiles once) replaces deprecated `@import` (global, compiles each time).

### Loops and Conditionals
```scss
@for $i from 1 through 12 {
  .col-#{$i} { width: (100% / 12) * $i; }
}

@each $color, $value in (primary: #3b82f6, danger: #ef4444) {
  .text-#{$color} { color: $value; }
  .bg-#{$color} { background: $value; }
}
```

## Advanced CSS Properties

```css
/* Clip to shape */
clip-path: circle(50%);
clip-path: polygon(50% 0%, 100% 100%, 0% 100%);  /* Triangle */

/* Blend modes */
mix-blend-mode: multiply;   /* Dark overlay */
mix-blend-mode: screen;     /* Light overlay */

/* Backdrop filter (glassmorphism) */
backdrop-filter: blur(10px) saturate(1.5);
```

## Gotchas

- **Deep nesting**: produces high-specificity selectors, hard to override
- **`@extend` pitfalls**: can create huge combined selectors with complex CSS
- **SASS vs CSS variables**: SASS variables disappear after compilation; CSS custom properties are live in browser
- **Element of element**: `.card__body__title` is a BEM anti-pattern - flatten or create new block
- **`@import` deprecated**: use `@use` with namespaces instead

## See Also

- [[css-selectors-and-cascade]] - Specificity and cascade rules
- [[react-styling-approaches]] - CSS Modules and Tailwind as alternatives
- [[frontend-build-systems]] - SASS compilation in build pipeline
