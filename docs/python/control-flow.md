---
title: Control Flow
category: concepts
tags: [python, loops, conditionals, comprehensions, iteration]
---

# Control Flow

Python uses indentation (4 spaces) to delimit code blocks. Control flow constructs include conditionals, for/while loops, and comprehensions as concise alternatives to loop-and-accumulate patterns.

## Key Facts

- Indentation is syntactically significant - 4 spaces per level (PEP 8)
- `for` loops iterate over any iterable (list, tuple, string, range, generator, etc.)
- `range(n)` generates `0, 1, ..., n-1`; `range(start, stop, step)` for full control
- Comprehensions (list, dict, set) replace simple for-loop-with-append patterns
- `break` exits loop; `continue` skips to next iteration; `pass` is a no-op placeholder

## Patterns

### Conditionals
```python
if condition:
    pass
elif another:
    pass
else:
    pass

# Ternary expression
result = "even" if x % 2 == 0 else "odd"

# Truthy/falsy shortcuts
if my_list:    # True if non-empty
if name:       # True if non-empty string
if count:      # True if non-zero
```

### For Loops
```python
for item in [1, 2, 3]:
    print(item)

for i in range(5):              # 0, 1, 2, 3, 4
    print(i)

for i in range(2, 10, 3):      # 2, 5, 8
    print(i)

for i, val in enumerate(['a', 'b', 'c']):  # index + value
    print(i, val)

for char in "hello":            # iterate string characters
    print(char)
```

### While Loops
```python
count = 0
while count < 5:
    print(count)
    count += 1

# Infinite loop with break
while True:
    data = input("Enter (q to quit): ")
    if data == 'q':
        break
```

### Nested Loops
```python
for i in range(3):
    for j in range(3):
        print(f"({i},{j})", end=" ")
    print()
```

### List Comprehensions
```python
# [expression for item in iterable]
squares = [x**2 for x in range(10)]

# With filter
evens = [x for x in range(20) if x % 2 == 0]

# With transformation + filter
upper_a = [x.upper() for x in names if x.startswith('A')]

# Nested (flatten)
flat = [x for row in matrix for x in row]

# With if-else (expression, not filter)
labels = ["even" if x % 2 == 0 else "odd" for x in range(5)]
```

### Dict and Set Comprehensions
```python
squares = {x: x**2 for x in range(6)}
even_set = {x for x in range(20) if x % 2 == 0}
```

### Generator Expressions
```python
# Lazy evaluation - no list in memory
total = sum(x**2 for x in range(1_000_000))
longest = max(len(w) for w in words)
```

## Gotchas

- Complex comprehension logic (multiple conditions, nested ifs) hurts readability - use a regular loop instead
- Forgetting `enumerate()` and manually tracking index with `i += 1` is unpythonic
- `range()` returns a range object, not a list - use `list(range(n))` if you need a list
- `for/else` and `while/else`: the `else` block runs when loop completes without `break` - rarely used but exists

## See Also

- [[iterators-and-generators]] - custom iteration, generator functions
- [[functions]] - breaking loops into functions with early return
- [[data-structures]] - comprehension targets (list, dict, set)
