---
title: "Pydantic für Testvalidierung"
category: patterns
tags: [pydantic, validation, response-models, schema, type-checking, api-testing, basemodel]
level: 3
source_sha256: 0edbd8b9e5c42b1d968969f8d320426033de016560edf47ddbf48f90f066d339
translation: machine
translated_at: '2026-10-24'
---
# Pydantic für Testvalidierung {#pydantic-for-test-validation}

Pydantic-Modelle werden verwendet, um API-Antworten zu validieren, Testdaten zu erzeugen und Verträge durchzusetzen. Sie ersetzen fragile Assertions auf Dict-Schlüssel durch typisierte, selbstdokumentierende Validierung.

## Validierung von Antworten {#response-validation}

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

Wenn die Antwort falsche Typen, fehlende Felder oder ein ungültiges E-Mail-Format enthält, wirft Pydantic eine `ValidationError` mit detaillierten Meldungen.

## Validierung von Listenantworten {#list-response-validation}

```python
from pydantic import TypeAdapter

UserList = TypeAdapter(list[UserResponse])

def test_list_users(api_client):
    resp = api_client.get("/api/users")
    users = UserList.validate_python(resp.json())
    assert len(users) > 0
    assert all(isinstance(u, UserResponse) for u in users)
```

## Verschachtelte Modelle {#nested-models}

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

## Erzeugung von Testdaten {#test-data-generation}

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

## Strikte vs. nachsichtige Validierung {#strict-vs-lax-validation}

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

## Teilvalidierung (zusätzliche Felder ignorieren) {#partial-validation-ignore-extra-fields}

```python
class MinimalUser(BaseModel):
    model_config = {"extra": "ignore"}
    id: int
    name: str

# Response may have 20 fields - only validates id and name
```

## Vergleich: Pydantic vs. Assertions auf Roh-Dicts {#comparing-pydantic-vs-raw-dict-assertions}

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

## Stolpersteine {#gotchas}

- **Problem:** Pydantic v1 verwendet `class Config` und `.parse_obj()`, v2 verwendet das `model_config`-Dict und `.model_validate()`. Die Vermischung beider führt zu stillen Fehlern. **Lösung:** Die Pydantic-Version in den Requirements fixieren. Die v2-API verwenden: `model_validate`, `model_dump`, `model_config`.

- **Problem:** Standardmäßig erzwingt Pydantic Typen (der String "123" wird zu dem Integer 123), wodurch echte API-Fehler verdeckt werden, bei denen Zahlen als Strings übertragen werden. **Lösung:** Für die Validierung von Antworten `model_config = {"strict": True}` verwenden, um Typabweichungen zu erkennen.

- **Problem:** Optionale Felder mit dem Standardwert `None` bestehen die Validierung auch dann, wenn die API immer einen Wert liefern sollte. **Lösung:** `Optional` nur verwenden, wenn der API-Vertrag ausdrücklich null erlaubt. Standardmäßig Pflichtfelder verwenden.

## Siehe auch {#see-also}

- [[api-testing-requests]]
- [[test-data-management]]
- [[fastapi-test-services]]
