---
title: "Patrons de concurrence"
category: patterns
tags: [nodejs, actor-model, crdt, blockchain, webrtc, shared-worker, concurrency]
level: 3
source_sha256: 1d3fffcf541f71f424e6b8f5fabddbdfe1f6af233391b2fe8793940f8cb610f4
translation: machine
translated_at: '2026-10-24'
---
# Patrons de concurrence {#concurrency-patterns}

La concurrence dans Node.js dépasse async/await avec le modèle Actor, les CRDT pour l'état distribué, les SharedWorker pour la coordination entre onglets du navigateur, et des protocoles personnalisés pour les applications temps réel. Ces patrons répondent à la coordination entre contextes d'exécution indépendants.

## Modèle Actor (monothread) {#actor-model-single-threaded}

Selon Alan Kay, toute la POO était censée ressembler au patron Actor : état isolé, communication par messages.

```js
class Actor {
  #queue = [];
  #processing = false;

  send(message) {
    this.#queue.push(message);
    if (!this.#processing) this.#process();
  }

  async #process() {
    this.#processing = true;
    while (this.#queue.length > 0) {
      const msg = this.#queue.shift();
      await this.handle(msg);
    }
    this.#processing = false;
  }
}
```

La version monothread utilise une file asynchrone à la place de `process.send()` / `MessagePort`. La même API fonctionne en monothread, multithread et multiprocessus, en changeant simplement le transport des messages.

**Patron Reactor** : modèle de boucle d'événements pour le multitâche coopératif au sein d'un seul thread, fondement de Node.js.

## CRDT (Conflict-free Replicated Data Types) {#crdt-conflict-free-replicated-data-types}

### Méthodes de synchronisation {#synchronization-methods}

- **À base d'état :** l'état complet est envoyé (charges utiles plus volumineuses, mais plus simple)
- **À base d'opérations :** seules les opérations sont transmises (charges utiles plus petites, mais plus complexe)
- **À base de deltas :** seuls les changements sont transmis (le plus efficace pour le réseau)

### Structures de données disponibles {#available-data-structures}

- G-Counter (croissance seule), PN-Counter (positif-négatif)
- G-Set (croissance seule), 2P-Set (deux phases), OR-Set (observed-remove)
- Graphes, listes ordonnées, registres

### CRDT piloté par schéma {#schema-driven-crdt}

```js
const schema = {
  likes: { type: 'g-counter' },
  tags: { type: '2p-set' },
  inventory: { type: 'pn-counter' },
};
```

## WebSocket avec SharedWorker {#sharedworker-websocket}

Partager une seule connexion WebSocket entre plusieurs onglets du navigateur :

- 50 onglets ouverts mais une seule connexion WebSocket vers le serveur
- Le Service Worker joue le rôle de courtier de messages entre les onglets
- Tous les onglets synchronisent leur état via le Service Worker
- Économise les ressources serveur et la mémoire côté client

## Protocole binaire personnalisé (Metacom) {#custom-binary-protocol-metacom}

- Format de paquets avec identifiants : positif = client vers serveur, négatif = événements serveur vers client
- Identifiants de flux pour l'envoi et le téléchargement de fichiers multiplexés sur la même connexion
- La sérialisation binaire surpasse JSON en taille et en vitesse
- Version 3 : fonctions de sérialisation fusionnées, allocation d'un buffer unique pour les fragments de flux

### Client d'API dynamique (squelette) {#dynamic-api-client-scaffold}

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

## Patrons de déploiement {#deployment-patterns}

### Déploiement blue-green {#blue-green-deployment}
Deux clusters identiques. On déploie la nouvelle version sur l'un et on bascule le trafic instantanément si nécessaire.

### Canary release {#canary-release}
Une partie des utilisateurs est redirigée vers la nouvelle version. On détecte les problèmes avant le déploiement complet.

### Feature toggles {#feature-toggles}
Activer ou désactiver des fonctionnalités dynamiquement sans redéploiement : indicateurs en ligne de commande, contrôle à distance via un panneau d'administration, interrupteur d'arrêt d'urgence en cas de pic d'erreurs.

## Pièges courants {#gotchas}

- Un Actor monothread en JS doit tout de même gérer les situations de concurrence dans le gestionnaire de messages (plusieurs `await` peuvent s'entrelacer)
- Un CRDT converge à terme mais peut afficher des données obsolètes temporairement : il ne convient pas aux exigences de cohérence forte
- SharedWorker n'est pas disponible dans tous les navigateurs : vérifier la compatibilité

## Voir aussi {#see-also}

- [[async-patterns]] - async/await, EventEmitter comme primitives de concurrence
- [[event-loop-and-architecture]] - modèle d'exécution monothread
- [[data-access-patterns]] - transactions comme patron d'accès sérialisé
- [[streams]] - concurrence du traitement de données par flux
