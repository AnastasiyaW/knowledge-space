---
title: CMS, Hosting, and Domain Selection for SEO
category: reference
tags: [seo, cms, wordpress, tilda, hosting, domain, site-speed, ssl]
---

# CMS, Hosting, and Domain Selection for SEO

Technical infrastructure choices that impact SEO from day one. Choosing the right CMS, hosting provider, and domain before building a site gives a significant ranking advantage over projects that have to migrate later.

## Key Facts

- **CMS** (Content Management System) = the platform/engine used to build and manage the site; choice affects page speed, code quality, SEO flexibility, and scalability
- **WordPress** dominates SEO-focused sites: open-source, extensible via plugins (Yoast SEO, Rank Math), full HTML/meta control, large developer ecosystem; ~43% of all websites use WordPress
- **Tilda** = no-code website builder popular in RU market; good for landing pages and small service sites; limited SEO capabilities compared to WordPress (restricted URL control, slower page speed, limited structured data)
- **Hosting** impacts: page load speed (TTFB), uptime (availability), server location (affects regional ranking), SSL support, and scalability
- **Domain** factors for SEO: age (older domains have slight advantage), history (check for spam/penalties via Wayback Machine), extension (.com preferred globally, ccTLD like .ru for regional), keyword in domain (minimal impact post-2012 EMD update)
- Key WordPress SEO plugins: **Yoast SEO** or **Rank Math** (meta tags, sitemaps, Schema), **WP Rocket** or **LiteSpeed Cache** (page speed), **ShortPixel** or **Imagify** (image optimization), **Classic Editor** (optional, some prefer for SEO control)
- See [[technical-seo-audit]] for auditing the technical foundation after setup
- See [[site-structure-architecture]] for URL and structure configuration

## Patterns

### CMS comparison for SEO

```
| Feature              | WordPress      | Tilda          | Custom (React/Next) |
|----------------------|----------------|----------------|---------------------|
| SEO control          | Full           | Limited         | Full                |
| Page speed           | Good (cached)  | Moderate        | Best (if optimized) |
| Meta tags control    | Full (plugins) | Basic           | Full                |
| URL structure        | Full control   | Limited         | Full                |
| Schema.org           | Plugin-based   | Very limited    | Custom              |
| Blog capabilities    | Excellent      | Limited         | Custom              |
| E-commerce           | WooCommerce    | Basic store     | Custom              |
| Learning curve       | Medium         | Low             | High                |
| Cost                 | Hosting only   | Monthly plan    | Development cost    |
| Best for             | Most SEO sites | Landing pages   | Complex apps        |
```

### WordPress SEO setup checklist

```
IMMEDIATELY AFTER INSTALL:
[ ] Install Yoast SEO or Rank Math
[ ] Set permalink structure: Post name (/sample-post/)
[ ] Configure XML sitemap (via SEO plugin)
[ ] Disable "Discourage search engines" (Settings > Reading)
[ ] Install caching plugin (WP Rocket / LiteSpeed Cache)
[ ] Install image optimization plugin
[ ] Set up HTTPS (SSL certificate via hosting or Let's Encrypt)

SEO PLUGIN CONFIGURATION:
[ ] Set homepage Title and Description
[ ] Configure Title templates for posts/pages/categories
[ ] Enable breadcrumb navigation
[ ] Set canonical URL preferences
[ ] Configure social media (Open Graph) tags
[ ] Submit sitemap to GSC and Yandex Webmaster

PERFORMANCE:
[ ] Enable server-level caching (OPcache, Redis)
[ ] Minify CSS/JS (via caching plugin)
[ ] Enable Gzip/Brotli compression
[ ] Lazy load images
[ ] Use CDN for static assets
```

### Hosting selection criteria

```
MUST-HAVE for SEO:
- TTFB < 200ms (server response time)
- 99.9%+ uptime SLA
- Free SSL certificate (Let's Encrypt)
- Server location near target audience
- PHP 8.0+ for WordPress (performance)
- HTTP/2 support
- Gzip/Brotli compression

NICE-TO-HAVE:
- Built-in CDN
- Automatic daily backups
- Staging environment
- Redis/Memcached object caching
- Server-level caching (LiteSpeed, Nginx FastCGI)

AVOID:
- Shared hosting with 100+ sites per server (slow)
- Hosting without SSH access (limits optimization)
- Hosting with forced ads or tracking scripts
- Free hosting (unreliable, often no SSL)
```

### Domain selection checklist

```
BEFORE PURCHASING:
[ ] Check domain history: web.archive.org (Wayback Machine)
[ ] Check for penalties: search "site:domain.com" in Google
[ ] Check spam history: ahrefs.com/backlink-checker
[ ] Verify no trademark conflicts
[ ] Check domain age: whois lookup

DOMAIN BEST PRACTICES:
- Short and memorable (under 15 characters ideal)
- Easy to spell and pronounce
- Brand-oriented (not keyword-stuffed)
- .com for international, ccTLD (.ru, .de) for regional
- Avoid hyphens and numbers if possible
- Register for 2+ years (minor trust signal)
```

## Gotchas

- **Tilda is not for SEO-heavy projects** - limited URL control (/tproduct/ prefix), heavy JavaScript rendering, slow page speed, limited structured data support; fine for landing pages but not for sites targeting 100+ keywords
- **WordPress without caching is slow** - a vanilla WordPress install with 10+ plugins can have 3-5s load times; caching plugin is not optional, it's mandatory for SEO
- **Free themes have SEO issues** - bloated code, poor heading hierarchy, missing Schema support; invest in a well-coded theme (GeneratePress, Astra, Kadence are SEO-optimized)
- **Hosting migration can temporarily hurt rankings** - changing IP, server location, or response time can cause ranking fluctuations for 2-4 weeks; time migrations during low-traffic periods
- **EMD (Exact Match Domain) is not a strategy** - `buy-cheap-shoes-online.com` provides negligible SEO advantage and damages brand perception; brand domains rank better long-term
- **Buying expired domains for their authority** is risky - Google can detect domain drops and reset authority; if the previous site was penalized, the penalty may carry over

## See Also

- [[technical-seo-audit]] - Post-setup technical verification
- [[site-structure-architecture]] - Configuring URL structure on your CMS
- [WordPress SEO Plugin: Yoast](https://yoast.com/wordpress/plugins/seo/)
- [WordPress SEO Plugin: Rank Math](https://rankmath.com/)
- [Google PageSpeed Insights](https://pagespeed.web.dev/)
- [WordPress Performance Handbook](https://developer.wordpress.org/advanced-administration/performance/)
