---
title: "Services de test FastAPI"
category: tools
tags: [fastapi, microservices, testclient, starlette, mock-server, test-app, dependency-override]
level: 3
source_sha256: 46b2f67f5d41fdb459ce676252e30656149de2242b97d30b636c1ef8932f8328
translation: machine
translated_at: '2026-10-24'
---
# Services de test FastAPI {#fastapi-test-services}

Construire des microservices FastAPI testables et écrire des tests pour ceux-ci. TestClient pour les tests synchrones, surcharges de l'injection de dépendances, et exécution de vrais serveurs de test.

## TestClient (en processus) {#testclient-in-process}

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

TestClient exécute l'application en processus (sans réseau). Rapide, synchrone, idéal pour les tests unitaires.

## Surcharge de l'injection de dépendances {#dependency-injection-override}

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

Cela remplace la vraie base de données par la base de test sans modifier le code de l'application.

## TestClient asynchrone {#async-testclient}

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

Nécessaire pour tester les endpoints asynchrones qui utilisent `await`.

## Construire un microservice de test {#building-a-test-microservice}

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

## Tests avec un vrai serveur (uvicorn) {#testing-with-real-server-uvicorn}

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

## Tests de validation des requêtes {#request-validation-testing}

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

## Tests des middlewares et des événements {#middleware-and-event-testing}

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

## Pièges courants {#gotchas}

- **Problème :** `TestClient` n'exécute pas les événements `lifespan` (démarrage/arrêt) par défaut. **Solution :** Utiliser le gestionnaire de contexte `with TestClient(app) as client:` - cela déclenche les événements lifespan.

- **Problème :** `dependency_overrides` est un état global - la surcharge d'un test affecte un autre test. **Solution :** Toujours vider les surcharges dans le teardown de la fixture : `app.dependency_overrides.clear()`. Utiliser des fixtures à portée de fonction.

- **Problème :** Les endpoints asynchrones testés avec un `TestClient` synchrone fonctionnent mais perdent les avantages de l'asynchrone. **Solution :** Utiliser `httpx.AsyncClient` avec `pytest-asyncio` pour des tests réellement asynchrones. Particulièrement important si les endpoints utilisent `await` en interne.

## Voir aussi {#see-also}

- [[api-testing-requests]]
- [[pydantic-test-models]]
- [[docker-test-environments]]
