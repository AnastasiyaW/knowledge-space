---
title: "Pytest-Grundlagen"
category: framework
tags: [pytest, fixtures, conftest, parametrize, xdist, markers, hooks, parallel, scope]
level: 2
source_sha256: a85b9330858beea45defc069ea05f91be6d6b66202e5cdd8636a21b3fcf3579f
translation: machine
translated_at: '2026-10-24'
---
# Pytest-Grundlagen {#pytest-fundamentals}

Pytest ist das leistungsstärkste Test-Framework für Python. Fixtures ersetzen Setup und Teardown durch dependency-injizierte, gescopte und komponierbare Funktionen. Parametrize erzeugt Testmatrizen. xdist ermöglicht parallele Ausführung. Hooks erweitern das Verhalten von pytest an jedem Punkt des Lebenszyklus. Zusammen decken sie alles ab, von Unit-Tests bis zu komplexen E2E-Suites.

## Wichtige Fakten {#key-facts}

- Fixtures verwenden `@pytest.fixture` + `yield` (davor = Setup, danach = Teardown); der Teardown läuft auch bei Fehlschlägen
- Scopes: `function` (Standard), `class`, `module`, `session` – steuern den Lebenszyklus einer Fixture
- `conftest.py` = automatisch erkannte, verzeichnisbezogene Datei für Fixtures und Hooks (keine Imports nötig)
- `parametrize` erzeugt separate Testfälle; `indirect=True` übergibt Werte über `request.param` an Fixtures
- `pytest-xdist` führt parallele Prozesse aus (`-n 4`), NICHT Threads – Session-Fixtures werden in JEDEM Worker ausgeführt
- Hooks: `pytest_collection_modifyitems`, `pytest_runtest_call`, `pytest_generate_tests`, `pytest_addoption`

## Muster {#patterns}

### Fixtures mit Abhängigkeitskette {#fixtures-with-dependency-chain}

```python
@pytest.fixture(scope="session")
def envs():
    load_dotenv()

@pytest.fixture(scope="session")
def gateway_url(envs):  # explicit dependency ensures order
    return os.getenv("GATEWAY_URL")

@pytest.fixture(scope="session")
def auth_token(gateway_url):
    return login_and_get_token(gateway_url)

@pytest.fixture
def spend(spend_client, category):
    created = spend_client.add_spend({"category": category, "amount": 100})
    yield created  # test runs here
    spend_client.delete_spend(created["id"])  # cleanup
```

### Parametrize {#parametrize}

```python
@pytest.mark.parametrize("username, password, expected", [
    ("valid_user", "valid_pass", True),
    ("invalid_user", "wrong_pass", False)])
def test_login(username, password, expected):
    assert login(username, password) == expected

# Indirect: pass values to fixture
@pytest.fixture
def category(request):
    return create_if_missing(request.param)

@pytest.mark.parametrize("category", ["school", "food"], indirect=True)
def test_with_category(category):
    assert category is not None
```

### Parallele Ausführung (xdist) {#parallel-execution-xdist}

```bash
pytest -n 4                    # 4 parallel workers
pytest -n auto                 # one worker per CPU core
pytest --dist=loadscope        # group by module (default)
pytest --dist=load             # distribute individual tests
```

Session-Fixtures laufen in jedem Worker unabhängig voneinander – bei 4 Workern erstellt das DB-Setup somit 4 Datenbanken. Für gemeinsam genutzte Ressourcen Dateisperren oder `--dist=loadscope` verwenden.

### Marks und Testauswahl {#marks-and-test-selection}

```python
@pytest.mark.skip(reason="Not implemented yet")
@pytest.mark.skipif(sys.platform == "win32", reason="Unix only")
@pytest.mark.xfail(reason="BUG-123")  # expected failure

# Localized xfail (preferred - catches unexpected breakage)
def test_buggy():
    setup_data()
    try:
        result = buggy_operation()
    except SomeError:
        pytest.xfail("BUG-123: specific operation fails")
```

```bash
pytest -k "mobile"           # name filter
pytest -k "not slow"         # exclude
pytest -k "login and api"    # boolean
```

### Benutzerdefinierte Optionen über Hooks {#custom-options-via-hooks}

```python
# conftest.py
def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome")

@pytest.fixture
def browser_name(request):
    return request.config.getoption("--browser")
```

### conftest-Plugins (Skalierung von Fixtures) {#conftest-plugins-scaling-fixtures}

```python
# conftest.py - solves bloated conftest and sibling-directory visibility
pytest_plugins = [
    "fixtures.user_fixtures",
    "fixtures.auth_fixtures",
    "fixtures.db_fixtures"]
```

### Fuzz-Testing mit Hypothesis {#fuzz-testing-with-hypothesis}

```python
from hypothesis import given, strategies as st

@given(st.integers(), st.integers())
def test_addition_commutative(a, b):
    assert add(a, b) == add(b, a)
# Generates 100 random combinations; best for pure functions, bad for I/O
```

## Fallstricke {#gotchas}

- `autouse=True` garantiert NICHT die Reihenfolge einer Fixture relativ zu anderen Fixtures – explizite Abhängigkeiten verwenden
- Session-gescopte Fixtures mit xdist laufen pro Worker, nicht einmal global
- `pytest -l` (showlocals) gibt bei Fehlschlägen ALLE Variablen aus – kann Secrets in CI-Logs offenlegen
- Token-Ablauf in session-gescopten Fixtures: lange Läufe können mitten in der Session fehlschlagen; Module-Scope oder Refresh-Logik erwägen
- Coverage von ~85 % ist ein gutes Ziel; 100 % bedeuten nicht, dass der Code fehlerfrei ist

## Siehe auch {#see-also}

- [[allure-reporting]] - Test-Reporting mit Allure-Annotationen
- [[page-object-model]] - Fixture-Integration mit POM
- [[test-architecture]] - Projektstruktur und Organisation der conftest-Dateien
- [[ci-cd-test-automation]] - Ausführung von pytest in CI-Pipelines
