---
title: "CSS Flexbox"
category: concepts
tags: [web-frontend, css, flexbox, layout]
level: 3
source_sha256: 60f5f057fe41da7815cf2a4694315025343a9058ffce6dbe5ae261f067e42512
translation: machine
translated_at: '2026-10-24'
---
Wait — I need to output the translation, not this. Let me produce it.

---
title: CSS Flexbox
category: concepts
tags: [web-frontend, css, flexbox, layout]
---

# CSS Flexbox {#css-flexbox}

Flexbox ist ein eindimensionales Layoutsystem zur Verteilung von Platz und zur Ausrichtung von Elementen entlang einer einzelnen Achse (Zeile oder Spalte). Es hat floatbasierte Layouts für das Design auf Komponentenebene abgelöst.

## Flexbox aktivieren {#enabling-flexbox}

```css
.container { display: flex; }         /* Block-level flex container */
.container { display: inline-flex; }  /* Inline-level */
```

Alle direkten Kindelemente werden automatisch zu **Flex-Items**.

## Container-Eigenschaften {#container-properties}

### Richtung und Umbruch {#direction-and-wrapping}
```css
flex-direction: row;             /* Default: left-to-right */
flex-direction: row-reverse;     /* Right-to-left */
flex-direction: column;          /* Top-to-bottom */
flex-direction: column-reverse;

flex-wrap: nowrap;       /* Default: single line, items shrink */
flex-wrap: wrap;         /* Wrap to next line */

flex-flow: row wrap;     /* Shorthand: direction + wrap */
```

### Ausrichtung auf der Hauptachse (justify-content) {#main-axis-alignment-justify-content}
```css
justify-content: flex-start;      /* Packed to start (default) */
justify-content: flex-end;        /* Packed to end */
justify-content: center;          /* Centered */
justify-content: space-between;   /* First/last at edges, equal gaps */
justify-content: space-around;    /* Equal space around each (edges half) */
justify-content: space-evenly;    /* Equal space everywhere */
```

### Ausrichtung auf der Querachse (align-items) {#cross-axis-alignment-align-items}
```css
align-items: stretch;     /* Default: fill container height */
align-items: flex-start;  /* Top (for row) */
align-items: flex-end;    /* Bottom */
align-items: center;      /* Centered */
align-items: baseline;    /* Text baseline alignment */
```

### Mehrzeilige Querachse (align-content) {#multi-line-cross-axis-align-content}
Gilt nur bei `flex-wrap: wrap`, wenn mehrere Zeilen entstehen:
```css
align-content: flex-start | flex-end | center | space-between | space-around | stretch;
```

### Gap {#gap}
```css
gap: 16px;           /* Row and column gap */
gap: 16px 24px;      /* Row | Column */
```

Moderner Ersatz für Margin-Workarounds. Am äußeren Rand entsteht kein Gap.

## Item-Eigenschaften {#item-properties}

### flex-grow / flex-shrink / flex-basis {#flex-grow-flex-shrink-flex-basis}
```css
flex-grow: 0;      /* Default: don't grow */
flex-grow: 1;      /* Grow to fill available space (proportional) */

flex-shrink: 1;    /* Default: shrink when needed */
flex-shrink: 0;    /* Don't shrink (may overflow) */

flex-basis: auto;  /* Default: use content/width */
flex-basis: 200px; /* Starting size before grow/shrink */
flex-basis: 0;     /* Ignore content, distribute ALL space via grow */
```

### Kurzschreibweise {#shorthand}
```css
flex: 0 1 auto;     /* Default: no grow, shrink, auto basis */
flex: 1;            /* flex: 1 1 0 - grow equally, ignore content */
flex: auto;         /* flex: 1 1 auto - grow, respect content */
flex: none;         /* flex: 0 0 auto - fixed size */
flex: 0 0 200px;   /* Fixed 200px */
```

### Einzelne Item-Überschreibungen {#individual-item-overrides}
```css
.item { align-self: center; }     /* Override align-items for this item */
.item { order: -1; }              /* Move before items with order 0 */
```

`order` wirkt nur visuell – Screenreader folgen der DOM-Reihenfolge.

## Der auto-Margin-Trick {#auto-margin-trick}

```css
.nav-last  { margin-left: auto; }   /* Push to right in row */
.centered  { margin: auto; }        /* Center both axes in flex */
```

`margin: auto` in Flex absorbiert den verbleibenden Platz in dieser Richtung.

## Gängige Muster {#common-patterns}

### Zentrierung (Holy Grail) {#centering-holy-grail}
```css
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}
```

### Horizontale Navigation {#horizontal-navigation}
```css
nav { display: flex; justify-content: space-between; align-items: center; }
.nav-links { display: flex; gap: 24px; list-style: none; }
```

### Kartenzeile (gleiche Höhe) {#card-row-equal-height}
```css
.cards { display: flex; gap: 24px; }
.card { flex: 1; }  /* Equal width */
```

### Footer klebt am unteren Rand {#footer-sticks-to-bottom}
```css
body { display: flex; flex-direction: column; min-height: 100vh; }
main { flex: 1; }       /* Takes remaining space */
footer { flex-shrink: 0; }
```

### Responsives Umbrechen {#responsive-wrapping}
```css
.grid { display: flex; flex-wrap: wrap; gap: 16px; }
.grid-item { flex: 1 1 300px; }  /* Min 300px, wraps when needed */
```

## Flexbox vs. Grid {#flexbox-vs-grid}

| Merkmal | Flexbox | Grid |
|---------|---------|------|
| Dimension | 1D (Zeile ODER Spalte) | 2D (Zeilen UND Spalten) |
| Ideal für | Komponenten (Navigation, Karten) | Seitenlayout, komplexe Raster |
| Inhaltsgesteuert | Ja | Nein (Grid definiert Zellen) |

**Regel**: Flexbox für Komponenten, Grid für Seitenlayouts. Beide lassen sich gut kombinieren.

## Fallstricke {#gotchas}

- **`flex-basis` überschreibt `width`**: in Zeilenrichtung hat `flex-basis` Vorrang vor `width`
- **`flex: 1` entspricht `flex: 1 1 0`**: die Basis ist 0, daher wird der GESAMTE Platz verteilt, nicht nur der verbleibende
- **Standardmäßig `min-width: auto`**: Flex-Items schrumpfen nicht unter ihren Inhalt; überschreiben mit `min-width: 0` oder `overflow: hidden`
- **`order` und Barrierefreiheit**: Änderungen der visuellen Reihenfolge beeinflussen nicht die Tab- oder Screenreader-Reihenfolge
- **`margin: auto` absorbiert Platz**: kann `justify-content` außer Kraft setzen, wenn man das nicht erwartet

## Siehe auch {#see-also}

- [[css-grid]] - 2D-Layoutsystem
- [[css-box-model-and-layout]] - Display, Position, Box-Modell
- [[css-responsive-design]] - Media Queries und flexible Layouts
