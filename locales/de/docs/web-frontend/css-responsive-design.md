---
title: "CSS-Responsive-Design"
category: concepts
tags: [web-frontend, css, responsive, media-queries, mobile-first]
level: 3
source_sha256: 78c2c3bbcc6ac26b07503b53685a126255d9eb88e2ba6d6d1d73b22d5a56793b
translation: machine
translated_at: '2026-10-24'
---
# CSS-Responsive-Design {#css-responsive-design}

Eine Codebasis passt sich an alle Bildschirmgrößen an. Etwa 60 % des Webverkehrs stammen von mobilen Geräten; Google bewertet Seiten mobile-first.

## Viewport-Meta-Tag {#viewport-meta-tag}

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

**Muss auf jeder responsiven Seite vorhanden sein.** Ohne es rendern mobile Browser mit einer Breite von etwa 980px und zoomen heraus.

## Media Queries {#media-queries}

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

### Syntax {#syntax}
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

### Gängige Breakpoints {#common-breakpoints}
| Breakpoint | Zielgerät |
|-----------|--------|
| 375px | iPhone SE/12 mini |
| 768px | Tablets |
| 1024px | Kleine Laptops |
| 1200px | Desktop |
| 1440px | Großer Desktop |

### Mobile-First vs. Desktop-First {#mobile-first-vs-desktop-first}
**Mobile-First** (`min-width`): progressive Verbesserung, kleineres CSS für mobile Geräte, erzwingt die Priorisierung von Inhalten. Empfohlen.

**Desktop-First** (`max-width`): Überschreiben nach unten. Ältere Herangehensweise.

## Viewport-Einheiten {#viewport-units}

```css
width: 100vw;        /* 100% viewport width */
height: 100dvh;      /* Dynamic viewport height (mobile-friendly) */
height: 100svh;      /* Small viewport (bar visible) */
height: 100lvh;      /* Large viewport (bar hidden) */
```

**Problem mit `100vh` auf mobilen Geräten**: Die Adressleiste des mobilen Browsers erscheint und verschwindet, was zu Überlauf führt. Für vollbildige mobile Bereiche `100dvh` verwenden.

## Fließende Typografie mit clamp() {#fluid-typography-with-clamp}

```css
h1 { font-size: clamp(1.5rem, 4vw, 3rem); }
p  { font-size: clamp(1rem, 1rem + 0.5vw, 1.25rem); }
```

- **min**: Untergrenze für Barrierefreiheit (nie darunter)
- **preferred**: skaliert mit dem Viewport
- **max**: Obergrenze für Lesbarkeit (nie darüber)
- Entfällt in den meisten Fällen die Media Queries für Schriftgrößen

## calc(), min(), max() {#calc-min-max}

```css
width: calc(100% - 40px);        /* Mixed unit arithmetic */
width: min(100%, 800px);          /* Full width, max 800px */
width: max(300px, 50%);           /* At least 300px */
padding: clamp(16px, 4vw, 64px);
```

**calc() benötigt Leerzeichen** um Operatoren: `calc(100% - 20px)` statt `calc(100%-20px)`.

## Responsive Bilder {#responsive-images}

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

| Wert | Verhalten |
|-------|----------|
| `fill` | Wird gestreckt (verzerrt) |
| `contain` | Passt sich an, behält das Seitenverhältnis bei (kann Ränder erzeugen) |
| `cover` | Füllt aus und schneidet zu, behält das Seitenverhältnis bei |
| `none` | Originalgröße |

## Layout-Muster {#layout-patterns}

### Container mit Max-Width {#container-with-max-width}
```css
.container {
  width: 100%; max-width: 1200px;
  margin: 0 auto; padding: 0 16px;
}
```

### Responsives Grid (ohne Media Queries) {#responsive-grid-no-media-queries}
```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
}
```

### Hamburger-Menü {#hamburger-menu}
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

## Stolperfallen {#gotchas}

- **Fehlendes Viewport-Meta**: alles wird auf mobilen Geräten winzig dargestellt
- **`100vh` auf mobilen Geräten**: Die Adressleiste verursacht Überlauf, `100dvh` verwenden
- **`:hover` bei Touch**: Hover-Effekte funktionieren nicht; `@media (hover: hover)` für reine Hover-Stile verwenden
- **Nur bei Standard-Breakpoints testen**: langsam die Größe ändern, um zu finden, wo das Layout tatsächlich bricht
- **`vw` verursacht horizontales Scrollen**: `100vw` enthält die Scrollbar-Breite; für die Containerbreite `100%` verwenden

## Siehe auch {#see-also}

- [[css-grid]] - Automatisch responsive Grid-Muster
- [[css-flexbox]] - Responsives Umbrechen mit Flex
- [[css-box-model-and-layout]] - Viewport-Einheiten, Größenangaben
- [[figma-design-workflow]] - Gestaltung für mehrere Breakpoints
