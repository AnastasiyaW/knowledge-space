---
title: Docker Deployment
category: reference
tags: [python, docker, dockerfile, docker-compose, gunicorn, uvicorn, deployment, containerization]
---

# Docker Deployment

Containerizing Python applications with Docker provides reproducible, isolated deployments. Multi-stage builds minimize image size. Gunicorn with Uvicorn workers is the standard production ASGI server setup for FastAPI applications.

## Key Facts

- Multi-stage Docker builds separate build dependencies from runtime, reducing image size by 50-80%
- `python:3.11-slim` (~150MB) is the recommended base; `alpine` saves space but has musl/glibc compatibility issues
- Gunicorn manages worker processes; Uvicorn workers handle async requests: `gunicorn -k uvicorn.workers.UvicornWorker`
- Workers formula: `2 * CPU_CORES + 1` for sync, `1 * CPU_CORES` for async (Uvicorn workers are single-threaded event loops)
- Non-root user in containers is a security best practice
- `.dockerignore` excludes `.git`, `__pycache__`, `.venv`, `.env`, `node_modules`
- `docker compose` (v2, no hyphen) replaces `docker-compose` (v1)
- Health checks verify container readiness: `HEALTHCHECK CMD curl -f http://localhost:8000/health`
- See [[fastapi-fundamentals]] for the application, [[packaging-and-project-structure]] for project layout

## Patterns

### Multi-Stage Dockerfile for FastAPI

```dockerfile
# Stage 1: Build dependencies
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build tools (needed for some packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Create non-root user
RUN useradd --create-home appuser
USER appuser

# Copy application code
COPY --chown=appuser:appuser . .

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD ["gunicorn", "myapp.main:app", \
     "-k", "uvicorn.workers.UvicornWorker", \
     "-b", "0.0.0.0:8000", \
     "-w", "4", \
     "--access-logfile", "-"]
```

### `.dockerignore`

```
.git
.gitignore
__pycache__
*.pyc
.venv
.env
.env.*
*.egg-info
dist
build
.mypy_cache
.pytest_cache
.ruff_cache
node_modules
*.md
tests/
docs/
```

### Docker Compose for Full Stack

```yaml
# docker-compose.yml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:secret@db:5432/mydb
      - REDIS_URL=redis://redis:6379
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: secret
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

  worker:
    build: .
    command: celery -A myapp.tasks worker -l info -c 4
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:secret@db:5432/mydb
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis

volumes:
  postgres_data:
  redis_data:
```

### Gunicorn Configuration File

```python
# gunicorn.conf.py
import multiprocessing

# Workers
workers = multiprocessing.cpu_count()
worker_class = "uvicorn.workers.UvicornWorker"

# Binding
bind = "0.0.0.0:8000"

# Timeouts
timeout = 120
graceful_timeout = 30
keepalive = 5

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Process naming
proc_name = "myapp"

# Limits
max_requests = 1000           # restart worker after N requests (prevent memory leaks)
max_requests_jitter = 50      # randomize restart to avoid thundering herd
```

### Production-Ready Health Check Endpoint

```python
from fastapi import FastAPI
from sqlalchemy import text

@app.get("/health")
async def health_check(db: DBSession):
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "database": str(e)},
        )
```

### Alembic Migrations in Docker

```dockerfile
# Run migrations before starting the app
CMD ["sh", "-c", "alembic upgrade head && gunicorn myapp.main:app -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000"]
```

```yaml
# Or as a separate init container in docker-compose
services:
  migrate:
    build: .
    command: alembic upgrade head
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:secret@db:5432/mydb
    depends_on:
      db:
        condition: service_healthy
```

## Gotchas

- **Alpine images and Python**: `python:3.11-alpine` uses musl libc instead of glibc. Many Python packages (numpy, pandas, Pillow) need compilation from source, making builds slower and images larger than `slim`. Use `slim` unless you need Alpine's small footprint for simple apps
- **Layer caching for dependencies**: copy `requirements.txt` and install BEFORE copying source code. This way, `pip install` layer is cached when only code changes
- **Running as root in containers**: default Docker user is root. A compromised container running as root has elevated access. Always create and switch to a non-root user
- **`--reload` in production**: `uvicorn --reload` watches for file changes -- do NOT use in production. It adds overhead and is a security risk. Use in dev only
- **Gunicorn `--preload` with async workers**: `--preload` forks after loading the app. This can cause issues with async event loops (loop created in parent, forked into children). Test thoroughly or avoid `--preload` with Uvicorn workers

## See Also

- [Docker Python Guide](https://docs.docker.com/language/python/)
- [Uvicorn deployment](https://www.uvicorn.org/deployment/)
- [[fastapi-fundamentals]] - application setup
- [[packaging-and-project-structure]] - project layout for Docker builds
