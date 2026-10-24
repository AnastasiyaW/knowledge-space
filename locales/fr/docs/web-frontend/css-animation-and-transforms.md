---
title: "Animations CSS et transformations"
category: concepts
tags: [web-frontend, css, animation, transitions, transforms, performance]
level: 3
source_sha256: 8b2350c73cdbcb5ebc4e783c29189a3c459f4f7b45cc0879610125bfed6fa1ef
translation: machine
translated_at: '2026-10-24'
---
# Animations CSS et transformations {#css-animation-and-transforms}

Les animations CSS sont accélérées par le GPU, déclaratives et ne bloquent pas le thread principal. N'utilisez les animations JS que pour la création dynamique, l'orchestration complexe ou les mouvements basés sur la physique.

## Transitions {#transitions}

Animer les changements de propriétés en douceur. Nécessite un déclencheur de changement d'état (survol, bascule de classe).

```css
.button {
  background: #3b82f6;
  transform: scale(1);
  transition: background 0.3s ease, transform 0.2s ease;
}
.button:hover {
  background: #2563eb;
  transform: scale(1.05);
}
```

### Propriétés de transition {#transition-properties}
```css
transition-property: background, transform, opacity;
transition-duration: 0.3s;
transition-timing-function: ease;
transition-delay: 0.1s;

/* Shorthand */
transition: property duration timing delay;
transition: all 0.3s ease 0s;

/* Multiple with different timings */
transition: background 0.3s ease, transform 0.2s ease-out;
```

### Fonctions de temporisation {#timing-functions}
```css
linear                              /* Constant speed */
ease                                /* Default: slow-fast-slow */
ease-in                             /* Slow start (elements exiting) */
ease-out                            /* Fast start, slow end (most natural for UI) */
ease-in-out                         /* Slow both ends */
cubic-bezier(0.4, 0.0, 0.2, 1.0)   /* Material Design standard */
cubic-bezier(0.68, -0.55, 0.265, 1.55)  /* Bounce effect */
steps(4)                            /* Frame-by-frame */
```

### Propriétés animables ou non {#animatable-vs-not}
**Animables** : `opacity`, `transform`, `color`, `background-color`, `width`, `height`, `padding`, `margin`, `box-shadow`, `border-radius`, `filter`

**Non animables** : `display`, `font-family`, `background-image` (URL), `position`

## Transform {#transform}

Modifie le rendu visuel sans affecter le flux de mise en page.

```css
/* Translate (move) */
transform: translate(50px, -20px);
transform: translate(-50%, -50%);    /* % relative to ELEMENT size */

/* Scale */
transform: scale(1.5);
transform: scale(1.5, 0.8);         /* x, y independently */

/* Rotate */
transform: rotate(45deg);
transform: rotateY(180deg);         /* 3D card flip */

/* Skew */
transform: skew(10deg, 5deg);

/* Multiple (applied right-to-left) */
transform: translateX(100px) rotate(45deg) scale(1.2);

/* Origin (pivot point) */
transform-origin: top left;
transform-origin: 50% 100%;         /* Bottom center */
```

### Centrage avec transform {#centering-with-transform}
```css
.centered {
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
}
```

### Transformations 3D et effet de retournement de carte {#3d-transforms-and-card-flip}
```css
.card-container { perspective: 1000px; }
.card {
  transform-style: preserve-3d;
  transition: transform 0.6s;
}
.card-container:hover .card { transform: rotateY(180deg); }
.card-front, .card-back {
  position: absolute; width: 100%; height: 100%;
  backface-visibility: hidden;
}
.card-back { transform: rotateY(180deg); }
```

## Animations par images clés {#keyframe-animations}

Séquences en plusieurs étapes pouvant boucler sans déclencheur.

```css
@keyframes slideIn {
  0%   { transform: translateX(-100%); opacity: 0; }
  60%  { transform: translateX(10px); }
  100% { transform: translateX(0); opacity: 1; }
}

.element {
  animation: slideIn 0.8s ease forwards;
}
```

### Propriétés d'animation {#animation-properties}
```css
animation-name: bounce;
animation-duration: 1s;
animation-timing-function: ease;
animation-delay: 0.5s;
animation-iteration-count: infinite;
animation-direction: alternate;      /* Ping-pong */
animation-fill-mode: forwards;       /* Stay at final keyframe */
animation-play-state: paused;        /* Toggle with JS */

/* Shorthand */
animation: bounce 1s ease 0.5s infinite alternate forwards;
```

### fill-mode {#fill-mode}
| Valeur | Avant (pendant le délai) | Après |
|--------|--------------------------|-------|
| `none` | Original | Original |
| `forwards` | Original | Dernière image clé |
| `backwards` | Première image clé | Original |
| `both` | Première image clé | Dernière image clé |

## Filtre CSS {#css-filter}

```css
filter: blur(5px);
filter: brightness(1.2);
filter: grayscale(100%);
filter: saturate(2);
filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.3));
filter: brightness(1.1) contrast(1.2) saturate(1.1);

backdrop-filter: blur(10px);    /* Glassmorphism */
```

**`drop-shadow` vs `box-shadow`** : `box-shadow` suit le rectangle englobant ; `drop-shadow` suit la forme de l'élément (préférable pour les PNG transparents).

## Performance {#performance}

1. **N'animez que `transform` et `opacity`** : composés par le GPU, sans layout ni paint
2. **Évitez d'animer `width`/`height`/`margin`** : déclenche un recalcul de la mise en page
3. **`will-change: transform`** : promeut l'élément dans une couche GPU (à utiliser avec parcimonie, consomme de la mémoire)
4. **`prefers-reduced-motion`** : respecter l'accessibilité :

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Motifs courants {#common-patterns}

### Bouton au survol en douceur {#smooth-hover-button}
```css
.btn {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.btn:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
.btn:active { transform: translateY(0); }
```

### Pulsation de chargement squelette {#skeleton-loading-pulse}
```css
.skeleton {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}
@keyframes shimmer {
  0%   { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

### Apparition en fondu au chargement {#fade-in-on-load}
```css
.fade-in { animation: fadeIn 0.5s ease forwards; }
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

## Pièges à éviter {#gotchas}

- **`transition: all`** : moins performant que la liste explicite des propriétés
- **Animer `display`** : impossible ; utilisez plutôt `opacity` + `visibility`
- **`transform` sur des éléments inline** : sans effet ; définissez `display: inline-block`
- **Abus de `will-change`** : chaque élément avec `will-change` consomme de la mémoire GPU
- **Valeurs y de cubic-bezier > 1** : crée un dépassement/rebond, pouvant faire sortir temporairement les éléments de la zone visible

## Voir aussi {#see-also}

- [[css-selectors-and-cascade]] - Pseudo-classes pour les déclencheurs basés sur l'état
- [[css-box-model-and-layout]] - Transform n'affecte pas le flux de mise en page
- [[figma-design-workflow]] - Prototypage d'animations dans Figma
- [[react-styling-approaches]] - Utilitaires d'animation de Tailwind
