---
title: "Gestion des données de test"
category: patterns
tags: [test-data, fixtures, factories, env-config, dotenv, parametrize, data-driven]
level: 3
source_sha256: d54b70948ccaf7a40f931e94de509a9d8c9ad9d653351d45d5dfa0add646aa34
translation: machine
translated_at: '2026-10-24'
---
# Gestion des données de test {#test-data-management}

Stratégies de création, de gestion et de nettoyage des données de test dans les différents environnements. Couvre les configurations d'environnement, les factories de données, la paramétrisation et les données de test stockées dans des fichiers.

## Configuration de l'environnement {#environment-configuration}

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

Exécution : `TEST_ENV=staging pytest`

## Paramétrisation pour les tests pilotés par les données {#parametrize-for-data-driven-tests}

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

## Fichiers de données externes {#external-data-files}

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

## Fixtures de base de données avec rollback {#database-fixtures-with-rollback}

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

Chaque test voit un état de base de données propre, sans recréation coûteuse.

## Données aléatoires mais reproductibles {#random-but-reproducible-data}

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

## Stratégies de nettoyage {#cleanup-strategies}

| Stratégie | Quand l'utiliser |
|-----------|------------------|
| Rollback de transaction | Tests de base de données, le plus rapide |
| Teardown de fixture (yield) | Ressources créées via l'API |
| Factory + collecteur | Plusieurs ressources par test |
| Troncature de la base de données | Tests d'intégration complets |
| Recréation Docker | Isolation complète nécessaire |

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

## Points d'attention {#gotchas}

- **Problème :** Les données de test codées en dur (identifiants d'utilisateurs, URL) cassent lorsqu'on change d'environnement. **Correctif :** Toutes les valeurs propres à un environnement sont placées dans des fichiers de configuration chargés par les fixtures. Ne jamais coder en dur `/api/users/2`, utiliser `f"/api/users/{user_id}"`.

- **Problème :** Les tests dépendent de données créées par d'autres tests (dépendance à l'ordre d'exécution). **Correctif :** Chaque test doit créer ses propres données via les fixtures. Utiliser `pytest-randomly` pour détecter les dépendances cachées à l'ordre d'exécution.

- **Problème :** Un fichier `.env` contenant de vrais identifiants est versionné dans git. **Correctif :** Ajouter `.env*` à `.gitignore`. Utiliser un `.env.example` avec des valeurs factices. La CI récupère les secrets depuis les variables d'environnement.

## Voir aussi {#see-also}

- [[pytest-fixtures-advanced]]
- [[database-testing]]
- [[pydantic-test-models]]
