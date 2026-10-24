---
title: "Sélecteurs CSS et cascade"
category: concepts
tags: [web-frontend, css, selectors, specificity, variables]
level: 3
source_sha256: 01301e8235445276ef3cae8999d14ae4b2dd9e5e58a2b3dd9b79a3f83d59b0ed
translation: machine
translated_at: '2026-10-24'
---
# Sélecteurs CSS et cascade {#css-selectors-and-cascade}

CSS contrôle la présentation du HTML. La cascade, la spécificité et l'héritage déterminent quelles règles s'appliquent lorsque plusieurs règles ciblent le même élément.

## Intégrer le CSS {#connecting-css}

```html
<link rel="stylesheet" href="css/style.css">   <!-- External (preferred, cacheable) -->
<style>p { color: red; }</style>                 <!-- Internal (in <head>) -->
<p style="color: red;">Text</p>                  <!-- Inline (highest specificity) -->
```

## Sélecteurs {#selectors}

### De base {#basic}
```css
*         { }    /* Universal */
p         { }    /* Type */
.card     { }    /* Class */
#header   { }    /* ID (avoid for styling) */
```

### Attribut {#attribute}
```css
[href]              { }    /* Has attribute */
[type="text"]       { }    /* Exact value */
[href^="https"]     { }    /* Starts with */
[href$=".pdf"]      { }    /* Ends with */
[href*="example"]   { }    /* Contains */
[data-theme="dark" i] { }  /* Case-insensitive */
```

### Combinateurs {#combinators}
```css
div p       { }    /* Descendant (any depth) */
div > p     { }    /* Direct child */
h2 + p      { }    /* Adjacent sibling (immediately after) */
h2 ~ p      { }    /* General sibling (all after, same parent) */
```

### Pseudo-classes (état) {#pseudo-classes-state}
```css
a:hover       { }    a:active      { }    a:visited     { }
a:focus       { }    a:focus-visible { }   /* Keyboard focus only */
input:valid   { }    input:invalid { }    input:required  { }
input:disabled { }   input:checked { }    input:placeholder-shown { }
:empty        { }    :target       { }    :root          { }
```

### Pseudo-classes structurelles {#structural-pseudo-classes}
```css
:first-child    { }    :last-child     { }
:nth-child(2)   { }    :nth-child(odd) { }    :nth-child(3n+1) { }
:nth-last-child(2) { } :only-child     { }
:first-of-type  { }    :nth-of-type(2) { }    :only-of-type   { }
```

**Différence essentielle** : `:nth-child` compte TOUS les enfants. `:nth-of-type` ne compte que les éléments de même balise.

### Négation et logique {#negation-and-logical}
```css
:not(.hidden)     { }    /* Exclude matching */
:is(h1, h2, h3)  { }    /* Match any (forgiving selector list) */
:where(h1, h2)   { }    /* Like :is() but zero specificity */
:has(.icon)       { }    /* Parent selector - element containing .icon */
```

`:has()` est le « sélecteur parent » tant attendu. Par exemple, `.card:has(img)` sélectionne les cartes contenant une image.

### Pseudo-éléments {#pseudo-elements}
```css
p::first-line    { }    p::first-letter  { }
p::selection     { }    p::placeholder   { }
.item::before { content: ">> "; }
.item::after  { content: ""; display: block; }
```

`::before`/`::after` DOIVENT avoir une propriété `content`. Ils sont en ligne par défaut et ne peuvent pas être appliqués aux éléments vides (`<img>`, `<input>`).

## Cascade (résolution des conflits) {#cascade-conflict-resolution}

1. **Origine et importance** : `!important` > styles de l'auteur > styles par défaut du navigateur
2. **Spécificité** : le sélecteur le plus spécifique l'emporte
3. **Ordre des sources** : la dernière règle l'emporte (à spécificité égale)

## Spécificité {#specificity}

| Type de sélecteur | Poids |
|--------------|--------|
| Style en ligne | 1,0,0,0 |
| ID `#id` | 0,1,0,0 |
| Classe `.class`, `[attr]`, `:pseudo-class` | 0,0,1,0 |
| Élément `div`, `::pseudo-element` | 0,0,0,1 |
| Universel `*`, combinateurs | 0,0,0,0 |

```css
p                    /* 0,0,0,1 */
.card                /* 0,0,1,0 */
#header .nav li a    /* 0,1,1,2 */
div > p.text:hover   /* 0,0,2,2 */
```

La spécificité la plus élevée l'emporte TOUJOURS, quel que soit l'ordre des sources. Évitez `!important`, qui casse la cascade.

## Héritage {#inheritance}

**Hérité** : `color`, `font-*`, `line-height`, `text-align`, `visibility`, `cursor`, `list-style`
**Non hérité** : `margin`, `padding`, `border`, `background`, `width`, `height`, `display`, `position`

```css
.child { color: inherit; }   /* Force inheritance */
.element { all: unset; }     /* Reset to browser default */
```

## Couleurs {#colors}

```css
color: #ff0000;                  /* Hex */
color: #f00;                     /* Hex shorthand */
color: rgb(255, 0, 0);          /* RGB */
color: rgba(255, 0, 0, 0.5);    /* RGBA */
color: hsl(0, 100%, 50%);       /* HSL (most intuitive) */
color: hsla(0, 100%, 50%, 0.5);
```

**Avantage de HSL** : H = roue chromatique (0-360), S = saturation (0-100 %), L = luminosité (0-100 %). Assombrir = diminuer L. Éclaircir = augmenter L. Désaturer = diminuer S. Tout est prévisible.

Le mot-clé `currentColor` hérite de la couleur du texte, ce qui est utile pour les bordures et les remplissages SVG.

## Propriétés de texte et de police {#text-and-font-properties}

```css
font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif;
font-size: 1rem;              /* Relative to root (preferred) */
font-weight: 400;             /* Normal=400, Bold=700 */
line-height: 1.5;             /* Unitless multiplier (preferred) */
text-align: left | center | right | justify;
text-decoration: underline wavy red;
text-transform: uppercase | lowercase | capitalize;
letter-spacing: 0.05em;
white-space: nowrap; overflow: hidden; text-overflow: ellipsis;  /* Truncation */
font: italic 700 16px/1.5 'Inter', sans-serif;  /* Shorthand */
```

### Polices personnalisées {#custom-fonts}
```css
@font-face {
  font-family: 'MyFont';
  src: url('fonts/myfont.woff2') format('woff2');
  font-weight: 400;
  font-display: swap;  /* Show fallback immediately, swap when loaded */
}
```

WOFF2 offre la meilleure compression pour les navigateurs modernes. `font-display: swap` évite un texte invisible pendant le chargement.

## Propriétés personnalisées CSS {#css-custom-properties}

```css
:root {
  --color-primary: #3b82f6;
  --spacing-md: 16px;
  --border-radius: 8px;
}
.button {
  background: var(--color-primary);
  padding: var(--spacing-md);
  border-radius: var(--border-radius);
  font-size: var(--font-size-base, 14px);  /* Fallback value */
}
```

- Portée : `:root` = global, élément = portée locale
- En cascade et héritées comme les propriétés classiques
- Dynamiques via JS : `element.style.setProperty('--color', 'red')`
- Contrairement aux variables SASS, les variables CSS sont vivantes et suivent la cascade

## Pièges courants {#gotchas}

- **Abus de `!important`** : crée des cauchemars de maintenance, difficile à surcharger
- **Sélecteurs d'ID pour le style** : trop spécifiques, privilégier les classes
- **`:nth-child` vs `:nth-of-type`** : le comptage inclut TOUS les frères et sœurs, contre uniquement ceux du même type
- **`em` en cascade** : `em` pour `font-size` = relatif au parent ; pour les autres propriétés = relatif à la taille de police propre à l'élément
- **Hauteur en pourcentage** : ne fonctionne que si le parent a une hauteur explicite

## Voir aussi {#see-also}

- [[css-box-model-and-layout]] - Affichage, position, unités
- [[css-sass-and-methodology]] - Nommage BEM, prétraitement SASS
- [[html-fundamentals]] - Éléments HTML ciblés par le CSS
