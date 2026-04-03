---
title: Docker Compose
category: concepts
tags: [devops, docker, compose, multi-container, orchestration]
---

# Docker Compose

Docker Compose defines and runs multi-container applications in a single declarative YAML file. It creates a shared network where services resolve each other by name, manages volumes, and handles startup ordering.

## Core Structure

```yaml
services:
  db:
    image: mariadb:10
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_PASS}
    volumes:
      - db-data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "healthcheck.sh", "--connect"]
      interval: 30s
      timeout: 10s
      retries: 3

  app:
    build: ./app
    ports:
      - "8080:80"
    depends_on:
      db:
        condition: service_healthy
    env_file: .env

  frontend:
    build: ./ui
    ports:
      - "3000:3000"
    environment:
      - API_URL=http://app:8080    # service name as hostname
    depends_on:
      - app

volumes:
  db-data:
```

## Key Commands

```bash
docker compose build         # build all images
docker compose up -d         # start all services detached
docker compose down          # stop and remove containers + networks
docker compose down --volumes  # also remove volumes
docker compose logs -f       # follow all logs
docker compose logs -f app   # follow specific service
docker compose ps            # list services
docker compose exec app sh   # shell into running service
docker compose restart app   # restart specific service
```

## Service Discovery

- Compose creates a default bridge network for all services
- Services resolve each other by service name: `http://app:8080`
- `localhost` inside a container refers to THAT container, not the host
- This is the most common gotcha when connecting containers

## Startup Ordering

`depends_on` controls order but by default only waits for container start, not readiness:

```yaml
depends_on:
  configserver:
    condition: service_healthy   # wait for healthcheck to pass
  db:
    condition: service_started   # just wait for start (default)
```

## Environment Variables

```yaml
services:
  app:
    environment:
      - DB_HOST=db
      - DB_PORT=3306
    env_file: .env              # load from file
    env_file:
      - .env
      - .env.local              # override order
```

Variable substitution in compose file: `${VAR_NAME}` reads from shell or `.env` in project root.

## Build Configuration

```yaml
services:
  app:
    build:
      context: ./src/api        # build context path
      dockerfile: Dockerfile    # custom Dockerfile name
      args:
        VERSION: "3.11"         # build arguments
    image: myapp:latest         # tag the built image
```

## Volumes

```yaml
services:
  db:
    volumes:
      - db-data:/var/lib/mysql        # named volume
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql  # bind mount
      - /host/path:/container/path:ro  # read-only bind mount

volumes:
  db-data:                             # declare named volumes
```

## Patterns

### ML Stack (JupyterLab + MLflow + API + Frontend)

```yaml
services:
  mlflow:
    image: ghcr.io/mlflow/mlflow:latest
    ports: ["5555:5000"]
    command: mlflow server --host 0.0.0.0

  api:
    build: ./src/api
    ports: ["8000:8000"]
    depends_on: [mlflow]

  streamlit:
    build: ./src/streamlit
    ports: ["8501:8501"]
    environment:
      - API_URL=http://api:8000
    depends_on: [api]
```

### Reverse Proxy with Load Balancing (Caddy)

```yaml
services:
  caddy:
    image: caddy:latest
    ports: ["80:80", "443:443"]
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile

  app1:
    build: ./app
    expose: ["3000"]
  app2:
    build: ./app
    expose: ["3000"]
```

Caddyfile:
```
:80 {
    reverse_proxy app1:3000 app2:3000 {
        lb_policy round_robin
        health_uri /health
        health_interval 10s
    }
}
```

### Microservices Stack (Spring Boot)

```yaml
services:
  configserver:
    image: myorg/configserver:latest
    ports: ["8071:8071"]
    healthcheck:
      test: curl -f http://localhost:8071/actuator/health
      interval: 10s
      retries: 5

  eurekaserver:
    image: myorg/eurekaserver:latest
    depends_on:
      configserver: { condition: service_healthy }

  accounts:
    image: myorg/accounts:latest
    depends_on:
      configserver: { condition: service_healthy }
      eurekaserver: { condition: service_healthy }
    environment:
      SPRING_CONFIG_IMPORT: configserver:http://configserver:8071
```

### Docker Model Runner (Local LLM)

```yaml
services:
  api:
    build: ./app
    ports: ["8000:8000"]

  ai-runner:
    provider:
      type: model
      options:
        model: ai/smollm2
```

Providers extend Compose to connect to Docker plugins like Model Runner (Apple Silicon only).

## Gotchas

- Port conflicts: multiple services cannot bind the same host port
- `depends_on` without `condition: service_healthy` only waits for container start, not application readiness
- Named volumes persist across `docker compose down` - use `--volumes` flag to also remove them
- `.env` file is auto-loaded only from the project root directory
- `docker compose` (v2) replaces `docker-compose` (v1) - different binary, same functionality

## See Also

- [[docker-fundamentals]] - container basics, networking, volumes
- [[dockerfile-and-image-building]] - building custom images
- [[docker-for-ml]] - ML-specific Docker workflows
- [[kubernetes-architecture]] - when you outgrow Compose
