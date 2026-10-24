---
title: "Test-Logging und Maskierung von Geheimnissen"
category: patterns
tags: [logging, secrets, masking, sensitive-data, allure, debugging, filters]
level: 3
source_sha256: 17b1c2db2bbcfdf1081f16eb230ba6dfa196c73a25fa97d0f3686c3abe4a6671
translation: machine
translated_at: '2026-10-24'
---
# Test-Logging und Maskierung von Geheimnissen {#test-logging-and-secret-masking}

Strukturiertes Logging in Test-Frameworks, Maskierung sensibler Daten in Logs und Reports sowie DevTools-Techniken für das Debugging von Tests.

## Python-Logging in Tests {#python-logging-in-tests}

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

## HTTP-Request/Response-Logging {#http-requestresponse-logging}

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

## Maskierung von Geheimnissen in Logs {#secret-masking-in-logs}

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

## Maskierung in Allure-Reports {#masking-in-allure-reports}

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

## Benutzerdefiniertes Allure-Logging für Requests {#custom-allure-logging-for-requests}

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

## Schutz von Umgebungsvariablen {#environment-variable-protection}

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

## DevTools für das Debugging von UI-Tests {#devtools-for-ui-test-debugging}

Browser-DevTools aus dem Testcode heraus:

```python
# Playwright
page.on("console", lambda msg: logger.debug(f"Browser: {msg.text}"))
page.on("pageerror", lambda err: logger.error(f"Page error: {err}"))

# Selenium
logs = driver.get_log("browser")
for entry in logs:
    logger.debug(f"Browser [{entry['level']}]: {entry['message']}")
```

## Stolperfallen {#gotchas}

- **Problem:** Der Allure-Report enthält rohe Bearer-Tokens in Request-Headern, die für das gesamte Team sichtbar sind. **Lösung:** Immer den Masking-Session-Wrapper verwenden. Eine CI-Prüfung ergänzen, die die Allure-Ausgabe nach tokenähnlichen Mustern durchsucht.

- **Problem:** `logging.basicConfig()` in der `conftest` führt zu Konflikten mit der Log-Erfassung von pytest. **Lösung:** Die `caplog`-Fixture verwenden oder über `pytest.ini` konfigurieren: `log_cli = true`, `log_cli_level = DEBUG`.

- **Problem:** Maskierte Logs machen das Debugging unmöglich, wenn der tatsächliche Token- bzw. Wert benötigt wird. **Lösung:** Ein CLI-Flag `--debug-secrets` verwenden, das die Maskierung nur in lokalen Läufen deaktiviert. In der CI niemals zulassen.

## Siehe auch {#see-also}

- [[allure-reporting]]
- [[oauth-testing]]
- [[test-architecture]]
