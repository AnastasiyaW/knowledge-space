---
title: "Docker Compose"
category: concepts
tags: [devops, docker, compose, multi-container, orchestration]
level: 3
source_sha256: 1f0107ee43c8a009777cbaa780c88a1888190ffaa22119b5095bf8afda82804c
translation: machine
translated_at: '2026-10-24'
---
# Docker Compose {#docker-compose}

Docker Compose definiert und betreibt Multi-Container-Anwendungen in einer einzigen deklarativen YAML-Datei. Es erstellt ein gemeinsames Netzwerk, in dem Services sich gegenseitig über ihren Namen auflösen, verwaltet Volumes und steuert die Startreihenfolge.

## Core Structure {#core-structure}

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

## Key Commands {#key-commands}

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

## Service Discovery {#service-discovery}

- Compose erstellt für alle Services ein standardmäßiges Bridge-Netzwerk
- Services lösen sich gegenseitig über den Service-Namen auf: `http://app:8080`
- `localhost` innerhalb eines Containers bezieht sich auf DIESEN Container, nicht auf den Host
- Dies ist die häufigste Stolperfalle beim Verbinden von Containern

## Startup Ordering {#startup-ordering}

`depends_on` steuert die Reihenfolge, wartet standardmäßig jedoch nur auf den Start des Containers, nicht auf dessen Bereitschaft:

```yaml
depends_on:
  configserver:
    condition: service_healthy   # wait for healthcheck to pass
  db:
    condition: service_started   # just wait for start (default)
```

## Environment Variables {#environment-variables}

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

Variablensubstitution in der Compose-Datei: `${VAR_NAME}` liest aus der Shell oder aus `.env` im Projektverzeichnis.

## Build Configuration {#build-configuration}

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

## Volumes {#volumes}

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

## Patterns {#patterns}

### ML Stack (JupyterLab + MLflow + API + Frontend) {#ml-stack-jupyterlab-mlflow-api-frontend}

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

### Reverse Proxy with Load Balancing (Caddy) {#reverse-proxy-with-load-balancing-caddy}

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
```kotlin
:80 {
    reverse_proxy app1:3000 app2:3000 {
        lb_policy round_robin
        health_uri /health
        health_interval 10s
    }
}
```

### Microservices Stack (Spring Boot) {#microservices-stack-spring-boot}

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

### Docker Model Runner (Local LLM) {#docker-model-runner-local-llm}

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

Provider erweitern Compose, um sich mit Docker-Plugins wie Model Runner zu verbinden (nur Apple Silicon).

## Gotchas {#gotchas}

- Port-Konflikte: Mehrere Services können nicht denselben Host-Port binden
- `depends_on` ohne `condition: service_healthy` wartet nur auf den Start des Containers, nicht auf die Bereitschaft der Anwendung
- Named Volumes bleiben über `docker compose down` hinaus erhalten – mit dem Flag `--volumes` werden sie zusätzlich entfernt
- Die `.env`-Datei wird nur aus dem Projektstammverzeichnis automatisch geladen
- `docker compose` (v2) ersetzt `docker-compose` (v1) – anderes Binary, gleiche Funktionalität

## See Also {#see-also}

- [[docker-fundamentals]] - Grundlagen zu Containern, Netzwerken und Volumes
- [[dockerfile-and-image-building]] - Erstellen eigener Images
- [[docker-for-ml]] - ML-spezifische Docker-Workflows
- [[kubernetes-architecture]] - wenn Compose nicht mehr ausreicht
