---
title: CSS Animation and Transforms
category: concepts
tags: [web-frontend, css, animation, transitions, transforms, performance]
---

# CSS Animation and Transforms

CSS animations are GPU-accelerated, declarative, and don't block the main thread. Use JS animation only for dynamic creation, complex orchestration, or physics-based motion.

## Transitions

Animate property changes smoothly. Requires a state change trigger (hover, class toggle).

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

### Transition Properties
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

### Timing Functions
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

### Animatable vs Not
**Animatable**: `opacity`, `transform`, `color`, `background-color`, `width`, `height`, `padding`, `margin`, `box-shadow`, `border-radius`, `filter`

**NOT animatable**: `display`, `font-family`, `background-image` (URL), `position`

## Transform

Changes visual rendering without affecting layout flow.

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

### Centering with Transform
```css
.centered {
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
}
```

### 3D Transforms and Card Flip
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

## Keyframe Animations

Multi-step sequences that can loop without triggers.

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

### Animation Properties
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

### fill-mode
| Value | Before (during delay) | After |
|-------|----------------------|-------|
| `none` | Original | Original |
| `forwards` | Original | Final keyframe |
| `backwards` | First keyframe | Original |
| `both` | First keyframe | Final keyframe |

## CSS Filter

```css
filter: blur(5px);
filter: brightness(1.2);
filter: grayscale(100%);
filter: saturate(2);
filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.3));
filter: brightness(1.1) contrast(1.2) saturate(1.1);

backdrop-filter: blur(10px);    /* Glassmorphism */
```

**`drop-shadow` vs `box-shadow`**: `box-shadow` follows bounding rectangle; `drop-shadow` follows element shape (better for transparent PNGs).

## Performance

1. **Animate only `transform` and `opacity`** - GPU-composited, no layout/paint
2. **Avoid animating `width`/`height`/`margin`** - triggers layout recalculation
3. **`will-change: transform`** - promotes to GPU layer (use sparingly, consumes memory)
4. **`prefers-reduced-motion`** - respect accessibility:

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Common Patterns

### Smooth Hover Button
```css
.btn {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.btn:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
.btn:active { transform: translateY(0); }
```

### Skeleton Loading Pulse
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

### Fade-In on Load
```css
.fade-in { animation: fadeIn 0.5s ease forwards; }
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

## Gotchas

- **`transition: all`**: less performant than listing specific properties
- **Animating `display`**: not possible; use `opacity` + `visibility` instead
- **`transform` on inline elements**: has no effect; set `display: inline-block`
- **`will-change` overuse**: each element with `will-change` consumes GPU memory
- **Cubic-bezier y-values > 1**: creates overshoot/bounce, may cause elements to leave viewport temporarily

## See Also

- [[css-selectors-and-cascade]] - Pseudo-classes for state-based triggers
- [[css-box-model-and-layout]] - Transform doesn't affect layout flow
- [[figma-design-workflow]] - Prototyping animations in Figma
- [[react-styling-approaches]] - Tailwind animation utilities
