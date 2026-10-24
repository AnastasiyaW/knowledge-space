---
title: "Configuration du consommateur"
category: reference
tags: [kafka, consumer, configuration, fetch, polling, timeout]
level: 3
source_sha256: 213de6862339098c62ff67ea2397b13e0beb4cea646fc2deab449b9a696a7c89
translation: machine
translated_at: '2026-10-24'
---
# Configuration du consommateur {#consumer-configuration}

Référence complète des paramètres de configuration du consommateur Kafka, avec les valeurs par défaut, des recommandations de réglage et leur impact sur le comportement.

## Points clés {#key-facts}

- Le consommateur fonctionne en mode pull : il appelle `poll()` pour récupérer les données depuis les brokers ; Kafka ne pousse pas les données
- `fetch.max.wait.ms` contrôle le temps d'attente maximal lors d'un poll ; tout ce qui arrive pendant cette fenêtre est renvoyé
- `fetch.min.bytes` définit la taille minimale de données avant le retour ; Kafka attend que cette quantité soit disponible OU que `fetch.max.wait.ms` expire
- Kafka ne renvoie jamais de messages partiels, uniquement des enregistrements complets
- `max.poll.records` (valeur par défaut 500) limite le nombre de messages par poll, toutes partitions confondues
- Trois clients Kafka pour Python : confluent-kafka-python (wrapper de librdkafka, pour la production), kafka-python (Python pur) et kafka-go pour Go

## Modèles {#patterns}

### Consommateur optimisé pour le débit {#throughput-optimized-consumer}

```properties
fetch.min.bytes=1048576        # 1MB - wait for larger batches
fetch.max.wait.ms=500          # wait up to 500ms
max.poll.records=1000          # larger batches per poll
max.partition.fetch.bytes=2097152  # 2MB per partition
```

### Consommateur optimisé pour la latence {#latency-optimized-consumer}

```properties
fetch.min.bytes=1              # return as soon as any data available
fetch.max.wait.ms=100          # short wait
max.poll.records=100           # smaller batches, faster processing
```

### Consommateur à traitement long {#long-processing-consumer}

```properties
max.poll.interval.ms=600000    # 10 min between polls
max.poll.records=50            # smaller batches
session.timeout.ms=45000       # longer session
heartbeat.interval.ms=15000    # 1/3 of session timeout
```

### Opérations sur les groupes de consommateurs via l'API d'administration {#consumer-group-operations-via-admin-api}

```java
Admin admin = Admin.create(Map.of("bootstrap.servers", "localhost:9092"));

admin.listConsumerGroups();
admin.describeConsumerGroups(List.of("group-id"));
admin.listConsumerGroupOffsets("group-id");
admin.alterConsumerGroupOffsets("group-id", offsetMap);
admin.deleteConsumerGroupOffsets("group-id", partitions);
```

## Pièges courants {#gotchas}

- **`enable.auto.commit=true` est la valeur par défaut** : c'est la première source de bugs de perte de données chez les débutants ; désactivez-la pour toute charge de travail en production
- **`auto.commit.interval.ms` doit être inférieur à `session.timeout.ms`** : sinon le consommateur est déclaré mort avant le déclenchement du commit
- **Dépassement de `max.poll.interval.ms` = consommateur exclu du groupe** : même si les heartbeats fonctionnent correctement ; cela arrive avec les traitements longs
- **Il existe trois clients Go aux API différentes** : kafka-go (Go pur, basé sur les contextes), confluent-kafka-go (wrapper de librdkafka, style Java) et d'autres ; choisissez selon les préférences de l'équipe

## Voir aussi {#see-also}

- [[consumer-groups]] - mécanique des groupes, stratégies d'affectation
- [[offsets-and-commits]] - stratégies de gestion des offsets
- [[rebalancing-deep-dive]] - réglage des heartbeats, rééquilibrage coopératif
- [Configurations des consommateurs Apache Kafka](https://kafka.apache.org/documentation/#consumerconfigs)
