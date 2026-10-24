---
title: "Architecture applicative"
category: concepts
tags: [nodejs, architecture, ddd, layers, transport, context-isolation, server-structure]
level: 3
source_sha256: 87dfd82c028d8beaead5a4502d949b620488e886714576a8802269fc6246bf2a
translation: machine
translated_at: '2026-10-24'
---
# Architecture applicative {#application-architecture}

L'architecture d'une application Node.js repose sur la séparation en couches, l'abstraction du transport et l'isolation des contextes. La structure d'inspiration DDD garde la logique métier pure, indépendante du transport et pilotée par les schémas. Le principal défi pour les développeurs n'est pas la connaissance du framework ni les patterns asynchrones, mais la structuration de l'application.

## Points clés {#key-facts}

- La logique métier doit être pure : pas d'I/O, pas de dépendances au framework
- La couche transport ne diffère que par la manière dont les données sont envoyées/reçues (HTTP, WebSocket ou gRPC)
- Développement piloté par les schémas : définir les schémas en premier, puis générer les tables de base de données, les validateurs, les types, la documentation et les SDK
- Les schémas comme source unique de vérité empêchent la dérive entre les couches
- La configuration détermine le transport à l'exécution, ce qui permet de faire de l'A/B testing entre protocoles
- La même application de chat implémentée avec Pure Node.js, Fastify, NestJS et Metarhia montre que la logique du domaine reste identique ; seul le code boilerplate du framework change

## Quatre niveaux de contexte {#four-context-levels}

Les serveurs Node.js ont besoin d'un état isolé à quatre niveaux, avec des durées de vie différentes :

```text
Application Context (global, persistent)
  └─ Session Context (per-user, persistent, TTL)
      └─ Connection Context (per-socket, transient)
          └─ Call Context (per-request, shortest-lived)
```

1. **Contexte d'appel** - un appel de requête/RPC. Objets de requête et de réponse. Détruit après la réponse
2. **Contexte de connexion** - une connexion TCP/WebSocket. Métadonnées. Détruit à la déconnexion
3. **Contexte de session** - persiste à travers les connexions (adossé à la BD). Authentification, TTL configurable
4. **Contexte applicatif** - singleton global. Configuration, caches, pools de connexions

### Implémentation avec des champs privés {#implementation-with-private-fields}

```js
class Context {
  #session;
  #connection;
  #call;

  constructor(session, connection) {
    this.#session = session;
    this.#connection = connection;
  }

  startCall(request) {
    this.#call = { request, startTime: Date.now() };
    return this;
  }
}
```

Node.js moderne (16+) : utilisez la syntaxe `#privateField` plutôt que les closures ou le privé basé sur Symbol.

## Patterns {#patterns}

### Abstraction du transport {#transport-abstraction}

```js
// config.js
module.exports = { transport: 'ws' }; // or 'http'

// main.js
const transport = require(`./${config.transport}.js`);
// Domain logic is transport-agnostic
```

### Contexte par requête (Fastify) {#per-request-context-fastify}

```js
fastify.addHook('preHandler', (request) => {
  request.context = {
    logger: createLogger({ requestId: request.id }),
    db: connectionPool,
  };
});

async function transferMoney(context, from, to, amount) {
  const tx = await context.db.beginTransaction();
  // All queries use same connection; logger auto-injects requestId
  await tx.commit();
}
```

Le logger récupère automatiquement `request.id` : chaque entrée de log est traçable sans propagation manuelle.

### Scaffold - client API dynamique {#scaffold-dynamic-api-client}

```js
const scaffold = (url, structure) => {
  const api = {};
  for (const [entity, methods] of Object.entries(structure)) {
    api[entity] = {};
    for (const method of methods) {
      api[entity][method] = (...args) =>
        fetch(`${url}/${entity}/${method}`, {
          method: 'POST', body: JSON.stringify(args),
        }).then(r => r.json());
    }
  }
  return api;
};
```

## Gestion de la dette technique {#technical-debt-management}

- Si vous sentez qu'un élément est incorrect mais ne connaissez pas la bonne correction, NE réécrivez PAS encore : apprenez d'abord les bons patterns
- Introduisez les améliorations progressivement, avec chaque nouvelle fonctionnalité
- Écrivez le nouveau code correctement, même si le code environnant est désordonné
- Si vous n'êtes pas le tech lead, il ne vous revient pas de pousser pour un refactoring

## Pièges {#gotchas}

- Fonctionnel vs POO : la plupart des tâches métier doivent utiliser un style procédural ; Angular s'aligne sur GoF/SOLID, React penche vers le fonctionnel
- La sur-ingénierie (DDD strict) est aussi nuisible que la sous-ingénierie (objets Dieu) : le juste milieu est un schéma déclaratif et des patterns universels
- La configuration ESLint partagée (un dépôt unique pour les règles communes à tous les dépôts du projet) prévient la dérive stylistique

## Voir aussi {#see-also}

- [[dependency-injection]] - DI vs modules pour découpler les couches
- [[data-access-patterns]] - DAL comme couche d'architecture distincte
- [Design Patterns (GoF) en JavaScript](design-patterns-gof.md) - patterns pour l'isolation des couches (Adapter, Facade, Proxy)
- [[modules-and-packages]] - comment le système de modules soutient l'architecture
