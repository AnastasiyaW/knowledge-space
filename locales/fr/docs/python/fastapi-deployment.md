---
title: "Déploiement et mise en production de FastAPI"
category: frameworks
tags: [python, fastapi, docker, nginx, gunicorn, deployment, logging, monitoring]
level: 3
source_sha256: 85b19a5a241aa18c54c06eebba73d387a1595d2293289702bdfd18aedbf9a4d1
translation: machine
translated_at: '2026-10-24'
---
# Déploiement et mise en production de FastAPI {#fastapi-deployment-and-production}

Les déploiements FastAPI en production utilisent généralement Docker pour la conteneurisation, Nginx comme reverse proxy avec terminaison SSL, et Gunicorn qui gère plusieurs workers Uvicorn. La supervision avec Prometheus/Grafana et la journalisation structurée complètent la stack de production.

## Points clés {#key-facts}

- Architecture de production : Client -> Nginx (SSL) -> Gunicorn -> workers Uvicorn -> FastAPI
- Docker encapsule l'application avec toutes ses dépendances dans un conteneur portable
- `docker compose` orchestre plusieurs services (application, base de données, Redis, Celery)
- Versionnement de l'API via `fastapi-versioning` pour les clients externes
- Prometheus collecte les métriques, Grafana les visualise, Sentry suit les erreurs
- La journalisation JSON structurée produit des logs lisibles par machine et facilement consultables

## Patterns {#patterns}

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

Dans Docker Compose, remplacez `localhost` par les noms des services (`db`, `redis`) pour la communication entre conteneurs.

### Configuration HTTPS avec Nginx {#nginx-https-configuration}
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

Bundle de certificats SSL : `cat domain.crt intermediate.crt root.crt > bundle.crt` (l'ordre est important).

### Middleware de mesure du temps de requête {#request-timing-middleware}
```python
@app.middleware("http")
async def add_process_time(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    process_time = time.time() - start
    logger.info("Request", extra={"process_time": process_time, "path": request.url.path})
    return response
```

### Versionnement de l'API {#api-versioning}
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

### Lancement en production {#production-launch}
```bash
# Gunicorn with Uvicorn workers
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Niveaux de log {#log-levels}
- **DEBUG** - diagnostic en développement
- **INFO** - messages opérationnels (démarrage, création d'utilisateur)
- **WARNING** - problèmes récupérables
- **ERROR** - échecs nécessitant une intervention
- **CRITICAL** - défaillances au niveau système

## Pièges courants {#gotchas}

- `depends_on` ne contrôle que l'ordre de démarrage, pas la disponibilité : l'application peut échouer si la base de données n'est pas encore prête
- Montez les fichiers statiques et les panneaux d'administration APRÈS l'initialisation de `VersionedFastAPI`
- Hébergement gratuit (Render.com) : réglez workers=1 et utilisez BackgroundTasks à la place de Celery
- L'ordre des certificats dans le bundle SSL est important : domaine -> intermédiaire -> racine
- L'intégration Sentry fournit le suivi des erreurs avec les traces de pile et des statistiques de fréquence

## Voir aussi {#see-also}

- [[fastapi-fundamentals]] - concepts fondamentaux de FastAPI
- [[fastapi-caching-and-tasks]] - cache Redis, Celery
- [[devops/index]] - Docker, CI/CD, infrastructure
