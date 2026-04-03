---
title: Webpack and Vite - Frontend Build Tools
category: build-tools
tags: [webpack, vite, bundler, build-tools, code-splitting, tree-shaking, hmr]
---

# Webpack and Vite - Frontend Build Tools

## Key Facts

- **Bundlers** transform source files (JS/TS, CSS, images) into optimized bundles for the browser
- **Webpack**: mature, highly configurable, plugin ecosystem; uses `webpack.config.js`
- **Vite**: modern, fast dev server (native ES modules), Rollup-based production build
- **Code splitting**: break bundle into chunks loaded on demand; `import()` dynamic imports
- **Tree shaking**: eliminate unused exports from bundle; requires ES module `import/export` syntax
- **HMR** (Hot Module Replacement): update modules in browser without full page reload
- **Loaders** (Webpack): transform files - `babel-loader` (JS), `css-loader`, `file-loader`
- **Plugins** (Webpack): `HtmlWebpackPlugin`, `MiniCssExtractPlugin`, `DefinePlugin`
- Vite uses `vite.config.ts`; dev server serves source directly via ES modules (no bundling in dev)
- `import.meta.env.VITE_*` for environment variables in Vite; `process.env` in Webpack
- Related: [[react-components-and-jsx]], [[typescript-type-system]]

## Patterns

### Vite Config (React + TypeScript)

```typescript
// vite.config.ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    port: 3000,
    proxy: {
      "/api": {
        target: "http://localhost:8080",
        changeOrigin: true,
      },
    },
  },
  build: {
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ["react", "react-dom"],
        },
      },
    },
  },
});
```

### Webpack Config (Essential)

```javascript
// webpack.config.js
const HtmlWebpackPlugin = require("html-webpack-plugin");
const path = require("path");

module.exports = {
  entry: "./src/index.tsx",
  output: {
    path: path.resolve(__dirname, "dist"),
    filename: "[name].[contenthash].js",
    clean: true,
  },
  module: {
    rules: [
      { test: /\.tsx?$/, use: "ts-loader", exclude: /node_modules/ },
      { test: /\.css$/, use: ["style-loader", "css-loader", "postcss-loader"] },
      { test: /\.(png|svg|jpg)$/, type: "asset/resource" },
    ],
  },
  resolve: {
    extensions: [".tsx", ".ts", ".js"],
    alias: { "@": path.resolve(__dirname, "src") },
  },
  plugins: [
    new HtmlWebpackPlugin({ template: "./public/index.html" }),
  ],
  devServer: {
    port: 3000,
    hot: true,
    historyApiFallback: true, // for SPA routing
  },
};
```

### Dynamic Import (Code Splitting)

```typescript
// Route-based splitting (works with both Webpack and Vite)
const Dashboard = React.lazy(() => import("./pages/Dashboard"));

// Named chunk (Webpack magic comment)
const AdminPanel = React.lazy(() =>
  import(/* webpackChunkName: "admin" */ "./pages/AdminPanel")
);
```

### Environment Variables

```bash
# Vite: .env file (must prefix with VITE_)
VITE_API_URL=https://api.example.com

# Webpack: use DefinePlugin or dotenv-webpack
# process.env.REACT_APP_API_URL (Create React App)
```

```typescript
// Vite access
const apiUrl = import.meta.env.VITE_API_URL;

// Webpack access
const apiUrl = process.env.REACT_APP_API_URL;
```

## Gotchas

- Tree shaking requires ES module syntax (`import`/`export`); `require()` / `module.exports` prevents it
- `contenthash` in output filenames enables long-term caching; without it, browsers cache stale bundles
- Vite dev server uses ES modules natively; some libraries with CJS-only builds need `optimizeDeps.include` in config
- `historyApiFallback: true` (Webpack) or equivalent is required for SPAs with client-side routing; without it, direct URL access returns 404
- Source maps in production expose source code; use `hidden-source-map` for error tracking without public exposure

## See Also

- [Vite: Getting Started](https://vitejs.dev/guide/)
- [Webpack: Concepts](https://webpack.js.org/concepts/)
