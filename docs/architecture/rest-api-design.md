---
title: REST API Design
category: api
tags: [architecture, rest, http, api-design]
---

# REST API Design

REST (Representational State Transfer) is an architectural style for distributed systems, not a protocol. It defines constraints for building scalable, maintainable web APIs that leverage existing HTTP infrastructure.

## HTTP Foundations

### Request/Response Structure

```
# Request
<METHOD> <URI> HTTP/<VERSION>
<Headers>
<Empty line>
<Body>

# Response
HTTP/<VERSION> <STATUS_CODE> <REASON>
<Headers>
<Empty line>
<Body>
```

### HTTP Methods

| Method | CRUD | Idempotent | Safe | Body | Cacheable |
|--------|------|------------|------|------|-----------|
| GET | Read | Yes | Yes | No | Yes |
| POST | Create | No | No | Yes | No |
| PUT | Full Update/Replace | Yes | No | Yes | No |
| PATCH | Partial Update | No* | No | Yes | No |
| DELETE | Delete | Yes | No | Optional | No |
| HEAD | Read headers only | Yes | Yes | No | Yes |
| OPTIONS | Get capabilities | Yes | Yes | No | No |

*PATCH can be made idempotent with proper implementation.

**Idempotent** = multiple identical requests produce same result. **Safe** = doesn't modify server state.

### Status Codes

| Range | Meaning | Common Codes |
|-------|---------|-------------|
| 1xx | Informational | 100 Continue |
| 2xx | Success | 200 OK, 201 Created, 204 No Content |
| 3xx | Redirection | 301 Moved Permanently, 304 Not Modified |
| 4xx | Client Error | 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 429 Too Many Requests |
| 5xx | Server Error | 500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable |

### Key Headers

**Request**: `Host` (required in HTTP/1.1), `Content-Type`, `Accept`, `Authorization`, `Cache-Control`, `User-Agent`

**Response**: `Content-Type`, `Content-Length`, `Cache-Control`, `ETag`, `Last-Modified`, `Set-Cookie`

### HTTP Versions

- **HTTP/1.0**: One request per TCP connection
- **HTTP/1.1**: Persistent connections (keep-alive), Host header, chunked transfer, pipelining
- **HTTP/2**: Binary framing, multiplexing, header compression (HPACK), server push
- **HTTP/3**: Based on QUIC (UDP), reduced latency, better mobile performance

## Six REST Constraints

1. **Client-Server**: Separation of concerns - client handles UI, server handles data/logic
2. **Stateless**: Each request contains all information needed to process it
3. **Cacheable**: Responses must declare themselves cacheable or non-cacheable
4. **Uniform Interface**: Resource identification via URIs, manipulation through representations, self-descriptive messages, HATEOAS
5. **Layered System**: Client can't tell if connected directly to server or through intermediary
6. **Code on Demand** (optional): Server can send executable code to client

## Resource Design

- Resources are **nouns**, not verbs: `/users`, `/orders`, `/products`
- Use **plurals**: `/users/123` not `/user/123`
- **Hierarchical**: `/users/123/orders/456`
- Actions via HTTP methods: `DELETE /users/123` not `POST /users/123/delete`
- **Naming**: lowercase, hyphens for multi-word (`/order-items`), no trailing slashes, no file extensions

### Resource Types

| Type | Description | ID Source |
|------|-------------|-----------|
| **Object** | Single resource with unique ID | - |
| **Collection** | Server-managed catalog | Server generates IDs |
| **Store** | Client-managed storage | Client assigns IDs |
| **Controller** | Action/function (RPC-like) | POST-based |

## Filtering, Pagination, Search

**Filtering**: `?status=active&created_after=2024-01-01`
**Sorting**: `?sort=created_at&order=desc`
**Search**: `?q=search+term`
**Pagination**:
- Offset-based: `?offset=20&limit=10` - simple, allows jumping to any page
- Cursor-based: `?cursor=abc123&limit=10` - stable with live data, cannot jump
- Page-based: `?page=3&per_page=10`

## Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable description",
    "details": [{"field": "email", "issue": "invalid format"}]
  }
}
```

Use appropriate HTTP status codes. Never expose internal details (stack traces, SQL) in production.

## File Transfer

Binary data with proper headers:
- Client: `Accept: image/png`
- Server: `Content-Type: image/png`, `Content-Disposition: attachment; filename="file.png"`

For large files: `Transfer-Encoding: chunked` - server sends data in pieces without knowing total size.

## CORS (Cross-Origin Resource Sharing)

Browser security mechanism. Server specifies allowed origins:
- `Access-Control-Allow-Origin`
- `Access-Control-Allow-Methods`
- `Access-Control-Allow-Headers`

Preflight requests (OPTIONS) sent for non-simple requests.

## Gotchas

- PUT means **full replacement** - must send entire resource, not partial
- POST is not idempotent - multiple calls create duplicates
- PATCH is not idempotent by default - use conditional headers for safety
- JSON has no native date type - use ISO 8601 strings
- Large numbers in JavaScript lose precision beyond 2^53 - use strings for big IDs

## See Also

- [[rest-api-advanced]] - caching, versioning, rate limiting, retries
- [[api-authentication-security]] - auth methods for REST APIs
- [[api-documentation-tools]] - OpenAPI/Swagger for REST documentation
- [[graphql-api]] - alternative query-oriented API style
- [[grpc-and-protobuf]] - high-performance alternative for microservices
