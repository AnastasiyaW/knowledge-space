---
title: "FastAPI-Grundlagen"
category: frameworks
tags: [python, fastapi, rest-api, routing, dependency-injection, pydantic]
level: 3
source_sha256: b3dfe8677880040570afaa96413689fcb0a4d6af24b8fa3ba67197573e49345d
translation: machine
translated_at: '2026-10-24'
---
# FastAPI-Grundlagen {#fastapi-fundamentals}

FastAPI ist ein modernes, leistungsstarkes Python-Web-Framework zum Erstellen von APIs, aufbauend auf Starlette (ASGI) und Pydantic (Validierung). Es bietet automatisch generierte OpenAPI-Dokumentation, nativen async-Support und eine typ-Hinweis-gesteuerte Validierung von Requests.

## Wichtige Fakten {#key-facts}

- Generiert automatisch Swagger UI unter `/docs` und ReDoc unter `/redoc`
- Basiert auf Starlette (Web-Schicht) + Pydantic (Datenvalidierung)
- Vergleichbare Performance zu Go und Node.js (async-first)
- `Depends()` bietet Dependency Injection mit Verkettung
- APIRouter organisiert Endpunkte in Gruppen mit Prefix/Tags
- Path-Parameter werden nach Typ validiert; Query-Parameter ergeben sich aus den Standardwerten der Funktion

## Muster {#patterns}

### Minimale App {#minimal-app}
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

```bash
# Development
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### HTTP-Methoden {#http-methods}
```python
@app.get("/hotels")             # Read collection
@app.get("/hotels/{hotel_id}")  # Read single
@app.post("/hotels")            # Create
@app.put("/hotels/{hotel_id}")  # Full update
@app.patch("/hotels/{hotel_id}") # Partial update
@app.delete("/hotels/{hotel_id}") # Delete
```

### Path- und Query-Parameter {#path-and-query-parameters}
```python
@app.get("/hotels/{hotel_id}")
async def get_hotel(hotel_id: int):  # auto-validated as int
    return {"hotel_id": hotel_id}

@app.get("/hotels")
async def get_hotels(
    location: str,                # required
    date_from: date,              # auto-parsed
    stars: int | None = None,     # optional
    has_spa: bool = False,        # default
):
    ...
# GET /hotels?location=Moscow&date_from=2024-01-01&stars=4
```

### Request-Body (Pydantic) {#request-body-pydantic}
```python
from pydantic import BaseModel, EmailStr

class UserRegister(BaseModel):
    email: EmailStr
    password: str

@app.post("/auth/register")
async def register(user_data: UserRegister):
    # user_data is auto-validated; invalid -> 422 response
    ...
```

### Response-Modelle {#response-models}
```python
class UserResponse(BaseModel):
    id: int
    email: str
    # password NOT included

    model_config = {"from_attributes": True}

@app.get("/users/me", response_model=UserResponse)
async def get_me(user: User = Depends(get_current_user)):
    return user  # password auto-excluded
```

### Router {#routers}
```python
# routers/hotels.py
from fastapi import APIRouter

router = APIRouter(prefix="/hotels", tags=["Hotels"])

@router.get("")
async def get_hotels():
    return await HotelDAO.find_all()

# main.py
from routers.hotels import router as hotel_router
app.include_router(hotel_router)
```

### Abhängigkeiten (Depends) {#dependencies-depends}
```python
from fastapi import Depends

async def get_db_session():
    async with async_session() as session:
        yield session  # cleanup after request

async def get_current_user(token: str = Depends(get_token)):
    user = await verify_token(token)
    if not user:
        raise HTTPException(status_code=401)
    return user

@app.get("/bookings")
async def get_bookings(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    ...
```

### Query-Parameter als Schema {#query-parameters-as-schema}
```python
class HotelFilter(BaseModel):
    location: str
    date_from: date
    stars: int | None = None

@app.get("/hotels")
async def get_hotels(filters: HotelFilter = Depends()):
    return await HotelDAO.find_all(**filters.model_dump(exclude_none=True))
```

### Fehlerbehandlung {#error-handling}
```python
from fastapi import HTTPException

class UserAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=409, detail="User already exists")

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(status_code=404, content={"detail": "Not found"})
```

### Umgebungskonfiguration {#environment-configuration}
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    SECRET_KEY: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = {"env_file": ".env"}

settings = Settings()
```

## Projektstruktur {#project-structure}

```python
app/
  main.py           # FastAPI app, include routers
  config.py         # Settings from .env
  database.py       # Engine, session factory
  models/           # SQLAlchemy models
  schemas/          # Pydantic schemas
  dao/              # Data Access Objects
  routers/          # API endpoints
  exceptions.py     # Custom HTTP exceptions
  dependencies.py   # Shared dependencies
  migrations/       # Alembic
```

## Stolperfallen {#gotchas}

- Synchroner blockierender Code in `async def`-Endpunkten blockiert den Event Loop - stattdessen `def` verwenden (FastAPI führt es im Thread-Pool aus)
- `Depends()` ohne Argument sieht aus wie ein Funktionsaufruf, ist aber ein Dependency-Marker
- Fehlendes `response_model` kann interne/sensible Felder an den Client weitergeben
- Die Reihenfolge der Router-Einbindung ist relevant bei überlappenden Pfaden

## Siehe auch {#see-also}

- [[fastapi-pydantic-validation]] - View-Modelle, Feldvalidierung
- [[fastapi-database-layer]] - SQLAlchemy, Alembic, DAO-Muster
- [[fastapi-auth-and-security]] - JWT, bcrypt-Authentifizierung
- [[fastapi-deployment]] - Docker, Nginx, Produktionsaufbau
- [[web-frameworks-comparison]] - Django vs Flask vs FastAPI
