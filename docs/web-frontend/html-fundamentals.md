---
title: HTML Fundamentals
category: concepts
tags: [web-frontend, html, semantics, accessibility]
---

# HTML Fundamentals

HTML (HyperText Markup Language) defines the structure and meaning of web content. CSS adds styling, JavaScript adds behavior. Current standard: HTML5 Living Standard (WHATWG).

## Document Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Page description for SEO">
  <title>Page Title</title>
  <link rel="stylesheet" href="css/style.css">
  <link rel="icon" href="favicon.ico">
</head>
<body>
  <!-- All visible content -->
</body>
</html>
```

- `<!DOCTYPE html>` - must be first line, triggers standards mode (not quirks mode)
- `<meta charset="UTF-8">` - must be within first 1024 bytes
- `<meta name="viewport">` - essential for mobile responsiveness

## Element Anatomy

```html
<tagname attribute="value">Content</tagname>
```

**Self-closing (void) elements** - no content, no closing tag:
```html
<img src="photo.jpg" alt="Description">
<br>  <hr>  <input>  <meta>  <link>
```

**Nesting rules**: block elements can contain block and inline elements. Inline elements should only contain inline elements (exception: `<a>` can wrap blocks in HTML5).

## Headings

```html
<h1>Main page heading</h1>   <!-- ONE per page -->
<h2>Section heading</h2>
<h3>Subsection</h3>
<h4>-<h6>                     <!-- Deeper levels -->
```

- Only one `<h1>` per page (SEO + accessibility)
- Never skip levels: h1 -> h2 -> h3, not h1 -> h3
- Screen readers use headings for navigation
- Don't use headings for styling - use CSS

## Text Elements

```html
<p>Paragraph text.</p>
<strong>Semantic importance</strong>    <!-- Bold by default, read differently by screen readers -->
<em>Stress emphasis</em>               <!-- Italic by default -->
<b>Visual bold only</b>                <!-- No semantic meaning -->
<i>Visual italic only</i>
<mark>Highlighted</mark>
<del>Deleted</del>  <ins>Inserted</ins>
<sub>Subscript</sub>  <sup>Superscript</sup>
<code>inline code</code>
<pre><code>preformatted block</code></pre>
<blockquote><p>Quoted text</p><cite>- Author</cite></blockquote>
```

Always prefer semantic tags (`<strong>`, `<em>`) over presentational (`<b>`, `<i>`).

## Links

```html
<a href="https://example.com">External link</a>
<a href="https://example.com" target="_blank" rel="noopener noreferrer">New tab</a>
<a href="about.html">Internal page</a>
<a href="#section-id">Anchor link (same page)</a>
<a href="mailto:user@example.com">Email</a>
<a href="tel:+1234567890">Phone</a>
<a href="file.pdf" download>Download</a>
```

| Attribute | Purpose |
|-----------|---------|
| `href` | URL or path (required) |
| `target="_blank"` | Open in new tab |
| `rel="noopener noreferrer"` | Security for `_blank` links |
| `download` | Force download |

**Paths**: absolute (`https://...`), relative to file (`../images/photo.jpg`), relative to root (`/images/photo.jpg`).

## Images

```html
<img src="images/photo.jpg" alt="Description" width="600" height="400">
<img src="photo.jpg" alt="" loading="lazy" decoding="async">
```

- `alt` required: descriptive for informational images, empty `alt=""` for decorative
- `width`/`height` prevent layout shift (CLS optimization)
- `loading="lazy"` - loads when near viewport

| Format | Use Case |
|--------|----------|
| WebP | Modern replacement for JPG/PNG, best compression |
| SVG | Icons, logos, vector graphics (scales perfectly) |
| JPG | Photos, no transparency |
| PNG | Graphics with transparency |
| AVIF | Next-gen, best compression, growing support |

```html
<figure>
  <img src="chart.png" alt="Sales chart 2024">
  <figcaption>Figure 1: Quarterly growth</figcaption>
</figure>

<picture>
  <source media="(min-width: 1024px)" srcset="photo-desktop.jpg">
  <source media="(min-width: 768px)" srcset="photo-tablet.jpg">
  <img src="photo-mobile.jpg" alt="Description">
</picture>
```

## Lists

```html
<ul><li>Unordered item</li></ul>
<ol start="5" type="A"><li>Ordered item</li></ol>
<dl><dt>Term</dt><dd>Definition</dd></dl>
```

Navigation menus use `<nav>` + `<ul>` + `<li>` + `<a>`. Screen readers announce "navigation with N items".

## Block vs Inline

| Block | Inline |
|-------|--------|
| Full width, new line | Width of content, no new line |
| `<div>`, `<p>`, `<h1>`-`<h6>`, `<section>`, `<article>`, `<header>`, `<footer>`, `<main>`, `<nav>`, `<form>` | `<span>`, `<a>`, `<strong>`, `<em>`, `<img>`, `<code>`, `<input>`, `<button>` |

`display: inline-block` - inline flow but respects width/height.

## Semantic HTML5 Elements

```html
<body>
  <header><nav><ul>...</ul></nav></header>
  <main>
    <section>
      <h2>Section Title</h2>
      <article><h3>Article</h3><p>Content</p></article>
    </section>
    <aside><h3>Related</h3></aside>
  </main>
  <footer><p>&copy; 2024</p></footer>
</body>
```

| Element | Purpose |
|---------|---------|
| `<header>` | Page/section header |
| `<nav>` | Navigation links |
| `<main>` | Primary content (ONE per page) |
| `<section>` | Thematic grouping |
| `<article>` | Self-contained content |
| `<aside>` | Tangentially related |
| `<footer>` | Page/section footer |

**Why semantics matter**: accessibility (screen readers announce landmarks), SEO (search engines understand structure), maintainability.

## HTML Entities

| Entity | Char | Entity | Char |
|--------|------|--------|------|
| `&lt;` | < | `&gt;` | > |
| `&amp;` | & | `&quot;` | " |
| `&nbsp;` | (space) | `&copy;` | (c) |

## Gotchas

- **Missing viewport meta**: mobile browsers render at ~980px width, making content tiny
- **Skipping heading levels**: breaks screen reader navigation
- **`<div>` soup**: using `<div>` for everything instead of semantic elements
- **Missing alt on images**: accessibility violation, poor SEO
- **Comments contain sensitive info**: visible in page source

## See Also

- [[html-tables-and-forms]] - Tables, form inputs, validation
- [[css-selectors-and-cascade]] - Styling HTML elements
- [[css-box-model-and-layout]] - Block/inline display model in CSS
