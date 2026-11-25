---
title: "Datei-E/A und pathlib"
category: concepts
tags: [python, files, csv, json, pathlib, os, io, encoding]
level: 3
source_sha256: c529d9f745022ff40ca5933fa25af3a8d57e392c9e9c804b0a87deceac6c4540
translation: machine
translated_at: '2026-10-24'
---
# Datei-E/A und pathlib {#file-io-and-pathlib}

Python bietet integrierte Unterstützung für das Lesen und Schreiben von Text- und Binärdateien sowie für die Verarbeitung von CSV und JSON. Für die Pfadmanipulation stehen sowohl `os.path` (prozedural) als auch `pathlib` (objektorientiert) zur Verfügung. Verwenden Sie immer `with`-Anweisungen, damit Dateien automatisch geschlossen werden, und geben Sie die Kodierung explizit an.

## Wichtige Fakten {#key-facts}

- Immer `with open(...) as f:` verwenden, damit die Bereinigung automatisch erfolgt (auch bei Ausnahmen)
- Für Textdateien immer `encoding='utf-8'` angeben (der Standardwert hängt vom Betriebssystem ab)
- Dateimodi: `'r'` lesen, `'w'` schreiben (kürzt die Datei!), `'a'` anhängen, `'x'` exklusiv erstellen
- `pathlib.Path` ist die moderne API (Python 3.4+) und verwendet den `/`-Operator zum Verbinden von Pfaden
- `write()` fügt keine Zeilenumbrüche hinzu; `print(..., file=f)` fügt standardmäßig `\n` hinzu
- `newline=''` ist beim Schreiben von CSV unter Windows erforderlich (verhindert doppelte Zeilenumbrüche)

## Muster {#patterns}

### Dateien lesen {#reading-files}
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

### Dateien schreiben {#writing-files}
```python
with open('output.txt', 'w', encoding='utf-8') as f:
    f.write('Hello\n')           # no auto newline
    f.writelines(['a\n', 'b\n']) # no auto newline between items
    print('Hello', file=f)       # adds \n automatically
```

### CSV-Dateien {#csv-files}
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

### JSON-Dateien {#json-files}
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

JSON-Typzuordnung: `{}` -> dict, `[]` -> list, `""` -> str, `true/false` -> True/False, `null` -> None.

### pathlib (modern, empfohlen) {#pathlib-modern-recommended}
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

### os.path (veraltet) {#ospath-legacy}
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

### Datei kopieren/verschieben {#file-copymove}
```python
import shutil
shutil.copy('src.txt', 'dst.txt')        # copy file
shutil.copy2('src.txt', 'dst.txt')       # copy with metadata
shutil.copytree('src_dir', 'dst_dir')    # copy directory tree
shutil.rmtree('dir')                     # remove directory tree
```

### Temporäre Dateien {#temporary-files}
```python
import tempfile

with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
    f.write('temp data')
    print(f.name)  # path to temp file
```

## Fallstricke {#gotchas}

- Der `'w'`-Modus kürzt (löscht) vorhandene Dateien. Verwenden Sie `'a'`, um anzuhängen.
- Die Standardkodierung hängt vom Betriebssystem ab (Windows: `cp1252`, Linux: `utf-8`). Geben Sie sie daher immer an.
- `UnicodeDecodeError`: falsche Kodierung. Versuchen Sie `'cp1252'` oder `'latin-1'` oder `errors='replace'`.
- Der Binärmodus (`'rb'`/`'wb'`) umgeht die Kodierung. Verwenden Sie ihn für Bilder und ausführbare Dateien.
- `ensure_ascii=False` in `json.dump()` ist für Nicht-ASCII-Zeichen (kyrillisch, CJK) erforderlich.

## Siehe auch {#see-also}

- [[strings-and-text]] - Kodierung und Dekodierung von Zeichenketten
- [Fehlerbehandlung und Kontextmanager](error-handling.md) - Kontextmanager für die Bereinigung von Ressourcen
- [[standard-library]] - Module os, shutil und tempfile
