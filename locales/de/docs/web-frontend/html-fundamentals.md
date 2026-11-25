---
title: "HTML-Grundlagen"
category: concepts
tags: [web-frontend, html, semantics, accessibility]
level: 3
source_sha256: 3314112093a1db56fcf1ac5b372c1f39000e8720743fdfaf300bed058b7f60f6
translation: machine
translated_at: '2026-10-24'
---
# HTML-Grundlagen {#html-fundamentals}

HTML (HyperText Markup Language) definiert die Struktur und die Bedeutung von Webinhalten. CSS ergänzt die Gestaltung, JavaScript ergänzt das Verhalten. Aktueller Standard: HTML5 Living Standard (WHATWG).

## Dokumentstruktur {#document-structure}

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

- `<!DOCTYPE html>` - muss die erste Zeile sein, aktiviert den Standardmodus (nicht den Quirks-Modus)
- `<meta charset="UTF-8">` - muss innerhalb der ersten 1024 Bytes stehen
- `<meta name="viewport">` - essenziell für die Responsivität auf mobilen Geräten

## Aufbau von Elementen {#element-anatomy}

```html
<tagname attribute="value">Content</tagname>
```

**Selbstschließende (Void-)Elemente** - kein Inhalt, kein schließendes Tag:
```html
<img src="photo.jpg" alt="Description">
<br>  <hr>  <input>  <meta>  <link>
```

**Verschachtelungsregeln**: Block-Elemente können Block- und Inline-Elemente enthalten. Inline-Elemente sollten nur Inline-Elemente enthalten (Ausnahme: `<a>` kann in HTML5 Blöcke umschließen).

## Überschriften {#headings}

```html
<h1>Main page heading</h1>   <!-- ONE per page -->
<h2>Section heading</h2>
<h3>Subsection</h3>
<h4>-<h6>                     <!-- Deeper levels -->
```

- Nur ein `<h1>` pro Seite (SEO + Barrierefreiheit)
- Ebenen niemals überspringen: h1 -> h2 -> h3, nicht h1 -> h3
- Screenreader nutzen Überschriften zur Navigation
- Überschriften nicht zur Gestaltung verwenden - dafür CSS nutzen

## Textelemente {#text-elements}

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

Semantische Tags (`<strong>`, `<em>`) sind präsentationalen Tags (`<b>`, `<i>`) stets vorzuziehen.

## Links {#links}

```html
<a href="https://example.com">External link</a>
<a href="https://example.com" target="_blank" rel="noopener noreferrer">New tab</a>
<a href="about.html">Internal page</a>
<a href="#section-id">Anchor link (same page)</a>
<a href="mailto:user@example.com">Email</a>
<a href="tel:+1234567890">Phone</a>
<a href="file.pdf" download>Download</a>
```

| Attribut | Zweck |
|-----------|---------|
| `href` | URL oder Pfad (erforderlich) |
| `target="_blank"` | Öffnet in einem neuen Tab |
| `rel="noopener noreferrer"` | Sicherheit für `_blank`-Links |
| `download` | Erzwingt den Download |

**Pfade**: absolut (`https://...`), relativ zur Datei (`../images/photo.jpg`), relativ zur Wurzel (`/images/photo.jpg`).

## Bilder {#images}

```html
<img src="images/photo.jpg" alt="Description" width="600" height="400">
<img src="photo.jpg" alt="" loading="lazy" decoding="async">
```

- `alt` ist erforderlich: beschreibend bei informativen Bildern, leer (`alt=""`) bei dekorativen
- `width`/`height` verhindern Layoutverschiebungen (CLS-Optimierung)
- `loading="lazy"` - lädt, wenn das Bild nahe am Viewport ist

| Format | Anwendungsfall |
|--------|----------------|
| WebP | Moderner Ersatz für JPG/PNG, beste Kompression |
| SVG | Icons, Logos, Vektorgrafiken (skaliert verlustfrei) |
| JPG | Fotos, keine Transparenz |
| PNG | Grafiken mit Transparenz |
| AVIF | Nächste Generation, beste Kompression, wachsende Unterstützung |

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

## Listen {#lists}

```html
<ul><li>Unordered item</li></ul>
<ol start="5" type="A"><li>Ordered item</li></ol>
<dl><dt>Term</dt><dd>Definition</dd></dl>
```

Navigationsmenüs verwenden `<nav>` + `<ul>` + `<li>` + `<a>`. Screenreader kündigen "Navigation mit N Einträgen" an.

## Block vs. Inline {#block-vs-inline}

| Block | Inline |
|-------|--------|
| Volle Breite, neue Zeile | Breite des Inhalts, keine neue Zeile |
| `<div>`, `<p>`, `<h1>`-`<h6>`, `<section>`, `<article>`, `<header>`, `<footer>`, `<main>`, `<nav>`, `<form>` | `<span>`, `<a>`, `<strong>`, `<em>`, `<img>`, `<code>`, `<input>`, `<button>` |

`display: inline-block` - Inline-Fluss, berücksichtigt aber Breite/Höhe.

## Semantische HTML5-Elemente {#semantic-html5-elements}

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

| Element | Zweck |
|---------|---------|
| `<header>` | Kopfbereich der Seite/eines Abschnitts |
| `<nav>` | Navigationslinks |
| `<main>` | Hauptinhalt (EINMAL pro Seite) |
| `<section>` | Thematische Gruppierung |
| `<article>` | In sich geschlossener Inhalt |
| `<aside>` | Nur am Rande verwandt |
| `<footer>` | Fußbereich der Seite/eines Abschnitts |

**Warum Semantik wichtig ist**: Barrierefreiheit (Screenreader kündigen Landmarks an), SEO (Suchmaschinen verstehen die Struktur), Wartbarkeit.

## HTML-Entities {#html-entities}

| Entity | Zeichen | Entity | Zeichen |
|--------|---------|--------|---------|
| `&lt;` | < | `&gt;` | > |
| `&amp;` | & | `&quot;` | " |
| `&nbsp;` | (Leerzeichen) | `&copy;` | (c) |

## Stolperfallen {#gotchas}

- **Fehlendes Viewport-Meta**: Mobile Browser rendern mit ca. 980px Breite, wodurch Inhalte winzig wirken
- **Überspringen von Überschriftenebenen**: bricht die Navigation für Screenreader
- **`<div>`-Suppe**: `<div>` für alles verwenden statt semantischer Elemente
- **Fehlendes alt bei Bildern**: Verstoß gegen die Barrierefreiheit, schlechtes SEO
- **Kommentare enthalten sensible Informationen**: sind im Seitenquelltext sichtbar

## Siehe auch {#see-also}

- [[html-tables-and-forms]] - Tabellen, Formulareingaben, Validierung
- [[css-selectors-and-cascade]] - Gestaltung von HTML-Elementen
- [[css-box-model-and-layout]] - Block-/Inline-Anzeigemodell in CSS
