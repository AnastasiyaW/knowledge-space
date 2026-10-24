---
title: "npm und Task-Runner"
category: concepts
tags: [web-frontend, npm, gulp, package-management, node]
level: 3
source_sha256: 452196e5557285b20731f8b5dca8f3b049e95a7faa01502d9355c50eceb4f8d0
translation: machine
translated_at: '2026-10-24'
---
# npm und Task-Runner {#npm-and-task-runners}

Node.js-Laufzeitumgebung und npm-Paketmanager bilden das Fundament der Frontend-Tooling-Landschaft. Task-Runner automatisieren wiederkehrende Entwicklungsaufgaben.

## Node.js {#nodejs}

JavaScript-Laufzeitumgebung außerhalb des Browsers. Erforderlich für npm, Build-Tools und die SASS-Kompilierung. LTS-Version von nodejs.org installieren. Prüfen: `node -v`, `npm -v`.

## npm-Grundlagen {#npm-basics}

### Initialisieren {#initialize}
```bash
npm init -y              # Creates package.json with defaults
```

### package.json {#packagejson}
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

### Pakete installieren {#install-packages}
```bash
npm install package-name        # Production dependency
npm install package-name -D     # Dev dependency
npm install                     # All from package.json
npm install package@version     # Specific version
npm uninstall package-name
npm update                      # Within semver range
```

### dependencies vs. devDependencies {#dependencies-vs-devdependencies}
- **dependencies**: Laufzeit (normalize.css, lodash)
- **devDependencies**: nur Build/Entwicklung (sass, vite, eslint)

### node_modules {#node_modules}
- Wird von `npm install` erstellt und kann sehr groß werden
- **Immer in .gitignore** (wird aus package.json neu erzeugt)

### package-lock.json {#package-lockjson}
- Fixiert die exakten Versionen aller Pakete sowie deren Unterabhängigkeiten
- **In Git committen** (deterministische Builds auf allen Rechnern)

### npm-Skripte {#npm-scripts}
```json
"scripts": {
  "dev": "vite",
  "build": "vite build",
  "lint": "eslint src/"
}
```
Ausführen: `npm run dev`. Besonderheit: `npm start` und `npm test` benötigen kein `run`.

## Gulp (Task-Runner) {#gulp-task-runner}

Automatisiert: SASS-Kompilierung, CSS-Minifizierung, Bildoptimierung, Live-Reload.

```bash
npm install gulp gulp-sass sass browser-sync gulp-clean-css gulp-autoprefixer -D
```

### gulpfile.js {#gulpfilejs}
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

## SASS-CLI (ohne Gulp) {#sass-cli-without-gulp}

```bash
npm install -g sass
sass --watch src/scss:dist/css
sass --watch src/scss:dist/css --style=compressed
```

## Testen auf mobilen Geräten {#mobile-testing}

Bei laufendem lokalem Dev-Server:
1. Lokale IP ermitteln: `ipconfig` (Windows) / `ifconfig` (Mac)
2. Im selben Wi-Fi-Netzwerk sein
3. `http://YOUR-IP:PORT` im mobilen Browser aufrufen
4. BrowserSync zeigt die externe URL im Terminal an

## Stolperfallen {#gotchas}

- **node_modules in Git**: vor dem ersten Commit immer in .gitignore eintragen
- **Fehlendes `name` in package.json**: `npm install` kann bei Scoped Packages fehlschlagen
- **Semver `^` vs. `~`**: `^1.2.3` erlaubt Minor-Updates (1.x.x), `~1.2.3` erlaubt nur Patch-Updates (1.2.x)
- **Globale vs. lokale Installation**: lokale Installation (`-D`) bevorzugen, um Versionskonflikte zwischen Projekten zu vermeiden
- **`npx`**: führt lokale Paket-Binaries aus, ohne das Präfix `./node_modules/.bin/`

## Siehe auch {#see-also}

- [[frontend-build-systems]] - Webpack, Vite, Bundling
- [[css-sass-and-methodology]] - SASS-Sprachfeatures
- [[git-and-github]] - .gitignore, Versionskontrolle
- [[event-loop-and-architecture]] - Node.js-Serverentwicklung
