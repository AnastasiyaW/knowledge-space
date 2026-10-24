---
title: "Frontend-Build-Systeme"
category: concepts
tags: [web-frontend, bundlers, webpack, vite, optimization, code-splitting]
level: 3
source_sha256: be46d21c8d4c4687c9a6a4c01c8d9a274958e101241d8fdcf0cf6380c489f907
translation: machine
translated_at: '2026-10-24'
---
# Frontend-Build-Systeme {#frontend-build-systems}

Bundler fassen Module zu optimierter Ausgabe zusammen. Entwicklung: IIFE -> AMD/CommonJS -> ES Modules -> moderne Bundler.

## Modulsysteme {#module-systems}

```javascript
// CommonJS (Node.js)
const lodash = require('lodash');
module.exports = { myFunc };

// ES Modules (modern standard, tree-shakeable)
import lodash from 'lodash';
export const myFunc = () => {};

// Dynamic import (code splitting point)
const module = await import('./heavy-module.js');
```

## Bundler-Vergleich {#bundler-comparison}

| Bundler | Stärken | Am besten geeignet für |
|---------|-----------|----------|
| **Vite** | ESM-Dev-Server (sofortiger Start), Rollup für den Build, integriertes TS/JSX/CSS | Neue Projekte, React/Vue |
| **Webpack** | Am ausgereiftesten, riesiges Ökosystem, konfigurationsintensiv | Komplexe/Legacy-Projekte |
| **Rollup** | Hervorragendes Tree-Shaking, saubere Ausgabe | Bibliotheken, npm-Pakete |
| **esbuild** | Auf Go basierend, 10-100x schneller | Build-Geschwindigkeit, zugrundeliegendes Werkzeug |
| **Turbopack** | Auf Rust basierend, inkrementell, in Next.js integriert | Next.js-Projekte |
| **SWC** | Rust-Transpiler, 20-70x schneller als Babel | Ersatz für Babel/Terser |

**Vite-Entwicklungsmodus**: kein Bundling, liefert ESM direkt an den Browser aus. Extrem schnelles HMR.

## Kernkonzepte {#core-concepts}

### Entry, Output, Loader {#entry-output-loaders}
```javascript
// webpack.config.js
module.exports = {
  entry: { main: './src/index.js', admin: './src/admin.js' },
  output: {
    filename: '[name].[contenthash].js',
    path: path.resolve(__dirname, 'dist'),
    clean: true
  },
  module: {
    rules: [
      { test: /\.css$/, use: ['style-loader', 'css-loader'] },
      { test: /\.tsx?$/, use: 'ts-loader' },
      { test: /\.(png|jpg|svg)$/, type: 'asset' }
    ]
  },
  resolve: {
    extensions: ['.ts', '.tsx', '.js'],
    alias: { '@': path.resolve(__dirname, 'src') }
  }
};
```

### HMR (Hot Module Replacement) {#hmr-hot-module-replacement}
Aktualisiert geänderte Module in der laufenden Anwendung OHNE vollständiges Neuladen der Seite und behält dabei den Zustand bei. Der Dev-Server erkennt die Änderung -> baut das Modul neu -> sendet es über WebSocket -> der Client patcht es. React Fast Refresh übernimmt dies automatisch.

## Transpilierung {#transpilation}

### Babel {#babel}
```javascript
// babel.config.js
module.exports = {
  presets: [
    ['@babel/preset-env', {
      targets: '> 0.25%, not dead',
      useBuiltIns: 'usage', corejs: 3
    }],
    '@babel/preset-react',
    '@babel/preset-typescript'
  ]
};
```

### Browserslist {#browserlist}
```json
"browserslist": ["> 0.5%", "last 2 versions", "not dead", "not IE 11"]
```

Gemeinsame Konfiguration für Babel, Autoprefixer, PostCSS.

## Optimierung {#optimization}

### Tree Shaking {#tree-shaking}
Entfernung von ungenutztem Code durch statische Analyse von ES-Module-`import`/`export`. CommonJS-`require()` kann nicht per Tree Shaking entfernt werden. `"sideEffects": false` in package.json markiert das Paket als sicher.

### Code Splitting {#code-splitting}
```javascript
// Dynamic import = split point
const AdminPanel = React.lazy(() => import('./AdminPanel'));

// Route-based (most common)
const routes = [
  { path: '/admin', component: () => import('./pages/Admin') }
];
```

### Minifizierung {#minification}
Terser (Standard), esbuild (schneller), SWC (am schnellsten). CSS: cssnano, Lightning CSS.

### Content Hashing {#content-hashing}
```javascript
filename: '[name].[contenthash:8].js'
```
Der Hash ändert sich nur, wenn sich der Inhalt ändert -> langfristiges Browser-Caching.

### Chunk Splitting {#chunk-splitting}
```javascript
optimization: {
  splitChunks: {
    chunks: 'all',
    cacheGroups: {
      vendor: { test: /node_modules/, name: 'vendors', priority: 10 }
    }
  }
}
```

Vendor-Code (ändert sich selten) von App-Code (ändert sich häufig) trennen -> besseres Caching.

## Source Maps {#source-maps}

```javascript
devtool: 'source-map'              // Full (production debug)
devtool: 'eval-source-map'         // Fast rebuild (dev)
devtool: false                      // Fastest build
```

Nicht in die Produktion ausliefern (legt den Quellcode offen). Stattdessen in ein Error-Tracking-System (Sentry) hochladen.

## Asset-Behandlung {#asset-handling}

- **Bilder < 8 KB**: als Base64 eingebettet; größere werden als Dateien ausgegeben
- **CSS**: `css-loader` (löst Imports auf), `style-loader` (Injektion im Dev-Modus), `MiniCssExtractPlugin` (Dateien für Produktion)
- **CSS Modules**: lokal gescopte Klassennamen
- **PostCSS**: Transformationspipeline (Autoprefixer, cssnano)
- **Fonts**: WOFF2 als Assets

## Bibliothek vs. Anwendung {#library-vs-application}

| Aspekt | Anwendung | Bibliothek |
|---------|------------|---------|
| Modulformat | ESM | ESM + CJS (dual) |
| Abhängigkeiten | Gebündelt | Extern (peerDeps) |
| Tree Shaking | Aufgabe des Konsumenten | Muss schüttelbar sein |

```json
{
  "main": "./dist/index.cjs",
  "module": "./dist/index.mjs",
  "types": "./dist/index.d.ts",
  "exports": { ".": { "import": "./dist/index.mjs", "require": "./dist/index.cjs" } },
  "sideEffects": false
}
```

## Stolperfallen {#gotchas}

- **CommonJS verhindert Tree Shaking**: ESM-Imports für tree-shakebare Bundles verwenden
- **Source Maps in der Produktion**: legen Quellcode den Nutzern offen
- **Bundle-Analyzer**: `webpack-bundle-analyzer` verwenden, um Größenprobleme zu finden
- **Übermäßiges Splitting**: zu viele Chunks = zu viele HTTP-Anfragen; Anzahl der Chunks und deren Größe ausbalancieren
- **Dynamische Klassennamen brechen Purging**: Tailwind/PurgeCSS benötigen vollständige statische Strings

## Siehe auch {#see-also}

- [[npm-and-task-runners]] - npm, Gulp, Paketverwaltung
- [[git-and-github]] - CI/CD löst Builds aus
- [[react-rendering-internals]] - Code Splitting mit React.lazy
- [[typescript-fundamentals]] - TypeScript-Kompilierung
- [[architectural-styles]] - Microfrontends mit Module Federation
