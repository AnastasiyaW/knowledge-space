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

Alpakka Kafka relie les topics Kafka aux pipelines Akka Streams, en fournissant une contre-pression réactive, un Graph DSL pour les topologies complexes et un traitement asynchrone non bloquant sur la JVM.

## Points clés {#key-facts}

- Akka Streams implémente la spécification Reactive Streams avec contre-pression
- Composants principaux : **Source** (produit), **Flow** (transforme), **Sink** (consomme)
- Le **Materializer** exécute le graphe de flux en utilisant le système d'acteurs
- Contre-pression : lorsque le consommateur est plus lent que le producteur, le signal remonte en amont ; la source ne lit jamais plus vite que le sink ne peut traiter
- Tous les composants de flux s'exécutent dans un seul acteur par défaut (optimisation de fusion)
- Le Graph DSL permet des topologies complexes : broadcast (fan-out), zip (fan-in), merge
- Alpakka fournit une Source et un Sink Kafka avec une intégration native de la contre-pression

## Patterns {#patterns}

### Pipeline Akka Streams {#akka-streams-pipeline}

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

### Graph DSL (topologie complexe) {#graph-dsl-complex-topology}

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

### Producteur/Consommateur Alpakka Kafka {#alpakka-kafka-producerconsumer}

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

## Pièges à éviter {#gotchas}

- **Toujours importer depuis `akka.actor.typed`** - mélanger Akka typé et non typé produit des erreurs obscures
- **Materializer requis** - le graphe de flux est paresseux ; rien ne se passe tant que `run()` n'est pas appelé avec un Materializer
- **Le Graph DSL exige ClosedShape** - toutes les entrées et sorties doivent être connectées avant que le graphe puisse s'exécuter

## Voir aussi {#see-also}

- [[kafka-streams]] - bibliothèque native de traitement de flux de Kafka (Java)
- [[zio-kafka]] - alternative à base d'effets fonctionnels (Scala)
- [[spring-kafka]] - alternative basée sur les annotations (Java)
- [Documentation Alpakka Kafka](https://doc.akka.io/docs/alpakka-kafka/current/)
