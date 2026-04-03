---
title: Project Setup and Tooling
category: concepts
tags: [python, pip, venv, pep8, virtual-environments, packaging, ide]
---

# Project Setup and Tooling

Python project setup involves choosing an IDE, managing dependencies with virtual environments, and following PEP 8 style conventions. Modern tooling includes pip, venv, poetry, and type checkers like mypy.

## Key Facts

- Always use virtual environments to isolate project dependencies
- PEP 8: 4-space indent, `snake_case` for functions/variables, `PascalCase` for classes
- `requirements.txt` pins exact versions for reproducibility
- `pyproject.toml` is the modern project configuration standard
- Three IDE tiers: text editors (VS Code), full IDEs (PyCharm), notebooks (Jupyter)
- `python -m venv` is built-in; `poetry` and `pipenv` are higher-level alternatives

## Patterns

### Virtual Environments
```bash
python -m venv myenv              # create
source myenv/bin/activate         # activate (Linux/Mac)
myenv\Scripts\activate            # activate (Windows)
pip install package               # install in venv
deactivate                        # exit

pip freeze > requirements.txt     # save dependencies
pip install -r requirements.txt   # install from file
```

### Package Management
```bash
# pip (standard)
pip install fastapi uvicorn sqlalchemy
pip install -r requirements.txt

# poetry (modern)
poetry init
poetry add fastapi uvicorn
poetry install

# pipenv
pipenv install fastapi
pipenv shell
```

### PEP 8 Style Guide
```python
# Naming
my_variable = 42             # snake_case for variables/functions
MY_CONSTANT = 3.14           # UPPER_CASE for constants
class MyClass:               # PascalCase for classes
    pass

# Formatting
x = 1                        # spaces around operators
some_list[0]                 # no space before brackets
my_dict['key']               # no space before brackets

# Line length: max 79 (PEP 8) or 120 (modern projects)
# Imports: one per line, at top of file
# Order: stdlib, third-party, local
import os
import sys

import requests
from sqlalchemy import select

from myapp.models import User
```

### Running Python Code
```bash
# Script
python my_script.py

# Module
python -m pytest
python -m http.server 8000

# Interactive REPL
python
```

### Development Environments

| Tool | Type | Best For |
|------|------|----------|
| VS Code | Editor + extensions | General development, lightweight |
| PyCharm | Full IDE | Python-specific features, debugging |
| Jupyter | Notebook | Data exploration, learning, prototyping |

### Dependency Management Tools

| Tool | Lock file | Resolver | Virtual env |
|------|-----------|----------|-------------|
| pip + venv | requirements.txt | Basic | Manual |
| pipenv | Pipfile.lock | Yes | Automatic |
| poetry | poetry.lock | Yes | Automatic |
| uv | uv.lock | Yes | Automatic |

### Python Installation

- **Anaconda/Miniconda** - includes scientific packages (NumPy, pandas, Jupyter)
- **python.org** - standard installer
- **pyenv** - manage multiple Python versions

## Gotchas

- Without virtual env, `pip install` affects system Python - can break OS tools
- `pip freeze` captures ALL installed packages including transitive deps - use `pip-compile` for clean dependency management
- Default Python on macOS/Linux may be Python 2 - use `python3` explicitly
- `requirements.txt` doesn't capture dependency tree - poetry.lock/Pipfile.lock do
- VS Code needs the Python extension installed for IntelliSense, linting, debugging

## See Also

- [[type-hints]] - mypy, static type checking
- [[testing-with-pytest]] - test configuration
- [[fastapi-deployment]] - Docker, production setup
