---
title: "Docker-Grundlagen"
category: reference
tags: [linux-cli, docker, containers, images, volumes, devops]
level: 3
source_sha256: 204a8f29a0f9b080b9d93ca71d20a66325f0ca90203212ab5414dfe8f072d6a1
translation: machine
translated_at: '2026-10-24'
---
# Docker-Grundlagen {#docker-basics}

Docker verpackt Anwendungen in Container – isolierte, portable Laufzeitumgebungen, die aus Images erstellt werden. Dieser Eintrag behandelt Images, Container, Volumes, Dockerfiles und gängige betriebliche Muster.

## Kernkonzepte {#core-concepts}

| Konzept | Beschreibung |
|---------|--------------|
| **Image** | Unveränderliche Vorlage für Container. Wird in Registries gespeichert. |
| **Container** | Laufende Instanz eines Images. Kann gestartet/gestoppt/gelöscht werden. |
| **Volume** | Persistenter Speicher außerhalb des Container-Dateisystems. Übersteht `docker rm`. |
| **Registry** | Image-Repository (Docker Hub, GHCR, privat). |

Image-Benennung: `[registry/][namespace/]name[:tag]` (z. B. `nginx:latest`, `ghcr.io/org/repo:v1.2`)

## Images {#images}

```bash
docker pull ubuntu:20.04              # pull specific version
docker images                         # list local images
docker rmi ubuntu:20.04               # remove image
docker image prune                    # remove dangling images
docker image prune -a                 # remove ALL unused images
```

## Container {#containers}

### Ausführen {#run}

```bash
docker run ubuntu echo "hello"        # run command and exit
docker run -it ubuntu /bin/bash       # interactive terminal
docker run -d -p 8080:80 --name web nginx  # detached, port mapping
docker run --rm -it ubuntu bash       # auto-remove on exit
docker run -e KEY=VALUE myapp         # with env variable
docker run -v /host:/container image  # bind mount
docker run -v myvolume:/data image    # named volume
```

Wichtige Flags: `-i` (interaktiv), `-t` (TTY), `-d` (detach), `--rm` (automatisch entfernen), `--name` (Name), `-p` (Port), `-v` (Volume), `-e` (Umgebungsvariable)

### Lebenszyklus {#lifecycle}

```bash
docker ps                             # running containers
docker ps -a                          # all containers
docker stop container                 # graceful stop
docker kill container                 # force stop
docker start container                # start stopped
docker restart container
docker rm container                   # remove stopped
docker rm -f container                # force remove
docker container prune                # remove all stopped
```

### Interaktion {#interact}

```bash
docker exec -it container bash        # shell in running container
docker exec container ls /app         # run command
docker logs container                 # view stdout/stderr
docker logs -f container              # follow logs
docker logs --tail 100 container      # last 100 lines
docker inspect container              # detailed JSON info
docker stats container                # live resource usage
docker top container                  # processes inside
docker cp file.txt container:/path/   # copy to container
docker cp container:/path/file.txt ./ # copy from container
```

## Volumes {#volumes}

### Benannte Volumes {#named-volumes}

```bash
docker volume create myvol
docker volume ls
docker volume inspect myvol
docker volume rm myvol
docker volume prune                   # remove unused
```

### Bind Mounts {#bind-mounts}

```bash
docker run -v /host/path:/container/path image
docker run -v $(pwd):/app image           # mount current dir
docker run -v $(pwd):/app:ro image        # read-only
```

## Dockerfile {#dockerfile}

```dockerfile
FROM ubuntu:20.04
WORKDIR /app
COPY . .
COPY requirements.txt /app/
RUN apt-get update && apt-get install -y python3 pip
RUN pip install -r requirements.txt
ENV PORT=8080
EXPOSE 8080
CMD ["python3", "app.py"]

# ENTRYPOINT + CMD pattern
ENTRYPOINT ["python3"]
CMD ["app.py"]     # default arg, overridable
```

### Build {#build}

```bash
docker build -t myapp:latest .
docker build -t myapp:1.0 -f Dockerfile.prod .
docker tag myapp:latest registry/myapp:1.0
docker push registry/myapp:1.0
```

## Bereinigung {#cleanup}

```bash
docker container prune                # stopped containers
docker image prune -a                 # unused images
docker volume prune                   # unused volumes
docker network prune                  # unused networks
docker system prune -a --volumes      # EVERYTHING unused
docker system df                      # disk usage
```

## Muster {#patterns}

```bash
# Stop all running containers
docker stop $(docker ps -q)

# Remove all containers
docker rm $(docker ps -aq)

# Remove all images
docker rmi $(docker images -q)

# Enter running container by name filter
docker exec -it $(docker ps -q -f name=myapp) bash
```

### Reihenfolge beim Löschen {#deletion-order}

Beim Entfernen eines Images mit zugehörigen Containern:
1. `docker stop container` – stoppen
2. `docker rm container` – Container entfernen
3. `docker rmi image` – Image entfernen

## Stolpersteine {#gotchas}

- Das Container-Dateisystem ist flüchtig – Daten gehen bei `docker rm` verloren, sofern keine Volumes verwendet werden
- `EXPOSE` im Dockerfile ist nur Dokumentation – der Port wird dadurch NICHT veröffentlicht; verwende zur Laufzeit `-p`
- `CMD` wird durch Argumente von `docker run` überschrieben, `ENTRYPOINT` hingegen nicht (zum Überschreiben `--entrypoint` verwenden)
- Anonyme Volumes erhalten zufällige Namen und sind schwer zu verwalten – benannte Volumes bevorzugen
- `docker system prune` entfernt KEINE benannten Volumes – dafür das Flag `--volumes` ergänzen
- Der Build-Kontext (`.`) umfasst alle Dateien im aktuellen Verzeichnis – große Dateien mit `.dockerignore` ausschließen

## Siehe auch {#see-also}

- [[disks-and-filesystems]] – Mount-Befehle, Gerätedateien
- [[process-management]] – Prozesse in Containern
- [[linux-security]] – Namespaces, Isolation
