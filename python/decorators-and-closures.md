---
title: Decorators and Closures
category: concepts
tags: [python, decorators, closures, functools, wraps, higher-order-functions]
---

# Decorators and Closures

A **closure** is a nested function that captures variables from its enclosing scope. A **decorator** is a callable that takes a function and returns a modified version of it. Decorators are syntactic sugar for higher-order functions and are fundamental to Python's metaprogramming capabilities.

## Key Facts

- A closure is created when an inner function references a variable from an outer (enclosing) function that has finished executing
- The `nonlocal` keyword allows a closure to modify variables in the enclosing scope (without it, assignment creates a new local)
- Decorators are applied with `@decorator` syntax, equivalent to `func = decorator(func)`
- Stacking decorators applies bottom-up: `@a @b def f` means `f = a(b(f))`
- `functools.wraps` preserves the original function's `__name__`, `__doc__`, `__module__`, and `__qualname__`
- Decorators can be classes implementing `__call__`, not just functions
- Parametrized decorators require an extra nesting level (decorator factory)
- See [[generators-and-iterators]] for `yield`-based patterns, [[metaclasses-and-descriptors]] for class-level decoration

## Patterns

### Basic Decorator with `functools.wraps`

```python
import functools
import time

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@timer
def slow_function(n):
    """Simulate slow work."""
    time.sleep(n)

slow_function(1)  # slow_function took 1.0001s
print(slow_function.__name__)  # "slow_function" (preserved by @wraps)
```

### Parametrized Decorator (Decorator Factory)

```python
import functools

def retry(max_attempts=3, exceptions=(Exception,)):
    """Decorator factory: returns a decorator configured with parameters."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exc = e
                    print(f"Attempt {attempt}/{max_attempts} failed: {e}")
            raise last_exc
        return wrapper
    return decorator

@retry(max_attempts=5, exceptions=(ConnectionError, TimeoutError))
def fetch_data(url: str) -> dict:
    ...
```

### Class-Based Decorator

```python
import functools

class CacheResult:
    """Decorator as a class -- useful when you need to store state."""
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        if args not in self.cache:
            self.cache[args] = self.func(*args)
        return self.cache[args]

    def clear_cache(self):
        self.cache.clear()

@CacheResult
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

fibonacci(30)
fibonacci.clear_cache()  # extra method available on the decorator instance
```

### Closure for State Encapsulation

```python
def make_counter(start=0):
    count = start
    def counter():
        nonlocal count
        count += 1
        return count
    return counter

c = make_counter(10)
print(c(), c(), c())  # 11, 12, 13
```

### Stacking Decorators

```python
@login_required        # applied second (outermost)
@validate_input        # applied first (innermost)
def create_user(data):
    ...

# Equivalent to:
# create_user = login_required(validate_input(create_user))
```

## Gotchas

- **Forgetting `@functools.wraps`**: without it, `func.__name__` returns `"wrapper"`, breaking logging, debugging, and API documentation generation (FastAPI relies on function metadata)
- **Late binding in closures**: `lambda: i` inside a loop captures the variable `i`, not its value -- all lambdas will use the final value of `i`. Fix: `lambda i=i: i` (default argument binds eagerly)
- **Decorating methods**: `self` is part of `*args` in the wrapper; class-based decorators on methods need `__get__` to act as descriptors, or use `functools.wraps` on a regular function decorator
- **Decorator ordering matters**: `@app.route @login_required` is different from `@login_required @app.route` -- route must be outermost to register correctly
- **Async-aware decorators**: wrapping an `async def` with a sync decorator loses the coroutine. Use `inspect.iscoroutinefunction()` to detect and handle async functions

## See Also

- [functools.wraps -- Python docs](https://docs.python.org/3/library/functools.html#functools.wraps)
- [PEP 318 -- Decorators for Functions and Methods](https://peps.python.org/pep-0318/)
- [[context-managers]] - `contextmanager` decorator
- [[fastapi-fundamentals]] - decorators in route registration
