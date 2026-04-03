---
title: FastAPI Fundamentals
category: frameworks
tags: [python, fastapi, rest-api, routing, dependency-injection, pydantic]
---

# FastAPI Fundamentals

FastAPI is a modern, high-performance Python web framework for building APIs, built on Starlette (ASGI) and Pydantic (validation). It provides auto-generated OpenAPI docs, native async support, and type-hint-driven request validation.

## Key Facts

- Auto-generates Swagger UI at `/docs` and ReDoc at `/redoc`
- Built on Starlette (web layer) + Pydantic (data validation)
- Comparable performance to Go and Node.js (async-first)
- `Depends()` provides dependency injection with chaining
- APIRouter organizes endpoints into groups with prefix/tags
- Path parameters are validated by type; query parameters from function defaults

## Patterns

### Minimal App
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

### HTTP Methods
```python
@app.get("/hotels")             # Read collection
@app.get("/hotels/{hotel_id}")  # Read single
@app.post("/hotels")            # Create
@app.put("/hotels/{hotel_id}")  # Full update
@app.patch("/hotels/{hotel_id}") # Partial update
@app.delete("/hotels/{hotel_id}") # Delete
```

### Path and Query Parameters
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

### Request Body (Pydantic)
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

### Response Models
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

### Routers
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

### Dependencies (Depends)
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

### Query Parameters as Schema
```python
class HotelFilter(BaseModel):
    location: str
    date_from: date
    stars: int | None = None

@app.get("/hotels")
async def get_hotels(filters: HotelFilter = Depends()):
    return await HotelDAO.find_all(**filters.model_dump(exclude_none=True))
```

### Error Handling
```python
from fastapi import HTTPException

class UserAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=409, detail="User already exists")

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(status_code=404, content={"detail": "Not found"})
```

### Environment Configuration
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

## Project Structure

```
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

## Gotchas

- Sync blocking code in `async def` endpoints blocks the event loop - use `def` instead (FastAPI runs it in thread pool)
- `Depends()` without argument looks like a function call but is a dependency marker
- Missing `response_model` may leak internal/sensitive fields to the client
- Order of router inclusion matters for overlapping paths

## See Also

- [[fastapi-pydantic-validation]] - view models, field validation
- [[fastapi-database-layer]] - SQLAlchemy, Alembic, DAO pattern
- [[fastapi-auth-and-security]] - JWT, bcrypt authentication
- [[fastapi-deployment]] - Docker, Nginx, production setup
- [[web-frameworks-comparison]] - Django vs Flask vs FastAPI
