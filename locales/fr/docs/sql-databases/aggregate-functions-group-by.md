---
title: "Fonctions d'agrégation et GROUP BY"
category: concepts
tags: [sql-databases, sql, aggregation, group-by, having, count, sum, avg]
level: 3
source_sha256: cb0df95efe3ef4f09ff2e423a536bf2950e93522a3a05c0b28a68d9c5f54554a
translation: machine
translated_at: '2026-10-24'
---
# Fonctions d'agrégation et GROUP BY {#aggregate-functions-and-group-by}

Les fonctions d'agrégation regroupent plusieurs lignes en une seule valeur de synthèse. GROUP BY répartit les lignes en groupes avant l'agrégation, tandis que HAVING filtre les groupes obtenus.

## Points clés {#key-facts}

- `COUNT(*)` compte toutes les lignes, y compris celles contenant des NULL ; `COUNT(colonne)` ne compte que les valeurs non NULL
- `SUM`, `AVG`, `MIN` et `MAX` ignorent tous les NULL
- `GROUP BY` regroupe tous les NULL dans un même groupe
- HAVING filtre les groupes après l'agrégation ; WHERE filtre les lignes avant le regroupement
- Il est impossible d'utiliser des fonctions d'agrégation dans la clause WHERE

## Modèles {#patterns}

### Agrégation de base {#basic-aggregation}
```sql
SELECT COUNT(*) FROM users;
SELECT COUNT(DISTINCT city) FROM users;
SELECT SUM(amount), AVG(amount), MIN(amount), MAX(amount) FROM orders;
```

### GROUP BY {#group-by}
```sql
SELECT city, COUNT(*) AS user_count
FROM users
GROUP BY city
ORDER BY user_count DESC;

-- Multiple grouping columns
SELECT country_code, district, COUNT(*) AS city_count
FROM city
GROUP BY country_code, district;
```

### HAVING (filtrage sur les résultats agrégés) {#having-filter-on-aggregated-results}
```sql
SELECT genre, COUNT(*) AS cnt
FROM album
GROUP BY genre
HAVING COUNT(*) > 5
ORDER BY cnt DESC;

-- Combine WHERE and HAVING
SELECT continent, AVG(life_expectancy) AS avg_life
FROM country
WHERE population > 1000000        -- filter rows before grouping
GROUP BY continent
HAVING avg_life > 70              -- filter groups after aggregation
ORDER BY avg_life DESC;
```

### Performance de COUNT sur les grandes tables {#count-performance-on-large-tables}

`SELECT COUNT(*) FROM large_table` nécessite un parcours complet de la table ou de l'index : avec MVCC, des transactions différentes peuvent voir des nombres de lignes différents.

**Alternatives pour obtenir des comptages approximatifs :**
```sql
-- PostgreSQL: approximate from statistics
SELECT reltuples::bigint FROM pg_class WHERE relname = 'large_table';

-- MySQL: approximate from information_schema
SELECT table_rows FROM information_schema.tables
WHERE table_name = 'large_table';
```

Autres stratégies : table de comptage matérialisée mise à jour par des déclencheurs, compteur Redis incrémenté lors des INSERT/DELETE, HyperLogLog pour une approximation du nombre de valeurs distinctes.

## Pièges à éviter {#gotchas}

- `AVG` ignore les NULL : la moyenne de `[10, NULL, 20]` est 15, et non 10
- Les colonnes du SELECT doivent soit figurer dans le GROUP BY, soit être placées à l'intérieur de fonctions d'agrégation
- `COUNT(DISTINCT col)` est plus lent que `COUNT(*)` : il nécessite une déduplication
- MySQL autorise des colonnes non agrégées dans le SELECT sans GROUP BY (selon le `sql_mode`) ; PostgreSQL ne le permet pas

## Voir aussi {#see-also}

- [[select-fundamentals]] - clause WHERE et filtrage de base
- [[window-functions]] - agrégations sans réduction du nombre de lignes
- [[query-optimization-explain]] - optimisation des requêtes d'agrégation
