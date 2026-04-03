---
title: Chaos Engineering and Reliability Testing
category: concepts
tags: [devops, sre, chaos-engineering, testing, load-testing, resilience]
---

# Chaos Engineering and Reliability Testing

Reliability testing validates system behavior under stress and failure. Chaos engineering purposefully injects failures to discover weaknesses before they cause outages.

## Infrastructure Testing Pyramid

1. **Config validation** (unit) - syntax checks, schema validation
2. **Infrastructure integration** - service interaction tests
3. **System-level** - full stack validation
4. **Chaos** - failure injection

## Reliability Testing Types

| Type | Purpose | Tools |
|------|---------|-------|
| **Load testing** | Sustained expected load, verify SLOs | k6, Locust, JMeter |
| **Stress testing** | Beyond expected load, find breaking point | k6, Gatling |
| **Soak testing** | Extended duration, detect leaks/exhaustion | k6, custom |
| **Chaos engineering** | Inject failures, verify resilience | Chaos Monkey, Litmus, Gremlin |

## Chaos Engineering

### Prerequisites

1. Working incident management process
2. Culture of learning from errors (blameless)
3. Trust within organization
4. Good observability/monitoring

### Principles

1. Define steady state (normal SLI values)
2. Hypothesize that steady state continues during experiment
3. Introduce real-world events (kill pod, network partition, disk full)
4. Try to disprove hypothesis
5. Minimize blast radius (start small, automated kill switch)

### Tools

- **Chaos Monkey** (Netflix) - randomly terminates instances
- **Litmus** - Kubernetes-native chaos
- **Gremlin** - SaaS chaos platform
- **PowerfulSeal** - K8s pod/node failure injection

## Game Days

Planned reliability exercises simulating real incidents:

1. Define scenario and scope
2. Notify relevant teams
3. Execute simulated failure
4. Observe team response
5. Debrief and document lessons

Regular cadence (monthly/quarterly). Tests runbooks, alerting, communication.

## Infrastructure Testing Tools

### InSpec (Compliance)

```ruby
control 'sshd-8' do
  impact 0.6
  title 'Server: Configure the service port'
  describe sshd_config do
    its('Port') { should cmp 22 }
  end
end
```

### Testinfra (Python + Pytest)

```python
def test_access(host):
    addr = host.addr("google.com")
    assert addr.is_resolvable
    assert addr.port(443).is_reachable
```

### Configuration Validation

```bash
nginx -t -c nginx.conf
terraform validate
ansible --check
kubectl apply --dry-run=client -f deploy.yml
yamllint file.yaml
python -m json.tool sample.json
```

## Resilience Patterns

### Circuit Breaker

Three states: CLOSED (normal) -> OPEN (fail fast) -> HALF-OPEN (probe recovery).

```java
@CircuitBreaker(name = "service", fallbackMethod = "fallback")
public Response callService() { ... }
```

### Load Shedding

Reject requests when at capacity. Return 503. Better to serve 80% successfully than 100% slowly.

### Rate Limiting

- Per-client (token bucket, sliding window)
- Global (distributed counter in Redis)
- Adaptive (adjust based on current load)
- Back-pressure propagation

### Graceful Degradation

- Return cached/stale data when backend unavailable
- Disable non-critical features under load
- Priority queues for request processing

## Performance Metrics

### APDEX (Application Performance Index)

Standardized user satisfaction: Satisfied (<T), Tolerating (T-4T), Frustrated (>4T).

Score = (Satisfied + Tolerating/2) / Total. Range 0-1.

### Percentiles over Averages

p50, p95, p99 for latency. Averages hide outliers and tail latency.

## Gotchas

- Chaos engineering without working incident response is irresponsible
- Too large blast radius = real outage, not experiment
- Load testing should include realistic data and access patterns
- Soak tests are often skipped but catch memory leaks that short tests miss
- `siege -c 50 -t 30s http://localhost:80` for quick load testing

## See Also

- [[sre-principles]] - error budgets and reliability goals
- [[sre-incident-management]] - incident response tested by chaos
- [[monitoring-and-observability]] - detecting chaos experiment impact
- [[service-mesh-istio]] - circuit breaking, retries, timeouts
