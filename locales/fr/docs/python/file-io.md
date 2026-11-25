---
title: "E/S de fichiers et pathlib"
category: concepts
tags: [python, files, csv, json, pathlib, os, io, encoding]
level: 3
source_sha256: c529d9f745022ff40ca5933fa25af3a8d57e392c9e9c804b0a87deceac6c4540
translation: machine
translated_at: '2026-10-24'
---
# E/S de fichiers et pathlib {#file-io-and-pathlib}

Python fournit une prise en charge intégrée de la lecture et de l'écriture de fichiers texte et binaires, de la gestion des fichiers CSV et JSON, ainsi que de `os.path` (procédural) et `pathlib` (orienté objet) pour la manipulation des chemins. Utilisez toujours les instructions `with` pour une fermeture automatique des fichiers et spécifiez explicitement l'encodage.

## Points clés {#key-facts}

- Utilisez toujours `with open(...) as f:` pour un nettoyage automatique (même en cas d'exception)
- Spécifiez toujours `encoding='utf-8'` pour les fichiers texte (la valeur par défaut varie selon le système d'exploitation)
- Modes de fichier : `'r'` lecture, `'w'` écriture (tronque le fichier !), `'a'` ajout en fin de fichier, `'x'` création exclusive
- `pathlib.Path` est l'API moderne (Python 3.4+) ; elle utilise l'opérateur `/` pour la concaténation
- `write()` n'ajoute pas de sauts de ligne ; `print(..., file=f)` ajoute `\n` par défaut
- `newline=''` est requis lors de l'écriture de CSV sous Windows (évite les doubles sauts de ligne)

## Modèles {#patterns}

### Lecture de fichiers {#reading-files}
```python
# Read entire file
with open('data.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Read line by line (memory efficient)
with open('data.txt', encoding='utf-8') as f:
    for line in f:
        line = line.strip()  # remove trailing \n
        process(line)

# Read all lines as list
lines = f.readlines()  # ['line1\n', 'line2\n', ...]
```

### Écriture de fichiers {#writing-files}
```python
with open('output.txt', 'w', encoding='utf-8') as f:
    f.write('Hello\n')           # no auto newline
    f.writelines(['a\n', 'b\n']) # no auto newline between items
    print('Hello', file=f)       # adds \n automatically
```

### Fichiers CSV {#csv-files}
```python
import csv

# Reading
with open('data.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row['name'], row['age'])

# Writing
with open('out.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['name', 'age'])
    writer.writerows([['Alice', 30], ['Bob', 25]])
```

### Fichiers JSON {#json-files}
```python
import json

# Reading
with open('data.json', encoding='utf-8') as f:
    data = json.load(f)

# Writing
with open('out.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

# String operations
data = json.loads('{"name": "Alice"}')
json_str = json.dumps(data, indent=2)
```

Correspondance des types JSON : `{}` -> dict, `[]` -> list, `""` -> str, `true/false` -> True/False, `null` -> None.

### pathlib (moderne, recommandé) {#pathlib-modern-recommended}
```python
from pathlib import Path

p = Path('dir/subdir/file.txt')
p = Path.home() / 'Documents' / 'file.txt'  # / joins paths
p = Path.cwd()

# Properties
p.name         # 'file.txt'
p.stem         # 'file'
p.suffix       # '.txt'
p.parent       # Path('dir/subdir')
p.exists()     # True/False
p.is_file()    # True/False
p.is_dir()     # True/False

# Read/write shortcuts
text = p.read_text(encoding='utf-8')
p.write_text('content', encoding='utf-8')

# Directory operations
p.mkdir(parents=True, exist_ok=True)
list(Path('.').glob('*.py'))        # all .py files
list(Path('.').rglob('*.py'))       # recursive glob

# Iteration
for item in Path('.').iterdir():
    print(item.name, item.is_file())
```

### os.path (héritage) {#ospath-legacy}
```python
import os

os.path.join('dir', 'sub', 'file.txt')
os.path.basename('/a/b/file.txt')    # 'file.txt'
os.path.dirname('/a/b/file.txt')     # '/a/b'
os.path.splitext('file.txt')         # ('file', '.txt')
os.path.exists('file.txt')
os.path.getsize('file.txt')          # bytes

# Walk directory tree
for dirpath, dirnames, filenames in os.walk('.'):
    for f in filenames:
        print(os.path.join(dirpath, f))
```

### Copie/déplacement de fichiers {#file-copymove}
```python
import shutil
shutil.copy('src.txt', 'dst.txt')        # copy file
shutil.copy2('src.txt', 'dst.txt')       # copy with metadata
shutil.copytree('src_dir', 'dst_dir')    # copy directory tree
shutil.rmtree('dir')                     # remove directory tree
```

### Fichiers temporaires {#temporary-files}
```python
import tempfile

with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
    f.write('temp data')
    print(f.name)  # path to temp file
```

## Pièges {#gotchas}

- Le mode `'w'` tronque (efface) les fichiers existants : utilisez `'a'` pour ajouter du contenu
- L'encodage par défaut varie selon le système d'exploitation (Windows : `cp1252`, Linux : `utf-8`) : spécifiez-le toujours
- `UnicodeDecodeError` : encodage incorrect : essayez `'cp1252'`, `'latin-1'` ou `errors='replace'`
- Le mode binaire (`'rb'`/`'wb'`) contourne l'encodage : à utiliser pour les images et les exécutables
- `ensure_ascii=False` dans `json.dump()` est requis pour les caractères non ASCII (cyrillique, CJK)

## Voir aussi {#see-also}

- [[strings-and-text]] - encodage et décodage des chaînes
- [Error Handling and Context Managers](error-handling.md) - gestionnaires de contexte pour le nettoyage des ressources
- [[standard-library]] - modules os, shutil, tempfile
