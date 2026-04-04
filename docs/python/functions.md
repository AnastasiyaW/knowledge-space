---
title: Functions
category: concepts
tags: [python, functions, closures, lambda, scope, higher-order]
---

# Functions

Functions are first-class objects in Python - they can be passed as arguments, returned from other functions, and stored in variables. Understanding scope rules (LEGB), closures, and higher-order functions is essential for writing idiomatic Python.

## Key Facts

- `def` defines a function; without `return`, function returns `None`
- Parameter order: `def f(pos, *args, key=default, **kwargs)`
- `*args` collects extra positional args as tuple; `**kwargs` as dict
- LEGB scope: Local, Enclosing, Global, Built-in
- Lambdas are single-expression anonymous functions
- `map()` and `filter()` return one-time iterators (exhausted after single pass)

## Patterns

### Function Definition
```python
def greet(name, greeting="Hello"):
    """Greeting function with optional prefix."""
    return f"{greeting}, {name}!"

greet("Alice")            # "Hello, Alice!"
greet("Alice", "Hi")      # "Hi, Alice!"
```

### *args and **kwargs
```python
def my_func(*args, **kwargs):
    for item in args:        # tuple
        print(item)
    for key, val in kwargs.items():  # dict
        print(f"{key}={val}")

my_func(1, 2, fruit='apple', color='red')
```

### LEGB Scope
```python
x = 25          # Global

def outer():
    x = 50      # Enclosing
    def inner():
        x = 75  # Local
        print(x)  # 75
    inner()

outer()
print(x)  # 25 (global unchanged)
```

### global and nonlocal
```python
count = 0
def increment():
    global count    # modify module-level variable
    count += 1

def counter():
    n = 0
    def inc():
        nonlocal n  # modify enclosing scope variable
        n += 1
        return n
    return inc
```

### Closures
```python
def make_adder(n):
    def add(x):
        return x + n   # n captured from enclosing scope
    return add

plus_3 = make_adder(3)
plus_3(10)  # 13

# Closure with mutable state
def counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment
```

### Lambda
```python
square = lambda x: x ** 2
add = lambda a, b: a + b
classify = lambda x: 'even' if x % 2 == 0 else 'odd'

# Most useful inline
sorted(words, key=lambda w: len(w))
sorted(items, key=lambda x: x[1])  # sort by second element
```

### map() and filter()
```python
list(map(lambda x: x**2, [1, 2, 3]))       # [1, 4, 9]
list(filter(lambda x: x % 2 == 0, range(10)))  # [0, 2, 4, 6, 8]
list(filter(None, [0, '', None, 'hello']))  # ['hello'] (truthy filter)

# Multiple iterables
list(map(pow, [2, 3, 4], [4, 2, 3]))  # [16, 9, 64]
```

### operator Module (avoid trivial lambdas)
```python
import operator
sorted(items, key=operator.itemgetter(1))   # vs lambda x: x[1]
sorted(objs, key=operator.attrgetter('name'))  # vs lambda x: x.name
```

### Multiple Return Values
```python
def min_max(lst):
    return min(lst), max(lst)  # returns tuple

lo, hi = min_max([3, 1, 4, 1, 5])  # unpacking
```

### Early Return
```python
def find_first_even(nums):
    for n in nums:
        if n % 2 == 0:
            return n
    return None
```

### Functions as First-Class Objects
```python
def apply(func, value):
    return func(value)

apply(abs, -5)       # 5
apply(len, "hello")  # 5
```

### Docstrings
```python
def my_func(param):
    """
    Brief description.

    Args:
        param: description

    Returns:
        description of return value
    """
    pass

# Access: my_func.__doc__ or help(my_func)
```

## Built-in Functions Reference

| Category | Functions |
|----------|-----------|
| Type conversion | `int()`, `float()`, `str()`, `bool()`, `list()`, `tuple()`, `set()`, `dict()` |
| Math | `abs()`, `round()`, `divmod()`, `pow()`, `min()`, `max()`, `sum()` |
| Iteration | `len()`, `range()`, `enumerate()`, `zip()`, `sorted()`, `reversed()`, `all()`, `any()` |
| Functional | `map()`, `filter()` |
| Introspection | `type()`, `isinstance()`, `id()`, `dir()`, `help()`, `callable()` |
| Base conversion | `hex()`, `oct()`, `bin()`, `ord()`, `chr()` |

### Keyword-Only and Positional-Only Arguments (Python 3.8+)

```python
# Everything after * is keyword-only
def tag(name, *, cls=None, id=None):
    ...
tag("div", cls="main")       # OK
tag("div", "main")           # TypeError - cls is keyword-only

# Everything before / is positional-only
def pow(base, exp, /, mod=None):
    ...
pow(2, 10)                   # OK
pow(base=2, exp=10)          # TypeError - base and exp are positional-only

# Combined
def f(pos_only, /, normal, *, kw_only):
    ...
```

### Closure Late-Binding Trap

```python
# WRONG - all lambdas capture the same variable i
funcs = [lambda: i for i in range(5)]
[f() for f in funcs]  # [4, 4, 4, 4, 4] - all return last value!

# FIX - bind current value via default argument
funcs = [lambda i=i: i for i in range(5)]
[f() for f in funcs]  # [0, 1, 2, 3, 4] - each captures its own value
```

### functools.reduce

```python
from functools import reduce

# reduce(func, iterable, initial) - fold left
product = reduce(lambda a, b: a * b, [1, 2, 3, 4])  # 24
# Equivalent: ((1*2)*3)*4

# With initial value
total = reduce(lambda a, b: a + b, [], 0)  # 0 (empty list, no error)
```

### Function Annotations (Runtime Accessible)

```python
def greet(name: str, times: int = 1) -> str:
    return name * times

greet.__annotations__
# {'name': <class 'str'>, 'times': <class 'int'>, 'return': <class 'str'>}
# Annotations are metadata only - Python does NOT enforce them at runtime
```

## Gotchas

- Never shadow built-in names: `list = [1, 2]` breaks `list()` function
- `map(square, nums)` not `map(square(), nums)` - pass function object without calling it
- `map()`/`filter()` iterators are exhausted after one pass - convert to list if needed
- Mutable default arguments are shared across calls: use `def f(x=None): x = x or []`
- Without `return`, function returns `None` implicitly
- Closures capture variables by reference, not by value - loop variable trap: `lambda: i` captures the name `i`, not its current value
- `def f(x=[]): x.append(1)` - default list is created ONCE at function definition time and shared across all calls
- `*args` receives a tuple (immutable); `**kwargs` receives a dict (mutable)
- `f(*[1,2], *[3,4])` is valid (multiple unpacking in a single call, Python 3.5+)

## See Also

- [[decorators]] - wrapping functions
- [[iterators-and-generators]] - generator functions with yield
- [[oop-fundamentals]] - methods vs functions
