---
title: Testing Pyramid and Quality Assurance
category: patterns
tags: [testing, quality, automation, chaos-engineering]
---
# Testing Pyramid and Quality Assurance

The testing pyramid defines the optimal distribution of automated tests by type: many fast unit tests at the base, fewer integration tests in the middle, and minimal end-to-end tests at the top.

## Key Facts

- Test-design techniques (equivalence partitioning, boundary analysis) allow testing MORE with FEWER tests - this is the most valuable QA skill
- The pyramid shape matters: unit tests are fast/cheap to write and maintain, E2E tests are slow/expensive/fragile
- Chaos engineering (Netflix Chaos Monkey) is for Netflix-scale systems. If you are not operating at that scale, basic HA testing is sufficient
- Migration testing is crucial but often overlooked: data migration between schema versions, service migration during architecture changes
- Quality management is a tech lead/architect concern, not just a QA team concern. Architects should understand test strategy
- See [[quality-attributes]] for the quality goals that testing validates
- See [[system-design-template]] for where testing fits in the design process (step 7)

## Patterns

### Testing pyramid

```
           /  E2E Tests  \         Few, slow, expensive
          / (Selenium, etc)\       Test full user flows
         /------------------\
        / Integration Tests  \     Medium count
       /  (API, DB, queues)   \    Test component interactions
      /------------------------\
     /      Unit Tests          \  Many, fast, cheap
    /  (functions, classes)      \ Test business logic
   /------------------------------\

Ratio rule of thumb:
  Unit : Integration : E2E = 70% : 20% : 10%

Cost of finding bug:
  Unit test:         $1    (seconds to run)
  Integration test:  $10   (minutes to run)
  E2E test:          $100  (minutes + setup)
  Production:        $1000 (incident + fix + deploy)
```

### Test-design techniques

```
1. Equivalence Partitioning:
   Input: age (0-150)
   Partitions: invalid (<0), valid (0-150), invalid (>150)
   Test ONE value per partition: -1, 75, 151
   -> 3 tests cover entire range

2. Boundary Value Analysis:
   Boundaries: -1, 0, 1, 149, 150, 151
   Test AT and AROUND boundaries
   -> 6 tests catch off-by-one errors

3. Pairwise Testing:
   Parameters: browser(3), OS(3), language(5) = 45 combos
   Pairwise reduction: ~15 combos cover all pairs
   Tools: PICT (Microsoft), AllPairs

4. Decision Table:
   Conditions: premium_user, order > $100, free_shipping_promo
   8 combinations (2^3) -> test all
   But some conditions dominate -> reduce to meaningful combos
```

### Integration test patterns

```python
# Contract test (consumer-driven)
# Consumer defines expected API contract
def test_order_service_contract():
    response = client.get("/api/orders/123")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "status" in data
    assert data["status"] in ["pending", "shipped", "delivered"]
    # Consumer doesn't care about fields it doesn't use

# Component test (single service in isolation)
def test_order_creation():
    # Real service, mocked dependencies
    with mock_payment_service(), mock_inventory_service():
        response = client.post("/api/orders", json={...})
        assert response.status_code == 201
        assert mock_payment.called_once()
```

### Migration testing checklist

```
Data migration:
  [ ] Rollback procedure tested
  [ ] Data integrity verified post-migration
  [ ] Performance with production-scale data
  [ ] Null/edge case handling in transformations
  [ ] Encoding/charset compatibility (UTF-8 vs legacy)

Service migration (monolith -> microservices):
  [ ] Old and new service run in parallel
  [ ] Shadow traffic (send to both, compare results)
  [ ] Gradual traffic shift (1% -> 10% -> 50% -> 100%)
  [ ] Rollback switch works instantly
  [ ] Monitoring dashboards compare old vs new

Database migration:
  [ ] Schema change is backward-compatible
  [ ] Application works with both old and new schema
  [ ] Migration script is idempotent (can run twice safely)
  [ ] Lock duration estimated for large tables
  [ ] Blue-green schema migration considered
```

### When chaos engineering is appropriate

```
Prerequisites for chaos engineering:
  1. You have HA infrastructure (multi-AZ, replicas)
  2. You have monitoring and alerting
  3. You have runbooks for common failures
  4. You can DETECT failures automatically
  5. Your team can respond to incidents

Only then:
  - Kill random instances (Chaos Monkey)
  - Inject network latency (Toxiproxy)
  - Simulate AZ failure
  - Fill disk, exhaust CPU

If you don't have items 1-4:
  - Fix those first
  - Basic HA testing is more valuable than chaos
```

## Gotchas

- **Symptom**: Test suite takes 2+ hours, developers skip tests -> **Cause**: Too many E2E tests, inverted pyramid -> **Fix**: Audit test distribution. Move business logic validation to unit tests. Keep E2E for critical happy paths only
- **Symptom**: Tests pass but production has bugs -> **Cause**: Tests only cover happy paths, no boundary/edge case coverage -> **Fix**: Apply test-design techniques: boundary analysis for numeric inputs, equivalence partitioning for categories, decision tables for complex rules
- **Symptom**: Data migration corrupts production data -> **Cause**: Migration tested only on small dev dataset -> **Fix**: Test migration on production-scale data copy. Check edge cases: nulls, special characters, maximum field lengths. Always have a tested rollback procedure
- **Symptom**: Flaky E2E tests that randomly fail -> **Cause**: Tests depend on timing, external services, or shared state -> **Fix**: Isolate test environment per run, use explicit waits instead of sleep, mock external dependencies, reset state before each test

## See Also

- [[quality-attributes]] - Quality goals that testing validates
- [[system-design-template]] - Testing is part of step 7 (operational concerns)
- [[distributed-system-patterns]] - Circuit breaker and retry testing
- [[microservices-vs-monolith]] - Testing strategies differ by architecture
- Martin Fowler: [Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html)
- Microsoft: [Testing Approaches](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/multi-container-microservice-net-applications/test-aspnet-core-services-web-apps)
- Book: "Release It!" (Nygard) - Stability patterns and testing
