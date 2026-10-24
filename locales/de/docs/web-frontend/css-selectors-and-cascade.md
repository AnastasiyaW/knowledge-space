---
title: "CSS-Selektoren und Kaskade"
category: concepts
tags: [web-frontend, css, selectors, specificity, variables]
level: 3
source_sha256: 01301e8235445276ef3cae8999d14ae4b2dd9e5e58a2b3dd9b79a3f83d59b0ed
translation: machine
translated_at: '2026-10-24'
---
# CSS-Selektoren und Kaskade {#css-selectors-and-cascade}

CSS steuert die Darstellung von HTML. Kaskade, Spezifität und Vererbung bestimmen, welche Stile sich durchsetzen, wenn mehrere Regeln dasselbe Element ansprechen.

## CSS einbinden {#connecting-css}

```html
<link rel="stylesheet" href="css/style.css">   <!-- External (preferred, cacheable) -->
<style>p { color: red; }</style>                 <!-- Internal (in <head>) -->
<p style="color: red;">Text</p>                  <!-- Inline (highest specificity) -->
```

## Selektoren {#selectors}

### Basis {#basic}
```css
*         { }    /* Universal */
p         { }    /* Type */
.card     { }    /* Class */
#header   { }    /* ID (avoid for styling) */
```

### Attribut {#attribute}
```css
[href]              { }    /* Has attribute */
[type="text"]       { }    /* Exact value */
[href^="https"]     { }    /* Starts with */
[href$=".pdf"]      { }    /* Ends with */
[href*="example"]   { }    /* Contains */
[data-theme="dark" i] { }  /* Case-insensitive */
```

### Kombinatoren {#combinators}
```css
div p       { }    /* Descendant (any depth) */
div > p     { }    /* Direct child */
h2 + p      { }    /* Adjacent sibling (immediately after) */
h2 ~ p      { }    /* General sibling (all after, same parent) */
```

### Pseudoklassen (Zustand) {#pseudo-classes-state}
```css
a:hover       { }    a:active      { }    a:visited     { }
a:focus       { }    a:focus-visible { }   /* Keyboard focus only */
input:valid   { }    input:invalid { }    input:required  { }
input:disabled { }   input:checked { }    input:placeholder-shown { }
:empty        { }    :target       { }    :root          { }
```

### Strukturelle Pseudoklassen {#structural-pseudo-classes}
```css
:first-child    { }    :last-child     { }
:nth-child(2)   { }    :nth-child(odd) { }    :nth-child(3n+1) { }
:nth-last-child(2) { } :only-child     { }
:first-of-type  { }    :nth-of-type(2) { }    :only-of-type   { }
```

**Wichtiger Unterschied**: `:nth-child` zählt ALLE Kindelemente. `:nth-of-type` zählt nur Elemente desselben Tags.

### Negation und Logik {#negation-and-logical}
```css
:not(.hidden)     { }    /* Exclude matching */
:is(h1, h2, h3)  { }    /* Match any (forgiving selector list) */
:where(h1, h2)   { }    /* Like :is() but zero specificity */
:has(.icon)       { }    /* Parent selector - element containing .icon */
```

`:has()` ist der lang erwartete „Eltern-Selektor“ – z. B. wählt `.card:has(img)` Karten aus, die ein Bild enthalten.

### Pseudoelemente {#pseudo-elements}
```css
p::first-line    { }    p::first-letter  { }
p::selection     { }    p::placeholder   { }
.item::before { content: ">> "; }
.item::after  { content: ""; display: block; }
```

`::before`/`::after` MÜSSEN die Eigenschaft `content` haben. Sie sind standardmäßig inline und können nicht auf Void-Elemente (`<img>`, `<input>`) angewendet werden.

## Kaskade (Konfliktauflösung) {#cascade-conflict-resolution}

1. **Herkunft und Wichtigkeit**: `!important` > Autorenstile > Browser-Standards
2. **Spezifität**: spezifischerer Selektor gewinnt
3. **Quellreihenfolge**: letzte Regel gewinnt (gleiche Spezifität)

## Spezifität {#specificity}

| Selektortyp | Gewichtung |
|--------------|--------|
| Inline-Style | 1,0,0,0 |
| ID `#id` | 0,1,0,0 |
| Klasse `.class`, `[attr]`, `:pseudo-class` | 0,0,1,0 |
| Element `div`, `::pseudo-element` | 0,0,0,1 |
| Universal `*`, Kombinatoren | 0,0,0,0 |

```css
p                    /* 0,0,0,1 */
.card                /* 0,0,1,0 */
#header .nav li a    /* 0,1,1,2 */
div > p.text:hover   /* 0,0,2,2 */
```

Höhere Spezifität gewinnt IMMER, unabhängig von der Quellreihenfolge. Vermeide `!important` – es bricht die Kaskade.

## Vererbung {#inheritance}

**Vererbt**: `color`, `font-*`, `line-height`, `text-align`, `visibility`, `cursor`, `list-style`
**NICHT vererbt**: `margin`, `padding`, `border`, `background`, `width`, `height`, `display`, `position`

```css
.child { color: inherit; }   /* Force inheritance */
.element { all: unset; }     /* Reset to browser default */
```

## Farben {#colors}

```css
color: #ff0000;                  /* Hex */
color: #f00;                     /* Hex shorthand */
color: rgb(255, 0, 0);          /* RGB */
color: rgba(255, 0, 0, 0.5);    /* RGBA */
color: hsl(0, 100%, 50%);       /* HSL (most intuitive) */
color: hsla(0, 100%, 50%, 0.5);
```

**HSL-Vorteil**: H = Farbkreis (0–360), S = Sättigung (0–100 %), L = Helligkeit (0–100 %). Abdunkeln = L verringern. Aufhellen = L erhöhen. Entsättigen = S verringern. Alles gut vorhersagbar.

`currentColor` übernimmt die Textfarbe – nützlich für Rahmen und SVG-Füllungen.

## Text- und Schrifteigenschaften {#text-and-font-properties}

```css
font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif;
font-size: 1rem;              /* Relative to root (preferred) */
font-weight: 400;             /* Normal=400, Bold=700 */
line-height: 1.5;             /* Unitless multiplier (preferred) */
text-align: left | center | right | justify;
text-decoration: underline wavy red;
text-transform: uppercase | lowercase | capitalize;
letter-spacing: 0.05em;
white-space: nowrap; overflow: hidden; text-overflow: ellipsis;  /* Truncation */
font: italic 700 16px/1.5 'Inter', sans-serif;  /* Shorthand */
```

### Eigene Schriften {#custom-fonts}
```css
@font-face {
  font-family: 'MyFont';
  src: url('fonts/myfont.woff2') format('woff2');
  font-weight: 400;
  font-display: swap;  /* Show fallback immediately, swap when loaded */
}
```

WOFF2 bietet die beste Kompression für moderne Browser. `font-display: swap` verhindert unsichtbaren Text während des Ladens.

## CSS Custom Properties {#css-custom-properties}

```css
:root {
  --color-primary: #3b82f6;
  --spacing-md: 16px;
  --border-radius: 8px;
}
.button {
  background: var(--color-primary);
  padding: var(--spacing-md);
  border-radius: var(--border-radius);
  font-size: var(--font-size-base, 14px);  /* Fallback value */
}
```

- Gültigkeitsbereich: `:root` = global, Element = lokal
- Kaskadieren und vererben sich wie reguläre Eigenschaften
- Dynamisch per JS: `element.style.setProperty('--color', 'red')`
- Anders als SASS-Variablen sind CSS-Variablen live und kaskadieren

## Fallstricke {#gotchas}

- **Übermäßiger Einsatz von `!important`**: erzeugt Wartungsprobleme und ist schwer zu überschreiben
- **ID-Selektoren für Styling**: zu spezifisch, Klassen bevorzugen
- **`:nth-child` vs. `:nth-of-type`**: Zählung umfasst ALLE Geschwister vs. nur Geschwister desselben Typs
- **`em` bei Kaskadierung**: `em` für font-size = relativ zum Elternelement; für andere Eigenschaften = relativ zur eigenen font-size des Elements
- **Prozentuale Höhe**: funktioniert nur, wenn das Elternelement eine explizite Höhe hat

## Siehe auch {#see-also}

- [[css-box-model-and-layout]] - Display, Position, Einheiten
- [[css-sass-and-methodology]] - BEM-Namenskonventionen, SASS-Präprozessing
- [[html-fundamentals]] - HTML-Elemente, auf die CSS zielt
