---
title: Site Structure and URL Architecture
category: techniques
tags: [seo-marketing, site-structure, urls, nesting-level, click-depth, url-construction]
---

# Site Structure and URL Architecture

Site hierarchy principles, URL construction rules, nesting levels, and structure templates by site type. Structure errors can prevent ranking regardless of other optimizations.

## Principles of Structure Building

Four sequential steps:
1. **Collect semantics** - all demand segments
2. **Build visual structure** - mind map before implementation
3. **Analyze competitors** - look at structure of leaders (avoid identical structure - risk of affiliation filter)
4. **Prepare URL addresses** - create the URL tree

## Nesting Level

**Definition**: Number of clicks from homepage to reach the page (NOT number of slashes in URL).

### Rules
- All primary promoted pages: no deeper than 3 clicks from homepage
- Pages targeting HF queries: ideally no deeper than 2 clicks
- Moving a page from 5 clicks to 1 click can push it from top-20 to top-10

### URL Nesting vs Click Depth
URL nesting (slash count) does NOT equal click depth:
- `site.ru/catalog/category/subcategory` - 3 slashes but could be 2 clicks via mega-menu
- URL nesting doesn't directly affect rankings
- URL depth useful for analytics segmentation (filter by URL folder in Metrica/GA)

## Structure Under Semantics

**Core principle**: Semantics = a ready cross-section of user demand. Create pages to cover that demand.

- Cluster with frequency > 0 and distinct intent -> create separate page
- Warning: many zero-content or thin pages -> "page quality insufficient" notifications
- Homepage = strongest page; assign the most "parent" cluster
- Homepage must have feeds to all site sections

### Information/Commercial Separation
- **Commercial queries**: category, product, service pages
- **Informational queries**: blog, articles, FAQs
- **Super cards**: product/service pages with deep content satisfying both intent types

## URL Construction Rules

### SEO-Optimized URLs (Human-Readable)
1. Human-readable URLs are mandatory for SEO
2. Use correct transliteration (not English translation for Russian sites)
3. Must contain the target query words
4. Avoid commercial words in URL (buy, price, order)
5. Avoid keyword repetition in URL path:
   - BAD: `/baby-strollers/baby-strollers-for-newborns/`
   - GOOD: `/baby-strollers/for-newborns/`
6. Avoid too-long URLs or 6+ slashes

### URL Quality Examples
```
BAD:  splav.ru/catalog.aspx?cat=20081113151601100150
OK:   secretpoint.ru/catalog/shoes/military/
GOOD: voentorga.ru/catalog/bertsy/
```

### Technical URL Requirements
- Strictly Latin characters
- Only letters and digits, no special characters
- Words separated by hyphen only (no underscores)
- Lowercase only; uppercase -> 301 redirect to lowercase
- Relative URLs in code
- Main mirror: `https://site.ru/` (with trailing slash)
- No duplicate path segments
- No more than 2 redirects; no chains or infinite loops
- All dev/staging environments closed via HTTP authentication

## Structure Templates by Site Type

### E-commerce
```
/ (Homepage)
+-- /contacts/
+-- /about/
+-- /delivery/
+-- /blog/
|   +-- /blog/article-1/
+-- /catalog/
    +-- /catalog/category/           <- "Digital technology"
    |   +-- /catalog/category/sub/   <- "Laptops"
    |   +-- /catalog/category/brand/ <- "Laptops Asus"
    |   +-- /catalog/category/tag/   <- "Gaming laptops"
    +-- /catalog/product-card/       <- Product card
```

**Product card subpages** (SEO hack): create sub-pages optimized individually:
- `/product/reviews/` - reviews
- `/product/specifications/` - specs
- `/product/photos/` - photos
- `/product/accessories/` - accessories with H2 subheadings per type

### Service Site
```
/ (Homepage)
+-- /contacts/
+-- /about/
+-- /blog/          (with anchor links to services)
+-- /services/
    +-- /services/service-1/
    +-- /services/category-1/
        +-- /services/category-1/service-3/
```

### Blog/Informational
```
/ (Homepage)
+-- /about/
+-- /section-1/
|   +-- /section-1/article-1/
+-- /section-2/
|   +-- /section-2/article-3/
+-- /tags/
```

## Click-Through Structure Instruments

### Homepage
- Most powerful page (highest weight)
- Add links to high-priority pages to reduce click depth
- "New Arrivals" blocks for fast indexation of new pages
- Feature important subcategories to boost their weight

### HTML Sitemap
- User-accessible page with anchor links to all sections
- Reduces click depth: main page -> sitemap (1 click) -> any section (2 clicks)
- For large sites: split into multiple sitemaps by section
- Usually in footer as "Site Map"
- Up to 1,000 internal links per page - no problem; max 5,000

### XML Sitemap
- Technical file at `yourdomain.ru/sitemap.xml`
- Contains all URLs + `lastmod` tags
- Submit to Webmaster and Search Console
- Always include sitemap URL in robots.txt

### Cross-Navigational Menu
- Header/footer/sidebar navigation on all pages
- **Must be `<a href>` HTML tags** - not JavaScript
- JS-only navigation = invisible to search robots

## Common Structure Errors

1. **Breadcrumb errors**: current page clickable (self-referencing), title in breadcrumb (too long), breadcrumbs via JS (invisible to robots)
2. **Cyclic links**: page links to itself; wastes crawl budget
3. **Query cannibalization**: hub page competes with child pages for same queries. Fix: rename hub or close from indexation
4. **No promoted pages unreachable from homepage**
5. **No "hanging nodes"** - pages linking to nothing
6. **JS-only navigation** - bots cannot follow

## Deliverables from Structure Work
1. Completed mind map of site
2. Click-depth structure document
3. URL address table (URL hierarchy)
4. Menu schema and internal linking requirements per page type

## Gotchas
- **Click depth matters far more than URL depth** - a page at `site.com/a/b/c/d/` but 2 clicks from home outranks one at `site.com/x/` buried 5 clicks deep
- **Identical competitor structure risks affiliation filter** - analyze competitors but differentiate
- **HTML sitemap is an SEO instrument, not just UX** - it directly controls crawl depth
- **JavaScript navigation is invisible** - all critical links must be direct HTML `<a>` tags
- **Product card subpages are underused** - separate review/specs/accessories pages capture additional long-tail traffic

## See Also
- [[internal-linking]] - Linking methods, SILO, pagination
- [[keyword-research-semantic-core]] - How clusters map to structure
- [[technical-seo-audit]] - Technical validation of structure
- [[seo-strategy-by-site-type]] - Structure differences by site type
