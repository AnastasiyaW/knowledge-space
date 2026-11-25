---
title: "Fixtures Pytest - Patterns avancés"
category: patterns
tags: [pytest, fixtures, conftest, scope, yield, factory, dependency-injection]
level: 4
source_sha256: 78438788ad090b0a252c750b32e4d90783a60d0fdba3185c9af71e1c375ca85d
translation: machine
translated_at: '2026-10-24'
---
# Fixtures Pytest - Patterns avancés {#pytest-fixtures-advanced-patterns}

Au-delà des fixtures de base : stratégies de portée, patterns de fabrique, composition de fixtures et hiérarchie des conftest pour les suites de tests volumineuses.

## Portées des fixtures {#fixture-scopes}

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

- `session` - une fois par exécution de pytest (connexions à la base de données, démarrage du serveur)
- `module` - une fois par fichier .py (données de test partagées au sein du module)
- `class` - une fois par classe de test
- `function` - une fois par test (valeur par défaut, la plus sûre)

## Fixtures de fabrique {#factory-fixtures}

Lorsque les tests ont besoin de plusieurs instances avec des configurations différentes :

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

## Composition de fixtures via conftest.py {#fixture-composition-via-conftestpy}

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

Chaque `conftest.py` est découvert automatiquement par pytest. Les fixtures se propagent en cascade : un conftest interne peut utiliser les fixtures d'un conftest externe.

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

## Fixtures autouse {#autouse-fixtures}

```python
@pytest.fixture(autouse=True)
def reset_db(db_connection):
    """Runs before/after EVERY test in this scope."""
    yield
    db_connection.rollback()
```

- `autouse=True` applique la fixture à tous les tests de sa portée, sans paramètre explicite
- Utile pour le nettoyage, la mesure de temps et la journalisation
- Dangereux si la portée est trop large : cela peut ralentir la suite de tests

## Fixtures à yield pour l'initialisation et la libération {#yield-fixtures-for-setupteardown}

```python
@pytest.fixture
def temp_file():
    path = Path("/tmp/test_data.json")
    path.write_text('{"key": "value"}')
    yield path                    # test runs here
    path.unlink(missing_ok=True)  # cleanup after test
```

Tout ce qui précède `yield` constitue l'initialisation. Tout ce qui suit constitue la libération. La libération s'exécute même si le test échoue.

## Objet request pour les fixtures dynamiques {#request-object-for-dynamic-fixtures}

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

`request.node` donne accès aux métadonnées du test (marqueurs, nom, module).

## Finalisation de fixtures avec addfinalizer {#fixture-finalization-with-addfinalizer}

```python
@pytest.fixture
def resource(request):
    r = acquire_resource()

    def cleanup():
        r.release()

    request.addfinalizer(cleanup)
    return r
```

Différence avec yield : `addfinalizer` peut enregistrer plusieurs callbacks de nettoyage, et chacun s'exécute indépendamment même si un autre échoue.

## Configuration tenant compte de l'environnement {#environment-aware-configuration}

```python
# conftest.py
def pytest_addoption(parser):
    parser.addoption("--env", default="dev", choices=["dev", "staging", "prod"])

@pytest.fixture(scope="session")
def env_config(request):
    env = request.config.getoption("--env")
    return load_config(f"config/{env}.yaml")
```

Exécution avec : `pytest --env=staging`

## Pièges courants {#gotchas}

- **Problème :** Une fixture avec `scope="session"` dépend d'une fixture `scope="function"` -> erreur `ScopeMismatch`. **Correction :** Une fixture de portée plus large ne peut dépendre que de fixtures de même portée ou de portée plus large. Restructurez les fixtures de session pour qu'elles soient autonomes.

- **Problème :** `autouse=True` sur une fixture de session dans le conftest racine s'exécute pour TOUS les tests, y compris ceux qui n'ont aucun rapport. **Correction :** Placez les fixtures autouse dans le conftest le plus restreint possible. Utilisez des marqueurs pour ignorer conditionnellement : `if "skip_db" in request.keywords: return`.

- **Problème :** Une fixture de fabrique crée des ressources mais le test échoue avant que la liste de nettoyage ne soit remplie. **Correction :** Ajoutez toujours l'élément à la liste de nettoyage immédiatement après sa création, avant toute assertion.

- **Problème :** Plusieurs fichiers conftest.py définissent une fixture de même nom : la redéfinition se fait silencieusement, sans avertissement. **Correction :** Utilisez des noms uniques et préfixés, ou regroupez les définitions de fixtures dans un seul niveau de conftest.

## Voir aussi {#see-also}

- [[pytest-fundamentals]]
- [[test-architecture]]
- [[test-data-management]]
