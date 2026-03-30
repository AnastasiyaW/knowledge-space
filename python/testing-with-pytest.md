---
title: Testing with Pytest
category: concepts
tags: [python, pytest, testing, fixtures, mocking, parametrize, tdd]
---

# Testing with Pytest

`pytest` is Python's de facto testing framework. It uses plain `assert` statements, powerful fixtures for setup/teardown, parametrization for data-driven tests, and a rich plugin ecosystem. Tests are discovered automatically by file/function naming conventions.

## Key Facts

- Test discovery: files named `test_*.py` or `*_test.py`, functions/methods starting with `test_`
- Plain `assert` with introspection -- no need for `self.assertEqual`, pytest rewrites assertions to show diffs
- Fixtures provide dependency injection for tests; `@pytest.fixture` with scopes: `function`, `class`, `module`, `session`
- `@pytest.mark.parametrize` runs a test with multiple input sets
- `monkeypatch` fixture patches attributes, environment variables, dictionaries at test scope
- `pytest.raises(ExcType)` as context manager asserts an exception is raised
- `conftest.py` shares fixtures across test modules without imports
- `pytest-cov` for coverage, `pytest-asyncio` for async tests, `pytest-mock` for `unittest.mock` integration
- See [[error-handling-and-logging]] for exception patterns, [[fastapi-fundamentals]] for `TestClient`

## Patterns

### Basic Test with Assert

```python
# test_calculator.py
def add(a: int, b: int) -> int:
    return a + b

def test_add_positive():
    assert add(2, 3) == 5

def test_add_negative():
    assert add(-1, -1) == -2

def test_add_mixed():
    result = add(-1, 1)
    assert result == 0, f"Expected 0, got {result}"
```

### Fixtures

```python
import pytest

@pytest.fixture
def db_session():
    """Create a test database session."""
    session = create_test_session()
    yield session          # test runs here
    session.rollback()     # cleanup after test
    session.close()

@pytest.fixture
def sample_user(db_session):
    """Fixture that depends on another fixture."""
    user = User(name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.flush()
    return user

def test_user_creation(db_session, sample_user):
    assert sample_user.id is not None
    found = db_session.query(User).get(sample_user.id)
    assert found.name == "Test User"
```

### Parametrize

```python
import pytest

@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
    ("", ""),
    ("123abc", "123ABC"),
])
def test_upper(input, expected):
    assert input.upper() == expected

@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (-1, 1, 0),
    (0, 0, 0),
    (100, -50, 50),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

### Mocking and Monkeypatch

```python
import pytest
from unittest.mock import AsyncMock, patch

def test_env_variable(monkeypatch):
    monkeypatch.setenv("API_KEY", "test-key-123")
    from myapp.config import get_api_key
    assert get_api_key() == "test-key-123"

def test_with_mock():
    with patch("myapp.services.external_api.fetch") as mock_fetch:
        mock_fetch.return_value = {"status": "ok"}
        result = process_data()
        assert result["status"] == "ok"
        mock_fetch.assert_called_once()

@pytest.mark.asyncio
async def test_async_service():
    mock_client = AsyncMock()
    mock_client.get.return_value.json.return_value = {"id": 1}
    result = await fetch_user(mock_client, user_id=1)
    assert result["id"] == 1
```

### Testing Exceptions

```python
import pytest

def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        1 / 0

def test_validation_error_message():
    with pytest.raises(ValueError, match=r"must be positive"):
        create_product(price=-1)

def test_exception_attributes():
    with pytest.raises(NotFoundError) as exc_info:
        find_user(999)
    assert exc_info.value.entity == "User"
    assert exc_info.value.entity_id == 999
```

### FastAPI TestClient

```python
import pytest
from fastapi.testclient import TestClient
from myapp.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_create_user(client):
    response = client.post("/users/", json={
        "name": "Alice",
        "email": "alice@example.com"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Alice"
    assert "id" in data

def test_get_nonexistent_user(client):
    response = client.get("/users/99999")
    assert response.status_code == 404
```

### `conftest.py` for Shared Fixtures

```python
# tests/conftest.py -- shared across all tests in this directory
import pytest

@pytest.fixture(scope="session")
def database():
    """Session-scoped: created once, shared across all tests."""
    db = setup_test_database()
    yield db
    teardown_test_database(db)

@pytest.fixture(autouse=True)
def reset_db(database):
    """Auto-used: runs before each test to reset state."""
    database.reset()
```

## Gotchas

- **Fixture scope mismatch**: a `function`-scoped fixture cannot depend on a `session`-scoped fixture that yields mutable state -- changes from one test leak into the next
- **`monkeypatch` path**: `monkeypatch.setattr("myapp.views.requests.get", mock)` patches where the name is **used**, not where it is **defined**. If `views.py` does `from requests import get`, patch `myapp.views.get`
- **Async tests need `pytest-asyncio`**: install it and mark tests with `@pytest.mark.asyncio`. Without the marker, the test returns a coroutine and "passes" without executing
- **`conftest.py` location matters**: fixtures in `tests/conftest.py` are available to all tests under `tests/`. Fixtures in `tests/api/conftest.py` are only available to `tests/api/`
- **`parametrize` with fixtures**: you cannot directly parametrize fixture values via `@pytest.mark.parametrize`. Use `indirect=True` or `pytest.fixture(params=[...])` instead

## See Also

- [pytest documentation](https://docs.pytest.org/)
- [unittest.mock -- Python docs](https://docs.python.org/3/library/unittest.mock.html)
- [[error-handling-and-logging]] - testing exception hierarchies
- [[fastapi-fundamentals]] - `TestClient` for API testing
