---
title: "Sémantiques de livraison"
category: concepts
tags: [kafka, delivery, exactly-once, at-least-once, at-most-once, idempotent]
level: 3
source_sha256: 91408255db31fda830960730031e5b6913f422c64066a7a765a0a3c99d9e1aec
translation: machine
translated_at: '2026-10-24'
---
# Sémantiques de livraison {#delivery-semantics}

Kafka prend en charge trois sémantiques de livraison (au plus une fois, au moins une fois et exactement une fois), chacune avec des exigences de configuration spécifiques et des compromis à la fois côté producteur et côté consommateur.

## Points clés {#key-facts}

- **Au plus une fois** : des messages peuvent être perdus mais jamais dupliqués ; `acks=0` ou auto-commit avant traitement ; à utiliser pour les métriques, les journaux et les analyses où la perte est acceptable
- **Au moins une fois** : des messages peuvent être dupliqués mais jamais perdus ; `acks=all` + `retries>0` + commit manuel après traitement ; configuration de production la plus courante
- **Exactement une fois** : chaque message est traité exactement une fois malgré les pannes ; nécessite un producteur idempotent + des transactions OU une déduplication au niveau applicatif
- « Exactement une fois » est techniquement impossible (problème des deux généraux) ; l'exactement une fois en pratique = au moins une fois + idempotence à chaque frontière
- Des doublons peuvent survenir à la fois côté **producteur** (ACK perdu entraînant une nouvelle tentative) et côté **consommateur** (plantage après traitement mais avant le commit de l'offset)
- L'exactement une fois de Kafka ne fonctionne QUE pour le motif : lecture depuis Kafka -> traitement -> écriture dans Kafka (via [[kafka-transactions]])
- L'exactement une fois entre systèmes (Kafka -> base de données externe) nécessite une déduplication au niveau applicatif
- Une sémantique plus stricte = plus de surcharge = débit plus faible

## Motifs {#patterns}

### Configuration au plus une fois {#at-most-once-configuration}

```properties
# Producer
acks=0

# Consumer
enable.auto.commit=true
auto.commit.interval.ms=5000
```

### Configuration au moins une fois {#at-least-once-configuration}

```properties
# Producer
acks=all
retries=2147483647
enable.idempotence=true

# Consumer
enable.auto.commit=false
# Commit manually after successful processing
```

```java
// Java - at-least-once consumer
try {
    while (true) {
        ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
        for (ConsumerRecord<String, String> record : records) {
            processRecord(record);  // Process first
        }
        consumer.commitSync();  // Then commit
    }
} finally {
    consumer.close();
}
```

```python
# Python - at-least-once consumer
from confluent_kafka import Consumer

conf = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "my-group",
    "enable.auto.commit": False,
}
consumer = Consumer(conf)
consumer.subscribe(["my-topic"])

try:
    while True:
        msg = consumer.poll(0.1)
        if msg is None or msg.error():
            continue
        process_message(msg)
        consumer.commit(msg)  # Commit after processing
finally:
    consumer.close()
```

### Exactement une fois (Kafka vers Kafka) {#exactly-once-kafka-to-kafka}

```java
// Producer config
props.put("transactional.id", "my-transactional-id");
props.put("enable.idempotence", "true");

producer.initTransactions();
producer.beginTransaction();
try {
    producer.send(new ProducerRecord<>("output", key, value));
    producer.sendOffsetsToTransaction(offsets, consumerGroupMetadata);
    producer.commitTransaction();
} catch (Exception e) {
    producer.abortTransaction();
}

// Consumer config
props.put("isolation.level", "read_committed");
props.put("enable.auto.commit", "false");
```

### Où surviennent les doublons {#where-duplicates-occur}

```php
Producer Side:
  Producer sends -> Broker receives + stores -> ACK lost on network
  -> Producer retries -> DUPLICATE in broker

Consumer Side:
  Consumer receives batch -> Processes messages -> Crashes before commit
  -> Restart -> Re-reads same batch -> DUPLICATE processing
```

## Pièges à éviter {#gotchas}

- **L'auto-commit est la première source de bugs pour les débutants avec Kafka** : le consommateur reçoit des messages, l'auto-commit se déclenche, le consommateur plante pendant le traitement ; au redémarrage, Kafka considère les messages comme traités et livre le lot suivant ; les messages perdus sont perdus définitivement
- **Le producteur idempotent n'empêche que les doublons de nouvelles tentatives au niveau de la bibliothèque** : si le code applicatif intercepte une erreur et rappelle `produce()`, le message reçoit un nouveau numéro de séquence et le broker le considère comme un nouveau message
- **`isolation.level` vaut `read_uncommitted` par défaut** : les transactions n'ont aucun effet tant que le consommateur ne définit pas explicitement `isolation.level=read_committed`
- **L'exactement une fois ne couvre PAS les systèmes externes** : les écritures en base de données, les appels HTTP ou les opérations inter-clusters sortent du périmètre des garanties transactionnelles de Kafka

## Voir aussi {#see-also}

- [[kafka-transactions]] - API de producteur transactionnel pour l'exactement une fois au sein de Kafka
- [[idempotent-producer]] - mécanisme de déduplication par PID + numéro de séquence
- [[consumer-groups]] - gestion des offsets et stratégies de commit
- [[transactional-outbox]] - motif pour l'exactement une fois avec des bases de données externes
- [KIP-98 : Livraison exactement une fois et messagerie transactionnelle](https://cwiki.apache.org/confluence/display/KAFKA/KIP-98+-+Exactly+Once+Delivery+and+Transactional+Messaging)
