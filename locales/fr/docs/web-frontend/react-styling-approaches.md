---
title: "Approches de style avec React"
category: concepts
tags: [web-frontend, react, css-modules, tailwind, styling]
level: 3
source_sha256: 8868211078d402a16bc904f27e8b7c0b0b1a4ce1db2306314f1643d977f2d591
translation: machine
translated_at: '2026-10-24'
---
# Approches de style avec React {#react-styling-approaches}

Deux modèles dominants pour styler React : CSS Modules (CSS traditionnel à portée locale) et Tailwind CSS (orienté utilitaires). Les deux fonctionnent directement avec Vite.

## CSS Modules {#css-modules}

Noms de classes à portée locale : des suffixes uniques générés automatiquement évitent les conflits.

### Convention de fichiers {#file-convention}
```text
components/Header/
  Header.jsx
  Header.module.css       # Must include .module.css
```

### Utilisation {#usage}
```css
/* Header.module.css */
.header { background: #1a1a1a; padding: 16px; }
.title { color: white; font-size: 24px; }
```

```jsx
import styles from './Header.module.css';

function Header() {
  return (
    <header className={styles.header}>
      <h1 className={styles.title}>My App</h1>
    </header>
  );
}
```

L'import renvoie un objet : `{ header: "Header_header_x7d3f", title: "Header_title_k9m2p" }`.

### Plusieurs classes {#multiple-classes}
```jsx
<div className={`${styles.card} ${styles.active}`}>
// With classnames library
import cn from 'classnames';
<div className={cn(styles.card, { [styles.active]: isActive })}>
```

## Tailwind CSS {#tailwind-css}

Orienté utilitaires : composer les designs à partir de classes à usage unique.

### Configuration {#setup}
```bash
npm install -D tailwindcss @tailwindcss/vite
```
```js
// vite.config.js
import tailwindcss from '@tailwindcss/vite';
export default { plugins: [tailwindcss()] };
```
```css
/* index.css */
@import "tailwindcss";
```

### Utilitaires de base {#core-utilities}

**Espacement** (1 unité = 4px) :
```html
<div class="p-4 px-6 py-2 m-auto mt-8 space-y-4">
```

**Typographie** :
```html
<p class="text-lg font-bold text-gray-700 text-center leading-relaxed uppercase truncate">
```

**Couleurs** : `{property}-{color}-{shade}` - nuances de 50 (clair) à 950 (sombre) :
```html
<div class="bg-blue-500 text-white border-gray-300">
```

**Mise en page** :
```html
<div class="flex items-center justify-between gap-4">
<div class="grid grid-cols-3 gap-6">
<div class="w-full max-w-md mx-auto hidden md:block">
```

**Bordures/Ombres** :
```html
<div class="border border-gray-300 rounded-lg shadow-md hover:shadow-lg ring-2 ring-blue-500">
```

### Responsive (mobile-first) {#responsive-mobile-first}
```html
<div class="text-sm md:text-base lg:text-lg">
<div class="flex-col md:flex-row">
<div class="grid-cols-1 sm:grid-cols-2 lg:grid-cols-4">
```

| Préfixe | Largeur minimale |
|---------|------------------|
| (aucun) | 0 (mobile) |
| `sm:` | 640px |
| `md:` | 768px |
| `lg:` | 1024px |
| `xl:` | 1280px |

### États {#states}
```html
<button class="bg-blue-500 hover:bg-blue-600 active:bg-blue-700 focus:ring-2">
<tr class="odd:bg-white even:bg-gray-50">
```

### group et peer {#group-and-peer}
```html
<!-- Style child on parent hover -->
<div class="group">
  <img class="group-hover:scale-105 transition" />
</div>

<!-- Style sibling on sibling state -->
<input class="peer" type="checkbox" />
<label class="peer-checked:text-blue-500">Option</label>
```

### Animations {#animations}
```html
<div class="transition duration-300 ease-in-out hover:scale-105">
<div class="animate-spin">   <!-- Built-in -->
<div class="animate-pulse">  <!-- Skeleton loading -->
```

### Valeurs arbitraires {#arbitrary-values}
```html
<div class="w-[300px] bg-[#1a1a2e] grid-cols-[200px_1fr_200px]">
```

### @apply (extraire des motifs) {#apply-extract-patterns}
```css
.btn-primary {
  @apply px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition;
}
```

À utiliser avec modération : en abuser va à l'encontre de l'approche orientée utilitaires.

### Mode sombre {#dark-mode}
```html
<div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100">
```

## Comparaison {#comparison}

| Aspect | CSS Modules | Tailwind |
|--------|-------------|----------|
| Approche | CSS traditionnel, fichiers séparés | Classes utilitaires dans le JSX |
| Bundle | Tout le CSS écrit | Purgé, seulement ce qui est utilisé |
| Apprentissage | Connaître déjà le CSS | Apprendre les noms des utilitaires |
| Co-location | `.module.css` séparé | Dans le fichier du composant |
| Cohérence du design | Discipline manuelle | Imposée par l'échelle des utilitaires |
| Lisibilité | JSX épuré | Chaînes de classes denses |

Les deux sont valables. Beaucoup d'équipes utilisent Tailwind pour un développement rapide et CSS Modules pour les composants personnalisés complexes.

## Pièges courants {#gotchas}

- **Styles globaux avec CSS Modules** : utiliser `:global(.class)` ou un fichier CSS séparé non modulaire
- **Purge de Tailwind** : les classes doivent être des chaînes complètes, non construites : `bg-${color}-500` ne fonctionnera pas
- **Spécificité de Tailwind** : les utilitaires ont la même spécificité ; la classe placée en dernier l'emporte (l'ordre compte)
- **Multi-classes verbeux avec CSS Modules** : les template literals deviennent difficiles à lire ; utiliser la bibliothèque `classnames`
- **Tailwind dynamique** : utiliser un ternaire pour les classes conditionnelles : `isActive ? "bg-blue-500" : "bg-gray-500"`

## Voir aussi {#see-also}

- [[css-sass-and-methodology]] - BEM, SASS comme approches alternatives
- [[css-flexbox]] - Flexbox auquel correspondent les utilitaires Tailwind
- [[css-grid]] - Utilitaires Grid dans Tailwind
- [[react-components-and-jsx]] - Structure des composants
