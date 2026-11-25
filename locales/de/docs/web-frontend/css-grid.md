---
title: "CSS Grid"
category: concepts
tags: [web-frontend, css, grid, layout]
level: 3
source_sha256: c3ad950e5bf464d10a49f665259afd25c01668ba9e13bfe2d106123e43446ca1
translation: machine
translated_at: '2026-10-24'
---
# CSS Grid {#css-grid}

Grid ist ein zweidimensionales Layoutsystem für Zeilen UND Spalten gleichzeitig. Anders als Flexbox (1D) definiert Grid eine Struktur, die die Elemente füllen.

## Grid aktivieren {#enabling-grid}

```css
.container { display: grid; }
```

Direkte Kindelemente werden zu Grid-Elementen. Sichtbar ändert sich zunächst nichts, bis du Zeilen und Spalten definierst.

## Struktur definieren {#defining-structure}

```css
grid-template-columns: 200px 1fr 200px;        /* Fixed sidebar, flexible center */
grid-template-columns: repeat(3, 1fr);           /* 3 equal columns */
grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));  /* Responsive */
grid-template-rows: 80px 1fr auto;              /* Fixed header, flexible main, auto footer */
```

### Die Einheit `fr` {#the-fr-unit}
`fr` verteilt den verbleibenden Platz nach den festen Größen. `1fr 2fr` ergibt 1/3 + 2/3 des verbleibenden Platzes. `fr` berücksichtigt `gap` automatisch (anders als `%`).

### repeat(), minmax(), auto-fill/auto-fit {#repeat-minmax-auto-fillauto-fit}
```css
repeat(3, 1fr)                              /* 1fr 1fr 1fr */
repeat(auto-fill, minmax(250px, 1fr))       /* Fill: keeps empty tracks */
repeat(auto-fit, minmax(250px, 1fr))        /* Fit: collapses empty tracks, items stretch */
minmax(200px, 1fr)                          /* Min 200px, max 1fr */
```

**Das mit Abstand nützlichste Grid-Muster**: ein responsives Grid ganz ohne Media Queries:
```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
}
```

## Gap {#gap}

```css
gap: 20px;             /* Row and column */
gap: 20px 30px;        /* Row | Column */
```

## Elemente platzieren {#placing-items}

Grid-Linien werden ab 1 nummeriert. Negative Zahlen zählen vom Ende aus.

```css
.item {
  grid-column: 1 / 3;       /* Start line / End line (exclusive) */
  grid-row: 1 / 4;
  grid-column: 1 / span 2;  /* Start at 1, span 2 columns */
  grid-column: span 2;      /* Span 2 from auto position */
  grid-area: 1 / 1 / 4 / 3; /* row-start / col-start / row-end / col-end */
}
```

## grid-template-areas {#grid-template-areas}

```css
.grid {
  display: grid;
  grid-template-columns: 250px 1fr;
  grid-template-rows: 80px 1fr 60px;
  grid-template-areas:
    "header  header"
    "sidebar content"
    "footer  footer";
}
.header  { grid-area: header; }
.sidebar { grid-area: sidebar; }
.content { grid-area: content; }
.footer  { grid-area: footer; }
```

- Jede Zeile ist ein String, Spalten werden durch Leerzeichen getrennt
- Bereiche müssen Rechtecke bilden
- `.` für leere Zellen: `"header ." ". content"`

### Responsiv mit Bereichen {#responsive-with-areas}
```css
@media (max-width: 768px) {
  .grid {
    grid-template-columns: 1fr;
    grid-template-areas: "header" "content" "sidebar" "footer";
  }
}
```

## Auto Flow und implizite Tracks {#auto-flow-and-implicit-tracks}

```css
grid-auto-flow: row;         /* Default: fill rows first */
grid-auto-flow: column;      /* Fill columns first */
grid-auto-flow: dense;       /* Backtrack to fill gaps */
grid-auto-rows: minmax(100px, auto);  /* Height of auto-generated rows */
```

## Ausrichtung {#alignment}

### Alle Elemente (Container) {#all-items-container}
```css
justify-items: stretch | start | end | center;   /* Horizontal in cells */
align-items: stretch | start | end | center;      /* Vertical in cells */
place-items: center;                               /* Both axes shorthand */

justify-content: center;   /* Align entire grid within container */
align-content: center;
place-content: center;
```

### Einzelnes Element {#individual-item}
```css
.item {
  justify-self: center;
  align-self: end;
  place-self: center end;
}
```

## Subgrid {#subgrid}

```css
.parent { display: grid; grid-template-columns: repeat(3, 1fr); }
.nested {
  display: grid;
  grid-template-columns: subgrid;  /* Inherit parent's column tracks */
  grid-column: span 3;
}
```

Subgrid richtet verschachtelte Elemente an den Tracks des übergeordneten Grids aus. Das ist essenziell für Card-Layouts, bei denen sich Inhalte über mehrere Cards hinweg ausrichten sollen.

## Häufige Muster {#common-patterns}

### Holy-Grail-Layout {#holy-grail}
```css
body {
  display: grid;
  grid-template-columns: 250px 1fr 200px;
  grid-template-rows: auto 1fr auto;
  grid-template-areas:
    "header header header"
    "nav    main   aside"
    "footer footer footer";
  min-height: 100vh;
}
```

### Masonry-artiges Layout (Dense Packing) {#masonry-like-dense-packing}
```css
.gallery {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  grid-auto-rows: 200px;
  grid-auto-flow: dense;
  gap: 8px;
}
.tall { grid-row: span 2; }
.wide { grid-column: span 2; }
```

### Überlappende Elemente {#overlapping-elements}
```css
.hero { display: grid; grid-template: 1fr / 1fr; }
.hero > * { grid-area: 1 / 1; }   /* All in same cell = overlap */
.hero-text { z-index: 2; }
```

## Grid vs. Flexbox {#grid-vs-flexbox}

| Grid verwenden | Flexbox verwenden |
|----------------|-------------------|
| 2D-Layout (Zeilen UND Spalten) | 1D (Zeile ODER Spalte) |
| Bekannte Struktur | Inhaltsgesteuerte Größen |
| Elemente richten sich über Zeilen hinweg aus | Elemente brechen natürlich um |
| Komplexe Seitenlayouts | Komponenten-Interna |
| `grid-template-areas` | Einfaches Zentrieren |

Beide lassen sich gut verschachteln: Grid für das Seitenlayout, Flexbox für Komponenten innerhalb der Zellen.

## Stolpersteine {#gotchas}

- **`fr` ist NICHT `%`**: `fr` berücksichtigt Gaps, `%` nicht (kann zu Überläufen führen)
- **`auto-fill` vs. `auto-fit`**: beide sind responsiv, aber `auto-fit` kollabiert leere Tracks
- **Grid-Linien beginnen bei 1**: nicht bei 0
- **`minmax()` ist für Responsivität erforderlich**: `repeat(auto-fit, 1fr)` ist ungültig; benötigt wird `minmax(min, 1fr)`
- **Subgrid erfordert Spanning**: das verschachtelte Element muss sich über die Tracks des übergeordneten Grids erstrecken, damit `subgrid` genutzt werden kann

## Siehe auch {#see-also}

- [[css-flexbox]] - 1D-Layout als Ergänzung
- [[css-responsive-design]] - Media Queries, Viewport-Einheiten
- [[figma-layout-and-components]] - Grid-Design in Figma
