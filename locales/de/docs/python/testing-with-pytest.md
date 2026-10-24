---
title: "Testen mit Pytest"
category: concepts
tags: [python, pytest, unittest, testing, fixtures, mocking, coverage]
level: 3
source_sha256: db693f447e71e145086a9087577d34a0ef28d437809884d627110e2004caa9b6
translation: machine
translated_at: '2026-10-24'
---
# Testen mit Pytest {#testing-with-pytest}

pytest ist der De-facto-Standard für Python-Testframeworks – prägnanter und leistungsfähiger als das integrierte unittest. Es verwendet einfache `assert`-Anweisungen, Fixtures für Setup und Teardown sowie Parametrize für datengetriebene Tests.

## Wichtige Fakten {#key-facts}

- Testdateien: `test_*.py` oder `*_test.py`; Testfunktionen: `test_*`
- Einfaches `assert` mit aussagekräftigen Fehlermeldungen (kein `self.assertEqual`)
- Fixtures stellen wiederverwendbares Setup/Teardown mit Dependency Injection bereit
- `conftest.py` teilt Fixtures über Testdateien hinweg (automatisch erkannt, kein Import nötig)
- Fixture-Gültigkeitsbereiche: function (Standard), class, module, session
- `pytest-cov` für Coverage-Berichte; `pytest-mock` für Mocking

## Muster {#patterns}

### Einfache Tests {#basic-tests}
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

### Fixture-Gültigkeitsbereiche {#fixture-scopes}
```python
@pytest.fixture(scope="session")   # once per entire test session
def app():
    return create_app(testing=True)

@pytest.fixture(scope="module")    # once per test file
def db():
    return setup_db()
```

### conftest.py (gemeinsam genutzte Fixtures) {#conftestpy-shared-fixtures}
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

### Testen von FastAPI {#testing-fastapi}
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

### Authentifizierter Test-Client {#authenticated-test-client}
```python
@pytest.fixture
async def auth_client(async_client):
    await async_client.post("/auth/login", json={
        "email": "test@test.com", "password": "test"
    })
    return async_client  # cookie stored in client
```

### Coverage {#coverage}
```bash
pip install pytest-cov
pytest --cov=mypackage --cov-report=html
# Generates htmlcov/ directory with visual report
```

## unittest (integriert) {#unittest-built-in}

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

## Testpyramide {#testing-pyramid}

1. **Unit-Tests** (die meisten) – einzelne Funktionen, schnell, externe Abhängigkeiten gemockt
2. **Integrationstests** (mittlere Ebene) – Zusammenspiel von Komponenten, echte bzw. Test-Datenbank
3. **E2E-Tests** (die wenigsten) – vollständige Workflows, am langsamsten, am anfälligsten für Brüche

## Fallstricke {#gotchas}

- Sowohl den Happy Path als auch Fehlerfälle testen
- Keine Implementierungsdetails testen – das Verhalten testen
- Externe Abhängigkeiten (APIs, E-Mail) in Unit-Tests mocken; für Integrationstests echte Abhängigkeiten verwenden
- `pytest.fixture` mit `yield` stellt sicher, dass die Bereinigung auch dann läuft, wenn der Test fehlschlägt
- `conftest.py` auf verschiedenen Verzeichnisebenen liefert unterschiedliche Fixture-Gültigkeitsbereiche

## Siehe auch {#see-also}

- [Fehlerbehandlung und Kontextmanager](error-handling.md) – Testen von Exception-Auslösung
- [[fastapi-fundamentals]] – Endpunkt-Tests
- [[type-hints]] – mypy in der CI-Pipeline
