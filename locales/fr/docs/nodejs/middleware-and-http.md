---
title: "Middleware et HTTP"
category: concepts
tags: [nodejs, middleware, http, fastify, express, transport, static-files]
level: 3
source_sha256: 2ef1ee37fedebc5d5cba67ade6f2c293c864d7177767ac123af825e1b37a75e8
translation: machine
translated_at: '2026-10-24'
---
# Middleware et HTTP {#middleware-and-http}

La gestion HTTP dans Node.js va des serveurs purs Node.js aux approches basées sur des frameworks (Fastify, NestJS, Metarhia). Le middleware implémente le patron Chain of Responsibility, et l'abstraction du transport permet de basculer entre HTTP et WebSocket sans modifier la logique métier.

## Points clés {#key-facts}

- Le middleware dans Express/Fastify relève du Chain of Responsibility : chaque handler décide de traiter la requête ou de la transmettre à `next()`
- Abstraction du transport : les handlers HTTP et WebSocket partagent la logique métier et ne diffèrent que par le transport des données
- Service des fichiers statiques : toujours vérifier l'existence du fichier avant de l'envoyer (404 vs 500)
- La même application implémentée avec Pure Node.js, Fastify, NestJS et Metarhia montre que la logique métier est identique et que seul le code boilerplate du framework diffère

## Patterns {#patterns}

### Comparaison multi-framework {#multi-framework-comparison}

```javascript
metatech-university/
  NodeJS-Pure/         # Pure Node.js (no framework)
  NodeJS-Fastify/      # Fastify - lightweight, good DX
  NodeJS-Nest/         # NestJS - enterprise-grade, TypeScript-first
  NodeJS-Metarhia/     # Metarhia - schema-driven, transport-abstracted

All implement: user registration, authentication, session management,
messaging, file upload, room management, push notifications
```

### Basculement de configuration du transport {#transport-config-switching}

```js
// config.js
module.exports = { transport: 'ws' }; // or 'http'

// main.js - load transport module dynamically
const transport = require(`./${config.transport}.js`);
// Enables: per-environment transport, A/B testing, fallback mechanisms
```

### Configuration ESLint partagée {#eslint-shared-configuration}

```javascript
eslint-config-metarhia/     # Shared rules package
  index.js                  # Rules in JavaScript (not JSON)
  browser.js                # Browser-specific overrides
  node.js                   # Node-specific overrides
```

Chaque projet étend cette configuration et la surcharge éventuellement. Gestion centralisée des règles, avec une flexibilité par dépôt.

## Pièges {#gotchas}

- Un serveur Pure Node.js est peu volumineux en code, mais complexe à maintenir à grande échelle
- Le choix du framework compte moins que la qualité de l'architecture : tous les frameworks peuvent produire le même résultat
- Le workflow de pull request pour les bibliothèques d'infrastructure doit stabiliser la structure avant d'écrire les tests (pour éviter le churn de tests)

## Voir aussi {#see-also}

- [[application-architecture]] - abstraction du transport, conception de serveur en couches
- [Design Patterns (GoF) in JavaScript](design-patterns-gof.md) - Chain of Responsibility comme patron de middleware
- [Gestion des erreurs](error-handling.md) - gestion des erreurs dans les pipelines de requêtes
