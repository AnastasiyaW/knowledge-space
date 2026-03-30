---
title: FastAPI Fundamentals
category: concepts
tags: [python, fastapi, api, rest, pydantic, routing, middleware, openapi]
---

# FastAPI Fundamentals

FastAPI is a modern, high-performance Python web framework built on Starlette (ASGI) and Pydantic. It provides automatic request validation, serialization, OpenAPI documentation, and native async support. FastAPI is the de facto standard for building Python REST APIs.

## Key Facts

- Built on Starlette (ASGI server framework) and Pydantic (data validation)
- Auto-generates OpenAPI (Swagger) docs at `/docs` and ReDoc at `/redoc`
- Path parameters, query parameters, and request bodies are validated via type hints and Pydantic models
- `async def` endpoints run on the event loop; `def` endpoints run in a thread pool (both work)
- `APIRouter` organizes endpoints into modules with shared prefixes and tags
- `HTTPException` returns error responses with status code and detail
- Middleware supports request/response processing (CORS, logging, auth)
- Lifespan events (`@asynccontextmanager` on `lifespan`) replace deprecated `on_event("startup")`
- See [[fastapi-dependency-injection]] for `Depends`, [[fastapi-authentication]] for security, [[dataclasses-and-pydantic]] for models

## Patterns

### Basic Application

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="My API", version="1.0.0")

class ItemCreate(BaseModel):
    name: str
    price: float
    in_stock: bool = True

class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    in_stock: bool

items_db: dict[int, dict] = {}
counter = 0

@app.post("/items/", response_model=ItemResponse, status_code=201)
async def create_item(item: ItemCreate):
    global counter
    counter += 1
    item_data = {"id": counter, **item.model_dump()}
    items_db[counter] = item_data
    return item_data

@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]
```

### APIRouter for Modular Structure

```python
# app/routers/users.py
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
async def list_users():
    return await UserService.list_all()

@router.get("/{user_id}")
async def get_user(user_id: int):
    return await UserService.get(user_id)

# app/main.py
from fastapi import FastAPI
from app.routers import users, items

app = FastAPI()
app.include_router(users.router)
app.include_router(items.router, prefix="/api/v1")
```

### Query Parameters and Path Validation

```python
from fastapi import FastAPI, Query, Path
from enum import Enum

class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"

@app.get("/items/")
async def list_items(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    search: str | None = Query(default=None, min_length=1),
    sort: SortOrder = SortOrder.asc,
):
    ...

@app.get("/items/{item_id}")
async def get_item(
    item_id: int = Path(gt=0, description="The item ID"),
):
    ...
```

### Lifespan Events (Startup/Shutdown)

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app.state.db = await create_db_pool()
    app.state.redis = await create_redis_pool()
    yield
    # Shutdown
    await app.state.db.close()
    await app.state.redis.close()

app = FastAPI(lifespan=lifespan)
```

### Middleware

```python
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom timing middleware
@app.middleware("http")
async def add_timing_header(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start
    response.headers["X-Process-Time"] = f"{duration:.4f}"
    return response
```

### Response Models and Status Codes

```python
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

@app.post(
    "/items/",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {"description": "Item already exists"},
        422: {"description": "Validation error"},
    },
)
async def create_item(item: ItemCreate):
    ...

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    ...
    return None  # 204 returns no body
```

## Gotchas

- **`def` vs `async def` endpoints**: `def` endpoints run in a thread pool (blocking is OK). `async def` endpoints run on the event loop -- blocking calls (e.g., `time.sleep`, `requests.get`) freeze the entire server. Use `await` or `run_in_executor`
- **`response_model` filters output**: fields not in the response model are excluded from the response, even if present in the returned dict. This is intentional for hiding internal fields
- **Order of route registration matters**: `/items/all` must be registered before `/items/{item_id}`, otherwise `"all"` is interpreted as an item_id
- **`HTTPException` vs `Response`**: `HTTPException` is for error responses with automatic JSON formatting. For custom responses (HTML, streaming, files), use `Response` subclasses
- **Lifespan replaces deprecated `on_event`**: `@app.on_event("startup")` still works but is deprecated since FastAPI 0.93. Use the lifespan context manager

## See Also

- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [Starlette documentation](https://www.starlette.io/)
- [[fastapi-dependency-injection]] - `Depends` for DI, database sessions, services
- [[fastapi-authentication]] - JWT, OAuth2, security utilities
