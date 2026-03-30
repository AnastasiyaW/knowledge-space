---
title: PostgreSQL Table Partitioning
category: concepts
tags: [postgresql, partitioning, declarative, range, list, hash, partition-pruning, citus, sharding]
---

# PostgreSQL Table Partitioning

Partitioning splits a large table into smaller physical pieces (partitions) while presenting a single logical table. It improves query performance through partition pruning, simplifies maintenance (VACUUM, backups per partition), and enables efficient data lifecycle management.

## Key Facts

- **Declarative partitioning** (PostgreSQL 10+) - native PARTITION BY syntax. Supports RANGE, LIST, HASH (PG 11+)
- **RANGE** partitioning - by continuous ranges (dates, IDs). Most common for time-series data
- **LIST** partitioning - by discrete values (region, status, category)
- **HASH** partitioning (PG 11+) - by hash of column value. Even data distribution when no natural range exists
- **Partition pruning** - optimizer skips partitions that cannot contain matching rows. Enabled by default (`enable_partition_pruning = on`)
- **Sub-partitioning** - partitions can be further partitioned (e.g., RANGE by year, then LIST by region)
- **Citus** - extension for distributed PostgreSQL. Shards tables across multiple nodes. Used for horizontal scaling beyond single-server capacity
- See [[indexes-and-btree]] for indexing strategies on partitioned tables
- See [[postgresql-vacuum-and-mvcc]] for per-partition VACUUM benefits

## Patterns

### Range partitioning (time-series)

```sql
-- Create partitioned table
CREATE TABLE events (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    event_time TIMESTAMPTZ NOT NULL,
    event_type TEXT NOT NULL,
    payload JSONB
) PARTITION BY RANGE (event_time);

-- Create partitions
CREATE TABLE events_2024_q1 PARTITION OF events
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');
CREATE TABLE events_2024_q2 PARTITION OF events
    FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');
CREATE TABLE events_2024_q3 PARTITION OF events
    FOR VALUES FROM ('2024-07-01') TO ('2024-10-01');
CREATE TABLE events_2024_q4 PARTITION OF events
    FOR VALUES FROM ('2024-10-01') TO ('2025-01-01');

-- Default partition (catches rows not matching any partition)
CREATE TABLE events_default PARTITION OF events DEFAULT;

-- Indexes are created per partition
CREATE INDEX ON events (event_time);  -- creates index on each partition

-- Query with partition pruning (only scans relevant partition)
SELECT * FROM events WHERE event_time >= '2024-07-01' AND event_time < '2024-08-01';
```

### List partitioning

```sql
CREATE TABLE sales (
    id SERIAL,
    region TEXT NOT NULL,
    amount NUMERIC(10,2),
    sale_date DATE
) PARTITION BY LIST (region);

CREATE TABLE sales_us PARTITION OF sales FOR VALUES IN ('us-east', 'us-west');
CREATE TABLE sales_eu PARTITION OF sales FOR VALUES IN ('eu-west', 'eu-central');
CREATE TABLE sales_asia PARTITION OF sales FOR VALUES IN ('asia-east', 'asia-south');
CREATE TABLE sales_other PARTITION OF sales DEFAULT;
```

### Automated partition management

```sql
-- pg_partman extension for automatic partition creation
CREATE EXTENSION pg_partman;

SELECT partman.create_parent(
    p_parent_table := 'public.events',
    p_control := 'event_time',
    p_type := 'native',
    p_interval := 'monthly',
    p_premake := 3                    -- create 3 future partitions
);

-- Run maintenance periodically (cron or pg_cron)
SELECT partman.run_maintenance();

-- Drop old partitions (data lifecycle)
-- Detach partition (instant, non-blocking)
ALTER TABLE events DETACH PARTITION events_2023_q1;
-- Then DROP or archive at leisure
DROP TABLE events_2023_q1;
```

### Citus distributed tables

```sql
-- Citus extension for horizontal sharding
CREATE EXTENSION citus;

-- Distribute table across nodes
SELECT create_distributed_table('orders', 'customer_id');

-- Queries automatically routed to correct shard
SELECT * FROM orders WHERE customer_id = 42;  -- single-shard query (fast)

-- Cross-shard queries (slower, requires coordination)
SELECT customer_id, SUM(total) FROM orders GROUP BY customer_id;

-- Reference tables (replicated to all nodes, for JOINs)
SELECT create_reference_table('countries');
```

## Gotchas

- **No global unique index** - unique constraints on partitioned tables must include the partition key. `CREATE UNIQUE INDEX ON events (id)` fails; must be `(id, event_time)`
- **Partition creation is not automatic** - unlike MySQL, PostgreSQL requires manual partition creation or use of pg_partman. Inserting into a range with no matching partition causes an error (unless DEFAULT partition exists)
- **Foreign keys TO partitioned tables** - not supported until PostgreSQL 12. FK FROM partitioned table to regular table works fine
- **Partition pruning requires literal values** - `WHERE event_time = $1` with a parameter may not prune at plan time; runtime pruning (PG 11+) handles this, but verify with EXPLAIN
- **Too many partitions** - each partition has overhead (file descriptors, planner time). Hundreds of partitions is fine; thousands can degrade planning time
- **Moving rows between partitions** - UPDATE that changes the partition key column moves the row to the correct partition (PG 11+). Before PG 11, this was an error

## See Also

- [[indexes-and-btree]] - per-partition index strategies
- [[query-optimization-explain]] - verifying partition pruning in EXPLAIN output
- [PostgreSQL partitioning](https://www.postgresql.org/docs/current/ddl-partitioning.html)
- [pg_partman docs](https://github.com/pgpartman/pg_partman)
- [Citus docs](https://docs.citusdata.com/)
