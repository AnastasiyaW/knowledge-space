---
title: Dataclasses and Pydantic
category: concepts
tags: [python, dataclasses, pydantic, basemodel, validation, serialization, namedtuple]
---

# Dataclasses and Pydantic

**Dataclasses** (`dataclasses.dataclass`) auto-generate `__init__`, `__repr__`, `__eq__` and more from annotated class attributes. **Pydantic** (`BaseModel`) adds runtime validation, serialization, and settings management. Both reduce boilerplate for data-holding classes but serve different purposes: dataclasses are a stdlib tool for structured data, Pydantic is a validation library.

## Key Facts

- `@dataclass` generates `__init__`, `__repr__`, `__eq__` by default; opt-in for `__hash__`, `__order__`, `frozen`
- `field(default_factory=list)` avoids the mutable default argument trap
- `frozen=True` makes instances immutable (sets `__hash__` automatically)
- `@dataclass(slots=True)` (Python 3.10+) generates `__slots__` for memory efficiency
- `@dataclass(kw_only=True)` (Python 3.10+) forces keyword-only arguments
- Pydantic v2 uses Rust-based core (`pydantic-core`) for 5-50x speed improvement over v1
- `BaseModel` validates on construction; `model_validate()` from dict, `model_dump()` to dict
- Pydantic `Field()` supports `alias`, `min_length`, `ge`, `le`, `pattern` constraints
- `NamedTuple` and `TypedDict` are simpler alternatives for typed tuples/dicts
- See [[type-hints-and-generics]] for annotation syntax, [[fastapi-fundamentals]] for Pydantic in request/response models

## Patterns

### Dataclass Basics

```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class User:
    name: str
    email: str
    age: int
    tags: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def is_adult(self) -> bool:
        return self.age >= 18

u = User("Alice", "alice@example.com", 30)
print(u)  # User(name='Alice', email='alice@example.com', age=30, tags=[], created_at=...)
```

### Frozen Dataclass (Immutable)

```python
@dataclass(frozen=True)
class Point:
    x: float
    y: float

p = Point(1.0, 2.0)
# p.x = 3.0  # FrozenInstanceError
{p}  # works -- frozen dataclasses are hashable
```

### Dataclass with `__post_init__`

```python
@dataclass
class Rectangle:
    width: float
    height: float
    area: float = field(init=False)

    def __post_init__(self):
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Dimensions must be positive")
        self.area = self.width * self.height

r = Rectangle(5.0, 3.0)
print(r.area)  # 15.0
```

### Pydantic v2 BaseModel

```python
from pydantic import BaseModel, Field, field_validator, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(ge=0, le=150)
    tags: list[str] = []

    @field_validator("name")
    @classmethod
    def name_must_be_capitalized(cls, v: str) -> str:
        if not v[0].isupper():
            raise ValueError("Name must start with a capital letter")
        return v

# Validates on construction
user = UserCreate(name="Alice", email="alice@example.com", age=30)

# Serialization
user.model_dump()         # {'name': 'Alice', 'email': 'alice@example.com', 'age': 30, 'tags': []}
user.model_dump_json()    # JSON string

# Deserialization with validation
data = {"name": "Bob", "email": "bob@test.com", "age": 25}
user2 = UserCreate.model_validate(data)
```

### Pydantic Settings (Environment Variables)

```python
from pydantic_settings import BaseSettings

class AppSettings(BaseSettings):
    database_url: str
    redis_url: str = "redis://localhost:6379"
    debug: bool = False
    allowed_origins: list[str] = ["http://localhost:3000"]

    model_config = {"env_file": ".env", "env_prefix": "APP_"}

# Reads from environment: APP_DATABASE_URL, APP_REDIS_URL, etc.
settings = AppSettings()
```

### NamedTuple and TypedDict

```python
from typing import NamedTuple, TypedDict

# NamedTuple -- immutable, hashable, positional access
class Coordinate(NamedTuple):
    lat: float
    lon: float
    alt: float = 0.0

c = Coordinate(55.75, 37.62)
lat, lon, alt = c  # unpacking works

# TypedDict -- typed dict, runtime it's a regular dict
class MovieData(TypedDict):
    title: str
    year: int
    rating: float

movie: MovieData = {"title": "Inception", "year": 2010, "rating": 8.8}
```

## Gotchas

- **Mutable default values**: `@dataclass` with `tags: list = []` raises `ValueError`. Always use `field(default_factory=list)`. Pydantic handles this automatically
- **Dataclass inheritance**: child class fields come after parent fields in `__init__`. A parent with defaults followed by a child with non-default fields causes `TypeError`. Fix: use `kw_only=True` on parent defaults or restructure
- **Pydantic v1 vs v2 API**: `dict()` -> `model_dump()`, `parse_obj()` -> `model_validate()`, `schema()` -> `model_json_schema()`. V1 validators use `@validator`, V2 uses `@field_validator`
- **`dataclass` does not validate types**: `User(name=42, age="hello")` succeeds -- dataclass trusts annotations but does not enforce them at runtime. Use Pydantic if you need validation
- **`frozen=True` with `__post_init__`**: cannot use `self.field = value` in `__post_init__` on a frozen dataclass. Use `object.__setattr__(self, 'field', value)` instead

## See Also

- [dataclasses -- Python docs](https://docs.python.org/3/library/dataclasses.html)
- [Pydantic v2 docs](https://docs.pydantic.dev/latest/)
- [[type-hints-and-generics]] - annotation patterns used by dataclasses and Pydantic
- [[fastapi-fundamentals]] - Pydantic models as request/response schemas
