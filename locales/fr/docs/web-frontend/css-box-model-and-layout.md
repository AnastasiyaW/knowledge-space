---
title: "Modèle de boîte CSS et mise en page"
category: concepts
tags: [web-frontend, css, box-model, position, units]
level: 3
source_sha256: bcd6ba9c2193c5ba624541a65fe571242484c2b54a92b157be6fd0639442dca4
translation: machine
translated_at: '2026-10-24'
---
# Modèle de boîte CSS et mise en page {#css-box-model-and-layout}

Chaque élément HTML est une boîte rectangulaire composée de quatre couches. Comprendre le modèle de boîte, `display`, `position` et les unités est fondamental pour toute mise en page CSS.

## Modèle de boîte {#box-model}

```text
┌────────── Margin ──────────┐
│  ┌──────── Border ──────┐  │
│  │  ┌──── Padding ────┐ │  │
│  │  │  Content area    │ │  │
│  │  └─────────────────┘ │  │
│  └──────────────────────┘  │
└────────────────────────────┘
```

### border-box (à utiliser systématiquement) {#border-box-always-use}
```css
*, *::before, *::after { box-sizing: border-box; }
```

| Box-sizing | `width: 200px; padding: 20px; border: 2px` |
|-----------|---------------------------------------------|
| `content-box` (par défaut) | Total = 244px |
| `border-box` | Total = 200px (le contenu se réduit à 156px) |

## Largeur et hauteur {#width-and-height}

```css
width: 300px;  width: 50%;  width: auto;
min-width: 200px;  max-width: 800px;
height: 100px;  min-height: 100vh;
overflow: visible | hidden | scroll | auto;
overflow-x: auto;  overflow-y: auto;
```

**Piège** : la `height` en pourcentage ne fonctionne que si le parent a une hauteur explicite. La `width` en pourcentage fonctionne toujours.

## Padding {#padding}

```css
padding: 20px;                   /* All sides */
padding: 10px 20px;             /* Vertical | Horizontal */
padding: 10px 20px 15px 25px;   /* Top Right Bottom Left (clockwise) */
```

- Ne peut pas être négatif
- Le fond s'étend à travers le padding
- Le padding en pourcentage est relatif à la LARGEUR du parent (y compris pour le haut et le bas)

## Border {#border}

```css
border: 1px solid #333;
border-radius: 8px;             /* Rounded corners */
border-radius: 50%;             /* Perfect circle (square element) */
outline: 2px solid blue;        /* Outside box model, no layout impact */
outline-offset: 4px;
```

**Border vs Outline** : `border` occupe de la place dans le modèle de boîte, `outline` non. `outline` est utilisé pour les indicateurs de focus.

## Margin {#margin}

```css
margin: 20px;
margin: 0 auto;                 /* Center block horizontally (requires width) */
margin-top: -20px;              /* Negative margins pull element */
```

### Fusion des marges (margin collapsing) {#margin-collapsing}
Les marges verticales adjacentes fusionnent : seule la plus grande s'applique :
```css
.top    { margin-bottom: 30px; }
.bottom { margin-top: 20px; }
/* Gap = 30px, NOT 50px */
```

- Seules les marges verticales fusionnent (pas les horizontales)
- Cela ne se produit PAS à l'intérieur des conteneurs flex/grid
- Cela ne se produit PAS lorsque padding/border séparent les marges du parent et de l'enfant

## Display {#display}

```css
display: block;          /* Full width, new line */
display: inline;         /* Flows with text, ignores width/height */
display: inline-block;   /* Inline flow + respects width/height */
display: none;           /* Removed from layout entirely */
display: flex;           /* Flex container */
display: grid;           /* Grid container */
```

`display: none` retire l'élément de la mise en page. `visibility: hidden` le masque mais conserve l'espace.

## Position {#position}

```css
position: static;     /* Default: normal flow */
position: relative;   /* Offset from normal position, still takes space */
position: absolute;   /* Removed from flow, relative to nearest positioned ancestor */
position: fixed;      /* Relative to viewport, stays on scroll */
position: sticky;     /* Normal until scroll threshold, then fixed */
```

### Motif relative + absolute {#relative-absolute-pattern}
```css
.parent { position: relative; }   /* Establishes context */
.child  { position: absolute; top: 0; right: 0; }  /* Positioned within parent */
```

### Sticky {#sticky}
```css
.nav { position: sticky; top: 0; z-index: 100; }
```
Nécessite une valeur de `top`/`bottom`. Ne fonctionne que dans son bloc conteneur.

### z-index {#z-index}
Ne fonctionne que sur les éléments positionnés (pas `static`). Échelle courante : contenu 0, en-têtes 100, menus déroulants 200, modales 1000, toasts 2000.

## Float (héritage) {#float-legacy}

```css
.image { float: left; }   /* Text wraps around */
.container::after { content: ""; display: table; clear: both; }  /* Clearfix */
```

`float` est un mécanisme hérité pour la mise en page. Utilisez Flexbox/Grid. `float` reste utile pour faire contourner le texte autour des images.

## Unités CSS {#css-units}

### Unités relatives {#relative-units}
| Unité | Relative à | Usage |
|------|-------------|-----|
| `rem` | Taille de police racine (16px par défaut) | Tailles de police, espacements (recommandé) |
| `em` | Taille de police du parent (pour `font-size`) / taille de police propre (autres) | Espacement relatif au texte |
| `%` | Propriété du parent | Largeurs, padding |
| `vw`/`vh` | 1 % de la largeur/hauteur de la fenêtre | Pleine largeur/hauteur |
| `dvh` | Hauteur de fenêtre dynamique | Pleine hauteur sur mobile (tient compte de la barre du navigateur) |
| `ch` | Largeur du caractère « 0 » | Largeurs de champs de saisie |

### Recommandations pratiques {#practical-recommendations}
- **Tailles de police** : `rem` (cohérent, accessible, s'adapte aux préférences de l'utilisateur)
- **Espacements** : `rem` ou `px`
- **Largeurs** : `%` pour le fluide, `max-width` pour les contraintes
- **Hauteurs** : éviter les valeurs fixes, utiliser `min-height`
- **Pleine hauteur sur mobile** : `100dvh` (et non `100vh`, qui ignore la barre du navigateur mobile)

### em vs rem {#em-vs-rem}
```css
html { font-size: 16px; }
.parent { font-size: 20px; }
.child {
  font-size: 1.5em;    /* 30px (1.5 * parent's 20px) */
  font-size: 1.5rem;   /* 24px (1.5 * root's 16px) */
  padding: 1em;        /* relative to element's OWN font-size */
}
```

## Arrière-plan {#background}

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

`background-size: cover` remplit et recadre. `contain` ajuste l'image entièrement.

## Pièges {#gotchas}

- **Oublier `border-box`** : éléments plus grands que prévu
- **`100vh` sur mobile** : déborde car il ignore la barre d'adresse, utiliser `100dvh`
- **Surprises de fusion des marges** : les marges verticales entre frères et sœurs fusionnent
- **Padding haut/bas en pourcentage** : relatif à la LARGEUR du parent, pas à sa hauteur
- **`z-index` sans position** : sans effet sur les éléments `static`
- **Cascade de `em`** : `em` se cumule à travers les éléments imbriqués, `rem` reste constant

## Voir aussi {#see-also}

- [[css-flexbox]] - Système de mise en page 1D
- [[css-grid]] - Système de mise en page 2D
- [[css-responsive-design]] - Unités de fenêtre, media queries, dimensionnement fluide
- [[css-selectors-and-cascade]] - Sélection des éléments à styliser
