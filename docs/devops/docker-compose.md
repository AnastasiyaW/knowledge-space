---
title: Docker Compose
category: containers
tags: [docker-compose, multi-container, services, volumes, networks]
---
# Docker Compose

Declarative multi-container application definition and orchestration for development and simple production.

## Key Facts

- Compose file (`docker-compose.yml` / `compose.yaml`) defines services, networks, volumes as YAML
- Each **service** maps to one container (or multiple replicas in Swarm mode)
- `docker compose up -d` starts all services in detached mode; `docker compose down` stops and removes
- **Depends_on** controls startup order but NOT readiness; use healthchecks for actual readiness
- Services on same Compose network resolve each other by service name (built-in DNS)
- **Volumes** persist data across container restarts; named volumes managed by Docker, bind mounts map host paths
- `.env` file in same directory auto-loaded for variable substitution in compose file
- Compose V2 is a Docker CLI plugin (`docker compose`); V1 was standalone binary (`docker-compose`)
- [[docker-images-containers]] define the image each service runs
- [[docker-networking]] Compose creates a default bridge network per project

## Patterns

```yaml
# docker-compose.yml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/mydb
      - REDIS_URL=redis://cache:6379
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_started
    volumes:
      - ./src:/app/src          # bind mount for dev
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 5s
      timeout: 3s
      retries: 5

  cache:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  pgdata:
```

```bash
# Lifecycle commands
docker compose up -d                   # start all services
docker compose up -d --build           # rebuild images then start
docker compose down                    # stop and remove containers
docker compose down -v                 # also remove named volumes
docker compose restart app             # restart single service

# Monitoring
docker compose ps                      # list service status
docker compose logs -f app             # follow logs for service
docker compose top                     # show running processes

# Scaling (Compose V2)
docker compose up -d --scale app=3     # run 3 replicas of app

# Execute command in running service
docker compose exec app /bin/sh
docker compose exec db psql -U user mydb

# Override for dev/prod
docker compose -f compose.yaml -f compose.prod.yaml up -d
```

## Gotchas

- `depends_on` only waits for container start, not application readiness; always add `healthcheck` + `condition: service_healthy`
- `docker compose down` removes containers but NOT volumes; use `-v` flag to also remove volumes
- Port conflicts: if host port is already in use, compose fails silently on that service
- Environment variables in `.env` are only for compose file interpolation; use `env_file` directive for container env
- Volume data persists across `down`/`up` cycles; this is a feature, not a bug - but can cause stale data issues
- Build context `.` sends entire directory; use `.dockerignore` to exclude large files

## See Also

- [[docker-images-containers]] - Dockerfile and image building
- [[docker-networking]] - network modes and service discovery
- [[kubernetes-pods]] - for production orchestration beyond Compose
- [[helm-charts]] - Kubernetes equivalent of Compose templating
- Compose specification: https://docs.docker.com/compose/compose-file/
