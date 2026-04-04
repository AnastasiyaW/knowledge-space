---
title: Pydantic for Test Validation
category: patterns
tags: [pydantic, validation, response-models, schema, type-checking, api-testing, basemodel]
---

# Pydantic for Test Validation

Using Pydantic models to validate API responses, generate test data, and enforce contracts. Replaces fragile dict-key assertions with typed, self-documenting validation.

## Response Validation

```python
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime
    role: str = "user"

    @field_validator("role")
    @classmethod
    def role_must_be_valid(cls, v):
        allowed = {"user", "admin", "moderator"}
        if v not in allowed:
            raise ValueError(f"role must be one of {allowed}")
        return v

def test_get_user(api_client):
    resp = api_client.get("/api/users/1")
    assert resp.status_code == 200
    user = UserResponse.model_validate(resp.json())  # validates all fields
    assert user.id == 1
```

If the response has wrong types, missing fields, or invalid email format - Pydantic raises `ValidationError` with detailed messages.

## List Response Validation

```python
from pydantic import TypeAdapter

UserList = TypeAdapter(list[UserResponse])

def test_list_users(api_client):
    resp = api_client.get("/api/users")
    users = UserList.validate_python(resp.json())
    assert len(users) > 0
    assert all(isinstance(u, UserResponse) for u in users)
```

## Nested Models

```python
class Address(BaseModel):
    city: str
    country: str
    zip_code: Optional[str] = None

class UserWithAddress(BaseModel):
    id: int
    name: str
    address: Address
    tags: list[str] = []

def test_user_with_address(api_client):
    resp = api_client.get("/api/users/1?expand=address")
    user = UserWithAddress.model_validate(resp.json())
    assert user.address.country != ""
```

## Test Data Generation

```python
class CreateUserRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

    @classmethod
    def random(cls, **overrides):
        from faker import Faker
        fake = Faker()
        defaults = {
            "name": fake.name(),
            "email": fake.email(),
            "password": fake.password(length=12),
        }
        defaults.update(overrides)
        return cls(**defaults)

def test_create_user(api_client):
    payload = CreateUserRequest.random(name="TestUser")
    resp = api_client.post("/api/users", json=payload.model_dump())
    assert resp.status_code == 201
```

## Strict vs Lax Validation

```python
class StrictUser(BaseModel):
    model_config = {"strict": True}
    id: int
    name: str

# Strict: "123" for int field -> ValidationError
# Lax (default): "123" for int field -> coerced to 123

def test_strict_response_types(api_client):
    resp = api_client.get("/api/users/1")
    StrictUser.model_validate(resp.json())  # no type coercion
```

## Partial Validation (Ignore Extra Fields)

```python
class MinimalUser(BaseModel):
    model_config = {"extra": "ignore"}
    id: int
    name: str

# Response may have 20 fields - only validates id and name
```

## Comparing Pydantic vs Raw Dict Assertions

```python
# Without Pydantic (fragile)
data = resp.json()
assert "id" in data
assert isinstance(data["id"], int)
assert "email" in data
assert "@" in data["email"]
# ... 10 more assertions

# With Pydantic (one line)
UserResponse.model_validate(resp.json())
```

## Gotchas

- **Issue:** Pydantic v1 uses `class Config` and `.parse_obj()`, v2 uses `model_config` dict and `.model_validate()`. Mixing them causes silent failures. **Fix:** Pin Pydantic version in requirements. Use v2 API: `model_validate`, `model_dump`, `model_config`.

- **Issue:** Default Pydantic coerces types (string "123" becomes int 123) - hiding real API bugs where numbers come as strings. **Fix:** Use `model_config = {"strict": True}` for response validation to catch type mismatches.

- **Issue:** Optional fields with `None` default pass validation even when API should always return a value. **Fix:** Only use `Optional` when the API contract explicitly allows null. Use required fields by default.

## See Also

- [[api-testing-requests]]
- [[test-data-management]]
- [[fastapi-test-services]]
