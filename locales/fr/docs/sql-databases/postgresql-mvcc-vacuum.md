---
title: "MVCC et VACUUM dans PostgreSQL"
category: concepts
tags: [sql-databases, postgresql, mvcc, vacuum, autovacuum, dead-tuples, hot-update, write-amplification, bloat]
level: 3
source_sha256: e3602ba4c62dbd9f8b1826ca27e9cff1cad15d41a6a41b121f4aa1233ffc59b3
translation: machine
translated_at: '2026-10-24'
---
# MVCC et VACUUM dans PostgreSQL {#postgresql-mvcc-and-vacuum}

PostgreSQL utilise le contrôle de concurrence multi-versions (MVCC, Multi-Version Concurrency Control) : les lectures ne bloquent jamais les écritures, et inversement. En contrepartie, les UPDATE et DELETE génèrent des tuples morts (dead tuples) qui doivent être nettoyés par VACUUM.

## Mécanique du MVCC {#mvcc-mechanics}

Chaque UPDATE crée une nouvelle version de la ligne (tuple) dans le heap. L'ancienne version est marquée comme morte, mais elle reste en place jusqu'à ce que VACUUM la supprime. DELETE marque le tuple comme mort sans récupérer l'espace. Chaque transaction voit un snapshot cohérent, déterminé par son niveau d'isolation.

## VACUUM {#vacuum}

VACUUM récupère l'espace occupé par les tuples morts et met à jour les statistiques utilisées par le planificateur de requêtes.

**VACUUM standard :** Marque l'espace des tuples morts comme réutilisable au sein de la table. Il ne rend PAS l'espace au système d'exploitation. Il autorise les lectures et écritures concurrentes (verrou SHARE UPDATE EXCLUSIVE).

**VACUUM FULL :** Réécrit l'intégralité de la table et rend l'espace au système d'exploitation. Il bloque TOUS les accès (verrou ACCESS EXCLUSIVE). À n'utiliser que lorsque la table est fortement gonflée.

**Autovacuum :** Processus d'arrière-plan qui exécute VACUUM automatiquement en fonction des seuils de tuples morts. Ne jamais le désactiver : des statistiques obsolètes entraînent de mauvais plans d'exécution et un bloat des tables et des index.

## Points clés {#key-facts}

- Une mise à jour HOT (Heap-Only Tuple) évite la mise à jour des index si : (1) les colonnes modifiées ne sont pas indexées ET (2) le nouveau tuple tient dans la même page
- Configuration de l'autovacuum : `autovacuum_vacuum_threshold` + `autovacuum_vacuum_scale_factor * reltuples`
- `pg_stat_user_tables.n_dead_tup` indique le nombre de tuples morts par table
- VACUUM met également à jour la visibility map (nécessaire pour les index-only scans)
- Processus PostgreSQL : postmaster, backend (un par connexion), background writer, WAL writer, checkpointer, lanceur d'autovacuum, collecteur de statistiques

## Modèles d'utilisation {#patterns}

### Surveillance du bloat et des tuples morts {#monitoring-bloat-and-dead-tuples}
```sql
-- Dead tuples per table
SELECT schemaname, relname, n_dead_tup, n_live_tup,
  round(n_dead_tup::numeric / GREATEST(n_live_tup, 1) * 100, 2) AS dead_pct,
  last_autovacuum, last_autoanalyze
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC;

-- Table bloat estimation
SELECT * FROM pgstattuple('my_table');

-- Check shared buffer contents
CREATE EXTENSION pg_buffercache;
```

### Réglage de l'autovacuum {#autovacuum-tuning}
```sql
-- Per-table autovacuum settings for high-churn tables
ALTER TABLE hot_table SET (
  autovacuum_vacuum_scale_factor = 0.01,  -- trigger at 1% dead tuples (default 20%)
  autovacuum_analyze_scale_factor = 0.01,
  autovacuum_vacuum_cost_delay = 0        -- no throttling for this table
);
```

### Ajout d'une colonne avec valeur par défaut (avant PG11) {#adding-column-with-default-pre-pg11}
```sql
-- Pre-PG11: batch update to avoid full table rewrite
ALTER TABLE big_table ADD COLUMN new_col INTEGER;
-- Then batch-update in chunks of 10-100K rows:
UPDATE big_table SET new_col = 42 WHERE id BETWEEN 1 AND 100000;
VACUUM big_table;  -- between batches
-- Finally: ALTER TABLE big_table ALTER COLUMN new_col SET DEFAULT 42;
-- PG 11+: ADD COLUMN with DEFAULT is instant (no rewrite)
```

## Architecture de PostgreSQL (processus) {#postgresql-architecture-processes}

| Processus | Rôle |
|-----------|------|
| Postmaster | Démon principal, crée les backends par fork |
| Backend | Un par connexion : analyse, planification, exécution |
| Background Writer | Écrit périodiquement les pages sales sur le disque |
| WAL Writer | Écrit les tampons WAL sur le disque |
| Checkpointer | Garantit un état cohérent du disque à chaque intervalle de checkpoint |
| Lanceur d'autovacuum | Lance les workers de VACUUM |
| Collecteur de statistiques | Collecte les statistiques de requêtes pour l'optimiseur |
| WAL Sender/Receiver | Réplication en flux |

Mémoire partagée : shared_buffers (cache de pages), tampons WAL, tables de verrous, proc array.

## Pièges à éviter {#gotchas}

- Ne jamais désactiver l'autovacuum : cela provoque des statistiques obsolètes, du bloat et une dégradation des performances
- VACUUM FULL nécessite un verrou exclusif et double temporairement l'espace disque utilisé
- Les transactions de longue durée empêchent VACUUM de nettoyer les tuples qu'elles pourraient encore voir (risque de wraparound de l'ID de transaction)
- `idle_in_transaction_session_timeout` empêche les transactions inactives de longue durée de bloquer VACUUM
- Amplification d'écriture : la mise à jour de n'importe quelle colonne réécrit le tuple entier et met à jour tous les index (sauf en cas de HOT)
- La migration de Uber de Postgres vers MySQL a été motivée par l'amplification d'écriture liée au grand nombre d'index secondaires

## Voir aussi {#see-also}

- [[transactions-and-acid]] - MVCC et niveaux d'isolation
- [[database-storage-internals]] - pages, heaps, amplification d'écriture
- [[concurrency-and-locking]] - types de verrous pendant VACUUM
- [[query-optimization-explain]] - statistiques obsolètes provoquant de mauvais plans
