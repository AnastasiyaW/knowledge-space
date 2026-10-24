---
title: "Admin API"
category: reference
tags: [kafka, admin, api, topic-management, acl, cluster, java, python]
level: 3
source_sha256: 7d373717ef4da4f32a6a1b873621c8e7570df6f1226bcd9dbc9f704f38bb0c96
translation: machine
translated_at: '2026-10-24'
---
# Admin API {#admin-api}

Die Admin API (Bibliothek `kafka-clients`) bietet programmatische Cluster-Verwaltung für Topics, Consumer Groups, ACLs und Konfigurationen. Alle Methoden liefern asynchrone `KafkaFuture`-Ergebnisse.

## Wichtige Fakten {#key-facts}

- Teil der Bibliothek `kafka-clients` zusammen mit den Producer- und Consumer-APIs
- Als `@InterfaceStability.Evolving` markiert - kann sich in Minor-Versionen ändern
- Alle Methoden sind **asynchron** - sie liefern ein `KafkaFuture` (erweitert Java Future um CompletionStage-Methoden)
- Die meisten Methoden akzeptieren **Collections** (Batch-Operationen) - mehrere Topics lassen sich gleichzeitig erstellen oder löschen
- Operationen sind **NICHT atomar** - Teilerfolge sind möglich (3 Topics erstellt, 1 schlägt fehl)
- Einzige erforderliche Konfiguration: `bootstrap.servers`
- Tools wie Kafdrop, AKHQ und Conduktor verwenden intern die Admin API

## Muster {#patterns}

### Admin-Client erstellen {#create-admin-client}

```java
Admin admin = Admin.create(Map.of(
    AdminClientConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092"
));
```

```python
from confluent_kafka.admin import AdminClient, NewTopic

admin = AdminClient({"bootstrap.servers": "localhost:9092"})
```

### Topic-Operationen {#topic-operations}

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

### Cluster-Konfiguration {#cluster-configuration}

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

### Consumer-Group-Verwaltung {#consumer-group-management}

```java
admin.listConsumerGroups();
admin.describeConsumerGroups(List.of("my-group"));
admin.listConsumerGroupOffsets("my-group");
admin.alterConsumerGroupOffsets("my-group", offsetMap);
admin.deleteConsumerGroupOffsets("my-group", partitions);
```

### ACL-Verwaltung {#acl-management}

```java
admin.createAcls(List.of(new AclBinding(
    new ResourcePattern(ResourceType.TOPIC, "orders", PatternType.LITERAL),
    new AccessControlEntry("User:alice", "*", AclOperation.WRITE, AclPermissionType.ALLOW)
)));
admin.describeAcls(filter);
admin.deleteAcls(List.of(filter));
```

### Cluster-Beschreibung {#cluster-description}

```java
DescribeClusterResult cluster = admin.describeCluster();
cluster.nodes().get();      // all broker nodes
cluster.controller().get(); // controller node
cluster.clusterId().get();  // cluster ID
```

## Stolperfallen {#gotchas}

- **Das Löschen eines Topics ist nicht sofort wirksam** - Dateien werden asynchron bereinigt; wird unmittelbar nach dem Löschen ein Topic mit demselben Namen erstellt, kann dies mit "already exists" fehlschlagen; in einer Schleife mit `validateOnly=true` wiederholen, bis es erfolgreich ist
- **Das Hinzufügen von Partitionen bricht die schlüsselbasierte Reihenfolge** - Nachrichten mit demselben Schlüssel können in einer anderen Partition landen; dies ist nicht rückgängig zu machen
- **Operationen sind NICHT atomar** - beim Erstellen mehrerer Topics können manche erfolgreich sein, während andere fehlschlagen; die Ergebnisse einzeln prüfen
- **`KafkaFuture.get()` blockiert** - für nicht-blockierende Nutzung über `.toCompletionStage()` umwandeln oder in `Mono.fromCompletionStage()` von Reactor einhüllen
- **Partition-Reassignment ist asynchron** - den Fortschritt von `alterPartitionReassignments()` mit `listPartitionReassignments()` verfolgen

## Siehe auch {#see-also}

- [[topics-and-partitions]] - Topic-Konfiguration und CLI-Operationen
- [[kafka-security]] - Details zur ACL-Konfiguration
- [[broker-architecture]] - Konfigurationshierarchie (Topic > Broker > Cluster > statisch)
- [Apache Kafka Admin API](https://kafka.apache.org/documentation/#adminapi)
