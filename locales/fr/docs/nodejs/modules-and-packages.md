---
title: "Modules et packages"
category: concepts
tags: [nodejs, modules, commonjs, esm, require, import, package-lock, npm]
level: 3
source_sha256: 8b1418bc62efa5678c6ad4322622a213bdb18cb6e4d817025b0ca724dc9f51ef
translation: machine
translated_at: '2026-10-24'
---
# Modules et packages {#modules-and-packages}

Node.js prend en charge deux systèmes de modules : CommonJS (`require`/`module.exports`) et ESM (`import`/`export`). Les deux coexistent et continueront de le faire indéfiniment, car supprimer `require` de Node.js exigerait une réécriture complète. Le système de modules fournit nativement un comportement de singleton, des capacités d'injection de dépendances (DI) et une isolation de portée.

## Points clés {#key-facts}

- `require()` est synchrone, `import` est asynchrone
- Node.js assure une bonne interopérabilité entre les deux systèmes
- Le cache des modules en CommonJS fournit un comportement de singleton par défaut : `require()` renvoie la même instance
- Dans Node.js, il n'existe pas de véritable portée globale pour le code utilisateur : chaque module est encapsulé dans une fonction, ce qui crée une portée au niveau du module
- En JavaScript côté navigateur, tous les fichiers partagent une même portée, sauf s'ils sont encapsulés dans des IIFE ou utilisent des bundlers de modules
- `import.meta.url` fournit l'URL du fichier en ESM ; utilisez `createRequire(import.meta.url)` pour obtenir `require()` en ESM
- Validez toujours `package-lock.json` dans le dépôt : même les versions de correctif peuvent tout casser à cause des dépendances transitives

### Les modules comme alternative à la DI {#modules-as-di-alternative}

Le système de modules JavaScript peut remplacer de nombreux patrons de DI :
- **Singleton :** le cache des modules renvoie la même instance
- **Stratégie :** exporter un objet ou une Map contenant les implémentations de stratégies
- **Configuration :** exporter un objet de configuration et l'importer là où il est nécessaire
- **Fabrique :** exporter des fonctions de fabrique

## Patrons {#patterns}

### ESM dans Node.js avec interopérabilité CommonJS {#esm-in-nodejs-with-commonjs-interop}

```js
// Using require() inside ESM
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const fs = require('fs'); // CommonJS require inside ESM
```

### Configuration sous forme de module {#config-as-module}

```js
// config.js
module.exports = {
  port: 8000,
  db: { host: 'localhost', port: 5432, database: 'app' },
  crypto: { saltLength: 16, keyLength: 64 },
  session: { timeout: 3600000 },
  transport: 'ws', // 'http' or 'ws'
};

// main.js - dynamic transport loading
const config = require('./config');
const transport = require(`./${config.transport}.js`);
```

### Importance de package-lock.json {#package-lockjson-importance}

`package.json` utilise des plages semver. Le fichier de verrouillage garantit des builds déterministes, pour les raisons suivantes :
- Une dépendance peut introduire une dépendance transitive modifiée
- Plusieurs packages peuvent avoir des exigences de version en conflit
- Un correctif dans un package peut modifier involontairement le comportement dont dépend un autre package

## Pièges courants {#gotchas}

- ESM est issu de l'écosystème frontend comme effort d'unification : CJS et ESM coexisteront indéfiniment dans Node.js
- `require()` renvoie le module mis en cache dès le second appel : les mutations de l'objet exporté sont visibles partout
- Les dépendances circulaires fonctionnent en CJS (le module partiellement chargé est renvoyé), mais peuvent provoquer des bogues subtils

## Voir aussi {#see-also}

- [[dependency-injection]] - DI et système de modules pour le découplage
- [[application-architecture]] - comment les modules s'intègrent dans une architecture en couches
- [[solid-and-grasp]] - le principe SRP appliqué à la conception des modules
