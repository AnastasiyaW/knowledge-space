---
title: "Apache Kafka"
category: tools
tags: [data-engineering, kafka, streaming, pubsub, message-broker, event-driven]
level: 2
source_sha256: bcc94e3cd20e0442924f9913b79e78331a80163e59682fe63253fd1944de219b
translation: machine
translated_at: '2026-10-24'
---
# Apache Kafka {#apache-kafka}

Apache Kafka est une plateforme distribuée de streaming d'événements. Elle découple les producteurs des consommateurs grâce à un broker de messages persistant, ce qui permet de construire des pipelines de données à haut débit et tolérants aux pannes, ainsi que des analyses en temps réel.

## Pourquoi PubSub {#why-pubsub}

La communication directe entre clients échoue lorsque :
- Le consommateur est hors ligne (le producteur n'a nulle part où envoyer les messages)
- Plusieurs consommateurs ont besoin des mêmes événements
- Le producteur doit connaître à l'avance tous les consommateurs

**Solution :** les éditeurs envoient les messages au broker, et les abonnés les lisent depuis le broker.

**Alternatives :** RabbitMQ, Apache Pulsar, AWS Kinesis, GCP Pub/Sub

## Architecture {#architecture}

| Composant | Rôle |
|-----------|------|
| **Brokers** | Serveurs qui stockent les messages |
| **Producers** | Envoient des messages vers des topics |
| **Consumers** | Lisent les messages depuis des topics |
| **Topics** | Séparation logique des types de messages |
| **Partitions** | Topics découpés en partitions ordonnées ; chaque message reçoit un offset |
| **Consumer groups** | Plusieurs consommateurs partageant la charge sur un topic |

## Propriétés clés {#key-properties}
- Haut débit, scalabilité horizontale
- Stockage persistant (rétention configurable : de quelques jours à plusieurs mois)
- Les messages sont ordonnés au sein d'une partition (et non entre partitions)
- Les groupes de consommateurs permettent une consommation en parallèle

## Cas d'usage {#use-cases}
- Messagerie entre services
- Supervision et analyse en temps réel
- Agrégation de logs
- Collecte de métriques
- Event sourcing

## À ne pas utiliser Kafka pour {#what-kafka-is-not-for}
- Stockage à long terme (utiliser un véritable entrepôt de données, DWH)
- Constitution de jeux de données d'entraînement (transférer d'abord les données vers un stockage)
- Transformations complexes (utiliser Spark/Flink en aval)

## Outillage {#tooling}
- **Kafka Tool / Offset Explorer** - interface graphique pour parcourir les brokers, topics et partitions
- **Confluent Platform** - Kafka managé avec outils supplémentaires (Schema Registry, ksqlDB)
- **KafkaStreams** - bibliothèque légère de traitement de flux

## Intégration avec Spark {#integration-with-spark}

```python
# Spark Structured Streaming from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "host:9092") \
    .option("subscribe", "topic_name") \
    .load()
```

## Pièges courants {#gotchas}
- Les messages ne sont ordonnés qu'au sein d'une partition, pas entre partitions
- Le retard des consommateurs (consumer lag) doit être surveillé, car les consommateurs peuvent se laisser distancer par les producteurs
- Le nombre de partitions ne peut pas être réduit après création
- La rétention est basée sur le temps ou sur la taille : les données disparaissent à l'issue de la période de rétention

## Voir aussi {#see-also}
- [[spark-streaming]] - moteur de traitement de flux
- [[etl-elt-pipelines]] - patterns de pipelines
- [[data-lineage-metadata]] - supervision du retard des consommateurs
