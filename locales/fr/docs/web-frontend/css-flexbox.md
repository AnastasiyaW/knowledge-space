---
title: "Flexbox CSS"
category: concepts
tags: [web-frontend, css, flexbox, layout]
level: 3
source_sha256: 60f5f057fe41da7815cf2a4694315025343a9058ffce6dbe5ae261f067e42512
translation: machine
translated_at: '2026-10-24'
---
# Flexbox CSS {#css-flexbox}

Flexbox est un système de mise en page unidimensionnel permettant de répartir l'espace et d'aligner les éléments le long d'un seul axe (ligne ou colonne). Il a remplacé les mises en page basées sur `float` pour la conception au niveau des composants.

## Activer Flexbox {#enabling-flexbox}

```css
.container { display: flex; }         /* Block-level flex container */
.container { display: inline-flex; }  /* Inline-level */
```

Tous les enfants directs deviennent automatiquement des **flex items** (éléments flex).

## Propriétés du conteneur {#container-properties}

### Direction et retour à la ligne {#direction-and-wrapping}
```css
flex-direction: row;             /* Default: left-to-right */
flex-direction: row-reverse;     /* Right-to-left */
flex-direction: column;          /* Top-to-bottom */
flex-direction: column-reverse;

flex-wrap: nowrap;       /* Default: single line, items shrink */
flex-wrap: wrap;         /* Wrap to next line */

flex-flow: row wrap;     /* Shorthand: direction + wrap */
```

### Alignement sur l'axe principal (justify-content) {#main-axis-alignment-justify-content}
```css
justify-content: flex-start;      /* Packed to start (default) */
justify-content: flex-end;        /* Packed to end */
justify-content: center;          /* Centered */
justify-content: space-between;   /* First/last at edges, equal gaps */
justify-content: space-around;    /* Equal space around each (edges half) */
justify-content: space-evenly;    /* Equal space everywhere */
```

### Alignement sur l'axe transversal (align-items) {#cross-axis-alignment-align-items}
```css
align-items: stretch;     /* Default: fill container height */
align-items: flex-start;  /* Top (for row) */
align-items: flex-end;    /* Bottom */
align-items: center;      /* Centered */
align-items: baseline;    /* Text baseline alignment */
```

### Axe transversal multi-ligne (align-content) {#multi-line-cross-axis-align-content}
S'applique uniquement avec `flex-wrap: wrap` lorsque plusieurs lignes sont créées :
```css
align-content: flex-start | flex-end | center | space-between | space-around | stretch;
```

### Gap {#gap}
```css
gap: 16px;           /* Row and column gap */
gap: 16px 24px;      /* Row | Column */
```

Remplacement moderne des astuces à base de marges. Aucun espacement sur les bords extérieurs.

## Propriétés des éléments {#item-properties}

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

### Raccourci {#shorthand}
```css
flex: 0 1 auto;     /* Default: no grow, shrink, auto basis */
flex: 1;            /* flex: 1 1 0 - grow equally, ignore content */
flex: auto;         /* flex: 1 1 auto - grow, respect content */
flex: none;         /* flex: 0 0 auto - fixed size */
flex: 0 0 200px;   /* Fixed 200px */
```

### Surcharges individuelles {#individual-item-overrides}
```css
.item { align-self: center; }     /* Override align-items for this item */
.item { order: -1; }              /* Move before items with order 0 */
```

`order` ne modifie que l'affichage visuel : les lecteurs d'écran suivent l'ordre du DOM.

## Astuce de la marge auto {#auto-margin-trick}

```css
.nav-last  { margin-left: auto; }   /* Push to right in row */
.centered  { margin: auto; }        /* Center both axes in flex */
```

`margin: auto` dans un conteneur flex absorbe l'espace restant dans cette direction.

## Schémas courants {#common-patterns}

### Centrage (Holy Grail) {#centering-holy-grail}
```css
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}
```

### Navigation horizontale {#horizontal-navigation}
```css
nav { display: flex; justify-content: space-between; align-items: center; }
.nav-links { display: flex; gap: 24px; list-style: none; }
```

### Ligne de cartes (hauteur égale) {#card-row-equal-height}
```css
.cards { display: flex; gap: 24px; }
.card { flex: 1; }  /* Equal width */
```

### Pied de page collé en bas {#footer-sticks-to-bottom}
```css
body { display: flex; flex-direction: column; min-height: 100vh; }
main { flex: 1; }       /* Takes remaining space */
footer { flex-shrink: 0; }
```

### Retour à la ligne adaptatif {#responsive-wrapping}
```css
.grid { display: flex; flex-wrap: wrap; gap: 16px; }
.grid-item { flex: 1 1 300px; }  /* Min 300px, wraps when needed */
```

## Flexbox ou Grid {#flexbox-vs-grid}

| Caractéristique | Flexbox | Grid |
|-----------------|---------|------|
| Dimension | 1D (ligne OU colonne) | 2D (lignes ET colonnes) |
| Idéal pour | Composants (navigation, cartes) | Mise en page de page, grilles complexes |
| Piloté par le contenu | Oui | Non (la grille définit les cellules) |

**Règle** : Flexbox pour le niveau composant, Grid pour le niveau page. Les deux se combinent très bien.

## Pièges courants {#gotchas}

- **`flex-basis` prime sur `width`** : dans une direction en ligne, `flex-basis` est prioritaire sur `width`
- **`flex: 1` équivaut à `flex: 1 1 0`** : la base est 0, ce qui répartit TOUT l'espace et non seulement l'espace restant
- **`min-width: auto` par défaut** : les flex items ne rétrécissent pas en dessous de leur contenu ; annulez ce comportement avec `min-width: 0` ou `overflow: hidden`
- **Accessibilité de `order`** : les changements d'ordre visuel n'affectent pas l'ordre de tabulation ni celui des lecteurs d'écran
- **`margin: auto` absorbe l'espace** : peut casser `justify-content` si vous ne vous y attendez pas

## Voir aussi {#see-also}

- [[css-grid]] - Système de mise en page 2D
- [[css-box-model-and-layout]] - Display, position, modèle de boîte
- [[css-responsive-design]] - Media queries et mises en page fluides
