---
title: Test Data Management
category: patterns
tags: [test-data, fixtures, factories, env-config, dotenv, parametrize, data-driven]
---

# Test Data Management

Strategies for creating, managing, and cleaning up test data across environments. Covers environment configs, data factories, parametrization, and file-based test data.

## Environment Configuration

```python
# config.py
from pydantic_settings import BaseSettings

class TestConfig(BaseSettings):
    base_url: str = "http://localhost:8000"
    db_url: str = "postgresql://test:test@localhost/testdb"
    api_token: str = ""

    class Config:
        env_file = ".env"
        env_prefix = "TEST_"
```

```bash
# .env.dev
TEST_BASE_URL=http://localhost:8000
TEST_API_TOKEN=dev-token-123

# .env.staging
TEST_BASE_URL=https://staging.example.com
TEST_API_TOKEN=staging-token-456
```

```python
# conftest.py
@pytest.fixture(scope="session")
def config():
    env = os.getenv("TEST_ENV", "dev")
    return TestConfig(_env_file=f".env.{env}")
```

Run: `TEST_ENV=staging pytest`

## Parametrize for Data-Driven Tests

```python
@pytest.mark.parametrize("username,password,expected_status", [
    ("admin", "admin123", 200),
    ("admin", "wrong", 401),
    ("", "admin123", 422),
    ("nonexistent", "pass", 401)])
def test_login(api_client, username, password, expected_status):
    resp = api_client.post("/login", json={"username": username, "password": password})
    assert resp.status_code == expected_status
```

## External Data Files

```python
import json
import csv

def load_test_data(filename):
    path = Path(__file__).parent / "data" / filename
    if path.suffix == ".json":
        return json.loads(path.read_text())
    elif path.suffix == ".csv":
        with open(path) as f:
            return list(csv.DictReader(f))

@pytest.mark.parametrize("case", load_test_data("login_cases.json"))
def test_login_from_file(api_client, case):
    resp = api_client.post("/login", json=case["input"])
    assert resp.status_code == case["expected_status"]
```

## Database Fixtures with Rollback

```python
@pytest.fixture
def db_session(db_engine):
    """Each test gets a transaction that rolls back."""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()
```

Every test sees a clean database state without expensive re-creation.

## Random but Reproducible Data

```python
from faker import Faker

fake = Faker()
Faker.seed(42)  # reproducible across runs

@pytest.fixture
def random_user():
    return {
        "name": fake.name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
    }
```

## Cleanup Strategies

| Strategy | When to use |
|----------|-------------|
| Transaction rollback | DB tests, fastest |
| Fixture teardown (yield) | API-created resources |
| Factory + collector | Multiple resources per test |
| Database truncation | Full integration tests |
| Docker recreate | Complete isolation needed |

```python
@pytest.fixture
def created_resources():
    """Collector pattern for cleanup."""
    resources = []
    yield resources
    for resource_type, resource_id in reversed(resources):
        delete_resource(resource_type, resource_id)

def test_order_flow(api_client, created_resources):
    user = api_client.post("/users", json={...}).json()
    created_resources.append(("user", user["id"]))

    order = api_client.post("/orders", json={"user_id": user["id"]}).json()
    created_resources.append(("order", order["id"]))
```

## Gotchas

- **Issue:** Hardcoded test data (user IDs, URLs) breaks when switching environments. **Fix:** All environment-specific values go into config files loaded by fixtures. Never hardcode `/api/users/2` - use `f"/api/users/{user_id}"`.

- **Issue:** Tests depend on data created by other tests (ordering dependency). **Fix:** Each test must create its own data via fixtures. Use `pytest-randomly` to catch hidden ordering dependencies.

- **Issue:** `.env` file with real credentials committed to git. **Fix:** Add `.env*` to `.gitignore`. Use `.env.example` with dummy values. CI gets secrets from environment variables.

## See Also

- [[pytest-fixtures-advanced]]
- [[database-testing]]
- [[pydantic-test-models]]
