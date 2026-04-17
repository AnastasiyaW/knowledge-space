---
title: Test Logging and Secret Masking
category: patterns
tags: [logging, secrets, masking, sensitive-data, allure, debugging, filters]
---

# Test Logging and Secret Masking

Structured logging in test frameworks, masking sensitive data in logs and reports, and DevTools techniques for test debugging.

## Python Logging in Tests

```python
import logging

logger = logging.getLogger(__name__)

@pytest.fixture(autouse=True)
def configure_logging(caplog):
    caplog.set_level(logging.DEBUG)

def test_api_call(api_client, caplog):
    resp = api_client.get("/api/users")
    assert resp.status_code == 200

    # Verify logging happened
    assert "GET /api/users" in caplog.text
    assert "200" in caplog.text
```

## HTTP Request/Response Logging

```python
import requests
import logging

def setup_request_logging(session):
    """Log all HTTP requests made by this session."""
    def log_request(resp, *args, **kwargs):
        logger.info(f"{resp.request.method} {resp.request.url} -> {resp.status_code}")
        logger.debug(f"Request headers: {resp.request.headers}")
        logger.debug(f"Response body: {resp.text[:500]}")

    session.hooks["response"].append(log_request)
    return session
```

## Secret Masking in Logs

```python
import re
import logging

class SensitiveDataFilter(logging.Filter):
    PATTERNS = [
        (re.compile(r'(Bearer\s+)\S+'), r'\1***MASKED***'),
        (re.compile(r'(password["\s:=]+)\S+', re.I), r'\1***MASKED***'),
        (re.compile(r'(token["\s:=]+)\S+', re.I), r'\1***MASKED***'),
        (re.compile(r'(api[_-]?key["\s:=]+)\S+', re.I), r'\1***MASKED***')]

    def filter(self, record):
        msg = record.getMessage()
        for pattern, replacement in self.PATTERNS:
            msg = pattern.sub(replacement, msg)
        record.msg = msg
        record.args = ()
        return True

# Apply globally
logging.getLogger().addFilter(SensitiveDataFilter())
```

## Masking in Allure Reports

```python
import allure
import re

MASK_PATTERNS = [
    re.compile(r'"(password|token|secret|api_key)":\s*"[^"]*"')]

def safe_attach(content, name, attachment_type=allure.attachment_type.TEXT):
    """Attach content to Allure with sensitive data masked."""
    masked = content
    for pattern in MASK_PATTERNS:
        masked = pattern.sub(lambda m: m.group().split(":")[0] + ': "***"', masked)
    allure.attach(masked, name, attachment_type)
```

## Custom Allure Logging for Requests

```python
class AllureLoggingSession(requests.Session):
    def request(self, method, url, **kwargs):
        response = super().request(method, url, **kwargs)

        with allure.step(f"{method.upper()} {url}"):
            # Mask headers
            safe_headers = dict(response.request.headers)
            if "Authorization" in safe_headers:
                safe_headers["Authorization"] = "Bearer ***"

            safe_attach(str(safe_headers), "Request Headers")

            if kwargs.get("json"):
                body = json.dumps(kwargs["json"], indent=2)
                safe_attach(body, "Request Body")

            safe_attach(
                response.text[:2000],
                f"Response [{response.status_code}]"
            )

        return response
```

## Environment Variable Protection

```python
# conftest.py
import os

@pytest.fixture(autouse=True, scope="session")
def protect_env_vars():
    """Ensure sensitive env vars exist but warn if missing."""
    required = ["TEST_API_TOKEN", "TEST_DB_PASSWORD"]
    missing = [v for v in required if not os.getenv(v)]
    if missing:
        pytest.skip(f"Missing env vars: {missing}")

    # Log that we have them (not their values)
    for var in required:
        logger.info(f"Env var {var}: {'set' if os.getenv(var) else 'missing'}")
```

## DevTools for UI Test Debugging

Browser DevTools from test code:

```python
# Playwright
page.on("console", lambda msg: logger.debug(f"Browser: {msg.text}"))
page.on("pageerror", lambda err: logger.error(f"Page error: {err}"))

# Selenium
logs = driver.get_log("browser")
for entry in logs:
    logger.debug(f"Browser [{entry['level']}]: {entry['message']}")
```

## Gotchas

- **Issue:** Allure report contains raw Bearer tokens in request headers visible to entire team. **Fix:** Always use masking session wrapper. Add a CI check that greps Allure output for token-like patterns.

- **Issue:** `logging.basicConfig()` called in conftest conflicts with pytest's log capture. **Fix:** Use `caplog` fixture or configure via `pytest.ini`: `log_cli = true`, `log_cli_level = DEBUG`.

- **Issue:** Masked logs make debugging impossible when the actual token/value is needed. **Fix:** Use a `--debug-secrets` CLI flag that disables masking in local runs only. Never allow in CI.

## See Also

- [[allure-reporting]]
- [[oauth-testing]]
- [[test-architecture]]
