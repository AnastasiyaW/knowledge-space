---
title: ZIO Kafka
category: reference
tags: [kafka, zio, scala, functional, effects, zstream, zio-kafka]
---

# ZIO Kafka

ZIO Kafka provides purely functional Kafka integration using ZIO Streams, wrapping the standard Java client with explicit error handling, composable resource management, and type-safe effect tracking.

## Key Facts

- ZIO type signature: `ZIO[R, E, A]` - R = environment, E = error type, A = success type
- ZStream follows same pattern: `ZStream[R, E, A]`
- Functions never throw exceptions - errors returned as values, handled explicitly
- Effects are lazy: define computation first, execute on demand
- `ZLayer` for dependency injection - composable modules providing services
- Offset management integrated into the stream pipeline
- Backpressure built-in via ZStream operators

## Patterns

### ZIO Kafka Producer

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

### ZIO Kafka Consumer

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

### Comparison: Akka vs Spring vs ZIO

| Aspect | Akka/Alpakka | Spring Kafka | ZIO Kafka |
|--------|-------------|--------------|-----------|
| Language | Scala/Java | Java | Scala |
| Paradigm | Actor model | Annotations/DI | Functional effects |
| Error handling | Supervision | try-catch | Effect types |
| Backpressure | Built-in | N/A | Built-in |
| Learning curve | High | Medium | High |

## See Also

- [[alpakka-kafka]] - Akka Streams alternative
- [[spring-kafka]] - Spring Boot alternative
- [[kafka-streams]] - native Kafka stream processing
- [ZIO Kafka GitHub](https://github.com/zio/zio-kafka)
