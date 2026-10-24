---
title: "React-Styling-Ansätze"
category: concepts
tags: [web-frontend, react, css-modules, tailwind, styling]
level: 3
source_sha256: 8868211078d402a16bc904f27e8b7c0b0b1a4ce1db2306314f1643d977f2d591
translation: machine
translated_at: '2026-10-24'
---
# React-Styling-Ansätze {#react-styling-approaches}

Zwei dominante Muster für das Styling von React: CSS Modules (scoped traditionelles CSS) und Tailwind CSS (utility-first). Beide funktionieren mit Vite sofort ohne weitere Konfiguration.

## CSS Modules {#css-modules}

Lokal gescopte Klassennamen – automatisch generierte, eindeutige Suffixe verhindern Konflikte.

### Dateikonvention {#file-convention}
```text
components/Header/
  Header.jsx
  Header.module.css       # Must include .module.css
```

### Verwendung {#usage}
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

Der Import liefert ein Objekt: `{ header: "Header_header_x7d3f", title: "Header_title_k9m2p" }`.

### Mehrere Klassen {#multiple-classes}
```jsx
<div className={`${styles.card} ${styles.active}`}>
// With classnames library
import cn from 'classnames';
<div className={cn(styles.card, { [styles.active]: isActive })}>
```

## Tailwind CSS {#tailwind-css}

Utility-first: Designs werden aus Klassen mit jeweils einem Zweck zusammengesetzt.

### Einrichtung {#setup}
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

### Kern-Utilities {#core-utilities}

**Abstände** (1 Einheit = 4px):
```html
<div class="p-4 px-6 py-2 m-auto mt-8 space-y-4">
```

**Typografie**:
```html
<p class="text-lg font-bold text-gray-700 text-center leading-relaxed uppercase truncate">
```

**Farben**: `{property}-{color}-{shade}` – Abstufungen 50 (hell) bis 950 (dunkel):
```html
<div class="bg-blue-500 text-white border-gray-300">
```

**Layout**:
```html
<div class="flex items-center justify-between gap-4">
<div class="grid grid-cols-3 gap-6">
<div class="w-full max-w-md mx-auto hidden md:block">
```

**Rahmen/Schatten**:
```html
<div class="border border-gray-300 rounded-lg shadow-md hover:shadow-lg ring-2 ring-blue-500">
```

### Responsive (Mobile-First) {#responsive-mobile-first}
```html
<div class="text-sm md:text-base lg:text-lg">
<div class="flex-col md:flex-row">
<div class="grid-cols-1 sm:grid-cols-2 lg:grid-cols-4">
```

| Präfix | Min-Breite |
|--------|-----------|
| (keiner) | 0 (Mobil) |
| `sm:` | 640px |
| `md:` | 768px |
| `lg:` | 1024px |
| `xl:` | 1280px |

### Zustände {#states}
```html
<button class="bg-blue-500 hover:bg-blue-600 active:bg-blue-700 focus:ring-2">
<tr class="odd:bg-white even:bg-gray-50">
```

### group und peer {#group-and-peer}
```html
<!-- Style child on parent hover -->
<div class="group">
  <img class="group-hover:scale-105 transition" />
</div>

<!-- Style sibling on sibling state -->
<input class="peer" type="checkbox" />
<label class="peer-checked:text-blue-500">Option</label>
```

### Animationen {#animations}
```html
<div class="transition duration-300 ease-in-out hover:scale-105">
<div class="animate-spin">   <!-- Built-in -->
<div class="animate-pulse">  <!-- Skeleton loading -->
```

### Arbitrary Values {#arbitrary-values}
```html
<div class="w-[300px] bg-[#1a1a2e] grid-cols-[200px_1fr_200px]">
```

### @apply (Muster extrahieren) {#apply-extract-patterns}
```css
.btn-primary {
  @apply px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition;
}
```

Sparsam einsetzen – übermäßige Nutzung hebelt den utility-first Ansatz aus.

### Dark Mode {#dark-mode}
```html
<div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100">
```

## Vergleich {#comparison}

| Aspekt | CSS Modules | Tailwind |
|--------|-------------|----------|
| Ansatz | Traditionelles CSS, separate Dateien | Utility-Klassen im JSX |
| Bundle | Gesamtes geschriebenes CSS | Auf die verwendeten Klassen reduziert (purged) |
| Lernaufwand | CSS bereits bekannt | Utility-Namen lernen |
| Co-Location | Separate .module.css | Im Komponentendatei |
| Design-Konsistenz | Manuelle Disziplin | Durch die Utility-Skala erzwungen |
| Lesbarkeit | Übersichtliches JSX | Dichte Klassen-Strings |

Beide sind gültig. Viele Teams nutzen Tailwind für schnelle Entwicklung und CSS Modules für komplexe individuelle Komponenten.

## Stolperfallen {#gotchas}

- **CSS Modules globale Styles**: `:global(.class)` verwenden oder eine separate CSS-Datei ohne Modul-Status nutzen
- **Tailwind Purge**: Klassen müssen vollständige Strings sein, nicht zusammengesetzt: `bg-${color}-500` funktioniert nicht
- **Tailwind-Spezifität**: Utilities haben dieselbe Spezifität; die später stehende Klasse gewinnt (Reihenfolge zählt)
- **CSS Modules bei mehreren Klassen**: Template-Literale werden unübersichtlich; die Bibliothek `classnames` verwenden
- **Dynamisches Tailwind**: für bedingte Klassen einen ternären Operator verwenden: `isActive ? "bg-blue-500" : "bg-gray-500"`

## Siehe auch {#see-also}

- [[css-sass-and-methodology]] - BEM, SASS als alternative Ansätze
- [[css-flexbox]] - Flexbox, auf das Tailwind-Utilities abbilden
- [[css-grid]] - Grid-Utilities in Tailwind
- [[react-components-and-jsx]] - Komponentenstruktur
