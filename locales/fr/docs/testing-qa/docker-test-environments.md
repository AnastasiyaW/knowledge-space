---
title: "Docker pour les environnements de test"
category: infrastructure
tags: [docker, docker-compose, testcontainers, containers, isolation, database, microservices]
level: 3
source_sha256: b91c8f300f7cc2abe643e4ca69032a89c051abc750c34fbdbcc663d2993eb710
translation: machine
translated_at: '2026-10-24'
---
# Docker pour les environnements de test {#docker-for-test-environments}

Exécution des services testés dans des conteneurs Docker : fichiers compose pour les environnements locaux, testcontainers pour le cycle de vie piloté par le code, et schémas d'intégration CI.

## Docker Compose pour la pile de test {#docker-compose-for-test-stack}

```yaml
# docker-compose.test.yml
version: "3.8"
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://test:test@db:5432/testdb
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16
    environment:
      POSTGRES_USER: test
      POSTGRES_PASSWORD: test
      POSTGRES_DB: testdb
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U test"]
      interval: 5s
      timeout: 3s
      retries: 5
    ports:
      - "5432:5432"
```

```bash
# Start stack, run tests, tear down
docker compose -f docker-compose.test.yml up -d --wait
pytest tests/
docker compose -f docker-compose.test.yml down -v
```

## Testcontainers (piloté par le code) {#testcontainers-programmatic}

```python
from testcontainers.postgres import PostgresContainer

@pytest.fixture(scope="session")
def postgres():
    with PostgresContainer("postgres:16") as pg:
        yield pg

@pytest.fixture(scope="session")
def db_url(postgres):
    return postgres.get_connection_url()

def test_user_crud(db_url):
    engine = create_engine(db_url)
    # test against real PostgreSQL
```

Testcontainers démarre un conteneur Docker réel par fixture, puis le supprime après utilisation.

## Tests multi-services {#multi-service-testing}

```python
from testcontainers.compose import DockerCompose

@pytest.fixture(scope="session")
def compose():
    with DockerCompose(".", compose_file_name="docker-compose.test.yml") as c:
        c.wait_for("http://localhost:8000/health")
        yield c
```

## Construction des images de test {#building-test-images}

```dockerfile
# Dockerfile.test
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["pytest", "--tb=short", "-v"]
```

```bash
docker build -f Dockerfile.test -t myapp-tests .
docker run --network host myapp-tests
```

## Stratégies d'attente {#wait-strategies}

Ne supposez jamais que les services sont prêts après `docker compose up` :

```python
import time
import requests
from requests.exceptions import ConnectionError

def wait_for_service(url, timeout=30, interval=1):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                return
        except ConnectionError:
            pass
        time.sleep(interval)
    raise TimeoutError(f"Service {url} not ready after {timeout}s")
```

## Montages de volumes pour les données de test {#volume-mounts-for-test-data}

```yaml
services:
  app:
    volumes:
      - ./test-data:/app/test-data:ro
      - ./tests/fixtures:/app/fixtures:ro
```

Les montages en lecture seule (`:ro`) empêchent les tests de modifier accidentellement les données source.

## Intégration CI {#ci-integration}

```yaml
# .github/workflows/test.yml
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: testdb
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - run: pip install -r requirements.txt
      - run: pytest
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/testdb
```

## Pièges courants {#gotchas}

- **Problème :** Tests instables parce que le service n'est pas prêt malgré `depends_on`. **Solution :** `depends_on` de Docker attend uniquement le démarrage du conteneur, pas la disponibilité de l'application. Utilisez toujours des healthchecks ou une logique explicite d'attente de port.

- **Problème :** Conflits de ports lorsque les tests sont exécutés simultanément en local et en CI. **Solution :** Utilisez un mappage de port dynamique : `ports: ["0:5432"]` et lisez le port attribué depuis Docker. Ou utilisez testcontainers, qui gère cela automatiquement.

- **Problème :** Les volumes Docker conservent les données entre les exécutions de tests, ce qui pollue les tests. **Solution :** Utilisez `docker compose down -v` pour supprimer les volumes. Ou utilisez des montages `tmpfs` : `tmpfs: /var/lib/postgresql/data`.

## Voir aussi {#see-also}

- [[ci-cd-test-automation]]
- [[database-testing]]
- [[fastapi-test-services]]
