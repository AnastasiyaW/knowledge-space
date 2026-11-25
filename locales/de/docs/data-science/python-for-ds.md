---
title: "Python-Grundlagen für Data Science"
category: tools
tags: [data-science, python, fundamentals, jupyter]
level: 3
source_sha256: f7fe09eaeb33f04b5975a96ee4928de6f4f75c42ed614256d9e2b1a76bc49f33
translation: machine
translated_at: '2026-10-24'
---
# Python-Grundlagen für Data Science {#python-fundamentals-for-data-science}

Python für Data Science ist in erster Linie eine Schnittstelle zu bestehenden Bibliotheken (pandas, sklearn, torch) und kein Allzweck-Programmierwerkzeug. Man sollte es als Plattform zum Ausführen vorgefertigter Werkzeuge betrachten.

## Umgebung {#environment}

**Jupyter Notebook / Google Colab**: primäre Arbeitsumgebung. Interaktiv, zellenweise Ausführung.

Colab-Tipps:
- Auf englische Oberfläche umstellen (besser für die Suche nach Fehlermeldungen)
- `Shift+Enter`: Zelle ausführen und zur nächsten wechseln
- `Ctrl+M, B`: Zelle darunter einfügen
- `Ctrl+M, D`: Zelle löschen
- Dateien sind nur für die Sitzung verfügbar - nach einem Neustart erneut herunterladen

## Grundlegende Datentypen {#core-types}

```python
# Numbers
x = 42
y = 3.14
z = x + y  # 45.14

# Strings
name = 'data science'
f"My field is {name}"  # f-string formatting

# Booleans
flag = True  # also: False
# 0, None, [], '' are falsy; everything else truthy

# Lists (ordered, mutable)
nums = [1, 2, 3]
nums.append(4)     # [1, 2, 3, 4]
nums[0]            # 1 (indexing from 0)
nums[-1]           # 4 (last element)

# Tuples (ordered, immutable)
point = (3, 4)     # can't modify

# Dictionaries
d = {'name': 'Alice', 'age': 30}
d['name']          # 'Alice'
d['city'] = 'NYC'  # add key
```

## Slicing {#slicing}

Funktioniert für Listen und Strings: `[start:stop:step]`, wobei `stop` nicht eingeschlossen ist.

```python
nums = [1, 2, 3, 4, 5]
nums[:2]    # [1, 2]
nums[1:]    # [2, 3, 4, 5]
nums[-1]    # 5
nums[::2]   # [1, 3, 5]
nums[::-1]  # [5, 4, 3, 2, 1]
```

## Kontrollfluss {#control-flow}

```python
# Conditionals
if x > 10:
    print('big')
elif x > 5:
    print('medium')
else:
    print('small')

# Loops
for item in my_list:
    print(item)

for i, item in enumerate(my_list):
    print(i, item)

for i in range(10):      # 0 to 9
    print(i)

# While
while condition:
    do_something()
```

## List Comprehensions {#list-comprehensions}

Drei Zeilen lange Schleifen durch eine einzeilige Form ersetzen:

```python
# Transform
doubled = [x * 2 for x in nums]

# Filter
big = [x for x in nums if x > 3]

# Transform + filter
result = [x * 2 for x in nums if x > 3]

# Conditional expression
labels = ['pos' if x > 0 else 'neg' for x in values]
```

## Funktionen {#functions}

```python
def calculate_metric(actual, predicted):
    """Calculate MAE between actual and predicted values."""
    errors = [abs(a - p) for a, p in zip(actual, predicted)]
    return sum(errors) / len(errors)

# Lambda (anonymous functions)
df['col'].apply(lambda x: x * 2)
```

## Dictionaries {#dictionaries}

```python
# Merge
merged = {**dict_a, **dict_b}  # right overrides left

# Comprehension
squares = {x: x**2 for x in range(10)}

# Iteration
for key, value in d.items():
    print(key, value)
```

## String-Formatierung {#string-formatting}

```python
f"{value:.2f}"     # 2 decimal places
f"{name:>10}"      # right-align, width 10
'...'.join(['a', 'b', 'c'])  # 'a...b...c'
```

## Fehlerbehandlung {#error-handling}

```python
try:
    result = risky_operation()
except ValueError as e:
    print(f"Value error: {e}")
except Exception as e:
    print(f"Unexpected: {e}")
```

## Namenskonventionen {#naming-conventions}

- Variablen: `snake_case` (nicht camelCase)
- Klassen: `CamelCase`
- Dateien: keine Leerzeichen, keine kyrillischen Zeichen: `my_analysis.ipynb`
- Aussagekräftige Namen: `salary_range` statt `x`

## Muster für den Import von Bibliotheken {#libraries-import-pattern}

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
```

## Fallstricke {#gotchas}
- Einrückung ist relevant (Standard: 4 Leerzeichen) - das Mischen von Tabs und Leerzeichen führt zu Fehlern
- `=` ist eine Zuweisung, `==` ist ein Vergleich
- Listen sind veränderlich: `b = a` erzeugt eine Referenz, keine Kopie. Stattdessen `b = a.copy()` verwenden
- Ganzzahlige Division: `7 / 2 = 3.5`, `7 // 2 = 3`
- `print()` niemals für pandas-DataFrames in Jupyter verwenden - die Formatierung geht dabei verloren

## Siehe auch {#see-also}
- [[pandas-eda]] - primäre DS-Bibliothek
- [[numpy-fundamentals]] - numerisches Rechnen
- [[data-visualization]] - matplotlib/seaborn
