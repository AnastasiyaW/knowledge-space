---
title: Built-in Data Structures
category: concepts
tags: [python, list, tuple, set, dict, collections, data-structures]
---

# Built-in Data Structures

Python provides four primary collection types: lists (ordered, mutable), tuples (ordered, immutable), sets (unordered, unique), and dictionaries (key-value mapping). Choosing the right structure impacts both correctness and performance.

## Key Facts

- `x in set` is O(1) average; `x in list` is O(n) - use sets for membership testing
- Lists are mutable; tuples are immutable (can be dict keys, slightly faster, less memory)
- `set()` creates empty set, not `{}` (which creates empty dict)
- Dicts are insertion-ordered since Python 3.7
- Keys must be hashable (immutable): str, int, float, tuple, frozenset

## Patterns

### Lists
```python
lst = [1, 2, 3, "hello", True]   # can mix types

# Adding
lst.append(x)          # add to end
lst.insert(0, x)       # insert at index
lst.extend([4, 5])     # add multiple

# Removing
lst.remove(x)          # first occurrence (ValueError if missing)
lst.pop()              # remove and return last
lst.pop(0)             # remove and return at index
del lst[0]             # delete by index

# Searching
x in lst               # membership O(n)
lst.index(x)           # first index (ValueError if missing)
lst.count(x)           # occurrences

# Sorting
lst.sort()             # in-place
sorted(lst)            # returns new sorted list

# Copying
copy1 = lst.copy()     # shallow copy
copy2 = lst[:]         # shallow copy via slice
import copy
deep = copy.deepcopy(nested_list)  # recursive copy
```

### List Comprehensions
```python
squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]
flat = [x for row in matrix for x in row]  # flatten
labels = ["even" if x % 2 == 0 else "odd" for x in range(5)]
```

### Tuples
```python
t = (1, 2, 3)
single = (1,)          # trailing comma required for single element
x, y, z = (1, 2, 3)   # unpacking
first, *rest = (1, 2, 3, 4)  # first=1, rest=[2, 3, 4]

# Functions returning multiple values return tuples
def min_max(lst):
    return min(lst), max(lst)
lo, hi = min_max([3, 1, 4])
```

### Sets
```python
s = {1, 2, 3, 2, 1}   # {1, 2, 3} - duplicates removed
s = set()              # empty set

s.add(4)
s.discard(2)           # no error if missing
s.remove(2)            # KeyError if missing

# Set operations
a | b                  # union
a & b                  # intersection
a - b                  # difference
a ^ b                  # symmetric difference
a.issubset(b)          # True if a <= b

# Remove duplicates preserving order (Python 3.7+)
unique = list(dict.fromkeys(names))
```

### Dictionaries
```python
d = {"name": "Alice", "age": 30}

d["name"]              # "Alice" (KeyError if missing)
d.get("name")          # "Alice" (None if missing)
d.get("phone", "N/A")  # default if missing
d["email"] = "a@b.com" # add/update
del d["age"]           # delete (KeyError if missing)
d.pop("age", None)     # delete, return None if missing

# Iteration
for key in d: ...                 # keys
for value in d.values(): ...      # values
for key, value in d.items(): ...  # pairs

# Merge (Python 3.9+)
d3 = d1 | d2           # d2 wins on conflicts
d1.update(d2)          # in-place merge
d3 = {**d1, **d2}      # unpacking merge
```

### Dict Comprehensions
```python
squares = {x: x**2 for x in range(6)}
swapped = {v: k for k, v in original.items()}
d = dict(zip(keys, values))  # from two lists
```

### Common Dict Patterns
```python
# Counting
from collections import Counter
counts = Counter("mississippi")
counts.most_common(3)  # [('i', 4), ('s', 4), ('p', 2)]

# Grouping with defaultdict
from collections import defaultdict
groups = defaultdict(list)
for name, dept in employees:
    groups[dept].append(name)

# Dispatch table
operations = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
}
result = operations["+"](5, 3)  # 8

# setdefault for grouping
groups = {}
for category, item in items:
    groups.setdefault(category, []).append(item)
```

### Frozen Types
```python
fs = frozenset([1, 2, 3])  # immutable set, can be dict key
# tuples can also be dict keys
coordinates = {(0, 0): "origin", (1, 1): "diagonal"}
```

## When to Use What

| Type | Mutable | Ordered | Duplicates | Use Case |
|------|---------|---------|------------|----------|
| list | Yes | Yes | Yes | General-purpose collection |
| tuple | No | Yes | Yes | Fixed data, dict keys, return values |
| set | Yes | No | No | Uniqueness, membership, set math |
| dict | Yes | Yes* | Keys: No | Key-value mapping, lookup |

*Insertion-ordered since Python 3.7

### Named Tuples

```python
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
p = Point(3, 4)
p.x                  # 3 (attribute access)
x, y = p             # still unpacks like a tuple
p._asdict()          # {'x': 3, 'y': 4}
p._replace(x=10)     # Point(x=10, y=4) - returns new instance

# Typing-friendly alternative (Python 3.6+)
from typing import NamedTuple

class Point(NamedTuple):
    x: float
    y: float
    label: str = "origin"
```

### ChainMap - Layered Lookups

```python
from collections import ChainMap

defaults = {'color': 'red', 'size': 10}
user_prefs = {'color': 'blue'}
runtime = {'debug': True}

config = ChainMap(runtime, user_prefs, defaults)
config['color']   # 'blue' - first match wins
config['size']    # 10 - falls through to defaults
config['debug']   # True
```

### deque - Fast Appends and Pops from Both Ends

```python
from collections import deque

d = deque(maxlen=5)          # bounded buffer
d.append(1)                  # right end
d.appendleft(0)              # left end - O(1) unlike list.insert(0, x) which is O(n)
d.rotate(2)                  # rotate right by 2

# Sliding window pattern
def sliding_window(iterable, n):
    it = iter(iterable)
    window = deque(maxlen=n)
    for _ in range(n):
        window.append(next(it))
    yield tuple(window)
    for item in it:
        window.append(item)
        yield tuple(window)
```

### Repetition and Shared References Trap

```python
# DANGER: repetition creates shared references for mutable objects
board = [[0] * 3] * 3    # 3 references to SAME inner list
board[0][0] = 1
print(board)              # [[1, 0, 0], [1, 0, 0], [1, 0, 0]] - all rows affected!

# FIX: use comprehension to create independent lists
board = [[0] * 3 for _ in range(3)]
board[0][0] = 1
print(board)              # [[1, 0, 0], [0, 0, 0], [0, 0, 0]] - correct
```

### Walrus Operator in Comprehensions (Python 3.8+)

```python
# Avoid computing expensive function twice
results = [y for x in data if (y := expensive(x)) > threshold]
```

## Gotchas

- `b = a` for lists creates shared reference, not a copy - use `a.copy()` or `a[:]`
- Shallow copy only copies top level - nested lists still share references
- `list.sort()` returns `None` (sorts in-place); `sorted()` returns new list
- `{1, 2} | {3}` is set union, not dict merge - context matters for `|`
- Modifying a dict during iteration raises `RuntimeError` - iterate over a copy
- `[[0]*3]*3` shares inner lists - use `[[0]*3 for _ in range(3)]` for independent rows
- `tuple` is NOT always immutable in practice: `t = ([1, 2],)` - the tuple itself is immutable but the list inside is mutable
- `dict.fromkeys(['a','b'], [])` shares the SAME list for all keys - use dict comprehension instead
- `in` operator on dict checks keys, not values - use `val in d.values()` for value check

## See Also

- [[standard-library]] - Counter, defaultdict, ChainMap, OrderedDict
- [[iterators-and-generators]] - lazy sequences
- [[oop-fundamentals]] - custom data classes
