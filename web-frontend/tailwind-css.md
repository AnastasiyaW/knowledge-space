---
title: Tailwind CSS
category: css-framework
tags: [tailwind, utility-first, responsive, design-system, css-framework]
---

# Tailwind CSS

## Key Facts

- **Utility-first** CSS framework: compose styles from atomic classes (`flex`, `p-4`, `text-lg`, `bg-blue-500`)
- Generates only the CSS classes actually used in your code (tree-shaking via content scanning)
- Responsive prefixes: `sm:`, `md:`, `lg:`, `xl:`, `2xl:` - mobile-first (apply at breakpoint and up)
- State prefixes: `hover:`, `focus:`, `active:`, `disabled:`, `group-hover:`, `dark:`
- Spacing scale: `p-1` = 0.25rem (4px), `p-2` = 0.5rem, `p-4` = 1rem, `p-8` = 2rem
- `@apply` directive inlines utility classes into custom CSS (use sparingly - defeats utility-first purpose)
- Tailwind v4 uses CSS-first configuration (no `tailwind.config.js`); v3 uses JS config
- **Arbitrary values**: `w-[350px]`, `bg-[#1a2b3c]`, `grid-cols-[200px_1fr]` for one-off values
- `cn()` utility (clsx + tailwind-merge) for conditional class merging in React components
- Related: [[css-flexbox]], [[css-grid-layout]], [[responsive-design-and-media-queries]]

## Patterns

### Common Layout Patterns

```html
<!-- Centered container -->
<div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">

<!-- Flex row, centered, gap -->
<div class="flex items-center justify-between gap-4">

<!-- Grid responsive -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">

<!-- Full-height page with sticky footer -->
<div class="flex min-h-screen flex-col">
  <header>...</header>
  <main class="flex-1">...</main>
  <footer>...</footer>
</div>
```

### Card Component

```html
<div class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm
            transition-shadow hover:shadow-md dark:border-gray-700 dark:bg-gray-800">
  <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Title</h3>
  <p class="mt-2 text-sm text-gray-600 dark:text-gray-300">Description</p>
  <button class="mt-4 rounded-md bg-blue-600 px-4 py-2 text-sm font-medium
                  text-white hover:bg-blue-700 focus:outline-none focus:ring-2
                  focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50">
    Action
  </button>
</div>
```

### Conditional Classes in React (cn utility)

```tsx
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// Usage
function Badge({ variant = "default", children }: BadgeProps) {
  return (
    <span className={cn(
      "inline-flex items-center rounded-full px-2 py-1 text-xs font-medium",
      variant === "success" && "bg-green-100 text-green-700",
      variant === "error" && "bg-red-100 text-red-700",
      variant === "default" && "bg-gray-100 text-gray-700",
    )}>
      {children}
    </span>
  );
}
```

### Dark Mode

```html
<!-- With class strategy (tailwind.config.js: darkMode: "class") -->
<html class="dark">
  <body class="bg-white text-gray-900 dark:bg-gray-900 dark:text-gray-100">
    ...
  </body>
</html>

<!-- Toggle in React -->
<script>
document.documentElement.classList.toggle("dark");
</script>
```

## Gotchas

- Tailwind classes are scanned from source files; dynamically constructed class names (`text-${color}-500`) won't be detected - use full class names or safelist
- `@apply` inside component styles breaks the utility-first model; prefer `cn()` for conditional classes
- Tailwind spacing is in `rem` (relative to root font-size); changing root font-size scales everything
- `tailwind-merge` resolves conflicting classes: `cn("p-4", "p-6")` = `"p-6"` (last wins); without it, both apply and result is unpredictable
- Tailwind v4 migration: config moves from `tailwind.config.js` to CSS `@theme` block; plugins use CSS instead of JS

## See Also

- [Tailwind CSS: Documentation](https://tailwindcss.com/docs)
- [Tailwind CSS: Customization](https://tailwindcss.com/docs/configuration)
