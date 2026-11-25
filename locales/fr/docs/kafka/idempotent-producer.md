---
title: "Producteur idempotent"
category: concepts
tags: [kafka, producer, idempotent, deduplication, ordering, exactly-once]
level: 3
source_sha256: c4f092912e5735c2bf2acb6e34a0521c5bc44a95d569e61e1380fdf602191ad1
translation: machine
translated_at: '2026-10-24'
---
# Producteur idempotent {#idempotent-producer}

Le producteur idempotent attribue un PID (Producer ID) et des numéros de séquence à chaque message, ce qui permet au broker de dédupliquer les nouvelles tentatives au sein d'une session de producteur, avec un surcoût négligeable.

## Faits clés {#key-facts}

- Chaque producteur reçoit un **PID** (Producer ID) attribué par le broker lors de l'initialisation
- Chaque message reçoit un **numéro de séquence** monotone dans son epoch, par partition
- Le broker détecte et rejette les paires `(PID, sequence_number)` en double
- Le surcoût est minimal : quelques octets supplémentaires par message (impact négligeable sur les performances)
- **Activé automatiquement depuis Kafka 3.0.0** lorsque toutes les conditions suivantes sont réunies : `max.in.flight.requests.per.connection` <= 5, `retries` > 0, `acks=all`
- Si `enable.idempotence=true` est défini explicitement alors que les conditions ne sont pas remplies, le constructeur `KafkaProducer` lève une exception
- Portée : par partition, par session de producteur ; le broker conserve les 5 derniers numéros de séquence par PID et par partition
- **Bonus** : avec l'idempotence activée, Kafka garantit un ordre correct même lorsque les messages arrivent dans le désordre à cause des nouvelles tentatives
- Sans idempotence et avec `max.in.flight > 1`, une nouvelle tentative du lot N peut arriver après le succès du lot N+1, ce qui provoque des écritures dans le désordre

## Modèles {#patterns}

### Configuration {#configuration}

```java
// Java - explicit idempotent setup
Properties props = new Properties();
props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "broker1:9092,broker2:9092");
props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);
// These are automatically enforced when idempotence is enabled:
//   acks = all
//   retries = Integer.MAX_VALUE
//   max.in.flight.requests.per.connection <= 5
props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
```

```python
# Python - idempotent producer
from confluent_kafka import Producer

p = Producer({
    "bootstrap.servers": "broker1:9092,broker2:9092",
    "enable.idempotence": True,
    # acks automatically set to "all"
    # max.in.flight.requests.per.connection automatically capped at 5
})
```

### Mécanisme de garantie d'ordre {#ordering-guarantee-mechanism}

```bash
Without idempotency (max.in.flight=2):
  Batch 1 sent -> fails -> retry queued
  Batch 2 sent -> succeeds -> written at offset N
  Batch 1 retry -> succeeds -> written at offset N+1
  Result: messages OUT OF ORDER

With idempotency (max.in.flight<=5):
  Batch 1 sent -> fails -> retry queued
  Batch 2 sent -> broker rejects (out-of-sequence for this PID)
  Batch 1 retry -> succeeds
  Batch 2 retry -> succeeds
  Result: messages IN ORDER
```

## Pièges courants {#gotchas}

- **Ne protège PAS contre les nouvelles tentatives au niveau applicatif** : si votre code intercepte une erreur et rappelle `produce()`, le message reçoit un nouveau numéro de séquence ; le broker le considère comme un nouveau message, et non comme un doublon
- **Frontière de session** : si le producteur redémarre, il reçoit un nouveau PID ; les anciennes tentatives en cours ne peuvent pas être dédupliquées par rapport au nouveau PID ; pour l'exactly-once entre sessions, utilisez [[kafka-transactions]] avec `transactional.id`
- **Impossible de remplacer la génération des numéros de séquence** : aucune API ne permet de définir manuellement les numéros de séquence
- **`max.in.flight.requests.per.connection > 5` avec l'idempotence** lève une ConfigException : le broker ne peut suivre que 5 lots en vol au maximum par PID et par partition

## Voir aussi {#see-also}

- [[kafka-transactions]] - étend le producteur idempotent avec des écritures atomiques inter-partitions
- [[delivery-semantics]] - place du producteur idempotent dans les garanties exactly-once
- [[kafka-producer-fundamentals]] - pipeline complet du producteur, batching, compression, gestion des erreurs
- [KIP-98 : livraison exactement une fois et messages transactionnels](https://cwiki.apache.org/confluence/display/KAFKA/KIP-98+-+Exactly+Once+Delivery+and+Transactional+Messaging)
