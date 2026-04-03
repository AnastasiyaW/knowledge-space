---
title: HTTP and REST API Fundamentals
category: reference
tags: [http, rest, api, web-services, protocol]
---

# HTTP and REST API Fundamentals

REST (Representational State Transfer) is an architectural style for distributed systems, not a protocol. It aligns with internet architecture and uses existing HTTP infrastructure. REST is the most widely used API style for public APIs.

## HTTP Protocol

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

| Method | CRUD | Idempotent | Safe | Has Body |
|--------|------|------------|------|----------|
| GET | Read | Yes | Yes | No |
| POST | Create | No | No | Yes |
| PUT | Full Update/Create | Yes | No | Yes |
| PATCH | Partial Update | No* | No | Yes |
| DELETE | Delete | Yes | No | Optional |
| HEAD | Read headers | Yes | Yes | No |
| OPTIONS | Get capabilities | Yes | Yes | No |

*PATCH can be made idempotent with proper implementation.

**Idempotent** = multiple identical requests produce same result. **Safe** = doesn't modify server state.

### Status Codes

| Range | Meaning | Key Codes |
|-------|---------|-----------|
| 2xx | Success | 200 OK, 201 Created, 204 No Content |
| 3xx | Redirection | 301 Moved Permanently, 304 Not Modified |
| 4xx | Client Error | 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 429 Too Many Requests |
| 5xx | Server Error | 500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable |

### Key Headers

**Request:** `Host` (required in HTTP/1.1), `Content-Type`, `Accept`, `Authorization`, `Cache-Control`, `User-Agent`

**Response:** `Content-Type`, `Content-Length`, `Cache-Control`, `ETag`, `Last-Modified`, `Set-Cookie`

### HTTP Versions

| Version | Key Features |
|---------|-------------|
| HTTP/1.0 | One request per TCP connection |
| HTTP/1.1 | Persistent connections, Host header, chunked transfer, pipelining |
| HTTP/2 | Binary framing, multiplexing, header compression (HPACK), server push |
| HTTP/3 | Based on QUIC (UDP), reduced latency, better mobile performance |

## REST Six Constraints

1. **Client-Server** - separation of UI and data storage concerns
2. **Stateless** - each request contains all info needed to process it
3. **Cacheable** - responses declare themselves cacheable or not
4. **Uniform Interface** - resource identification via URIs, manipulation through representations, self-descriptive messages, HATEOAS
5. **Layered System** - client can't tell if connected directly to server or through intermediary
6. **Code on Demand** (optional) - server can send executable code (JavaScript)

## Resource-Based URL Design

```
# Resources are nouns, not verbs
/users            # collection
/users/123        # specific resource
/users/123/orders # nested resource

# Actions via HTTP methods, not URL
DELETE /users/123          # correct
POST /users/123/delete     # wrong

# Naming conventions
/order-items     # hyphens for multi-word
/users/123       # plurals
                 # lowercase, no trailing slashes, no file extensions
```

## REST Resource Types

| Type | Description | ID Source |
|------|-------------|-----------|
| **Object** | Single resource with unique ID | - |
| **Collection** | Server-managed catalog | Server generates IDs |
| **Store** | Client-managed storage | Client assigns IDs |
| **Controller** | Action/function (RPC-like) | POST-based |

## Filtering, Pagination, Search

### Pagination Approaches

| Approach | Example | Pros/Cons |
|----------|---------|-----------|
| **Offset-based** | `?offset=20&limit=10` | Simple, allows jumping; inconsistent with live data |
| **Cursor-based** | `?cursor=abc123&limit=10` | Stable with live data; can't jump to arbitrary page |
| **Keyset-based** | `?after_id=100&limit=20` | Very performant with indexed columns |

### Filtering and Sorting

```
?status=active&created_after=2024-01-01    # filtering
?sort=created_at&order=desc                # sorting
?q=search+term                             # full-text search
```

## File Transfer

```
# Client request
Accept: image/png

# Server response
Content-Type: image/png
Content-Disposition: attachment; filename="file.png"
Content-Length: 12345

# Large files
Transfer-Encoding: chunked
```

## CORS (Cross-Origin Resource Sharing)

Browser security mechanism. Server declares allowed origins:
- `Access-Control-Allow-Origin`
- `Access-Control-Allow-Methods`
- `Access-Control-Allow-Headers`

Preflight requests (OPTIONS) sent for non-simple requests. Critical for frontend-backend integration.

## API Style Comparison

| Aspect | REST | JSON-RPC | GraphQL | gRPC |
|--------|------|----------|---------|------|
| Paradigm | Resource-oriented | Function-oriented | Query-oriented | Function-oriented |
| Transport | HTTP | HTTP/TCP/WS | HTTP | HTTP/2 |
| Format | JSON/XML | JSON | JSON-like | Protobuf (binary) |
| Caching | Native HTTP | Difficult | Difficult | Difficult |
| Typing | Weak (OpenAPI) | Weak | Strong (schema) | Strong (proto) |
| Best for | Public APIs, CRUD | Internal simple APIs | Complex queries | Microservices |

## Gotchas

- **PUT is full replacement** - must send entire resource, not partial. Use PATCH for partial updates
- **POST is not idempotent** - multiple identical calls create duplicates unless deduplication implemented
- **HTTP 200 for SOAP errors** - SOAP returns 200 for business errors, only 4xx for protocol errors
- **HATEOAS** is part of REST spec but rarely implemented in practice
- **URL versioning** (`/api/v1/users`) is most common, keep max 2 active versions

## See Also

- [[rest-api-advanced]] - Rate limiting, caching strategies, batch requests, retry patterns
- [[api-authentication-security]] - OAuth 2.0, JWT, mTLS, CORS details
- [[graphql-api]] - Query language for flexible data fetching
- [[grpc-api]] - High-performance binary RPC framework
