---
title: "MkDocs Material : SEO technique"
description: "Configuration SEO pour les sites MkDocs Material : sitemap, URL canoniques, plugins, données structurées Schema.org, stratégie d'indexation."
level: 3
source_sha256: 1da2aaa75980b6b22dd5b179f6f50cb24e5c3ddc5dd277f9e65f8de62f460b8d
translation: machine
translated_at: '2026-10-24'
---
# MkDocs Material : SEO technique {#mkdocs-material-technical-seo}

MkDocs Material offre de solides valeurs SEO par défaut : l'essentiel du travail consiste en de la configuration et quelques surcharges de templates.

## Ce qui est automatique (zéro configuration) {#whats-automatic-zero-config}

Si `site_url` est correctement défini, vous obtenez gratuitement :

- un `sitemap.xml` généré au moment du build, avec des URL canoniques
- un `<link rel="canonical">` sur chaque page
- du HTML5 sémantique et une hiérarchie de titres correcte
- un rendu compatible sans JavaScript (les crawlers fonctionnent sans JS)
- une mise en page responsive pour mobile (conforme à l'indexation mobile-first)
- des données JSON-LD BreadcrumbList lorsque `navigation.path` est activé

**`site_url` est obligatoire.** Sans cette option, les URL du sitemap sont cassées et les balises canoniques sont absentes.

## Configuration de base de `mkdocs.yml` {#core-mkdocsyml-configuration}

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

**Le plugin `optimize`** nécessite `pngquant` (PNG) et Pillow (JPG). Les résultats sont mis en cache entre les builds.

**Le plugin `social`** génère une image de carte OG unique pour chaque page, avec le titre et l'identité visuelle. Aucune création manuelle d'image n'est nécessaire.

## `robots.txt` {#robotstxt}

MkDocs ne génère **pas** automatiquement de `robots.txt`. Placez-le manuellement dans `docs/` :

```yaml
User-agent: *
Allow: /

Sitemap: https://example.github.io/your-site/sitemap.xml
```

## Balises Open Graph / Twitter Card {#open-graph-twitter-card-tags}

**Option A : plugin social** (images OG automatiques et balises de base)

**Option B : template personnalisé** `overrides/main.html` :

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

## Données structurées Schema.org {#schemaorg-structured-data}

**BreadcrumbList** est automatique grâce à la fonctionnalité `navigation.path`.

**Schéma TechArticle** via `overrides/main.html` :

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

## Meta description par page {#per-page-meta-description}

Via le front matter :

```yaml
---
description: "Specific 150-160 char description with primary keyword. End with action/value."
---
```

Valeurs par défaut en masse via le plugin Meta : placez un fichier `.meta.yml` dans chaque répertoire :

```yaml
# docs/kafka/.meta.yml
description_template: "Kafka {title} - configuration, examples, and production patterns."
```

## Plugins tiers {#third-party-plugins}

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

## Stratégie d'indexation pour les grands sites {#indexing-strategy-for-large-sites}

### Problème de GitHub Pages {#github-pages-problem}

`*.github.io` partage son autorité de domaine avec des millions d'autres sites. Google alloue un budget de crawl par domaine : l'état « Détectée, actuellement non indexée » peut persister pendant des mois. **Un domaine personnalisé accélère nettement l'indexation** (environ 12 à 20 $ par an).

### Configuration de Google Search Console {#google-search-console-setup}

1. Ajoutez une propriété de type préfixe d'URL : `https://yourname.github.io/your-site/`
2. Vérifiez la propriété via un fichier HTML placé dans `docs/`
3. Soumettez le sitemap
4. Inspectez manuellement les URL des pages clés (limite de 10 par jour : commencez par les pages piliers)

### Soumission automatique à IndexNow lors du déploiement {#indexnow-auto-submit-on-deploy}

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

Bing et Yandex utilisent IndexNow nativement. Google utilise son propre système, mais le signal se propage.

### Maillage interne pilier-cluster {#pillar-cluster-internal-linking}

- Chaque dossier de domaine contient un `index.md` (page pilier) grâce à `navigation.indexes`
- Les articles individuels sont des pages de cluster
- Chaque article de cluster renvoie vers l'index du domaine
- Liens inter-domaines lorsque les sujets sont liés
- Utilisez `mkdocs-redirects` si vous restructurez les URL : des liens internes cassés nuisent au budget de crawl

## SEO du contenu {#content-seo}

### Modèles de titres {#title-templates}

```text
[Specific Topic]: [What/How/Why] [Context] | Site Name
```

50 à 60 caractères. Le mot-clé se trouve dans la première moitié.

### Hiérarchie des titres {#header-hierarchy}

```sql
H1: One per page (auto from filename or front matter title)
  H2: Major sections (3-8 per article)
    H3: Subsections
      H4: Rare - avoid in most articles
```

Les systèmes d'IA utilisent les titres comme étiquettes sémantiques. Ne sautez jamais de niveau.

### Chargement différé des images {#lazy-loading-images}

```markdown
![Description](image.png){ loading=lazy }
```

### Optimisation pour les featured snippets {#featured-snippet-optimization}

- **Extraits de définition** : un paragraphe de 40 à 60 mots placé immédiatement après le H1
- **Extraits de liste** : des `ul`/`ol` correctement formés, et non du texte en gras imitant des puces
- **Extraits de tableau** : des tableaux comparatifs aux en-têtes de colonnes clairs
- Sections FAQ : questions en H3 et réponses de 40 à 60 mots. Ajoutez le schéma `FAQPage`.

## Pièges courants {#gotchas}

- **Un `site_url` sans slash final casse les sitemaps** : utilisez `https://example.github.io/repo/` et non `https://example.github.io/repo`
- **Le plugin `optimize` en CI** : nécessite des paquets système (`pngquant`). Ajoutez à la CI : `apt-get install pngquant`, faute de quoi le plugin ignorera silencieusement l'optimisation
- **Le plugin `social` nécessite Pillow et CairoSVG** : des dépendances manquantes provoquent des échecs de build silencieux. Ajoutez les deux à `requirements.txt`
- **`navigation.instant` et les ressources non MkDocs** : le chargement instantané (mode SPA) peut casser les scripts d'analytique externes qui reposent sur des chargements de page complets. Utilisez `navigation.instant.progress` et testez vos analytics
- **Portée du `.meta.yml` du plugin Meta** : ne s'applique qu'au répertoire courant, pas récursivement par défaut. Ajoutez un `.meta.yml` dans chaque sous-répertoire si nécessaire
- **Délais d'indexation de GitHub Pages** : même avec IndexNow, comptez 2 à 8 semaines pour une indexation complète sur `*.github.io`. Un domaine personnalisé réduit ce délai à quelques jours.
- **TransitionSeries dans les redirections MkDocs** : les URL de redirection doivent inclure un slash final pour correspondre aux URL générées par `use_directory_urls: true`

## Voir aussi {#see-also}

- [[robots-txt-sitemaps-indexation]]
- [[technical-seo-audit]]
- [[site-structure-urls]]
- [[technical-content-seo-strategy]]
