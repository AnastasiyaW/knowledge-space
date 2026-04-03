---
title: Python Fundamentals for Data Science
category: tools
tags: [data-science, python, fundamentals, jupyter]
---

# Python Fundamentals for Data Science

Python for DS is primarily an interface to existing libraries (pandas, sklearn, torch), not general-purpose programming. Treat it as a platform for running pre-built tools.

## Environment

**Jupyter Notebook / Google Colab**: primary workspace. Interactive, cell-by-cell execution.

Colab tips:
- Switch to English interface (better for googling errors)
- `Shift+Enter`: run cell, move to next
- `Ctrl+M, B`: insert cell below
- `Ctrl+M, D`: delete cell
- Files are session-only - re-download after restart

## Core Types

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

## Slicing

Works on lists and strings: `[start:stop:step]`, stop is exclusive.

```python
nums = [1, 2, 3, 4, 5]
nums[:2]    # [1, 2]
nums[1:]    # [2, 3, 4, 5]
nums[-1]    # 5
nums[::2]   # [1, 3, 5]
nums[::-1]  # [5, 4, 3, 2, 1]
```

## Control Flow

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

## List Comprehensions

Replace 3-line loops with 1 line:

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

## Functions

```python
def calculate_metric(actual, predicted):
    """Calculate MAE between actual and predicted values."""
    errors = [abs(a - p) for a, p in zip(actual, predicted)]
    return sum(errors) / len(errors)

# Lambda (anonymous functions)
df['col'].apply(lambda x: x * 2)
```

## Dictionaries

```python
# Merge
merged = {**dict_a, **dict_b}  # right overrides left

# Comprehension
squares = {x: x**2 for x in range(10)}

# Iteration
for key, value in d.items():
    print(key, value)
```

## String Formatting

```python
f"{value:.2f}"     # 2 decimal places
f"{name:>10}"      # right-align, width 10
'...'.join(['a', 'b', 'c'])  # 'a...b...c'
```

## Error Handling

```python
try:
    result = risky_operation()
except ValueError as e:
    print(f"Value error: {e}")
except Exception as e:
    print(f"Unexpected: {e}")
```

## Naming Conventions

- Variables: `snake_case` (not camelCase)
- Classes: `CamelCase`
- Files: no spaces, no Cyrillic: `my_analysis.ipynb`
- Meaningful names: `salary_range` not `x`

## Libraries Import Pattern

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
```

## Gotchas
- Indentation matters (4 spaces standard) - mixing tabs and spaces causes errors
- `=` is assignment, `==` is comparison
- Lists are mutable: `b = a` creates reference, not copy. Use `b = a.copy()`
- Integer division: `7 / 2 = 3.5`, `7 // 2 = 3`
- Never use `print()` for pandas DataFrames in Jupyter - destroys formatting

## See Also
- [[pandas-eda]] - primary DS library
- [[numpy-fundamentals]] - numerical computing
- [[data-visualization]] - matplotlib/seaborn
