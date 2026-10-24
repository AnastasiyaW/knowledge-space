---
title: "CSS-Methodik und SASS"
category: concepts
tags: [web-frontend, css, bem, sass, scss, architecture]
level: 3
source_sha256: f59f39b42c67960e9cf9c72ce7de65054782b8b25e2affed47afc2d384a4b762
translation: machine
translated_at: '2026-10-24'
---
# CSS-Methodik und SASS {#css-methodology-and-sass}

Ohne Methodik wird CSS unwartbar: fragile Spezifitätsketten, inkonsistente Benennung und unvorhersehbare Kaskadierung. BEM + SASS lösen dieses Problem auch im großen Maßstab.

## BEM (Block Element Modifier) {#bem-block-element-modifier}

### Struktur {#structure}
```text
.block            - standalone component
.block__element   - part of block (child)
.block--modifier  - variant of block or element
```

### Beispiele {#examples}
```css
.card { }
.card__title { }
.card__image { }
.card--featured { }
.card--dark { }
.button { }
.button--large { }
.button--disabled { }
```

```html
<div class="card card--featured">
  <img class="card__image" src="...">
  <h3 class="card__title">Title</h3>
  <button class="button button--large">Read more</button>
</div>
```

### BEM-Regeln {#bem-rules}
1. **Flache Selektoren**: `.card__title` statt `.card .title` – konsistente Spezifität
2. **Kein Element eines Elements**: `.card__footer__button` ist falsch – stattdessen einen neuen Block oder `.card__action` verwenden
3. **Modifikatoren benötigen eine Basisklasse**: `class="button button--large"` statt `class="button--large"` allein
4. **Blöcke sind ortsunabhängig**: Stile hängen nicht davon ab, wo der Block platziert wird

### Vorteile {#benefits}
- Alle Klassen haben die Spezifität `0,0,1,0` (flach, vorhersehbar)
- Selbstdokumentierend: Der Klassenname beschreibt Komponente und Rolle
- Blöcke lassen sich sicher zwischen Seiten verschieben oder kopieren

## SMACSS-Kategorien {#smacss-categories}

| Kategorie | Präfix | Beispiel |
|-----------|--------|----------|
| Base | keine | `html, body { margin: 0; }` |
| Layout | `l-` | `.l-header`, `.l-sidebar` |
| Module | keine | `.card`, `.nav` |
| State | `is-` | `.is-hidden`, `.is-active` |
| Theme | `theme-` | `.theme-dark` |

## Dateiorganisation {#file-organization}

```text
css/
  global.css         - Reset, variables, base element styles
  layout.css         - Page-level layout
  components/
    card.css
    button.css
    form.css
  utils.css          - .hidden, .sr-only, .text-center
```

### Modernes Reset {#modern-reset}
```css
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { font-size: 16px; -webkit-font-smoothing: antialiased; }
img, picture, video, canvas, svg { display: block; max-width: 100%; }
input, button, textarea, select { font: inherit; }
```

## SASS/SCSS {#sassscss}

CSS-Präprozessor, der zu regulärem CSS kompiliert. Die SCSS-Syntax (`.scss`) ist CSS-kompatibel.

### Variablen {#variables}
```scss
$color-primary: #3b82f6;
$font-body: 'Inter', sans-serif;
$breakpoint-tablet: 768px;

.button {
  background: $color-primary;
  font-family: $font-body;
}
```

SASS-Variablen werden zur Compile-Zeit ausgewertet. Für Laufzeitwerte werden CSS Custom Properties verwendet.

### Verschachtelung (BEM-Muster) {#nesting-bem-pattern}
```scss
.nav {
  display: flex;

  &__item {                /* .nav__item */
    padding: 8px 16px;

    &--active {            /* .nav__item--active */
      color: $color-primary;
    }
    &:hover {              /* .nav__item:hover */
      background: #f5f5f5;
    }
  }
}
```

**Regel**: Nicht tiefer als 3 Ebenen verschachteln.

### Mixins {#mixins}
```scss
@mixin flex-center {
  display: flex; justify-content: center; align-items: center;
}

@mixin responsive($breakpoint) {
  @media (min-width: $breakpoint) { @content; }
}

@mixin button-variant($bg, $color: white) {
  background: $bg; color: $color;
  &:hover { background: darken($bg, 10%); }
}

.hero { @include flex-center; min-height: 100vh; }
.sidebar {
  display: none;
  @include responsive(768px) { display: block; width: 250px; }
}
.btn-primary { @include button-variant(#3b82f6); }
.btn-danger  { @include button-variant(#ef4444); }
```

### Extend / Placeholder {#extend-placeholder}
```scss
%card-base {
  border-radius: 8px; padding: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.card  { @extend %card-base; }
.modal { @extend %card-base; }
```

`@mixin` ist in den meisten Fällen vorzuziehen – `@extend` kann unerwartetes CSS erzeugen.

### Funktionen {#functions}
```scss
@function rem($px) {
  @return ($px / 16) * 1rem;
}
.title { font-size: rem(24); }    /* 1.5rem */
```

Eingebaut: `darken()`, `lighten()`, `saturate()`, `mix()`, `rgba()`.

### Partials und @use {#partials-and-use}
```scss
// _variables.scss
$color-primary: #3b82f6;

// main.scss
@use 'variables' as vars;
.button { background: vars.$color-primary; }
```

`@use` (mit Namensraum, wird einmal kompiliert) ersetzt das veraltete `@import` (global, wird bei jedem Einbinden erneut kompiliert).

### Schleifen und Bedingungen {#loops-and-conditionals}
```scss
@for $i from 1 through 12 {
  .col-#{$i} { width: (100% / 12) * $i; }
}

@each $color, $value in (primary: #3b82f6, danger: #ef4444) {
  .text-#{$color} { color: $value; }
  .bg-#{$color} { background: $value; }
}
```

## Erweiterte CSS-Eigenschaften {#advanced-css-properties}

```css
/* Clip to shape */
clip-path: circle(50%);
clip-path: polygon(50% 0%, 100% 100%, 0% 100%);  /* Triangle */

/* Blend modes */
mix-blend-mode: multiply;   /* Dark overlay */
mix-blend-mode: screen;     /* Light overlay */

/* Backdrop filter (glassmorphism) */
backdrop-filter: blur(10px) saturate(1.5);
```

## Fallstricke {#gotchas}

- **Tiefe Verschachtelung**: erzeugt Selektoren mit hoher Spezifität, die schwer zu überschreiben sind
- **`@extend`-Fallstricke**: können riesige kombinierte Selektoren mit komplexem CSS erzeugen
- **SASS- vs. CSS-Variablen**: SASS-Variablen verschwinden nach der Kompilierung; CSS Custom Properties sind im Browser zur Laufzeit verfügbar
- **Element eines Elements**: `.card__body__title` ist ein BEM-Antipattern – flach strukturieren oder einen neuen Block anlegen
- **`@import` veraltet**: stattdessen `@use` mit Namensräumen verwenden

## Siehe auch {#see-also}

- [[css-selectors-and-cascade]] - Spezifität und Kaskadenregeln
- [[react-styling-approaches]] - CSS Modules und Tailwind als Alternativen
- [[frontend-build-systems]] - SASS-Kompilierung in der Build-Pipeline
