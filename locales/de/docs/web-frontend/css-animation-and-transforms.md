---
title: "CSS-Animationen und Transformationen"
category: concepts
tags: [web-frontend, css, animation, transitions, transforms, performance]
level: 3
source_sha256: 8b2350c73cdbcb5ebc4e783c29189a3c459f4f7b45cc0879610125bfed6fa1ef
translation: machine
translated_at: '2026-10-24'
---
# CSS-Animationen und Transformationen {#css-animation-and-transforms}

CSS-Animationen werden von der GPU beschleunigt, sind deklarativ und blockieren nicht den Haupt-Thread. JS-Animationen sollten nur für dynamische Erzeugung, komplexe Orchestrierung oder physikbasierte Bewegungen verwendet werden.

## Transitions {#transitions}

Änderungen von Eigenschaften sanft animieren. Erfordert einen Auslöser für den Zustandswechsel (Hover, Klassenwechsel).

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

### Transition-Eigenschaften {#transition-properties}
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

### Timing-Funktionen {#timing-functions}
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

### Animierbar und nicht animierbar {#animatable-vs-not}
**Animierbar**: `opacity`, `transform`, `color`, `background-color`, `width`, `height`, `padding`, `margin`, `box-shadow`, `border-radius`, `filter`

**Nicht animierbar**: `display`, `font-family`, `background-image` (URL), `position`

## Transform {#transform}

Verändert die visuelle Darstellung, ohne den Layout-Fluss zu beeinflussen.

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

### Zentrieren mit Transform {#centering-with-transform}
```css
.centered {
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
}
```

### 3D-Transformationen und Karten-Flip {#3d-transforms-and-card-flip}
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

## Keyframe-Animationen {#keyframe-animations}

Mehrstufige Sequenzen, die ohne Auslöser wiederholt werden können.

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

### Animation-Eigenschaften {#animation-properties}
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
| Wert | Vorher (während Verzögerung) | Nachher |
|-------|----------------------|-------|
| `none` | Original | Original |
| `forwards` | Original | Letztes Keyframe |
| `backwards` | Erstes Keyframe | Original |
| `both` | Erstes Keyframe | Letztes Keyframe |

## CSS-Filter {#css-filter}

```css
filter: blur(5px);
filter: brightness(1.2);
filter: grayscale(100%);
filter: saturate(2);
filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.3));
filter: brightness(1.1) contrast(1.2) saturate(1.1);

backdrop-filter: blur(10px);    /* Glassmorphism */
```

**`drop-shadow` vs. `box-shadow`**: `box-shadow` folgt dem umschließenden Rechteck; `drop-shadow` folgt der Form des Elements (besser für transparente PNGs).

## Performance {#performance}

1. **Nur `transform` und `opacity` animieren** - GPU-composited, kein Layout/Paint
2. **Animation von `width`/`height`/`margin` vermeiden** - löst eine Layout-Neuberechnung aus
3. **`will-change: transform`** - hebt das Element auf eine GPU-Ebene (sparsam einsetzen, verbraucht Speicher)
4. **`prefers-reduced-motion`** - Barrierefreiheit berücksichtigen:

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Häufige Muster {#common-patterns}

### Sanfter Hover-Button {#smooth-hover-button}
```css
.btn {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.btn:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
.btn:active { transform: translateY(0); }
```

### Skeleton-Loading-Puls {#skeleton-loading-pulse}
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

### Einblenden beim Laden {#fade-in-on-load}
```css
.fade-in { animation: fadeIn 0.5s ease forwards; }
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

## Fallstricke {#gotchas}

- **`transition: all`**: weniger performant als das Auflisten konkreter Eigenschaften
- **Animation von `display`**: nicht möglich; stattdessen `opacity` + `visibility` verwenden
- **`transform` auf Inline-Elementen**: hat keine Wirkung; `display: inline-block` setzen
- **Übermäßige Nutzung von `will-change`**: jedes Element mit `will-change` verbraucht GPU-Speicher
- **Cubic-Bezier-y-Werte > 1**: erzeugen Überschwingen/Abprallen und können dazu führen, dass Elemente vorübergehend den Viewport verlassen

## Siehe auch {#see-also}

- [[css-selectors-and-cascade]] - Pseudo-Klassen für zustandsbasierte Auslöser
- [[css-box-model-and-layout]] - Transform beeinflusst den Layout-Fluss nicht
- [[figma-design-workflow]] - Animationen in Figma prototypisieren
- [[react-styling-approaches]] - Tailwind-Animations-Utilities
