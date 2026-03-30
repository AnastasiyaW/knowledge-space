---
title: Context Managers
category: concepts
tags: [python, context-manager, with, contextlib, enter, exit, resource-management]
---

# Context Managers

A context manager is an object implementing `__enter__` and `__exit__` that manages resource acquisition and release via the `with` statement. The `contextlib` module provides utilities for creating context managers from generators and composing multiple contexts.

## Key Facts

- `__enter__` is called on entering `with` block; its return value is bound by `as`
- `__exit__(self, exc_type, exc_val, exc_tb)` is called on exit; returning `True` suppresses the exception
- `@contextmanager` from `contextlib` turns a generator function with a single `yield` into a context manager
- `contextlib.suppress(*exceptions)` silently ignores specified exceptions
- `contextlib.ExitStack` manages a dynamic number of context managers
- `async with` uses `__aenter__` and `__aexit__` for async context managers
- `@asynccontextmanager` creates async context managers from async generators
- See [[generators-and-iterators]] for `yield` mechanics, [[async-programming]] for `async with`

## Patterns

### Class-Based Context Manager

```python
import time

class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.perf_counter() - self.start
        print(f"Elapsed: {self.elapsed:.4f}s")
        return False  # do not suppress exceptions

with Timer() as t:
    time.sleep(1)
# Elapsed: 1.0002s
print(t.elapsed)  # 1.0002
```

### Generator-Based Context Manager

```python
from contextlib import contextmanager
import os

@contextmanager
def temp_directory(path: str):
    """Create temp dir, yield it, clean up on exit."""
    os.makedirs(path, exist_ok=True)
    try:
        yield path
    finally:
        import shutil
        shutil.rmtree(path, ignore_errors=True)

with temp_directory("/tmp/work") as d:
    # d == "/tmp/work", directory exists
    open(f"{d}/file.txt", "w").write("data")
# directory is removed after the block
```

### Database Transaction Context Manager

```python
@contextmanager
def transaction(conn):
    """Commit on success, rollback on exception."""
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise

with transaction(db_connection) as conn:
    conn.execute("INSERT INTO users VALUES (?)", ("Alice",))
    conn.execute("INSERT INTO orders VALUES (?)", (42,))
# Both inserts committed, or both rolled back
```

### `ExitStack` for Dynamic Resources

```python
from contextlib import ExitStack

def process_files(paths: list[str]):
    with ExitStack() as stack:
        files = [stack.enter_context(open(p)) for p in paths]
        # All files open; all will be closed on exit
        for f in files:
            process(f.read())

# Also useful for conditional context managers:
with ExitStack() as stack:
    if need_lock:
        stack.enter_context(lock)
    if need_transaction:
        stack.enter_context(transaction(conn))
    do_work()
```

### Exception Suppression

```python
from contextlib import suppress
import os

# Instead of try/except/pass:
with suppress(FileNotFoundError):
    os.remove("temp.txt")

# Equivalent to:
# try:
#     os.remove("temp.txt")
# except FileNotFoundError:
#     pass
```

### Async Context Manager

```python
from contextlib import asynccontextmanager
import httpx

@asynccontextmanager
async def managed_client(**kwargs):
    client = httpx.AsyncClient(**kwargs)
    try:
        yield client
    finally:
        await client.aclose()

async def main():
    async with managed_client(timeout=30) as client:
        response = await client.get("https://api.example.com")
```

## Gotchas

- **`__exit__` returning `True` suppresses ALL exceptions**: including `KeyboardInterrupt` and `SystemExit`. Only suppress specific, expected exceptions
- **Generator-based context manager exception handling**: code after `yield` in `@contextmanager` runs in `finally`. If you need to handle the exception, wrap `yield` in `try/except`, re-raise if needed
- **`@contextmanager` can only `yield` once**: yielding more than once raises `RuntimeError`. The single yield is the point where the `with` block body runs
- **`as` variable scope**: `with open(f) as handle:` -- `handle` remains accessible after the `with` block exits (unlike some languages), but the resource is closed. Accessing it may raise `ValueError: I/O operation on closed file`
- **Nested `with` statements**: Python 3.10+ supports `with (open(a) as f1, open(b) as f2):` using parenthesized context managers. Before 3.10, use `contextlib.ExitStack` or nested `with` blocks

## See Also

- [contextlib -- Python docs](https://docs.python.org/3/library/contextlib.html)
- [PEP 343 -- The "with" statement](https://peps.python.org/pep-0343/)
- [[error-handling-and-logging]] - exception patterns in `__exit__`
- [[async-programming]] - `async with` and `@asynccontextmanager`
