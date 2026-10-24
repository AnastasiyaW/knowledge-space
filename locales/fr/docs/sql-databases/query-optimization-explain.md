---
title: "Optimisation des requêtes et EXPLAIN"
category: concepts
tags: [sql-databases, explain, explain-analyze, query-plan, optimizer, sequential-scan, index-scan, postgresql, mysql, performance]
level: 4
source_sha256: 978fe76033d74e9fdbfa49a64f5d25a0ce4385033f34be0064a6e4d23dc9adf9
translation: machine
translated_at: '2026-10-24'
---
# Optimisation des requêtes et EXPLAIN {#query-optimization-and-explain}

EXPLAIN révèle la manière dont la base de données prévoit d'exécuter une requête. EXPLAIN ANALYZE l'exécute et affiche les métriques réelles. Comprendre les opérateurs du plan et le modèle de coût est indispensable pour diagnostiquer les requêtes lentes.

## Sortie d'EXPLAIN {#explain-output}

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) SELECT * FROM orders WHERE user_id = 42;
```

Champs clés de la sortie :
- **cost :** startup_cost..total_cost, en unités arbitraires (PAS en millisecondes)
- **rows :** nombre estimé de lignes renvoyées (basé sur les statistiques des tables)
- **width :** taille moyenne d'une ligne, en octets
- **actual time :** en millisecondes (uniquement avec ANALYZE), first_row..total
- **loops :** nombre d'exécutions de ce nœud
- **Buffers :** shared hit (cache) par opposition à read (disque)

### Unités de coût (PostgreSQL) {#cost-units-postgresql}
```toml
seq_page_cost = 1.0       -- baseline: sequential page read
random_page_cost = 4.0    -- random page read (lower to 1.1-2.0 for SSD)
cpu_tuple_cost = 0.01     -- processing one row
cpu_index_tuple_cost = 0.005
cpu_operator_cost = 0.0025
```

## Types de nœuds du plan {#plan-node-types}

| Opérateur | Description | Notes de performance |
|-----------|-------------|----------------------|
| Seq Scan | Parcours complet de la table | Coût proportionnel à la taille de la table |
| Index Scan | Recherche dans le B+Tree + lecture du heap | 2 E/S ou plus par ligne (index + heap) |
| Index Only Scan | Toutes les données lues dans l'index, sans heap | Le plus rapide : nécessite un index couvrant et une visibility map à jour |
| Bitmap Index Scan | Construction d'un bitmap, lecture séquentielle des pages | Adapté à une sélectivité modérée |
| Nested Loop Join | Pour chaque ligne externe, parcours de la table interne | Efficace lorsque la table interne possède un index ou est petite |
| Hash Join | Construction d'une table de hachage à partir de la plus petite table, puis sondage | Adapté aux grandes jointures d'égalité |
| Merge Join | Les deux entrées triées, parcours par fusion | Efficace lorsque les entrées sont déjà triées |
| Sort | Tri externe si la taille dépasse work_mem | Crée des fichiers temporaires si la mémoire est insuffisante |
| Aggregate | Traitement GROUP BY | Par hachage ou par tri |
| Gather | Coordination de requête parallèle | |

## Outils de visualisation {#visualization-tools}

- https://explain.tensor.ru - visualisation interactive du plan
- https://tatiyants.com/pev - visualiseur de plan
- https://explain.depesz.com - analyse détaillée

## Liste de contrôle pour l'optimisation des requêtes {#query-optimization-checklist}

### Niveau SQL {#sql-level}
- Utiliser UNION ALL au lieu de UNION lorsque les doublons sont acceptables
- Ne sélectionner que les colonnes nécessaires (éviter `SELECT *`)
- Éviter DISTINCT lorsque c'est possible (il signale souvent une mauvaise JOIN)
- Pour les index composites, inclure la première colonne dans les requêtes
- Utiliser EXISTS/IN lorsque c'est applicable
- Petites tables : un parcours complet est plus rapide qu'un parcours d'index (tient dans une seule page)
- Les fonctions appliquées aux colonnes indexées désactivent l'utilisation de l'index

### Niveau base de données {#database-level}
- Exécuter `ANALYZE` régulièrement pour disposer de statistiques à jour
- Ajuster `work_mem` pour les requêtes complexes avec tris et hachages
- Définir `random_page_cost = 1.1-2.0` pour un stockage SSD
- Augmenter `default_statistics_target` pour de meilleures estimations de cardinalité
- Activer `pg_stat_statements` pour repérer les requêtes lentes ou fréquentes

### Niveau architecture {#architecture-level}
- Ajouter un pooler de connexions lorsque max_connections dépasse 100-200
- Envisager des réplicas en lecture pour les charges à dominante lecture
- Vues matérialisées pour les agrégations lourdes et répétées
- Partitionner les grandes tables par date ou par intervalle
- Regrouper les opérations DML volumineuses en lots

## Modèles {#patterns}

### Diagnostic de statistiques obsolètes {#diagnosing-stale-statistics}
```sql
-- Compare estimated vs actual rows - large discrepancy = stale stats
EXPLAIN ANALYZE SELECT * FROM orders WHERE status = 'active';
-- If estimated: 100, actual: 50000 -> run ANALYZE
ANALYZE orders;
```

### Forcer l'utilisation d'un index (test uniquement) {#forcing-index-use-testing-only}
```sql
-- PostgreSQL: disable seq scan to test if index would help
SET enable_seqscan = off;
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 42;
RESET enable_seqscan;

-- MySQL: force specific index
SELECT * FROM orders FORCE INDEX (idx_user_id) WHERE user_id = 42;
```

### Extensions de supervision {#monitoring-extensions}
```sql
-- pg_stat_statements: find slowest/most frequent queries
CREATE EXTENSION pg_stat_statements;
SELECT query, calls, mean_exec_time, total_exec_time
FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 10;

-- auto_explain: automatically log slow query plans
ALTER SYSTEM SET auto_explain.log_min_duration = '1s';
```

### Deferred Joins (optimisation MySQL) {#deferred-joins-mysql-optimization}

Lors de la pagination avec OFFSET sur de grandes tables, la base lit et rejette tout de même les lignes :
```sql
-- SLOW: reads and discards 100000 rows
SELECT * FROM posts ORDER BY created_at DESC LIMIT 20 OFFSET 100000;

-- FAST: deferred join - only fetch IDs first, then join for data
SELECT p.* FROM posts p
INNER JOIN (
    SELECT id FROM posts ORDER BY created_at DESC LIMIT 20 OFFSET 100000
) AS sub ON p.id = sub.id;
-- Inner query uses covering index (id, created_at), outer fetches full rows only for 20 results
```

### Pagination par curseur (alternative à OFFSET) {#cursor-based-pagination-alternative-to-offset}

```sql
-- Instead of OFFSET (scans discarded rows):
SELECT * FROM posts ORDER BY id DESC LIMIT 20 OFFSET 100000;

-- Use cursor (seeks directly via index):
SELECT * FROM posts WHERE id < :last_seen_id ORDER BY id DESC LIMIT 20;
-- O(1) seek vs O(N) scan - cursor pagination is constant time regardless of page depth
```

### Motif horodatages ou booléens {#timestamps-vs-booleans-pattern}

```sql
-- Instead of boolean columns with unclear semantics:
ALTER TABLE orders ADD COLUMN is_shipped BOOLEAN DEFAULT FALSE;

-- Use timestamp - carries both state AND timing:
ALTER TABLE orders ADD COLUMN shipped_at TIMESTAMP NULL;
-- NULL = not shipped, non-NULL = shipped (and you know when)
-- WHERE shipped_at IS NOT NULL = WHERE is_shipped = TRUE
-- Bonus: indexable, sortable, auditable
```

### Tables de synthèse pour les agrégations coûteuses {#summary-tables-for-expensive-aggregations}

```sql
-- Instead of running COUNT(*) GROUP BY on millions of rows:
CREATE TABLE daily_stats (
    date DATE PRIMARY KEY,
    order_count INT,
    total_revenue DECIMAL(12,2),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Populate periodically or via trigger
INSERT INTO daily_stats (date, order_count, total_revenue)
SELECT DATE(created_at), COUNT(*), SUM(amount)
FROM orders
WHERE DATE(created_at) = CURRENT_DATE
ON CONFLICT (date) DO UPDATE SET
    order_count = EXCLUDED.order_count,
    total_revenue = EXCLUDED.total_revenue,
    updated_at = CURRENT_TIMESTAMP;
```

### Signaux d'alerte dans EXPLAIN {#explain-red-flags-to-watch-for}

| Signal d'alerte | Signification | Action |
|-----------------|---------------|--------|
| Seq Scan sur une grande table | Index absent ou non utilisé | Ajouter un index, vérifier la SARGabilité |
| Estimation de lignes très éloignée de la réalité | Statistiques obsolètes | `ANALYZE table` |
| Tri sur disque | `work_mem` trop faible | Augmenter `work_mem` ou ajouter un index trié |
| Nested Loop avec Seq Scan en interne | Index absent sur la colonne de jointure | Ajouter un index sur la clé de jointure de la table interne |
| Hash Join débordant sur disque | `work_mem` trop faible pour la table de hachage | Augmenter `work_mem` |

## Pièges {#gotchas}

- EXPLAIN ANALYZE exécute réellement la requête (y compris les DML !) : l'encapsuler dans une transaction et faire un ROLLBACK
- Les plans valables pour des tables de 1000 lignes ne se extrapolent pas à des millions de lignes : les coûts du planificateur ne sont pas linéaires
- Les tables tenant sur une seule page utilisent toujours un parcours séquentiel, quels que soient les index
- La durée mesurée par EXPLAIN ANALYZE exclut le transfert réseau et la conversion de format
- Une valeur élevée de `join_collapse_limit` améliore le plan mais ralentit la planification pour les jointures portant sur de nombreuses tables
- Après un VACUUM, la visibility map est mise à jour : un Index Only Scan peut remplacer un Seq Scan
- `EXPLAIN` de MySQL affiche le plan estimé ; `EXPLAIN ANALYZE` (8.0.18+) affiche l'exécution réelle : pour un diagnostic fiable, utiliser toujours ANALYZE
- `SELECT *` empêche les index-only scans : spécifier uniquement les colonnes nécessaires pour permettre l'utilisation d'un index couvrant
- Les sous-requêtes corrélées s'exécutent une fois par ligne externe : les réécrire en JOIN, ou utiliser une jointure latérale lorsque c'est possible

## Voir aussi {#see-also}

- [[index-strategies]] - création et choix des index
- [[btree-and-index-internals]] - comprendre les types de parcours
- [[postgresql-configuration-tuning]] - paramètres du planificateur
- [[postgresql-mvcc-vacuum]] - VACUUM et fraîcheur des statistiques
