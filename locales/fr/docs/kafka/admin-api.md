---
title: "API d'administration"
category: reference
tags: [kafka, admin, api, topic-management, acl, cluster, java, python]
level: 3
source_sha256: 7d373717ef4da4f32a6a1b873621c8e7570df6f1226bcd9dbc9f704f38bb0c96
translation: machine
translated_at: '2026-10-24'
---
# API d'administration {#admin-api}

L'API d'administration (bibliothèque `kafka-clients`) fournit une gestion programmatique du cluster pour les topics, les groupes de consommateurs, les ACL et les configurations. Toutes les méthodes renvoient des résultats `KafkaFuture` asynchrones.

## Points clés {#key-facts}

- Fait partie de la bibliothèque `kafka-clients`, avec les API Producer et Consumer
- Marquée `@InterfaceStability.Evolving`, elle peut changer dans les versions mineures
- Toutes les méthodes sont **asynchrones** : elles renvoient un `KafkaFuture` (qui étend Java Future avec les méthodes de CompletionStage)
- La plupart des méthodes acceptent des **collections** (opérations par lot) : on peut créer ou supprimer plusieurs topics en une seule fois
- Les opérations ne sont **PAS atomiques** : un succès partiel est possible (3 topics créés, 1 en échec)
- Seule configuration requise : `bootstrap.servers`
- Des outils comme Kafdrop, AKHQ ou Conduktor utilisent l'API d'administration en interne

## Modèles d'utilisation {#patterns}

### Créer le client d'administration {#create-admin-client}

```java
Admin admin = Admin.create(Map.of(
    AdminClientConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092"
));
```

```python
from confluent_kafka.admin import AdminClient, NewTopic

admin = AdminClient({"bootstrap.servers": "localhost:9092"})
```

### Opérations sur les topics {#topic-operations}

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

### Configuration du cluster {#cluster-configuration}

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

### Gestion des groupes de consommateurs {#consumer-group-management}

```java
admin.listConsumerGroups();
admin.describeConsumerGroups(List.of("my-group"));
admin.listConsumerGroupOffsets("my-group");
admin.alterConsumerGroupOffsets("my-group", offsetMap);
admin.deleteConsumerGroupOffsets("my-group", partitions);
```

### Gestion des ACL {#acl-management}

```java
admin.createAcls(List.of(new AclBinding(
    new ResourcePattern(ResourceType.TOPIC, "orders", PatternType.LITERAL),
    new AccessControlEntry("User:alice", "*", AclOperation.WRITE, AclPermissionType.ALLOW)
)));
admin.describeAcls(filter);
admin.deleteAcls(List.of(filter));
```

### Description du cluster {#cluster-description}

```java
DescribeClusterResult cluster = admin.describeCluster();
cluster.nodes().get();      // all broker nodes
cluster.controller().get(); // controller node
cluster.clusterId().get();  // cluster ID
```

## Pièges à éviter {#gotchas}

- **La suppression d'un topic n'est pas immédiate** : les fichiers sont nettoyés de manière asynchrone. Créer un topic portant le même nom juste après sa suppression peut échouer avec « already exists ». Il faut boucler avec `validateOnly=true` jusqu'à obtenir un succès.
- **Ajouter des partitions casse l'ordre basé sur la clé** : des messages ayant la même clé peuvent atterrir dans des partitions différentes. Cette opération est irréversible.
- **Les opérations ne sont PAS atomiques** : lors de la création de plusieurs topics, certains peuvent réussir pendant que d'autres échouent. Il faut vérifier les résultats individuellement.
- **`KafkaFuture.get()` bloque** : pour une utilisation non bloquante, convertir via `.toCompletionStage()` ou encapsuler avec `Mono.fromCompletionStage()` de Reactor.
- **La réaffectation des partitions est asynchrone** : utiliser `listPartitionReassignments()` pour suivre la progression de `alterPartitionReassignments()`.

## Voir aussi {#see-also}

- [[topics-and-partitions]] - configuration des topics et opérations en ligne de commande
- [[kafka-security]] - détails de la configuration des ACL
- [[broker-architecture]] - hiérarchie des configurations (topic > broker > cluster > statique)
- [Documentation Apache Kafka sur l'API d'administration](https://kafka.apache.org/documentation/#adminapi)
