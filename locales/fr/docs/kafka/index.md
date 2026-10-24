---
title: "Kafka et files de messages"
type: MOC
level: 3
source_sha256: 435a580e2d2b0365545772cdef275bf6602a1ab2c83732d14cc5fb0cf5403b2b
translation: machine
translated_at: '2026-10-24'
---
# Kafka et files de messages {#kafka-message-queues}

## Concepts fondamentaux {#core-concepts}
- [[broker-architecture]] - Cluster de brokers, élection du contrôleur (ZooKeeper/KRaft), segments de log, rétention
- [[topics-and-partitions]] - Topics, partitions, ordre, routage par clé, politiques de nettoyage
- [[consumer-groups]] - Protocole de groupe, affectation des partitions, gestion des offsets, rééquilibrage
- [[kafka-replication-fundamentals]] - ISR, HW/LEO, acks + min.insync.replicas
- [[kafka-fault-tolerance]] - Élection de leader non propre, réplication tenant compte des racks, patterns multi-DC

## Traitement de flux {#stream-processing}
- [[kafka-streams]] - KStream/KTable, opérations avec état, fenêtrage, jointures, exactly-once, requêtes interactives
- [[ksqldb]] - SQL sur les flux, requêtes push/pull, agrégations fenêtrées, requêtes persistantes

## Intégration {#integration}
- [[kafka-connect]] - Connecteurs source/sink, SMT, API REST, DLQ, gestion des erreurs
- [[schema-registry]] - Évolution des schémas, modes de compatibilité, Avro/Protobuf/JSON Schema, stratégies de subject

## Patterns et bonnes pratiques {#patterns-best-practices}
- [[kafka-producer-fundamentals]] - Modes d'acks, batching, compression, retries, patterns d'envoi
- [[kafka-producer-advanced-patterns]] - Partitioners personnalisés, headers, intercepteurs, backpressure, producer idempotent
- [[kafka-transactions]] - Producer idempotent, API transactionnelle, sémantique exactly-once, zombie fencing

## Exploitation et sécurité {#operations-security}
- [[kafka-cluster-management]] - Dimensionnement, mises à jour progressives, panne de disque, réaffectation des partitions
- [[kafka-monitoring-and-tuning]] - Métriques JMX, Prometheus/Grafana, optimisation OS/JVM/broker
- [[kafka-backup-and-dr]] - MirrorMaker 2, stratégies de sauvegarde, patterns de reprise après sinistre
- [[kafka-security]] - SSL/TLS, SASL, ACL, listeners, RBAC, journalisation d'audit

## Références complémentaires {#additional-references}

- [[admin-api]] - L'API d'administration (bibliothèque kafka-clients) fournit une gestion programmatique du cluster pour les topics, les consumer
- [[alpakka-kafka]] - Alpakka Kafka connecte les topics Kafka aux pipelines Akka Streams, avec backpressure réactif
- [[confluent-rest-proxy]] - Le Confluent REST Proxy fournit une interface HTTP vers Kafka (port par défaut 8082), permettant
- [[consumer-configuration]] - Référence complète des paramètres de configuration du consumer Kafka avec valeurs par défaut, recommandations de réglage
- [[cqrs-pattern]] - CQRS (Command Query Responsibility Segregation) sépare le chemin d'écriture (Command API avec event
- [[delivery-semantics]] - Kafka prend en charge trois sémantiques de livraison - at-most-once, at-least-once et exactly-once - chacune avec
- [[docker-development-setup]] - Configurations Docker Compose minimales pour le développement local de Kafka en mode KRaft (sans ZooKeeper)
- [[event-sourcing]] - L'event sourcing stocke chaque changement d'état sous forme d'événement immuable dans Kafka plutôt que d'écraser
- [[idempotent-producer]] - Le producer idempotent attribue un PID (Producer ID) et des numéros de séquence à chaque message, permettant
- [[kafka-messaging-fundamentals]] - Garanties de livraison Kafka, mécanique des consumer groups, stratégies de rééquilibrage, et intégration
- [[kafka-monitoring]] - Kafka expose ses métriques via JMX
- [[kafka-queues-v4]] - Kafka 4.0 introduit la sémantique de work queue où chaque message est traité par un seul consumer dans un
- [[kafka-streams-state-stores]] - Les state stores fournissent un stockage clé-valeur local par tâche Kafka Streams, adossé à RocksDB sur disque et
- [[kafka-streams-time-semantics]] - La sémantique temporelle du traitement de flux, basée sur le modèle Google Dataflow, définit comment les événements sont regroupés
- [[kafka-streams-windowing]] - Les opérations fenêtrées regroupent les enregistrements d'un flux dans des intervalles de temps finis pour l'agrégation, en prenant en charge
- [[kafka-troubleshooting]] - Problèmes courants de Kafka associés aux symptômes, causes racines et correctifs, côté producer et
- [[messaging-models]] - Il existe trois modèles de messagerie fondamentaux dans les systèmes distribués
- [[mirrormaker]] - MirrorMaker 2 (MM2) réplique des topics entre clusters Kafka pour la reprise après sinistre et
- [[nats-comparison]] - NATS est un système de messagerie léger à trois couches (Core, JetStream, Clustering), offrant
- [[offsets-and-commits]] - Un offset est un numéro de message séquentiel au sein d'une partition, attribué à l'écriture
- [[partitioning-strategies]] - Le partitionnement Kafka détermine comment les messages sont répartis entre les partitions par hachage de clé
- [[rebalancing-deep-dive]] - Le rééquilibrage est le processus de redistribution des affectations de partitions entre les consumers d'un groupe
- [[saga-pattern]] - Le pattern Saga gère les transactions distribuées entre microservices via Kafka en utilisant soit
- [[spring-kafka]] - Spring Kafka fournit une intégration Kafka déclarative basée sur les annotations, avec KafkaTemplate pour
- [[transactional-outbox]] - Le pattern Transactional Outbox écrit les événements dans une table outbox au sein de la même base de données
- [[zero-copy-and-disk-io]] - Kafka atteint un haut débit grâce aux I/O disque séquentielles, à l'utilisation du page cache de l'OS, et
- [[zio-kafka]] - ZIO Kafka fournit une intégration Kafka purement fonctionnelle avec ZIO Streams, en encapsulant le standard
