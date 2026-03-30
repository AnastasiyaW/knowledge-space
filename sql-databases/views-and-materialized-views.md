---
title: Views and Materialized Views
category: syntax
tags: [sql, view, materialized-view, updatable-view, security, postgresql, mysql]
---

# Views and Materialized Views

Views are named queries stored in the database. Regular views execute the underlying query on each access. Materialized views store the query result physically, trading freshness for read performance.

## Key Facts

- **Regular view** - stored query definition, no data stored. Executed on each SELECT. Always returns current data
- **Materialized view** (PostgreSQL) - stores query result on disk. Must be refreshed explicitly. Has indexes. MySQL does NOT have native materialized views
- **Updatable views** - simple views (single table, no aggregates, no DISTINCT, no GROUP BY) can accept INSERT/UPDATE/DELETE in both PostgreSQL and MySQL
- **Security barrier views** (PostgreSQL) - prevents information leakage through optimizer reordering. Use `WITH (security_barrier)` for row-level security
- **WITH CHECK OPTION** - prevents INSERT/UPDATE through a view that would make the row invisible to the view
- See [[query-optimization-explain]] for how the planner handles views
- See [[common-table-expressions]] for inline named queries within a single statement

## Patterns

### Regular views

```sql
-- Create view
CREATE VIEW active_users AS
SELECT id, name, email, last_login
FROM users
WHERE status = 'active';

-- Use like a table
SELECT * FROM active_users WHERE last_login > now() - INTERVAL '7 days';

-- Replace view definition
CREATE OR REPLACE VIEW active_users AS
SELECT id, name, email, last_login, department
FROM users
WHERE status = 'active';

-- Updatable view with check option
CREATE VIEW premium_products AS
SELECT * FROM products WHERE price > 100
WITH CASCADED CHECK OPTION;
-- Prevents: INSERT INTO premium_products VALUES (..., 50);  -- price < 100 rejected
```

### Materialized views (PostgreSQL)

```sql
-- Create materialized view
CREATE MATERIALIZED VIEW monthly_sales_summary AS
SELECT date_trunc('month', sale_date) AS month,
       category,
       COUNT(*) AS num_sales,
       SUM(amount) AS total_amount,
       AVG(amount) AS avg_amount
FROM sales
GROUP BY 1, 2;

-- Add indexes on materialized view
CREATE INDEX idx_mvsales_month ON monthly_sales_summary (month);
CREATE INDEX idx_mvsales_category ON monthly_sales_summary (category);

-- Refresh (blocks reads during refresh)
REFRESH MATERIALIZED VIEW monthly_sales_summary;

-- Concurrent refresh (allows reads during refresh, requires unique index)
CREATE UNIQUE INDEX idx_mvsales_unique ON monthly_sales_summary (month, category);
REFRESH MATERIALIZED VIEW CONCURRENTLY monthly_sales_summary;

-- Check when last refreshed
SELECT relname, last_refresh
FROM pg_matviews
JOIN pg_stat_user_tables ON matviewname = relname
WHERE schemaname = 'public';
```

### Simulating materialized views in MySQL

```sql
-- MySQL: use a regular table + scheduled refresh
CREATE TABLE monthly_sales_summary AS
SELECT DATE_FORMAT(sale_date, '%Y-%m-01') AS month,
       category, COUNT(*) AS num_sales, SUM(amount) AS total_amount
FROM sales
GROUP BY 1, 2;

-- Refresh via scheduled event
CREATE EVENT refresh_sales_summary
ON SCHEDULE EVERY 1 HOUR
DO
BEGIN
    TRUNCATE TABLE monthly_sales_summary;
    INSERT INTO monthly_sales_summary
    SELECT DATE_FORMAT(sale_date, '%Y-%m-01'), category, COUNT(*), SUM(amount)
    FROM sales GROUP BY 1, 2;
END;
```

### Security views

```sql
-- PostgreSQL: security barrier view prevents filter pushdown attacks
CREATE VIEW user_data WITH (security_barrier) AS
SELECT id, name, email FROM users
WHERE tenant_id = current_setting('app.tenant_id')::int;

-- Without security_barrier, a malicious function in WHERE could
-- leak data from rows outside the view's filter
```

## Gotchas

- **View performance** - regular views are NOT cached; the underlying query runs every time. Complex views on large tables are slow. Consider materialized views for expensive aggregations
- **Materialized view refresh is expensive** - REFRESH rewrites the entire materialized view. For large datasets, CONCURRENTLY is essential but requires a unique index
- **MySQL no native MVIEW** - must simulate with tables + events/cron. No CONCURRENTLY refresh equivalent
- **View dependency chains** - dropping a table referenced by a view requires CASCADE. Views referencing other views create chains that are hard to manage
- **Updatable view limitations** - views with JOINs, aggregates, DISTINCT, UNION are not updatable. PostgreSQL supports INSTEAD OF triggers for complex updatable views
- **Stale materialized views** - applications reading from materialized views may see stale data. Design refresh strategy based on acceptable staleness

## See Also

- [[common-table-expressions]] - inline temporary named queries
- [[query-optimization-explain]] - how views are expanded in execution plans
- [PostgreSQL CREATE VIEW](https://www.postgresql.org/docs/current/sql-createview.html)
- [PostgreSQL CREATE MATERIALIZED VIEW](https://www.postgresql.org/docs/current/sql-creatematerializedview.html)
- [MySQL CREATE VIEW](https://dev.mysql.com/doc/refman/8.0/en/create-view.html)
