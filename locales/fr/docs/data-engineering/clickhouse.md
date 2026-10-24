---
title: "ClickHouse"
category: tools
tags: [data-engineering, clickhouse, olap, columnar, analytics, database]
level: 3
source_sha256: 1a98d0e5f157926866ae0d05c9a331100bda9c7be64ae7e4fa0cf0fd603d6242
translation: machine
translated_at: '2026-10-24'
---
# ClickHouse {#clickhouse}

ClickHouse est un SGBD en colonnes pour les charges de travail OLAP. Créé chez Yandex pour Yandex.Metrica (13 000 milliards d'enregistrements, 20 milliards d'événements par jour). Optimisé pour le débit plutôt que la latence : des milliards de lignes/s, une latence d'environ 50 ms acceptable, environ 100 requêtes/s par serveur.

## Quand utiliser ClickHouse {#when-to-use-clickhouse}

| Profil | Adéquation |
|--------|------------|
| Gestion de logs (tables larges plates, append-only) | Excellent |
| Séries temporelles (insertions en flux, agrégations simples) | Excellent |
| DWH analytique (schéma en étoile/flocon, insertions ETL) | Bon |
| DWH très normalisé (Data Vault, changements fréquents) | Faible |

## Ce que ClickHouse n'est pas {#what-clickhouse-is-not}
Pas un SGBD relationnel complet : pas de transactions, pas de garanties de cohérence, pas de curseurs, pas de procédures stockées, pas de contraintes UNIQUE/FOREIGN KEY. PRIMARY KEY n'impose PAS l'unicité. UPDATE/DELETE partiels uniquement (mutations asynchrones via ALTER TABLE).

## Stockage colonnaire {#columnar-storage}

Les données sont stockées colonne par colonne. Lire 3 colonnes d'une table large ne représente qu'environ 3 % des données, contre un scan de lignes complètes. Les colonnes triées se compressent fortement via RLE.

**Règle :** moins de colonnes dans SELECT = moins d'E/S. Spécifiez toujours les colonnes nécessaires, évitez `SELECT *`.

## Stockage physique {#physical-storage}

```php
Table
  -> Partitions (independent file groups on disk)
    -> Granules (default 8192 rows)
      -> Files: primary.idx, [column].mrk2, [column].bin
```

### Recommandations de partitionnement {#partition-guidelines}
- L'attribut DOIT apparaître dans les requêtes - sinon pas d'élagage de partitions
- Taille : de quelques Go à 150 Go par partition
- Typique : `PARTITION BY toYYYYMM(date_column)`

```sql
SELECT partition, formatReadableSize(sum(bytes))
FROM system.parts WHERE table = 'my_table'
GROUP BY partition;
```

## Clé primaire et granules {#primary-key-and-granules}

**Règle critique :** la clé primaire fonctionne de gauche à droite. Pour `ORDER BY (a, b, c)` :
- Filtrer par `a` - utilise l'index
- Filtrer par `a AND b` - utilise l'index
- Filtrer par `b` seul - **ne peut pas utiliser l'index**, lit tous les granules

**PK dans ClickHouse != PK en relationnel :** pas d'unicité, pas de références FK. Il s'agit uniquement d'une optimisation des performances de lecture.

## DML {#dml}

```sql
INSERT INTO table VALUES (...), (...);
INSERT INTO table SELECT ... FROM other_table;

-- Async mutations (not instant!)
ALTER TABLE table UPDATE col = val WHERE condition;
ALTER TABLE table DELETE WHERE condition;
OPTIMIZE TABLE table FINAL;  -- force merge
```

## Fonctions spécifiques à ClickHouse {#clickhouse-specific-functions}

### Comptage approximatif vs exact {#approximate-vs-exact-counting}

| Fonction | Précision | Performance |
|----------|-----------|-------------|
| `uniq()` | Approximative (HyperLogLog) | Rapide |
| `uniqExact()` | Exacte | Lente, forte consommation mémoire |
| `uniqCombined()` | Hybride | Équilibrée |

### Suffixes d'agrégats {#aggregate-suffixes}

```sql
sumIf(amount, status = 'completed')   -- conditional sum
countIf(id, type = 'click')           -- conditional count
avgIf(score, score > 0)               -- conditional average
```

### Quantiles {#quantiles}

```sql
SELECT quantile(0.5)(price) AS median_approx FROM prices;
SELECT quantileExact(0.5)(salary) AS median_exact FROM employees;
SELECT quantiles(0.25, 0.5, 0.75)(price) AS quartiles FROM prices;
```

## JOIN étendus {#extended-joins}

| Type | Comportement |
|------|--------------|
| LEFT SEMI JOIN | Lignes de gauche ayant une correspondance (sans colonnes de droite) |
| LEFT ANTI JOIN | Lignes de gauche SANS correspondance |
| LEFT ANY JOIN | Une correspondance quelconque à droite |
| ASOF JOIN | Correspondance par la valeur ordonnée la plus proche |

### ASOF JOIN {#asof-join}

```sql
SELECT m.time, m.value, e.event
FROM metrics m
ASOF LEFT JOIN events e
  ON m.user_id = e.user_id AND m.time >= e.time;
```

## Analyse des requêtes {#query-analysis}

```sql
EXPLAIN PLAN indexes = 1 SELECT ...;
```

**Optimal :** filtrer à la fois sur la clé de partitionnement ET sur la clé primaire pour un élagage en deux étapes.

## Pièges à éviter {#gotchas}
- UPDATE/DELETE sont des mutations asynchrones - non conçues pour des opérations fréquentes sur une seule ligne
- La déduplication de ReplacingMergeTree a lieu lors des fusions - elle n'est pas immédiate ; utilisez `SELECT ... FINAL`
- La clé primaire n'impose PAS l'unicité
- Les UDF ralentissent considérablement ClickHouse
- Utilisez toujours des types de données adaptés (UInt32 et non String pour les identifiants) pour la compression

## Voir aussi {#see-also}
- [[clickhouse-engines]] - La famille MergeTree et le choix du moteur
- [[dwh-architecture]] - ClickHouse comme couche OLAP
- [[sql-for-de]] - Patterns SQL
