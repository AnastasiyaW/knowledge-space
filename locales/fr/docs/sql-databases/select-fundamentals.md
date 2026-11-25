---
title: "Fondamentaux de SELECT"
category: concepts
tags: [sql-databases, sql, select, where, order-by, limit, filtering, case]
level: 2
source_sha256: 16f849e2d8ff86f430323d964515049dc74b7c4eef4957713acce7c7bd83df43
translation: machine
translated_at: '2026-10-24'
---
# Fondamentaux de SELECT {#select-fundamentals}

L'instruction SELECT est l'outil principal pour lire des données dans les bases de données relationnelles. Maîtriser ses clauses et leur ordre d'exécution est indispensable pour écrire des requêtes performantes.

## Ordre d'exécution des requêtes {#query-execution-order}

L'ordre de traitement logique diffère de la syntaxe écrite :

```sql
FROM / JOIN  ->  WHERE  ->  GROUP BY  ->  HAVING  ->  SELECT  ->  DISTINCT  ->  ORDER BY  ->  LIMIT / OFFSET
```

C'est pourquoi les alias de colonnes fonctionnent dans ORDER BY mais pas dans WHERE.

## Points clés {#key-facts}

- `SELECT *` est néfaste en production : il empêche les index-only scans, récupère les données TOAST, augmente le coût réseau et son comportement devient imprévisible lorsque des colonnes sont ajoutées
- `DISTINCT` nécessite un tri ou un hachage : à éviter lorsque c'est possible
- `LIMIT N OFFSET M` se dégrade linéairement avec M (il parcourt puis rejette M lignes)
- Les mots-clés SQL ne sont pas sensibles à la casse ; la convention consiste à écrire les mots-clés en MAJUSCULES et les identifiants en minuscules
- Avec MySQL, `LIKE` est insensible à la casse par défaut ; avec PostgreSQL, `LIKE` est sensible à la casse (utiliser `ILIKE`)

## Modèles {#patterns}

### Sélection de colonnes de base {#basic-column-selection}
```sql
SELECT * FROM users;
SELECT firstname, lastname FROM users;
SELECT firstname AS name, lastname AS surname FROM users;
SELECT DISTINCT city FROM users;
```

### Filtrage avec la clause WHERE {#where-clause-filtering}
```sql
-- Comparison: =, !=, <>, <, >, <=, >=
SELECT * FROM users WHERE age > 25;
SELECT * FROM users WHERE city = 'Moscow' AND age >= 18;

-- Range (inclusive both ends)
SELECT * FROM users WHERE age BETWEEN 18 AND 65;

-- Set membership
SELECT * FROM users WHERE city IN ('Moscow', 'London', 'Tokyo');

-- Pattern matching (% = any chars, _ = one char)
SELECT * FROM users WHERE name LIKE 'A%';
SELECT * FROM users WHERE email LIKE '%@gmail.com';

-- NULL checks (never use = NULL)
SELECT * FROM users WHERE phone IS NULL;
SELECT * FROM users WHERE phone IS NOT NULL;
```

### ORDER BY et LIMIT {#order-by-and-limit}
```sql
SELECT * FROM users ORDER BY lastname ASC, firstname DESC;
SELECT * FROM users ORDER BY created_at DESC LIMIT 10;
SELECT * FROM users LIMIT 10 OFFSET 20;  -- skip 20, take 10
```

### Champs calculés et CASE {#computed-fields-and-case}
```sql
SELECT name, population / surface_area AS density FROM country;
SELECT CONCAT(name, ' (', code, ')') AS info FROM country;  -- MySQL
SELECT name || ' (' || code || ')' AS info FROM country;     -- PostgreSQL

SELECT name,
  CASE
    WHEN age < 18 THEN 'minor'
    WHEN age BETWEEN 18 AND 65 THEN 'adult'
    ELSE 'senior'
  END AS category
FROM users;

-- Simple CASE
SELECT name,
  CASE status WHEN 'A' THEN 'Active' WHEN 'I' THEN 'Inactive' ELSE 'Unknown' END
FROM users;

-- CASE in aggregation
SELECT continent,
  SUM(CASE WHEN life_expectancy > 70 THEN 1 ELSE 0 END) AS healthy_count
FROM country GROUP BY continent;
```

### Pagination par clé (alternative à OFFSET) {#keyset-pagination-alternative-to-offset}
```sql
-- Instead of slow OFFSET:
SELECT * FROM posts WHERE id < :last_seen_id ORDER BY id DESC LIMIT 10;
-- Uses index, constant time regardless of "page number"
```

## Pièges {#gotchas}

- `OFFSET 10000 LIMIT 10` parcourt puis rejette 10 000 lignes : utiliser la pagination par clé pour les grands décalages
- Les comparaisons de `NULL` avec `=` ou `!=` donnent toujours UNKNOWN (la ligne est exclue)
- `WHERE phone != '123'` ne renvoie PAS les lignes où phone IS NULL : ajouter `OR phone IS NULL`
- Trier par position de colonne (`ORDER BY 2`) est valide mais fragile : à éviter en production
- La pagination par clé ne permet pas d'accéder à une page arbitraire, seulement « suivante » ou « précédente »

## Voir aussi {#see-also}

- [[aggregate-functions-group-by]] - COUNT, SUM, AVG avec GROUP BY et HAVING
- [[joins-and-set-operations]] - combiner des données de plusieurs tables
- [[subqueries-and-ctes]] - requêtes imbriquées et expressions de table communes
- [[window-functions]] - calculs par ligne sur des partitions
