---
title: "Testparallelisierung"
category: patterns
tags: [pytest-xdist, parallel, concurrency, test-isolation, performance, scaling]
level: 3
source_sha256: 35899b2f16d4418d3b1f7d7db89c873e8a598713b31d79686daa218f36239963
translation: machine
translated_at: '2026-10-24'
---
# Testparallelisierung {#test-parallelization}

Ausführung von Tests parallel mit pytest-xdist. Verkürzt die Ausführungszeit der Suite proportional zur Anzahl der Worker, setzt jedoch Test-Isolation voraus.

## pytest-xdist Setup {#pytest-xdist-setup}

```bash
pip install pytest-xdist
```

```bash
# Auto-detect CPU count
pytest -n auto

# Fixed worker count
pytest -n 4

# Distribute by file (default: round-robin)
pytest -n 4 --dist loadfile

# Distribute by test group
pytest -n 4 --dist loadgroup
```

## Verteilungsmodi {#distribution-modes}

| Modus | Verhalten | Geeignet für |
|------|----------|----------|
| `load` (Standard) | Round-Robin auf verfügbare Worker | Unabhängige Tests |
| `loadfile` | Alle Tests aus derselben Datei laufen auf demselben Worker | Tests, die Fixtures auf Modulebene teilen |
| `loadgroup` | Tests mit demselben `@pytest.mark.xdist_group` laufen auf demselben Worker | Tests, die Ressourcen teilen |
| `loadscope` | Gruppierung nach Modul/Klasse | Fixtures mit Scope `module` |

## Gruppierung abhängiger Tests {#grouping-dependent-tests}

```python
@pytest.mark.xdist_group("user_crud")
def test_create_user():
    ...

@pytest.mark.xdist_group("user_crud")
def test_update_user():
    ...

@pytest.mark.xdist_group("user_crud")
def test_delete_user():
    ...
```

Ausführung mit `pytest -n 4 --dist loadgroup`: Diese drei Tests laufen in dieser Reihenfolge auf demselben Worker.

## Fixture-Scoping mit xdist {#fixture-scoping-with-xdist}

Fixtures mit Scope `session` gelten pro Worker, nicht pro Lauf:

```python
@pytest.fixture(scope="session")
def db_connection():
    # Each xdist worker gets its own connection
    conn = connect_db()
    yield conn
    conn.close()
```

Für tatsächlich gemeinsam genutzten Zustand über Worker hinweg verwendet man `tmp_path_factory` oder Dateisperren:

```python
@pytest.fixture(scope="session")
def shared_setup(tmp_path_factory, worker_id):
    if worker_id == "master":
        # not running with xdist
        setup_once()
        return

    root_tmp = tmp_path_factory.getbasetemp().parent
    lock = root_tmp / "setup.lock"
    marker = root_tmp / "setup.done"

    with FileLock(str(lock)):
        if not marker.exists():
            setup_once()
            marker.touch()
```

## Worker-bewusste Datenbankisolation {#worker-aware-database-isolation}

```python
@pytest.fixture(scope="session")
def db_name(worker_id):
    """Each worker gets its own database."""
    if worker_id == "master":
        return "testdb"
    return f"testdb_{worker_id}"

@pytest.fixture(scope="session")
def db_connection(db_name):
    create_database(db_name)
    conn = connect(db_name)
    yield conn
    conn.close()
    drop_database(db_name)
```

## Performance-Messung {#performance-measurement}

```bash
# Sequential baseline
time pytest tests/ -v
# 120 seconds

# Parallel with 4 workers
time pytest tests/ -n 4 -v
# 35 seconds
```

Der Speedup hängt von der Unabhängigkeit der Tests und vom I/O-Muster ab. CPU-gebundene Tests skalieren linear. I/O-gebundene Tests (API-Aufrufe, Datenbank) skalieren aufgrund von Überlappung überlinear.

## Marker für sequenzielle Tests {#marks-for-sequential-tests}

```python
# conftest.py
def pytest_collection_modifyitems(config, items):
    if config.getoption("-n", default=None):
        for item in items:
            if "sequential" in item.keywords:
                item.add_marker(pytest.mark.xdist_group("sequential"))

@pytest.mark.sequential
def test_must_run_alone():
    ...
```

## Stolperfallen {#gotchas}

- **Problem:** Tests laufen sequenziell fehlerfrei, schlagen aber mit xdist fehl – geteilter veränderlicher Zustand (globale Variablen, Dateien, Datenbankzeilen). **Lösung:** Jeder Test muss seine eigenen Daten erzeugen. Eindeutige Bezeichner pro Worker verwenden: `f"user_{worker_id}_{uuid4()}"`.

- **Problem:** Session-Fixtures laufen mehrfach (einmal pro Worker), wodurch aufwendiges Setup wiederholt wird. **Lösung:** Dateibasierte Sperren (Paket `filelock`) für einmalige Initialisierung verwenden. Alternativ die Verteilung `loadscope` nutzen.

- **Problem:** `-n auto` auf CI-Systemen mit vielen Kernen startet zu viele Worker und überlastet die Datenbank. **Lösung:** Eine explizite Worker-Anzahl setzen, die zu den verfügbaren Ressourcen passt: `-n 4` statt `-n auto`. Die Anzahl der DB-Verbindungen überwachen.

## Siehe auch {#see-also}

- [[pytest-fundamentals]]
- [[pytest-fixtures-advanced]]
- [[ci-cd-test-automation]]
