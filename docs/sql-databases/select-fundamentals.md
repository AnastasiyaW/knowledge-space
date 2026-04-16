---
title: SELECT Fundamentals
category: concepts
tags: [sql-databases, sql, select, where, order-by, limit, filtering, case]
---

# SELECT Fundamentals

The SELECT statement is the primary tool for reading data from relational databases. Mastering its clauses and execution order is essential for writing efficient queries.

## Query Execution Order

The logical processing order differs from written syntax:

```sql
FROM / JOIN  ->  WHERE  ->  GROUP BY  ->  HAVING  ->  SELECT  ->  DISTINCT  ->  ORDER BY  ->  LIMIT / OFFSET
```

This explains why column aliases work in ORDER BY but not in WHERE.

## Key Facts

- `SELECT *` is harmful in production - kills index-only scans, fetches TOAST data, increases network cost, unpredictable when columns added
- `DISTINCT` requires sorting/hashing - avoid when possible
- `LIMIT N OFFSET M` degrades linearly with M (scans and discards M rows)
- SQL keywords are case-insensitive; convention is UPPERCASE keywords, lowercase identifiers
- MySQL `LIKE` is case-insensitive by default; PostgreSQL `LIKE` is case-sensitive (use `ILIKE`)

## Patterns

### Basic Column Selection
```sql
SELECT * FROM users;
SELECT firstname, lastname FROM users;
SELECT firstname AS name, lastname AS surname FROM users;
SELECT DISTINCT city FROM users;
```

### WHERE Clause Filtering
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

### ORDER BY and LIMIT
```sql
SELECT * FROM users ORDER BY lastname ASC, firstname DESC;
SELECT * FROM users ORDER BY created_at DESC LIMIT 10;
SELECT * FROM users LIMIT 10 OFFSET 20;  -- skip 20, take 10
```

### Computed Fields and CASE
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

### Keyset Pagination (Alternative to OFFSET)
```sql
-- Instead of slow OFFSET:
SELECT * FROM posts WHERE id < :last_seen_id ORDER BY id DESC LIMIT 10;
-- Uses index, constant time regardless of "page number"
```

## Gotchas

- `OFFSET 10000 LIMIT 10` scans and discards 10,000 rows - use keyset pagination for large offsets
- `NULL` comparisons with `=` or `!=` always yield UNKNOWN (row excluded)
- `WHERE phone != '123'` does NOT return rows where phone IS NULL - add `OR phone IS NULL`
- Sorting by column position (`ORDER BY 2`) is valid but fragile - avoid in production
- Keyset pagination cannot jump to arbitrary page - only "next"/"previous"

## See Also

- [[aggregate-functions-group-by]] - COUNT, SUM, AVG with GROUP BY and HAVING
- [[joins-and-set-operations]] - combining data from multiple tables
- [[subqueries-and-ctes]] - nested queries and common table expressions
- [[window-functions]] - row-level calculations across partitions
