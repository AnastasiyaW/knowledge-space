---
title: Admin API
category: reference
tags: [kafka, admin, api, topic-management, acl, cluster, java, python]
---

# Admin API

The Admin API (`kafka-clients` library) provides programmatic cluster management for topics, consumer groups, ACLs, and configurations with all methods returning asynchronous `KafkaFuture` results.

## Key Facts

- Part of `kafka-clients` library alongside Producer and Consumer APIs
- Marked as `@InterfaceStability.Evolving` - may change in minor versions
- All methods are **asynchronous** - return `KafkaFuture` (extends Java Future with CompletionStage methods)
- Most methods accept **collections** (batch operations) - can create/delete multiple topics at once
- Operations are **NOT atomic** - partial success possible (3 topics created, 1 fails)
- Only required config: `bootstrap.servers`
- Tools like Kafdrop, AKHQ, Conduktor use Admin API internally

## Patterns

### Create Admin Client

```java
Admin admin = Admin.create(Map.of(
    AdminClientConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092"
));
```

```python
from confluent_kafka.admin import AdminClient, NewTopic

admin = AdminClient({"bootstrap.servers": "localhost:9092"})
```

### Topic Operations

```java
// Create with explicit config
NewTopic topic = new NewTopic("orders", 6, (short) 3)
    .configs(Map.of("min.insync.replicas", "2"));
admin.createTopics(List.of(topic)).all().get();

// Create with broker defaults
new NewTopic("events", Optional.empty(), Optional.empty());

// Manual replica placement
new NewTopic("critical", Map.of(
    0, List.of(2, 3),  // partition 0 on brokers 2,3
    1, List.of(4, 5)   // partition 1 on brokers 4,5
));

// Add partitions (WARNING: breaks key-based ordering)
admin.createPartitions(Map.of(
    "orders", NewPartitions.increaseTo(12)
)).all().get();

// Delete topic (async cleanup, not instant)
admin.deleteTopics(List.of("old-topic")).all().get();

// Delete records up to offset (from beginning only)
admin.deleteRecords(Map.of(
    new TopicPartition("topic", 0), RecordsToDelete.beforeOffset(250)
));
```

```python
# Python - create topic
new_topic = NewTopic("my-topic", num_partitions=6, replication_factor=3,
    config={"min.insync.replicas": "2"})
admin.create_topics([new_topic])
```

### Cluster Configuration

```java
// Read configs
admin.describeConfigs(List.of(
    new ConfigResource(ConfigResource.Type.BROKER, "5"),
    new ConfigResource(ConfigResource.Type.TOPIC, "orders")
)).all().get();

// Modify configs (incrementally)
admin.incrementalAlterConfigs(Map.of(
    resource, List.of(new AlterConfigOp(
        new ConfigEntry("retention.ms", "259200000"),
        AlterConfigOp.OpType.SET))
)).all().get();
// OpTypes: SET, DELETE, APPEND, SUBTRACT
```

### Consumer Group Management

```java
admin.listConsumerGroups();
admin.describeConsumerGroups(List.of("my-group"));
admin.listConsumerGroupOffsets("my-group");
admin.alterConsumerGroupOffsets("my-group", offsetMap);
admin.deleteConsumerGroupOffsets("my-group", partitions);
```

### ACL Management

```java
admin.createAcls(List.of(new AclBinding(
    new ResourcePattern(ResourceType.TOPIC, "orders", PatternType.LITERAL),
    new AccessControlEntry("User:alice", "*", AclOperation.WRITE, AclPermissionType.ALLOW)
)));
admin.describeAcls(filter);
admin.deleteAcls(List.of(filter));
```

### Cluster Description

```java
DescribeClusterResult cluster = admin.describeCluster();
cluster.nodes().get();      // all broker nodes
cluster.controller().get(); // controller node
cluster.clusterId().get();  // cluster ID
```

## Gotchas

- **Topic delete is not instant** - files cleaned up asynchronously; creating topic with same name immediately after delete may fail with "already exists"; loop with `validateOnly=true` until success
- **Adding partitions breaks key-based ordering** - messages with same key may land in different partition; this is irreversible
- **Operations are NOT atomic** - when creating multiple topics, some may succeed while others fail; check results individually
- **KafkaFuture.get() blocks** - for non-blocking usage, convert via `.toCompletionStage()` or wrap in Reactor's `Mono.fromCompletionStage()`
- **Partition reassignment is async** - use `listPartitionReassignments()` to track progress of `alterPartitionReassignments()`

## See Also

- [[topics-and-partitions]] - topic configuration and CLI operations
- [[kafka-security]] - ACL configuration details
- [[broker-architecture]] - config hierarchy (topic > broker > cluster > static)
- [Apache Kafka Admin API](https://kafka.apache.org/documentation/#adminapi)
