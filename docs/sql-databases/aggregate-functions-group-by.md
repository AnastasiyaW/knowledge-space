---
title: Aggregate Functions and GROUP BY
category: concepts
tags: [sql-databases, sql, aggregation, group-by, having, count, sum, avg]
---

# Aggregate Functions and GROUP BY

Aggregate functions collapse multiple rows into single summary values. GROUP BY partitions rows into groups before aggregation, while HAVING filters the resulting groups.

## Key Facts

- `COUNT(*)` counts all rows including NULLs; `COUNT(column)` counts non-NULL values only
- `SUM`, `AVG`, `MIN`, `MAX` all ignore NULLs
- `GROUP BY` treats all NULLs as one group
- HAVING filters groups after aggregation; WHERE filters rows before grouping
- Cannot use aggregate functions in WHERE clause

## Patterns

### Basic Aggregation
```sql
SELECT COUNT(*) FROM users;
SELECT COUNT(DISTINCT city) FROM users;
SELECT SUM(amount), AVG(amount), MIN(amount), MAX(amount) FROM orders;
```

### GROUP BY
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

### HAVING (Filter on Aggregated Results)
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

### COUNT Performance on Large Tables

`SELECT COUNT(*) FROM large_table` requires full table/index scan - MVCC means different transactions see different row counts.

**Alternatives for approximate counts:**
```sql
-- PostgreSQL: approximate from statistics
SELECT reltuples::bigint FROM pg_class WHERE relname = 'large_table';

-- MySQL: approximate from information_schema
SELECT table_rows FROM information_schema.tables
WHERE table_name = 'large_table';
```

Other strategies: materialized count table updated by triggers, Redis counter incremented on INSERT/DELETE, HyperLogLog for distinct count approximation.

## Gotchas

- `AVG` ignores NULLs - `AVG` of `[10, NULL, 20]` is 15, not 10
- Columns in SELECT must either appear in GROUP BY or be inside aggregate functions
- `COUNT(DISTINCT col)` is slower than `COUNT(*)` - requires deduplication
- MySQL allows non-aggregated columns in SELECT without GROUP BY (sql_mode dependent) - PostgreSQL does not

## See Also

- [[select-fundamentals]] - WHERE clause and basic filtering
- [[window-functions]] - aggregations without collapsing rows
- [[query-optimization-explain]] - optimizing aggregate queries
