---
title: API Design Process
category: patterns
tags: [api, rest, graphql, grpc, openapi, versioning]
---
# API Design Process

A systematic algorithm for designing APIs that connects business requirements to technical implementation through user stories, data flow analysis, and protocol selection.

## Key Facts

- API design is context-dependent: a blockchain exchange API differs from a government services API
- Start from User Stories and BPMN diagrams, NOT from endpoints
- Choose protocol based on requirements: REST for CRUD/public APIs, gRPC for internal service-to-service, GraphQL for complex client-driven queries
- Stateless vs stateful: determine early whether the server needs to maintain request state
- Document everything: API spec (OpenAPI/Swagger) is the contract between teams
- API is just one component of a web service - architecture, data models, auth, and business processes all need documentation
- See [[system-design-template]] for the broader architecture context APIs fit into
- See [[data-serialization-formats]] for JSON/XML/Protobuf considerations

## Patterns

### API design algorithm

```
1. Collect User Stories + business process diagrams
2. Extract functional requirements from stories
3. Identify non-functional requirements:
   - Scalability, performance, security
   - Stateless or stateful?
4. Choose architectural style + protocol:
   - REST + HTTP/HTTPS
   - gRPC + HTTP/2
   - GraphQL + HTTP
   - WebSocket for bidirectional real-time
5. Analyze data flow (DFD diagrams)
6. Choose data format: JSON, XML, Protobuf
7. Define resources/endpoints:
   - REST: nouns as resources, HTTP verbs as operations
   - gRPC: service definitions + methods
8. Design use case scenarios
9. Create UML activity diagrams for key flows
10. Define request/response schemas:
    - Pagination, filtering, sorting
    - Error response format
    - Versioning strategy
```

### Protocol comparison

| Criterion | REST | gRPC | GraphQL |
|-----------|------|------|---------|
| Data format | JSON/XML | Protobuf | JSON |
| Transport | HTTP/1.1+ | HTTP/2 | HTTP |
| Contract | OpenAPI | .proto files | Schema |
| Streaming | No (SSE possible) | Bidirectional | Subscriptions |
| Browser support | Native | Needs proxy | Native |
| Caching | HTTP caching | No standard | Client-side |
| Best for | Public APIs | Internal services | Flexible queries |
| Payload size | Larger | Compact (binary) | Variable |

### REST API versioning strategies

```
1. URL path versioning (most common):
   GET /api/v1/orders
   GET /api/v2/orders
   + Clear, cacheable
   - New version = new URL space

2. Header versioning:
   GET /api/orders
   Accept: application/vnd.myapi.v2+json
   + Clean URLs
   - Harder to test (curl needs headers)

3. Query parameter:
   GET /api/orders?version=2
   + Easy to test
   - Pollutes query params

Deprecation process:
  1. Mark old API as deprecated (Deprecation header)
  2. Announce timeline: "Will be removed in Q3 2025"
  3. Monitor usage of deprecated endpoints
  4. Remove after grace period
```

### Idempotency

```
Idempotent: calling N times = same result as calling once

GET    - always idempotent (read-only)
PUT    - idempotent (full replace)
DELETE - idempotent (already deleted = success)
POST   - NOT idempotent by default

Making POST idempotent:
  Client sends: POST /orders
    Idempotency-Key: "uuid-12345"
  Server checks: have I processed uuid-12345?
    Yes -> return cached response
    No  -> process, store result keyed by uuid-12345
```

### OpenAPI/Swagger workflow

```yaml
openapi: "3.0.0"
info:
  title: Order Service API
  version: "1.0"
paths:
  /orders:
    get:
      summary: List orders
      parameters:
        - name: status
          in: query
          schema:
            type: string
            enum: [pending, completed, cancelled]
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Order'
```

## Gotchas

- **Symptom**: API change breaks existing clients -> **Cause**: No versioning strategy, breaking changes in existing endpoints -> **Fix**: Adopt URL versioning from day one. All breaking changes go to new version. Old version maintained during deprecation period
- **Symptom**: N+1 API calls from frontend for a single page -> **Cause**: Over-normalized REST resources, no aggregation layer -> **Fix**: Add [[bff-pattern]] or consider GraphQL for complex aggregation needs
- **Symptom**: API endpoint does everything (GET /api?action=create&type=order) -> **Cause**: RPC-style thinking applied to REST -> **Fix**: Model as resources: POST /orders to create, GET /orders/{id} to read. REST = nouns + HTTP verbs
- **Symptom**: API documentation is always outdated -> **Cause**: Documentation maintained separately from code -> **Fix**: Generate OpenAPI spec from code annotations (or code-first approach). Spec is the source of truth

## See Also

- [[system-design-template]] - API design is one step in the broader process
- [[data-serialization-formats]] - JSON vs XML vs Protobuf for API payloads
- [[bff-pattern]] - Backend-for-Frontend for API aggregation
- [[orchestration-vs-choreography]] - How APIs connect to service interaction patterns
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- Microsoft: [API Design Best Practices](https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design)
- Martin Fowler: [Richardson Maturity Model](https://martinfowler.com/articles/richardsonMaturityModel.html)
