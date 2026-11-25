---
title: "ZIO Kafka"
category: reference
tags: [kafka, zio, scala, functional, effects, zstream, zio-kafka]
level: 3
source_sha256: 82182d6ec3aa80b513d0dda5e98606b472523d3d9b2cc25ec1f6c9218fbdab4c
translation: machine
translated_at: '2026-10-24'
---
# ZIO Kafka {#zio-kafka}

ZIO Kafka fournit une intégration Kafka purement fonctionnelle à l'aide de ZIO Streams, en enveloppant le client Java standard avec une gestion explicite des erreurs, une gestion des ressources composable et un suivi des effets typé.

## Points clés {#key-facts}

- Signature de type ZIO : `ZIO[R, E, A]` - R = environnement, E = type d'erreur, A = type de succès
- ZStream suit le même schéma : `ZStream[R, E, A]`
- Les fonctions ne lèvent jamais d'exceptions : les erreurs sont retournées comme valeurs et gérées explicitement
- Les effets sont paresseux : on définit d'abord le calcul, puis on l'exécute à la demande
- `ZLayer` pour l'injection de dépendances : modules composables fournissant des services
- Gestion des offsets intégrée au pipeline de flux
- Backpressure intégré via les opérateurs de ZStream

## Patterns {#patterns}

### Producteur ZIO Kafka {#zio-kafka-producer}

```scala
val producerSettings = ProducerSettings(List("localhost:9092"))
val producer = ZLayer.scoped(Producer.make(producerSettings))

val produceEffect = Producer.produce(
  topic = "test-topic",
  key = "key",
  value = "value",
  keySerializer = Serde.string,
  valueSerializer = Serde.string
)
```

### Consommateur ZIO Kafka {#zio-kafka-consumer}

```scala
val consumerSettings = ConsumerSettings(List("localhost:9092"))
  .withGroupId("group1")

Consumer
  .subscribeAnd(Subscription.topics("test-topic"))
  .plainStream(Serde.string, Serde.string)
  .tap(record => Console.printLine(record.value))
  .map(_.offset)
  .aggregateAsync(Consumer.offsetBatches)
  .mapZIO(_.commit)
  .runDrain
```

### Comparaison : Akka vs Spring vs ZIO {#comparison-akka-vs-spring-vs-zio}

| Aspect | Akka/Alpakka | Spring Kafka | ZIO Kafka |
|--------|-------------|--------------|-----------|
| Langage | Scala/Java | Java | Scala |
| Paradigme | Modèle d'acteurs | Annotations/DI | Effets fonctionnels |
| Gestion des erreurs | Supervision | try-catch | Types d'effets |
| Backpressure | Intégré | N/A | Intégré |
| Courbe d'apprentissage | Élevée | Moyenne | Élevée |

## Voir aussi {#see-also}

- [[alpakka-kafka]] - Alternative Akka Streams
- [[spring-kafka]] - Alternative Spring Boot
- [[kafka-streams]] - traitement natif de flux Kafka
- [ZIO Kafka GitHub](https://github.com/zio/zio-kafka)
