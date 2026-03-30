---
title: Pytest Parametrize
category: framework
tags: [pytest, parametrize, data-driven, test-matrix]
---
# Pytest Parametrize

Data-driven testing - run the same test logic with different inputs and expected outputs.

## Key Facts

- `@pytest.mark.parametrize("arg_names", values_list)` decorator
- Each set of values creates an independent test case with unique test ID
- Multiple `@pytest.mark.parametrize` decorators = cartesian product (test matrix)
- Custom test IDs via `ids` parameter or `pytest.param(..., id="name")`
- `pytest.param(..., marks=pytest.mark.xfail)` - mark individual parameter sets
- Can parametrize fixtures with `@pytest.fixture(params=[...])` for reusable variants
- `indirect=True` - pass parameter values through fixtures instead of directly to test
- Combine with [[pytest-fixtures]] for complex data preparation

## Patterns

```python
import pytest

# Basic parametrize
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (0, 0),
    (-1, -2),
])
def test_double(input, expected):
    assert input * 2 == expected

# With custom IDs
@pytest.mark.parametrize("status_code,is_success", [
    pytest.param(200, True, id="ok"),
    pytest.param(404, False, id="not-found"),
    pytest.param(500, False, id="server-error"),
])
def test_status_check(status_code, is_success):
    assert (status_code < 400) == is_success

# Cartesian product (2x3 = 6 test cases)
@pytest.mark.parametrize("method", ["GET", "POST"])
@pytest.mark.parametrize("endpoint", ["/users", "/courses", "/files"])
def test_api_access(api_client, method, endpoint):
    response = api_client.request(method, endpoint)
    assert response.status_code != 500

# Marking individual cases
@pytest.mark.parametrize("browser", [
    "chrome",
    "firefox",
    pytest.param("safari", marks=pytest.mark.xfail(reason="Safari flaky")),
])
def test_login(browser):
    ...

# Parametrized fixture
@pytest.fixture(params=["sqlite", "postgres"])
def db(request):
    conn = connect(request.param)
    yield conn
    conn.close()

def test_insert(db):  # runs twice - once per DB
    db.insert({"key": "value"})
    assert db.count() == 1

# indirect parametrize - values go through fixture
@pytest.fixture
def user(request):
    return create_user(role=request.param)

@pytest.mark.parametrize("user", ["admin", "viewer"], indirect=True)
def test_permissions(user):
    ...
```

## Gotchas

- **Symptom**: `TypeError: test_x() got multiple values for argument` - **Cause**: parameter name conflicts with fixture name - **Fix**: use distinct names for parametrize args and fixtures
- **Symptom**: hundreds of test cases from matrix - **Cause**: multiple `@pytest.mark.parametrize` decorators create cartesian product - **Fix**: combine into single decorator if product not needed
- String arguments in parametrize IDs with special chars can break XML reports - use `ids` parameter
- Parametrize values are evaluated at collection time, not at test time - avoid side effects in value lists

## See Also

- [[pytest-fixtures]] - parametrized fixtures, indirect
- [[test-data-management]] - generating test data with Faker
- [[pytest-fundamentals]] - markers, test selection
- [pytest parametrize docs](https://docs.pytest.org/en/stable/how-to/parametrize.html)
