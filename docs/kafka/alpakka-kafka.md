---
title: Alpakka Kafka (Akka Streams)
category: reference
tags: [kafka, akka, alpakka, reactive-streams, backpressure, scala, graph-dsl]
---

# Alpakka Kafka (Akka Streams)

Alpakka Kafka connects Kafka topics to Akka Streams pipelines, providing reactive backpressure, Graph DSL for complex topologies, and non-blocking asynchronous processing on the JVM.

## Key Facts

- Akka Streams implements Reactive Streams specification with backpressure
- Core components: **Source** (produces), **Flow** (transforms), **Sink** (consumes)
- **Materializer** executes the stream graph using the Actor system
- Backpressure: when consumer slower than producer, signal propagates upstream; source never reads faster than sink can process
- All stream components run in a single actor by default (fusion optimization)
- Graph DSL enables complex topologies: broadcast (fan-out), zip (fan-in), merge
- Alpakka provides Kafka Source and Sink with built-in backpressure integration

## Patterns

### Akka Streams Pipeline

```scala
implicit val system: ActorSystem = ActorSystem("my-system")
implicit val materializer: ActorMaterializer = ActorMaterializer()

// Simple pipeline
Source(1 to 100)
  .map(_ * 2)
  .filter(_ > 50)
  .runWith(Sink.foreach(println))

// Backpressure buffer
flow.buffer(size = 10, overflowStrategy = OverflowStrategy.dropHead)
// Strategies: dropHead, dropTail, dropBuffer, dropNew, backpressure, fail
```

### Graph DSL (Complex Topology)

```scala
val graph = RunnableGraph.fromGraph(GraphDSL.create() { implicit builder =>
  import GraphDSL.Implicits._
  val bcast = builder.add(Broadcast[Int](2))
  val zip = builder.add(Zip[Int, Int]())

  input ~> bcast
  bcast.out(0) ~> Flow[Int].map(_ + 1) ~> zip.in0
  bcast.out(1) ~> Flow[Int].map(_ * 10) ~> zip.in1
  zip.out ~> Sink.foreach[(Int, Int)](println)
  ClosedShape
})
graph.run()
```

### Alpakka Kafka Producer/Consumer

```scala
// Producer
val producerSettings = ProducerSettings(config, new StringSerializer, new StringSerializer)
Source(1 to 100)
  .map(i => new ProducerRecord[String, String]("topic", i.toString, s"msg-$i"))
  .runWith(Producer.plainSink(producerSettings))

// Consumer
val consumerSettings = ConsumerSettings(config, new StringDeserializer, new StringDeserializer)
  .withGroupId("my-group")
Consumer.plainSource(consumerSettings, Subscriptions.topics("topic"))
  .map(record => record.value())
  .runWith(Sink.foreach(println))
```

### Configuration (application.conf)

```hocon
akka.kafka.producer {
  kafka-clients { bootstrap.servers = "localhost:9092" }
}
akka.kafka.consumer {
  kafka-clients {
    bootstrap.servers = "localhost:9092"
    group.id = "my-group"
    auto.offset.reset = "earliest"
  }
}
```

## Gotchas

- **Always import from `akka.actor.typed`** - mixing typed/untyped Akka produces obscure errors
- **Materializer required** - stream graph is lazy; nothing happens until `run()` is called with a Materializer
- **Graph DSL requires ClosedShape** - all inputs and outputs must be connected before the graph can run

## See Also

- [[kafka-streams]] - Kafka's native stream processing library (Java)
- [[zio-kafka]] - functional effects alternative (Scala)
- [[spring-kafka]] - annotation-based alternative (Java)
- [Alpakka Kafka Documentation](https://doc.akka.io/docs/alpakka-kafka/current/)
