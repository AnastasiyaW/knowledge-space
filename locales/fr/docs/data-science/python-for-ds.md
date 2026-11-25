---
title: "Python Fundamentals for Data Science"
category: tools
tags: [data-science, python, fundamentals, jupyter]
level: 3
source_sha256: f7fe09eaeb33f04b5975a96ee4928de6f4f75c42ed614256d9e2b1a76bc49f33
translation: machine
translated_at: '2026-10-24'
---
# Python Fundamentals for Data Science {#python-fundamentals-for-data-science}

Python pour la data science est principalement une interface vers des bibliothèques existantes (pandas, sklearn, torch), et non un langage de programmation généraliste. Considérez-le comme une plateforme permettant d'exécuter des outils préconstruits.

## Environment {#environment}

**Jupyter Notebook / Google Colab** : espace de travail principal. Interactif, exécution cellule par cellule.

Astuces Colab :
- Passer l'interface en anglais (plus adapté pour rechercher les erreurs sur Google)
- `Shift+Enter` : exécuter la cellule et passer à la suivante
- `Ctrl+M, B` : insérer une cellule en dessous
- `Ctrl+M, D` : supprimer la cellule
- Les fichiers ne sont conservés que pendant la session : téléchargez-les à nouveau après un redémarrage

## Core Types {#core-types}

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

Fonctionne sur les listes et les chaînes : `[start:stop:step]`, où stop est exclu.

```python
nums = [1, 2, 3, 4, 5]
nums[:2]    # [1, 2]
nums[1:]    # [2, 3, 4, 5]
nums[-1]    # 5
nums[::2]   # [1, 3, 5]
nums[::-1]  # [5, 4, 3, 2, 1]
```

## Control Flow {#control-flow}

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

Remplacer des boucles de 3 lignes par une seule ligne :

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

## Functions {#functions}

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

## String Formatting {#string-formatting}

```python
f"{value:.2f}"     # 2 decimal places
f"{name:>10}"      # right-align, width 10
'...'.join(['a', 'b', 'c'])  # 'a...b...c'
```

## Error Handling {#error-handling}

```python
try:
    result = risky_operation()
except ValueError as e:
    print(f"Value error: {e}")
except Exception as e:
    print(f"Unexpected: {e}")
```

## Naming Conventions {#naming-conventions}

- Variables : `snake_case` (et non camelCase)
- Classes : `CamelCase`
- Fichiers : sans espaces ni caractères cyrilliques : `my_analysis.ipynb`
- Noms explicites : `salary_range` plutôt que `x`

## Libraries Import Pattern {#libraries-import-pattern}

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
```

## Gotchas {#gotchas}
- L'indentation compte (4 espaces par convention) : mélanger tabulations et espaces provoque des erreurs
- `=` est l'affectation, `==` est la comparaison
- Les listes sont mutables : `b = a` crée une référence, et non une copie. Utilisez `b = a.copy()`
- Division entière : `7 / 2 = 3.5`, `7 // 2 = 3`
- Ne jamais utiliser `print()` pour les DataFrames pandas dans Jupyter : cela détruit la mise en forme

## See Also {#see-also}
- [[pandas-eda]] - bibliothèque DS principale
- [[numpy-fundamentals]] - calcul numérique
- [[data-visualization]] - matplotlib/seaborn
