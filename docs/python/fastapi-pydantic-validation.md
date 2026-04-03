---
title: FastAPI Pydantic and Validation
category: frameworks
tags: [python, fastapi, pydantic, validation, schemas, view-models]
---

# FastAPI Pydantic and Validation

Pydantic provides runtime data validation using Python type hints. In FastAPI, separate Pydantic models (schemas) handle input validation, output filtering, and the view model pattern for HTML forms.

## Key Facts

- Input models (request) and output models (response) should be separate
- `model_config = {"from_attributes": True}` enables SQLAlchemy -> Pydantic conversion
- `Field()` provides validation constraints (min/max, regex, etc.)
- `@field_validator` for custom validation logic
- `model_dump()` converts to dict; `model_dump(exclude_none=True)` skips None values
- Invalid request data returns automatic 422 Unprocessable Entity with detailed errors

## Patterns

### View Model Pattern (Separate Schemas)
```python
# Input: what client sends
class HotelCreate(BaseModel):
    name: str
    location: str
    stars: int
    rooms_quantity: int

# Input: search parameters
class HotelSearch(BaseModel):
    location: str
    date_from: date
    date_to: date
    stars: int | None = None

# Output: what server returns (no sensitive fields)
class HotelResponse(BaseModel):
    id: int
    name: str
    location: str
    stars: int

    model_config = {"from_attributes": True}

# Output: with computed field
class HotelWithAvailability(HotelResponse):
    rooms_left: int
```

### Field Validation
```python
from pydantic import BaseModel, Field, field_validator

class HotelCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    stars: int = Field(ge=1, le=5)       # 1-5 inclusive
    rooms_quantity: int = Field(gt=0)

    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be blank')
        return v.strip()
```

### Using in Endpoints
```python
# Request validation
@router.post("/hotels")
async def create_hotel(hotel: HotelCreate):
    new_hotel = await HotelDAO.add(**hotel.model_dump())
    return new_hotel

# Response filtering
@router.get("/hotels/{id}", response_model=HotelResponse)
async def get_hotel(id: int):
    return await HotelDAO.find_by_id(id)  # auto-converted, sensitive fields excluded

# Query parameters from schema
@router.get("/hotels")
async def get_hotels(params: HotelSearch = Depends()):
    return await HotelDAO.find_all(**params.model_dump(exclude_none=True))
```

### ORM to Pydantic Conversion
```python
# SQLAlchemy model
class Hotel(Base):
    __tablename__ = "hotels"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    internal_notes = mapped_column(String)  # should NOT be exposed

# Pydantic schema (only safe fields)
class HotelResponse(BaseModel):
    id: int
    name: str
    model_config = {"from_attributes": True}

# Conversion
hotel_schema = HotelResponse.model_validate(hotel_orm)
```

### Model Config
```python
class HotelResponse(BaseModel):
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [{
                "id": 1,
                "name": "Grand Hotel",
                "stars": 5,
            }]
        }
    }
```

### ViewModel Pattern for HTML Forms
```python
class RegisterViewModel:
    """Forgiving validation for HTML forms (unlike strict Pydantic)."""
    # Knows required fields, types, validation rules
    # Can re-render form with previously entered data + errors

    def __init__(self, request):
        self.request = request
        self.errors = []

    async def load(self):
        form = await self.request.form()
        self.email = form.get('email', '')
        self.password = form.get('password', '')

    @property
    def is_valid(self):
        if not self.email:
            self.errors.append("Email required")
        return len(self.errors) == 0
```

## Gotchas

- SQLAlchemy ORM objects need `from_attributes=True` for Pydantic conversion
- `model_dump()` replaces deprecated `dict()` method in Pydantic v2
- Mutable default in Pydantic: use `Field(default_factory=list)` not `Field(default=[])`
- `exclude_none=True` in `model_dump()` is essential for optional query parameters

## See Also

- [[fastapi-fundamentals]] - routes, params, dependencies
- [[fastapi-database-layer]] - SQLAlchemy models, DAO pattern
- [[type-hints]] - Python type annotations
