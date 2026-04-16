---
title: gRPC API Design
category: reference
tags: [grpc, protobuf, http2, rpc, binary-protocol, microservices]
---

# gRPC API Design

gRPC is an open-source RPC framework created by Google (2016). It uses Protocol Buffers as its data exchange format over HTTP/2. Ideal for high-performance microservice-to-microservice communication where JSON overhead is unacceptable.

## Architecture

Client calls a method on the server as if it were a local function. The `.proto` file defines the service interface. Code generators produce client stubs and server skeletons from the proto definition.

```sql
[Client Stub] --binary over HTTP/2--> [Server Skeleton]
     |                                       |
  generated from .proto              generated from .proto
```

## Protocol Buffers (Protobuf)

Binary serialization format. More compact and faster than JSON/XML. Field numbers (not names) are transmitted.

```protobuf
syntax = "proto3";

service Hello {
  rpc SayHi (HiRequest) returns (HiReply);
}

message HiRequest {
  string name = 1;
}

message HiReply {
  string message = 1;
}

message Client {
  string name = 1;
  int32 id = 2;
  bool has_car = 3;
}
```

The proto file must exist on both client and server. Field types: `string`, `int32`, `int64`, `bool`, `float`, `double`, `bytes`, nested messages.

## Four Communication Patterns

| Pattern | Description |
|---------|-------------|
| **Unary** | Single request, single response (like REST) |
| **Server streaming** | Single request, stream of responses |
| **Client streaming** | Stream of requests, single response |
| **Bidirectional streaming** | Both sides stream simultaneously |

## HTTP/2 Foundation

gRPC requires HTTP/2 features:
- **Multiplexing** - multiple requests over single connection
- **Header compression** (HPACK) - reduces overhead
- **Binary framing** - more efficient than text-based HTTP/1.1
- **Server push** - proactive data sending
- **Stream prioritization** - important requests first

## Advantages

- **High performance** - lightweight binary protocol, faster than JSON-based REST
- **Interoperability** - multi-language support through code generation
- **Strongly typed contracts** - protobuf schemas provide clear, type-safe interfaces
- **Bidirectional streaming** - real-time data in both directions
- **Code generation** - auto-generated client/server code from proto files

## Disadvantages

- **Limited browser support** - requires gRPC-Web proxy for browsers
- **Debugging difficulty** - binary format harder to inspect than JSON
- **Versioning complexity** - proto schema changes require careful management
- **Smaller ecosystem** - less tooling and community than REST
- **Custom error handling** - uses its own error codes, unfamiliar to some developers

## When to Use

- High-performance microservice-to-microservice (internal APIs)
- Bidirectional streaming (real-time data, chat, monitoring)
- Polyglot environments (services in different languages)
- Latency-sensitive applications

## When NOT to Use

- Public-facing APIs (browser clients)
- Simple CRUD operations
- Small projects with minimal services
- When human-readable payloads are needed for debugging

## Gotchas

- **Only ~45% of websites** support HTTP/2 despite 2015 release - verify infrastructure compatibility
- **Proto schema evolution** - never reuse field numbers (deleted fields), only add new fields with new numbers
- **gRPC-Web** adds a proxy layer between browser and gRPC server, adding latency and complexity
- **Load balancing** - gRPC uses long-lived HTTP/2 connections, so L4 load balancers don't distribute well. Use L7 or client-side balancing
- **Tool:** json-to-proto.github.io for proto file conversion

## See Also

- [[http-rest-fundamentals]] - REST comparison, HTTP protocol
- [[graphql-api]] - Alternative query-based API style
- [[data-serialization-formats]] - JSON, XML, Protobuf comparison
- [[microservices-communication]] - Inter-service communication patterns
