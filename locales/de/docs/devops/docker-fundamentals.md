---
title: "Docker-Grundlagen"
category: concepts
tags: [devops, docker, containers, images, networking, volumes]
level: 2
source_sha256: 24a5692db2be29635796afa81a2bc64a9e2aaa884a2fb8ab199b1509894672b2
translation: machine
translated_at: '2026-10-24'
---
# Docker-Grundlagen {#docker-fundamentals}

Docker ist eine Plattform zum Bauen, Paketieren und Ausführen von Anwendungen in isolierten Containern, die sich den Kernel des Host-Betriebssystems teilen. Container sind leichter als VMs (MB statt GB, Startzeit in Sekunden statt Minuten) und bieten über Linux-Namespaces und cgroups eine Isolation auf Prozessebene.

## Architektur {#architecture}

- **Docker Daemon** (`dockerd`) - Hintergrunddienst, der Container, Images und Netzwerke verwaltet
- **Docker CLI** (`docker`) - Kommandozeilenclient, der über die REST API mit dem Daemon kommuniziert
- **containerd** - Container-Runtime, die unter dockerd den Lebenszyklus der Container verwaltet
- **runc** - OCI-konforme Low-Level-Runtime, die die Container tatsächlich erzeugt
- **Docker Hub** - standardmäßige öffentliche Registry für Container-Images

Images werden in `/var/lib/docker/` gespeichert. Der Daemon lauscht auf dem Unix-Socket `/var/run/docker.sock`.

## Container vs. VMs {#containers-vs-vms}

| Merkmal | Container | VM |
|---------|-----------|-----|
| Isolation | Prozessebene (geteilter Kernel) | Vollständiges OS (Hypervisor) |
| Startzeit | Sekunden | Minuten |
| Größe | MB | GB |
| Overhead | Minimal | Erheblich (Gast-OS) |
| Dichte | Hunderte pro Host | Dutzende pro Host |

## Container ausführen {#running-containers}

```bash
docker run nginx                              # foreground (attached)
docker run -d nginx                           # background (detached)
docker run -d --name web nginx                # custom name
docker run -d -p 8080:80 nginx               # port mapping host:container
docker run -it ubuntu /bin/bash               # interactive + TTY
docker run --rm nginx echo "hello"            # auto-remove after exit
docker run -d -e MYSQL_ROOT_PASSWORD=secret mysql:8  # env var
docker run -d -v /host/path:/container/path nginx    # volume mount
docker run -d --restart=always nginx          # restart policy
```

### Port-Mapping {#port-mapping}

Mehrere Container können denselben Container-Port freigeben, müssen dabei aber unterschiedliche Host-Ports verwenden:
```bash
docker run -d -p 3000:80 --name app1 nginx
docker run -d -p 3001:80 --name app2 nginx
```

### Restart-Policies {#restart-policies}

- `no` (Standard) - niemals neu starten
- `always` - bei jedem Beenden neu starten, auch nach einem Neustart des Systems
- `unless-stopped` - wie `always`, aber nicht nach einem manuellen Stopp
- `on-failure[:N]` - nur bei einem Exit-Code ungleich null neu starten, optional mit maximaler Anzahl an Versuchen

## Lebenszyklus eines Containers {#container-lifecycle}

```bash
docker ps                    # list running
docker ps -a                 # list all (including stopped)
docker stop <name|id>        # graceful (SIGTERM, then SIGKILL after 10s)
docker start <name|id>       # start stopped container
docker restart <name|id>     # stop + start
docker kill <name|id>        # force stop (SIGKILL immediately)
docker rm <name|id>          # remove stopped container
docker rm -f <name|id>       # force remove running
docker rm $(docker ps -aq)   # remove all stopped
```

### Container inspizieren {#inspecting-containers}

```bash
docker exec -it <name> /bin/bash   # shell into container
docker exec <name> ls /app         # single command
docker logs <name>                 # stdout/stderr
docker logs -f <name>              # follow logs (live)
docker logs --tail 100 <name>      # last 100 lines
docker inspect <name>              # full metadata (JSON)
docker stats                       # live resource usage
docker top <name>                  # processes in container
```

## Docker-Images {#docker-images}

Images sind schreibgeschützte, geschichtete Vorlagen. Jede Anweisung im Dockerfile erzeugt eine Schicht. Schichten werden gecacht, sodass nur geänderte Schichten neu gebaut werden.

```bash
docker images                   # list local images
docker pull nginx:1.25          # download
docker image inspect nginx      # metadata
docker image history nginx      # layer history
docker tag myapp:latest myapp:v1.0   # create tag
docker rmi nginx:1.25           # remove image
docker image prune -a           # remove ALL unused images
```

Verwende in Produktivumgebungen immer konkrete Tags. `latest` ist lediglich eine Konvention und nicht zwingend die neueste Version.

## Volumes und Datenpersistenz {#volumes-and-data-persistence}

Container sind flüchtig: Beim Entfernen gehen die Daten verloren. Volumes speichern Daten dauerhaft.

```bash
# Named volume (Docker-managed)
docker volume create mydata
docker run -d -v mydata:/var/lib/mysql mysql

# Bind mount (host directory)
docker run -d -v $(pwd)/html:/usr/share/nginx/html nginx

# Volume management
docker volume ls
docker volume inspect mydata
docker volume rm mydata
docker volume prune            # remove unused
```

**Schreibbare Schicht**: Jeder Container besitzt eine eigene schreibbare Schicht (Copy-on-Write). Änderungen gehen beim Entfernen verloren. Volumes umgehen diese Schicht.

**Muster für Datenbank-Upgrades**: Ein benanntes Volume mit den Datenbankdaten übersteht den Austausch des Containers. Dazu wird eine neuere Image-Version mit demselben Volume gestartet.

## Docker-Netzwerke {#docker-networking}

```bash
docker network ls
docker network create mynet
docker run -d --network mynet --name app1 nginx
docker run -d --network mynet --name app2 nginx
# app1 and app2 communicate by name (DNS resolution)
```

| Typ | Beschreibung |
|-----|--------------|
| bridge | Standard. Kommunikation zwischen Containern auf demselben Host. Eigene Bridges ermöglichen DNS-Auflösung über den Namen |
| host | Teilt das Netzwerk des Hosts. Kein Port-Mapping nötig |
| none | Keine Netzwerkanbindung. Vollständig isoliert |
| overlay | Multi-Host (Docker Swarm) |

**Standard-Bridge**: Container kommunizieren nur über IP-Adressen, nicht über Namen. **Eigene Bridge**: DNS-Auflösung über den Container-Namen. Empfohlen für Anwendungen aus mehreren Containern.

## Aufräumen {#cleanup}

```bash
docker system prune              # stopped containers + unused networks + dangling images
docker system prune -a           # also unused images
docker system prune --volumes    # also unused volumes
docker system df                 # disk usage
```

## Fallstricke {#gotchas}

- `EXPOSE` im Dockerfile dient nur der Dokumentation und veröffentlicht den Port nicht. Verwende `-p` zur Laufzeit
- `localhost` innerhalb eines Containers verweist auf DIESEN Container, nicht auf den Host. Verwende in eigenen Netzwerken die Container-Namen
- Das Standard-Bridge-Netzwerk bietet keine DNS-Auflösung über Namen. Lege daher immer eigene Netzwerke an
- `docker cp` ist eine einmalige Kopie und keine Synchronisation. Verwende für kontinuierliche Synchronisation während der Entwicklung Bind Mounts
- Alpine-Images verwenden musl libc. Bei C-Erweiterungen (Python, native Node-Module) können Kompatibilitätsprobleme auftreten

## Siehe auch {#see-also}

- [[dockerfile-and-image-building]] - Dockerfile-Syntax, Multi-Stage-Builds, Optimierung
- [[docker-compose]] - Orchestrierung mehrerer Container
- [[docker-for-ml]] - Docker-Muster speziell für ML
- [[kubernetes-architecture]] - Container-Orchestrierung im großen Maßstab
