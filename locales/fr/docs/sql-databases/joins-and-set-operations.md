---
title: "JOINs et opérations ensemblistes"
category: concepts
tags: [sql-databases, sql, join, inner-join, left-join, cross-join, union, intersect, except, anti-join]
level: 3
source_sha256: 936e7d1b2431f0399976db70e839bb3953888984b7eb359a7e2f8aaa4fac2492
translation: machine
translated_at: '2026-10-24'
---
# JOINs et opérations ensemblistes {#joins-and-set-operations}

Les JOINs combinent des lignes de deux tables ou plus à partir de colonnes liées. Les opérations ensemblistes combinent des ensembles de résultats verticalement. Ces deux mécanismes sont fondamentaux pour l'interrogation relationnelle.

## Points clés {#key-facts}

- INNER JOIN ne renvoie que les lignes correspondantes des deux tables
- LEFT JOIN renvoie toutes les lignes de la table de gauche, avec des NULL là où il n'y a pas de correspondance à droite
- CROSS JOIN produit le produit cartésien (chaque ligne associée à chaque ligne)
- Les colonnes de JOIN doivent toujours être indexées pour des raisons de performance
- UNION supprime les doublons (un tri est nécessaire) ; UNION ALL conserve les doublons (plus rapide)
- MySQL ne dispose pas de FULL OUTER JOIN natif : on l'émule avec un UNION de LEFT JOIN et de RIGHT JOIN

## Patterns {#patterns}

### INNER JOIN {#inner-join}
```sql
SELECT u.firstname, o.amount
FROM users u
INNER JOIN orders o ON u.id = o.user_id;
```

### LEFT JOIN (LEFT OUTER JOIN) {#left-join-left-outer-join}
```sql
SELECT u.firstname, o.amount
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;

-- Anti-join: find users with no orders
SELECT u.* FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE o.id IS NULL;
```

### CROSS JOIN {#cross-join}
```sql
-- Cartesian product: every size paired with every color
SELECT * FROM sizes CROSS JOIN colors;
```

### Self-JOIN {#self-join}
```sql
-- Employees and their managers
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;
```

### JOINs multi-tables {#multi-table-joins}
```sql
SELECT c.name AS city, co.name AS country, cl.language
FROM city c
JOIN country co ON c.country_code = co.code
JOIN country_language cl ON co.code = cl.country_code
WHERE cl.is_official = 'T';
```

### JOIN avec agrégation {#join-with-aggregation}
```sql
SELECT u.firstname, COUNT(pm.id) AS msg_count
FROM users u
LEFT JOIN private_messages pm ON u.id = pm.sender_id
GROUP BY u.id, u.firstname
ORDER BY msg_count DESC;
```

### Opérations ensemblistes {#set-operations}
```sql
-- UNION: combine results, remove duplicates
SELECT city FROM customers UNION SELECT city FROM suppliers;

-- UNION ALL: combine results, keep duplicates (faster)
SELECT city FROM customers UNION ALL SELECT city FROM suppliers;

-- INTERSECT: rows in both (PostgreSQL; MySQL uses INNER JOIN or IN)
SELECT genre FROM rock_albums INTERSECT SELECT genre FROM metal_albums;

-- EXCEPT: rows in first but not second (MySQL: LEFT JOIN WHERE IS NULL)
SELECT genre FROM all_albums EXCEPT SELECT genre FROM jazz_albums;
```

### FULL OUTER JOIN (contournement pour MySQL) {#full-outer-join-mysql-workaround}
```sql
-- MySQL doesn't support FULL OUTER JOIN directly
SELECT * FROM t1 LEFT JOIN t2 ON t1.id = t2.t1_id
UNION
SELECT * FROM t1 RIGHT JOIN t2 ON t1.id = t2.t1_id;
```

## Pièges à éviter {#gotchas}

- La syntaxe de jointure implicite (`FROM t1, t2 WHERE t1.id = t2.fk`) est un anti-pattern : utilisez systématiquement un JOIN explicite
- Les opérations ensemblistes exigent le même nombre de colonnes et des types compatibles
- Les noms de colonnes du résultat d'un UNION proviennent de la première requête
- Les JOINs sont généralement plus rapides que les sous-requêtes corrélées
- Une condition de JOIN manquante produit un produit cartésien accidentel (ensemble de résultats énorme)

## Voir aussi {#see-also}

- [[subqueries-and-ctes]] - EXISTS comme alternative aux JOINs
- [[index-strategies]] - indexation des colonnes FK pour la performance des JOINs
- [[query-optimization-explain]] - Hash Join vs Merge Join vs Nested Loop
