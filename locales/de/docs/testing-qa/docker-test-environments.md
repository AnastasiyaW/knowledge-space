---
title: "Docker für Testumgebungen"
category: infrastructure
tags: [docker, docker-compose, testcontainers, containers, isolation, database, microservices]
level: 3
source_sha256: b91c8f300f7cc2abe643e4ca69032a89c051abc750c34fbdbcc663d2993eb710
translation: machine
translated_at: '2026-10-24'
---
# Docker für Testumgebungen {#docker-for-test-environments}

Dienste unter Test in Docker-Containern ausführen: Compose-Dateien für lokale Stacks, Testcontainers für den programmatischen Lebenszyklus und Muster zur CI-Integration.

## Docker Compose für den Teststack {#docker-compose-for-test-stack}

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

## Testcontainers (programmatisch) {#testcontainers-programmatic}

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

Testcontainers startet pro Fixture einen echten Docker-Container und entfernt ihn anschließend wieder.

## Multi-Service-Tests {#multi-service-testing}

```python
from testcontainers.compose import DockerCompose

@pytest.fixture(scope="session")
def compose():
    with DockerCompose(".", compose_file_name="docker-compose.test.yml") as c:
        c.wait_for("http://localhost:8000/health")
        yield c
```

## Testimages erstellen {#building-test-images}

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

## Wartestrategien {#wait-strategies}

Nach `docker compose up` niemals davon ausgehen, dass Dienste bereit sind:

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

## Volume-Mounts für Testdaten {#volume-mounts-for-test-data}

```yaml
services:
  app:
    volumes:
      - ./test-data:/app/test-data:ro
      - ./tests/fixtures:/app/fixtures:ro
```

Schreibgeschützte Mounts (`:ro`) verhindern, dass Tests versehentlich Quelldaten verändern.

## CI-Integration {#ci-integration}

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

## Stolperfallen {#gotchas}

- **Problem:** Tests instabil, weil der Dienst trotz `depends_on` nicht bereit ist. **Lösung:** Docker `depends_on` wartet nur auf den Containerstart, nicht auf die Bereitschaft der Anwendung. Immer Healthchecks oder explizite Wait-for-Port-Logik verwenden.

- **Problem:** Portkonflikte, wenn Tests lokal und in CI gleichzeitig laufen. **Lösung:** Dynamisches Port-Mapping verwenden: `ports: ["0:5432"]` und den zugewiesenen Port von Docker auslesen. Alternativ übernimmt Testcontainers dies automatisch.

- **Problem:** Docker-Volumes behalten Daten zwischen Testläufen, was zu Testverunreinigung führt. **Lösung:** `docker compose down -v` verwenden, um Volumes zu entfernen. Alternativ `tmpfs`-Mounts nutzen: `tmpfs: /var/lib/postgresql/data`.

## Siehe auch {#see-also}

- [[ci-cd-test-automation]]
- [[database-testing]]
- [[fastapi-test-services]]
