---
title: npm and Task Runners
category: concepts
tags: [web-frontend, npm, gulp, package-management, node]
---

# npm and Task Runners

Node.js runtime + npm package manager form the foundation of frontend tooling. Task runners automate repetitive dev tasks.

## Node.js

JavaScript runtime outside the browser. Required for npm, build tools, SASS compilation. Install LTS from nodejs.org. Verify: `node -v`, `npm -v`.

## npm Basics

### Initialize
```bash
npm init -y              # Creates package.json with defaults
```

### package.json
```json
{
  "name": "my-project",
  "version": "1.0.0",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "sass": "sass --watch src/scss:dist/css"
  },
  "dependencies": {
    "normalize.css": "^8.0.1"
  },
  "devDependencies": {
    "sass": "^1.72.0",
    "vite": "^5.0.0"
  }
}
```

### Install Packages
```bash
npm install package-name        # Production dependency
npm install package-name -D     # Dev dependency
npm install                     # All from package.json
npm install package@version     # Specific version
npm uninstall package-name
npm update                      # Within semver range
```

### dependencies vs devDependencies
- **dependencies**: runtime (normalize.css, lodash)
- **devDependencies**: build/dev only (sass, vite, eslint)

### node_modules
- Created by `npm install`, can be huge
- **Always in .gitignore** (regenerated from package.json)

### package-lock.json
- Locks exact versions of all packages + sub-dependencies
- **Commit to Git** (deterministic builds across machines)

### npm Scripts
```json
"scripts": {
  "dev": "vite",
  "build": "vite build",
  "lint": "eslint src/"
}
```
Run: `npm run dev`. Special: `npm start` and `npm test` don't need `run`.

## Gulp (Task Runner)

Automates: SASS compilation, CSS minification, image optimization, live reload.

```bash
npm install gulp gulp-sass sass browser-sync gulp-clean-css gulp-autoprefixer -D
```

### gulpfile.js
```javascript
const { src, dest, watch, series } = require('gulp');
const sass = require('gulp-sass')(require('sass'));
const cleanCSS = require('gulp-clean-css');
const autoprefixer = require('gulp-autoprefixer');
const browserSync = require('browser-sync').create();

function styles() {
  return src('src/scss/**/*.scss')
    .pipe(sass().on('error', sass.logError))
    .pipe(autoprefixer())
    .pipe(cleanCSS())
    .pipe(dest('dist/css'))
    .pipe(browserSync.stream());
}

function serve() {
  browserSync.init({ server: { baseDir: './dist' } });
  watch('src/scss/**/*.scss', styles);
  watch('dist/*.html').on('change', browserSync.reload);
}

exports.default = series(styles, serve);
```

## SASS CLI (without Gulp)

```bash
npm install -g sass
sass --watch src/scss:dist/css
sass --watch src/scss:dist/css --style=compressed
```

## Mobile Testing

With local dev server running:
1. Find local IP: `ipconfig` (Windows) / `ifconfig` (Mac)
2. Same Wi-Fi network
3. Access `http://YOUR-IP:PORT` from mobile browser
4. BrowserSync shows external URL in terminal

## Gotchas

- **node_modules in git**: always add to .gitignore before first commit
- **Missing `name` in package.json**: `npm install` may fail for scoped packages
- **Semver `^` vs `~`**: `^1.2.3` allows minor updates (1.x.x), `~1.2.3` allows patches only (1.2.x)
- **Global vs local install**: prefer local (`-D`) to avoid version conflicts across projects
- **`npx`**: runs local package binaries without `./node_modules/.bin/` prefix

## See Also

- [[frontend-build-systems]] - Webpack, Vite, bundling
- [[css-sass-and-methodology]] - SASS language features
- [[git-and-github]] - .gitignore, version control
- [[event-loop-and-architecture]] - Node.js server-side development
