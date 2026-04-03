---
title: Variables, Types, and Operators
category: fundamentals
tags: [python, types, operators, variables, numbers, boolean]
---

# Variables, Types, and Operators

Python is dynamically typed - variables don't need type declarations. Every value is an object with an identity (`id()`), type (`type()`), and value. Variables are references (pointers) to objects, not containers.

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

## Numbers

### Integers
Arbitrary precision - no overflow. Supports standard arithmetic:

```python
10 + 3    # 13  addition
10 - 3    # 7   subtraction
10 * 3    # 30  multiplication
10 / 3    # 3.333...  true division (always float!)
10 // 3   # 3   floor division (integer result)
10 % 3    # 1   modulo (remainder)
10 ** 3   # 1000  exponentiation
```

**Division always returns float**: `10 / 2` returns `5.0`, not `5`. Use `//` for integer division.

### Floating-Point Precision

```python
0.1 + 0.2          # 0.30000000000000004 (NOT 0.3!)
0.1 + 0.2 == 0.3   # False!

# Solutions
round(0.1 + 0.2, 1) == 0.3     # True - round before comparing
abs((0.1 + 0.2) - 0.3) < 1e-9  # True - epsilon comparison

from decimal import Decimal
Decimal('0.1') + Decimal('0.2')  # Decimal('0.3') exactly
```

### Rounding Behavior

```python
round(2.5)       # 2 (banker's rounding - to nearest even!)
round(3.5)       # 4
round(2.666, 2)  # 2.67

import math
math.floor(2.9)  # 2 (always down)
math.ceil(2.1)   # 3 (always up)
math.trunc(2.9)  # 2 (towards zero)
```

Special values: `float('inf')`, `float('-inf')`, `float('nan')`.

## Variables and Assignment

```python
x = 10              # assignment
x = "hello"         # rebinding to different type (dynamic typing)
x, y = 1, 2         # multiple assignment
x, y = y, x         # swap values
a = b = c = 0       # chained assignment
```

**Naming conventions**: `snake_case` for variables/functions, `PascalCase` for classes, `UPPER_CASE` for constants. Cannot start with digit. Case-sensitive.

### Identity vs Equality

```python
a = [1, 2, 3]
b = a              # b points to same list
b.append(4)
print(a)           # [1, 2, 3, 4] - a is also changed!

c = a.copy()       # c is a NEW list with same values
c.append(5)        # only c is changed
```

`is` checks identity (same object in memory). `==` checks equality (same value).

## Type Conversion

```python
int(3.7)      # 3 (truncates, not rounds)
float(3)      # 3.0
int("42")     # 42
str(42)       # "42"
bool(0)       # False
bool(1)       # True
```

## Truthiness

Falsy values: `0`, `0.0`, `""`, `[]`, `()`, `{}`, `set()`, `None`, `False`. Everything else is truthy.

```python
if my_list:   # True if list is non-empty
if name:      # True if string is non-empty
if count:     # True if count != 0
```

## Comparison and Logical Operators

```python
# Comparison (chaining supported)
1 < x < 10  # equivalent to: 1 < x and x < 10

# Logical operators return actual values, not just True/False
0 or "default"     # "default"
"value" and 42     # 42
None or "fallback" # "fallback"
```

Short-circuit evaluation: `and` stops if first operand is falsy, `or` stops if first is truthy.

## Conditional Statements

```python
if condition:
    pass
elif another:
    pass
else:
    pass

# Ternary expression
result = "even" if x % 2 == 0 else "odd"
```

## Loops

```python
# for loop with range
for i in range(5):           # 0, 1, 2, 3, 4
for i in range(2, 10):       # 2, 3, ..., 9
for i in range(0, 20, 3):    # 0, 3, 6, 9, 12, 15, 18

# enumerate for index + value
for i, val in enumerate(['a', 'b', 'c']):
    print(i, val)

# while loop
while condition:
    pass

# Loop control
break       # exit loop
continue    # skip to next iteration
```

## Gotchas

- `10 / 2` returns `5.0` (float), not `5`
- `round(2.5)` returns `2` (banker's rounding), not `3`
- `0.1 + 0.2 != 0.3` due to floating-point representation
- Naming a variable `list`, `str`, `dict`, or `print` shadows built-in functions
- `b = a` for mutable types creates an alias, not a copy

## See Also

- [[strings-and-text]] - string operations and formatting
- [[collections-and-data-structures]] - lists, dicts, sets, tuples
- [[type-hints-and-mypy]] - static type annotations
