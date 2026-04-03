---
title: JOINs and Set Operations
category: concepts
tags: [sql-databases, sql, join, inner-join, left-join, cross-join, union, intersect, except, anti-join]
---

# JOINs and Set Operations

JOINs combine rows from two or more tables based on related columns. Set operations combine result sets vertically. Both are fundamental to relational querying.

## Key Facts

- INNER JOIN returns only matching rows from both tables
- LEFT JOIN returns all rows from left table, NULLs where no match on right
- CROSS JOIN produces Cartesian product (every row paired with every row)
- JOIN columns should always be indexed for performance
- UNION removes duplicates (sorting required); UNION ALL keeps duplicates (faster)
- MySQL lacks native FULL OUTER JOIN - emulate with UNION of LEFT and RIGHT JOINs

## Patterns

### INNER JOIN
```sql
SELECT u.firstname, o.amount
FROM users u
INNER JOIN orders o ON u.id = o.user_id;
```

### LEFT JOIN (LEFT OUTER JOIN)
```sql
SELECT u.firstname, o.amount
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;

-- Anti-join: find users with no orders
SELECT u.* FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE o.id IS NULL;
```

### CROSS JOIN
```sql
-- Cartesian product: every size paired with every color
SELECT * FROM sizes CROSS JOIN colors;
```

### Self-JOIN
```sql
-- Employees and their managers
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;
```

### Multi-Table JOINs
```sql
SELECT c.name AS city, co.name AS country, cl.language
FROM city c
JOIN country co ON c.country_code = co.code
JOIN country_language cl ON co.code = cl.country_code
WHERE cl.is_official = 'T';
```

### JOIN with Aggregation
```sql
SELECT u.firstname, COUNT(pm.id) AS msg_count
FROM users u
LEFT JOIN private_messages pm ON u.id = pm.sender_id
GROUP BY u.id, u.firstname
ORDER BY msg_count DESC;
```

### Set Operations
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

### FULL OUTER JOIN (MySQL Workaround)
```sql
-- MySQL doesn't support FULL OUTER JOIN directly
SELECT * FROM t1 LEFT JOIN t2 ON t1.id = t2.t1_id
UNION
SELECT * FROM t1 RIGHT JOIN t2 ON t1.id = t2.t1_id;
```

## Gotchas

- Implicit join syntax (`FROM t1, t2 WHERE t1.id = t2.fk`) is an anti-pattern - always use explicit JOIN
- Set operations require same number of columns and compatible types
- Column names in UNION results come from the first query
- JOINs are generally faster than correlated subqueries
- Missing JOIN condition produces accidental Cartesian product (huge result set)

## See Also

- [[subqueries-and-ctes]] - EXISTS as alternative to JOINs
- [[index-strategies]] - indexing FK columns for JOIN performance
- [[query-optimization-explain]] - Hash Join vs Merge Join vs Nested Loop
