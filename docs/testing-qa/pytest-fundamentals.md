---
title: Pytest Fundamentals
category: framework
tags: [pytest, fixtures, conftest, parametrize, xdist, markers, hooks, parallel, scope]
---

# Pytest Fundamentals

Pytest is Python's most powerful test framework. Fixtures replace setup/teardown with dependency-injected, scoped, composable functions. Parametrize generates test matrices. xdist enables parallel execution. Hooks extend pytest's behavior at every lifecycle point. Together they handle everything from unit tests to complex E2E suites.

## Key Facts

- Fixtures use `@pytest.fixture` + `yield` (before = setup, after = teardown); teardown runs even on failure
- Scopes: `function` (default), `class`, `module`, `session` - control fixture lifecycle
- `conftest.py` = auto-discovered, directory-scoped fixture/hook file (no imports needed)
- `parametrize` generates separate test cases; `indirect=True` passes values to fixtures via `request.param`
- `pytest-xdist` runs parallel processes (`-n 4`), NOT threads - session fixtures execute in EACH worker
- Hooks: `pytest_collection_modifyitems`, `pytest_runtest_call`, `pytest_generate_tests`, `pytest_addoption`

## Patterns

### Fixtures with Dependency Chain

```python
@pytest.fixture(scope="session")
def envs():
    load_dotenv()

@pytest.fixture(scope="session")
def gateway_url(envs):  # explicit dependency ensures order
    return os.getenv("GATEWAY_URL")

@pytest.fixture(scope="session")
def auth_token(gateway_url):
    return login_and_get_token(gateway_url)

@pytest.fixture
def spend(spend_client, category):
    created = spend_client.add_spend({"category": category, "amount": 100})
    yield created  # test runs here
    spend_client.delete_spend(created["id"])  # cleanup
```

### Parametrize

```python
@pytest.mark.parametrize("username, password, expected", [
    ("valid_user", "valid_pass", True),
    ("invalid_user", "wrong_pass", False)])
def test_login(username, password, expected):
    assert login(username, password) == expected

# Indirect: pass values to fixture
@pytest.fixture
def category(request):
    return create_if_missing(request.param)

@pytest.mark.parametrize("category", ["school", "food"], indirect=True)
def test_with_category(category):
    assert category is not None
```

### Parallel Execution (xdist)

```bash
pytest -n 4                    # 4 parallel workers
pytest -n auto                 # one worker per CPU core
pytest --dist=loadscope        # group by module (default)
pytest --dist=load             # distribute individual tests
```

Session fixtures run independently in each worker - with 4 workers, DB setup creates 4 databases. Use file locks or `--dist=loadscope` for shared resources.

### Marks and Test Selection

```python
@pytest.mark.skip(reason="Not implemented yet")
@pytest.mark.skipif(sys.platform == "win32", reason="Unix only")
@pytest.mark.xfail(reason="BUG-123")  # expected failure

# Localized xfail (preferred - catches unexpected breakage)
def test_buggy():
    setup_data()
    try:
        result = buggy_operation()
    except SomeError:
        pytest.xfail("BUG-123: specific operation fails")
```

```bash
pytest -k "mobile"           # name filter
pytest -k "not slow"         # exclude
pytest -k "login and api"    # boolean
```

### Custom Options via Hooks

```python
# conftest.py
def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome")

@pytest.fixture
def browser_name(request):
    return request.config.getoption("--browser")
```

### conftest Plugins (Scaling Fixtures)

```python
# conftest.py - solves bloated conftest and sibling-directory visibility
pytest_plugins = [
    "fixtures.user_fixtures",
    "fixtures.auth_fixtures",
    "fixtures.db_fixtures"]
```

### Fuzz Testing with Hypothesis

```python
from hypothesis import given, strategies as st

@given(st.integers(), st.integers())
def test_addition_commutative(a, b):
    assert add(a, b) == add(b, a)
# Generates 100 random combinations; best for pure functions, bad for I/O
```

## Gotchas

- `autouse=True` does NOT guarantee fixture order relative to other fixtures - use explicit dependencies
- Session-scoped fixtures with xdist run per-worker, not once globally
- `pytest -l` (showlocals) dumps ALL variables on failure - can expose secrets in CI logs
- Token expiration in session-scoped fixtures: long runs may fail mid-session; consider module scope or refresh logic
- Coverage ~85% = good target; 100% doesn't mean bug-free

## See Also

- [[allure-reporting]] - test reporting with Allure annotations
- [[page-object-model]] - fixture integration with POM
- [[test-architecture]] - project structure and conftest organization
- [[ci-cd-test-automation]] - running pytest in CI pipelines
