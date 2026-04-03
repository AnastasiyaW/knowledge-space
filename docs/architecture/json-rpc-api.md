---
title: JSON-RPC API Design
category: reference
tags: [json-rpc, rpc, api, protocol]
---

# JSON-RPC API Design

JSON-RPC is a lightweight RPC protocol encoded in JSON. Client sends function name and parameters; server executes and returns result. All requests go to a single endpoint. Current version: 2.0.

## Request/Response Format

```json
// Request
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "getMenu",
  "params": {"category": "pizza"}
}

// Success response
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {"items": ["Margherita", "Pepperoni"]}
}

// Error response
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {"code": -32601, "message": "Method not found"}
}
```

Fields: `jsonrpc` (required, "2.0"), `id` (unique request ID), `method` (function name), `params` (optional).

## Standard Error Codes

| HTTP | JSON-RPC Code | Meaning |
|------|--------------|---------|
| 500 | -32700 | Parse error |
| 400 | -32600 | Invalid request |
| 404 | -32601 | Method not found |
| 500 | -32602 | Invalid params |
| 500 | -32603 | Internal error |
| 500 | -32099..-32000 | Custom server errors |

Spec: https://www.jsonrpc.org/specification

## Batch Requests

JSON-RPC natively supports batch requests - multiple operations in single HTTP request. More elegant than REST where each operation typically requires separate request.

## Advantages

- **Lightweight and performant** - compact JSON, fast for small data
- **Simple implementation** - straightforward structure, params in body only
- **Transport independence** - HTTP, TCP, WebSocket
- **Native batch support** - multiple operations per request

## Disadvantages

- **No built-in caching** - even showing same data twice requires new request
- **Limited error handling** - server returns HTTP 200 for business errors
- **No standard for complex schemas** - less mature than REST/GraphQL

## When to Use

- Internal service-to-service communication
- Blockchain projects (Ethereum JSON-RPC)
- IoT APIs (sensor -> controller)
- Simple open APIs (chat messengers)
- High-performance complex operations

## Gotchas

- **HTTP 200 for errors** - client must inspect response body, not just status code
- **No caching** means higher server load for repeated queries
- **Parameter passing** - positional (array) vs named (object). Named is more readable; positional requires less code

## See Also

- [[http-rest-fundamentals]] - REST vs JSON-RPC comparison
- [[async-event-apis]] - WebSocket transport for JSON-RPC
