---
title: "Mise en cache et tâches en arrière-plan avec FastAPI"
category: frameworks
tags: [python, fastapi, redis, celery, caching, background-tasks, task-queues]
level: 3
source_sha256: 08d9500f973fb78149fd22f24b1d14b4ec6a1a67359b7b5e06dfc4a278fc7eb6
translation: machine
translated_at: '2026-10-24'
---
# Mise en cache et tâches en arrière-plan avec FastAPI {#fastapi-caching-and-background-tasks}

La mise en cache avec Redis réduit la charge sur la base de données ; les tâches en arrière-plan déportent les opérations longues hors du cycle requête-réponse. FastAPI fournit `BackgroundTasks`, une solution légère intégrée, ainsi que Celery pour le traitement distribué de tâches lourdes ou critiques.

## Points clés {#key-facts}

- Redis : magasin clé-valeur en mémoire (port 6379) pour le cache, les sessions et les files de tâches
- `fastapi-cache2[redis]` fournit la mise en cache des endpoints par décorateur
- Celery : file de tâches distribuée nécessitant un broker (Redis/RabbitMQ) et un backend de résultats
- `BackgroundTasks` : intégré, sans configuration, même processus - adapté aux tâches simples de type fire-and-forget
- `.delay()` envoie la tâche à un worker Celery de manière asynchrone ; `.apply_async()` pour les options avancées

## Patterns {#patterns}

### Mise en cache Redis avec fastapi-cache2 {#redis-caching-with-fastapi-cache2}
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

### Configuration de Celery {#celery-setup}
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

### Appeler Celery depuis FastAPI {#calling-celery-from-fastapi}
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

### Fonctionnalités avancées de Celery {#celery-advanced-features}
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

### BackgroundTasks de FastAPI (intégré) {#fastapi-backgroundtasks-built-in}
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

### Structures de données des files {#queue-data-structures}
```python
from queue import Queue, LifoQueue, PriorityQueue

q = Queue()           # FIFO
q.put("first"); q.get()  # "first"

stack = LifoQueue()   # LIFO (stack)
stack.put("a"); stack.put("b"); stack.get()  # "b"

pq = PriorityQueue()  # lowest value first
pq.put((3, "low")); pq.put((1, "high")); pq.get()  # (1, "high")
```

## BackgroundTasks vs Celery {#backgroundtasks-vs-celery}

| Fonctionnalité | BackgroundTasks | Celery |
|----------------|-----------------|--------|
| Mise en place | Aucune configuration | Nécessite Redis/RabbitMQ |
| Mise à l'échelle | Même processus | Workers séparés |
| Supervision | Aucune | Tableau de bord Flower |
| Relances/priorité | Manuelles | Intégrées |
| Tâches périodiques | Non | Celery Beat |
| Idéal pour | Fire-and-forget rapide | Tâches lourdes/critiques |

## Pièges à éviter {#gotchas}

- Les objets ORM SQLAlchemy ne sont pas sérialisables en JSON - les convertir en Pydantic avant la mise en cache
- L'encodeur interne de `fastapi-cache` échoue sur les instances ORM brutes - les valider d'abord via Pydantic
- `.scalars().all()` pour les requêtes sur un seul modèle ; `.all()` pour les requêtes multi-colonnes (scalars élimine silencieusement des colonnes)
- Les arguments des tâches Celery doivent être sérialisables en JSON (pas d'objets complexes)
- `on_event("startup")` est déprécié dans les versions récentes de FastAPI - utiliser le gestionnaire de contexte lifespan

## Voir aussi {#see-also}

- [[fastapi-fundamentals]] - endpoints, dépendances
- [[profiling-and-optimization]] - stratégies de mise en cache
- [[async-programming]] - patterns asynchrones
