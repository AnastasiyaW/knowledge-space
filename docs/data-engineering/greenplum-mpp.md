---
title: Greenplum and MPP Architecture
category: tools
tags: [data-engineering, greenplum, mpp, distributed-database, parallel-processing]
---

# Greenplum and MPP Architecture

Greenplum is an MPP (Massive Parallel Processing) analytical database based on PostgreSQL. It uses shared-nothing architecture where each node has its own CPU, memory, and disk.

## Architecture

```php
Client -> Master (QD: Query Dispatcher)
              |
    +---------+---------+
    Segment1  Segment2  Segment3  (QE: Query Executors)
    (mirror)  (mirror)  (mirror)
```

- **Master (QD):** accepts queries, builds plan, dispatches to segments, aggregates results. Does NOT store user data
- **Segments (QE):** store data, execute in parallel. Each is a PostgreSQL instance
- **Mirrors:** standby copies for fault tolerance

## Motion Operators

| Operator | What It Does | Cost |
|----------|-------------|------|
| **Redistribute Motion** | Reshuffle data by hash key | Expensive |
| **Broadcast Motion** | Full copy of small table to all segments | Medium |
| **Gather Motion** | Collect results to master | Light |

## Distribution Strategies

```sql
-- Hash distribution (best for JOIN keys)
CREATE TABLE orders (...) DISTRIBUTED BY (order_id);

-- Random (default)
CREATE TABLE logs (...) DISTRIBUTED RANDOMLY;

-- Replicated (small dimension tables)
CREATE TABLE countries (...) DISTRIBUTED REPLICATED;
```

### Key Optimization

Distribute both tables in a JOIN by the join key to eliminate Redistribute Motion:

```sql
ALTER TABLE lineitem SET DISTRIBUTED BY (l_orderkey);
ALTER TABLE orders SET DISTRIBUTED BY (o_orderkey);
-- Redistribute Motion disappears from EXPLAIN plan
```

## ANALYZE (Critical)

```sql
ANALYZE table_name;
```

**Always run ANALYZE after bulk data changes.** Greenplum optimizer depends on statistics. Without fresh stats after INSERT/UPDATE, optimizer uses stale estimates leading to suboptimal plans.

**PostgreSQL auto-analyzes reasonably. Greenplum does NOT - explicit ANALYZE required.**

## Greenplum vs PostgreSQL: Indexes

- PostgreSQL: create index -> optimizer uses it -> faster queries
- Greenplum: create index -> **optimizer ignores it** (prefers sequential scan across segments)

```sql
-- Force index usage (rarely needed)
SET seq_page_cost = 100;
SET random_page_cost = 1;
SET optimizer = off;  -- GPORCA ignores hints
```

In MPP, sequential scan across many segments is often faster than index lookup.

## Compression (TPC-H lineitem, scale=10)

| Storage | Size |
|---------|------|
| Row-oriented (default) | 34 GB |
| Row + compression | 11 GB |
| Columnar + compression | 7.5 GB |

## Table Types

| Type | Persistence | Logged | Visible |
|------|-----------|--------|---------|
| Permanent | Survives restart | Yes (WAL) | All sessions |
| Temporary | Session only | No | Current session |
| Unlogged | Survives session, lost on crash | No | All sessions |
| External | Data outside DB (S3, HDFS via PXF) | N/A | All sessions |

## Gotchas
- Indexes are rarely useful in Greenplum - sequential scan dominates
- ANALYZE must be run manually after bulk operations
- External tables have no statistics - optimizer estimates heuristically
- Network latency kills cross-datacenter cluster performance
- GPORCA optimizer ignores hints - must disable for index forcing

## See Also
- [[dwh-architecture]] - DWH design context
- [[cloud-data-platforms]] - modern alternatives (Snowflake, BigQuery)
- [[spark-optimization]] - similar distributed optimization concepts
