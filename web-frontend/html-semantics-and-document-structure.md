---
title: HTML Semantics and Document Structure
category: html
tags: [html, semantic-html, accessibility, document-structure, meta-tags]
---

# HTML Semantics and Document Structure

## Key Facts

- **Semantic HTML** uses elements that convey meaning (`<article>`, `<nav>`, `<aside>`) instead of generic `<div>`/`<span>`
- Document structure: `<!DOCTYPE html>` -> `<html lang="en">` -> `<head>` (meta) + `<body>` (content)
- `<head>` contains `<meta charset="UTF-8">`, `<meta name="viewport">`, `<title>`, `<link>`, `<script>`
- **Block elements** (`<div>`, `<p>`, `<h1>`-`<h6>`, `<section>`) take full width, stack vertically
- **Inline elements** (`<span>`, `<a>`, `<strong>`, `<em>`) flow within text, no width/height by default
- `<header>`, `<main>`, `<footer>` define page landmarks; screen readers use them for navigation
- `<figure>` + `<figcaption>` for self-contained illustrative content
- `<details>` + `<summary>` provides native collapsible sections without JavaScript
- Related: [[css-box-model-and-display]], [[responsive-design-and-media-queries]]

## Patterns

### Semantic Page Layout

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Page Title</title>
</head>
<body>
  <header>
    <nav aria-label="Main">
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/about">About</a></li>
      </ul>
    </nav>
  </header>

  <main>
    <article>
      <h1>Article Title</h1>
      <p>Content...</p>
      <section>
        <h2>Subsection</h2>
        <p>More content...</p>
      </section>
    </article>
    <aside>
      <h2>Related Links</h2>
    </aside>
  </main>

  <footer>
    <p>&copy; 2026</p>
  </footer>
</body>
</html>
```

### Accessibility Attributes

```html
<!-- ARIA roles supplement semantic HTML -->
<button aria-expanded="false" aria-controls="menu">Toggle</button>
<div id="menu" role="menu" hidden>...</div>

<!-- Alt text for images -->
<img src="chart.png" alt="Sales increased 30% in Q1 2026">

<!-- Skip navigation link -->
<a href="#main-content" class="skip-link">Skip to content</a>
<main id="main-content">...</main>
```

## Gotchas

- `<div>` has no semantic meaning; use `<section>` (with heading) or `<article>` (self-contained) instead
- `<b>` vs `<strong>`: `<strong>` conveys importance (screen readers emphasize it), `<b>` is purely visual
- viewport meta is essential for mobile; without it, mobile browsers render at ~980px desktop width
- `<a>` without `href` is not keyboard-focusable; always include `href` or use `<button>` for actions
- Self-closing tags (`<br/>`, `<img/>`) don't need the slash in HTML5 but do in JSX/React

## See Also

- [MDN: HTML elements reference](https://developer.mozilla.org/en-US/docs/Web/HTML/Element)
- [MDN: ARIA roles](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Roles)
