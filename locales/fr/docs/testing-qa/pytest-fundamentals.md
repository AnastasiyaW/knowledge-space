---
title: "Fondamentaux de Pytest"
category: framework
tags: [pytest, fixtures, conftest, parametrize, xdist, markers, hooks, parallel, scope]
level: 2
source_sha256: a85b9330858beea45defc069ea05f91be6d6b66202e5cdd8636a21b3fcf3579f
translation: machine
translated_at: '2026-10-24'
---
# Fondamentaux de Pytest {#pytest-fundamentals}

Pytest est le framework de test le plus puissant de Python. Les fixtures remplacent setup/teardown par des fonctions à injection de dépendances, à portée définie et composables. Parametrize génère des matrices de tests. xdist permet l'exécution en parallèle. Les hooks étendent le comportement de pytest à chaque point du cycle de vie. Ensemble, ils couvrent tout, des tests unitaires aux suites E2E complexes.

## Points clés {#key-facts}

- Les fixtures utilisent `@pytest.fixture` + `yield` (avant = setup, après = teardown) ; le teardown s'exécute même en cas d'échec
- Portées : `function` (par défaut), `class`, `module`, `session` - contrôlent le cycle de vie des fixtures
- `conftest.py` = fichier de fixtures/hooks découvert automatiquement, à portée de répertoire (aucun import nécessaire)
- `parametrize` génère des cas de test distincts ; `indirect=True` transmet des valeurs aux fixtures via `request.param`
- `pytest-xdist` exécute des processus parallèles (`-n 4`), PAS des threads - les fixtures de session s'exécutent dans CHAQUE worker
- Hooks : `pytest_collection_modifyitems`, `pytest_runtest_call`, `pytest_generate_tests`, `pytest_addoption`

## Modèles d'utilisation {#patterns}

### Fixtures avec chaîne de dépendances {#fixtures-with-dependency-chain}

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

### Exécution en parallèle (xdist) {#parallel-execution-xdist}

```bash
pytest -n 4                    # 4 parallel workers
pytest -n auto                 # one worker per CPU core
pytest --dist=loadscope        # group by module (default)
pytest --dist=load             # distribute individual tests
```

Les fixtures de session s'exécutent indépendamment dans chaque worker - avec 4 workers, la mise en place de la base de données crée 4 bases. Utilisez des verrous de fichiers ou `--dist=loadscope` pour les ressources partagées.

### Marques et sélection de tests {#marks-and-test-selection}

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

### Options personnalisées via les hooks {#custom-options-via-hooks}

```python
# conftest.py
def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome")

@pytest.fixture
def browser_name(request):
    return request.config.getoption("--browser")
```

### Plugins conftest (mise à l'échelle des fixtures) {#conftest-plugins-scaling-fixtures}

```python
# conftest.py - solves bloated conftest and sibling-directory visibility
pytest_plugins = [
    "fixtures.user_fixtures",
    "fixtures.auth_fixtures",
    "fixtures.db_fixtures"]
```

### Fuzzing avec Hypothesis {#fuzz-testing-with-hypothesis}

```python
from hypothesis import given, strategies as st

@given(st.integers(), st.integers())
def test_addition_commutative(a, b):
    assert add(a, b) == add(b, a)
# Generates 100 random combinations; best for pure functions, bad for I/O
```

## Pièges {#gotchas}

- `autouse=True` ne garantit PAS l'ordre d'exécution des fixtures par rapport aux autres fixtures - utilisez des dépendances explicites
- Les fixtures de session avec xdist s'exécutent par worker, et non une seule fois globalement
- `pytest -l` (showlocals) affiche TOUTES les variables en cas d'échec - peut exposer des secrets dans les logs CI
- Expiration de jeton dans les fixtures de portée session : les longues exécutions peuvent échouer en cours de session ; envisagez une portée module ou une logique de rafraîchissement
- Couverture ~85% = bon objectif ; 100% ne signifie pas absence de bugs

## Voir aussi {#see-also}

- [[allure-reporting]] - reporting de tests avec les annotations Allure
- [[page-object-model]] - intégration des fixtures avec le POM
- [[test-architecture]] - structure du projet et organisation des conftest
- [[ci-cd-test-automation]] - exécution de pytest dans les pipelines CI
