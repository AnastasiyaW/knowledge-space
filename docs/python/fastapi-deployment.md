---
title: FastAPI Deployment and Production
category: frameworks
tags: [python, fastapi, docker, nginx, gunicorn, deployment, logging, monitoring]
---

# FastAPI Deployment and Production

Production FastAPI deployments typically use Docker for containerization, Nginx as reverse proxy with SSL termination, and Gunicorn managing multiple Uvicorn workers. Monitoring with Prometheus/Grafana and structured logging complete the production stack.

## Key Facts

- Production architecture: Client -> Nginx (SSL) -> Gunicorn -> Uvicorn workers -> FastAPI
- Docker wraps the app with all dependencies into a portable container
- `docker compose` orchestrates multiple services (app, DB, Redis, Celery)
- API versioning via `fastapi-versioning` for external clients
- Prometheus collects metrics; Grafana visualizes; Sentry tracks errors
- Structured JSON logging enables machine-parseable, searchable logs

## Patterns

### Dockerfile
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

```bash
docker build .
docker run -p 1234:8000 <image>  # host:container port mapping
```

### Docker Compose
```yaml
services:
  db:
    image: postgres:15
    env_file: .env-non-dev
  redis:
    image: redis:7
  booking:
    build: .
    ports:
      - "7777:8000"
    depends_on:
      - db
      - redis
    env_file: .env-non-dev
  celery:
    build: .
    command: celery -A celery_config worker
    depends_on:
      - redis
  flower:
    build: .
    command: celery flower
    ports:
      - "5555:5555"
```

In Docker Compose, replace `localhost` with service names (`db`, `redis`) for inter-container networking.

### Nginx HTTPS Configuration
```nginx
server {
    listen 80;
    server_name example.ru;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name example.ru;
    ssl_certificate /etc/nginx/ssl/bundle.crt;
    ssl_certificate_key /etc/nginx/ssl/private.key;

    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:8000;
    }
}
```

SSL certificate bundle: `cat domain.crt intermediate.crt root.crt > bundle.crt` (order matters).

### Request Timing Middleware
```python
@app.middleware("http")
async def add_process_time(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    process_time = time.time() - start
    logger.info("Request", extra={"process_time": process_time, "path": request.url.path})
    return response
```

### API Versioning
```python
from fastapi_versioning import VersionedFastAPI, version

@router.get("/bookings")
@version(1)
async def get_bookings_v1(): ...

@router.post("/bookings")
@version(2)
async def create_booking_v2(): ...
# Docs at /v1/docs, /v2/docs
```

### Production Launch
```bash
# Gunicorn with Uvicorn workers
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Log Levels
- **DEBUG** - development diagnostics
- **INFO** - operational messages (started, user created)
- **WARNING** - recoverable issues
- **ERROR** - failures requiring attention
- **CRITICAL** - system-level failures

## Gotchas

- `depends_on` only controls startup order, not readiness - app may fail if DB isn't ready yet
- Mount static files / admin panels AFTER `VersionedFastAPI` initialization
- Free tier hosting (Render.com): set workers=1, use BackgroundTasks instead of Celery
- SSL bundle certificate order matters: domain -> intermediate -> root
- Sentry integration provides error tracking with stack traces and frequency analytics

## See Also

- [[fastapi-fundamentals]] - core FastAPI concepts
- [[fastapi-caching-and-tasks]] - Redis caching, Celery
- [[devops/index]] - Docker, CI/CD, infrastructure
