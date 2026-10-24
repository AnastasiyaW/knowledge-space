---
title: "Flux"
category: concepts
tags: [nodejs, streams, readable, writable, transform, duplex, backpressure]
level: 3
source_sha256: 0dabfc9d2aac717b71a96cbc7a1e75e0d86cc9f424d6bdf3f41036aba75a49c9
translation: machine
translated_at: '2026-10-24'
---
# Flux {#streams}

Les flux (streams) de Node.js fournissent une interface pour travailler avec des données qui arrivent ou sont consommées de manière incrémentale. Plutôt que de charger des jeux de données entiers en mémoire, les flux traitent les données par morceaux (chunks), ce qui permet de gérer des fichiers et des données réseau plus volumineux que la RAM disponible.

## Points clés {#key-facts}

- **Readable** - source de données (lecture de fichier, corps d'une requête HTTP)
- **Writable** - destination de données (écriture de fichier, réponse HTTP)
- **Transform** - lit et écrit, en modifiant les données au passage (compression, chiffrement)
- **Duplex** - à la fois readable et writable, de façon indépendante (WebSocket, socket TCP)
- Les flux implémentent le backpressure automatiquement : lorsqu'un writable est plus lent qu'un readable, le readable se met en pause
- Lorsqu'une socket est mise en pause, le noyau du système d'exploitation met en tampon les données entrantes - la boucle d'événements du thread principal continue de traiter les autres événements

## Patrons {#patterns}

### Flux de backpressure {#stream-backpressure-flow}

1. Le readable envoie des données plus vite que le writable ne peut les consommer
2. Le tampon interne se remplit
3. Le readable se met automatiquement en pause (signal de backpressure)
4. Lorsque le writable vide le tampon, le readable reprend

### Découpage optimisé en morceaux {#optimized-chunk-streaming}

```js
// Optimized: single buffer allocation for streaming over WebSocket
const sendChunk = (streamId, data) => {
  const packet = Buffer.allocUnsafe(8 + data.length);
  packet.writeInt32BE(streamId, 0);
  packet.writeInt32BE(data.length, 4);
  data.copy(packet, 8);
  return packet;
};

// Before optimization: two typed arrays, copied into one
// const header = new Uint8Array(8);
// const body = new Uint8Array(data);
// const packet = Buffer.concat([header, body]); // 2 allocations
```

### Motif curseur (flux en mémoire) {#cursor-pattern-stream-like-in-memory}

```js
class Cursor {
  constructor(data) { this.data = data; }

  select(fields) {
    return new Cursor(this.data.map(row =>
      fields.reduce((obj, f) => ({ ...obj, [f]: row[f] }), {})
    ));
  }

  order(field) {
    return new Cursor([...this.data].sort((a, b) =>
      a[field] > b[field] ? 1 : -1
    ));
  }

  union(other) {
    return new Cursor([...this.data, ...other.data]);
  }

  intersect(other) {
    const keys = new Set(other.data.map(r => JSON.stringify(r)));
    return new Cursor(this.data.filter(r => keys.has(JSON.stringify(r))));
  }

  fetch() { return this.data; }
}

// Chaining mimics SQL:
// cursor.select(['name', 'age']).order('name').fetch()
```

Avancé : implémenter `Symbol.iterator` pour `for...of`, `Symbol.asyncIterator` pour l'itération asynchrone, et l'interface de flux pour `.pipe()`.

## Pièges {#gotchas}

- `Buffer.allocUnsafe()` est plus rapide mais contient de la mémoire non initialisée - écrivez toujours tous les octets avant l'envoi
- Comprendre le backpressure exige de connaître à la fois les mécanismes internes de Node.js et le réseau au niveau du système d'exploitation (tampons du noyau)
- Diffuser des morceaux de fichiers via WebSocket nécessite des identifiants pour multiplexer plusieurs flux sur la même connexion

## Voir aussi {#see-also}

- [[async-patterns]] - itérateurs asynchrones et générateurs comme alternatives aux flux
- [Performance Optimization](performance-optimization.md) - techniques d'optimisation des tampons
- [[event-loop-and-architecture]] - fonctionnement de libuv pour les E/S dans le pool de threads
