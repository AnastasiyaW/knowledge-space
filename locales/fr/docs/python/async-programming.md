---
title: "Programmation asynchrone (asyncio)"
category: concepts
tags: [python, asyncio, async, await, coroutines, event-loop, concurrency]
level: 3
source_sha256: 3039da4548f83412a0623518c1c1f4b82b8472ed587129ad9c158c9bc9e08eff
translation: machine
translated_at: '2026-10-24'
---
# Programmation asynchrone (asyncio) {#async-programming-asyncio}

`asyncio` de Python fournit un multitâche coopératif pour les charges liées aux E/S dans un seul thread. Pendant les attentes d'E/S (réseau, disque), le contrôle passe à d'autres tâches via `await`, ce qui permet de gérer simultanément de nombreuses connexions sans le surcoût des threads.

## Points clés {#key-facts}

- `async def` déclare une fonction coroutine ; l'appeler renvoie un objet coroutine (sans l'exécuter)
- `await` suspend la coroutine jusqu'à ce que l'objet attendu se termine, en rendant le contrôle à la boucle d'événements
- `asyncio.run(main())` est le point d'entrée standard : il crée la boucle, l'exécute, puis la ferme
- `asyncio.gather(*coros)` exécute des coroutines de manière concurrente et collecte les résultats
- `asyncio.create_task(coro)` planifie une coroutine sous forme de Task (démarrage immédiat)
- `TaskGroup` (Python 3.11+) fournit une concurrence structurée avec une gestion correcte des exceptions
- Seules les opérations liées aux E/S en tirent profit ; le travail lié au CPU bloque la boucle d'événements
- `uvloop` est une boucle d'événements en C, remplaçant directe (drop-in) et nettement plus rapide (utilisée par Uvicorn)

## Motifs {#patterns}

### async/await de base {#basic-asyncawait}
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

### asyncio.gather() avec gestion des erreurs {#asynciogather-with-error-handling}
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

### TaskGroup (Python 3.11+ - concurrence structurée) {#taskgroup-python-311-structured-concurrency}
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

### Sémaphore pour la limitation de débit {#semaphore-for-rate-limiting}
```python
async def fetch_with_limit(sem, url):
    async with sem:  # at most N concurrent
        async with httpx.AsyncClient() as client:
            return await client.get(url)

sem = asyncio.Semaphore(10)
tasks = [fetch_with_limit(sem, url) for url in urls]
results = await asyncio.gather(*tasks)
```

### Annulation de tâches {#task-cancellation}
```python
task = asyncio.create_task(long_operation())
task.cancel()
try:
    await task
except asyncio.CancelledError:
    print("Task was cancelled")
```

### E/S de fichiers asynchrones (aiofiles) {#async-file-io-aiofiles}
```python
import aiofiles

async def write_file(path, content):
    async with aiofiles.open(path, 'w') as f:
        await f.write(content)
```

### Producteur-consommateur avec asyncio.Queue {#producer-consumer-with-asyncioqueue}
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

### SQLAlchemy asynchrone {#async-sqlalchemy}
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import select

engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/db")

async def get_user(email):
    async with AsyncSession(engine) as session:
        result = await session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
```

## Performance synchrone vs asynchrone {#sync-vs-async-performance}

```yaml
Sync:  [Request1 -----] [Request2 -----] [Request3 -----]  = 1500ms
Async: [Req1 --][Req2 --][Req3 --]                          = ~500ms

Sync:  100 concurrent requests -> need 100 worker threads
Async: 100 concurrent requests -> 1 worker handles all during I/O waits
```

## Pièges {#gotchas}

- **Blocage de la boucle** : `requests.get()` et `time.sleep()` bloquent tout. Utilisez `httpx.AsyncClient` et `await asyncio.sleep()`. Pour le code synchrone inévitable : `await asyncio.to_thread(blocking_func)`
- **Coroutine non attendue** : `fetch_url(url)` sans `await` ne fait rien ; cela renvoie un objet coroutine et déclenche un `RuntimeWarning`
- **`asyncio.run()` imbriqué** : lève `RuntimeError` si la boucle est déjà en cours d'exécution. Dans Jupyter, utilisez directement `await main()`
- **`gather` avec `return_exceptions=True`** : les exceptions deviennent silencieusement des valeurs de retour, ce qui rend les échecs faciles à manquer
- FastAPI : si vous devez utiliser du code synchrone, déclarez l'endpoint avec `def` (et non `async def`) : il s'exécute dans un pool de threads

## Voir aussi {#see-also}

- [Concurrence - Threads et multiprocessing](concurrency.md) - threads et multiprocessing pour le travail lié au CPU
- [[fastapi-fundamentals]] - endpoints asynchrones
- [[fastapi-database-layer]] - sessions SQLAlchemy asynchrones
