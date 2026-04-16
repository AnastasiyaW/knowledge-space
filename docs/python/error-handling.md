---
title: Error Handling and Context Managers
category: concepts
tags: [python, exceptions, try-except, context-managers, with-statement, eafp]
---

# Error Handling and Context Managers

Python's exception handling uses try/except blocks and follows the EAFP (Easier to Ask Forgiveness than Permission) philosophy. Context managers (`with` statement) provide automatic resource cleanup. Custom exceptions create meaningful error hierarchies for applications.

## Key Facts

- Never use bare `except:` - it catches `SystemExit`, `KeyboardInterrupt`
- `finally` always runs, even if `return` is inside try/except
- `else` block runs only if no exception was raised in `try`
- EAFP is preferred over LBYL (Look Before You Leap) in Python
- Context managers (`with`) guarantee cleanup even on exceptions
- Custom exceptions should inherit from `Exception`, not `BaseException`

## Patterns

### Basic try/except
```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")
```

### Multiple Exception Types
```python
try:
    value = int(input("Number: "))
    result = 10 / value
except ValueError:
    print("Not a valid number")
except ZeroDivisionError:
    print("Cannot divide by zero")
except (TypeError, AttributeError) as e:
    print(f"Error: {e}")
```

### else and finally
```python
try:
    f = open("file.txt")
    data = f.read()
except FileNotFoundError:
    print("File not found")
else:
    print(f"Read {len(data)} chars")  # only if no exception
finally:
    f.close()  # ALWAYS runs
```

### Raising Exceptions
```python
def validate_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative")

# Re-raise current exception
try:
    process()
except ValueError:
    logging.error("Failed")
    raise  # re-raise same exception

# Exception chaining
try:
    value = int(user_input)
except ValueError as e:
    raise RuntimeError("Invalid config") from e
```

### Custom Exceptions
```python
class AppError(Exception):
    """Base exception for application."""
    pass

class ValidationError(AppError):
    def __init__(self, field, message):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")

class InsufficientFundsError(AppError):
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        super().__init__(f"Cannot withdraw {amount}, balance is {balance}")
```

### Context Managers (with statement)
```python
# File handling (automatic close)
with open("file.txt") as f:
    data = f.read()

# Multiple context managers
with open("in.txt") as src, open("out.txt", "w") as dst:
    dst.write(src.read())
```

### Custom Context Manager (class)
```python
class Timer:
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.time() - self.start
        print(f"Elapsed: {self.elapsed:.2f}s")
        return False  # don't suppress exceptions

with Timer() as t:
    heavy_computation()
```

### Custom Context Manager (contextlib)
```python
from contextlib import contextmanager

@contextmanager
def timer():
    start = time.time()
    yield  # code inside 'with' block runs here
    print(f"Elapsed: {time.time() - start:.2f}s")
```

### EAFP vs LBYL
```python
# EAFP (Pythonic) - try first, handle failure
try:
    value = my_dict[key]
except KeyError:
    value = default

# LBYL (less Pythonic) - check first
if key in my_dict:
    value = my_dict[key]
else:
    value = default
```

### Suppress Specific Exceptions
```python
from contextlib import suppress

with suppress(FileNotFoundError):
    os.remove("temp.txt")
```

### Logging Exceptions
```python
import logging

try:
    process()
except Exception:
    logging.exception("Processing failed")  # logs full traceback
    raise
```

## Exception Hierarchy (key classes)

```text
BaseException
 +-- SystemExit, KeyboardInterrupt, GeneratorExit
 +-- Exception
      +-- ArithmeticError (ZeroDivisionError, OverflowError)
      +-- AttributeError
      +-- ImportError (ModuleNotFoundError)
      +-- LookupError (IndexError, KeyError)
      +-- NameError (UnboundLocalError)
      +-- OSError (FileNotFoundError, PermissionError)
      +-- TypeError, ValueError, RuntimeError
```

### ExceptionGroup and except* (Python 3.11+)

Handle multiple concurrent exceptions (useful with asyncio `TaskGroup`):
```python
# ExceptionGroup bundles multiple exceptions
eg = ExceptionGroup("errors", [ValueError("bad"), TypeError("wrong")])

try:
    raise eg
except* ValueError as exc_group:
    print(f"Value errors: {exc_group.exceptions}")
except* TypeError as exc_group:
    print(f"Type errors: {exc_group.exceptions}")
# Both except* clauses can match - unlike regular except
```

### Exception Chaining Details

```python
# Implicit chaining - __context__ set automatically
try:
    1 / 0
except ZeroDivisionError:
    raise ValueError("bad input")
    # ValueError.__context__ = ZeroDivisionError (shown as "During handling...")

# Explicit chaining - __cause__ set with 'from'
try:
    data = json.loads(raw)
except json.JSONDecodeError as e:
    raise AppError("Invalid config") from e
    # AppError.__cause__ = JSONDecodeError (shown as "was the direct cause")

# Suppress context display
raise AppError("clean message") from None
```

### Nested Context Managers with ExitStack

```python
from contextlib import ExitStack

def process_files(filenames):
    with ExitStack() as stack:
        files = [stack.enter_context(open(f)) for f in filenames]
        # All files closed on exit, even if opening one fails
        return [f.read() for f in files]
```

### async Context Manager

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def managed_connection(url):
    conn = await connect(url)
    try:
        yield conn
    finally:
        await conn.close()

async with managed_connection("db://localhost") as conn:
    await conn.execute(query)
```

## Gotchas

- `except Exception as e` is acceptable; bare `except:` catches too much
- Execution order: try -> except (if error) -> else (if no error) -> finally (always)
- `finally` runs even with `return` in try/except - the `finally` return value wins
- `__exit__` returning `True` suppresses the exception - use carefully
- Retry loops should have a maximum attempt count to avoid infinite loops
- `except*` clauses are **not** mutually exclusive - multiple can match one ExceptionGroup
- Exception variable `e` in `except ValueError as e` is deleted after the except block exits (scoping rule to break reference cycles)
- Raising inside `__del__` is silently ignored - never rely on destructor exceptions
- `sys.exc_info()` returns `(None, None, None)` outside except blocks - use `e.__traceback__` to store tracebacks

## See Also

- [[functions]] - early return patterns
- [[fastapi-fundamentals]] - HTTP exception handling
- [[testing-with-pytest]] - testing exception raising
