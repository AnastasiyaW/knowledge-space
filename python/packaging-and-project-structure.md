---
title: Packaging and Project Structure
category: reference
tags: [python, packaging, pyproject-toml, virtual-environments, pip, poetry, uv, project-structure]
---

# Packaging and Project Structure

Modern Python projects use `pyproject.toml` as the single source of truth for metadata, dependencies, and build configuration. Virtual environments isolate project dependencies. Tools like `uv`, `poetry`, and `pip-tools` manage dependency resolution and locking.

## Key Facts

- `pyproject.toml` (PEP 518, PEP 621) replaces `setup.py`, `setup.cfg`, and `requirements.txt` for project metadata
- Virtual environments: `python -m venv .venv` creates an isolated environment; activate with `source .venv/bin/activate`
- `uv` is a fast Rust-based Python package manager (pip + venv replacement) with lockfile support
- `pip install -e .` (editable install) links the project into the environment for development
- `__init__.py` marks a directory as a Python package; can be empty or contain package-level exports
- `src/` layout (src-layout) prevents accidental imports from the project root during testing
- `requirements.txt` for pinned dependencies; `requirements-dev.txt` for dev tools
- `__main__.py` makes a package executable with `python -m package_name`
- See [[testing-with-pytest]] for test directory structure, [[docker-deployment]] for containerized builds

## Patterns

### Modern `pyproject.toml`

```toml
[project]
name = "myapp"
version = "1.0.0"
description = "My FastAPI application"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.100",
    "uvicorn[standard]>=0.23",
    "sqlalchemy[asyncio]>=2.0",
    "pydantic>=2.0",
    "httpx>=0.24",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-asyncio>=0.21",
    "pytest-cov>=4.0",
    "mypy>=1.0",
    "ruff>=0.1",
]

[project.scripts]
myapp = "myapp.cli:main"

[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.build_meta"

[tool.ruff]
target-version = "py311"
line-length = 100
select = ["E", "F", "I", "N", "W", "UP"]

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"

[tool.mypy]
python_version = "3.11"
strict = true
```

### Standard Project Layout

```
myapp/
  pyproject.toml
  README.md
  .env.example
  src/
    myapp/
      __init__.py
      __main__.py        # python -m myapp
      main.py            # FastAPI app
      config.py          # settings (pydantic-settings)
      models/
        __init__.py
        user.py
        order.py
      routers/
        __init__.py
        users.py
        items.py
      services/
        __init__.py
        user_service.py
      repositories/
        __init__.py
        user_repo.py
      schemas/
        __init__.py
        user.py           # Pydantic models
      deps.py             # FastAPI dependencies
  tests/
    __init__.py
    conftest.py           # shared fixtures
    test_users.py
    test_items.py
  alembic/
    env.py
    versions/
  Dockerfile
  docker-compose.yml
```

### Flat Layout (Simpler Projects)

```
myapp/
  pyproject.toml
  myapp/
    __init__.py
    main.py
    models.py
    routes.py
  tests/
    test_main.py
```

### Virtual Environment Management

```bash
# Standard venv
python -m venv .venv
source .venv/bin/activate    # Linux/Mac
.venv\Scripts\activate       # Windows
pip install -e ".[dev]"

# uv (faster alternative)
uv venv
uv pip install -e ".[dev]"
uv pip compile pyproject.toml -o requirements.lock
uv pip sync requirements.lock

# Poetry
poetry init
poetry add fastapi uvicorn
poetry add --group dev pytest mypy
poetry install
poetry lock
```

### `__init__.py` for Package Exports

```python
# myapp/__init__.py
from myapp.main import app
from myapp.config import settings

__version__ = "1.0.0"
__all__ = ["app", "settings"]
```

### Entry Points and CLI

```python
# myapp/cli.py
import argparse

def main():
    parser = argparse.ArgumentParser(description="My App CLI")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    import uvicorn
    uvicorn.run("myapp.main:app", host="0.0.0.0", port=args.port, reload=True)

# myapp/__main__.py
from myapp.cli import main
main()

# Now works as:
# python -m myapp --port 9000
# myapp --port 9000  (via [project.scripts])
```

## Gotchas

- **Relative imports in scripts**: `from .models import User` fails when running a file directly (`python myapp/routes.py`). Always run as a module (`python -m myapp.routes`) or use the installed package
- **`src/` layout gotcha**: with src-layout, `import myapp` fails without `pip install -e .` because `src/` is not on `sys.path` by default. This is intentional -- forces you to install the package properly
- **`requirements.txt` does not lock transitive deps**: `fastapi>=0.100` installs the latest, which may pull different sub-dependencies across environments. Use `pip-compile` or `uv pip compile` for full lockfiles
- **Circular imports**: `models.py` imports from `services.py` which imports from `models.py` -- `ImportError`. Break cycles by importing inside functions, using `TYPE_CHECKING`, or restructuring modules
- **`__all__` does not restrict imports**: `__all__` only affects `from module import *`. Direct imports (`from module import private_func`) still work

## See Also

- [Python Packaging User Guide](https://packaging.python.org/)
- [PEP 621 -- Storing project metadata in pyproject.toml](https://peps.python.org/pep-0621/)
- [[testing-with-pytest]] - test directory structure and conftest.py
- [[docker-deployment]] - multi-stage Docker builds
