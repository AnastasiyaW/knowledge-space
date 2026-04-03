---
title: Testing with Pytest
category: concepts
tags: [python, pytest, unittest, testing, fixtures, mocking, coverage]
---

# Testing with Pytest

pytest is the de facto standard Python testing framework - more concise and powerful than built-in unittest. It uses plain `assert` statements, fixtures for setup/teardown, and parametrize for data-driven tests.

## Key Facts

- Test files: `test_*.py` or `*_test.py`; test functions: `test_*`
- Plain `assert` with descriptive failure messages (no `self.assertEqual`)
- Fixtures provide reusable setup/teardown with dependency injection
- `conftest.py` shares fixtures across test files (auto-discovered, no import needed)
- Fixture scopes: function (default), class, module, session
- `pytest-cov` for coverage reports; `pytest-mock` for mocking

## Patterns

### Basic Tests
```python
def test_addition():
    assert add(2, 3) == 5

def test_raises():
    import pytest
    with pytest.raises(ValueError):
        parse_int("abc")

def test_approximate():
    assert 0.1 + 0.2 == pytest.approx(0.3)
```

### Fixtures
```python
import pytest

@pytest.fixture
def db_session():
    session = create_session()
    yield session       # test runs here
    session.close()     # cleanup after test

@pytest.fixture
def sample_user(db_session):  # fixtures can depend on other fixtures
    user = User(name="test", email="test@test.com")
    db_session.add(user)
    db_session.commit()
    return user

def test_user_exists(db_session, sample_user):
    result = db_session.query(User).filter_by(name="test").first()
    assert result.email == "test@test.com"
```

### Fixture Scopes
```python
@pytest.fixture(scope="session")   # once per entire test session
def app():
    return create_app(testing=True)

@pytest.fixture(scope="module")    # once per test file
def db():
    return setup_db()
```

### conftest.py (Shared Fixtures)
```python
# conftest.py - auto-discovered by pytest
@pytest.fixture(scope="session")
def app():
    return create_app(testing=True)

@pytest.fixture(scope="session")
def client(app):
    return TestClient(app)
```

### Parametrize
```python
@pytest.mark.parametrize("input,expected", [
    ("hello", 5),
    ("", 0),
    ("hi", 2),
])
def test_string_length(input, expected):
    assert len(input) == expected

# Parameterize fixtures too
@pytest.fixture(params=["sqlite", "postgresql"])
def db_engine(request):
    return create_engine(request.param)
```

### Testing FastAPI
```python
from fastapi.testclient import TestClient
from httpx import AsyncClient

# Sync testing
client = TestClient(app)
response = client.get("/api/hotels")
assert response.status_code == 200

# Async testing
@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.anyio
async def test_endpoint(async_client):
    response = await async_client.get("/api/hotels")
    assert response.status_code == 200
```

### Authenticated Test Client
```python
@pytest.fixture
async def auth_client(async_client):
    await async_client.post("/auth/login", json={
        "email": "test@test.com", "password": "test"
    })
    return async_client  # cookie stored in client
```

### Coverage
```bash
pip install pytest-cov
pytest --cov=mypackage --cov-report=html
# Generates htmlcov/ directory with visual report
```

## unittest (Built-in)

```python
import unittest

class TestMyCode(unittest.TestCase):
    def setUp(self):
        self.data = create_test_data()

    def tearDown(self):
        cleanup()

    def test_addition(self):
        self.assertEqual(add(2, 3), 5)

    def test_raises(self):
        with self.assertRaises(ValueError):
            parse_int("abc")

    def test_parameterized(self):
        for num in [2, 4, 6]:
            with self.subTest(num=num):
                self.assertTrue(num % 2 == 0)
```

## Testing Pyramid

1. **Unit tests** (most) - individual functions, fast, mock externals
2. **Integration tests** (middle) - component interaction, real/test DB
3. **E2E tests** (fewest) - full workflows, slowest, most brittle

## Gotchas

- Test both happy path and error cases
- Don't test implementation details - test behavior
- Mock external dependencies (APIs, email) for unit tests; use real deps for integration
- `pytest.fixture` with `yield` ensures cleanup runs even if test fails
- `conftest.py` at different directory levels provides different fixture scopes

## See Also

- [[error-handling]] - testing exception raising
- [[fastapi-fundamentals]] - endpoint testing
- [[type-hints]] - mypy in CI pipeline
