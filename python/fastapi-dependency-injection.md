---
title: FastAPI Dependency Injection
category: concepts
tags: [python, fastapi, dependency-injection, depends, annotated, services, repository-pattern]
---

# FastAPI Dependency Injection

FastAPI's `Depends()` system provides a declarative way to inject shared logic into endpoints: database sessions, authentication, pagination, services. Dependencies are callables (functions or classes) that are resolved recursively, cached per-request, and support both sync and async.

## Key Facts

- `Depends(callable)` declares a dependency; FastAPI calls it and injects the result
- Dependencies can depend on other dependencies (recursive resolution)
- Dependencies are cached per-request by default (same instance reused within one request)
- `Annotated[Type, Depends(dep)]` (Python 3.9+) is the recommended syntax
- Generator dependencies with `yield` support setup/teardown (e.g., DB session per request)
- Class-based dependencies use `__init__` parameters as query/path params
- Override dependencies in tests with `app.dependency_overrides[original] = mock`
- See [[fastapi-fundamentals]] for routing basics, [[sqlalchemy-and-alembic]] for DB session patterns

## Patterns

### Basic Dependency

```python
from typing import Annotated
from fastapi import Depends, FastAPI, Query

app = FastAPI()

async def pagination(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
) -> dict:
    return {"skip": skip, "limit": limit}

PaginationDep = Annotated[dict, Depends(pagination)]

@app.get("/items/")
async def list_items(pagination: PaginationDep):
    return await ItemService.list(
        skip=pagination["skip"],
        limit=pagination["limit"],
    )
```

### Database Session Dependency (yield)

```python
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/db")
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

DBSession = Annotated[AsyncSession, Depends(get_db)]

@app.get("/users/{user_id}")
async def get_user(user_id: int, db: DBSession):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(404, "User not found")
    return user
```

### Service Layer with Dependencies

```python
from typing import Annotated
from fastapi import Depends

class UserRepository:
    def __init__(self, db: DBSession):
        self.db = db

    async def get(self, user_id: int) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def create(self, data: UserCreate) -> User:
        user = User(**data.model_dump())
        self.db.add(user)
        await self.db.flush()
        return user

class UserService:
    def __init__(self, repo: Annotated[UserRepository, Depends()]):
        self.repo = repo

    async def register(self, data: UserCreate) -> User:
        existing = await self.repo.get_by_email(data.email)
        if existing:
            raise HTTPException(409, "Email already registered")
        return await self.repo.create(data)

@app.post("/users/", status_code=201)
async def create_user(
    data: UserCreate,
    service: Annotated[UserService, Depends()],
):
    return await service.register(data)
```

### Class-Based Dependency (Query Params)

```python
class ItemFilter:
    def __init__(
        self,
        category: str | None = None,
        min_price: float = Query(default=0, ge=0),
        max_price: float = Query(default=10000, le=100000),
        in_stock: bool = True,
    ):
        self.category = category
        self.min_price = min_price
        self.max_price = max_price
        self.in_stock = in_stock

@app.get("/items/")
async def list_items(
    filters: Annotated[ItemFilter, Depends()],
    pagination: PaginationDep,
):
    return await ItemService.search(filters, pagination)
```

### Testing with Dependency Overrides

```python
import pytest
from fastapi.testclient import TestClient
from myapp.main import app
from myapp.deps import get_db

@pytest.fixture
def client():
    async def override_get_db():
        async with test_session() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

def test_create_user(client):
    response = client.post("/users/", json={"name": "Alice", "email": "alice@test.com"})
    assert response.status_code == 201
```

### Global Dependencies

```python
from fastapi import FastAPI, Depends

async def verify_api_key(x_api_key: str = Header()):
    if x_api_key != "secret":
        raise HTTPException(403, "Invalid API key")

# Applied to ALL routes
app = FastAPI(dependencies=[Depends(verify_api_key)])

# Or per-router
router = APIRouter(
    prefix="/admin",
    dependencies=[Depends(verify_admin_role)],
)
```

## Gotchas

- **`Depends()` without argument**: `Depends()` (no arg) uses the type annotation itself as the callable. Works for classes but not for functions -- functions must be passed explicitly
- **Generator dependency cleanup**: if an exception occurs in the endpoint, the `finally` block of a `yield` dependency still runs (cleanup is guaranteed). But `except` in the dependency will catch endpoint exceptions too
- **Dependency caching**: the same `Depends(get_db)` used twice in one request returns the same session. Use `Depends(get_db, use_cache=False)` for separate instances
- **Circular dependencies**: `A depends on B, B depends on A` causes `RecursionError`. Restructure by introducing a third dependency or merging them
- **`dependency_overrides` is global**: `app.dependency_overrides` is a simple dict -- concurrent tests modifying it can interfere. Clear overrides after each test

## See Also

- [FastAPI Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [Annotated Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/#use-annotated)
- [[fastapi-fundamentals]] - routing and middleware
- [[sqlalchemy-and-alembic]] - session management patterns
