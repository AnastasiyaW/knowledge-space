---
title: CAP Theorem and Distributed Consistency
category: concepts
tags: [distributed-systems, consistency, availability, partition-tolerance]
---
# CAP Theorem and Distributed Consistency

The CAP theorem states that a distributed data store can provide at most two of three guarantees simultaneously: Consistency, Availability, and Partition tolerance.

## Key Facts

- In practice, partition tolerance is non-negotiable in distributed systems - you choose between CP and AP
- **CP systems**: Prioritize consistency during network partition (e.g., etcd, ZooKeeper, HBase). Reject writes/reads if they cannot guarantee consistency
- **AP systems**: Prioritize availability during partition (e.g., Cassandra, DynamoDB, CouchDB). Return potentially stale data rather than errors
- **Eventual consistency**: Most AP systems converge to consistent state after partition heals. Conflict resolution strategies matter (last-write-wins, vector clocks, CRDTs)
- CAP is often misunderstood: the tradeoff only applies DURING a partition. When the network is healthy, you can have all three
- See [[database-selection]] for how CAP influences storage choice
- See [[quality-attributes]] for how consistency requirements are derived from business needs

## Patterns

### Consistency spectrum

```
Strong              Linearizable
  |                 Sequential
  |                 Causal
  |                 Read-your-writes
  |                 Monotonic reads
  v                 Eventual
Weak                No guarantees
```

### PACELC extension

CAP only describes behavior during partitions. PACELC adds normal operation:

```
If Partition:
  Choose Availability or Consistency (PA or PC)
Else (normal operation):
  Choose Latency or Consistency (EL or EC)

Examples:
  Cassandra: PA/EL  (available + low latency, weak consistency)
  MongoDB:   PA/EC  (available but consistent when healthy)
  HBase:     PC/EC  (consistent always, higher latency)
```

### Tunable consistency (Cassandra example)

```
Write consistency: ONE / QUORUM / ALL
Read consistency:  ONE / QUORUM / ALL

Strong read: W + R > N (replication factor)
  - QUORUM write + QUORUM read with N=3: 2+2 > 3 -> strong
  - ONE write + ALL read: 1+3 > 3 -> strong
  - ONE write + ONE read: 1+1 < 3 -> eventual
```

## Gotchas

- **Symptom**: System returns stale data after node recovery -> **Cause**: Using AP database with ONE/ONE consistency and no read-repair -> **Fix**: Enable read-repair, use QUORUM reads for critical paths, or accept eventual consistency with proper UI feedback
- **Symptom**: Team demands "100% consistency AND 100% availability" -> **Cause**: Not understanding fundamental distributed systems tradeoffs -> **Fix**: Map each data domain to its actual consistency need. User profiles can be eventual, financial transactions need strong consistency
- **Symptom**: Split-brain in leader election -> **Cause**: Network partition without proper quorum configuration -> **Fix**: Use odd number of nodes (3, 5, 7), require majority quorum for leader election

## See Also

- [[distributed-system-patterns]] - Broader patterns for distributed architectures
- [[database-selection]] - How to choose databases considering CAP
- [[quality-attributes]] - Deriving consistency requirements from business
- Martin Fowler: [Consistency Models](https://martinfowler.com/articles/patterns-of-distributed-systems/paxos.html)
- Paper: "Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services" (Gilbert & Lynch, 2002)
- Paper: "Consistency Tradeoffs in Modern Distributed Database System Design" (Abadi, 2012) - PACELC
