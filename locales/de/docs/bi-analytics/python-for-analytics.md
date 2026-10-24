---
title: "Python für Analytics"
category: tools
tags: [bi-analytics, python, numpy, jupyter, basics, analytics]
level: 4
source_sha256: 8c8e5483551fd089c9572afc930521069c97108dc70ae393a7f706d2f90d8f60
translation: machine
translated_at: '2026-10-24'
---
# Python für Analytics {#python-for-analytics}

Python-Grundlagen für Data Analysts, mit Schwerpunkt auf Kernsyntax, NumPy für numerische Operationen und dem Workflow mit Jupyter Notebook. Dies ergänzt SQL-Kenntnisse und ermöglicht eine flexiblere Datenaufbereitung, als es BI-Tools allein erlauben.

## Wichtige Fakten {#key-facts}

- Python ist dynamisch typisiert (im Gegensatz zu Kotlin/Java, die statisch typisiert sind)
- NumPy bietet vektorisierte Operationen, die um Größenordnungen schneller sind als Python-Schleifen
- Jupyter Notebook ist die Standardumgebung für analytische Python-Arbeit
- Wichtige Bibliotheken: NumPy (numerisch), pandas (tabellarische Daten), matplotlib/seaborn (Visualisierung)
- List Comprehensions und Dict Comprehensions bieten eine kompakte Syntax für Datentransformationen

## Muster {#patterns}

### Grundlegende Datentypen und Strukturen {#core-data-types-and-structures}

```python
# Basic types
x = 5           # int
y = 3.14        # float
name = "Alice"  # str
active = True   # bool
nothing = None  # NoneType

# Lists
items = [1, 2, 3, 4, 5]
items.append(6)
items[0]         # first
items[-1]        # last
items[1:3]       # slice [2, 3]
squares = [x**2 for x in range(10)]
evens = [x for x in items if x % 2 == 0]

# Dictionaries
user = {"id": 1, "name": "Alice", "age": 28}
user.get("email", "")  # safe access with default
word_counts = {word: len(word) for word in ["hello", "world"]}
```

### Funktionen {#functions}

```python
def calculate_ltv(avg_order, frequency, months):
    """Calculate customer lifetime value."""
    return avg_order * frequency * months

def get_stats(numbers):
    return min(numbers), max(numbers), sum(numbers) / len(numbers)

min_val, max_val, avg = get_stats([1, 2, 3, 4, 5])
```

### NumPy {#numpy}

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])
zeros = np.zeros(10)
ones = np.ones((3, 4))

# Vectorized operations (no loops needed)
arr * 2          # [2, 4, 6, 8, 10]
arr ** 2         # [1, 4, 9, 16, 25]
np.sqrt(arr)     # element-wise sqrt

# Statistics
np.mean(arr)
np.median(arr)
np.std(arr)
np.percentile(arr, [25, 50, 75])

# 2D arrays (matrices)
matrix = np.array([[1, 2], [3, 4]])
matrix.shape     # (2, 2)
matrix.T         # transpose
matrix @ matrix  # matrix multiplication

# Boolean masking
arr[arr > 3]     # [4, 5]
```

### Workflow mit Jupyter Notebook {#jupyter-notebook-workflow}

Wichtige Tastenkürzel:
- `Shift+Enter` - Zelle ausführen, zur nächsten wechseln
- `Ctrl+Enter` - Zelle ausführen, auf derselben Zelle bleiben
- `A` / `B` - Zelle oberhalb/unterhalb einfügen (Befehlsmodus)
- `DD` - Zelle löschen
- `M` - in Markdown umwandeln; `Y` - in Code umwandeln

Best Practices:
- Kernel neu starten und alle Zellen ausführen, bevor das Notebook geteilt wird
- Markdown-Zellen für die Dokumentation verwenden
- Zellen fokussiert halten (ein Konzept pro Zelle)
- Variablen aussagekräftig benennen

## Stolperfallen {#gotchas}

- Ganzzahldivision in Python: `5 / 2 = 2.5` (float), aber `5 // 2 = 2` (Ganzzahl) - das unterscheidet sich von vielen anderen Sprachen
- Veränderliche Standardargumente in Funktionen sind eine klassische Falle: `def f(lst=[])` teilt die Liste über alle Aufrufe hinweg
- NumPy-Arrays haben einen festen dtype - das Mischen von Typen führt zu stillschweigendem Upcasting (Ganzzahlen werden zu Floats, sobald ein Float vorhanden ist)
- Jupyter-Zellen können out of order ausgeführt werden, was versteckte Zustandsfehler erzeugt - Kernel regelmäßig neu starten

## Siehe auch {#see-also}

- [[pandas-data-analysis]] - tabellarische Datenaufbereitung mit pandas
- [[sql-for-analytics]] - SQL als primäre Abfragesprache für Analytics
- [[web-marketing-analytics]] - Anbindung von Python an Analytics-Daten
