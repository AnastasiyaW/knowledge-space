---
title: "FastAPI-Deployment und Produktion"
category: frameworks
tags: [python, fastapi, docker, nginx, gunicorn, deployment, logging, monitoring]
level: 3
source_sha256: 85b19a5a241aa18c54c06eebba73d387a1595d2293289702bdfd18aedbf9a4d1
translation: machine
translated_at: '2026-10-24'
---
# FastAPI-Deployment und Produktion {#fastapi-deployment-and-production}

Produktive FastAPI-Deployments nutzen typischerweise Docker für die Containerisierung, Nginx als Reverse Proxy mit SSL-Terminierung und Gunicorn zur Verwaltung mehrerer Uvicorn-Worker. Monitoring mit Prometheus/Grafana und strukturiertes Logging vervollständigen den Produktionsstack.

## Wichtige Fakten {#key-facts}

- Produktionsarchitektur: Client -> Nginx (SSL) -> Gunicorn -> Uvicorn-Worker -> FastAPI
- Docker verpackt die App mit allen Abhängigkeiten in einen portablen Container
- `docker compose` orchestriert mehrere Dienste (App, DB, Redis, Celery)
- API-Versionierung über `fastapi-versioning` für externe Clients
- Prometheus sammelt Metriken; Grafana visualisiert; Sentry verfolgt Fehler
- Strukturiertes JSON-Logging ermöglicht maschinell auswertbare, durchsuchbare Logs

## Muster {#patterns}

### Dockerfile {#dockerfile}
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

### Docker Compose {#docker-compose}
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

In Docker Compose `localhost` durch Dienstnamen (`db`, `redis`) ersetzen, damit die Container untereinander kommunizieren können.

### Nginx-HTTPS-Konfiguration {#nginx-https-configuration}
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

SSL-Zertifikatskette: `cat domain.crt intermediate.crt root.crt > bundle.crt` (die Reihenfolge ist wichtig).

### Middleware zur Request-Zeitmessung {#request-timing-middleware}
```python
@app.middleware("http")
async def add_process_time(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    process_time = time.time() - start
    logger.info("Request", extra={"process_time": process_time, "path": request.url.path})
    return response
```

### API-Versionierung {#api-versioning}
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

### Produktionsstart {#production-launch}
```bash
# Gunicorn with Uvicorn workers
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Log-Level {#log-levels}
- **DEBUG** - Diagnose während der Entwicklung
- **INFO** - Betriebsmeldungen (gestartet, Benutzer angelegt)
- **WARNING** - behebbare Probleme
- **ERROR** - Fehler, die Aufmerksamkeit erfordern
- **CRITICAL** - Fehler auf Systemebene

## Stolperfallen {#gotchas}

- `depends_on` steuert nur die Startreihenfolge, nicht die Bereitschaft; die App kann fehlschlagen, wenn die DB noch nicht bereit ist
- Statische Dateien bzw. Admin-Panels NACH der Initialisierung von `VersionedFastAPI` einbinden
- Kostenlose Hosting-Tarife (Render.com): `workers=1` setzen und `BackgroundTasks` statt Celery verwenden
- Die Reihenfolge der SSL-Zertifikatskette ist wichtig: Domain -> Intermediate -> Root
- Die Sentry-Integration bietet Fehlererfassung mit Stack-Traces und Häufigkeitsanalysen

## Siehe auch {#see-also}

- [[fastapi-fundamentals]] - Grundlagen von FastAPI
- [[fastapi-caching-and-tasks]] - Redis-Caching, Celery
- [[devops/index]] - Docker, CI/CD, Infrastruktur
