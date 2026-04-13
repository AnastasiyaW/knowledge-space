---
title: "MkDocs Material: Technical SEO"
description: "SEO configuration for MkDocs Material sites: sitemap, canonical URLs, plugins, Schema.org structured data, indexing strategy."
---

# MkDocs Material: Technical SEO

MkDocs Material has strong SEO defaults - most of the work is configuration and a few template overrides.

## What's Automatic (Zero Config)

Set `site_url` correctly and you get for free:

- `sitemap.xml` generated at build time with canonical URLs
- `<link rel="canonical">` on every page
- Semantic HTML5, proper heading hierarchy
- JavaScript-optional rendering (crawlers work without JS)
- Mobile-responsive layout (satisfies mobile-first indexing)
- BreadcrumbList JSON-LD when `navigation.path` is enabled

**`site_url` is mandatory.** Without it, sitemap URLs are broken and canonical tags are missing.

## Core `mkdocs.yml` Configuration

```yaml
site_name: Your Site
site_url: https://example.github.io/your-site/
site_description: "Specific description, 155 chars max, include keywords."
site_author: YourHandle

theme:
  name: material
  custom_dir: overrides
  features:
    - navigation.path          # breadcrumbs + BreadcrumbList JSON-LD
    - navigation.indexes       # section index pages (pillar pages)
    - navigation.tabs
    - navigation.sections
    - navigation.instant       # XHR-based loading (SPA feel for crawlers)
    - navigation.instant.prefetch
    - navigation.top
    - content.code.copy
    - search.suggest
    - search.highlight
    - toc.follow

plugins:
  - search
  - social:                    # generates OG card image per page
      cards: true
  - optimize:                  # image compression
      optimize_png: true
      optimize_jpg: true
      optimize_jpg_quality: 75
      cache: true
      cache_dir: .cache/plugins/optimize
  - privacy:                   # self-hosts external assets (fonts, etc.)
      assets: true
  - meta                       # bulk front matter via .meta.yml per dir
  - minify:
      minify_html: true
  - redirects:
      redirect_maps: {}
```

**`optimize` plugin** requires `pngquant` (PNG) and Pillow (JPG). Results are cached between builds.

**`social` plugin** generates a unique OG card image per page with title and branding. No manual image creation needed.

## `robots.txt`

MkDocs does **not** auto-generate `robots.txt`. Place manually in `docs/`:

```
User-agent: *
Allow: /

Sitemap: https://example.github.io/your-site/sitemap.xml
```

## Open Graph / Twitter Card Tags

**Option A: Social plugin** (auto OG images + basic tags)

**Option B: Custom template** `overrides/main.html`:

```jinja2
{% extends "base.html" %}
{% block extrahead %}
  {{ super() }}
  <meta property="og:type" content="article" />
  <meta property="og:title" content="{{ page.title }} - {{ config.site_name }}" />
  <meta property="og:description" content="{{ page.meta.description | default(config.site_description) }}" />
  <meta property="og:url" content="{{ page.canonical_url }}" />
  <meta property="og:site_name" content="{{ config.site_name }}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{{ page.title }} - {{ config.site_name }}" />
  <meta name="twitter:description" content="{{ page.meta.description | default(config.site_description) }}" />
{% endblock %}
```

## Schema.org Structured Data

**BreadcrumbList** is automatic via `navigation.path` feature.

**TechArticle schema** via `overrides/main.html`:

```jinja2
{% block extrahead %}
  {{ super() }}
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "TechArticle",
    "headline": "{{ page.title }}",
    "description": "{{ page.meta.description | default(config.site_description) }}",
    "url": "{{ page.canonical_url }}",
    "datePublished": "{{ page.meta.date | default('') }}",
    "dateModified": "{{ page.meta.updated | default('') }}",
    "author": { "@type": "Person", "name": "YourName" },
    "publisher": { "@type": "Organization", "name": "{{ config.site_name }}" },
    "proficiencyLevel": "{{ page.meta.level | default('Intermediate') }}"
  }
  </script>
{% endblock %}
```

## Per-Page Meta Description

Via front matter:

```yaml
---
description: "Specific 150-160 char description with primary keyword. End with action/value."
---
```

Bulk defaults via Meta plugin - place `.meta.yml` in each directory:

```yaml
# docs/kafka/.meta.yml
description_template: "Kafka {title} - configuration, examples, and production patterns."
```

## Third-Party Plugins

```yaml
# mkdocs-redirects - for URL restructuring
plugins:
  - redirects:
      redirect_maps:
        'old-path.md': 'new-path.md'
        'old-dir/page.md': 'new-dir/page.md'

# mkdocs-ultralytics-plugin - auto JSON-LD, FAQ schema, share buttons
plugins:
  - mkdocs-ultralytics-plugin:
      add_desc: true
      add_image: true
      add_json_ld: true
      add_share_buttons: true
      default_image: "assets/images/default-og.png"
```

## Indexing Strategy for Large Sites

### GitHub Pages Problem

`*.github.io` shares domain authority with millions of sites. Google allocates crawl budget per domain - "Discovered - currently not indexed" can persist for months. **A custom domain significantly speeds up indexing** (~$12-20/year).

### Google Search Console Setup

1. Add property: URL prefix `https://yourname.github.io/your-site/`
2. Verify via HTML file in `docs/`
3. Submit sitemap
4. Manual URL inspection for key pages (10/day limit - use on pillar pages first)

### IndexNow Auto-Submit on Deploy

```yaml
# .github/workflows/indexnow.yml
name: Submit to IndexNow
on:
  workflow_run:
    workflows: ["Deploy MkDocs"]
    types: [completed]
jobs:
  indexnow:
    runs-on: ubuntu-latest
    steps:
      - uses: jakob-bagterp/index-now-submit-sitemap-urls-action@v1
        with:
          host: yourname.github.io
          key: ${{ secrets.INDEXNOW_API_KEY }}
          sitemap: https://yourname.github.io/your-site/sitemap.xml
```

Bing and Yandex use IndexNow natively. Google uses its own system but the signal propagates.

### Pillar-Cluster Internal Linking

- Each domain folder has an `index.md` (pillar page) via `navigation.indexes`
- Individual articles are cluster pages
- Every cluster article links back to domain index
- Cross-domain links where topics relate
- Use `mkdocs-redirects` if restructuring URLs - broken internal links hurt crawl budget

## Content SEO

### Title Templates

```
[Specific Topic]: [What/How/Why] [Context] | Site Name
```

50-60 characters. Keyword in first half.

### Header Hierarchy

```
H1: One per page (auto from filename or front matter title)
  H2: Major sections (3-8 per article)
    H3: Subsections
      H4: Rare - avoid in most articles
```

AI systems use headings as semantic labels. Never skip levels.

### Lazy Loading Images

```markdown
![Description](image.png){ loading=lazy }
```

### Featured Snippet Optimization

- **Definition snippets**: 40-60 word paragraph immediately after H1
- **List snippets**: proper `ul`/`ol`, not bold text faking bullets
- **Table snippets**: comparison tables with clear column headers
- FAQ sections: H3 questions + 40-60 word answers. Add `FAQPage` schema.

## Gotchas

- **`site_url` without trailing slash breaks sitemaps**: use `https://example.github.io/repo/` not `https://example.github.io/repo`
- **`optimize` plugin on CI**: requires system packages (`pngquant`). Add to CI: `apt-get install pngquant` or the plugin will silently skip optimization
- **`social` plugin requires Pillow and CairoSVG**: missing deps cause silent build failures - add both to `requirements.txt`
- **`navigation.instant` and non-MkDocs assets**: instant loading (SPA mode) can break external analytics scripts that rely on full page loads - use `navigation.instant.progress` and test analytics
- **Meta plugin `.meta.yml` scope**: applies to current directory only, not recursive by default - add `.meta.yml` to each subdirectory if needed
- **GitHub Pages indexing delays**: even with IndexNow, expect 2-8 weeks for full indexing on `*.github.io`. Custom domain cuts this to days.
- **TransitionSeries in MkDocs redirects**: redirect URLs must include trailing slash to match generated URLs from `use_directory_urls: true`

## See Also

- [[robots-txt-sitemaps-indexation]]
- [[technical-seo-audit]]
- [[site-structure-urls]]
- [[technical-content-seo-strategy]]
