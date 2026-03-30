---
title: Test Data Management
category: technique
tags: [faker, test-data, fixtures, factory, data-generation, isolation]
---
# Test Data Management

Strategies for generating, managing, and isolating test data - Faker, factories, fixtures.

## Key Facts

- `faker` library generates realistic fake data: names, emails, addresses, phone numbers, text
- Each test should create its own data - never depend on pre-existing database state
- Factory pattern: reusable functions/classes that produce test objects with sensible defaults
- Test data isolation: each test creates, uses, and cleans up its own data
- Unique data prevents parallel test conflicts - use UUIDs, timestamps, or Faker-generated values
- Environment files (`.env`) store config; `python-dotenv` or Pydantic Settings load them
- Fixtures create test data in setup, clean up in teardown (yield pattern)
- [[pytest-parametrize]] for running same test with multiple data sets

## Patterns

```python
from faker import Faker
import pytest

fake = Faker()

# Basic Faker usage
def test_user_creation(api_client):
    user_data = {
        "name": fake.name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "address": fake.address(),
    }
    response = api_client.create_user(**user_data)
    assert response.status_code == 201

# Faker with locale
fake_ru = Faker("ru_RU")
fake_ru.name()      # Russian name
fake_ru.address()    # Russian address

# Faker seed for reproducibility
Faker.seed(42)
fake.name()  # always same result with same seed

# Factory function
def create_test_user(**overrides):
    defaults = {
        "name": fake.name(),
        "email": fake.unique.email(),
        "role": "viewer",
        "is_active": True,
    }
    defaults.update(overrides)
    return defaults

def test_admin_access(api_client):
    admin = create_test_user(role="admin")
    response = api_client.create_user(**admin)
    assert response.status_code == 201

# Factory fixture with cleanup
@pytest.fixture
def user_factory(api_client):
    created = []
    def _create(**kwargs):
        data = create_test_user(**kwargs)
        resp = api_client.create_user(**data)
        user = resp.json()
        created.append(user["id"])
        return user
    yield _create
    for uid in created:
        api_client.delete_user(uid)

def test_multiple_users(user_factory):
    admin = user_factory(role="admin")
    viewer = user_factory(role="viewer")
    assert admin["role"] != viewer["role"]

# Environment-based configuration
# .env file:
# API_BASE_URL=https://staging.api.example.com
# API_TOKEN=secret_token_123

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_base_url: str = "http://localhost:8000"
    api_token: str = ""

    class Config:
        env_file = ".env"

settings = Settings()

# Data builders (builder pattern)
class UserBuilder:
    def __init__(self):
        self._data = {
            "name": fake.name(),
            "email": fake.unique.email(),
            "role": "viewer",
        }

    def with_role(self, role):
        self._data["role"] = role
        return self

    def with_name(self, name):
        self._data["name"] = name
        return self

    def build(self):
        return self._data

user = UserBuilder().with_role("admin").with_name("Test Admin").build()
```

## Gotchas

- **Symptom**: `faker.unique` raises `UniquenessException` - **Cause**: exhausted unique values in long test sessions - **Fix**: call `fake.unique.clear()` in fixture teardown or between test modules
- **Symptom**: tests fail with duplicate data errors - **Cause**: using static test data across parallel tests - **Fix**: generate unique data with Faker or UUID per test
- **Symptom**: test database fills up over multiple runs - **Cause**: missing cleanup in teardown - **Fix**: use yield fixtures with cleanup, or transaction rollback strategy
- Don't use production data in tests - generate everything; secrets in `.env` files excluded from version control

## See Also

- [[pytest-fixtures]] - factory fixtures, cleanup patterns
- [[pytest-parametrize]] - data-driven tests
- [[pydantic-test-validation]] - settings management with Pydantic
- [Faker docs](https://faker.readthedocs.io/)
- [python-dotenv](https://saurabh-kumar.com/python-dotenv/)
