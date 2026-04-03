---
title: Software Architecture
type: MOC
---

# Software Architecture

Reference knowledge base for software architecture, system design, API design, integration patterns, and technical leadership.

## Architecture Process & Leadership

The structured approach from business requirements to technology choices, and the people who drive it.

- [[solution-architecture-process]] - Requirements pipeline, stakeholder analysis, NFRs, trade-offs, data volume estimation
- [[architecture-documentation]] - C4 model, ADRs, 4+1 views, UML, ADD method, delivery sequence
- [[tech-lead-role]] - Role boundaries (senior/lead/architect), authority model, career growth, soft skills
- [[system-design-interviews]] - 7-step process, estimation tables, practice exercises, three-option rule

## Architecture Styles & Patterns

Choosing and implementing the right architecture style for your context.

- [[architectural-styles]] - Monolith to microservices spectrum, migration strategies, Strangler Fig
- [[microservices-communication]] - API Gateway, BFF, CQRS, Saga (orchestration/choreography), Event Sourcing, Circuit Breaker
- [[design-patterns-gof]] - SOLID, creational/structural/behavioral patterns, pattern selection guide
- [[microfrontends]] - Webpack Module Federation, Single-SPA, integration methods, inter-module communication

## Distributed Systems

Core theory and patterns for building reliable distributed systems.

- [[distributed-systems-fundamentals]] - CAP theorem, PACELC, consistency models, consensus (Raft/Paxos), replication, partitioning
- [[queueing-theory]] - Hockey-stick curve, M/M/1 formulas, single vs multiple queues, capacity planning
- [[quality-attributes-reliability]] - Availability (SLA nines), fault tolerance (MTTF/MTTR), recoverability (RTO/RPO), chaos engineering

## API Design

From REST fundamentals to specialized protocols - designing, documenting, and testing APIs.

- [[http-rest-fundamentals]] - HTTP methods, status codes, REST constraints, resource design, API style comparison
- [[rest-api-advanced]] - Rate limiting, HTTP caching strategies, versioning, retry patterns, batch requests
- [[graphql-api]] - Schema (SDL), queries/mutations/subscriptions, resolvers, when to use
- [[grpc-api]] - Protocol Buffers, HTTP/2, four communication patterns, when to use
- [[soap-api]] - XML envelopes, WSDL, WS-Security, enterprise use cases
- [[json-rpc-api]] - Lightweight RPC protocol, batch requests, error codes
- [[async-event-apis]] - WebSockets, SSE, webhooks, polling/long-polling, optimistic/pessimistic locking
- [[api-authentication-security]] - OAuth 2.0, JWT, mTLS, cryptography, TLS handshake, digital signatures
- [[api-documentation-specs]] - OpenAPI/Swagger, WSDL, AsyncAPI, OpenRPC, API First vs Code First
- [[api-testing-tools]] - cURL, Postman, Chrome DevTools, Swagger UI, SoapUI

## Data & Storage

Database selection, data formats, caching, and performance optimization.

- [[database-selection]] - OLTP/OLAP, selection by data type, normalization, indexes, ACID, ORM, query optimization
- [[data-serialization-formats]] - JSON Schema, XSD, Protobuf, XML vs JSON vs binary comparison
- [[caching-and-performance]] - Cache patterns (aside/through/behind), Redis vs Memcached, CDN, load balancing, optimization checklist

## Integration & Messaging

Enterprise integration, message brokers, and event-driven architecture.

- [[enterprise-integration]] - ESB, integration styles, EIP routing/transformation patterns, modern alternatives
- [[message-broker-patterns]] - Pub/sub vs queue, push vs pull, delivery guarantees, broker selection
- [[kafka-architecture]] - Partitions, consumer groups, replication, acks, data persistence
- [[rabbitmq-architecture]] - Exchanges (fanout/direct/topic/headers), queue types, ack/nack, DLE

## Security & Operations

Security architecture, DevOps practices, and operational concerns.

- [[security-architecture]] - Application/data security checklists, architect's workflow, Zero Trust, automation
- [[devops-cicd]] - CI/CD pipeline, IaC, Docker/K8s, deployment strategies, 12-factor app, monitoring
- [[testing-and-quality]] - Testing pyramid, contract testing, chaos engineering, quality + deployment connection
- [[bigdata-ml-architecture]] - Lambda/Kappa, data lake/warehouse/lakehouse, ML pipeline, MLOps, ETL vs ELT

---

## Quick Decision Trees

### "Which database?"
```
Need ACID transactions?       -> PostgreSQL
Need flexible schema?         -> MongoDB
Need >500K TPS writes?        -> Cassandra / ScyllaDB
Need sub-ms key lookups?      -> Redis
Need full-text search?        -> Elasticsearch
Need relationship traversal?  -> Neo4j
Need analytical aggregations? -> ClickHouse / BigQuery
```

### "Microservices or monolith?"
```
Team < 10, simple domain?     -> Monolith (or modular monolith)
Clear boundaries, need independence? -> Microservices
Unclear, need fast iteration? -> Start monolith, extract later (Strangler Fig)
```

### "Which API style?"
```
Public/browser API?           -> REST (with OpenAPI)
Internal, performance critical? -> gRPC
Complex queries, client flexibility? -> GraphQL
Bidirectional real-time?      -> WebSocket (or gRPC streaming)
Simple internal RPC?          -> JSON-RPC
Enterprise, strict contracts? -> SOAP
```

### "Kafka or RabbitMQ?"
```
High volume event streaming?  -> Kafka
Need message replay?          -> Kafka
Flexible routing logic?       -> RabbitMQ
Simple task queues?           -> RabbitMQ
Request-response pattern?     -> RabbitMQ
```
