---
title: Test Strategy and Coverage
category: methodology
tags: [test-strategy, test-pyramid, coverage, smoke, regression, test-types, qa-process]
---
# Test Strategy and Coverage

When, what, and how to test - test pyramid, test types, coverage metrics, automation strategy.

## Key Facts

- Test pyramid: many unit tests (fast, cheap) > fewer integration tests > fewest E2E/UI tests (slow, expensive)
- Test types by scope: smoke (critical paths), sanity (specific area), regression (full suite)
- Smoke tests: 5-15 min, run on every deploy, cover login, main flows, critical payments
- Regression tests: full suite, run nightly or before releases, can take hours
- API tests run 10-50x faster than UI tests - prefer API testing where possible
- UI test coverage tool: measures which page elements are exercised by tests
- Functional vs non-functional: functional tests features, non-functional tests performance/security/usability
- When to automate: repetitive, stable features, data-driven scenarios, regression checks
- When NOT to automate: exploratory testing, frequently changing UI, one-time checks
- Key metric: not "how many tests" but "what critical paths are covered"

## Patterns

```python
# Test organization by type
# tests/
#   smoke/           - critical path tests (run on every deploy)
#   api/             - API tests (fast, many)
#   ui/              - UI tests (slower, fewer)
#   regression/      - full regression suite
#   conftest.py      - shared fixtures

# Markers for test selection
import pytest

@pytest.mark.smoke
def test_login_success():
    """Critical: users must be able to log in."""
    ...

@pytest.mark.regression
def test_password_reset_email():
    """Regression: password reset flow."""
    ...

# CI pipeline strategy
# On every push:      pytest -m smoke          (2-5 min)
# On PR to main:      pytest -m "not slow"     (10-20 min)
# Nightly schedule:   pytest                    (full suite, 1-2 hours)
# Before release:     pytest --reruns=2         (full + retry flaky)

# pytest.ini configuration
# [pytest]
# markers =
#     smoke: Quick smoke tests for critical paths
#     regression: Full regression suite
#     slow: Tests that take >30 seconds
#     api: API-level tests
#     ui: Browser-based UI tests

# Test scope decision matrix
# +-----------------------+--------+--------+
# | What to test          | API    | UI     |
# +-----------------------+--------+--------+
# | Business logic        | YES    | no     |
# | Data validation       | YES    | no     |
# | Visual layout         | no     | YES    |
# | User flows            | partly | YES    |
# | Error messages        | YES    | verify |
# | Performance           | YES    | partly |
# +-----------------------+--------+--------+

# Coverage tracking (code coverage)
# pip install pytest-cov
# pytest --cov=src --cov-report=html tests/

# UI Coverage with UI Coverage Tool
# Tracks which UI elements are exercised during test execution
# Generates visual reports showing tested vs untested elements
```

## Gotchas

- **Symptom**: full test suite takes 3+ hours - **Cause**: too many UI tests, no parallelization - **Fix**: move validation to API level, use `pytest-xdist` for parallel runs
- **Symptom**: high test count but bugs still escape - **Cause**: testing trivial paths, missing edge cases - **Fix**: focus on risk-based testing, cover error paths and boundary conditions
- **Symptom**: flaky tests undermine confidence - **Cause**: shared state, timing issues, external dependencies - **Fix**: isolate tests, mock external services, use retry for known flaky infra
- 100% code coverage does not mean bug-free - coverage measures lines executed, not correctness of assertions
- Don't duplicate assertions: if `test_login` verifies redirect, other tests can assume login works

## See Also

- [[ci-cd-test-automation]] - implementing test strategy in CI
- [[pytest-plugins-and-parallel]] - parallel execution for faster suites
- [[api-testing-requests]] - API-level testing
- [[page-object-model]] - organizing UI tests
