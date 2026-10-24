---
title: "Projekteinrichtung und Tooling"
category: concepts
tags: [python, pip, venv, pep8, virtual-environments, packaging, ide]
level: 3
source_sha256: 845fac6c5b7ce3568c0f388af7c0dcef68cad017a5b93ef1da6320d9226892f1
translation: machine
translated_at: '2026-10-24'
---
# Projekteinrichtung und Tooling {#project-setup-and-tooling}

Die Einrichtung eines Python-Projekts umfasst die Wahl einer IDE, die Verwaltung von Abhängigkeiten mit virtuellen Umgebungen und die Einhaltung der Stilkonventionen von PEP 8. Zum modernen Tooling gehören pip, venv, poetry und Typprüfer wie mypy.

## Kernfakten {#key-facts}

- Immer virtuelle Umgebungen verwenden, um Projektabhängigkeiten zu isolieren
- PEP 8: 4 Leerzeichen Einrückung, `snake_case` für Funktionen/Variablen, `PascalCase` für Klassen
- `requirements.txt` fixiert exakte Versionen für Reproduzierbarkeit
- `pyproject.toml` ist der moderne Standard für die Projektkonfiguration
- Drei Stufen von IDEs: Texteditoren (VS Code), vollwertige IDEs (PyCharm), Notebooks (Jupyter)
- `python -m venv` ist integriert; `poetry` und `pipenv` sind übergeordnete Alternativen

## Muster {#patterns}

### Virtuelle Umgebungen {#virtual-environments}
```bash
python -m venv myenv              # create
source myenv/bin/activate         # activate (Linux/Mac)
myenv\Scripts\activate            # activate (Windows)
pip install package               # install in venv
deactivate                        # exit

pip freeze > requirements.txt     # save dependencies
pip install -r requirements.txt   # install from file
```

### Paketverwaltung {#package-management}
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

### PEP 8 Stilrichtlinie {#pep-8-style-guide}
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

### Python-Code ausführen {#running-python-code}
```bash
# Script
python my_script.py

# Module
python -m pytest
python -m http.server 8000

# Interactive REPL
python
```

### Entwicklungsumgebungen {#development-environments}

| Werkzeug | Typ | Geeignet für |
|----------|-----|--------------|
| VS Code | Editor + Erweiterungen | Allgemeine Entwicklung, leichtgewichtig |
| PyCharm | Vollwertige IDE | Python-spezifische Funktionen, Debugging |
| Jupyter | Notebook | Datenexploration, Lernen, Prototyping |

### Werkzeuge zur Abhängigkeitsverwaltung {#dependency-management-tools}

| Werkzeug | Lock-Datei | Resolver | Virtuelle Umgebung |
|----------|------------|----------|--------------------|
| pip + venv | requirements.txt | Basic | Manuell |
| pipenv | Pipfile.lock | Ja | Automatisch |
| poetry | poetry.lock | Ja | Automatisch |
| uv | uv.lock | Ja | Automatisch |

### Python-Installation {#python-installation}

- **Anaconda/Miniconda** - enthält wissenschaftliche Pakete (NumPy, pandas, Jupyter)
- **python.org** - Standard-Installationsprogramm
- **pyenv** - Verwaltung mehrerer Python-Versionen

## Fallstricke {#gotchas}

- Ohne virtuelle Umgebung wirkt sich `pip install` auf das systemweite Python aus - das kann Betriebssystem-Werkzeuge beschädigen
- `pip freeze` erfasst ALLE installierten Pakete einschließlich transitiver Abhängigkeiten - für eine saubere Verwaltung der Abhängigkeiten `pip-compile` verwenden
- Das Standard-Python unter macOS/Linux kann Python 2 sein - `python3` explizit verwenden
- `requirements.txt` bildet den Abhängigkeitsbaum nicht ab - poetry.lock/Pipfile.lock tun dies
- VS Code benötigt die installierte Python-Erweiterung für IntelliSense, Linting und Debugging

## Siehe auch {#see-also}

- [[type-hints]] - mypy, statische Typprüfung
- [[testing-with-pytest]] - Testkonfiguration
- [[fastapi-deployment]] - Docker, Produktionsaufbau
