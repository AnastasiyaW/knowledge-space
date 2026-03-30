---
title: Async Programming
category: concepts
tags: [python, asyncio, async, await, coroutines, event-loop, concurrency]
---

# Async Programming

Python's `asyncio` provides cooperative multitasking via coroutines, an event loop, and non-blocking I/O. A coroutine defined with `async def` suspends at `await` points, allowing other tasks to run. This is optimal for I/O-bound workloads (HTTP requests, database queries, file I/O) but does not bypass the GIL for CPU-bound work.

## Key Facts

- `async def` declares a coroutine function; calling it returns a coroutine object (does not execute)
- `await` suspends the coroutine until the awaited object completes, yielding control to the event loop
- `asyncio.run(main())` creates an event loop, runs the coroutine, and closes the loop
- `asyncio.gather(*coros)` runs multiple coroutines concurrently and collects results
- `asyncio.create_task(coro)` schedules a coroutine as a Task on the current loop (starts immediately)
- `TaskGroup` (Python 3.11+) provides structured concurrency with proper exception handling
- `async for` iterates over async iterables; `async with` uses async context managers
- `asyncio.Semaphore` limits concurrency; `asyncio.Queue` enables producer-consumer patterns
- See [[concurrency-and-parallelism]] for threading/multiprocessing comparison, [[fastapi-fundamentals]] for async endpoints

## Patterns

### Basic Async/Await

```python
import asyncio
import httpx

async def fetch_url(client: httpx.AsyncClient, url: str) -> str:
    response = await client.get(url)
    return response.text

async def main():
    async with httpx.AsyncClient() as client:
        urls = ["https://api.example.com/1", "https://api.example.com/2"]
        tasks = [fetch_url(client, url) for url in urls]
        results = await asyncio.gather(*tasks)
        for url, result in zip(urls, results):
            print(f"{url}: {len(result)} chars")

asyncio.run(main())
```

### TaskGroup (Python 3.11+ -- Structured Concurrency)

```python
import asyncio

async def process_item(item_id: int) -> dict:
    await asyncio.sleep(0.1)
    return {"id": item_id, "status": "done"}

async def main():
    results = []
    async with asyncio.TaskGroup() as tg:
        for i in range(10):
            task = tg.create_task(process_item(i))
            results.append(task)
    # All tasks are guaranteed complete here
    # If any task raises, all others are cancelled and ExceptionGroup is raised
    return [t.result() for t in results]
```

### Semaphore for Rate Limiting

```python
import asyncio

async def fetch_with_limit(sem: asyncio.Semaphore, url: str):
    async with sem:  # at most N concurrent requests
        async with httpx.AsyncClient() as client:
            return await client.get(url)

async def main():
    sem = asyncio.Semaphore(10)  # max 10 concurrent
    urls = [f"https://api.example.com/{i}" for i in range(100)]
    tasks = [fetch_with_limit(sem, url) for url in urls]
    results = await asyncio.gather(*tasks)
```

### Async Generator

```python
async def stream_events(url: str):
    """Async generator -- yields events as they arrive."""
    async with httpx.AsyncClient() as client:
        async with client.stream("GET", url) as response:
            async for line in response.aiter_lines():
                if line.startswith("data:"):
                    yield line[5:].strip()

async def main():
    async for event in stream_events("https://api.example.com/sse"):
        print(event)
```

### Producer-Consumer with asyncio.Queue

```python
import asyncio

async def producer(queue: asyncio.Queue, items: list):
    for item in items:
        await queue.put(item)
    await queue.put(None)  # sentinel

async def consumer(queue: asyncio.Queue, worker_id: int):
    while True:
        item = await queue.get()
        if item is None:
            queue.task_done()
            break
        await asyncio.sleep(0.1)  # simulate work
        print(f"Worker {worker_id} processed {item}")
        queue.task_done()

async def main():
    queue = asyncio.Queue(maxsize=20)
    items = list(range(50))
    producers = [asyncio.create_task(producer(queue, items))]
    consumers = [asyncio.create_task(consumer(queue, i)) for i in range(5)]
    await asyncio.gather(*producers, *consumers)
```

## Gotchas

- **Calling a coroutine without `await`**: `fetch_url(client, url)` returns a coroutine object, does not execute. A `RuntimeWarning: coroutine was never awaited` appears
- **Blocking calls inside async code**: `time.sleep(5)` or `requests.get()` blocks the entire event loop. Use `await asyncio.sleep()` and `httpx.AsyncClient` instead. For unavoidable sync calls: `await asyncio.to_thread(blocking_func)`
- **`asyncio.run()` nested calls**: calling `asyncio.run()` inside a running loop raises `RuntimeError`. Use `await` or `loop.run_in_executor()` instead. In Jupyter: `await main()` directly
- **Exception swallowing in `gather`**: with `return_exceptions=True`, exceptions become return values instead of being raised -- easy to miss failures silently
- **Task cancellation**: `task.cancel()` raises `CancelledError` at the next `await` point. If the coroutine catches all `BaseException`, cancellation is suppressed

## See Also

- [asyncio -- Python docs](https://docs.python.org/3/library/asyncio.html)
- [PEP 492 -- Coroutines with async and await](https://peps.python.org/pep-0492/)
- [[concurrency-and-parallelism]] - GIL, threading, multiprocessing
- [[fastapi-fundamentals]] - async endpoints in FastAPI
