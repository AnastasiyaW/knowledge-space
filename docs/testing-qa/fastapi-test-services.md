---
title: FastAPI Test Services
category: tools
tags: [fastapi, microservices, testclient, starlette, mock-server, test-app, dependency-override]
---

# FastAPI Test Services

Building testable FastAPI microservices and writing tests against them. TestClient for synchronous tests, dependency injection overrides, and running real test servers.

## TestClient (In-Process)

```python
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    return {"id": user_id, "name": "Alice"}

@pytest.fixture
def client():
    return TestClient(app)

def test_get_user(client):
    resp = client.get("/api/users/1")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Alice"
```

TestClient runs the app in-process (no network). Fast, synchronous, ideal for unit tests.

## Dependency Injection Override

```python
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/users")
def list_users(db=Depends(get_db)):
    return db.query(User).all()

# In tests: override the dependency
@pytest.fixture
def client():
    def override_get_db():
        db = TestSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
```

This replaces the real DB with test DB without modifying application code.

## Async TestClient

```python
import httpx
import pytest_asyncio

@pytest_asyncio.fixture
async def async_client():
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_async_endpoint(async_client):
    resp = await async_client.get("/api/users")
    assert resp.status_code == 200
```

Required for testing async endpoints that use `await`.

## Building a Test Microservice

```python
# test_service/app.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

users_db = {}

class User(BaseModel):
    name: str
    email: str

@app.post("/api/users", status_code=201)
def create_user(user: User):
    user_id = len(users_db) + 1
    users_db[user_id] = user.model_dump()
    users_db[user_id]["id"] = user_id
    return users_db[user_id]

@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]

@app.get("/api/users")
def list_users():
    return list(users_db.values())
```

## Testing with Real Server (uvicorn)

```python
import subprocess
import time

@pytest.fixture(scope="session")
def live_server():
    proc = subprocess.Popen(
        ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"],
        stdout=subprocess.PIPE,
    )
    wait_for_port(8000, timeout=10)
    yield "http://localhost:8000"
    proc.terminate()
    proc.wait()

def test_live_endpoint(live_server):
    resp = requests.get(f"{live_server}/api/users")
    assert resp.status_code == 200
```

## Request Validation Testing

```python
@pytest.mark.parametrize("payload,expected_status", [
    ({"name": "Alice", "email": "alice@test.com"}, 201),
    ({"name": "", "email": "alice@test.com"}, 422),       # empty name
    ({"name": "Alice"}, 422),                              # missing email
    ({"name": "Alice", "email": "not-an-email"}, 422),    # invalid email
    ({}, 422),                                              # empty body
])
def test_create_user_validation(client, payload, expected_status):
    resp = client.post("/api/users", json=payload)
    assert resp.status_code == expected_status
```

## Middleware and Event Testing

```python
@app.middleware("http")
async def add_request_id(request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid4()))
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response

def test_request_id_header(client):
    resp = client.get("/api/users", headers={"X-Request-ID": "test-123"})
    assert resp.headers["X-Request-ID"] == "test-123"

def test_request_id_generated(client):
    resp = client.get("/api/users")
    assert "X-Request-ID" in resp.headers
```

## Gotchas

- **Issue:** `TestClient` does not run `lifespan` events (startup/shutdown) by default. **Fix:** Use `with TestClient(app) as client:` context manager - this triggers lifespan events.

- **Issue:** `dependency_overrides` is global state - one test's override affects another. **Fix:** Always clear overrides in fixture teardown: `app.dependency_overrides.clear()`. Use function-scoped fixtures.

- **Issue:** Async endpoints tested with sync `TestClient` work but lose async benefits. **Fix:** Use `httpx.AsyncClient` with `pytest-asyncio` for true async testing. Especially important if endpoints use `await` internally.

## See Also

- [[api-testing-requests]]
- [[pydantic-test-models]]
- [[docker-test-environments]]
