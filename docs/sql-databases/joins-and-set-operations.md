---
title: JOINs and Set Operations
category: concepts
tags: [sql-databases, joins, inner-join, outer-join, union, set-operations]
---

# JOINs and Set Operations

JOINs combine rows from two or more tables based on related columns. Set operations (UNION, INTERSECT, EXCEPT) combine result sets vertically. Understanding JOIN mechanics and when to use each type is critical for writing correct and performant queries.

## INNER JOIN

Returns only rows with matches in both tables.

```sql
SELECT u.firstname, o.amount
FROM users u
INNER JOIN orders o ON u.id = o.user_id;
```

## LEFT JOIN (LEFT OUTER JOIN)

Returns all rows from left table; NULL for unmatched right side. The anti-join pattern finds rows without matches:

```sql
-- All users, even those without orders
SELECT u.firstname, o.amount
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;

-- Users with NO orders (anti-join)
SELECT u.* FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE o.id IS NULL;
```

## RIGHT JOIN

Returns all rows from right table. Rarely used - equivalent to LEFT JOIN with tables swapped.

## FULL OUTER JOIN

Returns all rows from both tables. MySQL lacks native support - emulate with UNION:

```sql
-- PostgreSQL: native
SELECT * FROM t1 FULL OUTER JOIN t2 ON t1.id = t2.t1_id;

-- MySQL: emulation
SELECT * FROM t1 LEFT JOIN t2 ON t1.id = t2.t1_id
UNION
SELECT * FROM t1 RIGHT JOIN t2 ON t1.id = t2.t1_id;
```

## CROSS JOIN

Cartesian product - every row from A paired with every row from B. Use intentionally (e.g., generating combinations):

```sql
SELECT s.size, c.color FROM sizes s CROSS JOIN colors c;
```

## Self-JOIN

Table joined with itself for hierarchical data:

```sql
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;

-- Reply chains in messages
SELECT orig.body AS original, reply.body AS reply
FROM messages orig
JOIN messages reply ON reply.reply_to_id = orig.id;
```

## Multi-Table JOINs

```sql
SELECT city.Name AS city, country.Name AS country, cl.Language
FROM city
JOIN country ON city.CountryCode = country.Code
JOIN countrylanguage cl ON country.Code = cl.CountryCode
WHERE cl.IsOfficial = 'T';
```

## JOIN with Aggregation

```sql
SELECT u.firstname, u.lastname, COUNT(pm.id) AS msg_count
FROM users u
LEFT JOIN private_messages pm ON u.id = pm.sender_id
GROUP BY u.id, u.firstname, u.lastname
ORDER BY msg_count DESC;
```

## Set Operations

```sql
-- UNION: combine results, remove duplicates
SELECT city FROM customers UNION SELECT city FROM suppliers;

-- UNION ALL: keep duplicates (faster - no deduplication sort)
SELECT city FROM customers UNION ALL SELECT city FROM suppliers;

-- INTERSECT: rows in both result sets
SELECT genre FROM rock_albums INTERSECT SELECT genre FROM metal_albums;

-- EXCEPT (MINUS in Oracle): rows in first but not second
SELECT genre FROM all_albums EXCEPT SELECT genre FROM jazz_albums;
```

Requirements: same number of columns, compatible types. Column names come from first query. ORDER BY only at the end.

### Table Comparison Pattern

```sql
SELECT band_id, COUNT(*) FROM album GROUP BY band_id
EXCEPT
SELECT id, album_count FROM band_summary;
```

## Patterns

### Subquery vs JOIN Performance

JOINs are generally faster than correlated subqueries (subquery executes once per outer row). Rewrite correlated subqueries as JOINs when possible. EXISTS is efficient when you only need an existence check (stops at first match).

```sql
-- Slow: correlated subquery
SELECT * FROM users u WHERE (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) > 5;

-- Fast: JOIN with aggregation
SELECT u.* FROM users u
JOIN (SELECT user_id, COUNT(*) AS cnt FROM orders GROUP BY user_id HAVING cnt > 5) o
ON u.id = o.user_id;
```

## Gotchas

- JOIN columns should always be indexed - FK columns are prime candidates
- Implicit joins (`FROM t1, t2 WHERE t1.id = t2.fk`) are harder to read and error-prone - always use explicit JOIN syntax
- CROSS JOIN between large tables produces N*M rows - ensure intentional use
- MySQL emulation of FULL OUTER JOIN via UNION may produce duplicate rows if not handled carefully
- Cartesian products in JOINs (missing ON clause) can silently produce massive result sets

## See Also

- [[select-fundamentals]] - basic query structure
- [[subqueries-and-ctes]] - nested queries as alternatives to JOINs
- [[index-strategy-optimization]] - indexing JOIN columns
- [[query-optimization-explain]] - comparing JOIN plan operators
