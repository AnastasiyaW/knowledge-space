---
title: "Alpakka Kafka (Akka Streams)"
category: reference
tags: [kafka, akka, alpakka, reactive-streams, backpressure, scala, graph-dsl]
level: 3
source_sha256: 8458e1cdec21adb676b6863d1ff5214fa598b1d7ed14e686657b5c7fd89c810c
translation: machine
translated_at: '2026-10-24'
---
# Alpakka Kafka (Akka Streams) {#alpakka-kafka-akka-streams}

Alpakka Kafka verbindet Kafka-Topics mit Akka-Streams-Pipelines und bietet reaktives Backpressure, Graph DSL für komplexe Topologien sowie nicht blockierende asynchrone Verarbeitung auf der JVM.

## Key Facts {#key-facts}

- Akka Streams implementiert die Reactive-Streams-Spezifikation mit Backpressure
- Kernkomponenten: **Source** (erzeugt), **Flow** (transformiert), **Sink** (konsumiert)
- Der **Materializer** führt den Stream-Graphen mithilfe des Actor-Systems aus
- Backpressure: Ist der Konsument langsamer als der Produzent, wird das Signal stromaufwärts weitergegeben; die Source liest nie schneller, als die Sink verarbeiten kann
- Alle Stream-Komponenten laufen standardmäßig in einem einzigen Actor (Fusion-Optimierung)
- Das Graph DSL ermöglicht komplexe Topologien: Broadcast (Fan-out), Zip (Fan-in), Merge
- Alpakka stellt Kafka Source und Sink mit integrierter Backpressure-Unterstützung bereit

## Patterns {#patterns}

### Akka Streams Pipeline {#akka-streams-pipeline}

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

### Graph DSL (Complex Topology) {#graph-dsl-complex-topology}

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

### Alpakka Kafka Producer/Consumer {#alpakka-kafka-producerconsumer}

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

### Configuration (application.conf) {#configuration-applicationconf}

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

## Gotchas {#gotchas}

- **Immer aus `akka.actor.typed` importieren** - das Mischen von typisiertem und untypisiertem Akka führt zu schwer nachvollziehbaren Fehlern
- **Materializer erforderlich** - der Stream-Graph ist lazy; es passiert nichts, bis `run()` mit einem Materializer aufgerufen wird
- **Graph DSL erfordert ClosedShape** - alle Ein- und Ausgänge müssen verbunden sein, bevor der Graph ausgeführt werden kann

## See Also {#see-also}

- [[kafka-streams]] - Kafkas native Stream-Processing-Bibliothek (Java)
- [[zio-kafka]] - Alternative mit funktionalen Effekten (Scala)
- [[spring-kafka]] - annotationsbasierte Alternative (Java)
- [Alpakka Kafka Documentation](https://doc.akka.io/docs/alpakka-kafka/current/)
