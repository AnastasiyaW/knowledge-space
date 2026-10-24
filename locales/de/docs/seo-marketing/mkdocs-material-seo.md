---
title: "MkDocs Material: Technisches SEO"
description: "SEO-Konfiguration für MkDocs-Material-Sites: Sitemap, kanonische URLs, Plugins, strukturierte Daten (Schema.org), Indexierungsstrategie."
level: 3
source_sha256: 1da2aaa75980b6b22dd5b179f6f50cb24e5c3ddc5dd277f9e65f8de62f460b8d
translation: machine
translated_at: '2026-10-24'
---
# MkDocs Material: Technisches SEO {#mkdocs-material-technical-seo}

MkDocs Material bietet starke SEO-Standardeinstellungen. Der Großteil der Arbeit besteht aus Konfiguration und einigen Template-Overrides.

## Was automatisch funktioniert (keine Konfiguration nötig) {#whats-automatic-zero-config}

Wenn `site_url` korrekt gesetzt ist, erhältst du folgende Funktionen ohne weiteren Aufwand:

- `sitemap.xml`, die beim Build mit kanonischen URLs erzeugt wird
- `<link rel="canonical">` auf jeder Seite
- Semantisches HTML5 und eine saubere Überschriftenhierarchie
- Optionales JavaScript beim Rendern (Crawler funktionieren auch ohne JS)
- Mobil responsives Layout (erfüllt die Anforderungen des Mobile-First-Indexings)
- BreadcrumbList-JSON-LD, wenn `navigation.path` aktiviert ist

**`site_url` ist zwingend erforderlich.** Ohne diese Angabe sind die Sitemap-URLs fehlerhaft und die Canonical-Tags fehlen.

## Zentrale `mkdocs.yml`-Konfiguration {#core-mkdocsyml-configuration}

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

**Das `optimize`-Plugin** benötigt `pngquant` (PNG) und Pillow (JPG). Die Ergebnisse werden zwischen Builds zwischengespeichert.

**Das `social`-Plugin** erzeugt pro Seite ein eigenes OG-Kartenbild mit Titel und Branding. Manuelle Bilderstellung ist nicht nötig.

## `robots.txt` {#robotstxt}

MkDocs erzeugt **keine** `robots.txt` automatisch. Lege sie manuell in `docs/` ab:

```yaml
User-agent: *
Allow: /

Sitemap: https://example.github.io/your-site/sitemap.xml
```

## Open-Graph- / Twitter-Card-Tags {#open-graph-twitter-card-tags}

**Option A: Social-Plugin** (automatische OG-Bilder und Basis-Tags)

**Option B: Eigenes Template** `overrides/main.html`:

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

## Strukturierte Daten (Schema.org) {#schemaorg-structured-data}

**BreadcrumbList** wird über die Funktion `navigation.path` automatisch erzeugt.

**TechArticle-Schema** über `overrides/main.html`:

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

## Meta-Description pro Seite {#per-page-meta-description}

Über das Front Matter:

```yaml
---
description: "Specific 150-160 char description with primary keyword. End with action/value."
---
```

Standardwerte für ganze Verzeichnisse über das Meta-Plugin – lege dazu in jedem Verzeichnis eine `.meta.yml` ab:

```yaml
# docs/kafka/.meta.yml
description_template: "Kafka {title} - configuration, examples, and production patterns."
```

## Plugins von Drittanbietern {#third-party-plugins}

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

## Indexierungsstrategie für große Sites {#indexing-strategy-for-large-sites}

### Das Problem mit GitHub Pages {#github-pages-problem}

`*.github.io` teilt sich die Domain-Autorität mit Millionen anderen Sites. Google teilt das Crawl-Budget pro Domain zu. Der Status „Entdeckt – derzeit nicht indexiert“ kann daher monatelang bestehen bleiben. **Eine eigene Domain beschleunigt die Indexierung deutlich** (ca. 12–20 $ pro Jahr).

### Einrichtung der Google Search Console {#google-search-console-setup}

1. Property hinzufügen: URL-Präfix `https://yourname.github.io/your-site/`
2. Verifizierung per HTML-Datei in `docs/`
3. Sitemap einreichen
4. Manuelle URL-Prüfung für zentrale Seiten (Limit: 10 pro Tag – zuerst die Pillar-Seiten verwenden)

### Automatisches Einreichen über IndexNow beim Deployment {#indexnow-auto-submit-on-deploy}

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

Bing und Yandex unterstützen IndexNow nativ. Google nutzt ein eigenes System, das Signal wird aber trotzdem weitergegeben.

### Pillar-Cluster-Verlinkung {#pillar-cluster-internal-linking}

- Jeder Domain-Ordner hat eine `index.md` (Pillar-Seite), aktiviert über `navigation.indexes`
- Einzelne Artikel sind Cluster-Seiten
- Jeder Cluster-Artikel verlinkt zurück auf die Domain-Index-Seite
- Querverlinkungen zwischen Domains, wenn sich die Themen überschneiden
- `mkdocs-redirects` verwenden, wenn URLs umstrukturiert werden – defekte interne Links belasten das Crawl-Budget

## Content-SEO {#content-seo}

### Titel-Vorlagen {#title-templates}

```text
[Specific Topic]: [What/How/Why] [Context] | Site Name
```

50–60 Zeichen. Das Keyword gehört in die erste Hälfte.

### Überschriftenhierarchie {#header-hierarchy}

```sql
H1: One per page (auto from filename or front matter title)
  H2: Major sections (3-8 per article)
    H3: Subsections
      H4: Rare - avoid in most articles
```

KI-Systeme nutzen Überschriften als semantische Marker. Überspringe nie Ebenen.

### Lazy Loading für Bilder {#lazy-loading-images}

```markdown
![Description](image.png){ loading=lazy }
```

### Optimierung für Featured Snippets {#featured-snippet-optimization}

- **Definitions-Snippets**: Absatz mit 40–60 Wörtern direkt nach der H1
- **Listen-Snippets**: saubere `ul`/`ol`-Listen, keine fett formatierten Textzeilen, die Aufzählungen nur vortäuschen
- **Tabellen-Snippets**: Vergleichstabellen mit klaren Spaltenüberschriften
- FAQ-Abschnitte: H3-Fragen und Antworten mit 40–60 Wörtern. Zusätzlich das `FAQPage`-Schema ergänzen.

## Stolperfallen {#gotchas}

- **`site_url` ohne abschließenden Schrägstrich bricht die Sitemaps**: verwende `https://example.github.io/repo/` statt `https://example.github.io/repo`
- **`optimize`-Plugin in der CI**: benötigt Systempakete (`pngquant`). Ergänze in der CI `apt-get install pngquant`, sonst überspringt das Plugin die Optimierung ohne Fehlermeldung
- **`social`-Plugin benötigt Pillow und CairoSVG**: fehlende Abhängigkeiten führen zu stillen Build-Fehlern – trage beide in `requirements.txt` ein
- **`navigation.instant` und Assets außerhalb von MkDocs**: das instant-Laden (SPA-Modus) kann externe Analytics-Skripte stören, die auf vollständige Seitenladevorgänge angewiesen sind. Verwende `navigation.instant.progress` und teste die Analytics
- **Geltungsbereich der Meta-Plugin-`.meta.yml`**: gilt nur für das aktuelle Verzeichnis, standardmäßig nicht rekursiv. Lege bei Bedarf in jedem Unterverzeichnis eine eigene `.meta.yml` ab
- **Verzögerungen bei der Indexierung auf GitHub Pages**: auch mit IndexNow ist für eine vollständige Indexierung auf `*.github.io` mit 2–8 Wochen zu rechnen. Mit einer eigenen Domain dauert es nur noch Tage.
- **TransitionSeries in MkDocs-Weiterleitungen**: Weiterleitungs-URLs müssen einen abschließenden Schrägstrich enthalten, damit sie zu den über `use_directory_urls: true` erzeugten URLs passen

## Siehe auch {#see-also}

- [[robots-txt-sitemaps-indexation]]
- [[technical-seo-audit]]
- [[site-structure-urls]]
- [[technical-content-seo-strategy]]
