---
title: "Backend Node.js & JavaScript"
type: MOC
level: 3
source_sha256: 6969a856c822a20871790101b6c7e9b8f17a4e46034df8854e1f01d26d0da0c5
translation: machine
translated_at: '2026-10-24'
---
# Backend Node.js & JavaScript {#nodejs-javascript-backend}

## Runtime & internes {#runtime-internals}
- [[event-loop-and-architecture]] - V8, libuv, boucle d'événements, clustering, où Node.js s'inscrit et où il ne s'inscrit pas
- [[v8-optimization]] - Classes cachées, code monomorphe/polymorphe, JIT, inlining de petites fonctions
- [[closures-and-scope]] - Portée lexicale, closures comme structures de données sur le tas, portée des modules

## Programmation asynchrone {#async-programming}
- [[async-patterns]] - Callbacks, Promises, async/await, objets thenable, AbortController
- [[streams]] - Readable/Writable/Transform/Duplex, backpressure, optimisation des buffers
- [Patterns de concurrence](concurrency-patterns.md) - Modèle d'acteurs, CRDT, SharedWorker, protocoles binaires, déploiement

## Langage & système de types {#language-type-system}
- [[modules-and-packages]] - CommonJS vs ESM, interopérabilité, package-lock, npm, cache des modules
- [[solid-and-grasp]] - SOLID/GRASP en JavaScript, types algébriques, enregistrements immuables, LSP
- [Design Patterns (GoF) en JavaScript](design-patterns-gof.md) - Factory, Strategy, Observer, Adapter, Facade, Proxy, Flyweight, State

## Architecture {#architecture}
- [[application-architecture]] - Structure DDD, couches, abstraction du transport, isolation des contextes
- [[data-access-patterns]] - Repository, Active Record, curseurs, transactions, DAL
- [[dependency-injection]] - DI vs système de modules, réduction du couplage, abstraction de la plateforme
- [[middleware-and-http]] - Transport HTTP/WS, middleware comme Chain of Responsibility, multi-framework

## Exploitation {#operations}
- [Gestion des erreurs](error-handling.md) - AppError, AggregateError, Error.cause, fail-fast, types d'erreurs
- [[security-and-sandboxing]] - Crypto, hachage de mots de passe, sandbox vm, macaroons vs JWT
- [Optimisation des performances](performance-optimization.md) - Réduction des allers-retours, Map vs Object, optimisation des buffers, DSL vs impératif
