---
title: "Optimisation des performances"
category: operations
tags: [nodejs, performance, benchmarking, map-vs-object, round-trips, buffer-optimization]
level: 5
source_sha256: 4277af90b6c3e9a61ebd4be7d37dd9e8b3be34582bf2ee308f212c5c5f29898f
translation: machine
translated_at: '2026-10-24'
---
# Optimisation des performances {#performance-optimization}

L'optimisation des performances de Node.js repose sur la réduction des allers-retours, le choix de structures de données efficaces, l'optimisation des allocations de buffers et la compréhension des mécanismes internes de V8. La mesure est indispensable : le profil de performance de chaque application est unique.

## Points clés {#key-facts}

- Minimiser les allers-retours est plus important que la vitesse brute
- Le système A traite deux fois plus vite mais nécessite 50 requêtes ; le système B est plus lent mais traite tout en une seule requête : le système B l'emporte souvent
- Même en localhost (sur la même machine), la communication par socket a un coût mesurable
- Map est systématiquement plus rapide qu'Object à partir de 1 M+ d'entrées
- Exécutez les benchmarks séquentiellement (et non en parallèle) pour éviter que la contention sur les ressources ne fausse les résultats
- PostgreSQL peut être configuré pour un cache agressif en mémoire, mais un cache in-process (Map/Object de Node.js) évite même le surcoût inter-processus

## Patterns {#patterns}

### Réduction des allers-retours {#round-trip-reduction}

```javascript
// BAD: 50 separate requests
for (const id of ids) {
  const user = await api.getUser(id);
}

// GOOD: batch request
const users = await api.getUsers(ids);
```

Aucune surcharge de sérialisation/désérialisation par requête, aucune latence réseau, aucune gestion de connexion.

### Optimisation des buffers {#buffer-optimization}

```js
// Before: two allocations
const header = new Uint8Array(8);
const body = new Uint8Array(data);
const packet = Buffer.concat([header, body]);

// After: single allocation
const packet = Buffer.allocUnsafe(8 + data.length);
packet.writeInt32BE(streamId, 0);
packet.writeInt32BE(data.length, 4);
data.copy(packet, 8);
```

### Benchmark Map vs Object {#map-vs-object-benchmarking}

```js
// Benchmark methodology:
// - Separate threads for each test
// - Run GC between tests
// - Generate keys once, reuse
// - Run sequentially, not in parallel

const map = new Map();
const obj = Object.create(null);

// For 1M+ entries: Map wins consistently
// Object has overhead from prototype chain and hidden class management
```

### DSL vs impératif (performance et maintenabilité) {#dsl-vs-imperative-performance-and-maintainability}

```js
// LLM-generated: verbose imperative IndexedDB code
db.createObjectStore('users', { keyPath: 'id', autoIncrement: true });
const usersStore = transaction.objectStore('users');
usersStore.createIndex('name', 'name', { unique: false });
// ... repeated for every entity

// Human-written DSL: declarative, shorter, reusable, with migrations
const schema = {
  users: { keyPath: 'id', autoIncrement: true,
    indexes: { name: {}, email: { unique: true } } },
};
const db = await openDatabase('myApp', schema);
```

Une fonction générique unique gère toutes les entités. Le LLM génère manuellement du code impératif pour chaque store.

## Pièges {#gotchas}

- `Buffer.allocUnsafe()` est plus rapide mais contient de la mémoire non initialisée : remplissez toujours tous les octets
- Les protocoles binaires (de type protobuf) surpassent JSON en taille comme en vitesse pour les données à haute fréquence
- Le pattern Flyweight pour les timers échange 2 instructions CMP supplémentaires (dispatch polymorphe) contre des millions d'allocations évitées : mesurez toujours le compromis

## Voir aussi {#see-also}

- [[v8-optimization]] - classes cachées, code monomorphe, mécanismes internes du JIT
- [[streams]] - optimisation des streams et gestion des chunks
- [Patterns de concurrence](concurrency-patterns.md) - batching WebSocket, protocoles binaires
- [[event-loop-and-architecture]] - facteurs de performance dans Node.js
