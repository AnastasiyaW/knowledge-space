---
title: HTML, CSS, and JavaScript for SEO
category: reference
tags: [seo, html, css, javascript, structured-data, schema-org, rendering, web-vitals]
---

# HTML, CSS, and JavaScript for SEO

The minimum level of web development knowledge required for SEO work. SEO specialists don't need to be programmers, but must be able to read HTML source code, understand how CSS affects rendering, and know how JavaScript impacts crawling and indexing.

## Key Facts

- **HTML** (HyperText Markup Language) = the structure/markup language of web pages; SEO specialists must understand key HTML tags and how search engines parse them
- **CSS** (Cascading Style Sheets) = controls visual appearance; relevant to SEO through Core Web Vitals (CLS, render-blocking resources), hidden content, and mobile responsiveness
- **JavaScript** = programming language that adds interactivity; critical SEO concern because search engines may not execute JS fully, affecting content visibility and indexing
- Google renders JavaScript (via Chromium-based renderer) but with delays - JS-dependent content may take days to weeks longer to be indexed compared to server-rendered HTML
- Yandex has limited JavaScript rendering capabilities compared to Google; JS-heavy sites may not index properly in Yandex
- **Schema.org structured data** = JSON-LD markup that helps search engines understand page content and enables rich results (stars, prices, FAQ, breadcrumbs in SERP)
- Key HTML tags for SEO: `<title>`, `<meta name="description">`, `<h1>`-`<h6>`, `<a href>`, `<img alt>`, `<canonical>`, `<meta name="robots">`, `<hreflang>`
- See [[on-page-optimization]] for how to optimize HTML meta tags
- See [[technical-seo-audit]] for identifying HTML/rendering issues

## Patterns

### Essential HTML tags for SEO

```html
<head>
  <!-- Page title (most important on-page factor) -->
  <title>Primary Keyword - Brand Name</title>

  <!-- Meta description (affects CTR) -->
  <meta name="description" content="Page description with CTA">

  <!-- Canonical URL (prevents duplicate content) -->
  <link rel="canonical" href="https://site.com/page/">

  <!-- Robots directives -->
  <meta name="robots" content="index, follow">
  <!-- or: noindex, nofollow, noarchive, nosnippet -->

  <!-- Open Graph for social sharing -->
  <meta property="og:title" content="Page Title">
  <meta property="og:description" content="Description">
  <meta property="og:image" content="https://site.com/image.jpg">

  <!-- Mobile viewport (required for mobile-first indexing) -->
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <!-- Hreflang for multi-language sites -->
  <link rel="alternate" hreflang="en" href="https://site.com/en/page/">
  <link rel="alternate" hreflang="ru" href="https://site.com/ru/page/">
</head>

<body>
  <!-- One H1 per page -->
  <h1>Primary Keyword in Natural Form</h1>

  <!-- Heading hierarchy (no skipping levels) -->
  <h2>Section Heading</h2>
  <h3>Subsection Heading</h3>

  <!-- Links with descriptive anchor text -->
  <a href="/related-page/">Descriptive Anchor Text</a>

  <!-- Images with alt text -->
  <img src="photo.webp" alt="Descriptive alt text with keyword"
       width="800" height="600" loading="lazy">
</body>
```

### Schema.org JSON-LD examples

```html
<!-- FAQ Schema (enables FAQ rich results in SERP) -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "What is SEO?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "SEO stands for Search Engine Optimization..."
    }
  }]
}
</script>

<!-- Breadcrumb Schema -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type":"ListItem","position":1,
     "name":"Home","item":"https://site.com/"},
    {"@type":"ListItem","position":2,
     "name":"Category","item":"https://site.com/category/"},
    {"@type":"ListItem","position":3,
     "name":"Page Title"}
  ]
}
</script>

<!-- Product Schema (enables price/rating in SERP) -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Product Name",
  "offers": {
    "@type": "Offer",
    "price": "99.99",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.5",
    "reviewCount": "89"
  }
}
</script>
```

### CSS performance for Core Web Vitals

```html
<!-- Critical CSS inlined (reduces render-blocking) -->
<style>
  /* Only above-the-fold styles here */
  body { font-family: system-ui; margin: 0; }
  .header { height: 60px; }
</style>

<!-- Non-critical CSS loaded asynchronously -->
<link rel="preload" href="/styles.css" as="style"
      onload="this.onload=null;this.rel='stylesheet'">

<!-- Prevent CLS: always set width/height on images -->
<img src="hero.webp" width="1200" height="630"
     style="aspect-ratio: 1200/630;">

<!-- Prevent CLS: reserve space for dynamic content -->
<div style="min-height: 300px;">
  <!-- Ad or dynamic content loads here -->
</div>
```

### JavaScript SEO checklist

```
RENDERING:
[ ] Critical content is in initial HTML (not JS-only)
[ ] Server-Side Rendering (SSR) or Static Generation for key pages
[ ] Test rendering: Google Search Console > URL Inspection > View Tested Page
[ ] Verify with "View Source" (what crawler sees) vs "Inspect Element" (rendered DOM)

COMMON JS SEO ISSUES:
[ ] Internal links use <a href> not onClick handlers
[ ] Content loaded via AJAX/fetch is visible to Googlebot
[ ] Infinite scroll has paginated HTML fallback
[ ] Lazy-loaded content is in viewport when crawler visits
[ ] Client-side routing provides unique URLs for each page
[ ] No content behind user interactions (click-to-reveal)
```

## Gotchas

- **View Source != Inspect Element** - View Source shows raw HTML (what the crawler initially sees); Inspect Element shows the rendered DOM (after JS execution); SEO-critical content must be in raw HTML or rendered within seconds
- **CSS `display: none` content is devalued** - hidden text may be crawled but given less weight or ignored; don't hide important content with CSS
- **Schema.org markup must match page content** - adding Product schema to a page that doesn't show a product is a structured data spam violation and can result in manual action
- **Render-blocking CSS/JS** delays First Contentful Paint and hurts Core Web Vitals; critical CSS should be inlined, non-critical deferred
- **Single Page Applications (SPAs)** built with React/Vue/Angular without SSR are often invisible to search engines; Next.js/Nuxt.js with SSR solve this but add complexity
- **Hreflang implementation errors** are the most common international SEO mistake - every page must reference all language variants including itself; missing return tags invalidate the signal

## See Also

- [[on-page-optimization]] - Using HTML tags for SEO optimization
- [[technical-seo-audit]] - Finding HTML/rendering issues
- [Google Structured Data Documentation](https://developers.google.com/search/docs/appearance/structured-data)
- [Schema.org Full Hierarchy](https://schema.org/docs/full.html)
- [Google JavaScript SEO Guide](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics)
- [Rich Results Test Tool](https://search.google.com/test/rich-results)
