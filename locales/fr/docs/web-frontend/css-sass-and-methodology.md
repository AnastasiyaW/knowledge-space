---
title: "Méthodologie CSS et SASS"
category: concepts
tags: [web-frontend, css, bem, sass, scss, architecture]
level: 3
source_sha256: f59f39b42c67960e9cf9c72ce7de65054782b8b25e2affed47afc2d384a4b762
translation: machine
translated_at: '2026-10-24'
---
# Méthodologie CSS et SASS {#css-methodology-and-sass}

Sans méthodologie, le CSS devient difficile à maintenir : chaînes de spécificité fragiles, nommage incohérent, cascade imprévisible. BEM et SASS répondent à ce problème à grande échelle.

## BEM (Block Element Modifier) {#bem-block-element-modifier}

### Structure {#structure}
```text
.block            - standalone component
.block__element   - part of block (child)
.block--modifier  - variant of block or element
```

### Exemples {#examples}
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

### Règles BEM {#bem-rules}
1. **Sélecteurs à plat** : `.card__title` et non `.card .title` - spécificité constante
2. **Pas d'élément d'élément** : `.card__footer__button` est incorrect - créer un nouveau bloc ou utiliser `.card__action`
3. **Les modificateurs nécessitent une base** : `class="button button--large"` et non `class="button--large"` seul
4. **Les blocs sont indépendants de leur emplacement** : les styles ne dépendent pas de l'endroit où le bloc est placé

### Avantages {#benefits}
- Toutes les classes ont une spécificité de `0,0,1,0` (à plat, prévisible)
- Auto-documenté : le nom de la classe indique le composant et son rôle
- Déplacement ou copie de blocs entre pages sans risque

## Catégories SMACSS {#smacss-categories}

| Catégorie | Préfixe | Exemple |
|-----------|---------|---------|
| Base | aucun | `html, body { margin: 0; }` |
| Layout | `l-` | `.l-header`, `.l-sidebar` |
| Module | aucun | `.card`, `.nav` |
| État | `is-` | `.is-hidden`, `.is-active` |
| Thème | `theme-` | `.theme-dark` |

## Organisation des fichiers {#file-organization}

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

### Reset moderne {#modern-reset}
```css
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { font-size: 16px; -webkit-font-smoothing: antialiased; }
img, picture, video, canvas, svg { display: block; max-width: 100%; }
input, button, textarea, select { font: inherit; }
```

## SASS/SCSS {#sassscss}

Préprocesseur CSS qui se compile en CSS classique. La syntaxe SCSS (`.scss`) est compatible avec CSS.

### Variables {#variables}
```scss
$color-primary: #3b82f6;
$font-body: 'Inter', sans-serif;
$breakpoint-tablet: 768px;

.button {
  background: $color-primary;
  font-family: $font-body;
}
```

Les variables SASS sont résolues à la compilation. Pour une valeur évaluée à l'exécution, utiliser les propriétés personnalisées CSS.

### Imbrication (motif BEM) {#nesting-bem-pattern}
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

**Règle** : ne pas imbriquer au-delà de 3 niveaux.

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

Préférer `@mixin` dans la plupart des cas, car `@extend` peut produire du CSS inattendu.

### Fonctions {#functions}
```scss
@function rem($px) {
  @return ($px / 16) * 1rem;
}
.title { font-size: rem(24); }    /* 1.5rem */
```

Fonctions intégrées : `darken()`, `lighten()`, `saturate()`, `mix()`, `rgba()`.

### Partials et @use {#partials-and-use}
```scss
// _variables.scss
$color-primary: #3b82f6;

// main.scss
@use 'variables' as vars;
.button { background: vars.$color-primary; }
```

`@use` (avec espaces de noms, compilé une seule fois) remplace `@import` déprécié (global, compilé à chaque import).

### Boucles et conditions {#loops-and-conditionals}
```scss
@for $i from 1 through 12 {
  .col-#{$i} { width: (100% / 12) * $i; }
}

@each $color, $value in (primary: #3b82f6, danger: #ef4444) {
  .text-#{$color} { color: $value; }
  .bg-#{$color} { background: $value; }
}
```

## Propriétés CSS avancées {#advanced-css-properties}

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

## Pièges courants {#gotchas}

- **Imbrication profonde** : produit des sélecteurs à forte spécificité, difficiles à surcharger
- **Pièges de `@extend`** : peut créer de très longs sélecteurs combinés au CSS complexe
- **Variables SASS et variables CSS** : les variables SASS disparaissent après compilation ; les propriétés personnalisées CSS restent actives dans le navigateur
- **Élément d'élément** : `.card__body__title` est un antipattern BEM - aplatir la structure ou créer un nouveau bloc
- **`@import` déprécié** : utiliser `@use` avec des espaces de noms à la place

## Voir aussi {#see-also}

- [[css-selectors-and-cascade]] - Spécificité et règles de cascade
- [[react-styling-approaches]] - CSS Modules et Tailwind comme alternatives
- [[frontend-build-systems]] - Compilation SASS dans la chaîne de build
