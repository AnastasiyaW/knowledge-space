---
title: Iterators and Generators
category: concepts
tags: [python, iterators, generators, yield, itertools, lazy-evaluation]
---

# Iterators and Generators

Iterators implement the iteration protocol (`__iter__`/`__next__`), while generators provide a concise way to create iterators using `yield`. Generator expressions offer memory-efficient lazy evaluation. The `itertools` module provides a toolkit of composable iterator building blocks.

## Key Facts

- Iterable: has `__iter__()`. Iterator: has `__next__()` (raises `StopIteration` when done)
- All iterators are iterables, but not all iterables are iterators (lists are iterable, not iterators)
- Generators are one-shot - exhausted after single iteration
- Generator expressions use `()` instead of `[]` - constant memory regardless of size
- `yield` pauses function, preserves local state; `return` terminates function
- `yield from` delegates to another iterable/generator

## Patterns

### Iterator Protocol
```python
# How for-loop actually works:
my_list = [1, 2, 3]
iterator = iter(my_list)       # calls __iter__()
while True:
    try:
        item = next(iterator)  # calls __next__()
    except StopIteration:
        break
```

### Custom Iterator
```python
class CountDown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1
```

### Generator Functions
```python
def count_up(n):
    i = 1
    while i <= n:
        yield i    # pauses here, returns i
        i += 1     # resumes here on next()

gen = count_up(3)
next(gen)  # 1
next(gen)  # 2
next(gen)  # 3
next(gen)  # StopIteration
```

### yield from
```python
def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item

list(flatten([1, [2, [3, 4], 5], 6]))  # [1, 2, 3, 4, 5, 6]
```

### Generator Expressions
```python
squares = (x**2 for x in range(1_000_000))  # lazy, ~constant memory
sum(x**2 for x in range(100))               # no extra parentheses in function call
```

### send() - Two-Way Generators
```python
def accumulator():
    total = 0
    while True:
        value = yield total
        if value is None:
            break
        total += value

gen = accumulator()
next(gen)        # 0 (must initialize with next() first)
gen.send(10)     # 10
gen.send(20)     # 30
```

### Pipeline Pattern (Unix pipes)
```python
def read_lines(filename):
    with open(filename) as f:
        for line in f:
            yield line.strip()

def filter_comments(lines):
    for line in lines:
        if not line.startswith('#'):
            yield line

def parse_csv(lines):
    for line in lines:
        yield line.split(',')

# Chained - processes file line by line, minimal memory
pipeline = parse_csv(filter_comments(read_lines("data.csv")))
for row in pipeline:
    process(row)
```

### Infinite Sequences
```python
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

from itertools import islice
list(islice(fibonacci(), 10))  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

## itertools Module

### Infinite Iterators
```python
from itertools import count, cycle, repeat
count(10, 2)        # 10, 12, 14, 16, ...
cycle([1, 2, 3])    # 1, 2, 3, 1, 2, 3, ...
repeat('x', 3)      # 'x', 'x', 'x'
```

### Terminating Iterators
```python
from itertools import chain, islice, zip_longest, takewhile, dropwhile
from itertools import filterfalse, accumulate, groupby, tee, pairwise

chain([1,2], [3,4])             # [1, 2, 3, 4]
islice(count(), 5)              # [0, 1, 2, 3, 4]
zip_longest([1,2], [3,4,5], fillvalue=0)  # [(1,3), (2,4), (0,5)]
takewhile(lambda x: x < 5, [1,3,5,2])    # [1, 3]
dropwhile(lambda x: x < 5, [1,3,5,2])    # [5, 2]
accumulate([1,2,3,4,5])        # [1, 3, 6, 10, 15]
pairwise([1,2,3,4])            # [(1,2), (2,3), (3,4)]  (Python 3.10+)
```

### Combinatoric Iterators
```python
from itertools import product, permutations, combinations

product([1,2], ['a','b'])       # [(1,'a'), (1,'b'), (2,'a'), (2,'b')]
permutations([1,2,3], 2)       # [(1,2), (1,3), (2,1), (2,3), (3,1), (3,2)]
combinations([1,2,3,4], 2)     # [(1,2), (1,3), (1,4), (2,3), (2,4), (3,4)]
```

### groupby (requires sorted input)
```python
from itertools import groupby
data = sorted(students, key=lambda s: s.grade)
for grade, group in groupby(data, key=lambda s: s.grade):
    print(grade, list(group))
```

## Gotchas

- Generators are one-shot - exhausted after single iteration; create new one to iterate again
- `groupby` groups consecutive equal keys - requires pre-sorted input for complete grouping
- Can't get `len(gen)` - use `sum(1 for _ in gen)` but this exhausts it
- `tee(iterator, n)` creates n copies but advancing one doesn't advance others - memory grows
- Second `list(map_result)` returns empty list - iterators are consumed

## See Also

- [[functions]] - generator functions, yield
- [[async-programming]] - async generators
- [[data-structures]] - comprehensions as alternative
