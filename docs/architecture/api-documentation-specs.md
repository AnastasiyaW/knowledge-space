---
title: API Documentation and Specifications
category: reference
tags: [openapi, swagger, wsdl, asyncapi, openrpc, api-first, documentation]
---

# API Documentation and Specifications

API is only one component of a web service. Complete documentation covers architecture, data models, business processes, authorization, and component relationship diagrams.

## API First vs Code First

| Approach | Process | Best For |
|----------|---------|----------|
| **API First** | Design spec before implementation | Large projects, public APIs, multi-team |
| **Code First** | Write code, generate docs | Quick prototypes, small teams, internal APIs |

**API First advantages:** better collaboration via central document, generate stubs/SDKs/docs from spec, consistency. **Disadvantage:** time-consuming upfront design.

## OpenAPI / Swagger (REST)

```yaml
openapi: "3.0.0"
info:
  title: "Task API"
  version: "1.0.0"
paths:
  /tasks/{id}:
    get:
      summary: "Get task by ID"
      operationId: "getTask"
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      responses:
        "200":
          description: "Success"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Task"
components:
  schemas:
    Task:
      type: object
      required: [id, title]
      properties:
        id:
          type: integer
        title:
          type: string
```

**Tools:** editor.swagger.io (editor), Swagger UI (interactive docs).

### REST API Design Algorithm
1. Determine data needed for each action/method
2. Define parameter sets per entity
3. Prune: remove unnecessary parameters, entities, merge endpoints
4. Design both request and response - fewer parameters = better usability

## WSDL (SOAP)

XML-based specification. Structure: `types` (XSD schemas), `message` (request/response structures), `portType` (operations), `binding` (protocol), `service` (endpoint address).

Key namespaces: `xmlns:soap`, `xmlns:tns`, `xmlns:xsd`.

## OpenRPC (JSON-RPC)

Standard for documenting JSON-RPC APIs (spec.open-rpc.org):
- `openrpc`: spec version
- `info`: version, title
- `servers`: name, URL with variables
- `methods[]`: name, params, result, errors, examples

**Parameter passing:** positional (array - server must know order) vs named (object - any order, more readable).

## AsyncAPI (Event-Driven)

For Kafka, RabbitMQ, WebSocket, MQTT:
- Defines channels (topics/queues)
- Message schemas
- Server bindings per protocol

## Protocol Buffers / Proto (gRPC)

IDL for gRPC services:
```protobuf
service Hello {
  rpc SayHi (HiRequest) returns (HiReply);
}
message HiRequest {
  string name = 1;
}
```

## Web Service Documentation Template

Complete docs should include: service name, maintainer contacts, description, repository link, API docs link, host URLs (test/prod), monitoring URLs, deployment instructions, changelog, architecture diagrams, entity/data model, business process diagrams, access control.

### Endpoint Specification Format
- Path, HTTP method, auth method, rate limits
- Parameters table: name, location (body/header/path/query), required, format, example
- Request example (JSON)
- Response status codes with descriptions
- Success/error response examples

## MIME Types

Format: `type/subtype` - `text/html`, `application/json`, `image/png`. Client sends `Accept` header; server responds with `Content-Type`. Essential for correct data interpretation.

## Gotchas

- **OpenAPI 3.0 vs 2.0 (Swagger)** - different structure, ensure correct version
- **`$ref` for reuse** - define schemas once in `components/schemas`, reference everywhere
- **WSDL is self-documenting** - give developers the file and they understand the API
- **AsyncAPI is young** - less tooling than OpenAPI but growing rapidly
- **Documentation drift** - API First prevents this; Code First requires discipline to keep docs current

## See Also

- [[http-rest-fundamentals]] - REST protocol and conventions
- [[soap-api]] - SOAP protocol and WSDL details
- [[graphql-api]] - Schema as documentation
- [[data-serialization-formats]] - JSON Schema, XSD, Protobuf
- [[api-testing-tools]] - Postman, cURL, DevTools
