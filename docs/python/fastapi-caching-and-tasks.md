---
title: FastAPI Caching and Background Tasks
category: frameworks
tags: [python, fastapi, redis, celery, caching, background-tasks, task-queues]
---

# FastAPI Caching and Background Tasks

Caching with Redis reduces database load; background tasks offload long-running operations from the request-response cycle. FastAPI supports lightweight `BackgroundTasks` built-in, and Celery for heavy/critical distributed task processing.

## Key Facts

- Redis: in-memory key-value store (port 6379) for caching, sessions, task queues
- `fastapi-cache2[redis]` provides decorator-based endpoint caching
- Celery: distributed task queue needing broker (Redis/RabbitMQ) + result backend
- `BackgroundTasks`: built-in, zero-config, same-process - good for simple fire-and-forget
- `.delay()` sends task to Celery worker asynchronously; `.apply_async()` for advanced options

## Patterns

### Redis Caching with fastapi-cache2
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

### Celery Setup
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

### Calling Celery from FastAPI
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

### Celery Advanced Features
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

### FastAPI BackgroundTasks (Built-in)
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

### Queue Data Structures
```python
from queue import Queue, LifoQueue, PriorityQueue

q = Queue()           # FIFO
q.put("first"); q.get()  # "first"

stack = LifoQueue()   # LIFO (stack)
stack.put("a"); stack.put("b"); stack.get()  # "b"

pq = PriorityQueue()  # lowest value first
pq.put((3, "low")); pq.put((1, "high")); pq.get()  # (1, "high")
```

## BackgroundTasks vs Celery

| Feature | BackgroundTasks | Celery |
|---------|----------------|--------|
| Setup | Zero config | Needs Redis/RabbitMQ |
| Scaling | Same process | Separate workers |
| Monitoring | None | Flower dashboard |
| Retry/priority | Manual | Built-in |
| Periodic tasks | No | Celery Beat |
| Best for | Quick fire-and-forget | Heavy/critical tasks |

## Gotchas

- SQLAlchemy ORM objects are not JSON-serializable - convert to Pydantic before caching
- `fastapi-cache` internal encoder fails on raw ORM instances - pre-validate through Pydantic
- `.scalars().all()` for single-model queries; `.all()` for multi-column (scalars silently drops columns)
- Celery task arguments must be JSON-serializable (no complex objects)
- `on_event("startup")` is deprecated in newer FastAPI - use lifespan context manager

## See Also

- [[fastapi-fundamentals]] - endpoints, dependencies
- [[profiling-and-optimization]] - caching strategies
- [[async-programming]] - async patterns
