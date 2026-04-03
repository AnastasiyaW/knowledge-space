---
title: Docker for Data Engineering
category: tools
tags: [data-engineering, docker, containers, devops, deployment]
---

# Docker for Data Engineering

Docker provides isolated, reproducible environments for data engineering workloads. Containers package applications with dependencies, ensuring identical dev/test/prod environments.

## Containers vs VMs

| Feature | Containers | VMs |
|---------|-----------|-----|
| OS | Share host kernel | Full guest OS |
| Weight | Lightweight | Heavy |
| Startup | Seconds | Minutes |
| IaC tools | Dockerfile, docker-compose | Vagrant |

## Core Concepts
- **Image** - read-only template (blueprint)
- **Container** - running instance of an image
- **Layer** - each Dockerfile instruction creates a cached layer
- **Volume** - persistent storage outside container lifecycle
- **Registry** - image storage (Docker Hub, private)

## Essential Commands

```bash
# Run container
docker run --rm --name pg \
  -e POSTGRES_PASSWORD=test \
  -p 5432:5432 \
  -v $(pwd)/data:/var/lib/postgresql/data \
  -d postgres:14

# Management
docker ps                         # list running
docker exec -it pg psql -U postgres  # shell into container
docker logs --tail=10 -f pg      # follow logs
docker stop pg && docker rm pg

# Docker Compose
docker compose up -d              # start in background
docker compose ps                 # list services
docker compose logs --tail=100 -f
docker compose down               # stop + remove
```

## Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "etl.py"]
```

## Docker Compose

```yaml
version: '3.8'
services:
  postgres:
    image: postgres:14
    restart: always
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_PASSWORD=secret
    volumes:
      - pgdata:/var/lib/postgresql/data
volumes:
  pgdata:
```

## Best Practices
- **1 application = 1 container**
- Configure via **environment variables** (no rebuilds for config changes)
- **Persistent data on volumes** (container restarts don't lose data)
- Never store passwords in Dockerfile or docker-compose.yml

## Gotchas
- Env var changes: `docker compose restart` is NOT enough - must stop/rm/up
- Build context: keep only necessary files in Dockerfile directory
- Windows/Mac: Docker runs in a Linux VM (WSL2 or VirtualBox)
- After env var changes in docker-compose.yml, full recreate required

## See Also
- [[kubernetes-for-de]] - container orchestration at scale
- [[cloud-data-platforms]] - cloud deployment
- [[apache-airflow]] - Airflow in Docker
