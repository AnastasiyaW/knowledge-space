---
title: Test Project Structure
category: methodology
tags: [project-structure, architecture, dependencies, gitignore, requirements, best-practices]
---
# Test Project Structure

Organizing test automation projects - directory layout, dependency management, configuration, CI readiness.

## Key Facts

- Separate `tests/` directory from application code; further split by test type (api, ui, unit)
- `conftest.py` hierarchy: root for session fixtures, subdirs for scope-specific fixtures
- `requirements.txt` or `pyproject.toml` for pinned dependencies - critical for CI reproducibility
- `.env` files per environment: `.env.dev`, `.env.staging`, `.env.prod` - never committed to Git
- `.gitignore`: exclude `__pycache__`, `.pytest_cache`, `allure-results/`, `.env`, `venv/`
- `pytest.ini` or `pyproject.toml [tool.pytest.ini_options]` for test configuration
- README.md with setup instructions, run commands, project description
- Page objects, API clients, utilities in separate packages from tests
- Git workflow: one commit per task, descriptive messages, PRs for review

## Patterns

```
project-root/
|-- .github/
|   |-- workflows/
|       |-- tests.yml              # CI pipeline
|-- clients/                       # API client classes
|   |-- __init__.py
|   |-- base_client.py
|   |-- users_client.py
|   |-- courses_client.py
|-- pages/                         # Page objects (UI tests)
|   |-- __init__.py
|   |-- base_page.py
|   |-- login_page.py
|   |-- dashboard_page.py
|-- models/                        # Pydantic models
|   |-- __init__.py
|   |-- user.py
|   |-- course.py
|-- tools/                         # Utilities
|   |-- assertions/
|   |   |-- base.py
|   |   |-- api_assertions.py
|   |-- data_generators.py
|   |-- logger.py
|-- tests/
|   |-- conftest.py                # Root fixtures
|   |-- api/
|   |   |-- conftest.py            # API-specific fixtures
|   |   |-- test_users.py
|   |   |-- test_courses.py
|   |-- ui/
|       |-- conftest.py            # UI-specific fixtures (browser)
|       |-- test_login.py
|       |-- test_dashboard.py
|-- .env                           # Local config (gitignored)
|-- .env.example                   # Template for .env
|-- .gitignore
|-- pytest.ini
|-- requirements.txt
|-- README.md
```

```ini
# pytest.ini
[pytest]
testpaths = tests
markers =
    smoke: smoke tests
    regression: full regression
    api: API tests
    ui: UI tests
addopts = -v --tb=short
log_cli = true
log_cli_level = INFO
```

```text
# .gitignore for test projects
__pycache__/
*.pyc
.pytest_cache/
allure-results/
allure-report/
.env
venv/
.venv/
*.log
screenshots/
trace.zip
htmlcov/
.coverage
```

```text
# requirements.txt
pytest==8.0.0
pytest-xdist==3.5.0
allure-pytest==2.13.2
requests==2.31.0
httpx==0.27.0
pydantic==2.6.0
pydantic-settings==2.1.0
faker==22.0.0
playwright==1.41.0
python-dotenv==1.0.0
```

```python
# conftest.py - root level
import pytest
from config import Settings

@pytest.fixture(scope="session")
def settings():
    return Settings()

@pytest.fixture(scope="session")
def api_client(settings):
    from clients.users_client import UsersClient
    return UsersClient(settings.base_url, settings.api_token)
```

## Gotchas

- **Symptom**: imports fail in tests - **Cause**: missing `__init__.py` in packages or wrong Python path - **Fix**: add `__init__.py` to all packages, or configure `pythonpath` in `pytest.ini`
- **Symptom**: different results on different machines - **Cause**: unpinned dependencies - **Fix**: always pin exact versions in `requirements.txt` (`pip freeze > requirements.txt`)
- **Symptom**: `.env` changes not picked up - **Cause**: cached settings - **Fix**: restart test session, or create new Settings instance
- Keep test project "production ready" - clean, documented, CI-integrated - it represents your engineering quality
- `conftest.py` is NOT for test functions - only fixtures, hooks, and plugins

## See Also

- [[pytest-fundamentals]] - pytest configuration options
- [[ci-cd-test-automation]] - CI pipeline setup
- [[pydantic-test-validation]] - settings management
- [[allure-reporting]] - report generation setup
