---
title: "FastAPI Pydantic und Validierung"
category: frameworks
tags: [python, fastapi, pydantic, validation, schemas, view-models]
level: 3
source_sha256: 176f797df20e5a80ab79a3ab40fec572f3bcbd7c73f8cf63bbc1efbab4a669b2
translation: machine
translated_at: '2026-10-24'
---
# FastAPI Pydantic und Validierung {#fastapi-pydantic-and-validation}

Pydantic bietet Laufzeitvalidierung von Daten auf Basis von Python-Type-Hints. In FastAPI übernehmen separate Pydantic-Modelle (Schemas) die Eingabevalidierung, die Filterung der Ausgabe und das View-Model-Muster für HTML-Formulare.

## Wichtige Fakten {#key-facts}

- Eingabemodelle (Request) und Ausgabemodelle (Response) sollten getrennt sein
- `model_config = {"from_attributes": True}` ermöglicht die Konvertierung von SQLAlchemy → Pydantic
- `Field()` stellt Validierungsbeschränkungen bereit (min/max, Regex usw.)
- `@field_validator` für eigene Validierungslogik
- `model_dump()` wandelt in ein dict um; `model_dump(exclude_none=True)` überspringt None-Werte
- Ungültige Anfragedaten führen automatisch zu einer 422 Unprocessable Entity mit detaillierten Fehlern

## Muster {#patterns}

### View-Model-Muster (separate Schemas) {#view-model-pattern-separate-schemas}
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

### Feldvalidierung {#field-validation}
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

### Verwendung in Endpoints {#using-in-endpoints}
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

### Konvertierung von ORM zu Pydantic {#orm-to-pydantic-conversion}
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

### Model-Konfiguration {#model-config}
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

### ViewModel-Muster für HTML-Formulare {#viewmodel-pattern-for-html-forms}
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

## Fallstricke {#gotchas}

- SQLAlchemy-ORM-Objekte benötigen `from_attributes=True` für die Konvertierung nach Pydantic
- `model_dump()` ersetzt die veraltete Methode `dict()` in Pydantic v2
- Veränderliche Standardwerte in Pydantic: `Field(default_factory=list)` verwenden, nicht `Field(default=[])`
- `exclude_none=True` in `model_dump()` ist für optionale Query-Parameter unverzichtbar

## Siehe auch {#see-also}

- [[fastapi-fundamentals]] - Routen, Parameter, Abhängigkeiten
- [[fastapi-database-layer]] - SQLAlchemy-Modelle, DAO-Muster
- [[type-hints]] - Python-Typannotationen
