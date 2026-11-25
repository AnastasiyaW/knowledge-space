---
title: "Modèles de mise en tampon des écritures"
category: reference
tags: [write-buffer, durable-objects, d1, queues, event-sourcing, offline-first, batch-insert, dirty-flag]
level: 3
source_sha256: 20db2d98bcda5cec989511218257c3dedabb820013881982068e7809c5354545
translation: machine
translated_at: '2026-10-24'
---
# Modèles de mise en tampon des écritures {#write-buffering-patterns}

Modèles de durabilité et de débit pour absorber les écritures à forte fréquence avant un datastore canonique lent ou soumis à une limitation de débit. Couvre le choix du modèle, la coordination à écrivain unique, les tableaux de contraintes et la mécanique concrète de la pile edge.

## Faits clés {#key-facts}

- Latence d'écriture de D1 (SQLite en edge) : **200-300 ms** (routage vers le primaire global, SQLite à écrivain unique) ; latence de lecture P99 d'environ 8 ms. Source : retours d'expérience en production, 2026.
- Benchmark de `.batch()` sur D1 : 5 000 lignes en **14 ms** avec batch contre **78 ms** en séquentiel. Source : étude d'optimisation D1 de rxliuli.com.
- Plafond strict de D1 : **10 Go** par base de données. Planifiez les migrations avant d'approcher cette limite.
- Contrainte de batch D1 : **100 paramètres liés au maximum par instruction** ; avec 10 colonnes, cela fait 10 lignes par instruction, il faut donc découper en conséquence.
- [[caching-and-performance]] présente les définitions de write-through et write-behind au niveau conceptuel ; cet article se concentre sur les mécanismes de durabilité et les primitives de coordination.
- Fenêtre de cohérence éventuelle de Cloudflare KV : **60 s** de propagation globale ; limite de **1 écriture/s** par clé ; lecture de sa propre écriture uniquement au sein d'un même PoP.
- Écriture en mémoire d'un Durable Object (DO) : **< 1 ms** ; environ 500-1 000 req/s par instance pour une logique modérée ; les instances sont colocalisées avec le Worker de routage, dans le même PoP.
- Cloudflare Queues : `max_batch_size` de 1 à 100 (défaut 10), `max_batch_timeout` de 0 à 60 s (défaut 5 s) ; livraison au moins une fois ; 1 M d'opérations par mois incluses, puis 0,40 $/M. Source : [documentation Cloudflare Queues](https://developers.cloudflare.com/queues/configuration/batching-retries/).
- Tarification des DO : 0,15 $/M de requêtes, 50 M de lignes écrites par mois incluses, puis 1,00 $/M. Source : [tarification Cloudflare DO](https://developers.cloudflare.com/durable-objects/platform/pricing/).
- Taille de lot pour la synchronisation offline-first : **50 éléments par segment** est un optimum validé empiriquement, qui équilibre la taille des requêtes et la reprise après échec partiel.

## Catalogue des modèles {#pattern-catalog}

### Write-Through {#write-through}
Chaque écriture atteint à la fois le store rapide (cache/tampon) **et** le datastore canonique de façon synchrone, avant que le client ne reçoive l'ACK.

- **Latence :** l'aller-retour complet vers le datastore est visible par le client (par exemple 200-300 ms pour D1)
- **Durabilité :** forte, aucun flush séparé nécessaire
- **Quand l'utiliser :** écritures à faible volume où la cohérence compte davantage que la vitesse ; registres financiers ; opérations qui doivent être immédiatement lisibles par d'autres services

### Write-Back (Write-Behind) {#write-back-write-behind}
Le client écrit dans un tampon rapide ; un processus asynchrone vide les entrées accumulées vers le store canonique par lots.

- **Latence pour le client :** inférieure à la milliseconde (écriture dans le tampon uniquement)
- **Risque de durabilité :** perte du tampon entre l'écriture et le flush
- **Bénéfice de fusion (coalescing) :** 100 mises à jour de la même clé = 1 écriture dans le datastore
- **Quand l'utiliser :** écritures d'état utilisateur à forte fréquence (progression, préférences, compteurs) ; état de jeu ; toute charge de travail où la latence de la base par opération est inacceptable
- Atténuation du risque de perte : persister le tampon dans un stockage durable (DO Storage / Redis) dès réception ; la copie en mémoire sert les lectures, la copie durable survit à l'éviction

### Dirty-Flag (modèle du tick de serveur de jeu) {#dirty-flag-game-server-tick-pattern}
Le serveur détient un objet d'état mutable en mémoire. Les champs sont marqués « dirty » à chaque mutation. Un flush périodique (« tick ») n'écrit que les champs modifiés dans le datastore et réinitialise les marqueurs.

- **Granularité :** au niveau du champ, et non de l'opération, ce qui réduit l'amplification d'écriture
- **Résolution des conflits :** le dernier écrit gagne (LWW) selon l'horodatage est la stratégie standard lorsque plusieurs clients peuvent mettre à jour le même champ de façon indépendante
- **Quand l'utiliser :** état d'entité qui change de nombreuses fois entre deux persistances (statut d'apprentissage de mots, position d'une entité de jeu, brouillons de formulaires) ; synchronisation multi-appareils où une seule valeur canonique par champ et par entité est acceptable

```javascript
// Conceptual dirty-flag flush inside a single-writer coordinator
class EntityBuffer {
  state = {};    // { fieldName: { value, ts, dirty } }

  mutate(field, value, ts) {
    const current = this.state[field];
    if (!current || ts > current.ts) {
      this.state[field] = { value, ts, dirty: true };
    }
  }

  dirtyFields() {
    return Object.entries(this.state)
      .filter(([, v]) => v.dirty)
      .map(([k, v]) => ({ field: k, value: v.value, ts: v.ts }));
  }

  markClean() {
    for (const k of Object.keys(this.state)) this.state[k].dirty = false;
  }
}
```

### Batch-Flush {#batch-flush}
Accumuler les écritures dans un tampon (en mémoire ou file durable) et les vider vers le datastore dans un lot transactionnel unique, déclenché par le temps ou par la taille.

- **Déclencheurs possibles :** durée écoulée (alarm/cron), seuil de taille du tampon, signal explicite du client (navigation, fermeture d'onglet, reconnexion)
- **Atomicité :** utiliser le batch ou la transaction au niveau de la base de données, pour qu'un échec partiel ne laisse aucun état à moitié écrit ; les insertions idempotentes (`INSERT OR REPLACE` / `ON CONFLICT DO UPDATE`) protègent contre la redélivrance « au moins une fois »
- **Quand l'utiliser :** toute implémentation de write-back ; consommateur de file qui écrit en base ; micro-lot ETL ; synchronisation à la reconnexion pour les clients hors ligne

```sql
-- LWW upsert: newer timestamp wins, avoids overwriting fresher data
INSERT INTO entity_state (user_id, key, value, updated_at)
VALUES (?, ?, ?, ?)
ON CONFLICT(user_id, key)
DO UPDATE SET
  value      = CASE WHEN excluded.updated_at > entity_state.updated_at
                    THEN excluded.value ELSE entity_state.value END,
  updated_at = MAX(excluded.updated_at, entity_state.updated_at);
```

### Event Sourcing pour l'état utilisateur {#event-sourcing-for-user-state}
Journal d'événements en ajout seul ; l'état courant est dérivé en rejouant ou en compactant le journal. Des snapshots périodiques limitent le coût de rejeu.

- **Chemin d'écriture :** chaque changement d'état est un ajout immuable (par exemple `{userId, event: "saved", wordId, ts}`), jamais une mise à jour sur place
- **Chemin de lecture :** rejouer depuis le dernier snapshot plus les événements suivants, ou interroger une vue matérialisée
- **Fusion via compactage du journal :** « l'utilisateur a enregistré le mot X » puis « l'utilisateur a ignoré le mot X » → le compactage ne conserve que le second ; réduit la taille du datastore canonique
- **Adéquation avec l'offline-first :** le client accumule les événements dans un stockage local (IndexedDB / SQLite) ; il synchronise tout le lot d'événements à la reconnexion ; le serveur fusionne par horodatage
- **Quand l'utiliser :** exigences de piste d'audit ; résolution de conflits multi-appareils où l'historique complet compte ; charges de travail où rejouer les événements est acceptable plutôt que de maintenir une table d'état modifiable
- **Quand ne PAS l'utiliser :** état CRUD simple sans valeur historique ; compteurs à fort volume dont le coût de compactage dépasse le bénéfice

### Files de messages vs coordinateur à écrivain unique {#queues-vs-single-writer-coordinator}

| Dimension | File de messages (ex. CF Queues) | Coordinateur de type DO |
|---|---|---|
| Garantie de livraison | Au moins une fois | Exactement une fois (écrivain unique) |
| ACK client | Envoyer-et-oublier ; aucune garantie de lecture après écriture | ACK synchrone ; le client peut lire ses propres écritures |
| Ordonnancement | FIFO par message au sein de la file ; aucun ordre au niveau de l'entité | Sériel par entité (une instance = une entité) |
| Fusion (coalescing) | Aucune : chaque message est discret | Fusion complète dans un tampon en mémoire |
| Coût pour 750 K écritures/jour | environ 0,50 $/mois (après l'offre gratuite) | environ 3 $/mois (coût des requêtes) |
| Idéal pour | Pipelines à sens unique, analytique, journaux d'audit, livraison au moins une fois acceptable | Écritures interactives, état utilisateur, lecture après écriture requise |

## Mise en tampon à écrivain unique : coordinateur Durable Object {#single-writer-buffering-durable-object-coordinator}

Une instance DO par entité (utilisateur, session, entité de jeu) sérialise toutes les écritures, détient un tampon en mémoire et utilise une alarme planifiée pour vider le tampon vers le datastore canonique.

### Pourquoi l'écrivain unique compte {#why-single-writer-matters}
SQLite et les stores similaires à écrivain unique sérialisent en interne les écritures concurrentes, ce qui crée des files d'attente sous charge. Pré-sérialiser au niveau du coordinateur transforme N écritures concurrentes de clients en un seul lot planifié, ce qui supprime la contention.

### Modèle de flush par alarme {#alarm-flush-pattern}

```javascript
// Cloudflare Durable Object - UserStateBuffer
export class UserStateBuffer extends DurableObject {
  buffer = [];  // in-memory; fast, lost on eviction

  async sync(payload) {
    // Persist to DO Storage first for durability across evictions
    const id = crypto.randomUUID();
    this.ctx.storage.sql.exec(
      'INSERT INTO pending (id, data) VALUES (?, ?)',
      id, JSON.stringify(payload)
    );
    this.buffer.push({ id, ...payload });

    // Schedule flush only if no alarm is already set
    if (!(await this.ctx.storage.getAlarm())) {
      await this.ctx.storage.setAlarm(Date.now() + 30_000); // 30 s window
    }
    return { ok: true };  // client ACK before D1 write
  }

  async alarm() {
    // Drain DO Storage (covers eviction scenario where in-memory buffer was lost)
    const rows = [...this.ctx.storage.sql.exec('SELECT id, data FROM pending').results];
    if (rows.length === 0) return;

    const stmts = rows.flatMap(r => buildD1Statements(JSON.parse(r.data)));
    await this.env.DB.batch(stmts);

    // Remove flushed entries
    const ids = rows.map(r => r.id);
    for (const id of ids) {
      this.ctx.storage.sql.exec('DELETE FROM pending WHERE id = ?', id);
    }
    this.buffer = this.buffer.filter(b => !ids.includes(b.id));

    // Reschedule if new writes arrived during flush
    if (this.buffer.length > 0) {
      await this.ctx.storage.setAlarm(Date.now() + 5_000);
    }
  }
}
```

```javascript
// Worker: route to per-user DO
async function handleSync(request, env) {
  const { userId, ...payload } = await request.json();
  const stub = env.USER_BUFFER.get(env.USER_BUFFER.idFromName(userId));
  return Response.json(await stub.sync(payload));
}
```

```javascript
// Helper: chunk rows respecting D1's 100 bound-parameter limit
function buildD1Statements(payload) {
  const stmts = [];
  if (payload.words) {
    for (const chunk of chunkArray(payload.words, 10)) { // 10 rows × 10 cols = 100 params
      stmts.push(buildUpsert('entity_state', chunk));
    }
  }
  return stmts;
}

function chunkArray(arr, size) {
  const out = [];
  for (let i = 0; i < arr.length; i += size) out.push(arr.slice(i, i + size));
  return out;
}
```

### Portes de sortie et visibilité {#output-gates-and-visibility}
Les écritures dans le stockage d'un DO sans `await` intermédiaire sont automatiquement fusionnées en une seule transaction implicite (fusion d'écritures de Cloudflare). L'ACK client revient avant le commit D1 ; les mises à jour optimistes de l'interface doivent donc être réconciliées à la reconnexion à l'aide des horodatages serveur.

## Tableau des contraintes {#constraints-table}

| Store | Latence d'écriture | Plafond de taille | Fenêtre de cohérence | Limite de débit |
|---|---|---|---|---|
| D1 (SQLite en edge) | 200-300 ms (primaire global) | 10 Go strict | Forte (écrivain unique) | Contention sur les écritures concurrentes |
| DO Storage (SQLite) | < 5 ms (local au PoP) | 1 Go par instance | Forte (locale) | environ 500-1 000 req/s par instance |
| Cloudflare KV | 5-10 ms en écriture | Aucun plafond strict | 60 s de cohérence éventuelle globale | 1 écriture/s par clé |
| Cloudflare Queues | 5-10 ms à l'enqueue | Limites par file | Au moins une fois ; pas de lecture après écriture | 400 msg/s par défaut |
| Redis (auto-hébergé) | < 1 ms | Limitée par la RAM | Configurable (AOF/RDB) | Dépend de l'instance |

## Lot de synchronisation offline-first {#offline-first-sync-batch}

Le client accumule les écritures localement (IndexedDB pour une PWA, SQLite pour le mobile natif) et rejoue le lot à la reconnexion ou lors d'événements de navigation.

```typescript
// Client-side sync trigger
async function syncPendingWrites() {
  const pending = await localDb.getAll('pending_writes'); // IndexedDB
  if (pending.length === 0) return;

  // Chunk to 50 items per request to limit payload and enable partial retry
  for (const chunk of chunkArray(pending, 50)) {
    const res = await fetch('/api/sync', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ client_ts: Date.now(), items: chunk }),
    });
    if (res.ok) {
      const ids = chunk.map(w => w.id);
      await localDb.deleteBatch('pending_writes', ids);
    }
    // On failure: leave chunk in local store, retry on next sync cycle
  }
}

// Trigger points
window.addEventListener('online', syncPendingWrites);
document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'hidden') syncPendingWrites();
});
```

**Résolution des conflits :** le LWW sur `client_ts` suffit pour l'état indépendant par utilisateur (vocabulaire, préférences). Pour les entités collaboratives, privilégier les horloges vectorielles ou les transformations opérationnelles (voir [[distributed-systems-fundamentals]]).

## Pièges {#gotchas}

- **Problème :** le DO est évincé de la mémoire avant le déclenchement de l'alarme ; le tampon en mémoire est perdu, et les écritures sont silencieusement abandonnées. -> **Correction :** toujours écrire dans le DO Storage (SQLite durable) dès réception, et ne garder la copie en mémoire que comme optimisation de lecture. `alarm()` vide le Storage, et non `this.buffer`. Vérification : redémarrer le DO (le laisser inactif pendant 60 s) et confirmer que le Storage contient toujours les lignes en attente.

- **Problème :** KV utilisé comme file d'écriture ; en pic de charge (plus de 1 écriture/s par clé), la limite de débit déclenche des 429 ; la fenêtre de cohérence éventuelle de 60 s rompt les hypothèses de lecture après écriture (le client écrit, lit aussitôt, et obtient une valeur périmée provenant d'un autre PoP). -> **Correction :** ne pas utiliser KV comme file d'écriture modifiable. Utiliser Queues (pipeline à sens unique, sans lecture après écriture) ou DO (sérialisé par entité avec lecture locale immédiate). KV convient à une configuration partagée à gros grain, pas à un état utilisateur modifiable.

- **Problème :** le plafond strict de 10 Go de D1 est atteint sans avertissement ; toutes les écritures commencent à échouer. -> **Correction :** surveiller la métrique `d1_storage_bytes` ; prévoir un sharding ou une migration vers Postgres/Hyperdrive avant d'atteindre environ 8 Go. D1 convient aux applications dont les jeux de données sont bornés ou archivables ; les tables d'état utilisateur à forte croissance nécessitent un chemin de migration défini dès le départ.

- **Problème :** la livraison « au moins une fois » de la file provoque des lignes dupliquées lorsque le consommateur plante en cours de lot. L'idempotence n'est pas implémentée, ce qui produit des doublons fantômes. -> **Correction :** utiliser `INSERT OR REPLACE` / `ON CONFLICT DO UPDATE` sur une clé composite stable `(entity_id, event_ts)`. Ne jamais utiliser un `INSERT` simple pour les écritures issues de la file.

- **Problème :** le batch D1 tronque silencieusement lorsqu'une instruction unique dépasse 100 paramètres liés (par exemple l'insertion en masse de 15 lignes de 10 colonnes = 150 paramètres). Le batch s'exécute pour les autres instructions, mais l'instruction trop grande est abandonnée. -> **Correction :** découper l'entrée à raison de `floor(100 / nombre_de_colonnes)` lignes par instruction avant de construire le batch. Appliquer cette règle dans la fonction utilitaire qui construit les instructions D1, et non au niveau de chaque appel.

## Voir aussi {#see-also}

- [[caching-and-performance]] — définitions conceptuelles de write-through/write-behind ; hiérarchie de cache et stratégies d'invalidation
- [[async-event-apis]] — sémantiques de livraison (au moins une fois, webhooks, scrutation) ; non traité ici
- [[message-broker-patterns]] — compactage de journal Kafka, event sourcing à grande échelle, coordination des groupes de consommateurs
- [[distributed-systems-fundamentals]] — horloges vectorielles, dérive d'horloge du LWW, délai de réplication
- [[database-selection]] — quand migrer de D1/SQLite vers Postgres ou un store distribué
- [[quality-attributes-reliability]] — SLO de durabilité, objectifs de temps de reprise
- [[queueing-theory]] — pourquoi la latence lors des rafales d'écritures est non linéaire ; loi de Little appliquée au dimensionnement des flushes par lot

**Recherche source :**
- [Cloudflare DO : Rules of Durable Objects](https://developers.cloudflare.com/durable-objects/best-practices/rules-of-durable-objects/)
- [Blog Cloudflare : SQLite in every Durable Object](https://blog.cloudflare.com/sqlite-in-durable-objects/)
- [Limites de Cloudflare D1](https://developers.cloudflare.com/d1/platform/limits/)
- [Cloudflare Queues : Batching and Retries](https://developers.cloudflare.com/queues/configuration/batching-retries/)
- [Cloudflare KV : How KV Works](https://developers.cloudflare.com/kv/concepts/how-kv-works/)
- [Microsoft Azure : Event Sourcing Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing)
- [AWS : Database Caching Strategies Using Redis](https://docs.aws.amazon.com/whitepapers/latest/database-caching-strategies-using-redis/caching-patterns.html)
