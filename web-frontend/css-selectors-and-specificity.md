---
title: CSS Selectors and Specificity
category: css
tags: [css, selectors, specificity, cascade, pseudo-classes, pseudo-elements]
---

# CSS Selectors and Specificity

## Key Facts

- **Specificity** is calculated as (inline, IDs, classes/attrs/pseudo-classes, elements/pseudo-elements)
- `#id` = (0,1,0,0), `.class` = (0,0,1,0), `element` = (0,0,0,1), `*` = (0,0,0,0)
- `!important` overrides all specificity (avoid; use only for utility overrides)
- **Cascade order** (lowest to highest): user agent, author normal, author `!important`, inline styles
- `:is()` and `:where()` simplify compound selectors; `:where()` has zero specificity, `:is()` takes highest argument's specificity
- `:has()` is the "parent selector" - `article:has(img)` selects articles containing images
- `::before` and `::after` pseudo-elements create generated content (require `content` property)
- `[data-attr="value"]` attribute selectors match HTML attributes; `[href^="https"]` starts-with
- `:nth-child(2n)` selects even elements; `:nth-child(3n+1)` selects every 3rd starting from 1st
- Related: [[css-box-model-and-display]], [[css-custom-properties-and-animations]]

## Patterns

### Specificity Examples

```css
p { }                    /* 0,0,0,1 */
.card { }                /* 0,0,1,0 */
#header { }              /* 0,1,0,0 */
div.card.active { }      /* 0,0,2,1 */
#header .nav a:hover { } /* 0,1,1,2 -- pseudo-class counts as class */

/* :where() for zero-specificity defaults */
:where(.card, .panel) { border: 1px solid gray; }
/* Easy to override: .card { border: none; } wins */

/* :is() for grouping */
:is(h1, h2, h3) { font-weight: 700; }
```

### Modern Selectors

```css
/* :has() - parent/relational selector */
.card:has(img) { grid-template-rows: auto 1fr; }
.form:has(:invalid) .submit-btn { opacity: 0.5; }

/* :not() */
a:not([href^="#"]) { text-decoration: underline; }

/* :nth-child(of selector) */
li:nth-child(odd of .visible) { background: #f5f5f5; }
```

### Pseudo-Elements

```css
/* Custom bullet */
li::before {
  content: "\2022"; /* bullet character */
  color: var(--accent);
  margin-right: 0.5em;
}

/* Decorative line under heading */
h2::after {
  content: "";
  display: block;
  width: 3rem;
  height: 3px;
  background: var(--primary);
  margin-top: 0.5rem;
}
```

## Gotchas

- Specificity is not decimal: (0,0,11,0) does NOT beat (0,1,0,0) - one ID always beats any number of classes
- `:nth-child()` counts ALL siblings, not just matching ones; use `:nth-child(n of .selector)` or `:nth-of-type()` for type-specific counting
- `::before`/`::after` don't work on replaced elements (`<img>`, `<input>`, `<br>`)
- `:has()` is expensive for rendering; avoid deeply nested selectors like `body:has(.x .y .z)`
- CSS custom properties (variables) do NOT contribute to specificity; the selector they're used in does

## See Also

- [MDN: Specificity](https://developer.mozilla.org/en-US/docs/Web/CSS/Specificity)
- [MDN: CSS selectors](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_selectors)
