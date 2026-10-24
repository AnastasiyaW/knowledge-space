---
title: "Docker für Data Engineering"
category: tools
tags: [data-engineering, docker, containers, devops, deployment]
level: 3
source_sha256: 09bf5b78b5d3bca142a4e7b5130250094f7b27224727663eabe1a5e9befb62e6
translation: machine
translated_at: '2026-10-24'
---
# Docker für Data Engineering {#docker-for-data-engineering}

Docker stellt isolierte, reproduzierbare Umgebungen für Data-Engineering-Workloads bereit. Container bündeln Anwendungen mit ihren Abhängigkeiten und sorgen so für identische Dev-, Test- und Produktionsumgebungen.

## Container vs. VMs {#containers-vs-vms}

| Merkmal | Container | VMs |
|---------|-----------|-----|
| Betriebssystem | Teilen den Kernel des Hosts | Vollständiges Gast-Betriebssystem |
| Gewicht | Leichtgewichtig | Schwergewichtig |
| Startzeit | Sekunden | Minuten |
| IaC-Tools | Dockerfile, docker-compose | Vagrant |

## Grundlegende Konzepte {#core-concepts}
- **Image** - schreibgeschützte Vorlage (Blaupause)
- **Container** - laufende Instanz eines Images
- **Layer** - jede Dockerfile-Anweisung erzeugt einen gecachten Layer
- **Volume** - persistenter Speicher außerhalb des Container-Lebenszyklus
- **Registry** - Speicher für Images (Docker Hub, privat)

## Wichtige Befehle {#essential-commands}

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

## Dockerfile {#dockerfile}

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "etl.py"]
```

## Docker Compose {#docker-compose}

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

## Best Practices {#best-practices}
- **1 Anwendung = 1 Container**
- Konfiguration über **Umgebungsvariablen** (keine Rebuilds bei Konfigurationsänderungen)
- **Persistente Daten auf Volumes** (Neustarts des Containers führen nicht zu Datenverlust)
- Passwörter niemals im Dockerfile oder in docker-compose.yml speichern

## Stolperfallen {#gotchas}
- Änderungen an Umgebungsvariablen: `docker compose restart` reicht NICHT aus – es muss gestoppt, entfernt (rm) und neu gestartet (up) werden
- Build-Kontext: im Verzeichnis des Dockerfiles nur die notwendigen Dateien belassen
- Windows/Mac: Docker läuft in einer Linux-VM (WSL2 oder VirtualBox)
- Nach Änderungen an Umgebungsvariablen in docker-compose.yml ist eine vollständige Neuerstellung erforderlich

## Siehe auch {#see-also}
- [[kubernetes-for-de]] - Container-Orchestrierung im großen Maßstab
- [[cloud-data-platforms]] - Cloud-Deployment
- [[apache-airflow]] - Airflow in Docker
