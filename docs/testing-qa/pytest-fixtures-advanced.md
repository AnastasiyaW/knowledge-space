---
title: Pytest Fixtures - Advanced Patterns
category: patterns
tags: [pytest, fixtures, conftest, scope, yield, factory, dependency-injection]
---

# Pytest Fixtures - Advanced Patterns

Beyond basic fixtures: scoping strategies, factory patterns, fixture composition, and conftest hierarchy for large test suites.

## Fixture Scopes

```python
import pytest

@pytest.fixture(scope="session")
def db_connection():
    """One connection for entire test run."""
    conn = create_connection()
    yield conn
    conn.close()

@pytest.fixture(scope="module")
def test_user(db_connection):
    """One user per test module."""
    user = db_connection.create_user(name="test")
    yield user
    db_connection.delete_user(user.id)

@pytest.fixture(scope="function")  # default
def fresh_token(test_user):
    """New token per test function."""
    return test_user.generate_token()
```

- `session` - once per pytest run (DB connections, server startup)
- `module` - once per .py file (shared test data within module)
- `class` - once per test class
- `function` - once per test (default, safest)

## Factory Fixtures

When tests need multiple instances with different configs:

```python
@pytest.fixture
def make_user(db_connection):
    """Factory: create users with custom attributes."""
    created = []

    def _make_user(name="default", role="user", **kwargs):
        user = db_connection.create_user(name=name, role=role, **kwargs)
        created.append(user)
        return user

    yield _make_user

    # cleanup all created users
    for user in created:
        db_connection.delete_user(user.id)


def test_admin_permissions(make_user):
    admin = make_user(name="admin", role="admin")
    regular = make_user(name="regular", role="user")
    assert admin.can_delete(regular)
```

## Fixture Composition via conftest.py

```python
tests/
  conftest.py           # session-scoped: DB, app server
  api/
    conftest.py         # API client, auth tokens
    test_users.py
    test_orders.py
  ui/
    conftest.py         # browser, page objects
    test_login.py
```

Each `conftest.py` is auto-discovered by pytest. Fixtures cascade: inner conftest can use outer conftest fixtures.

```python
# tests/conftest.py
@pytest.fixture(scope="session")
def app():
    return create_app(config="test")

# tests/api/conftest.py
@pytest.fixture
def api_client(app):
    return app.test_client()

# tests/api/test_users.py
def test_list_users(api_client):
    resp = api_client.get("/api/users")
    assert resp.status_code == 200
```

## autouse Fixtures

```python
@pytest.fixture(autouse=True)
def reset_db(db_connection):
    """Runs before/after EVERY test in this scope."""
    yield
    db_connection.rollback()
```

- `autouse=True` applies the fixture to all tests in scope without explicit parameter
- Useful for cleanup, timing, logging
- Dangerous if scope is too broad - can slow test suite

## Yield Fixtures for Setup/Teardown

```python
@pytest.fixture
def temp_file():
    path = Path("/tmp/test_data.json")
    path.write_text('{"key": "value"}')
    yield path                    # test runs here
    path.unlink(missing_ok=True)  # cleanup after test
```

Everything before `yield` = setup. Everything after = teardown. Teardown runs even if the test fails.

## Request Object for Dynamic Fixtures

```python
@pytest.fixture
def browser(request):
    browser_name = request.param  # from parametrize
    driver = create_driver(browser_name)
    yield driver
    driver.quit()

@pytest.mark.parametrize("browser", ["chrome", "firefox"], indirect=True)
def test_homepage(browser):
    browser.get("https://example.com")
```

`request.node` gives access to test metadata (markers, name, module).

## Fixture Finalization with addfinalizer

```python
@pytest.fixture
def resource(request):
    r = acquire_resource()

    def cleanup():
        r.release()

    request.addfinalizer(cleanup)
    return r
```

Difference from yield: `addfinalizer` can register multiple cleanup callbacks, and each runs independently even if another fails.

## Environment-Aware Configuration

```python
# conftest.py
def pytest_addoption(parser):
    parser.addoption("--env", default="dev", choices=["dev", "staging", "prod"])

@pytest.fixture(scope="session")
def env_config(request):
    env = request.config.getoption("--env")
    return load_config(f"config/{env}.yaml")
```

Run with: `pytest --env=staging`

## Gotchas

- **Issue:** Fixture with `scope="session"` depends on `scope="function"` fixture -> `ScopeMismatch` error. **Fix:** Higher-scoped fixtures can only depend on same-or-higher-scoped fixtures. Restructure so session fixtures are self-contained.

- **Issue:** `autouse=True` on a session fixture in root conftest runs for ALL tests including unrelated ones. **Fix:** Place autouse fixtures in the narrowest conftest possible. Use markers to conditionally skip: `if "skip_db" in request.keywords: return`.

- **Issue:** Factory fixture creates resources but test fails before cleanup list is populated. **Fix:** Always append to cleanup list immediately after creation, before any assertions.

- **Issue:** Multiple conftest.py files define fixture with same name - silent override with no warning. **Fix:** Use unique prefixed names or keep fixture definitions in a single conftest level.

## See Also

- [[pytest-fundamentals]]
- [[test-architecture]]
- [[test-data-management]]
