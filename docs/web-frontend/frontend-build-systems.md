---
title: Frontend Build Systems
category: concepts
tags: [web-frontend, bundlers, webpack, vite, optimization, code-splitting]
---

# Frontend Build Systems

Bundlers combine modules into optimized output. Evolution: IIFE -> AMD/CommonJS -> ES Modules -> modern bundlers.

## Module Systems

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

## Bundler Comparison

| Bundler | Strengths | Best For |
|---------|-----------|----------|
| **Vite** | ESM dev server (instant start), Rollup for build, built-in TS/JSX/CSS | New projects, React/Vue |
| **Webpack** | Most mature, huge ecosystem, config-heavy | Complex/legacy projects |
| **Rollup** | Excellent tree-shaking, clean output | Libraries, npm packages |
| **esbuild** | Go-based, 10-100x faster | Build speed, underlying tool |
| **Turbopack** | Rust-based, incremental, Next.js integrated | Next.js projects |
| **SWC** | Rust transpiler, 20-70x faster than Babel | Replace Babel/Terser |

**Vite dev mode**: no bundling, serves ESM directly to browser. Extremely fast HMR.

## Core Concepts

### Entry, Output, Loaders
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

### HMR (Hot Module Replacement)
Updates changed modules in running app WITHOUT full page reload, preserving state. Dev server detects change -> rebuilds module -> sends via WebSocket -> client patches. React Fast Refresh handles this automatically.

## Transpilation

### Babel
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

### Browserlist
```json
"browserslist": ["> 0.5%", "last 2 versions", "not dead", "not IE 11"]
```

Shared config for Babel, Autoprefixer, PostCSS.

## Optimization

### Tree Shaking
Dead code elimination via static analysis of ES Module `import`/`export`. CommonJS `require()` can't be tree-shaken. `"sideEffects": false` in package.json marks package as safe.

### Code Splitting
```javascript
// Dynamic import = split point
const AdminPanel = React.lazy(() => import('./AdminPanel'));

// Route-based (most common)
const routes = [
  { path: '/admin', component: () => import('./pages/Admin') }
];
```

### Minification
Terser (standard), esbuild (faster), SWC (fastest). CSS: cssnano, Lightning CSS.

### Content Hashing
```javascript
filename: '[name].[contenthash:8].js'
```
Hash changes only when content changes -> long-term browser caching.

### Chunk Splitting
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

Separate vendor (changes rarely) from app code (changes often) -> better caching.

## Source Maps

```javascript
devtool: 'source-map'              // Full (production debug)
devtool: 'eval-source-map'         // Fast rebuild (dev)
devtool: false                      // Fastest build
```

Don't ship to production (exposes source). Upload to error tracking (Sentry) instead.

## Asset Handling

- **Images < 8KB**: inlined as base64; larger emitted as files
- **CSS**: `css-loader` (resolves imports), `style-loader` (dev inject), `MiniCssExtractPlugin` (prod files)
- **CSS Modules**: locally scoped class names
- **PostCSS**: transformation pipeline (autoprefixer, cssnano)
- **Fonts**: WOFF2 as assets

## Library vs Application

| Concern | Application | Library |
|---------|------------|---------|
| Module format | ESM | ESM + CJS (dual) |
| Dependencies | Bundled | External (peerDeps) |
| Tree-shaking | Consumer's job | Must be shakeable |

```json
{
  "main": "./dist/index.cjs",
  "module": "./dist/index.mjs",
  "types": "./dist/index.d.ts",
  "exports": { ".": { "import": "./dist/index.mjs", "require": "./dist/index.cjs" } },
  "sideEffects": false
}
```

## Gotchas

- **CommonJS blocks tree-shaking**: use ESM imports for tree-shakeable bundles
- **Source maps in production**: expose source code to users
- **Bundle analyzer**: use `webpack-bundle-analyzer` to find size problems
- **Over-splitting**: too many chunks = too many HTTP requests; balance chunk count vs size
- **Dynamic class names break purging**: Tailwind/PurgeCSS need complete static strings

## See Also

- [[npm-and-task-runners]] - npm, Gulp, package management
- [[git-and-github]] - CI/CD triggers builds
- [[react-rendering-internals]] - Code splitting with React.lazy
- [[typescript-fundamentals]] - TypeScript compilation
- [[architecture]] - Microfrontends with Module Federation
