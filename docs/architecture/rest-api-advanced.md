---
title: REST API Advanced - Performance, Versioning, Caching
category: reference
tags: [rest, api, caching, rate-limiting, versioning, retry]
---

# REST API Advanced - Performance, Versioning, Caching

API performance depends on speed, data volume, and call frequency. Factors like mobile data costs, device battery drain, and serverless billing make efficiency critical.

## Rate Limiting and Throttling

### Request-Level Rate Limiting
Limit requests per time window by IP, API key, or user. On exceeding:
- **HTTP 429 Too Many Requests**
- `X-Rate-Limit-Limit` - allowed requests in current period
- `X-Rate-Limit-Remaining` - remaining requests
- `X-Rate-Limit-Reset` - seconds until period resets

### Rate Limiting Algorithms
- **Fixed window** - simple counter per time window
- **Sliding window** - more accurate, prevents burst at window boundary
- **Token bucket** - allows short bursts while maintaining average rate (most common)
- **Leaky bucket** - smooth output rate regardless of input

### Application-Level Throttling
Internal protection against surges. Prioritizes urgent requests. Implemented via delays or batch processing.

## HTTP Caching Strategies

### Four Caching Approaches

| Strategy | Header | Use Case |
|----------|--------|----------|
| **No cache** | `Cache-Control: private, no-cache, no-store` | Confidential/dynamic data |
| **Time-based** | `Cache-Control: max-age=3600, must-revalidate` | Known change interval |
| **Validation-based** | `Cache-Control: no-cache` + `ETag` | Unknown change interval |
| **Cache forever** | `Cache-Control: max-age=31536000, public, immutable` | Immutable content |

### Validation Flow (ETag)
```rust
1. Server responds with: ETag: "abc123"
2. Client conditional request: If-None-Match: "abc123"
3. Server responds: 304 Not Modified (use cache)
   OR sends new data with new ETag
```

### Cache Management
- Cache files forever with versioned names (`style1a.css`)
- On update, rename to `style2b.css` - browser treats as new resource
- Full invalidation: `Clear-Site-Data: "cache", "cookies", "storage"`

## Compression

No API design change needed:
```yaml
# Client
Accept-Encoding: gzip, deflate, br

# Server
Content-Encoding: gzip
```

## Batch Requests

Combine multiple API operations into one. Reduces latency, saves bandwidth. All sub-requests packaged in single request; responses returned together. See Google Drive API batch format as reference.

## API Versioning

### Why Version
- Maintain backward compatibility for existing clients
- Clear communication of available features
- Allow clients to migrate at their own pace

### Semantic Versioning
- **Non-breaking** (new endpoints, new optional fields, new response fields): minor bump (1.0 -> 1.1)
- **Breaking** (removed endpoints, changed required fields, changed error codes): major bump (1.x -> 2.0)
- Keep max 2 active versions; notify clients of deprecation

### Versioning Approaches

| Approach | Example | Notes |
|----------|---------|-------|
| **URL path** | `/api/v1/users` | Most common, explicit |
| **Query parameter** | `/api/users?version=1` | Simple but messy |
| **Header** | `Accept: application/vnd.api.v1+json` | Cleaner URLs |

### Zero-Downtime API Migration
- Deprecation announcements with clear timeline
- Monitor usage of old versions before removal
- Keep old API versions longer than expected - some clients call APIs only once per year
- Expand-contract pattern: add new alongside old, migrate, remove old

## Retry Patterns

### Exponential Backoff
Start with short delay, exponentially increase: 5s -> 25s -> 125s

### Jitter
Add randomness to retry delays to prevent thundering herd when multiple clients retry simultaneously.

### Retry Rules
- Only retry on transient errors (5xx, network timeouts)
- Don't retry client errors (4xx) - they won't self-resolve
- Set maximum retry count
- Consider circuit breaker for persistent failures

## Error Response Format

Standardized format across all APIs:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable description",
    "details": [
      {"field": "email", "issue": "invalid format"}
    ]
  }
}
```

Never expose internal error details (stack traces, SQL queries) in production.

## Gotchas

- **Caching + auth** - never cache responses with `Authorization` header unless explicitly `public`
- **429 without headers** - always include rate limit headers so clients can self-throttle
- **Retry on POST** - dangerous without idempotency keys, can create duplicate resources
- **Cache stampede** - when popular key expires, many requests hit DB simultaneously. Use locking or probabilistic early expiration
- **Compression CPU cost** - enable for text content (JSON, HTML) but not for already-compressed content (images, video)

## See Also

- [[http-rest-fundamentals]] - HTTP protocol, REST constraints, resource design
- [[api-authentication-security]] - OAuth 2.0, JWT, TLS
- [[caching-and-performance]] - Application-level caching patterns
- [[api-documentation-specs]] - OpenAPI, Swagger, AsyncAPI
