---
title: "Configuration du projet et outillage"
category: concepts
tags: [python, pip, venv, pep8, virtual-environments, packaging, ide]
level: 3
source_sha256: 845fac6c5b7ce3568c0f388af7c0dcef68cad017a5b93ef1da6320d9226892f1
translation: machine
translated_at: '2026-10-24'
---
# Configuration du projet et outillage {#project-setup-and-tooling}

La configuration d'un projet Python implique de choisir un IDE, de gérer les dépendances avec des environnements virtuels et de suivre les conventions de style PEP 8. L'outillage moderne comprend pip, venv, poetry et des vérificateurs de types comme mypy.

## Faits clés {#key-facts}

- Utiliser systématiquement des environnements virtuels pour isoler les dépendances du projet
- PEP 8 : indentation de 4 espaces, `snake_case` pour les fonctions et variables, `PascalCase` pour les classes
- `requirements.txt` fige les versions exactes pour garantir la reproductibilité
- `pyproject.toml` est le standard moderne de configuration des projets
- Trois niveaux d'IDE : éditeurs de texte (VS Code), IDE complets (PyCharm), notebooks (Jupyter)
- `python -m venv` est intégré à Python ; `poetry` et `pipenv` sont des alternatives de plus haut niveau

## Modèles {#patterns}

### Environnements virtuels {#virtual-environments}
```bash
python -m venv myenv              # create
source myenv/bin/activate         # activate (Linux/Mac)
myenv\Scripts\activate            # activate (Windows)
pip install package               # install in venv
deactivate                        # exit

pip freeze > requirements.txt     # save dependencies
pip install -r requirements.txt   # install from file
```

### Gestion des paquets {#package-management}
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

### Guide de style PEP 8 {#pep-8-style-guide}
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

### Exécution de code Python {#running-python-code}
```bash
# Script
python my_script.py

# Module
python -m pytest
python -m http.server 8000

# Interactive REPL
python
```

### Environnements de développement {#development-environments}

| Outil | Type | Idéal pour |
|-------|------|------------|
| VS Code | Éditeur + extensions | Développement général, léger |
| PyCharm | IDE complet | Fonctionnalités spécifiques à Python, débogage |
| Jupyter | Notebook | Exploration de données, apprentissage, prototypage |

### Outils de gestion des dépendances {#dependency-management-tools}

| Outil | Fichier de verrouillage | Résolveur | Environnement virtuel |
|-------|-------------------------|-----------|------------------------|
| pip + venv | requirements.txt | Basique | Manuel |
| pipenv | Pipfile.lock | Oui | Automatique |
| poetry | poetry.lock | Oui | Automatique |
| uv | uv.lock | Oui | Automatique |

### Installation de Python {#python-installation}

- **Anaconda/Miniconda** - inclut les paquets scientifiques (NumPy, pandas, Jupyter)
- **python.org** - installateur standard
- **pyenv** - gestion de plusieurs versions de Python

## Pièges {#gotchas}

- Sans environnement virtuel, `pip install` affecte le Python du système, ce qui peut casser les outils du système d'exploitation
- `pip freeze` capture TOUS les paquets installés, y compris les dépendances transitives ; utiliser `pip-compile` pour une gestion propre des dépendances
- Le Python par défaut sur macOS/Linux peut être Python 2 ; utiliser explicitement `python3`
- `requirements.txt` ne capture pas l'arbre des dépendances, contrairement à poetry.lock et Pipfile.lock
- VS Code nécessite l'installation de l'extension Python pour IntelliSense, le linting et le débogage

## Voir aussi {#see-also}

- [[type-hints]] - mypy, vérification statique des types
- [[testing-with-pytest]] - configuration des tests
- [[fastapi-deployment]] - Docker, configuration de production
