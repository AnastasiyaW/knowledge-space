---
title: Docker for Test Environments
category: infrastructure
tags: [docker, docker-compose, testcontainers, containers, isolation, database, microservices]
---

# Docker for Test Environments

Running services under test in Docker containers: compose files for local stacks, testcontainers for programmatic lifecycle, and CI integration patterns.

## Docker Compose for Test Stack

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

## Testcontainers (Programmatic)

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

Testcontainers starts a real Docker container per fixture, tears it down after.

## Multi-Service Testing

```python
from testcontainers.compose import DockerCompose

@pytest.fixture(scope="session")
def compose():
    with DockerCompose(".", compose_file_name="docker-compose.test.yml") as c:
        c.wait_for("http://localhost:8000/health")
        yield c
```

## Building Test Images

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

## Wait Strategies

Never assume services are ready after `docker compose up`:

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

## Volume Mounts for Test Data

```yaml
services:
  app:
    volumes:
      - ./test-data:/app/test-data:ro
      - ./tests/fixtures:/app/fixtures:ro
```

Read-only mounts (`:ro`) prevent tests from accidentally modifying source data.

## CI Integration

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

## Gotchas

- **Issue:** Tests flaky because service not ready despite `depends_on`. **Fix:** Docker `depends_on` only waits for container start, not application readiness. Always use healthchecks or explicit wait-for-port logic.

- **Issue:** Port conflicts when running tests locally and in CI simultaneously. **Fix:** Use dynamic port mapping: `ports: ["0:5432"]` and read assigned port from Docker. Or use testcontainers which handles this automatically.

- **Issue:** Docker volumes persist data between test runs, causing test pollution. **Fix:** Use `docker compose down -v` to remove volumes. Or use `tmpfs` mounts: `tmpfs: /var/lib/postgresql/data`.

## See Also

- [[ci-cd-test-automation]]
- [[database-testing]]
- [[fastapi-test-services]]
