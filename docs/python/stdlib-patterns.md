---
title: Python Standard Library Patterns - Collections, Itertools, Closures
category: concepts
tags: [python, collections, itertools, functools, closures, scoping]
---

# Python Standard Library Patterns - Collections, Itertools, Closures

Python standard library data structures and functional programming tools - collections module, itertools, functools, heapq, scoping rules (LEGB), and closure patterns.

## Key Facts

- `defaultdict` auto-initializes missing keys; `Counter` counts frequencies; `deque` is O(1) at both ends
- `list.pop(0)` is O(N); `deque.popleft()` is O(1) - always use deque for queue operations
- LEGB scoping: Local -> Enclosing -> Global -> Built-in
- `nonlocal` modifies enclosing scope; `global` modifies module scope
- Closures capture variables by reference (late binding) - common gotcha with loops
- `functools.lru_cache` provides automatic memoization decorator

## Patterns

### Collections Module

```python
from collections import defaultdict, Counter, deque, namedtuple

# defaultdict - auto-initialize missing keys
graph = defaultdict(list)
graph['A'].append('B')  # no KeyError

# Counter - frequency counting
c = Counter('abracadabra')  # {'a': 5, 'b': 2, ...}
c.most_common(3)             # top 3 elements
c1 + c2                      # combine counters
c1 - c2                      # subtract (drops <= 0)

# deque - O(1) both ends, optional maxlen
d = deque(maxlen=100)  # fixed-size circular buffer
d.appendleft(x)
d.popleft()            # O(1) unlike list.pop(0)
d.rotate(2)            # rotate elements

# namedtuple - lightweight data class
Point = namedtuple('Point', ['x', 'y'])
p = Point(1, 2)
p.x, p._asdict(), p._replace(x=3)
```

### itertools

```python
import itertools

itertools.chain(iter1, iter2)           # flatten iterables
itertools.combinations(seq, r)          # r-length combinations
itertools.permutations(seq, r)          # r-length permutations
itertools.groupby(sorted_seq, key)      # group consecutive equal elements
itertools.accumulate(seq, operator.add) # running totals
itertools.product(seq1, seq2)           # Cartesian product
```

### functools

```python
import functools

functools.reduce(fn, seq, initial)       # fold left
functools.lru_cache(maxsize=128)         # memoization decorator
functools.partial(fn, arg1)              # partial application
functools.total_ordering                 # class decorator: define __eq__+__lt__, get rest
```

### heapq (Priority Queue)

```python
import heapq

heap = []
heapq.heappush(heap, (priority, item))
priority, item = heapq.heappop(heap)    # min-heap by default
heapq.heapify(lst)                      # O(N) in-place

# Max-heap: negate priorities
heapq.heappush(heap, (-priority, item))

heapq.nlargest(k, iterable, key=fn)
heapq.nsmallest(k, iterable, key=fn)
```

### LEGB Scoping Rule

Python name resolution: **L**ocal -> **E**nclosing -> **G**lobal -> **B**uilt-in.

```python
x = 'global'

def outer():
    x = 'enclosing'
    def inner():
        x = 'local'
        print(x)  # 'local'
    inner()

# global and nonlocal modify outer scopes
counter = 0
def increment():
    global counter
    counter += 1

def make_counter():
    count = 0
    def inc():
        nonlocal count
        count += 1
        return count
    return inc
```

### Closures

```python
def multiplier(factor):
    def multiply(x):
        return x * factor  # factor is "closed over"
    return multiply

double = multiplier(2)
double(5)  # 10

# Inspect closure cells
double.__closure__[0].cell_contents  # 2
```

### Guard Clause Pattern

```python
# Nested (avoid)
def process(user):
    if user:
        if user.is_active:
            if user.has_permission:
                return do_work(user)

# Guard clauses (prefer)
def process(user):
    if not user: return None
    if not user.is_active: raise InactiveUserError()
    if not user.has_permission: raise PermissionDenied()
    return do_work(user)
```

## Gotchas

- **Late binding in closures**: `[lambda: i for i in range(5)]` - all return 4, not 0-4. Fix: `[lambda i=i: i for i in range(5)]`
- `groupby` requires sorted input - it groups consecutive equal elements only
- `deque(maxlen=N)` silently discards oldest elements when full - no error raised
- `Counter` subtraction drops zero and negative counts; use `counter.subtract()` to keep them
- `namedtuple` is immutable; for mutable version use `dataclasses.dataclass`
- Without `global` or `nonlocal`, assignment creates a new local variable that shadows the outer one

## See Also

- [[dynamic-programming]] - memoization with `lru_cache`
- [[algorithms/problem-patterns]] - Counter/defaultdict for frequency problems
- [[data-structures-fundamentals]] - Big O of standard library operations
