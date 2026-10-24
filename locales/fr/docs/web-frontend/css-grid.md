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

Grid est un système de mise en page à 2 dimensions, pour les lignes ET les colonnes simultanément. Contrairement à Flexbox (1D), Grid définit une structure que les éléments viennent remplir.

## Activer Grid {#enabling-grid}

```css
.container { display: grid; }
```

Les enfants directs deviennent des éléments de grille. Rien de visible ne change tant que vous n'avez pas défini les lignes et les colonnes.

## Définir la structure {#defining-structure}

```css
grid-template-columns: 200px 1fr 200px;        /* Fixed sidebar, flexible center */
grid-template-columns: repeat(3, 1fr);           /* 3 equal columns */
grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));  /* Responsive */
grid-template-rows: 80px 1fr auto;              /* Fixed header, flexible main, auto footer */
```

### L'unité `fr` {#the-fr-unit}
`fr` répartit l'espace restant après les tailles fixes. `1fr 2fr` = 1/3 + 2/3 de l'espace restant. `fr` prend automatiquement en compte `gap` (contrairement à `%`).

### repeat(), minmax(), auto-fill/auto-fit {#repeat-minmax-auto-fillauto-fit}
```css
repeat(3, 1fr)                              /* 1fr 1fr 1fr */
repeat(auto-fill, minmax(250px, 1fr))       /* Fill: keeps empty tracks */
repeat(auto-fit, minmax(250px, 1fr))        /* Fit: collapses empty tracks, items stretch */
minmax(200px, 1fr)                          /* Min 200px, max 1fr */
```

**Le motif Grid le plus utile** : une grille responsive sans media queries :
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

## Placer les éléments {#placing-items}

Les lignes de grille sont numérotées à partir de 1. Les nombres négatifs comptent depuis la fin.

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

- Chaque ligne est une chaîne de caractères, les colonnes étant séparées par des espaces
- Les zones doivent former des rectangles
- `.` pour les cellules vides : `"header ." ". content"`

### Responsive avec les zones {#responsive-with-areas}
```css
@media (max-width: 768px) {
  .grid {
    grid-template-columns: 1fr;
    grid-template-areas: "header" "content" "sidebar" "footer";
  }
}
```

## Flux automatique et pistes implicites {#auto-flow-and-implicit-tracks}

```css
grid-auto-flow: row;         /* Default: fill rows first */
grid-auto-flow: column;      /* Fill columns first */
grid-auto-flow: dense;       /* Backtrack to fill gaps */
grid-auto-rows: minmax(100px, auto);  /* Height of auto-generated rows */
```

## Alignement {#alignment}

### Tous les éléments (conteneur) {#all-items-container}
```css
justify-items: stretch | start | end | center;   /* Horizontal in cells */
align-items: stretch | start | end | center;      /* Vertical in cells */
place-items: center;                               /* Both axes shorthand */

justify-content: center;   /* Align entire grid within container */
align-content: center;
place-content: center;
```

### Élément individuel {#individual-item}
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

Subgrid aligne les éléments imbriqués sur les pistes du parent, ce qui est indispensable pour les mises en page en cartes où le contenu doit s'aligner d'une carte à l'autre.

## Motifs courants {#common-patterns}

### Holy Grail {#holy-grail}
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

### Type maçonnerie (empaquetage dense) {#masonry-like-dense-packing}
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

### Éléments qui se chevauchent {#overlapping-elements}
```css
.hero { display: grid; grid-template: 1fr / 1fr; }
.hero > * { grid-area: 1 / 1; }   /* All in same cell = overlap */
.hero-text { z-index: 2; }
```

## Grid ou Flexbox {#grid-vs-flexbox}

| Utiliser Grid | Utiliser Flexbox |
|----------|-------------|
| Mise en page 2D (lignes ET colonnes) | 1D (ligne OU colonne) |
| Structure connue | Tailles dictées par le contenu |
| Éléments alignés entre les lignes | Éléments qui passent naturellement à la ligne |
| Mises en page de pages complexes | Composants internes |
| `grid-template-areas` | Centrage simple |

Ils se combinent bien : Grid pour la mise en page de la page, Flexbox pour les composants à l'intérieur des cellules.

## Pièges {#gotchas}

- **`fr` n'est PAS `%`** : `fr` prend en compte les gaps, `%` non (risque de débordement)
- **`auto-fill` ou `auto-fit`** : tous deux responsives, mais `auto-fit` supprime les pistes vides
- **La numérotation des lignes de grille commence à 1** : pas à 0
- **`minmax()` requis pour le responsive** : `repeat(auto-fit, 1fr)` est invalide ; il faut `minmax(min, 1fr)`
- **Subgrid exige un élément qui s'étend** : l'élément imbriqué doit couvrir les pistes du parent pour utiliser `subgrid`

## Voir aussi {#see-also}

- [[css-flexbox]] - compagnon de mise en page 1D
- [[css-responsive-design]] - Media queries, unités de viewport
- [[figma-layout-and-components]] - Conception de grilles dans Figma
