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

Docker Compose définit et exécute des applications multi-conteneurs dans un seul fichier YAML déclaratif. Il crée un réseau partagé où les services se résolvent mutuellement par leur nom, gère les volumes et contrôle l'ordre de démarrage.

## Structure de base {#core-structure}

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

## Commandes principales {#key-commands}

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

## Découverte des services {#service-discovery}

- Compose crée un réseau bridge par défaut pour tous les services
- Les services se résolvent mutuellement par leur nom de service : `http://app:8080`
- `localhost` à l'intérieur d'un conteneur désigne CE conteneur, et non l'hôte
- C'est le piège le plus courant lors de la connexion de conteneurs

## Ordre de démarrage {#startup-ordering}

`depends_on` contrôle l'ordre, mais par défaut il attend uniquement le démarrage du conteneur, et non sa disponibilité :

```yaml
depends_on:
  configserver:
    condition: service_healthy   # wait for healthcheck to pass
  db:
    condition: service_started   # just wait for start (default)
```

## Variables d'environnement {#environment-variables}

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

Substitution de variables dans le fichier compose : `${VAR_NAME}` lit la valeur depuis le shell ou depuis le `.env` à la racine du projet.

## Configuration de build {#build-configuration}

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

## Modèles {#patterns}

### Stack ML (JupyterLab + MLflow + API + Frontend) {#ml-stack-jupyterlab-mlflow-api-frontend}

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

### Reverse proxy avec répartition de charge (Caddy) {#reverse-proxy-with-load-balancing-caddy}

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

Caddyfile :
```kotlin
:80 {
    reverse_proxy app1:3000 app2:3000 {
        lb_policy round_robin
        health_uri /health
        health_interval 10s
    }
}
```

### Stack microservices (Spring Boot) {#microservices-stack-spring-boot}

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

### Docker Model Runner (LLM local) {#docker-model-runner-local-llm}

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

Les providers étendent Compose pour se connecter à des plugins Docker comme Model Runner (Apple Silicon uniquement).

## Pièges {#gotchas}

- Conflits de ports : plusieurs services ne peuvent pas se lier au même port hôte
- `depends_on` sans `condition: service_healthy` attend uniquement le démarrage du conteneur, et non la disponibilité de l'application
- Les volumes nommés persistent après `docker compose down` ; utilisez le flag `--volumes` pour les supprimer également
- Le fichier `.env` n'est chargé automatiquement que depuis le répertoire racine du projet
- `docker compose` (v2) remplace `docker-compose` (v1) : binaire différent, mêmes fonctionnalités

## Voir aussi {#see-also}

- [[docker-fundamentals]] - bases des conteneurs, réseaux, volumes
- [[dockerfile-and-image-building]] - construction d'images personnalisées
- [[docker-for-ml]] - workflows Docker spécifiques au ML
- [[kubernetes-architecture]] - quand vous dépassez Compose
