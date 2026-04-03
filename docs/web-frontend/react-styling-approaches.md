---
title: React Styling Approaches
category: concepts
tags: [web-frontend, react, css-modules, tailwind, styling]
---

# React Styling Approaches

Two dominant patterns for styling React: CSS Modules (scoped traditional CSS) and Tailwind CSS (utility-first). Both work out of the box with Vite.

## CSS Modules

Locally-scoped class names - auto-generated unique suffixes prevent conflicts.

### File Convention
```
components/Header/
  Header.jsx
  Header.module.css       # Must include .module.css
```

### Usage
```css
/* Header.module.css */
.header { background: #1a1a1a; padding: 16px; }
.title { color: white; font-size: 24px; }
```

```jsx
import styles from './Header.module.css';

function Header() {
  return (
    <header className={styles.header}>
      <h1 className={styles.title}>My App</h1>
    </header>
  );
}
```

Import returns object: `{ header: "Header_header_x7d3f", title: "Header_title_k9m2p" }`.

### Multiple Classes
```jsx
<div className={`${styles.card} ${styles.active}`}>
// With classnames library
import cn from 'classnames';
<div className={cn(styles.card, { [styles.active]: isActive })}>
```

## Tailwind CSS

Utility-first: compose designs from single-purpose classes.

### Setup
```bash
npm install -D tailwindcss @tailwindcss/vite
```
```js
// vite.config.js
import tailwindcss from '@tailwindcss/vite';
export default { plugins: [tailwindcss()] };
```
```css
/* index.css */
@import "tailwindcss";
```

### Core Utilities

**Spacing** (1 unit = 4px):
```html
<div class="p-4 px-6 py-2 m-auto mt-8 space-y-4">
```

**Typography**:
```html
<p class="text-lg font-bold text-gray-700 text-center leading-relaxed uppercase truncate">
```

**Colors**: `{property}-{color}-{shade}` - shades 50 (light) to 950 (dark):
```html
<div class="bg-blue-500 text-white border-gray-300">
```

**Layout**:
```html
<div class="flex items-center justify-between gap-4">
<div class="grid grid-cols-3 gap-6">
<div class="w-full max-w-md mx-auto hidden md:block">
```

**Borders/Shadows**:
```html
<div class="border border-gray-300 rounded-lg shadow-md hover:shadow-lg ring-2 ring-blue-500">
```

### Responsive (mobile-first)
```html
<div class="text-sm md:text-base lg:text-lg">
<div class="flex-col md:flex-row">
<div class="grid-cols-1 sm:grid-cols-2 lg:grid-cols-4">
```

| Prefix | Min-width |
|--------|-----------|
| (none) | 0 (mobile) |
| `sm:` | 640px |
| `md:` | 768px |
| `lg:` | 1024px |
| `xl:` | 1280px |

### States
```html
<button class="bg-blue-500 hover:bg-blue-600 active:bg-blue-700 focus:ring-2">
<tr class="odd:bg-white even:bg-gray-50">
```

### group and peer
```html
<!-- Style child on parent hover -->
<div class="group">
  <img class="group-hover:scale-105 transition" />
</div>

<!-- Style sibling on sibling state -->
<input class="peer" type="checkbox" />
<label class="peer-checked:text-blue-500">Option</label>
```

### Animations
```html
<div class="transition duration-300 ease-in-out hover:scale-105">
<div class="animate-spin">   <!-- Built-in -->
<div class="animate-pulse">  <!-- Skeleton loading -->
```

### Arbitrary Values
```html
<div class="w-[300px] bg-[#1a1a2e] grid-cols-[200px_1fr_200px]">
```

### @apply (Extract Patterns)
```css
.btn-primary {
  @apply px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition;
}
```

Use sparingly - overuse defeats utility-first purpose.

### Dark Mode
```html
<div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100">
```

## Comparison

| Aspect | CSS Modules | Tailwind |
|--------|-------------|----------|
| Approach | Traditional CSS, separate files | Utility classes in JSX |
| Bundle | All written CSS | Purged to used only |
| Learning | Know CSS already | Learn utility names |
| Co-location | Separate .module.css | In component file |
| Design consistency | Manual discipline | Enforced by utility scale |
| Readability | Clean JSX | Dense class strings |

Both are valid. Many teams use Tailwind for rapid development and CSS Modules for complex custom components.

## Gotchas

- **CSS Modules global styles**: use `:global(.class)` or separate non-module CSS file
- **Tailwind purge**: classes must be complete strings, not constructed: `bg-${color}-500` won't work
- **Tailwind specificity**: utilities have same specificity; later class wins (order matters)
- **CSS Modules verbose multi-class**: template literals get messy; use `classnames` library
- **Dynamic Tailwind**: use ternary for conditional classes: `isActive ? "bg-blue-500" : "bg-gray-500"`

## See Also

- [[css-sass-and-methodology]] - BEM, SASS as alternative approaches
- [[css-flexbox]] - Flexbox that Tailwind utilities map to
- [[css-grid]] - Grid utilities in Tailwind
- [[react-components-and-jsx]] - Component structure
