---
title: CSS Selectors and Cascade
category: concepts
tags: [web-frontend, css, selectors, specificity, variables]
---

# CSS Selectors and Cascade

CSS controls presentation of HTML. The cascade, specificity, and inheritance determine which styles win when multiple rules target the same element.

## Connecting CSS

```html
<link rel="stylesheet" href="css/style.css">   <!-- External (preferred, cacheable) -->
<style>p { color: red; }</style>                 <!-- Internal (in <head>) -->
<p style="color: red;">Text</p>                  <!-- Inline (highest specificity) -->
```

## Selectors

### Basic
```css
*         { }    /* Universal */
p         { }    /* Type */
.card     { }    /* Class */
#header   { }    /* ID (avoid for styling) */
```

### Attribute
```css
[href]              { }    /* Has attribute */
[type="text"]       { }    /* Exact value */
[href^="https"]     { }    /* Starts with */
[href$=".pdf"]      { }    /* Ends with */
[href*="example"]   { }    /* Contains */
[data-theme="dark" i] { }  /* Case-insensitive */
```

### Combinators
```css
div p       { }    /* Descendant (any depth) */
div > p     { }    /* Direct child */
h2 + p      { }    /* Adjacent sibling (immediately after) */
h2 ~ p      { }    /* General sibling (all after, same parent) */
```

### Pseudo-classes (State)
```css
a:hover       { }    a:active      { }    a:visited     { }
a:focus       { }    a:focus-visible { }   /* Keyboard focus only */
input:valid   { }    input:invalid { }    input:required  { }
input:disabled { }   input:checked { }    input:placeholder-shown { }
:empty        { }    :target       { }    :root          { }
```

### Structural Pseudo-classes
```css
:first-child    { }    :last-child     { }
:nth-child(2)   { }    :nth-child(odd) { }    :nth-child(3n+1) { }
:nth-last-child(2) { } :only-child     { }
:first-of-type  { }    :nth-of-type(2) { }    :only-of-type   { }
```

**Key difference**: `:nth-child` counts ALL children. `:nth-of-type` counts only same-tag elements.

### Negation and Logical
```css
:not(.hidden)     { }    /* Exclude matching */
:is(h1, h2, h3)  { }    /* Match any (forgiving selector list) */
:where(h1, h2)   { }    /* Like :is() but zero specificity */
:has(.icon)       { }    /* Parent selector - element containing .icon */
```

`:has()` is the long-awaited "parent selector" - e.g., `.card:has(img)` selects cards containing an image.

### Pseudo-elements
```css
p::first-line    { }    p::first-letter  { }
p::selection     { }    p::placeholder   { }
.item::before { content: ">> "; }
.item::after  { content: ""; display: block; }
```

`::before`/`::after` MUST have `content` property. They are inline by default, cannot be applied to void elements (`<img>`, `<input>`).

## Cascade (Conflict Resolution)

1. **Origin and importance**: `!important` > author styles > browser defaults
2. **Specificity**: more specific selector wins
3. **Source order**: last rule wins (equal specificity)

## Specificity

| Selector Type | Weight |
|--------------|--------|
| Inline style | 1,0,0,0 |
| ID `#id` | 0,1,0,0 |
| Class `.class`, `[attr]`, `:pseudo-class` | 0,0,1,0 |
| Element `div`, `::pseudo-element` | 0,0,0,1 |
| Universal `*`, combinators | 0,0,0,0 |

```css
p                    /* 0,0,0,1 */
.card                /* 0,0,1,0 */
#header .nav li a    /* 0,1,1,2 */
div > p.text:hover   /* 0,0,2,2 */
```

Higher specificity ALWAYS wins regardless of source order. Avoid `!important` - it breaks the cascade.

## Inheritance

**Inherited**: `color`, `font-*`, `line-height`, `text-align`, `visibility`, `cursor`, `list-style`
**NOT inherited**: `margin`, `padding`, `border`, `background`, `width`, `height`, `display`, `position`

```css
.child { color: inherit; }   /* Force inheritance */
.element { all: unset; }     /* Reset to browser default */
```

## Colors

```css
color: #ff0000;                  /* Hex */
color: #f00;                     /* Hex shorthand */
color: rgb(255, 0, 0);          /* RGB */
color: rgba(255, 0, 0, 0.5);    /* RGBA */
color: hsl(0, 100%, 50%);       /* HSL (most intuitive) */
color: hsla(0, 100%, 50%, 0.5);
```

**HSL advantage**: H = color wheel (0-360), S = saturation (0-100%), L = lightness (0-100%). Darken = decrease L. Lighten = increase L. Desaturate = decrease S. All predictable.

`currentColor` keyword inherits text color - useful for borders and SVG fills.

## Text and Font Properties

```css
font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif;
font-size: 1rem;              /* Relative to root (preferred) */
font-weight: 400;             /* Normal=400, Bold=700 */
line-height: 1.5;             /* Unitless multiplier (preferred) */
text-align: left | center | right | justify;
text-decoration: underline wavy red;
text-transform: uppercase | lowercase | capitalize;
letter-spacing: 0.05em;
white-space: nowrap; overflow: hidden; text-overflow: ellipsis;  /* Truncation */
font: italic 700 16px/1.5 'Inter', sans-serif;  /* Shorthand */
```

### Custom Fonts
```css
@font-face {
  font-family: 'MyFont';
  src: url('fonts/myfont.woff2') format('woff2');
  font-weight: 400;
  font-display: swap;  /* Show fallback immediately, swap when loaded */
}
```

WOFF2 is best compression for modern browsers. `font-display: swap` prevents invisible text during loading.

## CSS Custom Properties

```css
:root {
  --color-primary: #3b82f6;
  --spacing-md: 16px;
  --border-radius: 8px;
}
.button {
  background: var(--color-primary);
  padding: var(--spacing-md);
  border-radius: var(--border-radius);
  font-size: var(--font-size-base, 14px);  /* Fallback value */
}
```

- Scoped: `:root` = global, element = local scope
- Cascade and inherit like regular properties
- Dynamic via JS: `element.style.setProperty('--color', 'red')`
- Unlike SASS variables, CSS variables are live and cascade

## Gotchas

- **`!important` overuse**: creates maintenance nightmares, hard to override
- **ID selectors for styling**: too specific, prefer classes
- **`:nth-child` vs `:nth-of-type`**: counting includes ALL siblings vs same-type only
- **`em` cascading**: `em` for font-size = relative to parent; for other properties = relative to element's own font-size
- **Percentage height**: only works if parent has explicit height

## See Also

- [[css-box-model-and-layout]] - Display, position, units
- [[css-sass-and-methodology]] - BEM naming, SASS preprocessing
- [[html-fundamentals]] - HTML elements that CSS targets
