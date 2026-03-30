---
title: PostgreSQL for Data Engineering
category: concepts
tags: [postgresql, postgres, sql, indexes, partitioning, plpgsql, transactions]
---

# PostgreSQL for Data Engineering

PostgreSQL is a powerful open-source relational database widely used as an OLTP backend, staging database, and metadata store in data engineering. Understanding its indexing, partitioning, query optimization, and procedural capabilities is essential for DE work.

## Key Facts

- Row-oriented storage (HEAP): every query reads full rows even if only one column is needed. For analytical workloads, consider [[clickhouse]] or columnar extensions
- **ACID transactions**: full support with MVCC (Multi-Version Concurrency Control). Each transaction sees a consistent snapshot without blocking readers
- **Index types**: B-tree (default, range queries), Hash (equality only), GiST (geometric, full-text), GIN (arrays, JSONB, full-text), BRIN (block range, large sorted tables)
- **Table partitioning** (native since PG 10): splits large tables into smaller physical pieces. Strategies:
  - `RANGE` - by date ranges (most common for time-series)
  - `LIST` - by discrete values (region, status)
  - `HASH` - by hash of a column (uniform distribution)
- **Explain plan**: `EXPLAIN (ANALYZE, BUFFERS)` shows actual execution plan with timing and I/O stats. Key nodes: Seq Scan, Index Scan, Hash Join, Nested Loop, Sort, Aggregate
- **PL/pgSQL**: procedural language for stored functions and triggers. Supports variables, loops, conditionals, exception handling
- **COPY** command for bulk data loading (10-100x faster than row-by-row INSERT). `\copy` is client-side variant
- **Materialized views**: precomputed query results stored as a table. `REFRESH MATERIALIZED VIEW CONCURRENTLY` updates without locking reads

## Patterns

### Partitioned table

```sql
CREATE TABLE events (
    event_id    BIGSERIAL,
    event_time  TIMESTAMPTZ NOT NULL,
    user_id     INT,
    event_type  VARCHAR(50),
    payload     JSONB
) PARTITION BY RANGE (event_time);

CREATE TABLE events_2026_03 PARTITION OF events
    FOR VALUES FROM ('2026-03-01') TO ('2026-04-01');

CREATE TABLE events_2026_04 PARTITION OF events
    FOR VALUES FROM ('2026-04-01') TO ('2026-05-01');

-- Queries with event_time filter automatically prune partitions
```

### Bulk loading with COPY

```sql
COPY staging_orders FROM '/data/orders.csv'
    WITH (FORMAT csv, HEADER true, DELIMITER ',', NULL '');

-- From Python (psycopg2)
with open('data.csv', 'r') as f:
    cursor.copy_expert("COPY staging_orders FROM STDIN WITH CSV HEADER", f)
```

### Query optimization checklist

```sql
-- 1. Read the plan
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
    SELECT * FROM events WHERE user_id = 123 AND event_time > '2026-03-01';

-- 2. Add index if Seq Scan on filtered column
CREATE INDEX CONCURRENTLY idx_events_user ON events (user_id);

-- 3. Use partial index for hot queries
CREATE INDEX idx_active_users ON users (email) WHERE is_active = TRUE;

-- 4. Use BRIN for naturally ordered large tables
CREATE INDEX idx_events_time_brin ON events USING BRIN (event_time);
```

### MERGE (upsert, PG 15+)

```sql
MERGE INTO dim_customer AS target
USING staging_customer AS source ON target.customer_id = source.customer_id
WHEN MATCHED THEN UPDATE SET name = source.name, segment = source.segment
WHEN NOT MATCHED THEN INSERT (customer_id, name, segment)
    VALUES (source.customer_id, source.name, source.segment);
```

## Gotchas

- `VACUUM` is critical for PostgreSQL health. Dead tuples from updates/deletes consume space and slow queries. Autovacuum handles this, but heavy write tables may need manual VACUUM tuning
- Indexes on partitioned tables must include the partition key. Global indexes are not supported in native partitioning
- `EXPLAIN ANALYZE` actually executes the query (including writes!). Use `BEGIN; EXPLAIN ANALYZE ...; ROLLBACK;` for destructive queries
- `ORDER BY` on unindexed columns triggers full sort in memory/disk. For large result sets, ensure an appropriate index exists or accept the sort cost
- JSONB indexing: use GIN index for `@>` (containment) queries. Do NOT rely on B-tree for JSONB columns
- `fetchall()` in Python loads entire result set into memory. For large queries, use `fetchmany(batch_size)` or server-side cursors

## See Also

- [[normalization]] - schema design for OLTP
- [[data-modeling]] - dimensional modeling on PostgreSQL
- [[partitioning-and-sharding]] - physical data distribution strategies
- https://www.postgresql.org/docs/current/ - PostgreSQL documentation
