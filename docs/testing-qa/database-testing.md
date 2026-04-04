---
title: Database Testing from Test Code
category: patterns
tags: [database, sql, postgres, sqlalchemy, fixtures, rollback, data-verification, white-box]
---

# Database Testing from Test Code

Querying databases directly from tests: verifying data integrity after API calls, setting up preconditions, and using transactions for isolation. Essential for white-box testing of [[microservice architectures|test-architecture]].

## Why Query DB from Tests

API response says `201 Created` - but was the data actually saved correctly? DB queries verify:

- Data persisted with correct values
- Foreign keys and relations created
- Timestamps, defaults, computed columns correct
- No orphaned records after delete operations
- Side effects (audit logs, history tables) triggered

## SQLAlchemy Connection Setup

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

## Verify API Actions via DB

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

## Setup Test Data via DB

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

## Transaction Rollback for Isolation

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

Every test sees a clean state. No cleanup code needed. Fast (no data recreation).

## Async DB with asyncpg

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

## Multiple Database Verification

For microservices with separate databases:

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

## Gotchas

- **Issue:** Test modifies DB but API reads from a different connection/pool - sees stale data due to transaction isolation. **Fix:** Commit test data before API calls, or ensure both test and app share the same transaction (requires app-level support).

- **Issue:** Rollback fixture doesn't work when test commits explicitly. **Fix:** Use savepoints: `session.begin_nested()` for inner transactions that can be rolled back independently.

- **Issue:** DB schema changes break raw SQL queries in tests. **Fix:** Use ORM models for queries when possible. For raw SQL, keep queries in a helper module and update centrally. Add schema version checks in CI.

## See Also

- [[test-data-management]]
- [[docker-test-environments]]
- [[fastapi-test-services]]
