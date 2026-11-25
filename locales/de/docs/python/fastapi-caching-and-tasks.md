---
title: "FastAPI-Caching und Hintergrundaufgaben"
category: frameworks
tags: [python, fastapi, redis, celery, caching, background-tasks, task-queues]
level: 3
source_sha256: 08d9500f973fb78149fd22f24b1d14b4ec6a1a67359b7b5e06dfc4a278fc7eb6
translation: machine
translated_at: '2026-10-24'
---
# FastAPI-Caching und Hintergrundaufgaben {#fastapi-caching-and-background-tasks}

Caching mit Redis reduziert die Datenbanklast; Hintergrundaufgaben lagern länger laufende Operationen aus dem Request-Response-Zyklus aus. FastAPI unterstützt die leichtgewichtigen, eingebauten `BackgroundTasks` sowie Celery für aufwendige bzw. kritische verteilte Task-Verarbeitung.

## Wichtige Fakten {#key-facts}

- Redis: In-Memory-Key-Value-Store (Port 6379) für Caching, Sessions, Task-Queues
- `fastapi-cache2[redis]` stellt decoratorbasiertes Endpoint-Caching bereit
- Celery: verteilte Task-Queue, benötigt einen Broker (Redis/RabbitMQ) und ein Result-Backend
- `BackgroundTasks`: eingebaut, ohne Konfiguration, gleicher Prozess - geeignet für einfaches Fire-and-forget
- `.delay()` sendet einen Task asynchron an einen Celery-Worker; `.apply_async()` für erweiterte Optionen

## Muster {#patterns}

### Redis-Caching mit fastapi-cache2 {#redis-caching-with-fastapi-cache2}
```python
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost:6379", encoding="utf8")
    FastAPICache.init(RedisBackend(redis), prefix="cache")

@router.get("/hotels")
@cache(expire=30)  # cache for 30 seconds
async def get_hotels():
    hotels = await HotelDAO.find_all()
    # Convert to Pydantic BEFORE cache decorator processes response
    return parse_obj_as(list[SHotel], hotels)
```

### Celery-Einrichtung {#celery-setup}
```python
from celery import Celery

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
)

@celery_app.task
def process_image(path: str):
    img = Image.open(path)
    img.save(f"processed_{path}")
    return f"Processed: {path}"

@celery_app.task
def send_email(to: str, subject: str, body: str):
    # Email sending logic
    return f"Sent to {to}"
```

### Celery aus FastAPI aufrufen {#calling-celery-from-fastapi}
```python
@app.post("/upload")
async def upload(file: UploadFile):
    path = save_file(file)
    task = process_image.delay(path)  # async to Celery
    return {"task_id": task.id}

@app.get("/task/{task_id}")
async def get_status(task_id: str):
    from celery.result import AsyncResult
    result = AsyncResult(task_id)
    return {
        "status": result.status,  # PENDING, STARTED, SUCCESS, FAILURE
        "result": result.result if result.ready() else None,
    }
```

```bash
celery -A celery_config worker --loglevel=info --concurrency=4
celery -A celery_config flower  # web dashboard at :5555
```

### Erweiterte Celery-Funktionen {#celery-advanced-features}
```python
# Retry on failure
@celery_app.task(bind=True, max_retries=3)
def fetch_data(self, url):
    try:
        return requests.get(url).json()
    except Exception as exc:
        self.retry(exc=exc, countdown=60)

# Task chains and groups
from celery import chain, group
chain(task1.s(arg), task2.s())()        # sequential pipeline
group(task.s(i) for i in range(10))()   # parallel execution
```

### FastAPI BackgroundTasks (eingebaut) {#fastapi-backgroundtasks-built-in}
```python
from fastapi import BackgroundTasks

def write_log(message: str):
    with open("log.txt", "a") as f:
        f.write(f"{message}\n")

@app.post("/items/")
async def create_item(background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, "Item created")
    return {"status": "created"}
```

### Datenstrukturen für Queues {#queue-data-structures}
```python
from queue import Queue, LifoQueue, PriorityQueue

q = Queue()           # FIFO
q.put("first"); q.get()  # "first"

stack = LifoQueue()   # LIFO (stack)
stack.put("a"); stack.put("b"); stack.get()  # "b"

pq = PriorityQueue()  # lowest value first
pq.put((3, "low")); pq.put((1, "high")); pq.get()  # (1, "high")
```

## BackgroundTasks vs. Celery {#backgroundtasks-vs-celery}

| Merkmal | BackgroundTasks | Celery |
|---------|----------------|--------|
| Einrichtung | Ohne Konfiguration | Benötigt Redis/RabbitMQ |
| Skalierung | Gleicher Prozess | Separate Worker |
| Monitoring | Keines | Flower-Dashboard |
| Wiederholung/Priorität | Manuell | Eingebaut |
| Periodische Tasks | Nein | Celery Beat |
| Ideal für | Schnelles Fire-and-forget | Aufwendige/kritische Tasks |

## Fallstricke {#gotchas}

- SQLAlchemy-ORM-Objekte sind nicht JSON-serialisierbar - vor dem Caching in Pydantic-Modelle umwandeln
- Der interne Encoder von `fastapi-cache` scheitert an rohen ORM-Instanzen - vorher über Pydantic validieren
- `.scalars().all()` für Abfragen eines einzelnen Modells; `.all()` für mehrspaltige Abfragen (`scalars` verwirft Spalten stillschweigend)
- Argumente von Celery-Tasks müssen JSON-serialisierbar sein (keine komplexen Objekte)
- `on_event("startup")` ist in neueren FastAPI-Versionen veraltet - stattdessen den Lifespan-Context-Manager verwenden

## Siehe auch {#see-also}

- [[fastapi-fundamentals]] - Endpoints, Dependencies
- [[profiling-and-optimization]] - Caching-Strategien
- [[async-programming]] - Async-Muster
