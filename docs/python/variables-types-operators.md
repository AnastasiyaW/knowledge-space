---
title: Variables, Types, and Operators
category: concepts
tags: [python, types, variables, operators, numbers, booleans]
---

# Variables, Types, and Operators

Python is dynamically typed - variables don't need type declarations, and their type is determined at runtime. Everything in Python is an object, and variables are references (pointers) to objects.

## Data Types Overview

| Type | Example | Mutable | Description |
|------|---------|---------|-------------|
| `int` | `42` | No | Integer, arbitrary precision |
| `float` | `3.14` | No | Floating-point (64-bit IEEE 754) |
| `str` | `"hello"` | No | Text sequence |
| `bool` | `True/False` | No | Boolean |
| `NoneType` | `None` | No | Null/absence of value |
| `list` | `[1, 2, 3]` | Yes | Ordered, changeable sequence |
| `tuple` | `(1, 2, 3)` | No | Ordered, immutable sequence |
| `dict` | `{"a": 1}` | Yes | Key-value mapping |
| `set` | `{1, 2, 3}` | Yes | Unordered unique elements |

Check type with `type(x)`. Prefer `isinstance(x, int)` over `type(x) == int` - it respects inheritance.

## Key Facts

- Python integers have arbitrary precision - no overflow
- `10 / 2` returns `5.0` (float), not `5`. Use `//` for integer division
- `round(2.5)` returns `2` (banker's rounding to nearest even)
- `0.1 + 0.2 != 0.3` due to IEEE 754 floating-point representation
- `id(x)` shows memory address; `is` checks identity (same object), `==` checks equality
- Falsy values: `0`, `0.0`, `""`, `[]`, `()`, `{}`, `set()`, `None`, `False`

## Patterns

### Number Arithmetic
```python
10 + 3    # 13  addition
10 - 3    # 7   subtraction
10 * 3    # 30  multiplication
10 / 3    # 3.333...  true division (always float)
10 // 3   # 3   floor division
10 % 3    # 1   modulo
10 ** 3   # 1000  exponentiation
```

### Floating-Point Precision
```python
0.1 + 0.2 == 0.3               # False!
round(0.1 + 0.2, 1) == 0.3     # True
abs((0.1 + 0.2) - 0.3) < 1e-9  # True (epsilon comparison)

from decimal import Decimal
Decimal('0.1') + Decimal('0.2')  # Decimal('0.3') exactly
```

### Variables and Assignment
```python
x = 10              # assignment
x = "hello"         # rebinding (dynamic typing)
x, y = 1, 2         # multiple assignment
x, y = y, x         # swap values
a = b = c = 0       # chained assignment
```

### Type Conversion
```python
int(3.7)      # 3 (truncates, does NOT round)
float(3)      # 3.0
int("42")     # 42
str(42)       # "42"
bool(0)       # False
bool(1)       # True
```

### Reference Semantics
```python
a = [1, 2, 3]
b = a              # b points to SAME list
b.append(4)
print(a)           # [1, 2, 3, 4] - a changed too!

c = a.copy()       # c is a NEW list
c.append(5)        # only c changed
```

### Comparison and Logical Operators
```python
# Chaining
1 < x < 10  # equivalent to: 1 < x and x < 10

# Short-circuit evaluation - returns actual values
0 or "default"      # "default"
"value" and 42      # 42
None or "fallback"  # "fallback"
```

### Special Float Values
```python
float('inf')    # positive infinity
float('-inf')   # negative infinity
float('nan')    # not a number
```

## Gotchas

- Never name variables same as built-in functions (`list`, `str`, `dict`, `print`) - shadows them
- `b = a` for mutable types creates a shared reference, not a copy
- `int("3.14")` raises `ValueError` - must use `float("3.14")` first, then `int()`
- `math.floor(-2.3)` is `-3`, `int(-2.3)` is `-2` (truncates toward zero)

## See Also

- [[strings-and-text]] - string operations and formatting
- [[data-structures]] - lists, tuples, sets, dictionaries
- [[type-hints]] - static type annotations
