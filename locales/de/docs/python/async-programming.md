---
title: "Asynchrone Programmierung (asyncio)"
category: concepts
tags: [python, asyncio, async, await, coroutines, event-loop, concurrency]
level: 3
source_sha256: 3039da4548f83412a0623518c1c1f4b82b8472ed587129ad9c158c9bc9e08eff
translation: machine
translated_at: '2026-10-24'
---
# Asynchrone Programmierung (asyncio) {#async-programming-asyncio}

Pythons `asyncio` bietet kooperatives Multitasking für I/O-gebundene Workloads in einem einzelnen Thread. Während I/O-Wartezeiten (Netzwerk, Festplatte) gibt die Kontrolle per `await` an andere Tasks ab. So lassen sich viele Verbindungen nebenläufig bearbeiten, ohne den Overhead von Threading.

## Wichtige Fakten {#key-facts}

- `async def` deklariert eine Coroutine-Funktion; ihr Aufruf liefert ein Coroutine-Objekt zurück (führt den Code nicht aus)
- `await` suspendiert die Coroutine, bis das erwartete Objekt abgeschlossen ist, und gibt die Kontrolle an den Event Loop zurück
- `asyncio.run(main())` ist der Standard-Einstiegspunkt: erstellt den Loop, führt aus und schließt ihn
- `asyncio.gather(*coros)` führt Coroutines nebenläufig aus und sammelt die Ergebnisse
- `asyncio.create_task(coro)` plant eine Coroutine als Task ein (Start sofort)
- `TaskGroup` (Python 3.11+) bietet strukturierte Nebenläufigkeit mit sauberer Exception-Behandlung
- Nur I/O-gebundene Operationen profitieren; CPU-gebundene Arbeit blockiert den Event Loop
- `uvloop` ist ein drop-in C-basierter Event Loop, deutlich schneller (wird von Uvicorn verwendet)

## Muster {#patterns}

### Grundlegendes async/await {#basic-asyncawait}
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

### asyncio.gather() mit Fehlerbehandlung {#asynciogather-with-error-handling}
```python
results = await asyncio.gather(
    fetch("url1"),
    fetch("bad_url"),
    return_exceptions=True,  # exceptions become return values, don't cancel others
)
# results[1] will be the exception object
```

### asyncio.create_task() {#asynciocreate_task}
```python
async def main():
    task1 = asyncio.create_task(fetch("url1"))
    task2 = asyncio.create_task(fetch("url2"))
    process_something()  # runs while tasks execute
    result1 = await task1
    result2 = await task2
```

### TaskGroup (Python 3.11+ - strukturierte Nebenläufigkeit) {#taskgroup-python-311-structured-concurrency}
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

### Semaphore zur Ratenbegrenzung {#semaphore-for-rate-limiting}
```python
async def fetch_with_limit(sem, url):
    async with sem:  # at most N concurrent
        async with httpx.AsyncClient() as client:
            return await client.get(url)

sem = asyncio.Semaphore(10)
tasks = [fetch_with_limit(sem, url) for url in urls]
results = await asyncio.gather(*tasks)
```

### Task-Abbruch {#task-cancellation}
```python
task = asyncio.create_task(long_operation())
task.cancel()
try:
    await task
except asyncio.CancelledError:
    print("Task was cancelled")
```

### Asynchrone Datei-I/O (aiofiles) {#async-file-io-aiofiles}
```python
import aiofiles

async def write_file(path, content):
    async with aiofiles.open(path, 'w') as f:
        await f.write(content)
```

### Producer-Consumer mit asyncio.Queue {#producer-consumer-with-asyncioqueue}
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

### Asynchrones SQLAlchemy {#async-sqlalchemy}
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import select

engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/db")

async def get_user(email):
    async with AsyncSession(engine) as session:
        result = await session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
```

## Synchron vs. asynchron: Performance {#sync-vs-async-performance}

```yaml
Sync:  [Request1 -----] [Request2 -----] [Request3 -----]  = 1500ms
Async: [Req1 --][Req2 --][Req3 --]                          = ~500ms

Sync:  100 concurrent requests -> need 100 worker threads
Async: 100 concurrent requests -> 1 worker handles all during I/O waits
```

## Stolperfallen {#gotchas}

- **Blockieren des Loops**: `requests.get()` und `time.sleep()` blockieren alles. Stattdessen `httpx.AsyncClient` und `await asyncio.sleep()` verwenden. Für unvermeidbaren synchronen Code: `await asyncio.to_thread(blocking_func)`
- **Nicht awaited Coroutine**: `fetch_url(url)` ohne `await` tut nichts. Es wird nur ein Coroutine-Objekt zurückgegeben, und es erscheint eine `RuntimeWarning`
- **Verschachteltes `asyncio.run()`**: wirft `RuntimeError`, wenn der Loop bereits läuft. In Jupyter direkt `await main()` verwenden
- **`gather` mit `return_exceptions=True`**: Exceptions werden stillschweigend zu Rückgabewerten. Fehlschläge lassen sich dadurch leicht übersehen
- FastAPI: Wenn synchroner Code unvermeidbar ist, den Endpoint als `def` (nicht `async def`) deklarieren. Er läuft dann im Thread-Pool

## Siehe auch {#see-also}

- [Concurrency - Threading und Multiprocessing](concurrency.md) - Threading und Multiprocessing für CPU-gebundene Arbeit
- [[fastapi-fundamentals]] - asynchrone Endpoints
- [[fastapi-database-layer]] - asynchrone SQLAlchemy-Sessions
