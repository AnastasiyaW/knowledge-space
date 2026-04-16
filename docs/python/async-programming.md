---
title: Async Programming (asyncio)
category: concepts
tags: [python, asyncio, async, await, coroutines, event-loop, concurrency]
---

# Async Programming (asyncio)

Python's `asyncio` provides cooperative multitasking for I/O-bound workloads in a single thread. During I/O waits (network, disk), control yields to other tasks via `await`, enabling concurrent handling of many connections without threading overhead.

## Key Facts

- `async def` declares a coroutine function; calling it returns a coroutine object (does not execute)
- `await` suspends the coroutine until the awaited object completes, yielding control to the event loop
- `asyncio.run(main())` is the standard entry point - creates loop, runs, closes
- `asyncio.gather(*coros)` runs coroutines concurrently and collects results
- `asyncio.create_task(coro)` schedules a coroutine as a Task (starts immediately)
- `TaskGroup` (Python 3.11+) provides structured concurrency with proper exception handling
- Only I/O-bound operations benefit; CPU-bound work blocks the event loop
- `uvloop` is a drop-in C-based event loop, significantly faster (used by Uvicorn)

## Patterns

### Basic async/await
```python
import asyncio
import httpx

async def fetch_data(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

async def main():
    results = await asyncio.gather(
        fetch_data("https://api1.com"),
        fetch_data("https://api2.com"),
        fetch_data("https://api3.com"),
    )
    return results

asyncio.run(main())
```

### asyncio.gather() with Error Handling
```python
results = await asyncio.gather(
    fetch("url1"),
    fetch("bad_url"),
    return_exceptions=True,  # exceptions become return values, don't cancel others
)
# results[1] will be the exception object
```

### asyncio.create_task()
```python
async def main():
    task1 = asyncio.create_task(fetch("url1"))
    task2 = asyncio.create_task(fetch("url2"))
    process_something()  # runs while tasks execute
    result1 = await task1
    result2 = await task2
```

### TaskGroup (Python 3.11+ - Structured Concurrency)
```python
async def main():
    results = []
    async with asyncio.TaskGroup() as tg:
        for i in range(10):
            task = tg.create_task(process_item(i))
            results.append(task)
    # All tasks guaranteed complete; if any raises, all cancelled + ExceptionGroup raised
    return [t.result() for t in results]
```

### Semaphore for Rate Limiting
```python
async def fetch_with_limit(sem, url):
    async with sem:  # at most N concurrent
        async with httpx.AsyncClient() as client:
            return await client.get(url)

sem = asyncio.Semaphore(10)
tasks = [fetch_with_limit(sem, url) for url in urls]
results = await asyncio.gather(*tasks)
```

### Task Cancellation
```python
task = asyncio.create_task(long_operation())
task.cancel()
try:
    await task
except asyncio.CancelledError:
    print("Task was cancelled")
```

### Async File I/O (aiofiles)
```python
import aiofiles

async def write_file(path, content):
    async with aiofiles.open(path, 'w') as f:
        await f.write(content)
```

### Producer-Consumer with asyncio.Queue
```python
async def producer(queue):
    for i in range(10):
        await queue.put(f"item_{i}")
    await queue.put(None)  # sentinel

async def consumer(queue):
    while True:
        item = await queue.get()
        if item is None:
            break
        print(f"Processing {item}")
        queue.task_done()

queue = asyncio.Queue(maxsize=5)
await asyncio.gather(producer(queue), consumer(queue))
```

### Async SQLAlchemy
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import select

engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/db")

async def get_user(email):
    async with AsyncSession(engine) as session:
        result = await session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
```

## Sync vs Async Performance

```yaml
Sync:  [Request1 -----] [Request2 -----] [Request3 -----]  = 1500ms
Async: [Req1 --][Req2 --][Req3 --]                          = ~500ms

Sync:  100 concurrent requests -> need 100 worker threads
Async: 100 concurrent requests -> 1 worker handles all during I/O waits
```

## Gotchas

- **Blocking the loop**: `requests.get()`, `time.sleep()` block everything. Use `httpx.AsyncClient`, `await asyncio.sleep()`. For unavoidable sync: `await asyncio.to_thread(blocking_func)`
- **Unawaited coroutine**: `fetch_url(url)` without `await` does nothing - returns coroutine object, gives `RuntimeWarning`
- **Nested `asyncio.run()`**: raises `RuntimeError` if loop already running. In Jupyter: use `await main()` directly
- **`gather` with `return_exceptions=True`**: exceptions silently become return values - easy to miss failures
- FastAPI: if you must use sync code, declare endpoint as `def` (not `async def`) - runs in thread pool

## See Also

- [[concurrency]] - threading and multiprocessing for CPU-bound work
- [[fastapi-fundamentals]] - async endpoints
- [[fastapi-database-layer]] - async SQLAlchemy sessions
