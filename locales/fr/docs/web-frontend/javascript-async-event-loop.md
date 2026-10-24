---
title: "Patterns asynchrones JavaScript et boucle d'événements"
category: concepts
tags: [javascript, async, promises, event-loop, node-js, streams]
level: 3
source_sha256: 9669c00530aea1d18181e7959d95ed0f0b555d4cda55305412d2ae6ffc8866aa
translation: machine
translated_at: '2026-10-24'
---
# Patterns asynchrones JavaScript et boucle d'événements {#javascript-async-patterns-and-event-loop}

Référence complète de la programmation asynchrone en JavaScript, depuis les callbacks jusqu'à async/await, en passant par les streams et les signals. Couvre les mécanismes internes de la boucle d'événements de V8, les API propres à Node.js et les patterns réactifs modernes.

## Points clés {#key-facts}

- La programmation asynchrone en JavaScript suit une hiérarchie de contrats : callbacks -> promises -> async/await -> events -> streams -> signals -> locks -> iterators
- La boucle d'événements vide la file des microtâches (Promise `.then`, `queueMicrotask`) entre chaque phase
- `process.nextTick` s'exécute avant toute autre microtâche, et avant la phase suivante de la boucle d'événements
- `await` suspend l'exécution de la fonction et rend la main à la boucle d'événements : il ne bloque PAS le thread
- Les rejets non gérés font planter Node.js 15+ par défaut
- La taille par défaut du pool de threads de libuv est de 4 threads (variable d'environnement `UV_THREADPOOL_SIZE` pour la modifier)

## Patterns {#patterns}

### Phases de la boucle d'événements {#event-loop-phases}

La boucle d'événements exécute ses phases séquentiellement à chaque tick :

1. **timers** - callbacks de `setTimeout` et `setInterval`
2. **pending callbacks** - callbacks d'E/S différés de l'itération précédente
3. **idle/prepare** - usage interne
4. **poll** - récupération des nouveaux événements d'E/S ; se bloque ici si aucun timer n'est en attente
5. **check** - callbacks de `setImmediate`
6. **close callbacks** - événements de fermeture des sockets

Entre chaque phase, la file des microtâches est entièrement vidée.

**Reactor pattern** : libuv notifie la boucle d'événements lorsque les E/S sont prêtes (de manière non bloquante).
**Proactor pattern** : basé sur la complétion, l'opération se termine avant la notification.

### Contrat des callbacks {#callback-contract}

```js
// Callback-last, error-first convention
function doAsync(arg, callback) {
  callback(null, result);     // success
  callback(new Error('msg')); // failure
}
```

Règle essentielle : un callback doit être appelé **soit de manière synchrone, soit de manière asynchrone, jamais les deux** (problème de Zalgo). Utilisez `process.nextTick` ou `queueMicrotask` pour forcer l'asynchronisme.

### API Promise {#promise-api}

États d'une Promise : `pending` -> `fulfilled` | `rejected` (immuable une fois réglée).

```js
Promise.all(iterable)         // rejects on first rejection
Promise.allSettled(iterable)  // always resolves with {status, value|reason} array
Promise.race(iterable)        // settles with first settlement (any direction)
Promise.any(iterable)         // resolves with first fulfillment; AggregateError if all reject
Promise.withResolvers()       // returns {promise, resolve, reject} (newer API)
Promise.try(fn)               // wraps sync-or-async, catches sync throws too
```

**Contrat thenable** : tout objet disposant d'une méthode `.then(onFulfilled, onRejected)`. `await` fonctionne avec n'importe quel thenable, et pas seulement avec les Promises natives.

### Streams Node.js {#nodejs-streams}

Quatre types de streams :
- **Readable** - source de données (`read()`, `on('data')`, `for await...of`)
- **Writable** - destination (`write()`, `end()`)
- **Duplex** - à la fois lisible et inscriptible (socket TCP)
- **Transform** - Duplex qui transforme les données (gzip, chiffrement)

**Backpressure** : lorsque le consommateur est plus lent que le producteur, `write()` renvoie `false`, et l'événement `drain` est émis quand il est prêt à reprendre. Géré automatiquement avec `pipe()`.

**Web Streams API** (navigateur + Node 18+) : `ReadableStream`, `WritableStream`, `TransformStream`. Fonctionne nativement avec Response.body de `fetch`.

### Générateurs et itérateurs asynchrones {#generators-and-async-iterators}

```js
function* generator() {
  yield 1;
  yield 2;
  return 3; // done:true
}

// Async generator for paginated APIs, event streams
async function* asyncGen() {
  yield await fetch('/api');
}
for await (const item of asyncGen()) { ... }
```

`for...of` s'appuie sur le protocole d'itération. La syntaxe spread `[...iter]`, la déstructuration et `Array.from()` consomment tous des itérables.

### Signals (état réactif) {#signals-reactive-state}

Primitive réactive moderne (Angular Signals, Solid.js, Preact Signals, proposition TC39) :

- `signal(initialValue)` - conteneur d'état réactif
- `computed(fn)` - valeur dérivée, recalculée paresseusement lorsque ses dépendances changent
- `effect(fn)` - effet de bord relancé lorsque les dépendances changent

Les signals suivent leurs dépendances automatiquement au moment de l'accès. Contrairement à RxJS : propagation synchrone, pas de gestion de souscriptions.

### Annulation avec AbortController {#abortcontroller-cancellation}

```js
const controller = new AbortController();
const { signal } = controller;

fetch(url, { signal })
  .catch(err => {
    if (err.name === 'AbortError') { /* cancelled */ }
  });

setTimeout(() => controller.abort(), 5000);
```

Transmettez `signal` à travers les chaînes asynchrones. Vérifiez `signal.aborted` ou `signal.throwIfAborted()` dans le code asynchrone personnalisé.

### AsyncLocalStorage {#asynclocalstorage}

Équivalent du thread-local-storage pour le code asynchrone :

```js
const als = new AsyncLocalStorage();
als.run({ userId: 123 }, async () => {
  await someAsyncOp();
  als.getStore(); // { userId: 123 } - available in callbacks too
});
```

Utilisez-le pour propager le contexte de requête (traçage, authentification, journalisation) sans faire transiter les paramètres à travers les appels.

## Pièges à éviter {#gotchas}

- Un callback ne doit jamais être appelé à la fois de manière synchrone et asynchrone (problème de Zalgo) : choisissez toujours l'un des deux
- `process.nextTick` peut affamer la boucle d'événements s'il est appelé récursivement
- Le pool de threads de libuv (4 par défaut) est partagé entre les E/S de fichiers, le DNS et la cryptographie ; il peut devenir un goulot d'étranglement
- L'option `Error.cause` (`new Error('context', { cause: originalError })`) est la manière moderne d'encapsuler des erreurs
- L'API Web Locks (`navigator.locks.request(name, fn)`) fonctionne dans le navigateur et sur Node 18+ pour des verrous nommés exclusifs ou partagés
- Patterns hérités à éviter : `function*/yield` pour l'asynchrone, Deferred, Async.js, RxJS pour les cas simples

## Voir aussi {#see-also}

- [[javascript-concurrency-primitives]] - Semaphore, Mutex, AsyncQueue, Worker Threads
- [[go/concurrency-patterns]] - comparaison : goroutines contre modèle à boucle d'événements de JavaScript
