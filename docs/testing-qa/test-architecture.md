---
title: Test Architecture
category: methodology
tags: [test-strategy, test-pyramid, project-structure, conftest, test-types, coverage, logging, security]
---

# Test Architecture

Test automation projects are software projects - they need the same engineering practices: version control, code review, dependency management, CI/CD. Architecture covers project structure (conftest hierarchy, client classes, models), test strategy (pyramid, types, coverage), and operational concerns (logging, secret masking, metrics).

## Key Facts

- **Test pyramid**: many unit tests (fast), fewer integration, fewest E2E (slow, expensive)
- Project structure: `tests/api/`, `tests/ui/`, `clients/`, `models/` - separate concerns
- `conftest.py` bloat solution: `pytest_plugins` list imports fixtures from separate modules
- Sensitive data masking: custom logging filters + careful with `pytest -l` (showlocals)
- Test isolation: each test prepares own data, verifies independently, cleans up after
- Metrics to track: execution time, stability (pass rate), infrastructure availability, feedback loop time

## Patterns

### Project Structure

```
tests/
  conftest.py              # global fixtures + pytest_plugins
  api/
    conftest.py            # API-specific fixtures
    users/
      test_create_user.py
    spend/
      test_spending.py
  ui/
    conftest.py            # browser fixtures
    test_login.py
  clients/
    spend_client.py        # HTTP client classes
    db_client.py
  models/
    user.py                # Pydantic response models
    spend.py
  fixtures/
    user_fixtures.py       # extracted from conftest via plugins
    auth_fixtures.py
```

### Test Pyramid and Types

| Level | Speed | Cost | Examples |
|-------|-------|------|----------|
| Unit | Fast (ms) | Low | Pure functions, validators |
| Integration | Medium (s) | Medium | API calls, DB queries |
| E2E / UI | Slow (10s+) | High | Full user flows with browser |

- **Smoke tests**: critical paths, run first (login, core CRUD)
- **Regression tests**: full suite, run nightly or per-PR
- **Contract tests**: API schema validation between services

### Sensitive Data Masking

```python
import logging, re

class SensitiveDataFilter(logging.Filter):
    PATTERNS = [
        (re.compile(r'(password["\s:=]+)[^\s,}"]+', re.I), r'\1***'),
        (re.compile(r'(token["\s:=]+)[^\s,}"]+', re.I), r'\1***'),
        (re.compile(r'(Bearer\s+)\S+', re.I), r'\1***'),
    ]

    def filter(self, record):
        msg = record.getMessage()
        for pattern, replacement in self.PATTERNS:
            msg = pattern.sub(replacement, msg)
        record.msg = msg
        record.args = ()
        return True

logging.getLogger().addFilter(SensitiveDataFilter())
```

### Environment Management

```ini
# .env.sample (committed)
FRONTEND_URL=http://localhost:3000
TEST_USERNAME=
TEST_PASSWORD=

# .env (gitignored, actual values)
```

Switch environments: `.env.prod`, `.env.staging` + custom pytest option (`--env=prod`) or CI env vars.

### Dependency Management

```bash
# Simple: venv + pip
python -m venv .venv && pip install -r requirements.txt

# Teams: Poetry (deterministic builds via lockfile)
poetry init && poetry add pytest requests
```

## Gotchas

- Only one `conftest.py` per directory - use `pytest_plugins` for cross-directory fixture sharing
- Tests depending on other tests' side effects = fragile; enforce isolation
- `pytest -l` exposes local variables on failure - tokens, passwords visible in CI logs
- Coverage is a guide, not a target: ~85% is practical, 100% has diminishing returns

## See Also

- [[pytest-fundamentals]] - fixtures, parametrize, hooks
- [[allure-reporting]] - test reports as team communication
- [[ci-cd-test-automation]] - running tests in CI pipelines
- [[api-testing]] - HTTP client classes and response validation
