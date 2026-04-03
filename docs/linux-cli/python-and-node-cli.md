---
title: Python and Node.js CLI
category: reference
tags: [linux-cli, python, nodejs, pip, npm, venv, cli]
---

# Python and Node.js CLI

Installing and running Python and Node.js from the command line, managing packages with pip/npm, using virtual environments, and version management.

## Python

### Installation

```bash
# Linux (Debian/Ubuntu)
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Verify
python3 --version
pip3 --version
```

Windows: download from python.org, check "Add Python to PATH". Or install from Microsoft Store.

### Running Python

```bash
python3                         # interactive REPL
python3 script.py               # run script
python3 -c "print('hello')"    # inline command
python3 -m http.server          # run module

# Windows
py script.py                    # Windows launcher
py -3.11 script.py              # specific version
```

### pip - Package Manager

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

### Virtual Environments

```bash
python3 -m venv .venv           # create
source .venv/bin/activate       # activate (Linux/macOS)
.venv\Scripts\activate          # activate (Windows cmd)

# After activation: prompt shows (.venv)
pip install package             # installs only in venv
deactivate                      # exit venv
```

### uv - Fast Alternative

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv                         # create venv
uv pip install requests         # 10-100x faster than pip
uv run script.py                # run without activating
```

### Shebang for Scripts

```python
#!/usr/bin/env python3
```

```bash
chmod +x script.py && ./script.py
```

### Environment Variables

```bash
MY_VAR=hello python3 script.py  # pass for single run
export MY_VAR=hello             # export to session
```

```python
import os
value = os.environ.get("MY_VAR", "default")
```

## Node.js

### Installation

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

Windows: download from nodejs.org or use nvm-windows.

### Running Node.js

```bash
node                    # REPL
node script.js          # run script
node -e "console.log('hi')"  # inline
```

### npm - Package Manager

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

### package.json Scripts

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

## Comparison

| Task | Python | Node.js |
|------|--------|---------|
| Run script | `python3 script.py` | `node script.js` |
| REPL | `python3` | `node` |
| Package manager | `pip` | `npm` / `yarn` / `pnpm` |
| Package file | `requirements.txt` / `pyproject.toml` | `package.json` |
| Version manager | `pyenv` / `uv` | `nvm` |
| Virtual env | `python3 -m venv` | node_modules per project |
| Run without install | `python3 -m module` | `npx package` |

## Gotchas

- `pip install` without venv installs system-wide - always use virtual environments
- `nvm` is shell-specific; restart terminal after install
- `npm install -g` may need `sudo` on Linux (or fix npm prefix)
- Python `python` vs `python3`: on some systems `python` is Python 2
- `npx` downloads and runs packages - security risk if package name is typo-squatted
- Node.js version matters significantly - use LTS for production

## See Also

- [[package-management]] - System package managers (apt, yum)
- [[bash-scripting]] - Shell scripting
- [[terminal-basics]] - Shell fundamentals
