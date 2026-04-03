---
title: Caching - Redis and Memcached
category: concepts
tags: [sql-databases, redis, memcached, caching, cache-aside, write-through, lru, connection-cache]
---

# Caching - Redis and Memcached

Caching layers between application and database dramatically reduce query load. Redis and Memcached are the two dominant solutions with different trade-offs.

## Comparison

| Feature | Redis | Memcached |
|---------|-------|-----------|
| Data Structures | Strings, lists, sets, sorted sets, hashes, streams | Key-value strings only |
| Persistence | RDB snapshots + AOF | None (RAM only) |
| Threading | Single-threaded commands (I/O threads since 6.0) | Multi-threaded |
| Max Value Size | 512MB | 1MB |
| Pub/Sub | Yes | No |
| Replication | Master-replica | No built-in |
| Clustering | Hash slots (16384) | Client-side consistent hashing |

## Cache Patterns

**Cache-Aside (Lazy Loading):** App checks cache first. On miss, query DB, store in cache. Simple but first request always hits DB.

**Write-Through:** App writes to cache AND DB simultaneously. Cache always fresh but write latency increases.

**Write-Behind:** App writes to cache only. Cache asynchronously writes to DB. Fastest writes but risk of data loss if cache crashes.

**Cache Invalidation:** TTL-based (stale for TTL duration), event-based (invalidate on write), or versioning.

## Redis Durability

**RDB snapshots:** `save 900 1` (snapshot if 1+ keys changed in 900s). `BGSAVE` forks process, child writes while parent serves.

**AOF (Append-Only File):**
- `appendfsync always` - safest, slowest
- `appendfsync everysec` - good balance (lose max 1 second)
- `appendfsync no` - OS decides flush timing

**Hybrid (Redis 4.0+):** RDB + AOF of changes since snapshot. Fast restart + minimal data loss.

## Memcached Architecture

**Slab allocator:** Memory pre-divided into size classes (64B, 128B, 256B, ..., 1MB). Reduces fragmentation. Trade-off: internal fragmentation within chunks.

**LRU eviction:** Per-slab-class. When class full, evict least-recently-used item from THAT class.

**CAS (Compare-And-Swap):** `gets` returns CAS token, `cas` succeeds only if token unchanged. Prevents lost updates.

**Distributed:** Servers unaware of each other. Client implements consistent hashing. Adding server causes ~1/N keys to remap.

## Key Facts

- Redis as cache: `SETEX key ttl value` for TTL-based caching
- Redis Cluster: automatic sharding across nodes with 16384 hash slots
- Memcached: multi-threaded, better for simple key-value caching at scale
- Local cache requires sticky sessions from load balancer; shared cache adds network latency
- Cache hit ratio for popular URLs likely >80% (Pareto distribution)

## Gotchas

- Cache invalidation is the hardest problem - stale data can cause subtle bugs
- Redis single-threaded: one slow command blocks all other commands
- Memcached slab class imbalance: evicting 256B items can't free space for 64B items
- Redis persistence (RDB+AOF) is not equivalent to a real database backup
- Connection to cache adds network hop - only cache if DB query cost >> cache lookup cost
- Cache stampede: many concurrent misses for same key all hit DB simultaneously

## See Also

- [[connection-pooling]] - reducing database connections alongside caching
- [[query-optimization-explain]] - optimize queries before adding cache layer
- [[distributed-databases]] - when caching isn't enough
- [[database-security]] - separate credentials for cache and DB access
