---
title: Decorators
category: concepts
tags: [python, decorators, functools, wraps, metaprogramming]
---

# Decorators

A decorator is a function that wraps another function to extend its behavior without modifying its source code. Decorators are fundamental to Python - they power `@property`, `@classmethod`, `@staticmethod`, Flask/FastAPI routes, and many more patterns.

## Key Facts

- `@decorator` is syntactic sugar for `func = decorator(func)`
- Always use `@functools.wraps(func)` to preserve original function metadata
- Always use `*args, **kwargs` in wrapper and `return func(*args, **kwargs)`
- Stacked decorators apply bottom-up: `@bold @italic` = `bold(italic(func))`
- Decorators with arguments need an extra nesting level (decorator factory)
- Decorator code runs at definition/import time, not at call time

## Patterns

### Basic Decorator Template
```python
import functools

def decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # code before
        result = func(*args, **kwargs)
        # code after
        return result
    return wrapper
```

### Decorator with Arguments (Factory)
```python
def repeat(n):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(n):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def say(msg):
    print(msg)
```

### Stacking Decorators
```python
@bold       # applied second
@italic     # applied first
def greet():
    return "Hello!"
# Equivalent: greet = bold(italic(greet))
```

### Timing Decorator
```python
import time, functools

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper
```

### Retry Decorator
```python
def retry(max_attempts=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=2)
def fetch_data(url):
    ...
```

### Memoization / Caching
```python
def memoize(func):
    cache = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

# Built-in alternative:
@functools.lru_cache(maxsize=128)
def fib(n):
    if n < 2: return n
    return fib(n-1) + fib(n-2)
```

### Validation Decorator
```python
def validate_positive(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if any(arg < 0 for arg in args if isinstance(arg, (int, float))):
            raise ValueError("All numeric arguments must be positive")
        return func(*args, **kwargs)
    return wrapper
```

### Class-Based Decorator (with state)
```python
class CountCalls:
    def __init__(self, func):
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"Call {self.count}")
        return self.func(*args, **kwargs)

@CountCalls
def say_hello():
    print("Hello!")
```

### Class Decorator (decorating a class)
```python
def add_repr(cls):
    def __repr__(self):
        attrs = ', '.join(f'{k}={v!r}' for k, v in self.__dict__.items())
        return f'{cls.__name__}({attrs})'
    cls.__repr__ = __repr__
    return cls

@add_repr
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
```

## Gotchas

- Forgetting `return func(*args, **kwargs)` makes decorated function return `None`
- Without `@functools.wraps`, `func.__name__` becomes `'wrapper'` - breaks debugging
- Decorator runs at import time - `@decorator` line executes when function is defined
- Manual decoration preserves access to original: `decorated = my_decorator(original)` - `original` still usable
- Deep decorator stacking adds function call overhead - usually negligible but relevant for hot paths

## See Also

- [[functions]] - closures, higher-order functions
- [[oop-advanced]] - descriptors, class decorators
- [[profiling-and-optimization]] - `@lru_cache` for performance
