---
title: Test Parallelization
category: patterns
tags: [pytest-xdist, parallel, concurrency, test-isolation, performance, scaling]
---

# Test Parallelization

Running tests in parallel with pytest-xdist. Reduces suite execution time proportionally to worker count - but requires test isolation.

## pytest-xdist Setup

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

## Distribution Modes

| Mode | Behavior | Best for |
|------|----------|----------|
| `load` (default) | Round-robin to available workers | Independent tests |
| `loadfile` | All tests from same file go to same worker | Tests sharing module-level fixtures |
| `loadgroup` | Tests with same `@pytest.mark.xdist_group` go to same worker | Tests sharing resources |
| `loadscope` | Group by module/class | Module-scoped fixtures |

## Grouping Dependent Tests

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

Run with `pytest -n 4 --dist loadgroup` - these three run on same worker in order.

## Fixture Scoping with xdist

Session-scoped fixtures are per-worker, not per-run:

```python
@pytest.fixture(scope="session")
def db_connection():
    # Each xdist worker gets its own connection
    conn = connect_db()
    yield conn
    conn.close()
```

For truly shared state across workers, use `tmp_path_factory` or file locks:

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

## Worker-Aware Database Isolation

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

## Performance Measurement

```bash
# Sequential baseline
time pytest tests/ -v
# 120 seconds

# Parallel with 4 workers
time pytest tests/ -n 4 -v
# 35 seconds
```

Speedup depends on test independence and I/O patterns. CPU-bound tests scale linearly. I/O-bound tests (API calls, DB) scale super-linearly due to overlap.

## Marks for Sequential Tests

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

## Gotchas

- **Issue:** Tests pass in sequence but fail with xdist - shared mutable state (global variables, files, database rows). **Fix:** Each test must create its own data. Use unique identifiers per worker: `f"user_{worker_id}_{uuid4()}"`.

- **Issue:** Session fixtures run multiple times (once per worker), causing expensive setup to repeat. **Fix:** Use file-based locking (`filelock` package) for one-time setup. Or use `loadscope` distribution.

- **Issue:** `-n auto` on CI with many cores spawns too many workers, overwhelming the database. **Fix:** Set explicit worker count matching available resources: `-n 4` not `-n auto`. Monitor DB connection count.

## See Also

- [[pytest-fundamentals]]
- [[pytest-fixtures-advanced]]
- [[ci-cd-test-automation]]
