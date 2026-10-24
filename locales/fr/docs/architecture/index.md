---
title: "Architecture logicielle"
type: MOC
level: 4
source_sha256: 357f263c33678c189bfbf8a97dad4899ddae2612a09cb5dd5d684ff1bd24c263
translation: machine
translated_at: '2026-10-24'
---
# Architecture logicielle {#software-architecture}

Base de connaissances de référence sur l'architecture logicielle, la conception de systèmes, la conception d'API, les patrons d'intégration et le leadership technique.

## Projets et systèmes en production {#projects-and-live-systems}

- [[happyin-knowledge-space]] - Identité du projet, historique vérifié, navigation, déploiement et frontière avec les actualités
- [[news-development-graph]] - Fils d'actualités projet/entreprise relus et pont immuable vers le Knowledge Space
- [[news-research-knowledge-lifecycle]] - Preuves bilingues, recettes pratiques, statut temporel et contrat de récupération pour agents

## Processus d'architecture et leadership {#architecture-process-leadership}

L'approche structurée, depuis les exigences métier jusqu'aux choix technologiques, et les personnes qui la conduisent.

- [[solution-architecture-process]] - Pipeline d'exigences, analyse des parties prenantes, NFR, compromis, estimation du volume de données
- [[architecture-documentation]] - Modèle C4, ADR, vues 4+1, UML, méthode ADD, séquence de livraison
- [[boundary-driven-refactoring]] - Frontières de propriété et de consommateurs, abstractions justifiées, preuves de migration et vérification suffisante
- [[tech-lead-role]] - Frontières du rôle (senior/lead/architecte), modèle d'autorité, évolution de carrière, soft skills
- [[system-design-interviews]] - Processus en 7 étapes, tables d'estimation, exercices pratiques, règle des trois options

## Styles et patrons d'architecture {#architecture-styles-patterns}

Choisir et mettre en œuvre le style d'architecture adapté à votre contexte.

- [[architectural-styles]] - Du monolithe aux microservices, stratégies de migration, Strangler Fig
- [[microservices-communication]] - API Gateway, BFF, CQRS, Saga (orchestration/chorégraphie), Event Sourcing, Circuit Breaker
- [Patrons de conception (GoF)](design-patterns-gof.md) - SOLID, patrons créationnels/structurels/comportementaux, guide de sélection des patrons
- [[microfrontends]] - Webpack Module Federation, Single-SPA, méthodes d'intégration, communication inter-modules

## Systèmes distribués {#distributed-systems}

Théorie fondamentale et patrons pour construire des systèmes distribués fiables.

- [[distributed-systems-fundamentals]] - Théorème CAP, PACELC, modèles de cohérence, consensus (Raft/Paxos), réplication, partitionnement
- [[queueing-theory]] - Courbe en crosse de hockey, formules M/M/1, files simples vs multiples, planification de capacité
- [[quality-attributes-reliability]] - Disponibilité (nombre de neuf du SLA), tolérance aux pannes (MTTF/MTTR), récupérabilité (RTO/RPO), chaos engineering

## Conception d'API {#api-design}

Des fondamentaux REST aux protocoles spécialisés : concevoir, documenter et tester des API.

- [[http-rest-fundamentals]] - Méthodes HTTP, codes de statut, contraintes REST, conception des ressources, comparaison des styles d'API
- [[rest-api-advanced]] - Limitation de débit, stratégies de cache HTTP, versionnement, patrons de reprise, requêtes par lot
- [[graphql-api]] - Schéma (SDL), requêtes/mutations/abonnements, resolvers, quand l'utiliser
- [[grpc-api]] - Protocol Buffers, HTTP/2, quatre modes de communication, quand l'utiliser
- [[soap-api]] - Enveloppes XML, WSDL, WS-Security, cas d'usage en entreprise
- [[json-rpc-api]] - Protocole RPC léger, requêtes par lot, codes d'erreur
- [[async-event-apis]] - WebSockets, SSE, webhooks, polling/long-polling, verrouillage optimiste/pessimiste
- [[api-authentication-security]] - OAuth 2.0, JWT, mTLS, cryptographie, handshake TLS, signatures numériques
- [[api-documentation-specs]] - OpenAPI/Swagger, WSDL, AsyncAPI, OpenRPC, API First vs Code First
- [[api-testing-tools]] - cURL, Postman, Chrome DevTools, Swagger UI, SoapUI

## Données et stockage {#data-storage}

Choix de base de données, formats de données, mise en cache et optimisation des performances.

- [[database-selection]] - OLTP/OLAP, choix selon le type de données, normalisation, index, ACID, ORM, optimisation des requêtes
- [[data-serialization-formats]] - JSON Schema, XSD, Protobuf, comparaison XML vs JSON vs binaire
- [[caching-and-performance]] - Patrons de cache (aside/through/behind), Redis vs Memcached, CDN, répartition de charge, liste de contrôle d'optimisation

## Intégration et messagerie {#integration-messaging}

Intégration d'entreprise, courtiers de messages et architecture orientée événements.

- [[enterprise-integration]] - ESB, styles d'intégration, patrons de routage/transformation EIP, alternatives modernes
- [[message-broker-patterns]] - Pub/sub vs file d'attente, push vs pull, garanties de livraison, choix du courtier
- [[kafka-architecture]] - Partitions, groupes de consommateurs, réplication, acks, persistance des données
- [[rabbitmq-architecture]] - Exchanges (fanout/direct/topic/headers), types de files, ack/nack, DLE

## Sécurité et exploitation {#security-operations}

Architecture de sécurité, pratiques DevOps et enjeux opérationnels.

- [[security-architecture]] - Listes de contrôle sécurité applicative/données, démarche de l'architecte, Zero Trust, automatisation
- [[devops-cicd]] - Pipeline CI/CD, IaC, Docker/K8s, stratégies de déploiement, 12-factor app, supervision
- [[testing-and-quality]] - Pyramide de tests, tests de contrat, chaos engineering, lien qualité + déploiement
- [[bigdata-ml-architecture]] - Lambda/Kappa, data lake/entrepôt/lakehouse, pipeline ML, MLOps, ETL vs ELT

---

## Arbres de décision rapides {#quick-decision-trees}

### « Quelle base de données ? » {#which-database}
```rust
Need ACID transactions?       -> PostgreSQL
Need flexible schema?         -> MongoDB
Need >500K TPS writes?        -> Cassandra / ScyllaDB
Need sub-ms key lookups?      -> Redis
Need full-text search?        -> Elasticsearch
Need relationship traversal?  -> Neo4j
Need analytical aggregations? -> ClickHouse / BigQuery
```

### « Microservices ou monolithe ? » {#microservices-or-monolith}
```php
Team < 10, simple domain?     -> Monolith (or modular monolith)
Clear boundaries, need independence? -> Microservices
Unclear, need fast iteration? -> Start monolith, extract later (Strangler Fig)
```

### « Quel style d'API ? » {#which-api-style}
```php
Public/browser API?           -> REST (with OpenAPI)
Internal, performance critical? -> gRPC
Complex queries, client flexibility? -> GraphQL
Bidirectional real-time?      -> WebSocket (or gRPC streaming)
Simple internal RPC?          -> JSON-RPC
Enterprise, strict contracts? -> SOAP
```

### « Kafka ou RabbitMQ ? » {#kafka-or-rabbitmq}
```php
High volume event streaming?  -> Kafka
Need message replay?          -> Kafka
Flexible routing logic?       -> RabbitMQ
Simple task queues?           -> RabbitMQ
Request-response pattern?     -> RabbitMQ
```

## Références complémentaires {#additional-references}

- [[photoshop-plugin-architecture]] - Date : 2026-04-03 Contexte : Développement d'un plugin C++ d'inférence ML multiplateforme (Mac + Windows) pour
- [[write-buffering-patterns]] - Patrons de durabilité et de débit pour absorber les écritures à haute fréquence avant un(e) lent(e) ou
