---
title: "Python und Node.js CLI"
category: reference
tags: [linux-cli, python, nodejs, pip, npm, venv, cli]
level: 3
source_sha256: 08328f86980a665b7de581671bf1850793e6252c4c2ccd8acdc0836256b2a579
translation: machine
translated_at: '2026-10-24'
---
# Python und Node.js CLI {#python-and-nodejs-cli}

Installation und Ausführung von Python und Node.js über die Kommandozeile, Verwaltung von Paketen mit pip/npm, Nutzung virtueller Umgebungen und Versionsverwaltung.

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

Windows: Von python.org herunterladen und "Add Python to PATH" aktivieren. Alternativ aus dem Microsoft Store installieren.

### Python ausführen {#running-python}

```bash
python3                         # interactive REPL
python3 script.py               # run script
python3 -c "print('hello')"    # inline command
python3 -m http.server          # run module

# Windows
py script.py                    # Windows launcher
py -3.11 script.py              # specific version
```

### pip - Paketmanager {#pip-package-manager}

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

### Virtuelle Umgebungen {#virtual-environments}

```bash
python3 -m venv .venv           # create
source .venv/bin/activate       # activate (Linux/macOS)
.venv\Scripts\activate          # activate (Windows cmd)

# After activation: prompt shows (.venv)
pip install package             # installs only in venv
deactivate                      # exit venv
```

### uv - Schnelle Alternative {#uv-fast-alternative}

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv                         # create venv
uv pip install requests         # 10-100x faster than pip
uv run script.py                # run without activating
```

### Shebang für Skripte {#shebang-for-scripts}

```python
#!/usr/bin/env python3
```

```bash
chmod +x script.py && ./script.py
```

### Umgebungsvariablen {#environment-variables}

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

Windows: Von nodejs.org herunterladen oder nvm-windows verwenden.

### Node.js ausführen {#running-nodejs}

```bash
node                    # REPL
node script.js          # run script
node -e "console.log('hi')"  # inline
```

### npm - Paketmanager {#npm-package-manager}

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

### package.json-Skripte {#packagejson-scripts}

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

## Vergleich {#comparison}

| Aufgabe | Python | Node.js |
|------|--------|---------|
| Skript ausführen | `python3 script.py` | `node script.js` |
| REPL | `python3` | `node` |
| Paketmanager | `pip` | `npm` / `yarn` / `pnpm` |
| Paketdatei | `requirements.txt` / `pyproject.toml` | `package.json` |
| Versionsverwaltung | `pyenv` / `uv` | `nvm` |
| Virtuelle Umgebung | `python3 -m venv` | node_modules pro Projekt |
| Ohne Installation ausführen | `python3 -m module` | `npx package` |

## Stolperfallen {#gotchas}

- `pip install` ohne venv installiert systemweit - immer virtuelle Umgebungen verwenden
- `nvm` ist shell-spezifisch; nach der Installation das Terminal neu starten
- `npm install -g` benötigt unter Linux eventuell `sudo` (oder das npm-Präfix anpassen)
- Python `python` vs. `python3`: Auf manchen Systemen ist `python` Python 2
- `npx` lädt Pakete herunter und führt sie aus - Sicherheitsrisiko, wenn der Paketname ein Typosquatting-Ziel ist
- Die Node.js-Version ist wichtig - für Produktivsysteme LTS verwenden

## Siehe auch {#see-also}

- [[package-management]] - Systempaketmanager (apt, yum)
- [[bash-scripting]] - Shell-Skripting
- [[terminal-basics]] - Grundlagen der Shell
