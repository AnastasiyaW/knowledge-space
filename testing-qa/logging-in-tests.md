---
title: Logging in Tests
category: technique
tags: [logging, debugging, python-logging, test-output, tracing]
---
# Logging in Tests

Adding structured logging to test frameworks for debugging, tracing, and audit trails.

## Key Facts

- Python `logging` module - standard library, configurable levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Custom logger per module: `logger = logging.getLogger(__name__)`
- Log API requests/responses for debugging failed tests
- Log test steps (assertions, data transformations) for traceability
- `pytest --log-cli-level=INFO` - show log output in real-time during test execution
- `pytest.ini` logging config: `log_cli`, `log_cli_level`, `log_format`
- Combine with [[allure-reporting]] steps for both human and machine readability
- Structured logging (JSON format) for log aggregation in CI/CD environments
- Log levels: DEBUG (request details), INFO (test steps), WARNING (non-critical issues), ERROR (failures)

## Patterns

```python
import logging

# Configure custom logger
logger = logging.getLogger("api_tests")

def setup_logger():
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger

# Logging in API client
class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.logger = logging.getLogger("api_client")

    def get(self, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        self.logger.info(f"GET {url}")
        response = requests.get(url, **kwargs)
        self.logger.info(f"Response: {response.status_code}")
        self.logger.debug(f"Body: {response.text[:500]}")
        return response

    def post(self, endpoint, json=None, **kwargs):
        url = f"{self.base_url}{endpoint}"
        self.logger.info(f"POST {url}")
        self.logger.debug(f"Payload: {json}")
        response = requests.post(url, json=json, **kwargs)
        self.logger.info(f"Response: {response.status_code}")
        return response

# Logging in assertions
class Assertions:
    logger = logging.getLogger("assertions")

    @staticmethod
    def check_status(response, expected):
        actual = response.status_code
        Assertions.logger.info(
            f"Check status: expected={expected}, actual={actual}"
        )
        assert actual == expected, (
            f"Status mismatch: expected {expected}, got {actual}"
        )

    @staticmethod
    def check_field(data, field, expected):
        actual = data.get(field)
        Assertions.logger.info(
            f"Check {field}: expected={expected}, actual={actual}"
        )
        assert actual == expected

# pytest.ini logging config
# [pytest]
# log_cli = true
# log_cli_level = INFO
# log_cli_format = %(asctime)s %(levelname)s %(message)s
# log_cli_date_format = %H:%M:%S
# log_file = test_execution.log
# log_file_level = DEBUG

# Logging with allure integration
import allure

def log_and_step(message, level="info"):
    """Log message and create Allure step."""
    getattr(logger, level)(message)
    with allure.step(message):
        pass
```

## Gotchas

- **Symptom**: no log output visible during pytest run - **Cause**: pytest captures stdout/stderr by default - **Fix**: use `pytest --log-cli-level=INFO` or configure in `pytest.ini`
- **Symptom**: duplicate log messages - **Cause**: adding handlers multiple times (e.g., in fixture called per test) - **Fix**: check `if not logger.handlers:` before adding, or configure in `conftest.py` session fixture
- **Symptom**: sensitive data in logs (tokens, passwords) - **Cause**: logging full request headers/bodies - **Fix**: mask sensitive fields before logging
- Don't log at DEBUG level in CI by default - too verbose; use INFO for CI, DEBUG for local debugging

## See Also

- [[allure-reporting]] - visual test reporting with steps
- [[api-testing-requests]] - logging API interactions
- [[test-project-structure]] - where to configure logging
- [Python logging docs](https://docs.python.org/3/library/logging.html)
- [pytest logging docs](https://docs.pytest.org/en/stable/how-to/logging.html)
