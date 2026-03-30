---
title: Backend-for-Frontend (BFF)
category: patterns
tags: [bff, api-gateway, frontend, aggregation]
---
# Backend-for-Frontend (BFF)

An architectural pattern where a dedicated backend service is created for each type of frontend client (web, mobile, desktop), optimizing the API surface for each client's specific needs.

## Key Facts

- BFF sits stateless between frontend and backend services - it is NOT a monolithic backend
- A BFF typically uses [[orchestration-vs-choreography]] in orchestration mode: it calls backend services, aggregates data, and returns a client-optimized response
- Each client type gets its own BFF: web BFF returns rich HTML-ready data, mobile BFF returns compact payloads with images optimized for screen size
- BFF should NOT contain business logic - it transforms and aggregates data from business services
- Different user roles can also have different BFFs (admin BFF, customer BFF)
- BFF eliminates the N+1 API problem: instead of frontend making 5 calls, BFF makes them server-side (lower latency)
- See [[api-design-process]] for how to design the BFF's API surface
- See [[load-balancing]] for how BFF instances are distributed

## Patterns

### Basic BFF architecture

```
[Mobile App] --> [Mobile BFF]    --\
                                    +--> [Order Service]
[Web App]    --> [Web BFF]       --+--> [User Service]
                                    +--> [Payment Service]
[Admin Panel]--> [Admin BFF]     --/

Each BFF:
  - Tailored response format for its client
  - Client-specific aggregation logic
  - May apply different caching strategies
  - Stateless (no session state in BFF itself)
```

### BFF vs API Gateway vs direct access

```
Direct Service Access:
  [Client] --> [Service A]
  [Client] --> [Service B]
  [Client] --> [Service C]
  Problem: N+1 calls, client knows about internal services

API Gateway (single):
  [Client] --> [API Gateway] --> [Service A, B, C]
  Problem: gateway becomes monolithic, one-size-fits-all

BFF (per-client):
  [Mobile] --> [Mobile BFF] --> [Services]
  [Web]    --> [Web BFF]    --> [Services]
  Benefit: each BFF optimized for its client
```

### Response optimization example

```
Backend User Service returns:
{
  "id": 123,
  "name": "John Doe",
  "email": "john@example.com",
  "avatar_url": "https://cdn.example.com/avatars/123.jpg",
  "preferences": { ... 50 fields ... },
  "audit_log": [ ... thousands of entries ... ]
}

Mobile BFF returns:
{
  "id": 123,
  "name": "John Doe",
  "avatar_url": "https://cdn.example.com/avatars/123_thumb.jpg"
}

Web BFF returns:
{
  "id": 123,
  "name": "John Doe",
  "email": "john@example.com",
  "avatar_url": "https://cdn.example.com/avatars/123_medium.jpg",
  "preferences": { ... relevant subset ... }
}

Admin BFF returns:
{
  ... full user object including audit_log ...
}
```

### BFF with orchestration

```python
# Mobile BFF endpoint: GET /api/order-summary/{id}
async def get_order_summary(order_id: str):
    # Orchestrate: call multiple services in parallel
    order, user, shipping = await asyncio.gather(
        order_service.get_order(order_id),
        user_service.get_user(order.user_id),
        shipping_service.get_tracking(order_id)
    )

    # Aggregate and transform for mobile
    return {
        "order_id": order.id,
        "status": order.status,
        "buyer_name": user.name,
        "tracking_url": shipping.tracking_url,
        "estimated_delivery": shipping.eta
    }
```

## Gotchas

- **Symptom**: Business logic duplicated across multiple BFFs -> **Cause**: Business rules implemented in BFF instead of backend services -> **Fix**: BFF should only aggregate and transform. Business logic belongs in domain services that all BFFs call
- **Symptom**: BFF becomes a bottleneck with high latency -> **Cause**: Sequential calls to backend services instead of parallel -> **Fix**: Use async/parallel calls (Promise.all, asyncio.gather). Backend calls are independent - parallelize them
- **Symptom**: BFF for chorography (event-driven) feels awkward -> **Cause**: BFF is inherently request-response (synchronous from client perspective) -> **Fix**: BFF naturally fits orchestration. For async operations, BFF can: (1) submit to queue and return immediately, (2) provide polling endpoint for status, (3) use WebSocket/SSE for push updates
- **Symptom**: Too many BFFs to maintain -> **Cause**: Creating BFF per feature instead of per client type -> **Fix**: One BFF per distinct client platform. Different features for same platform go in same BFF

## See Also

- [[orchestration-vs-choreography]] - BFF uses orchestration pattern
- [[api-design-process]] - Designing the BFF's client-facing API
- [[load-balancing]] - BFF instances behind a load balancer
- [[service-mesh]] - Infrastructure layer for BFF-to-service communication
- Sam Newman: [BFF Pattern](https://samnewman.io/patterns/architectural/bff/)
- Microsoft: [BFF Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/backends-for-frontends)
