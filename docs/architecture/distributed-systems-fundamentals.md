---
title: Distributed Systems Fundamentals
category: concepts
tags: [distributed-systems, cap-theorem, consensus, replication, partitioning]
---

# Distributed Systems Fundamentals

Distributed systems introduce failure modes that don't exist in single-process systems - network partitions, partial failures, clock skew, message reordering. Understanding these limits is essential for informed architecture decisions.

## Latency Numbers Every Engineer Should Know

| Operation | Latency |
|-----------|---------|
| L1 cache reference | ~1 ns |
| L2 cache reference | ~4 ns |
| Main memory reference | ~100 ns |
| SSD random read | ~100 us |
| Distributed cache get (Redis) | ~1 ms |
| Simple DB query | ~1-10 ms |
| HDD seek | ~10 ms |
| Round trip within datacenter | ~0.5 ms |
| Cross-region network | ~50-150 ms |

**Key insight:** network calls are 10,000-1,000,000x slower than memory access. Local app cache vs. distributed cache: order of magnitude difference (100ns vs 1ms).

## CAP Theorem

In a distributed system, guarantee at most two of three:

- **Consistency** - all nodes see same data
- **Availability** - every request gets a response
- **Partition tolerance** - system works despite network failures

Since network partitions are inevitable, the real choice is **CP** (consistent but may reject requests during partition) vs **AP** (available but may return stale data).

### PACELC Extension

When **P**artitioned: choose **A**vailability or **C**onsistency. **E**lse (normal operation): choose **L**atency or **C**onsistency. Even without partitions, there's a consistency-latency trade-off.

### Practical Implications for API Design
- **Choose consistency** for: financial transactions, inventory management
- **Choose availability** for: social media feeds, recommendations
- Most systems need both at different points - design accordingly

## Consistency Models

| Model | Guarantee | Use Case |
|-------|-----------|----------|
| **Strong (linearizability)** | Every read returns most recent write | Distributed locks, leader election |
| **Causal** | Causally related ops seen in order | Good balance of correctness + performance |
| **Read-your-writes** | User sees own updates immediately | Most web applications |
| **Eventual** | Replicas converge given enough time | DNS, CDN caches, social counters |

## Consensus Algorithms

**Problem:** How do distributed nodes agree on a value despite failures?

**Raft** - leader-based. Leader election via randomized timeouts. Log replication to followers. Committed when majority acknowledges. Designed to be understandable. Used in: etcd, CockroachDB, TiKV.

**Paxos** - foundational, mathematically proven. Complex. Used in: Google Chubby, Spanner.

**Practical note:** consensus is expensive (multiple round trips). Use only when strong consistency is required. For most cases, eventual consistency with conflict resolution is sufficient.

## Replication Strategies

### Single-Leader
One node accepts writes, replicates to followers. Simple and consistent. Leader is bottleneck and SPOF. Used in: PostgreSQL streaming replication, MySQL replication.

### Multi-Leader
Multiple nodes accept writes, sync between each other. Better write availability for geo-distributed systems. Challenge: conflict resolution (last-writer-wins, merge functions, CRDTs).

### Leaderless (Dynamo-style)
Any node accepts reads/writes. Quorum-based: read R + write W > N replicas. Used in: Cassandra, DynamoDB, Riak. Challenge: read repair, anti-entropy.

## Partitioning (Sharding)

Split data across nodes when single node can't handle volume/throughput.

### Key-based (Hash) Partitioning
Hash of key determines partition. Even distribution but no range queries. Consistent hashing avoids full redistribution when nodes change.

### Range Partitioning
Continuous key ranges assigned to partitions. Supports range queries but risk of hot spots.

### Secondary Index Partitioning
- **Local indexes** - each partition indexes its own data (scatter-gather queries)
- **Global indexes** - partitioned separately (single-partition queries, more complex writes)

## Resilience Patterns

### Circuit Breaker
Prevent cascade failures by failing fast when downstream is unhealthy. States: Closed -> Open -> Half-Open.

### Bulkhead
Isolate failures by partitioning resources (thread pools, connection pools). Failure in one partition doesn't affect others.

### Timeouts and Retries
- **Exponential backoff** - exponentially increasing delay: 5s -> 25s -> 125s
- **Jitter** - random variation to prevent thundering herd
- Only retry transient errors (5xx, timeouts), never client errors (4xx)

### Graceful Degradation
Disable non-critical features to maintain core functionality. Feature flags for dynamic toggling.

## Fallacies of Distributed Computing (Peter Deutsch)

1. The network is reliable
2. Latency is zero
3. Bandwidth is infinite
4. The network is secure
5. Topology doesn't change
6. There is one administrator
7. Transport cost is zero
8. The network is homogeneous

Every fallacy becomes a bug in production.

## Gotchas

- **Essential vs accidental complexity** - don't add distributed system complexity unless needed. Start simple
- **Utilization above 70-80%** causes disproportionate response time increases (queueing theory hockey-stick curve)
- **Network calls in loops** - a seemingly simple loop with 100 iterations can take 50+ seconds if each involves a network call
- **Clock skew** between nodes makes timestamp-based ordering unreliable without vector clocks or hybrid logical clocks

## See Also

- [[queueing-theory]] - Why systems degrade nonlinearly under load
- [[quality-attributes-reliability]] - Availability, fault tolerance, recoverability
- [[microservices-communication]] - Saga, CQRS, event sourcing patterns
- [[cap-theorem]] in [[sql-databases]] topic for ACID vs BASE
