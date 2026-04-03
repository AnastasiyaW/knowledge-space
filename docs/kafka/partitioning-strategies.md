---
title: Partitioning Strategies
category: concepts
tags: [kafka, partition, key, hash, ordering, scaling, murmur2]
---

# Partitioning Strategies

Kafka partitioning determines how messages are distributed across partitions using key hashing (murmur2), round-robin for keyless messages, or custom partitioners, with strict ordering guaranteed only within a single partition.

## Key Facts

- Kafka uses **modulo on murmur2 key hash** to determine partition number (NOT consistent hashing)
- Same key = same partition = preserved order within that partition
- Without a key, messages distributed across partitions randomly via UniformStickyPartitioner (batching-friendly)
- **Ordering guaranteed ONLY within a single partition** - between partitions, order is NOT guaranteed
- Partition count can increase but CANNOT decrease (officially)
- When partition count changes, modulo results change, breaking key-to-partition mapping
- Practical rule: **4 partitions per consumer**; for unknown consumer count, default to 8 partitions
- For up to 100K messages/sec, 8 partitions works well
- Adding partitions at runtime causes reordering and may crash Kafka; better approach: use Kafka Streams to re-stream data
- Too many topics/partitions on a single broker (>1000) degrades performance
- Kafka distributes partitions across brokers on its own, but CAN put ALL partitions of one topic on a single node

## Patterns

### Partition Count Sizing

| Scale | Recommended Partitions |
|-------|----------------------|
| Small (unknown consumers) | 8 |
| Per consumer rule | 4 x expected consumer count |
| High throughput (>100K msg/s) | 12-24+ |
| Single consumer | 1 (ordering guaranteed) |

### Custom Partitioner (Java)

```java
public class RegionPartitioner implements Partitioner {
    private Map<String, Integer> regionToPartition;

    @Override
    public void configure(Map<String, ?> configs) {
        regionToPartition = Map.of("us-east", 0, "us-west", 1, "eu-west", 2);
    }

    @Override
    public int partition(String topic, Object key, byte[] keyBytes,
                         Object value, byte[] valueBytes, Cluster cluster) {
        int numPartitions = cluster.partitionsForTopic(topic).size();
        if (key == null) return ThreadLocalRandom.current().nextInt(numPartitions);

        String region = extractRegion(key.toString());
        Integer fixed = regionToPartition.get(region);
        if (fixed != null && fixed < numPartitions) return fixed;

        return Utils.toPositive(Utils.murmur2(keyBytes)) % numPartitions;
    }

    @Override public void close() {}
}

props.put(ProducerConfig.PARTITIONER_CLASS_CONFIG, RegionPartitioner.class.getName());
```

### Custom Partition Selection (Python)

```python
# confluent-kafka does not support partitioner class; compute and pass explicitly
import hashlib

def region_partition(key: str, num_partitions: int) -> int:
    region_map = {"us-east": 0, "us-west": 1, "eu-west": 2}
    if ":" in key:
        region = key.split(":")[0]
        p = region_map.get(region)
        if p is not None and p < num_partitions:
            return p
    return int(hashlib.md5(key.encode()).hexdigest(), 16) % num_partitions

p.produce("orders", key=key, value=payload, partition=region_partition(key, num_partitions))
```

### Partition Key Best Practices

```
# Use entity ID as key for ordering guarantees
key = customer_id      # All orders for same customer in same partition
key = camera_id        # All frames from same camera in order
key = user_id          # All impressions for same user co-located

# Avoid high-cardinality keys that create hot partitions
# Bad: key = timestamp (each message unique, no grouping benefit)
# Bad: key = "constant" (all messages to one partition)
```

## Gotchas

- **"Book recommendation (partitions = consumers) is wrong in practice"** - you gain ~4-5% performance but lose scalability; adding a consumer requires adding a partition (heavy operation)
- **Adding partitions breaks key-based ordering** - messages with same key may land in different partition due to modulo change; this is why changing partition count in production is problematic
- **Kafka auto-creates topics with `num.partitions=1`** when writing to non-existent topic - terrible for scalability; always set `auto.create.topics.enable=false` in production
- **All partitions of one topic can land on a single node** - invisible during testing, explodes in production under load; proper admin teams track partition assignments
- **Custom partitioner sees serialized bytes** - `partition()` method receives `keyBytes` (already serialized); to access original object, cast the `key` parameter

## See Also

- [[topics-and-partitions]] - topic operations, segment structure, retention
- [[consumer-groups]] - how partition count relates to consumer parallelism
- [[producer-patterns]] - partitioner in the send pipeline
- [Apache Kafka Partitioner Design](https://kafka.apache.org/documentation/#design_loadbalancing)
