---
title: SELECT Fundamentals
category: concepts
tags: [sql-databases, select, where, filtering, sorting, pagination]
---

# SELECT Fundamentals

The SELECT statement is the foundation of SQL data retrieval. It supports column selection, filtering, sorting, and pagination, and its execution order differs from its written syntax order.

## SQL Execution Order

Written order: SELECT - FROM - WHERE - GROUP BY - HAVING - ORDER BY - LIMIT. Actual execution order: FROM/JOIN - WHERE - GROUP BY - HAVING - SELECT - ORDER BY - LIMIT. Knowing this helps write efficient queries - filter early (WHERE) before aggregating (GROUP BY).

## Basic Column Selection

```sql
SELECT * FROM users;                           -- all columns (avoid in production)
SELECT firstname, lastname FROM users;         -- specific columns
SELECT firstname AS name, lastname AS surname FROM users;  -- aliases
SELECT DISTINCT city FROM users;               -- unique values only
SELECT DISTINCT ON (department) * FROM employees ORDER BY department, salary DESC;  -- PG only
```

## WHERE Clause Filtering

```sql
-- Comparison: =, !=, <>, <, >, <=, >=
SELECT * FROM city WHERE Population > 1000000;

-- Logical: AND, OR, NOT
SELECT * FROM city WHERE CountryCode = 'RUS' AND Population > 1000000;

-- Range: BETWEEN (inclusive both ends)
SELECT * FROM city WHERE Population BETWEEN 500000 AND 1000000;

-- Set membership: IN
SELECT * FROM city WHERE District IN ('Moscow', 'St Petersburg');

-- Pattern matching: LIKE
SELECT * FROM city WHERE Name LIKE 'Mos%';     -- starts with 'Mos'
SELECT * FROM city WHERE Name LIKE '%ow';      -- ends with 'ow'
SELECT * FROM city WHERE Name LIKE '_os%';     -- second char 'o', third 's'
-- MySQL: LIKE is case-insensitive by default
-- PostgreSQL: LIKE is case-sensitive; use ILIKE for case-insensitive

-- NULL checks (never use = NULL)
SELECT * FROM country WHERE IndepYear IS NULL;
SELECT * FROM country WHERE IndepYear IS NOT NULL;
```

## NULL Handling

NULL represents unknown/missing data - not a value itself. SQL uses three-valued logic: TRUE, FALSE, UNKNOWN. Any comparison with NULL yields UNKNOWN.

```sql
-- COALESCE: returns first non-NULL argument
SELECT name, COALESCE(country, 'Unknown') AS country FROM band;

-- NULLIF: returns NULL if two arguments are equal (avoid division by zero)
SELECT score / NULLIF(attempts, 0) FROM results;
```

**Key behaviors**: `NULL = NULL` is UNKNOWN (not TRUE). COUNT(*) counts all rows; COUNT(column) excludes NULLs. SUM, AVG, MIN, MAX all ignore NULLs. GROUP BY treats all NULLs as one group. NOT IN with NULL subquery values returns empty result - use NOT EXISTS instead.

## Sorting and Pagination

```sql
SELECT * FROM users ORDER BY lastname ASC, firstname DESC;
SELECT * FROM users ORDER BY created_at DESC LIMIT 10;
SELECT * FROM users LIMIT 10 OFFSET 20;  -- skip 20, take 10
```

### Pagination Performance

OFFSET-based pagination degrades linearly: `LIMIT 10 OFFSET 1000000` scans and discards 1M rows. Keyset (cursor) pagination is O(1) when indexed:

```sql
-- Instead of OFFSET:
SELECT * FROM posts WHERE id < :last_seen_id ORDER BY id DESC LIMIT 10;
```

Limitation: cannot jump to arbitrary page, only "next"/"previous". Acceptable for infinite scroll, not for "page 47 of 200".

## Computed Fields

```sql
-- Arithmetic
SELECT Name, Population / SurfaceArea AS density FROM country;

-- String concatenation
SELECT CONCAT(Name, ' (', Code, ')') AS info FROM country;        -- MySQL
SELECT Name || ' (' || Code || ')' AS info FROM country;           -- PostgreSQL

-- CASE expression
SELECT Name, Population,
  CASE
    WHEN Population > 1000000000 THEN 'Billion+'
    WHEN Population > 100000000 THEN '100M+'
    ELSE 'Under 100M'
  END AS size
FROM country;
```

## Gotchas

- `SELECT *` kills index-only scans, increases deserialization cost, pulls TOAST data, and silently degrades when columns are added
- LIKE patterns starting with `%` cannot use B-tree indexes
- NOT IN with NULLs in subquery returns zero rows - always add `WHERE col IS NOT NULL` or use NOT EXISTS
- ORDER BY on non-indexed columns requires a sort operation (check EXPLAIN for Sort nodes)
- MySQL `LIMIT offset, count` syntax has the offset first, unlike standard `LIMIT count OFFSET offset`

## See Also

- [[joins-and-set-operations]] - combining data from multiple tables
- [[aggregate-functions-grouping]] - COUNT, SUM, GROUP BY, HAVING
- [[subqueries-and-ctes]] - nested queries and CTEs
- [[query-optimization-explain]] - understanding execution plans
