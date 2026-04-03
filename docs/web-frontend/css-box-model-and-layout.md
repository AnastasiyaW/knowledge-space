---
title: CSS Box Model and Layout
category: concepts
tags: [web-frontend, css, box-model, position, units]
---

# CSS Box Model and Layout

Every HTML element is a rectangular box with four layers. Understanding the box model, display, position, and units is foundational for all CSS layout.

## Box Model

```
┌────────── Margin ──────────┐
│  ┌──────── Border ──────┐  │
│  │  ┌──── Padding ────┐ │  │
│  │  │  Content area    │ │  │
│  │  └─────────────────┘ │  │
│  └──────────────────────┘  │
└────────────────────────────┘
```

### border-box (Always Use)
```css
*, *::before, *::after { box-sizing: border-box; }
```

| Box-sizing | `width: 200px; padding: 20px; border: 2px` |
|-----------|---------------------------------------------|
| `content-box` (default) | Total = 244px |
| `border-box` | Total = 200px (content shrinks to 156px) |

## Width and Height

```css
width: 300px;  width: 50%;  width: auto;
min-width: 200px;  max-width: 800px;
height: 100px;  min-height: 100vh;
overflow: visible | hidden | scroll | auto;
overflow-x: auto;  overflow-y: auto;
```

**Gotcha**: Percentage `height` only works if parent has explicit height. Percentage `width` always works.

## Padding

```css
padding: 20px;                   /* All sides */
padding: 10px 20px;             /* Vertical | Horizontal */
padding: 10px 20px 15px 25px;   /* Top Right Bottom Left (clockwise) */
```

- Cannot be negative
- Background extends through padding
- Percentage padding is relative to parent's WIDTH (even top/bottom)

## Border

```css
border: 1px solid #333;
border-radius: 8px;             /* Rounded corners */
border-radius: 50%;             /* Perfect circle (square element) */
outline: 2px solid blue;        /* Outside box model, no layout impact */
outline-offset: 4px;
```

**Border vs Outline**: border takes space in box model, outline doesn't. Outline is used for focus indicators.

## Margin

```css
margin: 20px;
margin: 0 auto;                 /* Center block horizontally (requires width) */
margin-top: -20px;              /* Negative margins pull element */
```

### Margin Collapsing
Adjacent vertical margins merge - only the larger one applies:
```css
.top    { margin-bottom: 30px; }
.bottom { margin-top: 20px; }
/* Gap = 30px, NOT 50px */
```

- Only vertical margins collapse (not horizontal)
- Does NOT happen inside flex/grid containers
- Does NOT happen when padding/border separates parent-child margins

## Display

```css
display: block;          /* Full width, new line */
display: inline;         /* Flows with text, ignores width/height */
display: inline-block;   /* Inline flow + respects width/height */
display: none;           /* Removed from layout entirely */
display: flex;           /* Flex container */
display: grid;           /* Grid container */
```

`display: none` removes from layout. `visibility: hidden` hides but keeps space.

## Position

```css
position: static;     /* Default: normal flow */
position: relative;   /* Offset from normal position, still takes space */
position: absolute;   /* Removed from flow, relative to nearest positioned ancestor */
position: fixed;      /* Relative to viewport, stays on scroll */
position: sticky;     /* Normal until scroll threshold, then fixed */
```

### Relative + Absolute Pattern
```css
.parent { position: relative; }   /* Establishes context */
.child  { position: absolute; top: 0; right: 0; }  /* Positioned within parent */
```

### Sticky
```css
.nav { position: sticky; top: 0; z-index: 100; }
```
Requires `top`/`bottom` value. Only works within its containing block.

### z-index
Only works on positioned elements (not `static`). Common scale: content 0, headers 100, dropdowns 200, modals 1000, toasts 2000.

## Float (Legacy)

```css
.image { float: left; }   /* Text wraps around */
.container::after { content: ""; display: table; clear: both; }  /* Clearfix */
```

Float is legacy for layout. Use Flexbox/Grid. Float remains useful for text wrapping around images.

## CSS Units

### Relative Units
| Unit | Relative To | Use |
|------|-------------|-----|
| `rem` | Root font-size (16px default) | Font sizes, spacing (preferred) |
| `em` | Parent font-size (for font-size) / own font-size (other) | Spacing relative to text |
| `%` | Parent property | Widths, padding |
| `vw`/`vh` | 1% viewport width/height | Full-width/height |
| `dvh` | Dynamic viewport height | Mobile full-height (accounts for browser bar) |
| `ch` | Width of "0" character | Input field widths |

### Practical Recommendations
- **Font sizes**: `rem` (consistent, accessible, scales with user preference)
- **Spacing**: `rem` or `px`
- **Widths**: `%` for fluid, `max-width` for constraints
- **Heights**: avoid fixed, use `min-height`
- **Mobile full-height**: `100dvh` (not `100vh` which ignores mobile browser bar)

### em vs rem
```css
html { font-size: 16px; }
.parent { font-size: 20px; }
.child {
  font-size: 1.5em;    /* 30px (1.5 * parent's 20px) */
  font-size: 1.5rem;   /* 24px (1.5 * root's 16px) */
  padding: 1em;        /* relative to element's OWN font-size */
}
```

## Background

```css
background: #f5f5f5 url('image.jpg') no-repeat center/cover;

/* Multiple backgrounds with dark overlay */
background:
  linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)),
  url('image.jpg') center/cover;

/* Gradients */
background: linear-gradient(135deg, #667eea, #764ba2);
background: radial-gradient(circle, #3b82f6, transparent);
```

`background-size: cover` fills and crops. `contain` fits entirely.

## Gotchas

- **Forgetting `border-box`**: elements larger than expected
- **`100vh` on mobile**: overflows because it ignores the address bar, use `100dvh`
- **Margin collapse surprises**: vertical margins between siblings merge
- **Percentage padding top/bottom**: relative to parent WIDTH, not height
- **`z-index` without position**: has no effect on `static` elements
- **`em` cascading**: `em` compounds through nested elements, `rem` stays consistent

## See Also

- [[css-flexbox]] - 1D layout system
- [[css-grid]] - 2D layout system
- [[css-responsive-design]] - Viewport units, media queries, fluid sizing
- [[css-selectors-and-cascade]] - Selecting elements to style
