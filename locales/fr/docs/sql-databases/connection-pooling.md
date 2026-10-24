---
title: "Pooling de connexions"
category: concepts
tags: [sql-databases, connection-pooling, pgbouncer, proxysql, pool-sizing, postgresql, mysql]
level: 4
source_sha256: 250497c67ec869000630c23a5666cb5ab88222fa5e29cfb09c420225e8fce096
translation: machine
translated_at: '2026-10-24'
---
# Pooling de connexions {#connection-pooling}

Chaque connexion à une base de données est coûteuse : handshake TCP, négociation TLS, authentification, puis création d'un processus backend (PostgreSQL) ou allocation d'un thread (MySQL). Le pooling de connexions réutilise des connexions déjà établies entre les requêtes de l'application.

## Pourquoi utiliser un pool {#why-pool}

- PostgreSQL : chaque connexion = un processus système distinct (fork)
- MySQL : chaque connexion = un thread
- Ouvrir et fermer une connexion à chaque requête consomme des ressources et ajoute de la latence
- 10 instances applicatives x 20 connexions chacune = 200 connexions à la base sans pooler externe

## PgBouncer (PostgreSQL) {#pgbouncer-postgresql}

Proxy léger placé entre l'application et PostgreSQL.

### Modes de pooling {#pooling-modes}

| Mode | Comportement | Compatibilité |
|------|--------------|---------------|
| **Session** | Connexion conservée pendant toute la session du client | Complète : toutes les fonctionnalités fonctionnent |
| **Transaction** | Connexion rendue au pool après chaque transaction | Pas de prepared statements, pas de SET au niveau session, pas de LISTEN/NOTIFY |
| **Statement** | Connexion rendue au pool après chaque instruction | Casse les transactions multi-instructions |

Le mode transaction est recommandé pour la plupart des usages en production : c'est le meilleur compromis entre efficacité du pooling et compatibilité.

### Formule de dimensionnement du pool {#pool-sizing-formula}

```toml
connections = (cpu_cores * 2) + effective_spindle_count
```

Pour un SSD avec 4 cœurs : environ 9 à 10 connexions. Plus de connexions n'apporte pas plus de débit (surcoût de commutation de contexte et de contention sur les verrous).

PgBouncer utilise `default_pool_size = 20` par couple utilisateur/base de données.

## ProxySQL (MySQL) {#proxysql-mysql}

Multiplexage de connexions, routage des requêtes, répartition lecture/écriture, mise en cache des requêtes. Le jeu de fonctionnalités est plus riche que l'équivalent PgBouncer dans l'écosystème MySQL.

## Pooling au niveau applicatif {#application-level-pooling}

```javascript
// Node.js with pg (node-postgres)
const { Pool } = require('pg');
const pool = new Pool({
  connectionString: 'postgresql://user:pass@host:5432/db',
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000
});

// Transaction pattern
const client = await pool.connect();
try {
  await client.query('BEGIN');
  await client.query('INSERT INTO orders ...');
  await client.query('UPDATE inventory ...');
  await client.query('COMMIT');
} catch (e) {
  await client.query('ROLLBACK');
  throw e;
} finally {
  client.release();
}
```

## Points clés {#key-facts}

- PgBouncer est mono-thread (utiliser plusieurs instances pour un débit élevé)
- Odyssey (Yandex) est une alternative multi-thread à PgBouncer
- pgcat est un pooler plus récent écrit en Rust, avec support du sharding
- Pool de connexions trop petit : les requêtes attendent qu'une connexion se libère
- Pool de connexions trop grand : base de données surchargée, surcoût de commutation de contexte

## Pièges {#gotchas}

- **Prepared statements** cassés dans PgBouncer en mode transaction (la connexion est réutilisée, le prepared statement a disparu)
- **Commandes SET** perdues lorsque la connexion est rendue au pool (les paramètres de session sont réinitialisés)
- **Verrous consultatifs de session** libérés lorsque PgBouncer réattribue la connexion en mode transaction
- **Transactions longues** qui monopolisent les connexions et privent les autres requêtes
- **Fuites de connexions** dues à l'oubli de rendre les connexions au pool
- **LISTEN/NOTIFY** nécessite un pooling en mode session (connexion persistante)

## Voir aussi {#see-also}

- [[postgresql-configuration-tuning]] - réglage de max_connections
- [[postgresql-ha-patroni]] - HAProxy pour le routage des connexions
- [[transactions-and-acid]] - comportement des transactions avec les poolers
- [[concurrency-and-locking]] - comportement des verrous entre connexions poolées
