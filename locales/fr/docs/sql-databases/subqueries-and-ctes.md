---
title: "Sous-requêtes et CTE"
category: concepts
tags: [sql-databases, sql, subquery, cte, common-table-expression, exists, derived-table, correlated]
level: 3
source_sha256: 94ef2760a1a68f5966909b5560a65e3fab391dbb8b9d77262335c4f7a4780079
translation: machine
translated_at: '2026-10-24'
---
# Sous-requêtes et CTE {#subqueries-and-ctes}

Les sous-requêtes sont des requêtes imbriquées dans d'autres requêtes. Les CTE (Common Table Expressions) fournissent des blocs de requête nommés et réutilisables, qui améliorent la lisibilité des requêtes SQL complexes.

## Points clés {#key-facts}

- Les sous-requêtes scalaires renvoient une valeur unique ; les sous-requêtes de table renvoient plusieurs lignes
- Les sous-requêtes corrélées s'exécutent une fois par ligne externe (peut être coûteux)
- EXISTS s'arrête à la première correspondance, ce qui le rend plus efficace que IN pour les tests d'existence
- Les CTE sont définis avec le mot-clé `WITH` et peuvent enchaîner plusieurs blocs nommés
- PostgreSQL matérialise les CTE par défaut (avant la version 12) ; utilisez l'indication `NOT MATERIALIZED` pour les intégrer en ligne

## Modèles {#patterns}

### Sous-requête scalaire {#scalar-subquery}
```sql
SELECT * FROM users
WHERE id = (SELECT sender_id FROM messages GROUP BY sender_id ORDER BY COUNT(*) DESC LIMIT 1);

-- Scalar subquery in SELECT
SELECT u.name,
  (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) AS order_count
FROM users u;
```

### Sous-requête avec IN {#in-subquery}
```sql
SELECT * FROM users WHERE id IN (SELECT user_id FROM orders WHERE amount > 1000);

-- NOT IN: find users without orders
SELECT * FROM users WHERE id NOT IN (
  SELECT DISTINCT sender_id FROM messages WHERE sender_id IS NOT NULL
);
```

### Sous-requête avec EXISTS {#exists-subquery}
```sql
-- Users who have at least one order
SELECT * FROM users u WHERE EXISTS (
  SELECT 1 FROM orders o WHERE o.user_id = u.id AND o.amount > 1000
);

-- Anti-pattern replacement: safer than NOT IN
SELECT * FROM users u WHERE NOT EXISTS (
  SELECT 1 FROM messages m WHERE m.sender_id = u.id
);
```

### Table dérivée (sous-requête dans FROM) {#derived-table-subquery-in-from}
```sql
SELECT avg_amount FROM (
  SELECT user_id, AVG(amount) AS avg_amount
  FROM orders GROUP BY user_id
) AS user_avgs
WHERE avg_amount > 500;
```

### CTE (Common Table Expression) {#cte-common-table-expression}
```sql
WITH active_users AS (
  SELECT user_id, COUNT(*) AS order_count
  FROM orders
  WHERE created_at > '2024-01-01'
  GROUP BY user_id
),
high_value AS (
  SELECT user_id, SUM(amount) AS total
  FROM orders
  GROUP BY user_id
  HAVING total > 10000
)
SELECT u.*, au.order_count, hv.total
FROM users u
JOIN active_users au ON u.id = au.user_id
JOIN high_value hv ON u.id = hv.user_id;
```

### CTE récursive {#recursive-cte}
```sql
-- Organizational hierarchy
WITH RECURSIVE org_tree AS (
  SELECT id, name, manager_id, 1 AS depth
  FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT e.id, e.name, e.manager_id, ot.depth + 1
  FROM employees e
  JOIN org_tree ot ON e.manager_id = ot.id
)
SELECT * FROM org_tree ORDER BY depth, name;
```

## Pièges {#gotchas}

- **NOT IN et les valeurs NULL** : si la sous-requête renvoie ne serait-ce qu'une valeur NULL, `NOT IN` renvoie un résultat vide pour TOUTES les lignes. Ajoutez toujours `WHERE col IS NOT NULL` ou utilisez NOT EXISTS à la place
- Les sous-requêtes corrélées s'exécutent une fois par ligne externe ; réécrivez-les en JOIN lorsque c'est possible
- `EXISTS` vérifie uniquement l'existence, pas les valeurs ; `SELECT 1` à l'intérieur est une convention
- Les CTE dans PostgreSQL < 12 sont des barrières d'optimisation (toujours matérialisées)
- MySQL ne prend pas en charge les CTE récursives avant la version 8.0

## Voir aussi {#see-also}

- [[select-fundamentals]] - filtrage de base avec WHERE
- [[joins-and-set-operations]] - les JOIN comme alternative aux sous-requêtes
- [[window-functions]] - analyses sans sous-requêtes
