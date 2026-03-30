---
title: Caching Strategies
category: patterns
tags: [cache, redis, performance, data-access]
---
# Caching Strategies

Caching stores frequently accessed data in fast storage (typically in-memory) to reduce latency and backend load. Strategy selection depends on read/write ratio, consistency requirements, and data access patterns.

## Key Facts

- Caching is one of the highest-impact optimizations: L1 cache = 0.5ns vs HDD = 10ms (20 million times slower)
- Redis is the most popular in-memory cache; single-threaded but handles ~100K ops/sec per instance
- Redis documentation uses terms loosely (e.g., "transactions" in Redis are not ACID transactions) - verify behavior against your consistency needs
- Cache invalidation is one of the two hard problems in CS (Phil Karlton)
- For distributed applications with multiple instances, externalize session storage to Redis/Hazelcast rather than using sticky sessions
- See [[quality-attributes]] for latency requirements that drive caching decisions
- See [[database-selection]] for when to use in-memory databases vs caches

## Patterns

### Read strategies

```
Cache-Aside (Lazy Loading):
  1. App checks cache
  2. Cache miss -> read from DB
  3. App writes to cache
  4. Return data
  + Simple, only caches what's needed
  - Cache miss penalty (extra round trip)
  - Data can become stale

Read-Through:
  1. App reads from cache
  2. Cache miss -> cache itself reads from DB
  3. Cache stores and returns
  + Cache manages DB reads (simpler app code)
  - Same staleness issues as cache-aside

Refresh-Ahead:
  1. Cache proactively refreshes entries BEFORE expiry
  2. Predicts which entries will be needed
  + Eliminates cache miss latency for hot data
  - Wasted refreshes for unused entries
  - This is an improved version of cache-aside, NOT write-through
```

### Write strategies

```
Write-Through:
  1. App writes to cache
  2. Cache synchronously writes to DB
  3. Return success
  + Data always consistent between cache and DB
  - Write latency increased (2 writes per operation)
  - Every write cached, even if never read

Write-Behind (Write-Back):
  1. App writes to cache
  2. Cache asynchronously writes to DB (batch/delayed)
  3. Return success immediately
  + Lowest write latency
  + Batching reduces DB load
  - Data loss risk if cache crashes before flush
  - Complexity in failure handling

Write-Around:
  1. App writes directly to DB (skips cache)
  2. Cache populated only on reads
  + No write overhead on cache
  - First read after write is always a cache miss
```

### Session externalization pattern

```
Problem: Multiple app instances with local sessions
  Instance 1: session[user_A] = {...}
  Instance 2: session[user_B] = {...}
  -> Load balancer must use sticky sessions
  -> Instance crash loses all its sessions

Solution: External session store
  Instance 1 --\
  Instance 2 ---+--> Redis/Hazelcast session store
  Instance 3 --/
  -> Any instance serves any user
  -> Instance crash loses nothing
  -> Most web frameworks support this natively
```

### Cache eviction policies

```
LRU  (Least Recently Used)  - best general purpose
LFU  (Least Frequently Used) - good for stable hot sets
FIFO (First In First Out)   - simplest, rarely optimal
TTL  (Time To Live)         - time-based expiry
```

## Gotchas

- **Symptom**: Cache hit rate < 50% -> **Cause**: Cache size too small for working set, or random access pattern -> **Fix**: Monitor cache hit/miss ratio; increase memory or switch to more selective caching (only hot data)
- **Symptom**: Thundering herd after cache expiry -> **Cause**: Many requests hit expired key simultaneously, all go to DB -> **Fix**: Use cache stampede protection: lock-based refresh (only one request refreshes, others wait) or probabilistic early expiration
- **Symptom**: Stale data served indefinitely -> **Cause**: Write-around strategy with no TTL and no invalidation -> **Fix**: Always set TTL even if you also have explicit invalidation; TTL is your safety net
- **Symptom**: Redis memory grows unbounded -> **Cause**: No eviction policy configured, keys never expire -> **Fix**: Configure `maxmemory-policy` (allkeys-lru recommended) and set TTL on all keys

## See Also

- [[database-selection]] - When to use Redis as primary store vs cache
- [[quality-attributes]] - Latency requirements driving cache decisions
- [[load-balancing]] - Sticky sessions vs externalized state
- [[distributed-system-patterns]] - Cache-aside in distributed context
- Redis: [Eviction Policies](https://redis.io/docs/reference/eviction/)
- Martin Fowler: [Two Hard Things](https://martinfowler.com/bliki/TwoHardThings.html)
