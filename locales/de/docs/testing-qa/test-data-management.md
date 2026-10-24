---
title: "Testdatenverwaltung"
category: patterns
tags: [test-data, fixtures, factories, env-config, dotenv, parametrize, data-driven]
level: 3
source_sha256: d54b70948ccaf7a40f931e94de509a9d8c9ad9d653351d45d5dfa0add646aa34
translation: machine
translated_at: '2026-10-24'
---
# Testdatenverwaltung {#test-data-management}

Strategien zum Erstellen, Verwalten und Bereinigen von Testdaten über verschiedene Umgebungen hinweg. Behandelt werden Umgebungskonfigurationen, Daten-Factories, Parametrisierung und dateibasierte Testdaten.

## Umgebungskonfiguration {#environment-configuration}

```python
# config.py
from pydantic_settings import BaseSettings

class TestConfig(BaseSettings):
    base_url: str = "http://localhost:8000"
    db_url: str = "postgresql://test:test@localhost/testdb"
    api_token: str = ""

    class Config:
        env_file = ".env"
        env_prefix = "TEST_"
```

```bash
# .env.dev
TEST_BASE_URL=http://localhost:8000
TEST_API_TOKEN=dev-token-123

# .env.staging
TEST_BASE_URL=https://staging.example.com
TEST_API_TOKEN=staging-token-456
```

```python
# conftest.py
@pytest.fixture(scope="session")
def config():
    env = os.getenv("TEST_ENV", "dev")
    return TestConfig(_env_file=f".env.{env}")
```

Ausführen: `TEST_ENV=staging pytest`

## Parametrisierung für datengetriebene Tests {#parametrize-for-data-driven-tests}

```python
@pytest.mark.parametrize("username,password,expected_status", [
    ("admin", "admin123", 200),
    ("admin", "wrong", 401),
    ("", "admin123", 422),
    ("nonexistent", "pass", 401)])
def test_login(api_client, username, password, expected_status):
    resp = api_client.post("/login", json={"username": username, "password": password})
    assert resp.status_code == expected_status
```

## Externe Datendateien {#external-data-files}

```python
import json
import csv

def load_test_data(filename):
    path = Path(__file__).parent / "data" / filename
    if path.suffix == ".json":
        return json.loads(path.read_text())
    elif path.suffix == ".csv":
        with open(path) as f:
            return list(csv.DictReader(f))

@pytest.mark.parametrize("case", load_test_data("login_cases.json"))
def test_login_from_file(api_client, case):
    resp = api_client.post("/login", json=case["input"])
    assert resp.status_code == case["expected_status"]
```

## Datenbank-Fixtures mit Rollback {#database-fixtures-with-rollback}

```python
@pytest.fixture
def db_session(db_engine):
    """Each test gets a transaction that rolls back."""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()
```

Jeder Test sieht einen sauberen Datenbankzustand, ohne dass die Datenbank aufwendig neu erstellt werden muss.

## Zufällige, aber reproduzierbare Daten {#random-but-reproducible-data}

```python
from faker import Faker

fake = Faker()
Faker.seed(42)  # reproducible across runs

@pytest.fixture
def random_user():
    return {
        "name": fake.name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
    }
```

## Bereinigungsstrategien {#cleanup-strategies}

| Strategie | Anwendungsfall |
|----------|-------------|
| Transaktions-Rollback | DB-Tests, am schnellsten |
| Fixture-Teardown (yield) | Über die API erstellte Ressourcen |
| Factory + Collector | Mehrere Ressourcen pro Test |
| Datenbank-Truncation | Vollständige Integrationstests |
| Docker-Neuerstellung | Vollständige Isolation erforderlich |

```python
@pytest.fixture
def created_resources():
    """Collector pattern for cleanup."""
    resources = []
    yield resources
    for resource_type, resource_id in reversed(resources):
        delete_resource(resource_type, resource_id)

def test_order_flow(api_client, created_resources):
    user = api_client.post("/users", json={...}).json()
    created_resources.append(("user", user["id"]))

    order = api_client.post("/orders", json={"user_id": user["id"]}).json()
    created_resources.append(("order", order["id"]))
```

## Fallstricke {#gotchas}

- **Problem:** Fest codierte Testdaten (Benutzer-IDs, URLs) brechen beim Wechsel der Umgebung. **Lösung:** Alle umgebungsspezifischen Werte gehören in Konfigurationsdateien, die von Fixtures geladen werden. Niemals `/api/users/2` fest codieren – stattdessen `f"/api/users/{user_id}"` verwenden.

- **Problem:** Tests hängen von Daten ab, die andere Tests erzeugt haben (Reihenfolgeabhängigkeit). **Lösung:** Jeder Test muss seine eigenen Daten über Fixtures erzeugen. `pytest-randomly` verwenden, um versteckte Reihenfolgeabhängigkeiten aufzudecken.

- **Problem:** `.env`-Datei mit echten Zugangsdaten in Git committet. **Lösung:** `.env*` zu `.gitignore` hinzufügen. `.env.example` mit Dummy-Werten verwenden. CI bezieht Secrets aus Umgebungsvariablen.

## Siehe auch {#see-also}

- [[pytest-fixtures-advanced]]
- [[database-testing]]
- [[pydantic-test-models]]
