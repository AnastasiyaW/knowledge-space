---
title: "Python et Node.js en ligne de commande"
category: reference
tags: [linux-cli, python, nodejs, pip, npm, venv, cli]
level: 3
source_sha256: 08328f86980a665b7de581671bf1850793e6252c4c2ccd8acdc0836256b2a579
translation: machine
translated_at: '2026-10-24'
---
# Python et Node.js en ligne de commande {#python-and-nodejs-cli}

Installation et exécution de Python et Node.js depuis la ligne de commande, gestion des paquets avec pip/npm, utilisation des environnements virtuels et gestion des versions.

## Python {#python}

### Installation {#installation}

```bash
# Linux (Debian/Ubuntu)
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Verify
python3 --version
pip3 --version
```

Windows : télécharger depuis python.org et cocher « Add Python to PATH ». Vous pouvez aussi l'installer depuis le Microsoft Store.

### Exécuter Python {#running-python}

```bash
python3                         # interactive REPL
python3 script.py               # run script
python3 -c "print('hello')"    # inline command
python3 -m http.server          # run module

# Windows
py script.py                    # Windows launcher
py -3.11 script.py              # specific version
```

### pip - Gestionnaire de paquets {#pip-package-manager}

```bash
pip install requests            # install
pip install requests==2.31.0    # specific version
pip install -r requirements.txt # from requirements file
pip uninstall requests
pip list                        # installed packages
pip show requests               # package info
pip freeze > requirements.txt   # save current packages
pip install --upgrade pip       # upgrade pip itself
```

### Environnements virtuels {#virtual-environments}

```bash
python3 -m venv .venv           # create
source .venv/bin/activate       # activate (Linux/macOS)
.venv\Scripts\activate          # activate (Windows cmd)

# After activation: prompt shows (.venv)
pip install package             # installs only in venv
deactivate                      # exit venv
```

### uv - Alternative rapide {#uv-fast-alternative}

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv                         # create venv
uv pip install requests         # 10-100x faster than pip
uv run script.py                # run without activating
```

### Shebang pour les scripts {#shebang-for-scripts}

```python
#!/usr/bin/env python3
```

```bash
chmod +x script.py && ./script.py
```

### Variables d'environnement {#environment-variables}

```bash
MY_VAR=hello python3 script.py  # pass for single run
export MY_VAR=hello             # export to session
```

```python
import os
value = os.environ.get("MY_VAR", "default")
```

## Node.js {#nodejs}

### Installation {#installation_1}

```bash
# Via NodeSource (recommended)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install nodejs

# Via nvm (version manager)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install --lts
nvm use 20
nvm alias default 20
```

Windows : télécharger depuis nodejs.org ou utiliser nvm-windows.

### Exécuter Node.js {#running-nodejs}

```bash
node                    # REPL
node script.js          # run script
node -e "console.log('hi')"  # inline
```

### npm - Gestionnaire de paquets {#npm-package-manager}

```bash
npm init -y                     # create package.json
npm install express             # add dependency
npm install -D jest             # devDependency
npm install                     # install all from package.json
npm install -g nodemon          # install globally
npm uninstall express
npm list                        # local packages
npm list -g                     # global packages
npm outdated                    # show outdated
npm update                      # update packages
npm run dev                     # run script from package.json
npx create-react-app my-app    # run without installing
```

### Scripts package.json {#packagejson-scripts}

```json
{
  "scripts": {
    "start": "node server.js",
    "dev": "nodemon server.js",
    "test": "jest",
    "build": "tsc"
  }
}
```

## Comparaison {#comparison}

| Tâche | Python | Node.js |
|------|--------|---------|
| Exécuter un script | `python3 script.py` | `node script.js` |
| REPL | `python3` | `node` |
| Gestionnaire de paquets | `pip` | `npm` / `yarn` / `pnpm` |
| Fichier de paquets | `requirements.txt` / `pyproject.toml` | `package.json` |
| Gestionnaire de versions | `pyenv` / `uv` | `nvm` |
| Environnement virtuel | `python3 -m venv` | node_modules par projet |
| Exécuter sans installer | `python3 -m module` | `npx package` |

## Pièges courants {#gotchas}

- `pip install` sans venv installe les paquets à l'échelle du système : utilisez toujours des environnements virtuels
- `nvm` dépend du shell : redémarrez le terminal après l'installation
- `npm install -g` peut nécessiter `sudo` sous Linux (ou corriger le préfixe npm)
- Python `python` ou `python3` : sur certains systèmes, `python` correspond à Python 2
- `npx` télécharge et exécute des paquets : risque de sécurité si le nom du paquet est un typosquatting
- La version de Node.js a une importance notable : utilisez la version LTS en production

## Voir aussi {#see-also}

- [[package-management]] - Gestionnaires de paquets système (apt, yum)
- [[bash-scripting]] - Scripts shell
- [[terminal-basics]] - Fondamentaux du shell
