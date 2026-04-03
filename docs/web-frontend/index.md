---
title: Web & Frontend - Map of Content
category: index
tags: [moc, web, frontend, html, css, javascript, typescript, react, index]
---

# Web & Frontend

## HTML & CSS Fundamentals

- [[html-semantics-and-document-structure]] - semantic elements, accessibility, ARIA, document structure, meta tags
- [[css-box-model-and-display]] - box model, border-box reset, block/inline/inline-block, margin collapsing, logical properties
- [[css-selectors-and-specificity]] - specificity calculation, cascade, :has(), :is(), :where(), pseudo-elements
- [[css-custom-properties-and-animations]] - CSS variables, design tokens, transitions, @keyframes, prefers-reduced-motion

## CSS Layout

- [[css-flexbox]] - one-dimensional layout, justify-content, align-items, flex-grow/shrink/basis, gap
- [[css-grid-layout]] - two-dimensional layout, fr unit, auto-fit/auto-fill, grid-template-areas, subgrid
- [[css-positioning-and-z-index]] - static/relative/absolute/fixed/sticky, stacking contexts, modals, tooltips
- [[responsive-design-and-media-queries]] - mobile-first, breakpoints, clamp(), container queries, responsive images

## JavaScript

- [[javascript-fundamentals]] - let/const, types, destructuring, spread/rest, closures, optional chaining, arrow functions
- [[javascript-array-methods]] - map/filter/reduce, find, sort, toSorted (ES2023), groupBy (ES2024), iteration patterns
- [[javascript-async-and-promises]] - event loop, Promises, async/await, fetch, AbortController, Promise.all/allSettled
- [[javascript-dom-and-events]] - DOM manipulation, event delegation, bubbling, IntersectionObserver, debounce/throttle

## TypeScript

- [[typescript-type-system]] - interfaces, types, generics, utility types, type guards, discriminated unions
- [[typescript-advanced-patterns]] - mapped types, conditional types, template literals, infer, branded types, satisfies

## React Ecosystem

- [[react-components-and-jsx]] - JSX, function components, props, children, composition, conditional rendering, lists
- [[react-hooks]] - useState, useEffect, useRef, useMemo, useCallback, useReducer, custom hooks
- [[react-state-management]] - local state, lifted state, Context, Redux Toolkit, state decision matrix
- [[react-router-and-navigation]] - React Router v6, nested routes, params, protected routes, lazy loading

## Tooling & Frameworks

- [[tailwind-css]] - utility-first CSS, responsive prefixes, dark mode, cn() helper, arbitrary values
- [[webpack-and-vite]] - bundlers, code splitting, tree shaking, HMR, config, environment variables

## Design

- [[figma-design-to-code]] - auto layout to flexbox, design tokens, component mapping, responsive breakpoints

## Quick Reference: CSS Property Selection

| Goal | Property |
|------|----------|
| One-axis layout | `display: flex` |
| Two-axis layout | `display: grid` |
| Center anything | `display: grid; place-items: center` |
| Responsive grid | `grid-template-columns: repeat(auto-fit, minmax(250px, 1fr))` |
| Sticky header | `position: sticky; top: 0` |
| Fluid text | `font-size: clamp(1rem, 2.5vw, 2rem)` |
| Modal overlay | `position: fixed; inset: 0` |
| Spacing system | CSS custom properties + rem |

## Technology Stack Cheat Sheet

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Markup | HTML5 | Semantic structure |
| Styling | CSS3 / Tailwind | Visual presentation |
| Language | TypeScript | Type-safe JavaScript |
| UI Library | React 18+ | Component-based UI |
| Routing | React Router v6 | Client-side navigation |
| State | Redux Toolkit / Context | State management |
| Build | Vite | Dev server + bundling |
| Design | Figma | UI/UX design handoff |
