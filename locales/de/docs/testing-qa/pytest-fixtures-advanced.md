---
title: "Pytest-Fixtures – Fortgeschrittene Muster"
category: patterns
tags: [pytest, fixtures, conftest, scope, yield, factory, dependency-injection]
level: 4
source_sha256: 78438788ad090b0a252c750b32e4d90783a60d0fdba3185c9af71e1c375ca85d
translation: machine
translated_at: '2026-10-24'
---
# Pytest-Fixtures – Fortgeschrittene Muster {#pytest-fixtures-advanced-patterns}

Über die Grundlagen hinaus: Scope-Strategien, Factory-Muster, Fixture-Komposition und die conftest-Hierarchie für große Testsuiten.

## Fixture-Scopes {#fixture-scopes}

```python
import pytest

@pytest.fixture(scope="session")
def db_connection():
    """One connection for entire test run."""
    conn = create_connection()
    yield conn
    conn.close()

@pytest.fixture(scope="module")
def test_user(db_connection):
    """One user per test module."""
    user = db_connection.create_user(name="test")
    yield user
    db_connection.delete_user(user.id)

@pytest.fixture(scope="function")  # default
def fresh_token(test_user):
    """New token per test function."""
    return test_user.generate_token()
```

- `session` - einmal pro pytest-Lauf (DB-Verbindungen, Server-Start)
- `module` - einmal pro .py-Datei (gemeinsam genutzte Testdaten innerhalb des Moduls)
- `class` - einmal pro Testklasse
- `function` - einmal pro Test (Standard, am sichersten)

## Factory-Fixtures {#factory-fixtures}

Wenn Tests mehrere Instanzen mit unterschiedlichen Konfigurationen benötigen:

```python
@pytest.fixture
def make_user(db_connection):
    """Factory: create users with custom attributes."""
    created = []

    def _make_user(name="default", role="user", **kwargs):
        user = db_connection.create_user(name=name, role=role, **kwargs)
        created.append(user)
        return user

    yield _make_user

    # cleanup all created users
    for user in created:
        db_connection.delete_user(user.id)


def test_admin_permissions(make_user):
    admin = make_user(name="admin", role="admin")
    regular = make_user(name="regular", role="user")
    assert admin.can_delete(regular)
```

## Fixture-Komposition über conftest.py {#fixture-composition-via-conftestpy}

```python
tests/
  conftest.py           # session-scoped: DB, app server
  api/
    conftest.py         # API client, auth tokens
    test_users.py
    test_orders.py
  ui/
    conftest.py         # browser, page objects
    test_login.py
```

Jede `conftest.py` wird von pytest automatisch erkannt. Fixtures werden kaskadiert: Eine innere conftest kann Fixtures aus einer äußeren conftest verwenden.

```python
# tests/conftest.py
@pytest.fixture(scope="session")
def app():
    return create_app(config="test")

# tests/api/conftest.py
@pytest.fixture
def api_client(app):
    return app.test_client()

# tests/api/test_users.py
def test_list_users(api_client):
    resp = api_client.get("/api/users")
    assert resp.status_code == 200
```

## autouse-Fixtures {#autouse-fixtures}

```python
@pytest.fixture(autouse=True)
def reset_db(db_connection):
    """Runs before/after EVERY test in this scope."""
    yield
    db_connection.rollback()
```

- `autouse=True` wendet die Fixture auf alle Tests im Gültigkeitsbereich an, ohne dass sie explizit als Parameter angegeben werden muss
- Nützlich für Aufräumarbeiten, Zeitmessung, Logging
- Gefährlich, wenn der Scope zu breit ist – kann die Testsuite verlangsamen

## Yield-Fixtures für Setup/Teardown {#yield-fixtures-for-setupteardown}

```python
@pytest.fixture
def temp_file():
    path = Path("/tmp/test_data.json")
    path.write_text('{"key": "value"}')
    yield path                    # test runs here
    path.unlink(missing_ok=True)  # cleanup after test
```

Alles vor `yield` ist Setup. Alles nach `yield` ist Teardown. Der Teardown läuft auch dann, wenn der Test fehlschlägt.

## Request-Objekt für dynamische Fixtures {#request-object-for-dynamic-fixtures}

```python
@pytest.fixture
def browser(request):
    browser_name = request.param  # from parametrize
    driver = create_driver(browser_name)
    yield driver
    driver.quit()

@pytest.mark.parametrize("browser", ["chrome", "firefox"], indirect=True)
def test_homepage(browser):
    browser.get("https://example.com")
```

`request.node` ermöglicht den Zugriff auf Testmetadaten (Marker, Name, Modul).

## Fixture-Finalisierung mit addfinalizer {#fixture-finalization-with-addfinalizer}

```python
@pytest.fixture
def resource(request):
    r = acquire_resource()

    def cleanup():
        r.release()

    request.addfinalizer(cleanup)
    return r
```

Unterschied zu yield: `addfinalizer` kann mehrere Cleanup-Callbacks registrieren, und jeder läuft unabhängig, selbst wenn ein anderer fehlschlägt.

## Umgebungsabhängige Konfiguration {#environment-aware-configuration}

```python
# conftest.py
def pytest_addoption(parser):
    parser.addoption("--env", default="dev", choices=["dev", "staging", "prod"])

@pytest.fixture(scope="session")
def env_config(request):
    env = request.config.getoption("--env")
    return load_config(f"config/{env}.yaml")
```

Ausführung mit: `pytest --env=staging`

## Stolperfallen {#gotchas}

- **Problem:** Fixture mit `scope="session"` hängt von einer Fixture mit `scope="function"` ab -> Fehler `ScopeMismatch`. **Lösung:** Fixtures mit höherem Scope können nur von Fixtures mit gleichem oder höherem Scope abhängen. Strukturiere die Session-Fixtures so um, dass sie in sich geschlossen sind.

- **Problem:** `autouse=True` bei einer Session-Fixture in der Root-conftest läuft für ALLE Tests, auch für nicht zugehörige. **Lösung:** Platziere autouse-Fixtures in der möglichst engsten conftest. Verwende Marker, um bedingt zu überspringen: `if "skip_db" in request.keywords: return`.

- **Problem:** Factory-Fixture erstellt Ressourcen, aber der Test schlägt fehl, bevor die Cleanup-Liste befüllt wurde. **Lösung:** Füge Ressourcen immer sofort nach der Erstellung zur Cleanup-Liste hinzu, noch vor allen Assertions.

- **Problem:** Mehrere conftest.py-Dateien definieren eine Fixture mit demselben Namen – stilles Überschreiben ohne Warnung. **Lösung:** Verwende eindeutige, präfixierte Namen oder belasse Fixture-Definitionen auf einer einzigen conftest-Ebene.

## Siehe auch {#see-also}

- [[pytest-fundamentals]]
- [[test-architecture]]
- [[test-data-management]]
