---
title: File I/O and pathlib
category: concepts
tags: [python, files, csv, json, pathlib, os, io, encoding]
---

# File I/O and pathlib

Python provides built-in support for reading/writing text and binary files, CSV and JSON handling, and both `os.path` (procedural) and `pathlib` (object-oriented) for path manipulation. Always use `with` statements for automatic file closing and specify encoding explicitly.

## Key Facts

- Always use `with open(...) as f:` for automatic cleanup (even on exceptions)
- Always specify `encoding='utf-8'` for text files (default varies by OS)
- File modes: `'r'` read, `'w'` write (truncates!), `'a'` append, `'x'` exclusive create
- `pathlib.Path` is the modern API (Python 3.4+); uses `/` operator for joining
- `write()` does NOT add newlines; `print(..., file=f)` adds `\n` by default
- `newline=''` required when writing CSV on Windows (prevents double newlines)

## Patterns

### Reading Files
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

### Writing Files
```python
with open('output.txt', 'w', encoding='utf-8') as f:
    f.write('Hello\n')           # no auto newline
    f.writelines(['a\n', 'b\n']) # no auto newline between items
    print('Hello', file=f)       # adds \n automatically
```

### CSV Files
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

### JSON Files
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

JSON type mapping: `{}` -> dict, `[]` -> list, `""` -> str, `true/false` -> True/False, `null` -> None.

### pathlib (Modern, Recommended)
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

### os.path (Legacy)
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

### File Copy/Move
```python
import shutil
shutil.copy('src.txt', 'dst.txt')        # copy file
shutil.copy2('src.txt', 'dst.txt')       # copy with metadata
shutil.copytree('src_dir', 'dst_dir')    # copy directory tree
shutil.rmtree('dir')                     # remove directory tree
```

### Temporary Files
```python
import tempfile

with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
    f.write('temp data')
    print(f.name)  # path to temp file
```

## Gotchas

- `'w'` mode truncates (erases) existing files - use `'a'` to append
- Default encoding varies by OS (Windows: `cp1252`, Linux: `utf-8`) - always specify
- `UnicodeDecodeError`: wrong encoding - try `'cp1252'` or `'latin-1'` or `errors='replace'`
- Binary mode (`'rb'`/`'wb'`) bypasses encoding - use for images, executables
- `ensure_ascii=False` in `json.dump()` required for non-ASCII characters (Cyrillic, CJK)

## See Also

- [[strings-and-text]] - string encoding/decoding
- [[error-handling]] - context managers for resource cleanup
- [[standard-library]] - os, shutil, tempfile modules
