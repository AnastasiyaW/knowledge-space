---
title: Collections and Data Structures
category: fundamentals
tags: [python, list, dict, set, tuple, comprehension, collections]
---

# Collections and Data Structures

Python's built-in collections: lists (mutable, ordered), tuples (immutable, ordered), dicts (key-value), sets (unique, unordered).

## Lists

```python
lst = [1, 2, 3, "hello", True]  # mixed types allowed
```

### Operations

```python
# Adding
lst.append(x)          # add to end
lst.insert(0, x)       # insert at index
lst.extend([4, 5])     # add multiple
lst + [4, 5]           # concatenation (new list)

# Removing
lst.remove(x)          # first occurrence of value
lst.pop()              # remove and return last
lst.pop(0)             # remove at index
del lst[0]             # delete by index

# Searching
x in lst               # membership test
lst.index(x)           # first index (ValueError if missing)
lst.count(x)           # occurrences

# Sorting
lst.sort()             # in-place
sorted(lst)            # new sorted list
lst.sort(key=len)      # sort by custom key
lst.reverse()          # in-place reverse
```

### List Comprehensions

```python
squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]
flat = [x for row in matrix for x in row]      # flatten nested
labels = ["even" if x % 2 == 0 else "odd" for x in range(5)]
```

### Copying

```python
copy1 = lst.copy()          # shallow copy
copy2 = lst[:]              # shallow copy via slice
import copy
deep = copy.deepcopy(lst)   # deep copy (nested objects too)
```

**Gotcha**: `b = a` does NOT copy - both point to the same list.

## Dictionaries

Mutable key-value mapping. Insertion-ordered since Python 3.7. Keys must be hashable (immutable).

```python
d = {"name": "Alice", "age": 30}
d = dict(name="Alice", age=30)       # keyword syntax
d = dict(zip(keys, values))          # from parallel lists

# Access
d["name"]              # KeyError if missing!
d.get("name")          # None if missing
d.get("phone", "N/A")  # default if missing

# Modification
d["email"] = "a@b.com"  # add/update
del d["age"]             # delete
d.pop("age", None)       # delete with default

# Iteration
for key in d: ...
for value in d.values(): ...
for key, value in d.items(): ...

# Merge (Python 3.9+)
d3 = d1 | d2             # d2 wins on conflicts
d1.update(d2)             # in-place merge
d3 = {**d1, **d2}         # unpacking merge
```

### Dict Comprehensions

```python
squares = {x: x**2 for x in range(6)}
swapped = {v: k for k, v in d.items()}
```

### Counting and Grouping Patterns

```python
# Manual counting
counts = {}
for char in text:
    counts[char] = counts.get(char, 0) + 1

# Using Counter (recommended)
from collections import Counter
counts = Counter(text)
counts.most_common(3)  # top 3

# Grouping with setdefault
groups = {}
for category, item in items:
    groups.setdefault(category, []).append(item)

# Dict as dispatch table
ops = {"+": lambda a, b: a + b, "-": lambda a, b: a - b}
result = ops["+"](5, 3)  # 8
```

## Tuples

Immutable ordered sequences. Use for fixed data, dict keys, multiple return values.

```python
t = (1, 2, 3)
single = (1,)          # trailing comma required for single element
t.count(2)             # occurrences
t.index(3)             # first index

# Unpacking
x, y, z = (1, 2, 3)
first, *rest = (1, 2, 3, 4)     # first=1, rest=[2, 3, 4]
first, *_, last = (1, 2, 3, 4)  # first=1, last=4

# Multiple return values
def min_max(lst):
    return min(lst), max(lst)  # returns tuple
lo, hi = min_max([3, 1, 4])
```

## Sets

Unordered collection of unique hashable elements. O(1) membership testing.

```python
s = {1, 2, 3, 2, 1}   # {1, 2, 3}
s = set()              # empty set (NOT {})

s.add(4)               # add element
s.discard(2)           # remove (no error if missing)
s.remove(2)            # remove (KeyError if missing)

# Set operations
a | b    # union
a & b    # intersection
a - b    # difference
a ^ b    # symmetric difference

# Subset/superset
{1, 2}.issubset({1, 2, 3})    # True
{1, 2}.isdisjoint({3, 4})     # True

# Remove duplicates preserving order (Python 3.7+)
unique = list(dict.fromkeys(names))
```

`frozenset` - immutable set, can be dict key or set element.

## When to Use What

| Type | Mutable | Ordered | Duplicates | Lookup | Use Case |
|------|---------|---------|------------|--------|----------|
| list | Yes | Yes | Yes | O(n) | General collection |
| tuple | No | Yes | Yes | O(n) | Fixed data, dict keys |
| dict | Yes | Yes | Keys: No | O(1) | Key-value mapping |
| set | Yes | No | No | O(1) | Uniqueness, membership |

## Gotchas

- `{} ` creates empty dict, not set - use `set()` for empty set
- `b = a` for any mutable creates an alias, not a copy
- Dict keys and set elements must be hashable (immutable)
- `list.sort()` returns `None` (in-place); `sorted()` returns new list
- `x in set` is O(1), `x in list` is O(n) - use sets for membership testing on large collections
- Modifying a dict/set while iterating raises `RuntimeError`

## See Also

- [[stdlib-essentials]] - Counter, defaultdict, ChainMap, OrderedDict
- [[iterators-and-generators]] - lazy iteration over collections
- [[variables-types-operators]] - type conversion between collections
