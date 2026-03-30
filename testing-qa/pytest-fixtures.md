---
title: Pytest Fixtures
category: framework
tags: [pytest, fixtures, conftest, setup, teardown, yield, scope, dependency-injection]
---
# Pytest Fixtures

Fixtures provide setup/teardown, test data, and dependencies via injection - the core pytest mechanism for test infrastructure.

## Key Facts

- Fixtures are functions decorated with `@pytest.fixture` - injected by name into test function parameters
- `conftest.py` makes fixtures available to all tests in that directory and below without imports
- Scopes: `function` (default, per test), `class`, `module`, `package`, `session` (once per entire run)
- `yield` in fixture = setup before yield, teardown after yield (replaces `addfinalizer`)
- `autouse=True` - fixture runs for every test without explicit request
- Fixtures can request other fixtures (dependency chain)
- `request` parameter gives access to test context: `request.param`, `request.node`, `request.config`
- Factory fixtures return callables for creating multiple instances with different params
- Built-in fixtures: `tmp_path`, `capsys`, `monkeypatch`, `request`, `pytestconfig`

## Patterns

```python
import pytest

# Basic fixture with teardown
@pytest.fixture
def db_connection():
    conn = create_connection()
    yield conn
    conn.close()

# Session-scoped fixture (once per test session)
@pytest.fixture(scope="session")
def api_client(base_url):
    client = APIClient(base_url)
    client.authenticate()
    yield client
    client.logout()

# Parametrized fixture
@pytest.fixture(params=["chrome", "firefox"])
def browser(request):
    driver = create_driver(request.param)
    yield driver
    driver.quit()

# Factory fixture
@pytest.fixture
def create_user(api_client):
    created_users = []
    def _create_user(**kwargs):
        user = api_client.create_user(**kwargs)
        created_users.append(user)
        return user
    yield _create_user
    for user in created_users:
        api_client.delete_user(user.id)

# Autouse fixture
@pytest.fixture(autouse=True)
def log_test_name(request):
    print(f"\nStarting: {request.node.name}")
    yield
    print(f"Finished: {request.node.name}")

# conftest.py hierarchy
# tests/conftest.py         - session/module fixtures
# tests/api/conftest.py     - API-specific fixtures
# tests/ui/conftest.py      - UI-specific fixtures

# Fixture requesting another fixture
@pytest.fixture
def authenticated_user(api_client, create_user):
    user = create_user(role="admin")
    api_client.login_as(user)
    return user

# Built-in tmp_path fixture
def test_write_file(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("hello")
    assert file.read_text() == "hello"

# monkeypatch fixture
def test_env_var(monkeypatch):
    monkeypatch.setenv("API_URL", "http://localhost:8000")
    assert os.environ["API_URL"] == "http://localhost:8000"
```

## Gotchas

- **Symptom**: fixture finalizer not running - **Cause**: using `return` instead of `yield` - **Fix**: use `yield` for setup/teardown pattern
- **Symptom**: `ScopeMismatch` error - **Cause**: function-scoped fixture requesting session-scoped fixture's mutable state or lower scope requesting higher - **Fix**: match fixture scopes; lower scope can request higher but not vice versa
- **Symptom**: `autouse=True` fixture running in unexpected tests - **Cause**: placed in root `conftest.py` - **Fix**: move to appropriate subdirectory conftest
- Session-scoped fixtures: be careful with shared mutable state between tests - can cause flaky tests
- Fixture teardown (after `yield`) runs even if test fails - good for cleanup

## See Also

- [[pytest-fundamentals]] - test discovery, assertions, markers
- [[test-data-management]] - Faker, test data generation
- [[pytest-parametrize]] - parametrized fixtures and tests
- [pytest fixtures docs](https://docs.pytest.org/en/stable/how-to/fixtures.html)
