---
title: "Tests avec Pytest"
category: concepts
tags: [python, pytest, unittest, testing, fixtures, mocking, coverage]
level: 3
source_sha256: db693f447e71e145086a9087577d34a0ef28d437809884d627110e2004caa9b6
translation: machine
translated_at: '2026-10-24'
---
# Tests avec Pytest {#testing-with-pytest}

pytest est le framework de test de référence pour Python, plus concis et plus puissant que le module unittest intégré. Il utilise des instructions `assert` simples, des fixtures pour la mise en place et le nettoyage, ainsi que parametrize pour les tests pilotés par les données.

## Points clés {#key-facts}

- Fichiers de test : `test_*.py` ou `*_test.py` ; fonctions de test : `test_*`
- `assert` simple avec des messages d'échec descriptifs (pas de `self.assertEqual`)
- Les fixtures fournissent une mise en place et un nettoyage réutilisables, avec injection de dépendances
- `conftest.py` partage les fixtures entre les fichiers de test (découvert automatiquement, sans import nécessaire)
- Portées des fixtures : function (par défaut), class, module, session
- `pytest-cov` pour les rapports de couverture ; `pytest-mock` pour le mocking

## Patrons {#patterns}

### Tests de base {#basic-tests}
```python
def test_addition():
    assert add(2, 3) == 5

def test_raises():
    import pytest
    with pytest.raises(ValueError):
        parse_int("abc")

def test_approximate():
    assert 0.1 + 0.2 == pytest.approx(0.3)
```

### Fixtures {#fixtures}
```python
import pytest

@pytest.fixture
def db_session():
    session = create_session()
    yield session       # test runs here
    session.close()     # cleanup after test

@pytest.fixture
def sample_user(db_session):  # fixtures can depend on other fixtures
    user = User(name="test", email="test@test.com")
    db_session.add(user)
    db_session.commit()
    return user

def test_user_exists(db_session, sample_user):
    result = db_session.query(User).filter_by(name="test").first()
    assert result.email == "test@test.com"
```

### Portées des fixtures {#fixture-scopes}
```python
@pytest.fixture(scope="session")   # once per entire test session
def app():
    return create_app(testing=True)

@pytest.fixture(scope="module")    # once per test file
def db():
    return setup_db()
```

### conftest.py (fixtures partagées) {#conftestpy-shared-fixtures}
```python
# conftest.py - auto-discovered by pytest
@pytest.fixture(scope="session")
def app():
    return create_app(testing=True)

@pytest.fixture(scope="session")
def client(app):
    return TestClient(app)
```

### Parametrize {#parametrize}
```python
@pytest.mark.parametrize("input,expected", [
    ("hello", 5),
    ("", 0),
    ("hi", 2)])
def test_string_length(input, expected):
    assert len(input) == expected

# Parameterize fixtures too
@pytest.fixture(params=["sqlite", "postgresql"])
def db_engine(request):
    return create_engine(request.param)
```

### Tests avec FastAPI {#testing-fastapi}
```python
from fastapi.testclient import TestClient
from httpx import AsyncClient

# Sync testing
client = TestClient(app)
response = client.get("/api/hotels")
assert response.status_code == 200

# Async testing
@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.anyio
async def test_endpoint(async_client):
    response = await async_client.get("/api/hotels")
    assert response.status_code == 200
```

### Client de test authentifié {#authenticated-test-client}
```python
@pytest.fixture
async def auth_client(async_client):
    await async_client.post("/auth/login", json={
        "email": "test@test.com", "password": "test"
    })
    return async_client  # cookie stored in client
```

### Couverture de code {#coverage}
```bash
pip install pytest-cov
pytest --cov=mypackage --cov-report=html
# Generates htmlcov/ directory with visual report
```

## unittest (intégré) {#unittest-built-in}

```python
import unittest

class TestMyCode(unittest.TestCase):
    def setUp(self):
        self.data = create_test_data()

    def tearDown(self):
        cleanup()

    def test_addition(self):
        self.assertEqual(add(2, 3), 5)

    def test_raises(self):
        with self.assertRaises(ValueError):
            parse_int("abc")

    def test_parameterized(self):
        for num in [2, 4, 6]:
            with self.subTest(num=num):
                self.assertTrue(num % 2 == 0)
```

## Pyramide des tests {#testing-pyramid}

1. **Tests unitaires** (les plus nombreux) - fonctions individuelles, rapides, mocking des dépendances externes
2. **Tests d'intégration** (au milieu) - interaction entre composants, base de données réelle ou de test
3. **Tests E2E** (les moins nombreux) - parcours complets, les plus lents, les plus fragiles

## Pièges courants {#gotchas}

- Tester à la fois le cas nominal et les cas d'erreur
- Ne pas tester les détails d'implémentation : tester le comportement
- Mocker les dépendances externes (API, e-mail) pour les tests unitaires ; utiliser les vraies dépendances pour les tests d'intégration
- `pytest.fixture` avec `yield` garantit que le nettoyage s'exécute même si le test échoue
- `conftest.py` à différents niveaux de répertoire fournit différentes portées de fixtures

## Voir aussi {#see-also}

- [Gestion des erreurs et gestionnaires de contexte](error-handling.md) - tester la levée d'exceptions
- [[fastapi-fundamentals]] - tests des endpoints
- [[type-hints]] - mypy dans le pipeline CI
