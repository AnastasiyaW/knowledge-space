---
title: Distributed SQL Databases
category: concepts
tags: [sql-databases, distributed, cockroachdb, citus, greenplum, yugabytedb, mpp, olap, sharding]
---

# Distributed SQL Databases

When single-server PostgreSQL reaches its limits, distributed databases provide horizontal scaling. Each has different trade-offs between consistency, complexity, and workload suitability.

## Comparison

| Feature | Citus | CockroachDB | Greenplum | YugabyteDB |
|---------|-------|-------------|-----------|------------|
| Base | PG extension | Custom (PG wire) | PG fork | Custom (PG wire) |
| Consistency | Per-shard | Serializable | Per-segment | Serializable |
| Best for | Multi-tenant SaaS | Geo-distributed OLTP | Analytics/DWH | Distributed OLTP |
| OLTP | Good | Good | Poor | Good |
| OLAP | Good | Moderate | Excellent | Moderate |
| Complexity | Low (extension) | Medium | High (separate product) | Medium |

## Citus (PostgreSQL Extension)

Acquired by Microsoft (2019). Transforms single PostgreSQL into distributed database.

### Table Types
- **Distributed:** Hash-sharded across workers by distribution column
- **Reference:** Replicated to all workers (dimension/lookup tables)
- **Local:** On coordinator only

```sql
-- Create distributed table
SELECT create_distributed_table('events', 'tenant_id');

-- Queries automatically routed to relevant shard
SELECT count(*) FROM events WHERE tenant_id = 42;

-- Cross-shard queries supported but slower
SELECT tenant_id, count(*) FROM events GROUP BY tenant_id;
```

**Since Citus 11.0:** Queries can run from any node. `citus.shard_replication_factor` default 1 (no fault tolerance).

## CockroachDB

PostgreSQL-compatible distributed SQL. Multi-master, automatic sharding, serializable isolation.

```bash
# 3-node cluster
cockroach start --certs-dir=certs --advertise-addr=node1 --join=node1,node2,node3
cockroach init --certs-dir=certs --host=node1
```

Geo-distributed: 9 nodes across 3 regions. Requires time sync (500ms drift tolerance). Multi-master: writes on any region visible on all others.

## Greenplum MPP

Open-source MPP RDBMS based on PostgreSQL. Columnar storage, massively parallel processing.

### Architecture
- **Master host:** Entry point, SQL coordinator, no user data
- **Segment hosts:** 2-8 PostgreSQL segments per host, primary + mirror
- **Interconnect:** Dedicated high-speed network

### Storage Types

| Type | Best For |
|------|----------|
| Heap | Concurrent UPDATE/DELETE/INSERT |
| Append-Optimized (AO) | Batch loads + analytics, rarely updated |
| Row-oriented | Wide SELECT, mixed workloads |
| Column-oriented | Narrow SELECT on wide tables, aggregations |

### Performance Rules
- Speed = CPU cores / data ratio per node
- 1 query = max 1 core per segment
- Cluster speed = slowest segment - balanced distribution critical
- Design insert-only model; truncate daily partition before loading

## OLTP vs OLAP

**OLTP:** Normalized, high insert/update rate, many concurrent users, small transactions, indexed for fast access. Three-tier architecture.

**OLAP:** Historical data reports, columnar storage, denormalized fact tables with dimensions, infrequent updates, fast aggregation reads.

## MPP (Massive Parallel Processing)

Data and compute distributed across leader + worker nodes. Shared-nothing architecture.

**Pros:** Fast large-data processing, easy horizontal scaling, fault tolerance via mirroring.
**Cons:** High resource requirements, poor for many simple queries, segment distribution imbalance.

## ClickHouse

Column-oriented OLAP database (C++, Yandex). Vectorized query processing, efficient compression, built-in replication/sharding. Rich SQL dialect with JSON, IP, UUID, Array types. Integration with Kafka, MySQL, PostgreSQL.

## Other Solutions

- **YugabyteDB:** PG-compatible distributed SQL with serializable isolation
- **Postgres-BDR / Bucardo:** Multi-master using logical replication
- **Shardman (Postgres Pro):** FDW-based sharding, hash-only distribution, significant limitations
- **Arenadata DB:** Russian commercial Greenplum distribution

## Key Facts

- PostgreSQL is NOT designed for big data: transactions/WAL impede large operations, no built-in sharding
- Citus is the simplest path from single PostgreSQL to distributed
- CockroachDB provides strongest consistency (serializable) across distributed nodes
- Greenplum excels at analytics but is poor for OLTP
- Sharding key must have high cardinality and uniform distribution

## Gotchas

- Citus: `shard_replication_factor = 1` (default) means no fault tolerance for individual shards
- CockroachDB: 500ms time drift tolerance - NTP synchronization required
- Greenplum: 1 core per query per segment limits fine-grained query parallelism
- Shardman: no ALTER TABLE (except owner/NULL/ADD column), no foreign keys, SELECT-only transport
- Multi-master replication has complex conflict resolution - avoid unless truly needed

## See Also

- [[partitioning-and-sharding]] - single-server partitioning and sharding concepts
- [[replication-fundamentals]] - streaming replication as simpler alternative
- [[postgresql-ha-patroni]] - HA without distribution
- [[caching-redis-memcached]] - caching layer to reduce database load
