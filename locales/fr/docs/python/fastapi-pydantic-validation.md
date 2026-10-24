---
title: "FastAPI Pydantic et validation"
category: frameworks
tags: [python, fastapi, pydantic, validation, schemas, view-models]
level: 3
source_sha256: 176f797df20e5a80ab79a3ab40fec572f3bcbd7c73f8cf63bbc1efbab4a669b2
translation: machine
translated_at: '2026-10-24'
---
# FastAPI Pydantic et validation {#fastapi-pydantic-and-validation}

Pydantic assure la validation des données à l'exécution à partir des annotations de type Python. Dans FastAPI, des modèles Pydantic distincts (schémas) gèrent la validation des entrées, le filtrage des sorties et le patron view model pour les formulaires HTML.

## Points clés {#key-facts}

- Les modèles d'entrée (requête) et de sortie (réponse) doivent être séparés
- `model_config = {"from_attributes": True}` active la conversion SQLAlchemy -> Pydantic
- `Field()` fournit les contraintes de validation (min/max, regex, etc.)
- `@field_validator` pour la logique de validation personnalisée
- `model_dump()` convertit en dict ; `model_dump(exclude_none=True)` ignore les valeurs `None`
- Les données de requête invalides renvoient automatiquement une erreur 422 Unprocessable Entity avec des détails

## Patrons {#patterns}

### Patron View Model (schémas séparés) {#view-model-pattern-separate-schemas}
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

### Validation des champs {#field-validation}
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

### Utilisation dans les endpoints {#using-in-endpoints}
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

### Conversion ORM vers Pydantic {#orm-to-pydantic-conversion}
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

### Configuration du modèle {#model-config}
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

### Patron ViewModel pour les formulaires HTML {#viewmodel-pattern-for-html-forms}
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

## Pièges {#gotchas}

- Les objets ORM SQLAlchemy ont besoin de `from_attributes=True` pour la conversion Pydantic
- `model_dump()` remplace la méthode `dict()`, dépréciée dans Pydantic v2
- Valeur par défaut mutable dans Pydantic : utiliser `Field(default_factory=list)` et non `Field(default=[])`
- `exclude_none=True` dans `model_dump()` est indispensable pour les paramètres de requête optionnels

## Voir aussi {#see-also}

- [[fastapi-fundamentals]] - routes, paramètres, dépendances
- [[fastapi-database-layer]] - modèles SQLAlchemy, patron DAO
- [[type-hints]] - annotations de types Python
