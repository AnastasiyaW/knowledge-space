---
title: "Parallélisation des tests"
category: patterns
tags: [pytest-xdist, parallel, concurrency, test-isolation, performance, scaling]
level: 3
source_sha256: 35899b2f16d4418d3b1f7d7db89c873e8a598713b31d79686daa218f36239963
translation: machine
translated_at: '2026-10-24'
---
# Parallélisation des tests {#test-parallelization}

Exécution des tests en parallèle avec pytest-xdist. Réduit le temps d'exécution de la suite proportionnellement au nombre de workers, mais nécessite une isolation des tests.

## Configuration de pytest-xdist {#pytest-xdist-setup}

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

## Modes de distribution {#distribution-modes}

| Mode | Comportement | Idéal pour |
|------|--------------|------------|
| `load` (par défaut) | Répartition en round-robin entre les workers disponibles | Tests indépendants |
| `loadfile` | Tous les tests d'un même fichier vont au même worker | Tests partageant des fixtures de niveau module |
| `loadgroup` | Les tests ayant le même `@pytest.mark.xdist_group` vont au même worker | Tests partageant des ressources |
| `loadscope` | Regroupement par module/classe | Fixtures de scope module |

## Regroupement des tests dépendants {#grouping-dependent-tests}

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

Lancer avec `pytest -n 4 --dist loadgroup` : ces trois tests s'exécutent sur le même worker, dans l'ordre.

## Scope des fixtures avec xdist {#fixture-scoping-with-xdist}

Les fixtures de scope session sont propres à chaque worker, et non à l'exécution complète :

```python
@pytest.fixture(scope="session")
def db_connection():
    # Each xdist worker gets its own connection
    conn = connect_db()
    yield conn
    conn.close()
```

Pour un état réellement partagé entre les workers, utiliser `tmp_path_factory` ou des verrous de fichiers :

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

## Isolation de la base de données par worker {#worker-aware-database-isolation}

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

## Mesure de la performance {#performance-measurement}

```bash
# Sequential baseline
time pytest tests/ -v
# 120 seconds

# Parallel with 4 workers
time pytest tests/ -n 4 -v
# 35 seconds
```

Le gain dépend de l'indépendance des tests et des schémas d'E/S. Les tests liés au CPU passent à l'échelle de façon linéaire. Les tests liés aux E/S (appels API, base de données) passent à l'échelle de façon super-linéaire grâce au recouvrement des opérations.

## Marqueurs pour les tests séquentiels {#marks-for-sequential-tests}

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

## Pièges {#gotchas}

- **Problème :** les tests réussissent en séquentiel mais échouent avec xdist. Cause : état mutable partagé (variables globales, fichiers, lignes de base de données). **Correctif :** chaque test doit créer ses propres données. Utiliser des identifiants uniques par worker : `f"user_{worker_id}_{uuid4()}"`.

- **Problème :** les fixtures de session s'exécutent plusieurs fois (une fois par worker), ce qui répète une initialisation coûteuse. **Correctif :** utiliser un verrouillage par fichier (paquet `filelock`) pour l'initialisation unique. Ou utiliser la distribution `loadscope`.

- **Problème :** `-n auto` sur une CI disposant de nombreux cœurs lance trop de workers et surcharge la base de données. **Correctif :** définir un nombre de workers explicite adapté aux ressources disponibles : `-n 4` plutôt que `-n auto`. Surveiller le nombre de connexions à la base de données.

## Voir aussi {#see-also}

- [[pytest-fundamentals]]
- [[pytest-fixtures-advanced]]
- [[ci-cd-test-automation]]
