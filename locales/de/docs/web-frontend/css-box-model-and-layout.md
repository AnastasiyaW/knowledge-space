---
title: "CSS-Box-Modell und Layout"
category: concepts
tags: [web-frontend, css, box-model, position, units]
level: 3
source_sha256: bcd6ba9c2193c5ba624541a65fe571242484c2b54a92b157be6fd0639442dca4
translation: machine
translated_at: '2026-10-24'
---
Wait, I should not output placeholders like that. Let me produce the full translation properly.

---
title: CSS-Box-Modell und Layout
category: concepts
tags: [web-frontend, css, box-model, position, units]
---

# CSS-Box-Modell und Layout {#css-box-model-and-layout}

Jedes HTML-Element ist ein rechteckiger Kasten mit vier Schichten. Das Verständnis von Box-Modell, Display, Position und Einheiten bildet die Grundlage für jedes CSS-Layout.

## Box-Modell {#box-model}

```text
┌────────── Margin ──────────┐
│  ┌──────── Border ──────┐  │
│  │  ┌──── Padding ────┐ │  │
│  │  │  Content area    │ │  │
│  │  └─────────────────┘ │  │
│  └──────────────────────┘  │
└────────────────────────────┘
```

### border-box (immer verwenden) {#border-box-always-use}
```css
*, *::before, *::after { box-sizing: border-box; }
```

| Box-sizing | `width: 200px; padding: 20px; border: 2px` |
|-----------|---------------------------------------------|
| `content-box` (Standard) | Gesamt = 244px |
| `border-box` | Gesamt = 200px (Inhalt schrumpft auf 156px) |

## Breite und Höhe {#width-and-height}

```css
width: 300px;  width: 50%;  width: auto;
min-width: 200px;  max-width: 800px;
height: 100px;  min-height: 100vh;
overflow: visible | hidden | scroll | auto;
overflow-x: auto;  overflow-y: auto;
```

**Stolperfalle**: Eine prozentuale `height` funktioniert nur, wenn das übergeordnete Element eine explizite Höhe hat. Eine prozentuale `width` funktioniert immer.

## Padding {#padding}

```css
padding: 20px;                   /* All sides */
padding: 10px 20px;             /* Vertical | Horizontal */
padding: 10px 20px 15px 25px;   /* Top Right Bottom Left (clockwise) */
```

- Darf nicht negativ sein
- Der Hintergrund erstreckt sich über das Padding
- Prozentuales Padding bezieht sich auf die BREITE des übergeordneten Elements (auch oben/unten)

## Border {#border}

```css
border: 1px solid #333;
border-radius: 8px;             /* Rounded corners */
border-radius: 50%;             /* Perfect circle (square element) */
outline: 2px solid blue;        /* Outside box model, no layout impact */
outline-offset: 4px;
```

**Border vs. Outline**: Border beansprucht Platz im Box-Modell, Outline nicht. Outline wird für Fokusindikatoren verwendet.

## Margin {#margin}

```css
margin: 20px;
margin: 0 auto;                 /* Center block horizontally (requires width) */
margin-top: -20px;              /* Negative margins pull element */
```

### Margin-Collapsing {#margin-collapsing}
Benachbarte vertikale Margins verschmelzen – nur der größere gilt:
```css
.top    { margin-bottom: 30px; }
.bottom { margin-top: 20px; }
/* Gap = 30px, NOT 50px */
```

- Nur vertikale Margins kollabieren (nicht horizontale)
- Passiert NICHT innerhalb von Flex-/Grid-Containern
- Passiert NICHT, wenn Padding/Border die Margins von Eltern- und Kindelement trennt

## Display {#display}

```css
display: block;          /* Full width, new line */
display: inline;         /* Flows with text, ignores width/height */
display: inline-block;   /* Inline flow + respects width/height */
display: none;           /* Removed from layout entirely */
display: flex;           /* Flex container */
display: grid;           /* Grid container */
```

`display: none` entfernt das Element aus dem Layout. `visibility: hidden` blendet es aus, behält aber den Platz.

## Position {#position}

```css
position: static;     /* Default: normal flow */
position: relative;   /* Offset from normal position, still takes space */
position: absolute;   /* Removed from flow, relative to nearest positioned ancestor */
position: fixed;      /* Relative to viewport, stays on scroll */
position: sticky;     /* Normal until scroll threshold, then fixed */
```

### Relative + Absolute Muster {#relative-absolute-pattern}
```css
.parent { position: relative; }   /* Establishes context */
.child  { position: absolute; top: 0; right: 0; }  /* Positioned within parent */
```

### Sticky {#sticky}
```css
.nav { position: sticky; top: 0; z-index: 100; }
```
Benötigt einen Wert für `top`/`bottom`. Funktioniert nur innerhalb seines umschließenden Blocks.

### z-index {#z-index}
Funktioniert nur bei positionierten Elementen (nicht `static`). Gängige Skala: Inhalt 0, Header 100, Dropdowns 200, Modals 1000, Toasts 2000.

## Float (veraltet) {#float-legacy}

```css
.image { float: left; }   /* Text wraps around */
.container::after { content: ""; display: table; clear: both; }  /* Clearfix */
```

Float ist für Layouts veraltet. Verwenden Sie Flexbox/Grid. Float bleibt nützlich für Textumfluss um Bilder.

## CSS-Einheiten {#css-units}

### Relative Einheiten {#relative-units}
| Einheit | Bezug | Verwendung |
|------|-------------|-----|
| `rem` | Root-Schriftgröße (standardmäßig 16px) | Schriftgrößen, Abstände (bevorzugt) |
| `em` | Schriftgröße des Elternelements (bei font-size) / eigene Schriftgröße (sonst) | Abstände relativ zum Text |
| `%` | Eigenschaft des Elternelements | Breiten, Padding |
| `vw`/`vh` | 1 % der Viewport-Breite/-Höhe | Volle Breite/Höhe |
| `dvh` | Dynamische Viewport-Höhe | Vollhöhe auf Mobilgeräten (berücksichtigt die Browserleiste) |
| `ch` | Breite des Zeichens "0" | Breiten von Eingabefeldern |

### Praktische Empfehlungen {#practical-recommendations}
- **Schriftgrößen**: `rem` (konsistent, barrierefrei, skaliert mit der Benutzereinstellung)
- **Abstände**: `rem` oder `px`
- **Breiten**: `%` für flexibel, `max-width` für Begrenzungen
- **Höhen**: Feste Werte vermeiden, stattdessen `min-height` verwenden
- **Vollhöhe auf Mobilgeräten**: `100dvh` (nicht `100vh`, das die Browserleiste auf Mobilgeräten ignoriert)

### em vs. rem {#em-vs-rem}
```css
html { font-size: 16px; }
.parent { font-size: 20px; }
.child {
  font-size: 1.5em;    /* 30px (1.5 * parent's 20px) */
  font-size: 1.5rem;   /* 24px (1.5 * root's 16px) */
  padding: 1em;        /* relative to element's OWN font-size */
}
```

## Hintergrund {#background}

```css
background: #f5f5f5 url('image.jpg') no-repeat center/cover;

/* Multiple backgrounds with dark overlay */
background:
  linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)),
  url('image.jpg') center/cover;

/* Gradients */
background: linear-gradient(135deg, #667eea, #764ba2);
background: radial-gradient(circle, #3b82f6, transparent);
```

`background-size: cover` füllt und beschneidet. `contain` passt das Bild vollständig ein.

## Stolperfallen {#gotchas}

- **Vergessenes `border-box`**: Elemente sind größer als erwartet
- **`100vh` auf Mobilgeräten**: läuft über, da die Adressleiste ignoriert wird – stattdessen `100dvh` verwenden
- **Überraschungen durch Margin-Collapsing**: vertikale Margins zwischen Geschwistern verschmelzen
- **Prozentuales Padding oben/unten**: bezieht sich auf die BREITE des Elternelements, nicht auf die Höhe
- **`z-index` ohne position**: hat keine Wirkung auf `static`-Elemente
- **`em`-Kaskadierung**: `em` potenziert sich durch verschachtelte Elemente, `rem` bleibt konsistent

## Siehe auch {#see-also}

- [[css-flexbox]] - 1D-Layoutsystem
- [[css-grid]] - 2D-Layoutsystem
- [[css-responsive-design]] - Viewport-Einheiten, Media Queries, flexible Größen
- [[css-selectors-and-cascade]] - Auswahl der Elemente für die Gestaltung
