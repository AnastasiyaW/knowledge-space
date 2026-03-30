---
title: Error Handling and Logging
category: concepts
tags: [python, exceptions, logging, traceback, error-handling, custom-exceptions]
---

# Error Handling and Logging

Python uses exceptions for error control flow. The `logging` module provides a flexible, hierarchical logging system with handlers, formatters, and log levels. Combining structured exception handling with proper logging is essential for debuggable, production-grade applications.

## Key Facts

- Exception hierarchy: `BaseException` > `Exception` > `ValueError`, `TypeError`, etc.
- Never catch bare `except:` or `except BaseException` -- this swallows `KeyboardInterrupt` and `SystemExit`
- `except Exception as e:` catches all "normal" errors without swallowing system exits
- `raise ... from exc` chains exceptions, preserving the original traceback
- `ExceptionGroup` and `except*` (Python 3.11+) handle multiple concurrent errors
- Logging levels: `DEBUG` < `INFO` < `WARNING` < `ERROR` < `CRITICAL`
- `logging.getLogger(__name__)` creates a logger following the module hierarchy
- Structured logging (JSON) with `python-json-logger` or `structlog` is preferred for production
- See [[context-managers]] for `__exit__` exception handling, [[fastapi-fundamentals]] for HTTP exception patterns

## Patterns

### Custom Exception Hierarchy

```python
class AppError(Exception):
    """Base exception for the application."""
    def __init__(self, message: str, code: str = "UNKNOWN"):
        self.code = code
        super().__init__(message)

class NotFoundError(AppError):
    def __init__(self, entity: str, entity_id: int):
        super().__init__(f"{entity} #{entity_id} not found", code="NOT_FOUND")
        self.entity = entity
        self.entity_id = entity_id

class ValidationError(AppError):
    def __init__(self, field: str, reason: str):
        super().__init__(f"Validation failed for {field}: {reason}", code="VALIDATION")
        self.field = field
        self.reason = reason

# Usage
try:
    raise NotFoundError("User", 42)
except NotFoundError as e:
    print(e.code, e.entity, e.entity_id)  # NOT_FOUND User 42
except AppError as e:
    print(f"App error [{e.code}]: {e}")
```

### Exception Chaining

```python
import json

def parse_config(path: str) -> dict:
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError as e:
        raise ConfigError(f"Config file missing: {path}") from e
    except json.JSONDecodeError as e:
        raise ConfigError(f"Invalid JSON in {path}") from e

# Traceback shows both the original and the new exception:
# ConfigError: Config file missing: /etc/app.json
#   The above exception was the direct cause of:
# FileNotFoundError: [Errno 2] No such file or directory: '/etc/app.json'
```

### Logging Configuration

```python
import logging

# Basic setup (for scripts)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Module-level logger (recommended)
logger = logging.getLogger(__name__)

logger.debug("Detailed debug info: %s", data)    # lazy formatting
logger.info("User %s logged in", username)
logger.warning("Disk usage at %d%%", usage)
logger.error("Failed to connect to %s", host)
logger.exception("Unexpected error")  # includes traceback
```

### Production Logging Setup

```python
import logging
import logging.handlers
import sys

def setup_logging(level: str = "INFO"):
    root = logging.getLogger()
    root.setLevel(level)

    # Console handler -- human-readable
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    ))
    root.addHandler(console)

    # File handler -- rotating, for persistence
    file_handler = logging.handlers.RotatingFileHandler(
        "app.log", maxBytes=10_000_000, backupCount=5
    )
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(lineno)d): %(message)s"
    ))
    root.addHandler(file_handler)

    # Suppress noisy third-party loggers
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
```

### Structured Logging with `structlog`

```python
import structlog

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer(),
    ]
)

log = structlog.get_logger()
log.info("user_login", user_id=42, ip="10.0.0.1")
# {"event": "user_login", "user_id": 42, "ip": "10.0.0.1", "level": "info", "timestamp": "2026-..."}
```

### `ExceptionGroup` (Python 3.11+)

```python
# Handle multiple concurrent errors
async def process_batch(items):
    errors = []
    for item in items:
        try:
            await process(item)
        except Exception as e:
            errors.append(e)
    if errors:
        raise ExceptionGroup("batch processing failed", errors)

try:
    await process_batch(items)
except* ValueError as eg:
    print(f"Validation errors: {eg.exceptions}")
except* ConnectionError as eg:
    print(f"Connection errors: {eg.exceptions}")
```

## Gotchas

- **`logger.error(f"Error: {e}")` -- eager formatting**: wastes CPU if the message is filtered. Use `logger.error("Error: %s", e)` -- formatting is deferred until the message is actually emitted
- **`except Exception` swallows too much**: catching `Exception` in a loop silently ignores programming errors (`AttributeError`, `TypeError`). Catch specific exceptions when possible
- **`logging.exception()` outside `except` block**: logs `NoneType: None` for traceback. Only call inside an `except` handler
- **Logger hierarchy**: `getLogger("app.db")` is a child of `getLogger("app")`. Setting `app` to `WARNING` silences `app.db` `INFO` messages unless `app.db` has its own handler
- **`raise` vs `raise e`**: bare `raise` re-raises with original traceback. `raise e` resets the traceback to the current line, losing the original call stack

## See Also

- [logging -- Python docs](https://docs.python.org/3/library/logging.html)
- [Built-in Exceptions -- Python docs](https://docs.python.org/3/library/exceptions.html)
- [[context-managers]] - exception handling in `__exit__`
- [[testing-with-pytest]] - `pytest.raises` for testing exceptions
