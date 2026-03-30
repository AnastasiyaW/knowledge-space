---
title: Pydantic for Test Validation
category: technique
tags: [pydantic, validation, models, settings, response-validation, type-safety]
---
# Pydantic for Test Validation

Using Pydantic models for API response validation and test configuration management.

## Key Facts

- Pydantic v2: `BaseModel` for data validation with Python type hints
- Response deserialization: parse API JSON into typed models - catches missing/wrong fields automatically
- `pydantic-settings` (`BaseSettings`) for loading config from `.env` files and environment variables
- Validates types, required fields, string patterns, value ranges at parse time
- Nested models for complex JSON structures
- `model_dump()` / `model_dump_json()` for serialization
- `ConfigDict` for model configuration (aliases, extra fields policy)
- Replaces manual JSON key checks and jsonschema validation with type-safe models
- Integrates with [[api-testing-requests]] for response validation
- Integrates with [[pytest-fixtures]] for settings injection

## Patterns

```python
from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings
from typing import Optional
from enum import Enum

# Response model
class User(BaseModel):
    id: int
    name: str
    email: str
    role: str = "viewer"
    is_active: bool = True

# Nested models
class PaginatedResponse(BaseModel):
    total: int
    page: int
    per_page: int
    items: list[User]

# Validation in tests
def test_get_user(api_client):
    response = api_client.get("/users/1")
    assert response.status_code == 200

    user = User.model_validate(response.json())
    assert user.name == "Expected Name"
    assert user.is_active is True

# Enum for roles
class UserRole(str, Enum):
    ADMIN = "admin"
    VIEWER = "viewer"
    EDITOR = "editor"

class StrictUser(BaseModel):
    id: int
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(pattern=r'^[\w.-]+@[\w.-]+\.\w+$')
    role: UserRole

# Custom validator
class Course(BaseModel):
    id: int
    title: str
    max_students: int = Field(gt=0)

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()

# Settings from .env
# .env file:
# BASE_URL=https://staging.api.example.com
# API_TOKEN=secret123
# BROWSER=chromium

class TestSettings(BaseSettings):
    base_url: str = "http://localhost:8000"
    api_token: str = ""
    browser: str = "chromium"
    headless: bool = True
    timeout: int = 30

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

# Multiple env files per environment
class Settings(BaseSettings):
    base_url: str
    api_token: str

    model_config = ConfigDict(
        env_file=".env",  # default
    )

# Load specific env
settings = Settings(_env_file=".env.staging")

# Fixture for settings
import pytest

@pytest.fixture(scope="session")
def settings():
    return TestSettings()

@pytest.fixture(scope="session")
def api_client(settings):
    return APIClient(
        base_url=settings.base_url,
        token=settings.api_token
    )

# Request body model
class CreateUserRequest(BaseModel):
    name: str
    email: str
    role: UserRole = UserRole.VIEWER

def test_create_user(api_client):
    body = CreateUserRequest(
        name="Test User",
        email="test@example.com",
        role=UserRole.ADMIN
    )
    response = api_client.post("/users", json=body.model_dump())
    assert response.status_code == 201
    user = User.model_validate(response.json())
    assert user.role == "admin"
```

## Gotchas

- **Symptom**: `ValidationError` on API response - **Cause**: response JSON doesn't match model (missing field, wrong type) - this is the test catching a real bug
- **Symptom**: Pydantic v1 vs v2 API confusion - **Cause**: v2 renamed methods (`dict()` -> `model_dump()`, `parse_obj()` -> `model_validate()`) - **Fix**: use v2 API consistently
- **Symptom**: `.env` file not found - **Cause**: working directory mismatch - **Fix**: use absolute path or `env_file` relative to project root
- **Symptom**: extra fields in response cause error - **Cause**: strict model - **Fix**: add `model_config = ConfigDict(extra="ignore")` to allow extra fields
- Never commit `.env` files with real credentials to version control - add to `.gitignore`

## See Also

- [[api-testing-requests]] - API testing patterns
- [[test-data-management]] - environment-based configuration
- [[pytest-fixtures]] - settings fixture
- [Pydantic v2 docs](https://docs.pydantic.dev/latest/)
- [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
