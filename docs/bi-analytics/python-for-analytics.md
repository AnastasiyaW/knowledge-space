---
title: Python for Analytics
category: tools
tags: [bi-analytics, python, numpy, jupyter, basics, analytics]
---

# Python for Analytics

Python fundamentals for data analysts, covering core syntax, NumPy for numerical operations, and Jupyter Notebook workflow. This complements SQL skills and enables more flexible data manipulation than BI tools alone.

## Key Facts

- Python is dynamically typed (unlike Kotlin/Java which are statically typed)
- NumPy provides vectorized operations that are orders of magnitude faster than Python loops
- Jupyter Notebook is the standard environment for analytical Python work
- Key libraries: NumPy (numerical), pandas (tabular data), matplotlib/seaborn (visualization)
- List comprehensions and dict comprehensions provide concise data transformation syntax

## Patterns

### Core Data Types and Structures

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

### Functions

```python
def calculate_ltv(avg_order, frequency, months):
    """Calculate customer lifetime value."""
    return avg_order * frequency * months

def get_stats(numbers):
    return min(numbers), max(numbers), sum(numbers) / len(numbers)

min_val, max_val, avg = get_stats([1, 2, 3, 4, 5])
```

### NumPy

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

### Jupyter Notebook Workflow

Key shortcuts:
- `Shift+Enter` - run cell, move to next
- `Ctrl+Enter` - run cell, stay
- `A` / `B` - insert cell above/below (command mode)
- `DD` - delete cell
- `M` - convert to Markdown; `Y` - convert to Code

Best practices:
- Restart kernel and run all cells before sharing
- Use Markdown cells for documentation
- Keep cells focused (one concept per cell)
- Name variables descriptively

## Gotchas

- Python integer division: `5 / 2 = 2.5` (float) but `5 // 2 = 2` (integer) - this differs from many languages
- Mutable default arguments in functions are a classic trap: `def f(lst=[])` shares the list across calls
- NumPy arrays have fixed dtype - mixing types causes silent upcasting (ints become floats if any float present)
- Jupyter cells can run out of order, creating hidden state bugs - restart kernel regularly

## See Also

- [[pandas-data-analysis]] - tabular data manipulation with pandas
- [[sql-for-analytics]] - SQL as primary analytics query language
- [[web-marketing-analytics]] - connecting Python to analytics data
