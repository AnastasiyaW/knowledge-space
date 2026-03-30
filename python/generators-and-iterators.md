---
title: Generators and Iterators
category: concepts
tags: [python, generators, iterators, yield, itertools, lazy-evaluation]
---

# Generators and Iterators

An **iterator** is any object implementing `__iter__()` and `__next__()`. A **generator** is a function containing `yield` that returns a generator iterator -- a lazy, memory-efficient way to produce sequences on demand. Generator expressions provide a concise syntax for simple generators.

## Key Facts

- The iterator protocol: `__iter__()` returns self, `__next__()` returns the next value or raises `StopIteration`
- A generator function pauses at each `yield`, resuming on the next `next()` call
- `yield from iterable` delegates to a sub-iterator, propagating values and exceptions transparently
- Generator expressions use parentheses: `(x**2 for x in range(10))`
- Generators are single-pass -- once exhausted, they cannot be restarted
- `send(value)` resumes the generator and sends a value into the `yield` expression
- `throw(exc)` raises an exception at the point where the generator is paused
- `itertools` provides composable, memory-efficient iterator building blocks
- See [[decorators-and-closures]] for `@contextmanager` usage, [[async-programming]] for async generators

## Patterns

### Generator Function

```python
def read_large_file(path: str, chunk_size: int = 8192):
    """Memory-efficient file reader -- never loads full file."""
    with open(path, "rb") as f:
        while chunk := f.read(chunk_size):
            yield chunk

# Usage: processes any file size with constant memory
for chunk in read_large_file("/data/huge.csv"):
    process(chunk)
```

### Custom Iterator Class

```python
class Countdown:
    """Iterator protocol: __iter__ + __next__."""
    def __init__(self, start: int):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1

list(Countdown(5))  # [5, 4, 3, 2, 1]
```

### `yield from` for Delegation

```python
def flatten(nested):
    """Recursively flatten arbitrarily nested iterables."""
    for item in nested:
        if isinstance(item, (list, tuple, set)):
            yield from flatten(item)
        else:
            yield item

list(flatten([1, [2, [3, 4], 5], 6]))  # [1, 2, 3, 4, 5, 6]
```

### Generator Pipeline (Unix Pipes Pattern)

```python
def lines(path):
    with open(path) as f:
        yield from f

def grep(pattern, lines):
    for line in lines:
        if pattern in line:
            yield line

def upper(lines):
    for line in lines:
        yield line.upper()

# Compose: lazy pipeline, processes line by line
pipeline = upper(grep("ERROR", lines("/var/log/app.log")))
for line in pipeline:
    print(line)
```

### Key `itertools` Functions

```python
import itertools

# Infinite iterators
itertools.count(10, 2)           # 10, 12, 14, 16, ...
itertools.cycle([1, 2, 3])      # 1, 2, 3, 1, 2, 3, ...

# Combinatoric
list(itertools.product("AB", "12"))  # [('A','1'), ('A','2'), ('B','1'), ('B','2')]
list(itertools.combinations("ABC", 2))  # [('A','B'), ('A','C'), ('B','C')]

# Grouping
data = sorted(records, key=lambda r: r["category"])
for key, group in itertools.groupby(data, key=lambda r: r["category"]):
    print(key, list(group))

# Slicing infinite iterators
list(itertools.islice(itertools.count(), 5))  # [0, 1, 2, 3, 4]

# Chaining multiple iterables
itertools.chain(list1, list2, list3)  # single flat iterator
```

### `send()` for Coroutine-Style Generators

```python
def running_average():
    total = 0.0
    count = 0
    average = None
    while True:
        value = yield average
        total += value
        count += 1
        average = total / count

avg = running_average()
next(avg)               # prime the generator (advance to first yield)
avg.send(10)            # 10.0
avg.send(20)            # 15.0
avg.send(30)            # 20.0
```

## Gotchas

- **Single-pass exhaustion**: assigning a generator to a variable and iterating twice silently produces nothing on the second pass. Wrap in `list()` if you need reuse, or create a class implementing `__iter__` that returns a fresh generator
- **Generator expressions in function calls**: `sum(x**2 for x in range(10))` works (parentheses of the call serve double duty), but `sorted(x for x in items, key=len)` fails -- use `sorted((x for x in items), key=len)`
- **StopIteration propagation in Python 3.7+**: `StopIteration` raised inside a generator is converted to `RuntimeError` (PEP 479). Use `return` to end a generator, not `raise StopIteration`
- **Memory trap with `itertools.tee`**: `tee(gen, n)` caches elements -- if one copy advances far ahead, memory grows unboundedly
- **`yield` in exception handlers**: a generator paused inside a `try/finally` will run the `finally` block only when garbage collected or when `.close()` is called

## See Also

- [itertools -- Python docs](https://docs.python.org/3/library/itertools.html)
- [PEP 380 -- yield from](https://peps.python.org/pep-0380/)
- [[async-programming]] - async generators (`async for`, `async yield`)
- [[context-managers]] - `@contextmanager` uses `yield`
