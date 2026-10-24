---
title: "Datenbanktests aus Testcode"
category: patterns
tags: [database, sql, postgres, sqlalchemy, fixtures, rollback, data-verification, white-box]
level: 3
source_sha256: 8735b4ebfab0a67db6b87467e8619a2930afd3bb159df7e7474d9f011d8bcc6d
translation: machine
translated_at: '2026-10-24'
---
# Datenbanktests aus Testcode {#database-testing-from-test-code}

Direktes Abfragen von Datenbanken aus Tests: Überprüfung der Datenintegrität nach API-Aufrufen, Einrichtung von Vorbedingungen und Nutzung von Transaktionen zur Isolation. Unverzichtbar für White-Box-Tests von [[microservice architectures|Test-Architektur]].

## Warum die DB aus Tests abfragen {#why-query-db-from-tests}

Die API-Antwort lautet `201 Created`, aber wurden die Daten tatsächlich korrekt gespeichert? DB-Abfragen überprüfen:

- Daten wurden mit korrekten Werten persistiert
- Fremdschlüssel und Relationen wurden angelegt
- Zeitstempel, Standardwerte und berechnete Spalten sind korrekt
- Keine verwaisten Datensätze nach Löschvorgängen
- Nebenwirkungen (Audit-Logs, Historientabellen) wurden ausgelöst

## SQLAlchemy-Verbindungseinrichtung {#sqlalchemy-connection-setup}

```python
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

@pytest.fixture(scope="session")
def db_engine(config):
    engine = create_engine(config.db_url)
    yield engine
    engine.dispose()

@pytest.fixture
def db(db_engine):
    with Session(db_engine) as session:
        yield session
        session.rollback()
```

## API-Aktionen über die DB verifizieren {#verify-api-actions-via-db}

```python
def test_create_user_persisted(api_client, db):
    # Act via API
    resp = api_client.post("/api/users", json={
        "name": "Alice",
        "email": "alice@example.com"
    })
    assert resp.status_code == 201
    user_id = resp.json()["id"]

    # Verify via DB
    row = db.execute(
        text("SELECT name, email, created_at FROM users WHERE id = :id"),
        {"id": user_id}
    ).fetchone()

    assert row is not None
    assert row.name == "Alice"
    assert row.email == "alice@example.com"
    assert row.created_at is not None
```

## Testdaten über die DB einrichten {#setup-test-data-via-db}

```python
@pytest.fixture
def existing_user(db):
    """Insert user directly, bypassing API."""
    db.execute(text("""
        INSERT INTO users (id, name, email, role)
        VALUES (:id, :name, :email, :role)
    """), {"id": 999, "name": "TestUser", "email": "test@test.com", "role": "admin"})
    db.commit()
    yield {"id": 999, "name": "TestUser"}
    db.execute(text("DELETE FROM users WHERE id = :id"), {"id": 999})
    db.commit()

def test_get_user(api_client, existing_user):
    resp = api_client.get(f"/api/users/{existing_user['id']}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "TestUser"
```

## Transaktions-Rollback zur Isolation {#transaction-rollback-for-isolation}

```python
@pytest.fixture
def db_session(db_engine):
    """Transaction that rolls back after each test."""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()
```

Jeder Test sieht einen sauberen Zustand. Kein Aufräumcode nötig. Schnell (keine Neuerstellung der Daten).

## Asynchrone DB mit asyncpg {#async-db-with-asyncpg}

```python
import asyncpg

@pytest.fixture
async def async_db(config):
    conn = await asyncpg.connect(config.db_url)
    yield conn
    await conn.close()

async def test_user_count(async_db):
    count = await async_db.fetchval("SELECT count(*) FROM users")
    assert count > 0
```

## Verifikation mehrerer Datenbanken {#multiple-database-verification}

Für Microservices mit getrennten Datenbanken:

```python
@pytest.fixture(scope="session")
def user_db(config):
    return create_engine(config.user_db_url)

@pytest.fixture(scope="session")
def order_db(config):
    return create_engine(config.order_db_url)

def test_order_creates_cross_service_data(api_client, user_db, order_db):
    resp = api_client.post("/api/orders", json={...})
    order_id = resp.json()["id"]

    # Check order DB
    with Session(order_db) as s:
        order = s.execute(text("SELECT * FROM orders WHERE id = :id"),
                          {"id": order_id}).fetchone()
        assert order is not None

    # Check user DB (activity log)
    with Session(user_db) as s:
        log = s.execute(text("SELECT * FROM activity_log WHERE order_id = :id"),
                        {"id": order_id}).fetchone()
        assert log is not None
```

## Stolperfallen {#gotchas}

- **Problem:** Der Test ändert die DB, die API liest jedoch über eine andere Verbindung/einen anderen Pool und sieht aufgrund der Transaktionsisolation veraltete Daten. **Lösung:** Testdaten vor den API-Aufrufen committen oder sicherstellen, dass Test und Anwendung dieselbe Transaktion teilen (erfordert Unterstützung auf Anwendungsebene).

- **Problem:** Das Rollback-Fixture funktioniert nicht, wenn der Test explizit committet. **Lösung:** Savepoints verwenden: `session.begin_nested()` für innere Transaktionen, die unabhängig voneinander zurückgerollt werden können.

- **Problem:** Schemaänderungen der DB brechen Raw-SQL-Abfragen in Tests. **Lösung:** Nach Möglichkeit ORM-Modelle für Abfragen verwenden. Für Raw SQL die Abfragen in einem Hilfsmodul halten und zentral aktualisieren. Prüfungen der Schemaversion in der CI ergänzen.

## Siehe auch {#see-also}

- [[test-data-management]]
- [[docker-test-environments]]
- [[fastapi-test-services]]
