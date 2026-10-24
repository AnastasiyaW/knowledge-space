---
title: "npm et gestionnaires de tâches"
category: concepts
tags: [web-frontend, npm, gulp, package-management, node]
level: 3
source_sha256: 452196e5557285b20731f8b5dca8f3b049e95a7faa01502d9355c50eceb4f8d0
translation: machine
translated_at: '2026-10-24'
---
# npm et gestionnaires de tâches {#npm-and-task-runners}

L'environnement d'exécution Node.js associé au gestionnaire de paquets npm constitue la base de l'outillage frontend. Les gestionnaires de tâches automatisent les tâches de développement répétitives.

## Node.js {#nodejs}

Environnement d'exécution JavaScript en dehors du navigateur. Requis pour npm, les outils de build et la compilation SASS. Installer la version LTS depuis nodejs.org. Vérification : `node -v`, `npm -v`.

## Bases de npm {#npm-basics}

### Initialisation {#initialize}
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

### Installation des paquets {#install-packages}
```bash
npm install package-name        # Production dependency
npm install package-name -D     # Dev dependency
npm install                     # All from package.json
npm install package@version     # Specific version
npm uninstall package-name
npm update                      # Within semver range
```

### dependencies vs devDependencies {#dependencies-vs-devdependencies}
- **dependencies** : exécution (normalize.css, lodash)
- **devDependencies** : build/développement uniquement (sass, vite, eslint)

### node_modules {#node_modules}
- Créé par `npm install`, peut être très volumineux
- **Toujours dans .gitignore** (regénéré à partir de package.json)

### package-lock.json {#package-lockjson}
- Verrouille les versions exactes de tous les paquets et de leurs sous-dépendances
- **À committer dans Git** (builds déterministes d'une machine à l'autre)

### Scripts npm {#npm-scripts}
```json
"scripts": {
  "dev": "vite",
  "build": "vite build",
  "lint": "eslint src/"
}
```
Exécution : `npm run dev`. Cas particuliers : `npm start` et `npm test` ne nécessitent pas `run`.

## Gulp (gestionnaire de tâches) {#gulp-task-runner}

Automatise : la compilation SASS, la minification CSS, l'optimisation des images, le rechargement en direct.

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

## CLI SASS (sans Gulp) {#sass-cli-without-gulp}

```bash
npm install -g sass
sass --watch src/scss:dist/css
sass --watch src/scss:dist/css --style=compressed
```

## Tests sur mobile {#mobile-testing}

Avec le serveur de développement local en cours d'exécution :
1. Trouver l'IP locale : `ipconfig` (Windows) / `ifconfig` (Mac)
2. Être sur le même réseau Wi-Fi
3. Accéder à `http://YOUR-IP:PORT` depuis le navigateur mobile
4. BrowserSync affiche l'URL externe dans le terminal

## Pièges courants {#gotchas}

- **node_modules dans git** : toujours l'ajouter à .gitignore avant le premier commit
- **`name` absent de package.json** : `npm install` peut échouer pour les paquets scopés
- **Semver `^` vs `~`** : `^1.2.3` autorise les mises à jour mineures (1.x.x), `~1.2.3` n'autorise que les correctifs (1.2.x)
- **Installation globale vs locale** : privilégier l'installation locale (`-D`) pour éviter les conflits de versions entre projets
- **`npx`** : exécute les binaires des paquets locaux sans le préfixe `./node_modules/.bin/`

## Voir aussi {#see-also}

- [[frontend-build-systems]] - Webpack, Vite, bundling
- [[css-sass-and-methodology]] - Fonctionnalités du langage SASS
- [[git-and-github]] - .gitignore, gestion de version
- [[event-loop-and-architecture]] - Développement serveur avec Node.js
