---
title: Pytest Fundamentals
category: framework
tags: [pytest, test-runner, python, assertions, markers, conftest]
---
# Pytest Fundamentals

Core test framework for Python - test discovery, assertions, markers, and configuration.

## Key Facts

- Test files must match `test_*.py` or `*_test.py`; functions/methods must start with `test_`
- No boilerplate: plain `assert` statements with automatic introspection (shows actual vs expected on failure)
- `conftest.py` - shared fixtures/hooks/plugins, auto-discovered per directory; no imports needed
- Markers: `@pytest.mark.skip`, `@pytest.mark.xfail`, `@pytest.mark.slow`, custom markers via `pytest.ini`
- `-k "expression"` - filter tests by keyword expression (name matching)
- `-m "marker"` - filter by marker (e.g., `pytest -m "not slow"`)
- `--collect-only` / `--co` - list tests without running them
- `pytest.ini` or `pyproject.toml` `[tool.pytest.ini_options]` for project-wide config
- Exit codes: 0=all passed, 1=some failed, 2=interrupted, 5=no tests collected
- [[pytest-fixtures]] provide setup/teardown via dependency injection

## Patterns

```python
# Basic test
def test_addition():
    assert 1 + 1 == 2

# Assertion with message
def test_status_code(response):
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

# Testing exceptions
import pytest

def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        1 / 0

def test_value_error_message():
    with pytest.raises(ValueError, match="invalid literal"):
        int("abc")

# Custom markers in pytest.ini
# [pytest]
# markers =
#     smoke: smoke test suite
#     regression: full regression suite

@pytest.mark.smoke
def test_login():
    ...

# conftest.py - shared fixtures
import pytest

@pytest.fixture
def base_url():
    return "https://api.example.com/v1"

# Selecting tests
# pytest -k "test_login or test_register"
# pytest -m smoke
# pytest tests/api/ -v
# pytest --tb=short  (traceback format)
```

## Gotchas

- **Symptom**: tests not discovered - **Cause**: file/function not matching naming convention or `__init__.py` missing in test dirs - **Fix**: follow `test_*.py` naming, check `testpaths` in config
- **Symptom**: fixtures from conftest not found - **Cause**: conftest.py not in parent directory of test file or has syntax error - **Fix**: place conftest.py at correct directory level
- **Symptom**: marker warning "Unknown pytest.mark.X" - **Cause**: custom marker not registered - **Fix**: add to `markers` list in `pytest.ini`
- Running `pytest` from wrong directory can miss `conftest.py` - always run from project root

## See Also

- [[pytest-fixtures]] - fixture scopes, yield, factory pattern
- [[pytest-parametrize]] - data-driven testing
- [[pytest-plugins-and-parallel]] - xdist, plugins
- [pytest documentation](https://docs.pytest.org/en/stable/)
- [pytest configuration](https://docs.pytest.org/en/stable/reference/customize.html)
