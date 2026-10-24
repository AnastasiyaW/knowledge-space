---
title: "Patrons asynchrones"
category: concepts
tags: [nodejs, async, promises, callbacks, await, thenable, abort-controller]
level: 3
source_sha256: 1b5aac4ff44971ffc20907dad6d799972b0bcf171b43b5538c6621d92f54340a
translation: machine
translated_at: '2026-10-24'
---
# Patrons asynchrones {#async-patterns}

Le modèle de programmation asynchrone de JavaScript couvre les callbacks, les Promises, async/await, EventEmitter et les streams. Chaque patron a des cas d'usage spécifiques, des caractéristiques de performance et des mécanismes d'interopérabilité. La progression des callbacks vers async/await représente une abstraction croissante, et non une obsolescence : tous les patrons coexistent.

## Points clés {#key-facts}

- **Callback-last** : le callback est toujours le dernier argument
- **Error-first** : le premier argument du callback est l'erreur (ou `null`), suivi des données
- Le mot-clé `async` fait retourner une Promise à une fonction ; `await` en extrait la valeur
- `Promise.withResolvers()` a été conçu pour les cas où `resolve` et `reject` doivent sortir de la portée du constructeur, ce qui est plus efficace dans V8 qu'un stockage manuel
- Les objets thenables (objets disposant d'une méthode `.then()`) sont nettement plus rapides que les Promises complètes et entièrement compatibles avec `await`
- Les Promises annulables sont désormais intégrées via `AbortController` (auparavant, une implémentation personnalisée était nécessaire)
- L'implémentation des Promises dépend en partie de l'environnement hôte (Node.js ou navigateur), et pas uniquement de V8

## Priorité des patrons asynchrones {#priority-of-async-patterns}

**Connaissances indispensables :**
- Callbacks (callback-last, error-first)
- Promises (then/catch/finally)
- async/await
- EventEmitter / EventTarget
- Streams (Readable, Writable, Transform, Duplex)

**Avancé / programmation système :**
- Objets thenables, AsyncIterator/AsyncGenerator
- Worker threads, MessagePort, SharedArrayBuffer
- Atomics, Mutex, Semaphore, modèle Actor

**Héritage (peut être ignoré) :** la bibliothèque Async.js, les générateurs utilisés comme contrôle de flux asynchrone, Domain (obsolète)

## Patrons {#patterns}

### Adaptateurs Promisify / Callbackify {#promisify-callbackify-adapters}

```js
// Promisify: callback-last → Promise
const promisify = (fn) => (...args) =>
  new Promise((resolve, reject) =>
    fn(...args, (err, data) => err ? reject(err) : resolve(data))
  );

// Callbackify: Promise → callback-last
const callbackify = (fn) => (...args) => {
  const callback = args.pop();
  fn(...args)
    .then((data) => callback(null, data))
    .catch((err) => callback(err));
};
```

### Objets thenables (alternative légère aux Promises) {#thenable-objects-lightweight-promise-alternative}

```js
// Thenable - lightweight, V8-optimized
const thenable = {
  then(resolve) { resolve(42); }
};

const result = await thenable; // 42

// Works everywhere Promises are accepted per spec
// Created at V8 level with full optimizations
// Significantly faster than full Promises
```

### EventEmitter captureRejections {#eventemitter-capturerejections}

```js
const { EventEmitter } = require('events');

const ee = new EventEmitter({ captureRejections: true });
ee.on('event', async () => {
  throw new Error('async error'); // caught automatically
});
ee[Symbol.for('nodejs.rejection')] = (err) => console.error(err);
// Not available in browser's EventTarget
```

### Regroupement des messages WebSocket {#websocket-data-batching}

Problème : plus de 2000 abonnements temps réel à des instruments provoquent un blocage côté client lorsque les messages arrivent individuellement.

```js
class BatchedSender {
  #buffer = [];
  #interval;

  constructor(ws, intervalMs = 100) {
    this.#interval = setInterval(() => {
      if (this.#buffer.length > 0) {
        ws.send(JSON.stringify(this.#buffer));
        this.#buffer = [];
      }
    }, intervalMs);
  }

  send(data) { this.#buffer.push(data); }
}
```

Solutions : regrouper par fenêtre temporelle, combiner les mises à jour, implémenter une contre-pression (backpressure), utiliser des protocoles binaires pour les données à haute fréquence.

## Pièges à éviter {#gotchas}

- Retourner des erreurs à la manière de Go, sous la forme `{ error, data }`, est un anti-patron en JS : cela régresse vers le style de l'ère des callbacks, impose des vérifications `if (error)` après chaque appel et dégrade les traces de pile asynchrones
- Des situations de concurrence (race conditions) existent dans Node.js mono-thread : plusieurs opérations asynchrones modifiant un état partagé peuvent s'entrelacer
- `await` dans une boucle sérialise les opérations ; utilisez `Promise.all()` pour une exécution concurrente

## Voir aussi {#see-also}

- [[streams]] - Readable, Writable, Transform, Duplex avec contre-pression
- [Gestion des erreurs](error-handling.md) - AppError, AggregateError, patrons fail-fast
- [Patrons de conception (GoF) en JavaScript](design-patterns-gof.md) - EventEmitter comme patron de communication asynchrone
- [[event-loop-and-architecture]] - comment la boucle d'événements traite les callbacks asynchrones
