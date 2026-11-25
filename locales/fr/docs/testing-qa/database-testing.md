---
title: "Tests de base de données depuis le code de test"
category: patterns
tags: [database, sql, postgres, sqlalchemy, fixtures, rollback, data-verification, white-box]
level: 3
source_sha256: 8735b4ebfab0a67db6b87467e8619a2930afd3bb159df7e7474d9f011d8bcc6d
translation: machine
translated_at: '2026-10-24'
---
# Tests de base de données depuis le code de test {#database-testing-from-test-code}

Interroger directement la base de données depuis les tests : vérifier l'intégrité des données après les appels d'API, préparer les préconditions et utiliser les transactions pour l'isolation. Essentiel pour les tests en boîte blanche des [[microservice architectures|architectures de tests]].

## Pourquoi interroger la base depuis les tests {#why-query-db-from-tests}

La réponse de l'API indique `201 Created`, mais les données ont-elles réellement été correctement enregistrées ? Les requêtes sur la base permettent de vérifier :

- La persistance des données avec les valeurs correctes
- La création des clés étrangères et des relations
- L'exactitude des horodatages, des valeurs par défaut et des colonnes calculées
- L'absence d'enregistrements orphelins après les opérations de suppression
- Le déclenchement des effets de bord (journaux d'audit, tables d'historique)

## Configuration de la connexion SQLAlchemy {#sqlalchemy-connection-setup}

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

## Vérifier les actions de l'API via la base {#verify-api-actions-via-db}

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

## Préparer les données de test via la base {#setup-test-data-via-db}

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

## Annulation de transaction pour l'isolation {#transaction-rollback-for-isolation}

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

Chaque test voit un état propre. Aucun code de nettoyage n'est nécessaire. Rapide (pas de recréation des données).

## Base de données asynchrone avec asyncpg {#async-db-with-asyncpg}

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

## Vérification sur plusieurs bases de données {#multiple-database-verification}

Pour les microservices disposant de bases séparées :

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

## Pièges courants {#gotchas}

- **Problème :** Le test modifie la base mais l'API lit depuis une autre connexion ou un autre pool, et voit des données obsolètes en raison de l'isolation des transactions. **Solution :** Valider (commit) les données de test avant les appels à l'API, ou s'assurer que le test et l'application partagent la même transaction (nécessite une prise en charge au niveau de l'application).

- **Problème :** La fixture de rollback ne fonctionne pas lorsque le test effectue un commit explicite. **Solution :** Utiliser des points de sauvegarde (savepoints) avec `session.begin_nested()` pour les transactions imbriquées pouvant être annulées indépendamment.

- **Problème :** Les modifications du schéma de la base cassent les requêtes SQL brutes des tests. **Solution :** Utiliser les modèles ORM pour les requêtes lorsque c'est possible. Pour le SQL brut, regrouper les requêtes dans un module d'aide et les mettre à jour de manière centralisée. Ajouter des vérifications de version du schéma dans la CI.

## Voir aussi {#see-also}

- [[test-data-management]]
- [[docker-test-environments]]
- [[fastapi-test-services]]
