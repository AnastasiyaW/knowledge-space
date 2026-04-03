---
title: Caching Strategies and Performance
category: reference
tags: [caching, redis, memcached, cdn, performance, load-balancing]
---

# Caching Strategies and Performance

Caching is one of the most effective performance optimizations. Understanding cache patterns, invalidation, and the full caching hierarchy is critical for architecture decisions.

## Cache Hierarchy

| Layer | Latency | Scope | Example |
|-------|---------|-------|---------|
| L1/L2/L3 CPU cache | 1-10 ns | Single core/CPU | Hardware |
| In-process cache | ~100 ns | Single instance | HashMap, Guava, Caffeine |
| Distributed cache | ~1 ms | Cross-service | Redis, Memcached |
| CDN cache | 1-50 ms | Global edge | CloudFlare, CloudFront |
| Database cache | 1-10 ms | Single DB | Materialized views |

## Cache Patterns

### Cache-Aside (Lazy Loading) - Most Common
Application checks cache first. On miss, reads from DB, populates cache.
- **Pro:** simple, application controls caching logic
- **Con:** stale data until TTL or explicit invalidation; cache miss = slow first request

### Read-Through
Cache sits between app and DB. On miss, **cache itself** loads from DB.
- **Pro:** simpler application code
- **Con:** cache must understand data source

### Write-Through
Every write goes to cache AND DB synchronously.
- **Pro:** strong consistency, no stale data
- **Con:** higher write latency

### Write-Behind (Write-Back)
Writes go to cache immediately, flushed to DB asynchronously.
- **Pro:** lowest write latency
- **Con:** risk of data loss if cache fails before flush

### Refresh-Ahead
Proactively refreshes entries before expiration. Reduces cache miss latency for hot data. Requires access pattern prediction.

## Cache Invalidation Strategies

| Strategy | Mechanism | Trade-off |
|----------|-----------|-----------|
| **TTL** | Entries expire after fixed duration | Simple but serves stale data within window |
| **Event-driven** | Invalidate on data change (events, CDC) | Fresh data but more complex |
| **Versioned keys** | Include version in key (`user:123:v5`) | No explicit invalidation, old entries expire |

### Cache Stampede Prevention
When popular key expires, many requests simultaneously hit DB.
- **Locking** - only one request refreshes, others wait
- **Probabilistic early expiration** - add jitter so keys expire at different times
- **Pre-computation** - refresh before expiration

## Redis vs Memcached

| Feature | Redis | Memcached |
|---------|-------|-----------|
| Data types | Strings, hashes, lists, sets, sorted sets, streams | Key-value only |
| Persistence | RDB snapshots, AOF log | None |
| Clustering | Yes | Consistent hashing |
| Pub/Sub | Yes | No |
| Threading | Single-threaded (multi in 7.0+) | Multi-threaded |
| Best for | Complex data, persistence, pub/sub | Simple caching, large values |

**Redis common uses:** session store, rate limiting, leaderboards, real-time analytics.

## Caching at Different Layers

- **CDN** - static assets (images, CSS, JS), Cache-Control headers, ETags
- **API Gateway** - cache API responses, TTL per endpoint
- **Application** - object caching, query result caching
- **Page/fragment** - rendered HTML for CMS, product pages

## Load Balancing

### Algorithms
- **Round Robin** / **Weighted Round Robin** - equal or proportional distribution
- **Least Connections** - send to least busy server
- **IP Hash** - sticky sessions (same client, same server)
- **Consistent Hashing** - for cache distribution

### L4 vs L7

| Layer | Level | Capabilities |
|-------|-------|-------------|
| **L4** | TCP/UDP | Faster, no content inspection |
| **L7** | HTTP | Content-based routing, SSL termination, caching |

### Health Checks
- **Active** - probe backend periodically
- **Passive** - monitor real traffic errors
- Remove unhealthy backends from pool

### Session Affinity
Sticky sessions simplify stateful apps but reduce even distribution. **Prefer stateless backends with external session store (Redis).**

## Performance Optimization Checklist

1. **Profile first** - measure, identify bottlenecks, optimize biggest impact
2. **Database** - indexing, EXPLAIN ANALYZE, N+1 resolution, connection pooling, read replicas
3. **Connection pooling** - reuse DB/HTTP connections, configure pool size per concurrency
4. **Compression** - gzip/brotli for text content (JSON, HTML, CSS, JS)
5. **Async processing** - heavy work to background queues, return job ID immediately

## Gotchas

- **Cache invalidation** is one of the two hardest problems in computer science (alongside naming things)
- **Stale cache after deploy** - new code reads data in new format, cache has old format. Clear cache on deploy or use versioned keys
- **Cache warming** - cold cache after restart means all requests hit DB. Pre-warm critical keys
- **Distributed cache network** - 1ms per Redis call adds up. Batch operations with pipelines
- **CDN cache poisoning** - caching error responses at CDN serves errors to all users. Set `Cache-Control: no-store` for error responses

## See Also

- [[distributed-systems-fundamentals]] - Latency numbers, replication
- [[queueing-theory]] - Why load causes nonlinear degradation
- [[rest-api-advanced]] - HTTP caching headers, ETag, Cache-Control
- [[quality-attributes-reliability]] - Availability tools including auto-scaling
