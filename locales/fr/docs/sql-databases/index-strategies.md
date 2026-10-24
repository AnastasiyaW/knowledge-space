---
title: "Stratégies d'index"
category: concepts
tags: [sql-databases, index, composite-index, covering-index, partial-index, sargable, index-only-scan, create-index-concurrently]
level: 3
source_sha256: ad276054591fbf1f402fe5979a8cc9b088bcf318e23217472de564e59fec6e28
translation: machine
translated_at: '2026-10-24'
---
# Stratégies d'index {#index-strategies}

Les index accélèrent les lectures mais ralentissent les écritures. Le choix des index à créer, de leur ordre de colonnes et de leur type est déterminant pour les performances en production.

## Types de parcours d'index (PostgreSQL) {#index-scan-types-postgresql}

| Type de parcours | Description | Quand il est utilisé |
|-----------|-------------|-----------|
| Sequential Scan | Lecture complète du heap, page par page | Aucun index utilisable, grande fraction du résultat, petite table |
| Index Scan | Parcours du B+Tree, lecture des pages heap pour les correspondances | Requête sélective, peu de lignes correspondantes |
| Index-Only Scan | Restitution des données depuis l'index sans accès au heap | Toutes les colonnes présentes dans l'index (couvrant), visibility map à jour |
| Bitmap Index Scan | Construction d'un bitmap des pages correspondantes, lecture séquentielle | Sélectivité modérée, plusieurs index combinables |

## Faits essentiels {#key-facts}

- Index composite sur (a, b, c) utilisable pour WHERE a=1, WHERE a=1 AND b=2, mais PAS pour WHERE b=2 seul
- Index couvrant : inclut toutes les colonnes nécessaires à la requête, supprime totalement l'accès au heap
- Index partiel/filtré : n'indexe que les lignes répondant à une condition (plus petit, plus rapide à maintenir)
- SARGable : `WHERE col = 5` utilise l'index ; `WHERE YEAR(col) = 2024` ne l'utilise PAS (fonction appliquée sur la colonne)
- Chaque index ajoute un surcoût aux INSERT/UPDATE/DELETE : éviter la sur-indexation en OLTP

## Modèles {#patterns}

### Index composite {#composite-index}
```sql
-- Column order matters: equality columns first, then range
CREATE INDEX idx_orders ON orders (status, created_at);
-- Usable for: WHERE status = 'active' AND created_at > '2024-01-01'
-- Usable for: WHERE status = 'active'
-- NOT usable for: WHERE created_at > '2024-01-01' (skips leftmost column)
```

### Index couvrant (Index-Only Scan) {#covering-index-index-only-scan}
```sql
-- PostgreSQL: INCLUDE for non-key columns in leaf pages
CREATE INDEX idx_orders_covering ON orders (user_id) INCLUDE (amount, status);
-- Query can be answered entirely from index:
SELECT amount, status FROM orders WHERE user_id = 42;
```

### Index partiel/filtré {#partialfiltered-index}
```sql
-- Index only active users (much smaller than full index)
CREATE INDEX idx_active_users ON users (email) WHERE status = 'active';
-- Only used when query includes WHERE status = 'active'
```

### CREATE INDEX CONCURRENTLY {#create-index-concurrently}
```sql
-- PostgreSQL: build index without blocking DML
CREATE INDEX CONCURRENTLY idx_name ON table (column);
-- Takes longer, two table scans, can't run in transaction, may fail (cleanup required)

-- MySQL equivalent: online DDL
ALTER TABLE t ADD INDEX idx_name (column), ALGORITHM=INPLACE, LOCK=NONE;
```

### Génération de données de test {#generating-test-data}
```sql
-- PostgreSQL: generate millions of rows for index testing
INSERT INTO grades (g) SELECT floor(random() * 100) FROM generate_series(1, 10000000);
```

## Sélection d'index par l'optimiseur {#optimizer-index-selection}

Lorsque plusieurs index existent, l'optimiseur estime le coût à partir de :
- La taille de la table et les statistiques issues de `pg_stats`
- La sélectivité de l'index (fraction de lignes correspondantes)
- La corrélation (ordre physique par rapport à l'ordre de l'index)
- Les paramètres de coût (`seq_page_cost`, `random_page_cost`)

Mécanismes de hint : extension `pg_hint_plan` (PostgreSQL), `USE INDEX`/`FORCE INDEX` (MySQL). En règle générale, faire confiance à l'optimiseur, sauf si EXPLAIN ANALYZE montre qu'il se trompe.

## Spécificités de SQL Server {#sql-server-specifics}

- **Index columnstore :** stockage orienté colonnes pour l'OLAP. Les lignes sont regroupées en rowgroups (~1 M de lignes), avec traitement en mode batch (~900 lignes à la fois). Combinables avec les index rowstore.
- **Index de hachage :** uniquement pour les tables optimisées en mémoire. Recherches ponctuelles en O(1), inadaptés aux intervalles.
- **Colonnes incluses :** colonnes non clés placées dans les feuilles pour créer un index couvrant sans affecter l'ordre de tri.

### Sélectivité d'index et cas où il ne faut PAS indexer {#index-selectivity-and-when-not-to-index}

```sql
-- Check selectivity: values near 1.0 = highly selective (good for index)
SELECT COUNT(DISTINCT status)::float / COUNT(*) AS selectivity FROM orders;
-- 0.0001 (4 statuses / 1M rows) = low selectivity, index may not help

-- Rule of thumb: index useful when selecting < 10-15% of rows
-- For low selectivity columns, bitmap scan may still combine with other indexes
```

### Index préfixés (MySQL) {#prefix-indexes-mysql}

Pour les longues colonnes de chaînes, n'indexer que les N premiers caractères :
```sql
-- Full index on email wastes space
CREATE INDEX idx_email ON users (email(20));

-- Find optimal prefix length:
SELECT
    COUNT(DISTINCT LEFT(email, 10)) / COUNT(*) AS sel_10,
    COUNT(DISTINCT LEFT(email, 15)) / COUNT(*) AS sel_15,
    COUNT(DISTINCT LEFT(email, 20)) / COUNT(*) AS sel_20,
    COUNT(DISTINCT email) / COUNT(*) AS sel_full
FROM users;
-- Pick smallest N where selectivity approaches full column selectivity
```

### Index fonctionnels {#functional-indexes}

```sql
-- PostgreSQL: index on expression
CREATE INDEX idx_lower_email ON users (LOWER(email));
-- Now WHERE LOWER(email) = 'user@example.com' uses the index

-- MySQL 8.0+: functional index
CREATE INDEX idx_year ON events ((YEAR(created_at)));
-- WHERE YEAR(created_at) = 2024 can use this index
```

### Index invisibles (MySQL 8.0+) {#invisible-indexes-mysql-80}

Tester l'impact de la suppression d'un index sans le supprimer réellement :
```sql
ALTER TABLE orders ALTER INDEX idx_status INVISIBLE;
-- Index ignored by optimizer but still maintained
-- Run queries, check performance
ALTER TABLE orders ALTER INDEX idx_status VISIBLE;  -- restore if needed
```

### Ordre des colonnes d'un index composite {#composite-index-column-ordering}

Règle Égalité – Intervalle – Tri :
```sql
-- Query: WHERE status = 'active' AND created_at > '2024-01-01' ORDER BY amount
-- Best composite index:
CREATE INDEX idx_optimal ON orders (status, created_at, amount);
--  1. status    = equality (exact match, narrows quickly)
--  2. created_at = range (further narrows, but stops B-tree traversal)
--  3. amount    = sort (avoids filesort if after range column in same direction)
```

### Détection des index en double et redondants {#duplicate-and-redundant-index-detection}

```sql
-- PostgreSQL: find unused indexes
SELECT schemaname, relname, indexrelname, idx_scan, pg_size_pretty(pg_relation_size(indexrelid))
FROM pg_stat_user_indexes WHERE idx_scan = 0 ORDER BY pg_relation_size(indexrelid) DESC;

-- MySQL: find redundant indexes (index on (a,b) makes index on (a) redundant)
SELECT * FROM sys.schema_redundant_indexes;
```

## Pièges {#gotchas}

- `CREATE INDEX` standard acquiert un ShareLock (PostgreSQL) : bloque les INSERT/UPDATE/DELETE
- CONCURRENTLY peut échouer et laisser un index invalide : il faut le supprimer (DROP) et relancer
- Un index-only scan dans PostgreSQL nécessite une visibility map à jour : exécuter VACUUM au préalable
- Trop d'index sur des tables à forte écriture ralentissent fortement les INSERT/UPDATE/DELETE
- Les bitmap scans combinent plusieurs index (AND/OR) : parfois, deux index médiocres battent un index parfait
- Les index secondaires InnoDB de MySQL effectuent toujours une double recherche via l'index clusterisé
- Les index préfixés MySQL ne peuvent pas servir à ORDER BY ou GROUP BY, seulement au filtrage
- Les index fonctionnels doivent correspondre exactement à l'expression de la requête : un index sur `LOWER(email)` n'aide pas une requête sur `UPPER(email)`
- Ajouter des colonnes à un index couvrant augmente sa taille et ralentit les écritures : évaluer le compromis par des mesures
- `FORCE INDEX` de MySQL est un dernier recours : si l'optimiseur se trompe, corriger d'abord les statistiques avec `ANALYZE TABLE`

## Voir aussi {#see-also}

- [[btree-and-index-internals]] - Structure du B+Tree et divisions de pages
- [[query-optimization-explain]] - Lecture de la sortie EXPLAIN pour vérifier l'utilisation des index
- [[concurrency-and-locking]] - Implications de verrouillage de la création d'index
- [[postgresql-configuration-tuning]] - Paramètres de coût influant sur la sélection des index
