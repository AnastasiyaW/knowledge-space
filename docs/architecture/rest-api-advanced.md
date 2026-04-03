---
title: REST API Advanced Topics
category: api
tags: [architecture, rest, caching, versioning, rate-limiting, performance]
---

# REST API Advanced Topics

Advanced REST API design covering caching strategies, versioning, rate limiting, compression, retry patterns, and batch requests for production-grade APIs.

## HTTP Caching Strategies

### Four Caching Approaches

1. **No cache** (confidential/dynamic data):
   ```
   Cache-Control: private, no-cache, no-store
   ```

2. **Time-based** (known change interval):
   ```
   Cache-Control: max-age=3600, must-revalidate
   ```

3. **Validation-based** (unknown change interval):
   - Server sends `Cache-Control: no-cache` + `ETag: "hash"`
   - Client sends conditional: `If-None-Match: "hash"`
   - Server responds `304 Not Modified` or sends new data with new ETag

4. **Cache forever** (immutable content):
   ```
   Cache-Control: max-age=31536000, public, immutable
   ```

### Cache Management

- Cache files forever with versioned names (`style1a.css`)
- On update, rename to `style2b.css` - browser treats as new resource
- Full invalidation: `Clear-Site-Data: "cache", "cookies", "storage", "executionContexts"`

## Rate Limiting and Throttling

### Request-Level Rate Limiting

Limit requests per time window by IP, API key, or user. Response headers:
- `X-Rate-Limit-Limit` - allowed requests in current period
- `X-Rate-Limit-Remaining` - remaining requests
- `X-Rate-Limit-Reset` - seconds until period resets
- **HTTP 429 Too Many Requests** when exceeded

**Algorithms**: Fixed window, sliding window, token bucket, leaky bucket. Token bucket is most common - allows short bursts while maintaining average rate.

### Application-Level Throttling

Internal protection against sudden surges. Implemented via delays between processing or batch processing. Prioritizes urgent requests.

## API Versioning

### Versioning Approaches

1. **URL path**: `/api/v1/users` (most common, explicit)
2. **Query parameter**: `/api/users?version=1` (simple but messy)
3. **Header**: `Accept: application/vnd.myapi.v1+json` (cleaner URLs)
4. **Custom header**: `API-Version: 2`

### Semantic Versioning Strategy

- **Non-breaking changes** (new endpoints, new optional fields, new response fields): increment minor version (1.0 -> 1.1)
- **Breaking changes** (removed/changed endpoints, changed required fields, changed error codes): increment major version (1.x -> 2.0)
- Keep max 2 active versions; notify clients of deprecation
- Real-world lesson: Keep old API versions longer than expected - some clients call APIs only once per year

## Compression and Keep-Alive

**Compression** (no API design change needed):
```
Client: Accept-Encoding: gzip, deflate, br
Server: Content-Encoding: gzip
```

**Keep-Alive**: Default in HTTP/1.1, no explicit header needed.

## Batch Requests

Combine multiple API requests into one. Reduces latency, saves bandwidth. All sub-requests packaged in a single request; responses returned together.

## Retry Patterns

### Exponential Backoff
Start with short delay, exponentially increase: 5s -> 25s -> 125s

### Jitter
Add randomness to retry delays to prevent thundering herd when multiple clients retry simultaneously.

### Retry Rules
- Only retry on transient errors (5xx, network timeouts)
- Don't retry client errors (4xx) - they won't self-resolve
- Set maximum retry count
- Consider [[distributed-systems|circuit breaker]] for persistent failures

## Performance Optimization

API performance depends on speed, data volume, and call frequency. Factors like roaming data costs, device battery drain, and serverless billing make efficiency critical.

Key techniques:
- **Compression**: gzip/brotli for responses
- **Connection reuse**: HTTP keep-alive
- **Batch requests**: combine multiple operations
- **Pagination**: limit response size
- **Field selection**: return only needed fields (partial responses)
- **Caching**: HTTP cache headers

## Gotchas

- Validation-based caching with timestamps (`If-Modified-Since`) is not precise enough under high load - use ETag versioning
- Rate limiting must be applied per API key, not just per IP - shared IPs (NAT, corporate proxies) cause false positives
- Versioning via URL is most discoverable but hardest to maintain in code
- Batch endpoints must handle partial failures gracefully

## See Also

- [[rest-api-design]] - HTTP fundamentals and REST constraints
- [[api-authentication-security]] - auth methods for REST APIs
- [[caching-strategies]] - in-depth caching patterns beyond HTTP
- [[reliability-fault-tolerance]] - circuit breakers, timeouts, retries
