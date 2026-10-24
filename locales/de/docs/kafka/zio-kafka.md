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

ZIO Kafka bietet eine rein funktionale Kafka-Integration auf Basis von ZIO Streams. Der Ansatz umhüllt den Standard-Java-Client und ergänzt ihn um explizite Fehlerbehandlung, komponierbare Ressourcenverwaltung und typsichere Effektverfolgung.

## Wichtige Fakten {#key-facts}

- ZIO-Typsignatur: `ZIO[R, E, A]` - R = Umgebung (Environment), E = Fehlertyp, A = Erfolgstyp
- ZStream folgt demselben Muster: `ZStream[R, E, A]`
- Funktionen werfen niemals Exceptions. Fehler werden als Werte zurückgegeben und explizit behandelt.
- Effekte sind lazy: Zuerst wird die Berechnung definiert, bei Bedarf ausgeführt.
- `ZLayer` für Dependency Injection: komponierbare Module, die Services bereitstellen
- Offset-Verwaltung ist in die Stream-Pipeline integriert
- Backpressure ist über ZStream-Operatoren eingebaut

## Muster {#patterns}

### ZIO Kafka Producer {#zio-kafka-producer}

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

### ZIO Kafka Consumer {#zio-kafka-consumer}

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

### Vergleich: Akka vs. Spring vs. ZIO {#comparison-akka-vs-spring-vs-zio}

| Aspekt | Akka/Alpakka | Spring Kafka | ZIO Kafka |
|--------|-------------|--------------|-----------|
| Sprache | Scala/Java | Java | Scala |
| Paradigma | Actor-Modell | Annotationen/DI | Funktionale Effekte |
| Fehlerbehandlung | Supervision | try-catch | Effekt-Typen |
| Backpressure | Eingebaut | N/A | Eingebaut |
| Lernkurve | Hoch | Mittel | Hoch |

## Siehe auch {#see-also}

- [[alpakka-kafka]] - Alternative mit Akka Streams
- [[spring-kafka]] - Alternative mit Spring Boot
- [[kafka-streams]] - native Kafka-Stream-Verarbeitung
- [ZIO Kafka GitHub](https://github.com/zio/zio-kafka)
