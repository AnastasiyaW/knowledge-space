---
title: Partitioning and Sharding
category: concepts
tags: [sql-databases, partitioning, sharding, consistent-hashing, horizontal-partitioning, postgresql, billion-rows]
---

# Partitioning and Sharding

Partitioning splits a large table into smaller physical segments on the same server. Sharding distributes data across multiple servers. Both are strategies for handling tables that grow beyond single-server capacity.

## Strategy Hierarchy (Prefer Simpler First)

1. **Redesign data model** - avoid the billion-row table entirely
2. **Indexing** - B-tree/LSM indexes to narrow search
3. **Partitioning** - split table on same server
4. **Sharding** - distribute across servers
5. **MapReduce** - brute-force parallel processing (last resort)

## Horizontal Partitioning

```sql
-- PostgreSQL: range partitioning
CREATE TABLE grades (id SERIAL NOT NULL, g INTEGER NOT NULL)
PARTITION BY RANGE (g);

CREATE TABLE g_00_35 PARTITION OF grades FOR VALUES FROM (0) TO (35);
CREATE TABLE g_35_60 PARTITION OF grades FOR VALUES FROM (35) TO (60);
CREATE TABLE g_60_80 PARTITION OF grades FOR VALUES FROM (60) TO (80);
CREATE TABLE g_80_100 PARTITION OF grades FOR VALUES FROM (80) TO (100);

-- Index on partitioned table (applies to all partitions)
CREATE INDEX g_idx ON grades (g);
```

### Partition Types

| Type | Key | Best For |
|------|-----|----------|
| Range | Date, ID ranges | Time-series, archival (DROP old partitions) |
| List | Discrete values (country, status) | Categorical data |
| Hash | Hash of column value | Even distribution regardless of patterns |
| Composite | Range + Hash | Date range then hash by user within range |

### Partition Pruning
```sql
-- EXPLAIN shows only relevant partition scanned
EXPLAIN ANALYZE SELECT count(*) FROM grades WHERE g = 30;
-- Scans only g_00_35 partition
```

### Vertical Partitioning
Split columns into separate tables. Frequently accessed columns in one table, large BLOBs/text in another. Reduces page size = more rows per page = fewer I/Os.

## Sharding

Distribute data across multiple database servers. Each shard has its own partitions and indexes.

### Consistent Hashing
```javascript
// Hash key to determine shard
const crypto = require('crypto');
const hash = crypto.createHash('md5').update(urlId).digest('hex');
const shardIndex = parseInt(hash.substring(0, 8), 16) % NUM_SHARDS;
```

Adding/removing shards only redistributes keys from adjacent shard (not all keys).

### Sharding Key Selection
Critical for balanced distribution. Bad example: sharding by language when 90% users speak English - one shard gets 10x load. Use high-cardinality keys with even distribution.

### Sharding Trade-offs

**Pros:** Horizontal scaling, smaller indexes per shard, security isolation, data locality.

**Cons:** Client routing complexity, cross-shard transactions (need 2PC or eventual consistency), cross-shard JOINs impossible in SQL, schema changes on all shards, hotspot shards.

## Key Facts

- Partition key MUST be included in primary key and unique constraints
- `pg_partman` extension automates partition creation and retention
- Sharding should be last resort - first try: read replicas, caching, pooling, optimization, partitioning
- Cross-partition queries scan ALL partitions (worse than unpartitioned if no pruning)
- Moving row between partitions (UPDATE on partition key) is expensive

## Gotchas

- Over-partitioning: too many partitions = metadata overhead, many small files
- PostgreSQL weak lock fast-path: 16 slots per backend - heavily partitioned queries can exceed this
- Unique constraints must include partition key in PostgreSQL
- Foreign keys referencing partitioned tables have limitations
- Resharding requires data migration and potential downtime
- Cross-shard aggregations (COUNT, SUM) require querying all shards and merging

## See Also

- [[btree-and-index-internals]] - index behavior with partitions
- [[distributed-databases]] - Citus, CockroachDB for automatic sharding
- [[query-optimization-explain]] - partition pruning in EXPLAIN
- [[database-storage-internals]] - page-level implications of partitioning
