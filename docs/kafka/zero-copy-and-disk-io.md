---
title: Zero-Copy and Disk I/O
category: concepts
tags: [kafka, zero-copy, sendfile, page-cache, sequential-io, performance]
---

# Zero-Copy and Disk I/O

Kafka achieves high throughput through sequential disk I/O, OS page cache utilization, and zero-copy transfer via `sendfile()`, making CPU almost never the bottleneck.

## Key Facts

- Kafka uses `sendfile()` system call (zero-copy) to transfer data from disk to network socket, bypassing userspace buffers
- Data on disk is in the exact network wire format - no CPU transformation needed
- Sequential disk I/O is faster than random memory access at scale
- Data flows: disk -> kernel page cache -> NIC (network card) via DMA, CPU not involved
- Typical failure cascade: network dies first, then disk, CPU almost never
- Modern 10Gbps datacenter networks can handle dozens of independent readers per topic
- Multiple consumers are very cheap because data is served from page cache
- Zero-copy works ONLY when SSL is NOT enabled on the broker listener
- Messages are batched and compressed at the batch level, stored compressed on disk, decompressed by consumers
- Batch headers store the latest `CreateTime` of contained messages

## Patterns

### How Zero-Copy Works

```
Traditional (without zero-copy):
  Disk -> Kernel Buffer -> User Space Buffer -> Socket Buffer -> NIC
  (4 copies, 4 context switches)

Kafka (with zero-copy / sendfile):
  Disk -> Kernel Page Cache -> NIC (via DMA)
  (2 copies, 0 context switches, CPU uninvolved)
```

### Why Kafka Is Fast

```
1. Sequential I/O:
   - Append-only writes (no random seeks)
   - Sequential reads (consumers read in order)
   - HDD sequential: 200-300 MB/s vs random: 0.1-1 MB/s

2. Page Cache:
   - OS caches recently written/read data
   - Hot data served from memory without Kafka knowing
   - JVM heap stays clean (no GC pressure from data)

3. Batching:
   - Producer accumulates messages into batches
   - One batch = one disk write, one network send
   - 100 messages = 1 Kafka write

4. Compression:
   - Batch-level compression (lz4/zstd/snappy/gzip)
   - Stored compressed, transferred compressed
   - Consumer decompresses on read
```

### Segment File Structure

```
/var/kafka/data/
  orders-0/                          # topic "orders", partition 0
    00000000000000000000.log         # segment file (records)
    00000000000000000000.index       # offset-to-position index
    00000000000000000000.timeindex   # timestamp-to-offset index
    00000000000000123456.log         # next segment (starts at offset 123456)
    leader-epoch-checkpoint
```

- `.log` - actual message data (batch-compressed)
- `.index` - sparse offset-to-byte-position mapping
- `.timeindex` - sparse timestamp-to-offset mapping

## Gotchas

- **SSL disables zero-copy** - with SSL enabled, data must be encrypted in userspace, adding CPU overhead and eliminating the `sendfile()` optimization
- **JVM GC is NOT a concern for data path** - Kafka stores data in page cache (outside JVM heap); GC pressure comes from connection handling and metadata, not data
- **Page cache thrashing** - if the broker serves too many different partitions that don't fit in RAM, page cache evictions cause disk reads; monitor cache hit ratio
- **Segment stays open for a long time with slow writers** - actual data retention can be much longer than configured because retention applies only to closed segments

## See Also

- [[broker-architecture]] - log segments, retention policies, segment rolling
- [[topics-and-partitions]] - on-disk layout, segment configuration
- [[producer-patterns]] - batching and compression at producer level
- [Kafka Design: Efficiency](https://kafka.apache.org/documentation/#maximizingefficiency)
