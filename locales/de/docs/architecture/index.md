---
title: "Softwarearchitektur"
type: MOC
level: 4
source_sha256: 357f263c33678c189bfbf8a97dad4899ddae2612a09cb5dd5d684ff1bd24c263
translation: machine
translated_at: '2026-10-24'
---
# Softwarearchitektur {#software-architecture}

Referenzwissen für Softwarearchitektur, Systemdesign, API-Design, Integrationsmuster und technische Führung.

## Projekte und Live-Systeme {#projects-and-live-systems}

- [[happyin-knowledge-space]] - Projektidentität, verifizierte Historie, Navigation, Deployment und Abgrenzung zu den Nachrichten
- [[news-development-graph]] - Geprüfte Nachrichtenstränge zu Projekten und Unternehmen sowie unveränderliche Brücke zum Knowledge Space
- [[news-research-knowledge-lifecycle]] - Zweisprachige Belege, praktische Rezepte, zeitlicher Status und Vertrag für den Abruf durch Agenten

## Architekturprozess und Führung {#architecture-process-leadership}

Der strukturierte Weg von den Geschäftsanforderungen zu technologischen Entscheidungen und die Menschen, die ihn vorantreiben.

- [[solution-architecture-process]] - Anforderungspipeline, Stakeholder-Analyse, NFRs, Trade-offs, Schätzung des Datenvolumens
- [[architecture-documentation]] - C4-Modell, ADRs, 4+1-Sichten, UML, ADD-Methode, Lieferreihenfolge
- [[boundary-driven-refactoring]] - Verantwortungs- und Konsumentengrenzen, begründete Abstraktionen, Migrationsnachweise und ausreichende Verifikation
- [[tech-lead-role]] - Rollengrenzen (Senior/Lead/Architekt), Autoritätsmodell, Karriereentwicklung, Soft Skills
- [[system-design-interviews]] - 7-Schritte-Prozess, Schätztabellen, Übungsaufgaben, Drei-Optionen-Regel

## Architekturstile und Muster {#architecture-styles-patterns}

Auswahl und Umsetzung des passenden Architekturstils für den jeweiligen Kontext.

- [[architectural-styles]] - Spektrum von Monolith bis Microservices, Migrationsstrategien, Strangler Fig
- [[microservices-communication]] - API Gateway, BFF, CQRS, Saga (Orchestrierung/Choreografie), Event Sourcing, Circuit Breaker
- [Design Patterns (GoF)](design-patterns-gof.md) - SOLID, Erzeugungs-, Struktur- und Verhaltensmuster, Leitfaden zur Musterauswahl
- [[microfrontends]] - Webpack Module Federation, Single-SPA, Integrationsmethoden, Kommunikation zwischen Modulen

## Verteilte Systeme {#distributed-systems}

Kerntheorie und Muster für den Aufbau zuverlässiger verteilter Systeme.

- [[distributed-systems-fundamentals]] - CAP-Theorem, PACELC, Konsistenzmodelle, Konsens (Raft/Paxos), Replikation, Partitionierung
- [[queueing-theory]] - Hockey-Stick-Kurve, M/M/1-Formeln, einzelne vs. mehrere Warteschlangen, Kapazitätsplanung
- [[quality-attributes-reliability]] - Verfügbarkeit (SLA-Neunen), Fehlertoleranz (MTTF/MTTR), Wiederherstellbarkeit (RTO/RPO), Chaos Engineering

## API-Design {#api-design}

Von den REST-Grundlagen bis zu spezialisierten Protokollen: Entwurf, Dokumentation und Test von APIs.

- [[http-rest-fundamentals]] - HTTP-Methoden, Statuscodes, REST-Constraints, Ressourcendesign, Vergleich von API-Stilen
- [[rest-api-advanced]] - Rate Limiting, HTTP-Caching-Strategien, Versionierung, Retry-Muster, Batch-Anfragen
- [[graphql-api]] - Schema (SDL), Queries/Mutations/Subscriptions, Resolver, Einsatzzweck
- [[grpc-api]] - Protocol Buffers, HTTP/2, vier Kommunikationsmuster, Einsatzzweck
- [[soap-api]] - XML-Envelopes, WSDL, WS-Security, Anwendungsfälle im Unternehmensumfeld
- [[json-rpc-api]] - Leichtgewichtiges RPC-Protokoll, Batch-Anfragen, Fehlercodes
- [[async-event-apis]] - WebSockets, SSE, Webhooks, Polling/Long-Polling, optimistisches/pessimistisches Locking
- [[api-authentication-security]] - OAuth 2.0, JWT, mTLS, Kryptografie, TLS-Handshake, digitale Signaturen
- [[api-documentation-specs]] - OpenAPI/Swagger, WSDL, AsyncAPI, OpenRPC, API First vs. Code First
- [[api-testing-tools]] - cURL, Postman, Chrome DevTools, Swagger UI, SoapUI

## Daten und Speicherung {#data-storage}

Auswahl der Datenbank, Datenformate, Caching und Performance-Optimierung.

- [[database-selection]] - OLTP/OLAP, Auswahl nach Datentyp, Normalisierung, Indizes, ACID, ORM, Query-Optimierung
- [[data-serialization-formats]] - JSON Schema, XSD, Protobuf, Vergleich XML vs. JSON vs. Binärformate
- [[caching-and-performance]] - Cache-Muster (Aside/Through/Behind), Redis vs. Memcached, CDN, Lastverteilung, Checkliste zur Optimierung

## Integration und Messaging {#integration-messaging}

Unternehmensintegration, Message Broker und ereignisgesteuerte Architektur.

- [[enterprise-integration]] - ESB, Integrationsstile, EIP-Routing- und Transformationsmuster, moderne Alternativen
- [[message-broker-patterns]] - Pub/Sub vs. Queue, Push vs. Pull, Zustellungsgarantien, Auswahl des Brokers
- [[kafka-architecture]] - Partitionen, Consumer Groups, Replikation, Acks, Datenpersistenz
- [[rabbitmq-architecture]] - Exchanges (Fanout/Direct/Topic/Headers), Queue-Typen, Ack/Nack, DLE

## Sicherheit und Betrieb {#security-operations}

Sicherheitsarchitektur, DevOps-Praktiken und betriebliche Belange.

- [[security-architecture]] - Checklisten für Anwendungs- und Datensicherheit, Workflow des Architekten, Zero Trust, Automatisierung
- [[devops-cicd]] - CI/CD-Pipeline, IaC, Docker/K8s, Deployment-Strategien, 12-Factor-App, Monitoring
- [[testing-and-quality]] - Testpyramide, Contract Testing, Chaos Engineering, Zusammenhang zwischen Qualität und Deployment
- [[bigdata-ml-architecture]] - Lambda/Kappa, Data Lake/Warehouse/Lakehouse, ML-Pipeline, MLOps, ETL vs. ELT

---

## Schnelle Entscheidungsbäume {#quick-decision-trees}

### „Welche Datenbank?“ {#which-database}
```rust
Need ACID transactions?       -> PostgreSQL
Need flexible schema?         -> MongoDB
Need >500K TPS writes?        -> Cassandra / ScyllaDB
Need sub-ms key lookups?      -> Redis
Need full-text search?        -> Elasticsearch
Need relationship traversal?  -> Neo4j
Need analytical aggregations? -> ClickHouse / BigQuery
```

### „Microservices oder Monolith?“ {#microservices-or-monolith}
```php
Team < 10, simple domain?     -> Monolith (or modular monolith)
Clear boundaries, need independence? -> Microservices
Unclear, need fast iteration? -> Start monolith, extract later (Strangler Fig)
```

### „Welcher API-Stil?“ {#which-api-style}
```php
Public/browser API?           -> REST (with OpenAPI)
Internal, performance critical? -> gRPC
Complex queries, client flexibility? -> GraphQL
Bidirectional real-time?      -> WebSocket (or gRPC streaming)
Simple internal RPC?          -> JSON-RPC
Enterprise, strict contracts? -> SOAP
```

### „Kafka oder RabbitMQ?“ {#kafka-or-rabbitmq}
```php
High volume event streaming?  -> Kafka
Need message replay?          -> Kafka
Flexible routing logic?       -> RabbitMQ
Simple task queues?           -> RabbitMQ
Request-response pattern?     -> RabbitMQ
```

## Weitere Referenzen {#additional-references}

- [[photoshop-plugin-architecture]] - Datum: 2026-04-03 Kontext: Entwicklung eines plattformübergreifenden (Mac + Windows) C++-ML-Inferenz-Plugins für
- [[write-buffering-patterns]] - Haltbarkeits- und Durchsatzmuster zum Abfangen von hochfrequenten Schreibvorgängen, bevor ein langsamer oder
