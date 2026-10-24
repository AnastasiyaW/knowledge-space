---
title: "Systèmes de build frontend"
category: concepts
tags: [web-frontend, bundlers, webpack, vite, optimization, code-splitting]
level: 3
source_sha256: be46d21c8d4c4687c9a6a4c01c8d9a274958e101241d8fdcf0cf6380c489f907
translation: machine
translated_at: '2026-10-24'
---
# Systèmes de build frontend {#frontend-build-systems}

Les bundlers combinent les modules en une sortie optimisée. Évolution : IIFE -> AMD/CommonJS -> ES Modules -> bundlers modernes.

## Systèmes de modules {#module-systems}

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

## Comparaison des bundlers {#bundler-comparison}

| Bundler | Points forts | Idéal pour |
|---------|-----------|----------|
| **Vite** | Serveur de dev ESM (démarrage instantané), Rollup pour le build, TS/JSX/CSS intégrés | Nouveaux projets, React/Vue |
| **Webpack** | Le plus mature, écosystème immense, très configurable | Projets complexes/legacy |
| **Rollup** | Tree-shaking excellent, sortie propre | Bibliothèques, paquets npm |
| **esbuild** | Écrit en Go, 10 à 100 fois plus rapide | Vitesse de build, outil sous-jacent |
| **Turbopack** | Écrit en Rust, incrémental, intégré à Next.js | Projets Next.js |
| **SWC** | Transpileur en Rust, 20 à 70 fois plus rapide que Babel | Remplacer Babel/Terser |

**Mode dev de Vite** : pas de bundling, sert l'ESM directement au navigateur. HMR extrêmement rapide.

## Concepts fondamentaux {#core-concepts}

### Entrée, sortie, loaders {#entry-output-loaders}
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
Met à jour les modules modifiés dans l'application en cours d'exécution SANS rechargement complet de la page, en préservant l'état. Le serveur de dev détecte le changement -> reconstruit le module -> l'envoie via WebSocket -> le client applique le correctif. React Fast Refresh gère cela automatiquement.

## Transpilation {#transpilation}

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

Configuration partagée entre Babel, Autoprefixer, PostCSS.

## Optimisation {#optimization}

### Tree Shaking {#tree-shaking}
Élimination du code mort par analyse statique des `import`/`export` des ES Modules. Le `require()` de CommonJS ne peut pas être éliminé par tree-shaking. `"sideEffects": false` dans package.json indique que le paquet est sûr.

### Code Splitting {#code-splitting}
```javascript
// Dynamic import = split point
const AdminPanel = React.lazy(() => import('./AdminPanel'));

// Route-based (most common)
const routes = [
  { path: '/admin', component: () => import('./pages/Admin') }
];
```

### Minification {#minification}
Terser (standard), esbuild (plus rapide), SWC (le plus rapide). CSS : cssnano, Lightning CSS.

### Content Hashing {#content-hashing}
```javascript
filename: '[name].[contenthash:8].js'
```
Le hash ne change que lorsque le contenu change -> mise en cache longue durée côté navigateur.

### Découpage en chunks {#chunk-splitting}
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

Séparer le vendor (change rarement) du code applicatif (change souvent) -> meilleure mise en cache.

## Source Maps {#source-maps}

```javascript
devtool: 'source-map'              // Full (production debug)
devtool: 'eval-source-map'         // Fast rebuild (dev)
devtool: false                      // Fastest build
```

Ne pas les déployer en production (expose le code source). Les envoyer plutôt à un outil de suivi d'erreurs (Sentry).

## Gestion des assets {#asset-handling}

- **Images < 8 Ko** : intégrées en base64 ; les plus grandes sont émises sous forme de fichiers
- **CSS** : `css-loader` (résout les imports), `style-loader` (injection en dev), `MiniCssExtractPlugin` (fichiers en prod)
- **CSS Modules** : noms de classes à portée locale
- **PostCSS** : chaîne de transformation (autoprefixer, cssnano)
- **Polices** : WOFF2 comme assets

## Bibliothèque vs application {#library-vs-application}

| Préoccupation | Application | Bibliothèque |
|---------|------------|---------|
| Format de module | ESM | ESM + CJS (double) |
| Dépendances | Intégrées au bundle | Externes (peerDeps) |
| Tree-shaking | À la charge du consommateur | Doit être éliminable par tree-shaking |

```json
{
  "main": "./dist/index.cjs",
  "module": "./dist/index.mjs",
  "types": "./dist/index.d.ts",
  "exports": { ".": { "import": "./dist/index.mjs", "require": "./dist/index.cjs" } },
  "sideEffects": false
}
```

## Pièges à éviter {#gotchas}

- **CommonJS bloque le tree-shaking** : utiliser les imports ESM pour des bundles éliminables par tree-shaking
- **Source maps en production** : exposent le code source aux utilisateurs
- **Analyseur de bundle** : utiliser `webpack-bundle-analyzer` pour repérer les problèmes de taille
- **Sur-découpage** : trop de chunks = trop de requêtes HTTP ; trouver l'équilibre entre nombre et taille des chunks
- **Noms de classes dynamiques cassent le purge** : Tailwind/PurgeCSS ont besoin de chaînes statiques complètes

## Voir aussi {#see-also}

- [[npm-and-task-runners]] - npm, Gulp, gestion des paquets
- [[git-and-github]] - la CI/CD déclenche les builds
- [[react-rendering-internals]] - Code splitting avec React.lazy
- [[typescript-fundamentals]] - compilation TypeScript
- [[architectural-styles]] - Microfrontends avec Module Federation
