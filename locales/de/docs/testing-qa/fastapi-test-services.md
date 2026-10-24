---
title: "FastAPI-Testdienste"
category: tools
tags: [fastapi, microservices, testclient, starlette, mock-server, test-app, dependency-override]
level: 3
source_sha256: 46b2f67f5d41fdb459ce676252e30656149de2242b97d30b636c1ef8932f8328
translation: machine
translated_at: '2026-10-24'
---
# FastAPI-Testdienste {#fastapi-test-services}

Testbare FastAPI-Microservices entwickeln und Tests gegen sie schreiben. TestClient für synchrone Tests, Überschreibung von Dependency Injection und das Starten echter Testserver.

## TestClient (In-Process) {#testclient-in-process}

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

TestClient führt die App im selben Prozess aus (ohne Netzwerk). Schnell, synchron und ideal für Unit-Tests.

## Überschreiben der Dependency Injection {#dependency-injection-override}

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

Damit wird die echte Datenbank durch eine Test-Datenbank ersetzt, ohne den Anwendungscode zu verändern.

## Async TestClient {#async-testclient}

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

Erforderlich für Tests von async-Endpunkten, die `await` verwenden.

## Aufbau eines Test-Microservices {#building-a-test-microservice}

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

## Testen mit einem echten Server (uvicorn) {#testing-with-real-server-uvicorn}

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

## Testen der Request-Validierung {#request-validation-testing}

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

## Tests für Middleware und Events {#middleware-and-event-testing}

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

## Stolpersteine {#gotchas}

- **Problem:** `TestClient` führt standardmäßig keine `lifespan`-Events (Startup/Shutdown) aus. **Lösung:** Den Kontextmanager `with TestClient(app) as client:` verwenden; dadurch werden die Lifespan-Events ausgelöst.

- **Problem:** `dependency_overrides` ist globaler Zustand, sodass das Überschreiben in einem Test andere Tests beeinflusst. **Lösung:** Overrides immer im Teardown der Fixture zurücksetzen: `app.dependency_overrides.clear()`. Fixtures mit Function-Scope verwenden.

- **Problem:** Async-Endpunkte, die mit dem synchronen `TestClient` getestet werden, funktionieren, verlieren aber die Vorteile von async. **Lösung:** Für echtes asynchrones Testen `httpx.AsyncClient` mit `pytest-asyncio` verwenden. Besonders wichtig, wenn die Endpunkte intern `await` nutzen.

## Siehe auch {#see-also}

- [[api-testing-requests]]
- [[pydantic-test-models]]
- [[docker-test-environments]]
