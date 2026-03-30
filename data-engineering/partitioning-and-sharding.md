---
title: Partitioning and Sharding
category: concepts
tags: [partitioning, sharding, replication, distribution, scalability, performance]
---

# Partitioning and Sharding

Partitioning and sharding are strategies for distributing data across storage units to improve query performance, manageability, and scalability. Partitioning splits data within a single database; sharding distributes across multiple database instances.

## Key Facts

- **Partitioning** (single-node): divides a table into smaller physical segments based on a partition key. The database engine routes queries to relevant partitions automatically (partition pruning)
  - **Range partitioning**: by continuous ranges (date, ID ranges). Most common for time-series data
  - **List partitioning**: by discrete values (region, category, status)
  - **Hash partitioning**: by hash(key) % N. Ensures uniform distribution but breaks range queries
- **Sharding** (multi-node): distributes data across separate database instances. Each shard is an independent database. Used when a single node cannot handle the load
  - Application-level sharding: routing logic in the application
  - Database-level sharding: [[greenplum-and-mpp]] handles distribution transparently
- **Replication**: copying data to multiple nodes for fault tolerance and read scaling
  - Synchronous: write confirmed only after all replicas acknowledge (stronger consistency, higher latency)
  - Asynchronous: write confirmed after primary acknowledges; replicas catch up later (lower latency, risk of stale reads)
- **Partition key selection** is critical: queries that don't filter on partition key scan ALL partitions (worse than no partitioning)
- HDFS inherently shards data by blocks across DataNodes (see [[hdfs]])
- [[clickhouse]] uses `PARTITION BY` at table creation level; partitions affect data merging and TTL deletion

## Patterns

### PostgreSQL range partitioning

```sql
CREATE TABLE events (
    event_id    BIGINT,
    event_time  TIMESTAMPTZ NOT NULL,
    data        JSONB
) PARTITION BY RANGE (event_time);

-- Monthly partitions
CREATE TABLE events_2026_01 PARTITION OF events
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
CREATE TABLE events_2026_02 PARTITION OF events
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');

-- Auto-creation via pg_partman extension
CREATE EXTENSION pg_partman;
SELECT partman.create_parent('public.events', 'event_time', 'native', 'monthly');
```

### Spark output partitioning

```python
# Write partitioned by date and region
df.write \
    .mode("overwrite") \
    .partitionBy("dt", "region") \
    .parquet("s3://bucket/events/")

# Results in directory structure:
# s3://bucket/events/dt=2026-03-30/region=us/part-00000.parquet
# s3://bucket/events/dt=2026-03-30/region=eu/part-00000.parquet
```

### ClickHouse partitioning with TTL

```sql
CREATE TABLE logs (
    log_date Date,
    level    String,
    message  String
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(log_date)
ORDER BY (log_date, level)
TTL log_date + INTERVAL 6 MONTH;  -- auto-delete old partitions
```

### Greenplum distribution (sharding)

```sql
-- Hash distribution across segments
CREATE TABLE sales DISTRIBUTED BY (customer_id);

-- Replicated (small dimension table)
CREATE TABLE dim_region DISTRIBUTED REPLICATED;
```

## Gotchas

- Partitioning without filtering on partition key is WORSE than no partitioning: more files to open, more metadata to manage, no pruning benefit
- Over-partitioning creates too many small files/partitions. Rule of thumb: each partition should hold at least 100 MB - 1 GB of data
- In Spark, `partitionBy("high_cardinality_column")` with millions of distinct values creates millions of tiny files. Use `repartition()` or bucketing instead
- Hash partitioning prevents efficient range queries. If most queries filter by date range, use range partitioning on date
- Sharding (cross-node) makes JOINs expensive: data must be redistributed over the network. Co-locate (shard on same key) tables that are frequently joined
- Replication factor does not improve write performance - it increases write amplification. Higher RF = more durable but slower writes

## See Also

- [[postgresql-for-data-engineering]] - PG native partitioning
- [[clickhouse]] - PARTITION BY in MergeTree
- [[greenplum-and-mpp]] - distributed tables
- [[hdfs]] - block-level data distribution
- https://www.postgresql.org/docs/current/ddl-partitioning.html
