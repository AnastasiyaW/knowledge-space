---
title: "Boucle d'événements et architecture"
category: concepts
tags: [nodejs, event-loop, v8, libuv, architecture, runtime]
level: 3
source_sha256: e49c9d4b1b18b13f3e2d298de92af4e230df1dbb786a4c7aa53b316f6641ed08
translation: machine
translated_at: '2026-10-24'
---
# Boucle d'événements et architecture {#event-loop-and-architecture}

Node.js est un environnement d'exécution JavaScript destiné aux applications côté serveur, reposant sur trois piliers : V8 (moteur JavaScript), libuv (E/S asynchrones avec boucle d'événements et pool de threads) et la bibliothèque standard (fs, http, crypto, etc.). La boucle d'événements est le mécanisme central qui permet les E/S non bloquantes dans un environnement mono-thread.

## Points clés {#key-facts}

- V8 est le moteur JavaScript, mais Node.js pourrait théoriquement utiliser un autre moteur
- libuv fournit la boucle d'événements, le pool de threads pour les opérations sur fichiers et réseau, ainsi que des E/S asynchrones multiplateformes
- Node.js est mono-thread pour l'exécution du JavaScript, mais utilise le pool de threads pour les E/S bloquantes
- Rôle principal : serveur applicatif, serveur réseau ou orchestrateur de services
- PAS idéal pour : le calcul intensif en CPU (utiliser des Worker Threads ou des addons natifs), les systèmes temps réel stricts, ou les systèmes nécessitant une mémoire partagée entre threads (utiliser Go, Rust, C++)
- Les performances dépendent entièrement de la qualité du code applicatif - **il faut mesurer, on ne peut pas estimer**

## Mécanique de la boucle d'événements {#event-loop-mechanics}

1. Le code applicatif appelle une fonction de la bibliothèque standard (par exemple `fs.readFile`)
2. La bibliothèque standard peut utiliser le pool de threads de libuv pour les opérations d'E/S
3. Lorsque l'opération se termine, le callback est placé dans la file des callbacks
4. La boucle d'événements lit en continu la file des callbacks
5. Chaque callback est empilé sur la pile d'appels et exécuté dans V8
6. Lorsque la file des callbacks est vide ET qu'aucune opération en attente ne subsiste, le processus Node.js se termine

## Facteurs de performance {#performance-factors}

- Patterns asynchrones utilisés (callbacks vs Promises vs async/await)
- Opérations liées au CPU (boucles longues, JOIN en mémoire)
- Utilisation appropriée des structures de données JS (Map vs Object pour les grandes collections)
- Qualité des dépendances npm
- Efficacité des requêtes de base de données
- Gestion de la mémoire (pooling des buffers, prévention des fuites)

## Patterns {#patterns}

### Arrêt gracieux {#graceful-shutdown}

```js
const server = http.createServer(app);

process.on('SIGTERM', async () => {
  // 1. Stop accepting new connections
  server.close();
  // 2. Wait for in-flight requests to complete
  await drainConnections();
  // 3. Close database connections
  await db.end();
  // 4. Flush logs
  await logger.flush();
  // 5. Exit
  process.exit(0);
});
```

### Structure applicative - serveur DDD {#application-structure-ddd-server}

```javascript
project/
  schemas/         # Domain schemas (JSON Schema / metaschema)
    auth.schema
    messenger.schema
  db/              # Database creation scripts (NOT ORM)
    create.sql
  api/             # API layer
    auth/
    messenger/
  domain/          # Business logic (pure functions)
  transport/       # HTTP and WebSocket handlers
  config.js        # Centralized configuration
  main.js          # Entry point
```

La structure applicative est la principale difficulté du développement Node.js - non pas les frameworks, les patterns asynchrones ou les mécanismes internes, mais le découpage du code en couches et la gestion du couplage entre abstractions.

## Pièges courants {#gotchas}

- Bien que mono-thread, Node.js PEUT connaître des conditions de course : plusieurs opérations asynchrones modifiant un état partagé peuvent s'entrelacer (par exemple, deux requêtes vérifiant un solde, trouvant toutes deux des fonds suffisants, et débitant chacune le compte)
- `process.exit()` sans arrêt gracieux peut perdre les requêtes en cours de traitement et corrompre les données
- Les Worker Threads partagent la mémoire via SharedArrayBuffer mais nécessitent Atomics pour la synchronisation

## Voir aussi {#see-also}

- [[v8-optimization]] - classes cachées de V8, code monomorphe, compilation JIT
- [[async-patterns]] - callbacks, Promises, mécanique de async/await
- [[streams]] - types de streams et gestion du backpressure
- [Optimisation des performances](performance-optimization.md) - réduction des allers-retours, benchmarks Map vs Object
