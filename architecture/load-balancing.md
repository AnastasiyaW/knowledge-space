---
title: Load Balancing
category: reference
tags: [load-balancer, nginx, haproxy, scaling, api-gateway]
---
# Load Balancing

Load balancing distributes incoming network traffic across multiple server instances to improve availability, reliability, and performance. It operates at different layers and with different algorithms.

## Key Facts

- Load balancers themselves can fail - always consider HA for the balancer itself (active-passive, DNS failover)
- Nginx can handle ~50K concurrent WebSocket connections on average hardware; primarily memory-bound
- API Gateway != Load Balancer: a gateway can route to DIFFERENT services (orders, users), while a load balancer distributes to instances of the SAME service. Gateways can also do both
- Client-side load balancing (DNS-based, service mesh sidecar) eliminates the balancer as a single point of failure
- OpenResty = Nginx + Lua plugins. APISIX = OpenResty + ready-made plugin ecosystem
- See [[quality-attributes]] for how availability requirements influence balancing strategy
- See [[distributed-system-patterns]] for how load balancing fits into overall system design

## Patterns

### Layer 4 vs Layer 7

```
Layer 4 (Transport):
  - Routes based on IP + port
  - No HTTP awareness (cannot inspect headers, URL, cookies)
  - Lower latency, higher throughput
  - Example: HAProxy in TCP mode, AWS NLB

Layer 7 (Application):
  - Routes based on HTTP path, headers, cookies
  - Can do SSL termination, compression, caching
  - Higher latency, more features
  - Example: Nginx, HAProxy in HTTP mode, AWS ALB
```

### Load balancing algorithms

```
Round Robin:        A -> B -> C -> A -> B -> C
  Simple, ignores server capacity differences

Weighted Round Robin: A(3) -> A -> A -> B(1) -> C(2) -> C
  Respects server capacity (3x traffic to A)

Least Connections:  Route to server with fewest active connections
  Best for long-lived connections (WebSocket, gRPC streams)

IP Hash:           hash(client_ip) % N -> consistent server
  Ensures same client hits same server (poor man's sticky sessions)

Consistent Hashing: Minimizes remapping when adding/removing nodes
  Used in distributed caches and databases
```

### Balancing strategy by level

```
Level 1: DNS (geo-balancing, round robin)
  Client --> DNS --> [Datacenter A | Datacenter B]

Level 2: Hardware/Software L4 (TCP distribution)
  Client --> [L4 LB] --> [App Server 1..N]

Level 3: Software L7 (HTTP-aware routing)
  Client --> [Nginx/HAProxy] --> [Service A instances]
                              --> [Service B instances]

Level 4: Client-side (service mesh sidecar)
  [App] --> [Envoy sidecar] --> [Service instances]
```

### Sticky sessions vs externalized state

```
Sticky sessions (session affinity):
  - LB routes same client to same instance
  - Problem: uneven load distribution
  - Problem: instance crash loses sessions
  - Problem: harder to scale down

Externalized state (preferred):
  - Sessions stored in Redis/Memcached
  - Any instance can serve any client
  - See [[caching-strategies]] session externalization
```

### Health checks

```nginx
# Nginx upstream health check
upstream backend {
    server 10.0.0.1:8080;
    server 10.0.0.2:8080;
    server 10.0.0.3:8080 backup;  # only when others fail
}

# HAProxy health check
backend app_servers
    option httpchk GET /health
    server app1 10.0.0.1:8080 check inter 5s fall 3 rise 2
    server app2 10.0.0.2:8080 check inter 5s fall 3 rise 2
```

## Gotchas

- **Symptom**: Adding WebSocket support causes load balancer memory spike -> **Cause**: Each WebSocket connection holds state in the LB -> **Fix**: Plan memory for concurrent connection count, not just RPS. 50K connections at ~10KB each = 500MB per LB instance
- **Symptom**: Blue-green deployment causes dropped connections -> **Cause**: L4 balancer draining not configured; existing connections terminated -> **Fix**: Enable connection draining (graceful shutdown). Set drain timeout matching your longest expected request
- **Symptom**: One backend instance gets 10x more traffic than others -> **Cause**: Round robin with mixed fast/slow requests; slow requests accumulate -> **Fix**: Switch to least-connections algorithm for heterogeneous workloads
- **Symptom**: Cannot scale beyond load balancer throughput -> **Cause**: Single load balancer is the bottleneck -> **Fix**: Use DNS-based load balancing across multiple LB instances, or client-side load balancing with service discovery

## See Also

- [[quality-attributes]] - Availability targets driving redundancy
- [[caching-strategies]] - Session externalization instead of sticky sessions
- [[bff-pattern]] - How BFF sits between LB and backend services
- [[service-mesh]] - Client-side load balancing via sidecars
- Nginx: [Load Balancing](https://nginx.org/en/docs/http/load_balancing.html)
- HAProxy: [Configuration Guide](https://www.haproxy.org/download/2.8/doc/configuration.txt)
