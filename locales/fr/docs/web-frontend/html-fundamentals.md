---
title: "Fondamentaux HTML"
category: concepts
tags: [web-frontend, html, semantics, accessibility]
level: 3
source_sha256: 3314112093a1db56fcf1ac5b372c1f39000e8720743fdfaf300bed058b7f60f6
translation: machine
translated_at: '2026-10-24'
---
# Fondamentaux HTML {#html-fundamentals}

HTML (HyperText Markup Language) définit la structure et la signification du contenu web. CSS ajoute la mise en forme, JavaScript ajoute le comportement. Standard actuel : HTML Living Standard (WHATWG), dit HTML5.

## Structure d'un document {#document-structure}

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

- `<!DOCTYPE html>` - doit être la première ligne, active le mode standards (et non le mode quirks)
- `<meta charset="UTF-8">` - doit se trouver dans les 1024 premiers octets
- `<meta name="viewport">` - indispensable pour l'adaptation aux mobiles

## Anatomie d'un élément {#element-anatomy}

```html
<tagname attribute="value">Content</tagname>
```

**Éléments auto-fermants (void)** - sans contenu, sans balise de fermeture :
```html
<img src="photo.jpg" alt="Description">
<br>  <hr>  <input>  <meta>  <link>
```

**Règles d'imbrication** : les éléments de bloc peuvent contenir des éléments de bloc et de ligne. Les éléments de ligne ne doivent contenir que des éléments de ligne (exception : `<a>` peut englober des blocs en HTML5).

## Titres {#headings}

```html
<h1>Main page heading</h1>   <!-- ONE per page -->
<h2>Section heading</h2>
<h3>Subsection</h3>
<h4>-<h6>                     <!-- Deeper levels -->
```

- Un seul `<h1>` par page (SEO et accessibilité)
- Ne jamais sauter de niveaux : h1 -> h2 -> h3, et non h1 -> h3
- Les lecteurs d'écran utilisent les titres pour la navigation
- Ne pas utiliser les titres pour la mise en forme : utiliser CSS

## Éléments de texte {#text-elements}

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

Toujours préférer les balises sémantiques (`<strong>`, `<em>`) aux balises de présentation (`<b>`, `<i>`).

## Liens {#links}

```html
<a href="https://example.com">External link</a>
<a href="https://example.com" target="_blank" rel="noopener noreferrer">New tab</a>
<a href="about.html">Internal page</a>
<a href="#section-id">Anchor link (same page)</a>
<a href="mailto:user@example.com">Email</a>
<a href="tel:+1234567890">Phone</a>
<a href="file.pdf" download>Download</a>
```

| Attribut | Rôle |
|-----------|---------|
| `href` | URL ou chemin (obligatoire) |
| `target="_blank"` | Ouvrir dans un nouvel onglet |
| `rel="noopener noreferrer"` | Sécurité pour les liens `_blank` |
| `download` | Forcer le téléchargement |

**Chemins** : absolus (`https://...`), relatifs au fichier (`../images/photo.jpg`), relatifs à la racine (`/images/photo.jpg`).

## Images {#images}

```html
<img src="images/photo.jpg" alt="Description" width="600" height="400">
<img src="photo.jpg" alt="" loading="lazy" decoding="async">
```

- `alt` obligatoire : descriptif pour les images informatives, vide (`alt=""`) pour les images décoratives
- `width`/`height` évitent les décalages de mise en page (optimisation CLS)
- `loading="lazy"` - chargement à l'approche de la zone visible

| Format | Cas d'usage |
|--------|----------|
| WebP | Remplacement moderne de JPG/PNG, meilleure compression |
| SVG | Icônes, logos, graphiques vectoriels (mise à l'échelle parfaite) |
| JPG | Photos, sans transparence |
| PNG | Graphiques avec transparence |
| AVIF | Nouvelle génération, meilleure compression, prise en charge croissante |

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

## Listes {#lists}

```html
<ul><li>Unordered item</li></ul>
<ol start="5" type="A"><li>Ordered item</li></ol>
<dl><dt>Term</dt><dd>Definition</dd></dl>
```

Les menus de navigation utilisent `<nav>` + `<ul>` + `<li>` + `<a>`. Les lecteurs d'écran annoncent « navigation avec N éléments ».

## Bloc et ligne {#block-vs-inline}

| Bloc | Ligne |
|-------|--------|
| Pleine largeur, retour à la ligne | Largeur du contenu, pas de retour à la ligne |
| `<div>`, `<p>`, `<h1>`-`<h6>`, `<section>`, `<article>`, `<header>`, `<footer>`, `<main>`, `<nav>`, `<form>` | `<span>`, `<a>`, `<strong>`, `<em>`, `<img>`, `<code>`, `<input>`, `<button>` |

`display: inline-block` - flux de ligne mais respecte width/height.

## Éléments sémantiques HTML5 {#semantic-html5-elements}

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

| Élément | Rôle |
|---------|---------|
| `<header>` | En-tête de page ou de section |
| `<nav>` | Liens de navigation |
| `<main>` | Contenu principal (UN par page) |
| `<section>` | Regroupement thématique |
| `<article>` | Contenu autonome |
| `<aside>` | Contenu indirectement lié |
| `<footer>` | Pied de page ou de section |

**Pourquoi la sémantique compte** : accessibilité (les lecteurs d'écran annoncent les repères), SEO (les moteurs de recherche comprennent la structure), maintenabilité.

## Entités HTML {#html-entities}

| Entité | Caractère | Entité | Caractère |
|--------|------|--------|------|
| `&lt;` | < | `&gt;` | > |
| `&amp;` | & | `&quot;` | " |
| `&nbsp;` | (espace) | `&copy;` | (c) |

## Pièges courants {#gotchas}

- **Balise meta viewport absente** : les navigateurs mobiles rendent la page sur environ 980 px de large, ce qui rend le contenu minuscule
- **Niveaux de titres sautés** : cassent la navigation des lecteurs d'écran
- **Soupe de `<div>`** : utiliser `<div>` partout au lieu d'éléments sémantiques
- **Attribut alt absent sur les images** : violation d'accessibilité, SEO dégradé
- **Commentaires contenant des informations sensibles** : visibles dans le code source de la page

## Voir aussi {#see-also}

- [[html-tables-and-forms]] - Tableaux, champs de formulaire, validation
- [[css-selectors-and-cascade]] - Mise en forme des éléments HTML
- [[css-box-model-and-layout]] - Modèle d'affichage bloc/ligne en CSS
