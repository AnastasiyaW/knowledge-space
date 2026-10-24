---
title: "Conception CSS responsive"
category: concepts
tags: [web-frontend, css, responsive, media-queries, mobile-first]
level: 3
source_sha256: 78c2c3bbcc6ac26b07503b53685a126255d9eb88e2ba6d6d1d73b22d5a56793b
translation: machine
translated_at: '2026-10-24'
---
# Conception CSS responsive {#css-responsive-design}

Une seule base de code s'adapte à toutes les tailles d'écran. Environ 60 % du trafic web provient du mobile ; Google indexe selon une approche mobile-first.

## Balise meta viewport {#viewport-meta-tag}

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

**Indispensable sur chaque page responsive.** Sans elle, les navigateurs mobiles effectuent le rendu sur une largeur d'environ 980px et dézooment.

## Media queries {#media-queries}

```css
/* Mobile-first (recommended) */
.container { padding: 16px; }

@media (min-width: 768px) {
  .container { padding: 32px; }
}
@media (min-width: 1024px) {
  .container { padding: 64px; max-width: 1200px; margin: 0 auto; }
}
```

### Syntaxe {#syntax}
```css
@media screen and (min-width: 768px) { }
@media (max-width: 767px) { }
@media (min-width: 768px) and (max-width: 1023px) { }
@media (orientation: landscape) { }
@media (prefers-color-scheme: dark) { }
@media (prefers-reduced-motion: reduce) { }
@media (hover: hover) { }        /* Has hover capability */
@media (pointer: coarse) { }     /* Touch screen */

/* Modern range syntax (Level 4) */
@media (768px <= width <= 1024px) { }
```

### Points de rupture courants {#common-breakpoints}
| Point de rupture | Cible |
|-----------|--------|
| 375px | iPhone SE/12 mini |
| 768px | Tablettes |
| 1024px | Petits ordinateurs portables |
| 1200px | Ordinateurs de bureau |
| 1440px | Grands écrans de bureau |

### Mobile-first ou desktop-first {#mobile-first-vs-desktop-first}
**Mobile-first** (`min-width`) : amélioration progressive, CSS plus léger pour le mobile, hiérarchisation du contenu imposée. Recommandé.

**Desktop-first** (`max-width`) : surcharge en descendant. Approche plus ancienne.

## Unités de viewport {#viewport-units}

```css
width: 100vw;        /* 100% viewport width */
height: 100dvh;      /* Dynamic viewport height (mobile-friendly) */
height: 100svh;      /* Small viewport (bar visible) */
height: 100lvh;      /* Large viewport (bar hidden) */
```

**Problème de `100vh` sur mobile** : la barre d'adresse du navigateur mobile apparaît et disparaît, provoquant un débordement. Utilisez `100dvh` pour les sections plein écran sur mobile.

## Typographie fluide avec clamp() {#fluid-typography-with-clamp}

```css
h1 { font-size: clamp(1.5rem, 4vw, 3rem); }
p  { font-size: clamp(1rem, 1rem + 0.5vw, 1.25rem); }
```

- **min** : plancher d'accessibilité (ne descend jamais en dessous)
- **preferred** : s'adapte à la taille du viewport
- **max** : plafond de lisibilité (ne dépasse jamais)
- Supprime, dans la plupart des cas, les media queries pour les tailles de police

## calc(), min(), max() {#calc-min-max}

```css
width: calc(100% - 40px);        /* Mixed unit arithmetic */
width: min(100%, 800px);          /* Full width, max 800px */
width: max(300px, 50%);           /* At least 300px */
padding: clamp(16px, 4vw, 64px);
```

**calc() exige des espaces** autour des opérateurs : `calc(100% - 20px)` et non `calc(100%-20px)`.

## Images responsives {#responsive-images}

```html
<img src="photo.jpg" alt="..." style="max-width: 100%; height: auto;">

<!-- Art direction -->
<picture>
  <source media="(min-width: 1024px)" srcset="photo-desktop.jpg">
  <source media="(min-width: 768px)" srcset="photo-tablet.jpg">
  <img src="photo-mobile.jpg" alt="Description">
</picture>

<!-- Resolution switching -->
<img src="photo-400.jpg"
     srcset="photo-400.jpg 400w, photo-800.jpg 800w, photo-1200.jpg 1200w"
     sizes="(max-width: 600px) 100vw, (max-width: 1200px) 50vw, 600px"
     alt="Description">
```

### object-fit {#object-fit}
```css
.card-image {
  width: 100%; height: 200px;
  object-fit: cover;          /* Fill + crop (like background-size: cover) */
  object-position: center;
}
```

| Valeur | Comportement |
|-------|----------|
| `fill` | Étire (déforme) |
| `contain` | Ajuste en conservant le ratio (peut laisser des bandes) |
| `cover` | Remplit et recadre en conservant le ratio |
| `none` | Taille d'origine |

## Patterns de mise en page {#layout-patterns}

### Conteneur avec max-width {#container-with-max-width}
```css
.container {
  width: 100%; max-width: 1200px;
  margin: 0 auto; padding: 0 16px;
}
```

### Grille responsive (sans media queries) {#responsive-grid-no-media-queries}
```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
}
```

### Menu hamburger {#hamburger-menu}
```css
.nav-links { display: flex; gap: 24px; }
.hamburger { display: none; }

@media (max-width: 768px) {
  .nav-links { display: none; }
  .nav-links.active {
    display: flex; position: fixed;
    inset: 0; flex-direction: column;
    justify-content: center; align-items: center;
  }
  .hamburger { display: block; }
}
```

## Pièges à éviter {#gotchas}

- **Balise meta viewport absente** : tout s'affiche minuscule sur mobile
- **`100vh` sur mobile** : la barre d'adresse provoque un débordement, utilisez `100dvh`
- **`:hover` sur écran tactile** : les effets au survol ne fonctionnent pas ; utilisez `@media (hover: hover)` pour les styles réservés au survol
- **Tester uniquement aux points de rupture standard** : redimensionnez lentement la fenêtre pour trouver où la mise en page casse réellement
- **`vw` provoquant un défilement horizontal** : `100vw` inclut la largeur de la barre de défilement ; utilisez `100%` pour la largeur du conteneur

## Voir aussi {#see-also}

- [[css-grid]] - Motifs de grille à adaptation automatique
- [[css-flexbox]] - Retour à la ligne responsive avec flex
- [[css-box-model-and-layout]] - Unités de viewport, dimensionnement
- [[figma-design-workflow]] - Concevoir pour plusieurs points de rupture
