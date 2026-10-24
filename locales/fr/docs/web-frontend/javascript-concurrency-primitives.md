---
title: "Primitives de concurrence JavaScript et Workers"
category: concepts
tags: [javascript, concurrency, semaphore, mutex, worker-threads, design-patterns]
level: 3
source_sha256: 3a43d9f64ac3e15a0b958bd15d7e0b1e807f56a708dfa76f7c45b947dbf9b18f
translation: machine
translated_at: '2026-10-24'
---
# Primitives de concurrence JavaScript et Workers {#javascript-concurrency-primitives-and-workers}

Coordination asynchrone avancée en JavaScript - sémaphores, mutex, files et pools asynchrones, worker threads, et patrons GoF appliqués au code asynchrone. Couvre à la fois les API Node.js et navigateur.

## Points clés {#key-facts}

- Node.js est mono-thread pour l'exécution JS mais prend en charge les Worker Threads (de véritables threads OS)
- `SharedArrayBuffer` + `Atomics` permettent une mémoire partagée entre workers
- Un sémaphore limite les opérations concurrentes ; un Mutex est un sémaphore binaire pour l'accès exclusif
- `MessageChannel` crée des paires de ports connectés ; `BroadcastChannel` est de type un-vers-plusieurs
- Le module cluster crée des copies du processus principal par fork pour l'équilibrage de charge via round-robin du système d'exploitation

## Patrons {#patterns}

### Sémaphore {#semaphore}

Limite les opérations concurrentes à N :

```js
class Semaphore {
  constructor(count) { this.count = count; this.queue = []; }
  async acquire() {
    if (this.count > 0) { this.count--; return; }
    await new Promise(resolve => this.queue.push(resolve));
  }
  release() {
    this.count++;
    if (this.queue.length) { this.count--; this.queue.shift()(); }
  }
}
```

### AsyncQueue {#asyncqueue}

Producteur/consommateur avec backpressure et contrôle de la concurrence. Essentiel pour les pools de workers et la limitation de débit. Stratégies d'implémentation : tampon circulaire (favorable au cache), liste déroulée (moindre pression sur le GC).

### AsyncPool {#asyncpool}

Gère un pool de ressources coûteuses (connexions à une base de données, worker threads). Le patron Factory Method crée les instances. Le patron Pool réutilise les instances existantes et met en file d'attente les requêtes lorsque le pool est épuisé.

### AsyncCollector {#asynccollector}

Rassemble les résultats asynchrones jusqu'à ce que tous soient prêts. Contrairement à `Promise.all`, prend en charge l'ajout dynamique de sources et des stratégies de timeout partiel.

### Worker Threads vs Child Processes {#worker-threads-vs-child-processes}

**Worker Threads** (`worker_threads`) : de véritables threads OS partageant la même mémoire de processus. Communiquent via `postMessage()` ou `SharedArrayBuffer`. À utiliser pour les tâches intensives en CPU (traitement d'images, compression, inférence ML).

**Child Processes** (`child_process`) : processus séparés, sans mémoire partagée. À utiliser pour l'isolation, des runtimes différents, les outils en ligne de commande.

**SharedArrayBuffer + Atomics** : `Atomics.add/sub/load/store/exchange` sont atomiques. `Atomics.wait/notify` pour la synchronisation.

**SpinLock** : boucle d'attente active utilisant `Atomics.wait()/notify()` sur un SharedArrayBuffer. Uniquement pour les Worker Threads, avec des sections critiques très courtes.

### Patrons GoF pour le JS asynchrone {#gof-patterns-for-async-js}

**Adapter (asyncify/callbackify)** :
```js
util.promisify(cbFn)       // callback-based -> Promise
util.callbackify(asyncFn)  // async -> callback-last-error-first
```

**Chain of Responsibility** : évitez le style Express `(req, res, next)` - la propagation des erreurs y est fragile. Privilégiez les chaînes explicites : `compose(fn1, fn2, fn3)(value)`.

**Observer/EventEmitter** : `EventEmitter` (Node.js), `EventTarget` (navigateur + Node 14+). `EventTarget` prend en charge `{once: true}` et l'annulation via `AbortSignal`.

**Revealing Constructor** : utilisé dans les Promises et les streams - l'executor reçoit des capacités privées (resolve/reject ou push/done), les consommateurs obtiennent une interface restreinte.

### SOLID et GRASP pour JS {#solid-and-grasp-for-js}

**SOLID** : Responsabilité unique, Ouvert/Fermé (privilégier la composition à l'héritage), Substitution de Liskov, Ségrégation des interfaces, Inversion des dépendances.

**GRASP** : Expert en information, Créateur, Contrôleur, Forte cohésion / Faible couplage.

**Programmation par contrat** : spécifiez les préconditions, postconditions et invariants. Validez en mode debug, omettez en production.

### Gestion des erreurs {#error-handling}

**Erreurs opérationnelles** (timeout réseau, entrée invalide) - attendues, récupérables, à traiter explicitement.
**Erreurs de programmation** (TypeError, ReferenceError) - bugs, non récupérables, laissez le programme planter et redémarrer.

```js
// Graceful shutdown
process.on('SIGTERM', async () => {
  server.close(() => { process.exit(0); });
});
process.on('uncaughtException', (err) => {
  logger.fatal(err);
  process.exit(1); // must exit - state is unknown
});
```

## Pièges {#gotchas}

- Envoyer sur un canal fermé en Go provoque une panique ; en JS, l'équivalent - écrire dans un stream terminé lève une exception
- `BroadcastChannel` est de type un-vers-plusieurs uniquement au sein d'un même processus/origine, pas entre processus
- Un SpinLock avec `Atomics.wait` ne fonctionne que dans les Worker Threads, pas dans le thread principal (le navigateur le bloque)
- Le patron de middleware Express a une propagation des erreurs fragile - privilégiez la composition explicite

## Voir aussi {#see-also}

- [[javascript-async-event-loop]] - boucle d'événements, promises, streams, générateurs
- [[go/concurrency-patterns]] - goroutines, canaux, primitives de synchronisation
