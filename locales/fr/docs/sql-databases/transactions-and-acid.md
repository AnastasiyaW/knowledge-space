---
title: "Transactions et propriétés ACID"
category: concepts
tags: [sql-databases, transaction, acid, isolation-level, read-committed, repeatable-read, serializable, snapshot-isolation]
level: 4
source_sha256: d2f8001ee8f2f502fd4f8c3c6b01d9953ef64241937ec843d2bcc4d37e73cc22
translation: machine
translated_at: '2026-10-24'
---
# Transactions et propriétés ACID {#transactions-and-acid-properties}

Les transactions regroupent plusieurs requêtes en une unité de travail atomique. Les propriétés ACID (Atomicité, Cohérence, Isolation, Durabilité) garantissent un traitement fiable des données, même en cas d'accès concurrents et de défaillances système.

## Cycle de vie d'une transaction {#transaction-lifecycle}

```sql
BEGIN;
SELECT balance FROM accounts WHERE id = 1;  -- verify >= 100
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
-- Or ROLLBACK; to undo all changes
```

Les transactions en lecture seule sont valides : elles servent à obtenir des instantanés cohérents (rapports).

## Propriétés ACID {#acid-properties}

**Atomicité :** Toutes les requêtes réussissent, ou toutes sont annulées (rollback). Un crash entre les deux UPDATE ci-dessus déclenche un rollback automatique à la reprise : aucun état partiel ne subsiste.

**Cohérence :** Deux dimensions : (1) cohérence des données : intégrité référentielle, contraintes CHECK, contraintes UNIQUE ; (2) cohérence de lecture : la lecture suivante voit-elle les données qui viennent d'être validées (le C du théorème CAP) ?

**Isolation :** Contrôle la visibilité des modifications effectuées par les transactions concurrentes. Voir les niveaux d'isolation ci-dessous.

**Durabilité :** Les modifications validées survivent aux crashs. Elle est assurée par le WAL (write-ahead log). `fsync()` force l'écriture physique sur disque, mais cette opération est coûteuse. `synchronous_commit = off` dans PostgreSQL échange le risque de durabilité (fenêtre d'environ 600 ms) contre des commits 3 fois plus rapides.

## Phénomènes de lecture {#read-phenomena}

| Phénomène | Description |
|-----------|-------------|
| Dirty Read | Lecture de données non validées d'une autre transaction |
| Non-Repeatable Read | Une même ligne renvoie des valeurs différentes entre deux lectures dans une même transaction |
| Phantom Read | La réexécution d'une requête par plage renvoie de nouvelles lignes insérées par une autre transaction |
| Lost Update | Deux transactions lisent la même ligne, la mettent toutes deux à jour, et la seconde écrase la première |

## Niveaux d'isolation {#isolation-levels}

| Niveau | Dirty Read | Non-Repeatable | Phantom | Lost Update |
|--------|-----------|----------------|---------|-------------|
| Read Uncommitted | Oui | Oui | Oui | Oui |
| Read Committed | Non | Oui | Oui | Oui |
| Repeatable Read | Non | Non | Oui* | Non |
| Serializable | Non | Non | Non | Non |

*PostgreSQL implémente Repeatable Read sous forme de Snapshot Isolation, ce qui empêche aussi les phantoms. MySQL InnoDB utilise des verrous next-key au niveau RR.

**Read Committed** (valeur par défaut dans PostgreSQL et Oracle) : chaque instruction ne voit que les données validées avant son démarrage. C'est la valeur par défaut pour la plupart des usages en production.

**Repeatable Read :** la transaction voit l'instantané pris au début de celle-ci. PostgreSQL = snapshot isolation (optimiste, détection des conflits au moment du commit). MySQL = verrouillage next-key (pessimiste, prévention des conflits par des verrous).

**Serializable :** les transactions s'exécutent comme si elles étaient sérialisées. PostgreSQL utilise SSI (Serializable Snapshot Isolation) : exécution concurrente avec suivi des dépendances, avec annulation en cas d'anomalie.

```sql
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
-- Or globally:
ALTER DATABASE mydb SET DEFAULT_TRANSACTION_ISOLATION TO 'read committed';
```

## Approches d'implémentation {#implementation-approaches}

**Pessimiste (verrouillage) :** verrouiller les lignes ou les pages avant toute modification. Bloquer en cas de conflit. `SELECT FOR UPDATE` est un serializable pessimiste. Convient mieux aux charges à forte contention.

**Optimiste (MVCC) :** aucun verrou pendant l'exécution. Suivre les modifications et échouer en cas de conflit au moment du commit. Convient mieux aux charges à faible contention et majoritairement en lecture.

## Points clés {#key-facts}

- PostgreSQL : RR = Snapshot Isolation (pas de lectures fantômes, contrairement à MySQL)
- PostgreSQL ne prend pas en charge READ UNCOMMITTED (traité comme Read Committed)
- Le niveau par défaut de MySQL InnoDB est REPEATABLE READ avec des gap locks
- `SELECT FOR UPDATE` acquiert un verrou exclusif sur la ligne jusqu'à la fin de la transaction
- Les transactions longues conservent les connexions et les verrous : configurer `idle_in_transaction_session_timeout`

### Motif de réservation de lignes (workers concurrents) {#claiming-rows-pattern-concurrent-workers}

Plusieurs workers réservent des tâches sans conflit :
```sql
-- Atomically claim next unclaimed row
UPDATE tasks
SET status = 'processing', worker_id = :my_id, claimed_at = NOW()
WHERE id = (
    SELECT id FROM tasks
    WHERE status = 'pending'
    ORDER BY priority DESC, created_at ASC
    LIMIT 1
    FOR UPDATE SKIP LOCKED  -- skip rows locked by other workers
)
RETURNING *;
```
`SKIP LOCKED` (PostgreSQL 9.5+, MySQL 8.0+) : le worker ignore les lignes verrouillées au lieu d'attendre, ce qui permet une véritable file de travail parallèle.

### Verrous consultatifs (verrouillage au niveau applicatif) {#advisory-locks-application-level-locking}

```sql
-- PostgreSQL: application-level named locks (not tied to rows)
SELECT pg_advisory_lock(12345);     -- blocks until acquired
-- ... critical section ...
SELECT pg_advisory_unlock(12345);

-- Try without blocking:
SELECT pg_try_advisory_lock(12345); -- returns true/false immediately

-- Session-level: released on disconnect
-- Transaction-level: released on COMMIT/ROLLBACK
SELECT pg_advisory_xact_lock(12345);
```
Cas d'usage : empêcher l'exécution en double d'une tâche cron, coordonner l'accès à une ressource externe.

### Points de sauvegarde (rollback partiel) {#savepoints-partial-rollback}

```sql
BEGIN;
INSERT INTO orders (user_id, amount) VALUES (1, 100);

SAVEPOINT sp1;
INSERT INTO order_items (order_id, product_id) VALUES (1, 999);  -- might fail
-- If this fails:
ROLLBACK TO SAVEPOINT sp1;
-- order INSERT is preserved, only order_items rolled back

INSERT INTO order_items (order_id, product_id) VALUES (1, 42);  -- retry
COMMIT;  -- commits order + corrected order_items
```

## Pièges à éviter {#gotchas}

- Serializable ne sérialise pas littéralement les transactions : il s'appuie sur le suivi des dépendances (SSI dans PG)
- `SELECT FOR UPDATE` en pooling au niveau transaction (PgBouncer) peut provoquer une libération inattendue des verrous
- Deux transactions qui exécutent chacune `SELECT FOR SHARE` puis UPDATE sur la même ligne provoquent un deadlock
- Des lost updates restent possibles même en Read Committed : utiliser `SELECT FOR UPDATE` ou un niveau d'isolation plus élevé
- `SKIP LOCKED` ignore silencieusement les lignes : si toutes les lignes sont verrouillées, le résultat est vide (ce n'est pas une erreur)
- Les verrous consultatifs ne sont PAS libérés automatiquement à la fin de la transaction (variante au niveau session) : toujours les libérer explicitement, ou utiliser `pg_advisory_xact_lock`
- Les points de sauvegarde en mode `autocommit` n'ont aucun effet : les utiliser uniquement à l'intérieur d'un `BEGIN` explicite
- Les transactions longues en MVCC maintiennent en vie d'anciennes versions de lignes, ce qui empêche VACUUM : configurer `idle_in_transaction_session_timeout`

## Voir aussi {#see-also}

- [[concurrency-and-locking]] - types de verrous, deadlocks, verrous consultatifs
- [[postgresql-wal-durability]] - WAL et compromis de durabilité
- [[postgresql-mvcc-vacuum]] - détails de l'implémentation MVCC
- [[connection-pooling]] - modes de pooling et comportement transactionnel
