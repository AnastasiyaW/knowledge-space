---
title: Pytest Plugins and Parallel Execution
category: framework
tags: [pytest, xdist, parallel, plugins, pytest-html, pytest-rerunfailures]
---
# Pytest Plugins and Parallel Execution

Extending pytest with plugins for parallel execution, reporting, retries, and more.

## Key Facts

- `pytest-xdist` - parallel test execution across multiple CPUs or machines
- `pytest -n auto` - distribute tests across all available CPU cores
- `pytest -n 4` - run on 4 workers specifically
- `pytest-rerunfailures` - auto-retry flaky tests: `pytest --reruns 3 --reruns-delay 2`
- `pytest-html` - generate HTML test reports
- `pytest-timeout` - enforce time limits: `@pytest.mark.timeout(30)`
- `pytest-ordering` - control test execution order
- `pytest-env` - set environment variables from pytest config
- Plugin discovery: `pip install pytest-*`, auto-registered via entry points
- `conftest.py` hooks: `pytest_configure`, `pytest_collection_modifyitems`, `pytest_runtest_makereport`

## Patterns

```python
# Install and use xdist
# pip install pytest-xdist
# pytest -n auto tests/

# Handle parallel conflicts with fixtures
import pytest
import filelock

@pytest.fixture(scope="session")
def shared_resource(tmp_path_factory):
    """Thread-safe shared resource for parallel tests."""
    root = tmp_path_factory.getbasetemp().parent
    lock = root / "resource.lock"
    data_file = root / "data.json"

    with filelock.FileLock(str(lock)):
        if not data_file.exists():
            # First worker creates the resource
            setup_shared_data(data_file)
    return data_file

# Mark test for rerun on failure
# pip install pytest-rerunfailures
@pytest.mark.flaky(reruns=3, reruns_delay=2)
def test_external_api():
    response = requests.get("https://api.example.com/health")
    assert response.status_code == 200

# pytest-timeout
@pytest.mark.timeout(10)
def test_slow_operation():
    result = long_running_function()
    assert result is not None

# Custom plugin in conftest.py
def pytest_collection_modifyitems(config, items):
    """Put smoke tests first."""
    smoke = [i for i in items if "smoke" in i.keywords]
    rest = [i for i in items if "smoke" not in i.keywords]
    items[:] = smoke + rest

# Hook for screenshot on failure (UI tests)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("browser")
        if driver:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="failure_screenshot",
                attachment_type=allure.attachment_type.PNG
            )

# pytest.ini for plugins config
# [pytest]
# addopts = -n auto --timeout=60 --reruns=2
# timeout_method = signal
```

## Gotchas

- **Symptom**: tests fail only when running in parallel - **Cause**: shared mutable state (database, files, global variables) - **Fix**: use unique test data per worker, `filelock` for shared resources, or `tmp_path`
- **Symptom**: fixtures run multiple times with xdist - **Cause**: session-scoped fixtures run once per worker, not once globally - **Fix**: use `filelock` pattern for truly global setup
- **Symptom**: test order matters (passes alone, fails in suite) - **Cause**: test isolation violation - **Fix**: each test must set up and clean up its own state
- `-n auto` on CI may use too many cores - specify exact count with `-n 4`

## See Also

- [[pytest-fundamentals]] - core pytest features
- [[ci-cd-test-automation]] - running parallel tests in CI
- [[allure-reporting]] - advanced reporting
- [pytest-xdist docs](https://pytest-xdist.readthedocs.io/)
- [pytest plugins list](https://docs.pytest.org/en/stable/reference/plugin_list.html)
