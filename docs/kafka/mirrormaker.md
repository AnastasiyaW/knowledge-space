---
title: MirrorMaker 2
category: reference
tags: [kafka, mirrormaker, replication, cross-cluster, disaster-recovery, active-active, active-passive]
---

# MirrorMaker 2

MirrorMaker 2 (MM2) replicates topics between Kafka clusters for disaster recovery and geo-distribution, built on Kafka Connect with active-active support, automatic offset sync, and topic renaming.

## Key Facts

- Introduced in Kafka 2.4, built on [[kafka-connect]]
- Uses the same consumer protocol as regular consumers (cheap to implement)
- Supports active-passive and active-active replication patterns
- Active-active: bidirectional replication with topic naming prefixes (e.g., `DC1.orders`, `DC2.orders`)
- Cycle prevention via topic prefixing and/or header-based message filtering
- Automatic offset sync between clusters
- Replication latency means eventual consistency across clusters
- Replication uses the same protocol as consumer reads

## Patterns

### Active-Passive (DR Standby)

```php
DC1 (primary)  --MM2-->  DC2 (standby)
  writes + reads           receives replicated data
                           on DC1 failure: failover to DC2
```

Simpler but wastes standby resources.

### Active-Active (Geo-Distribution)

```rust
DC1 <--MM2--> DC2 (bidirectional)
  DC1 clients use DC1.* topics
  DC2 clients use DC2.* topics
  On DC loss: ~zero data loss, clients switch to surviving DC
```

Topic naming: `DC1.orders`, `DC2.orders` to prevent replication loops.

### MirrorMaker 2 Configuration

```properties
# Source cluster
clusters = DC1, DC2
DC1.bootstrap.servers = dc1-kafka:9092
DC2.bootstrap.servers = dc2-kafka:9092

# Replication flows
DC1->DC2.enabled = true
DC2->DC1.enabled = true

# Topic filtering
DC1->DC2.topics = .*
DC2->DC1.topics = .*

# Consumer group offset sync
sync.group.offsets.enabled = true
```

## Gotchas

- **Topic naming with prefixes is not ideal for active-active** - clients must be aware of DC-specific topic names; alternatives: subject mapping or routing layers
- **Replication lag = eventual consistency** - data at DC2 may lag behind DC1 by seconds to minutes
- **Cycle prevention is critical** - without it, messages replicate infinitely between clusters; use prefixes or header-based filtering
- **Monitor replication lag between clusters** - growing lag indicates network or capacity issues

## See Also

- [[kafka-connect]] - MM2 is built on Connect framework
- [[kafka-backup-and-dr]] - DR planning and failover procedures
- [[broker-architecture]] - cluster architecture
- [Apache Kafka MirrorMaker Documentation](https://kafka.apache.org/documentation/#georeplication)
