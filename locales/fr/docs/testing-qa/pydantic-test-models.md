---
title: "Pydantic pour la validation des tests"
category: patterns
tags: [pydantic, validation, response-models, schema, type-checking, api-testing, basemodel]
level: 3
source_sha256: 0edbd8b9e5c42b1d968969f8d320426033de016560edf47ddbf48f90f066d339
translation: machine
translated_at: '2026-10-24'
---
# Pydantic pour la validation des tests {#pydantic-for-test-validation}

Utiliser des modèles Pydantic pour valider les réponses d'API, générer des données de test et imposer des contrats. Remplace les assertions fragiles sur les clés de dictionnaires par une validation typée et auto-documentée.

## Validation des réponses {#response-validation}

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

Si la réponse contient des types incorrects, des champs manquants ou un format d'e-mail invalide, Pydantic lève une `ValidationError` avec des messages détaillés.

## Validation des réponses de type liste {#list-response-validation}

```python
from pydantic import TypeAdapter

UserList = TypeAdapter(list[UserResponse])

def test_list_users(api_client):
    resp = api_client.get("/api/users")
    users = UserList.validate_python(resp.json())
    assert len(users) > 0
    assert all(isinstance(u, UserResponse) for u in users)
```

## Modèles imbriqués {#nested-models}

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

## Génération de données de test {#test-data-generation}

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

## Validation stricte ou souple {#strict-vs-lax-validation}

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

## Validation partielle (ignorer les champs supplémentaires) {#partial-validation-ignore-extra-fields}

```python
class MinimalUser(BaseModel):
    model_config = {"extra": "ignore"}
    id: int
    name: str

# Response may have 20 fields - only validates id and name
```

## Comparaison entre Pydantic et les assertions sur dictionnaires bruts {#comparing-pydantic-vs-raw-dict-assertions}

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

## Pièges courants {#gotchas}

- **Problème :** Pydantic v1 utilise `class Config` et `.parse_obj()`, tandis que la v2 utilise un dictionnaire `model_config` et `.model_validate()`. Mélanger les deux provoque des échecs silencieux. **Correctif :** Fixer la version de Pydantic dans les fichiers de dépendances. Utiliser l'API v2 : `model_validate`, `model_dump`, `model_config`.

- **Problème :** Par défaut, Pydantic convertit les types (la chaîne "123" devient l'entier 123), ce qui masque de vrais bogues d'API où des nombres sont renvoyés sous forme de chaînes. **Correctif :** Utiliser `model_config = {"strict": True}` pour la validation des réponses afin de détecter les incompatibilités de types.

- **Problème :** Les champs optionnels ayant `None` pour valeur par défaut passent la validation alors que l'API devrait toujours renvoyer une valeur. **Correctif :** N'utiliser `Optional` que lorsque le contrat d'API autorise explicitement la valeur null. Par défaut, utiliser des champs obligatoires.

## Voir aussi {#see-also}

- [[api-testing-requests]]
- [[test-data-management]]
- [[fastapi-test-services]]
